from decimal import Decimal
from typing import Annotated, Any, Callable, Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Partner-Ready Agentic Commerce API",
    version="1.0.0",
    description="REST commerce API with orchestration, scoped auth, idempotency, and MCP tool shim.",
)

bearer = HTTPBearer(auto_error=False)


class Principal(BaseModel):
    subject: str
    tenant_id: str
    scopes: set[str]


TOKENS = {
    "naresh-partner-token": Principal(
        subject="partner-client",
        tenant_id="tenant_cincinnati",
        scopes={"catalog:read", "quote:write", "order:write", "tools:invoke"},
    ),
    "naresh-analyst-token": Principal(
        subject="analyst",
        tenant_id="tenant_cincinnati",
        scopes={"catalog:read", "quote:write"},
    ),
}


def principal_from_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> Principal:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    principal = TOKENS.get(credentials.credentials)
    if principal is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bearer token")
    return principal


def require_scope(scope: str) -> Callable[[Principal], Principal]:
    def dependency(principal: Annotated[Principal, Depends(principal_from_token)]) -> Principal:
        if scope not in principal.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"message": "Insufficient scope", "required_scope": scope},
            )
        return principal

    return dependency


class Product(BaseModel):
    sku: str
    title: str
    price: Decimal
    inventory: int


class LineItem(BaseModel):
    sku: str
    quantity: int = Field(gt=0, le=25)


class QuoteRequest(BaseModel):
    customer_id: str
    items: list[LineItem] = Field(min_length=1, max_length=10)
    destination_zip: str = Field(min_length=5, max_length=10)

    @field_validator("customer_id")
    @classmethod
    def customer_id_must_be_contract_safe(cls, value: str) -> str:
        if not value.startswith("cust_"):
            raise ValueError("customer_id must start with cust_")
        return value

    @field_validator("destination_zip")
    @classmethod
    def zip_must_start_numeric(cls, value: str) -> str:
        if not value[:5].isdigit():
            raise ValueError("destination_zip must start with five digits")
        return value


class QuoteLine(BaseModel):
    sku: str
    quantity: int
    unit_price: Decimal
    available: bool

    @property
    def extended_price(self) -> Decimal:
        return self.unit_price * self.quantity


class QuoteResponse(BaseModel):
    quote_id: str
    subtotal: Decimal
    tax: Decimal
    shipping: Decimal
    total: Decimal
    lines: list[QuoteLine]
    warnings: list[str] = []


class PaymentMethod(BaseModel):
    token: str = Field(min_length=8)
    brand: str = "demo-card"


class CheckoutRequest(QuoteRequest):
    payment_method: PaymentMethod


class CheckoutResponse(BaseModel):
    order_id: str
    status: Literal["accepted"]
    authorization_id: str
    quote: QuoteResponse


PRODUCTS = {
    "coffee-001": Product(
        sku="coffee-001", title="Cincinnati Blend Coffee", price=Decimal("12.99"), inventory=50
    ),
    "mug-002": Product(
        sku="mug-002", title="Agentic Commerce Mug", price=Decimal("9.50"), inventory=8
    ),
    "hoodie-003": Product(
        sku="hoodie-003", title="API-First Hoodie", price=Decimal("39.00"), inventory=0
    ),
}

IDEMPOTENCY_STORE: dict[str, CheckoutResponse] = {}


class CommerceOrchestrator:
    tax_rate = Decimal("0.075")

    def quote(self, request: QuoteRequest, principal: Principal) -> QuoteResponse:
        if principal.tenant_id != "tenant_cincinnati":
            raise HTTPException(status_code=403, detail="Tenant denied")

        lines: list[QuoteLine] = []
        warnings: list[str] = []
        for item in request.items:
            product = PRODUCTS.get(item.sku)
            if product is None:
                warnings.append(f"{item.sku} not found")
                lines.append(
                    QuoteLine(sku=item.sku, quantity=item.quantity, unit_price=Decimal("0.00"), available=False)
                )
                continue

            available = product.inventory >= item.quantity
            if not available:
                warnings.append(f"{item.sku} has insufficient inventory")
            lines.append(
                QuoteLine(
                    sku=item.sku,
                    quantity=item.quantity,
                    unit_price=product.price,
                    available=available,
                )
            )

        subtotal = sum((line.extended_price for line in lines), Decimal("0.00"))
        tax = (subtotal * self.tax_rate).quantize(Decimal("0.01"))
        shipping = Decimal("0.00") if subtotal >= Decimal("50.00") else Decimal("4.99")
        return QuoteResponse(
            quote_id=f"quote_{uuid4().hex[:10]}",
            subtotal=subtotal,
            tax=tax,
            shipping=shipping,
            total=subtotal + tax + shipping,
            lines=lines,
            warnings=warnings,
        )

    def checkout(self, request: CheckoutRequest, principal: Principal) -> CheckoutResponse:
        quote = self.quote(request, principal)
        if any(not line.available for line in quote.lines):
            raise HTTPException(status_code=409, detail={"message": "Inventory unavailable", "quote": quote.model_dump(mode="json")})
        return CheckoutResponse(
            order_id=f"order_{uuid4().hex[:10]}",
            status="accepted",
            authorization_id=f"auth_{request.payment_method.token[-4:]}",
            quote=quote,
        )


class ToolInvocation(BaseModel):
    name: Literal["commerce.quote"]
    arguments: dict[str, Any]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/products", response_model=list[Product])
def list_products(_: Principal = Depends(require_scope("catalog:read"))) -> list[Product]:
    return list(PRODUCTS.values())


@app.post("/v1/quotes", response_model=QuoteResponse)
def create_quote(
    request: QuoteRequest,
    principal: Principal = Depends(require_scope("quote:write")),
) -> QuoteResponse:
    return CommerceOrchestrator().quote(request, principal)


@app.post("/v1/orders", response_model=CheckoutResponse)
def create_order(
    request: CheckoutRequest,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    principal: Principal = Depends(require_scope("order:write")),
) -> CheckoutResponse:
    if idempotency_key in IDEMPOTENCY_STORE:
        return IDEMPOTENCY_STORE[idempotency_key]
    response = CommerceOrchestrator().checkout(request, principal)
    IDEMPOTENCY_STORE[idempotency_key] = response
    return response


@app.get("/mcp/tools")
def list_agent_tools(_: Principal = Depends(require_scope("tools:invoke"))) -> dict[str, list[dict[str, Any]]]:
    return {
        "tools": [
            {
                "name": "commerce.quote",
                "description": "Create a non-binding quote for commerce items. No payment or fulfillment side effects.",
                "input_schema": QuoteRequest.model_json_schema(),
                "side_effects": "none",
                "required_scope": "tools:invoke",
            }
        ]
    }


@app.post("/mcp/invoke")
def invoke_agent_tool(
    invocation: ToolInvocation,
    principal: Principal = Depends(require_scope("tools:invoke")),
) -> dict[str, Any]:
    request = QuoteRequest.model_validate(invocation.arguments)
    quote = CommerceOrchestrator().quote(request, principal)
    return {"tool": invocation.name, "result": quote.model_dump(mode="json")}

