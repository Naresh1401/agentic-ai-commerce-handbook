from dataclasses import dataclass
from decimal import Decimal
import json
import sys
from typing import Any, Literal

from pydantic import BaseModel, Field, ValidationError


class SearchProductsArgs(BaseModel):
    query: str = Field(min_length=2, max_length=80)
    max_results: int = Field(default=5, ge=1, le=10)


class QuoteArgs(BaseModel):
    sku: str
    quantity: int = Field(gt=0, le=25)
    destination_zip: str = Field(min_length=5, max_length=10)


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    input_schema: dict[str, Any]
    side_effects: Literal["none", "writes_data", "external_payment"]
    required_scope: str


PRODUCTS = {
    "coffee-001": {"title": "Cincinnati Blend Coffee", "price": Decimal("12.99")},
    "mug-002": {"title": "Agentic Commerce Mug", "price": Decimal("9.50")},
    "hoodie-003": {"title": "API-First Hoodie", "price": Decimal("39.00")},
}


class CommerceToolServer:
    def list_tools(self) -> list[dict[str, Any]]:
        tools = [
            ToolDefinition(
                name="catalog.search",
                description="Search catalog products by title or SKU. No side effects.",
                input_schema=SearchProductsArgs.model_json_schema(),
                side_effects="none",
                required_scope="catalog:read",
            ),
            ToolDefinition(
                name="commerce.quote",
                description="Create a non-binding quote for one SKU. No payment or fulfillment side effects.",
                input_schema=QuoteArgs.model_json_schema(),
                side_effects="none",
                required_scope="quote:write",
            ),
        ]
        return [tool.__dict__ for tool in tools]

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name == "catalog.search":
            args = SearchProductsArgs.model_validate(arguments)
            query = args.query.lower()
            matches = [
                {"sku": sku, "title": product["title"], "price": str(product["price"])}
                for sku, product in PRODUCTS.items()
                if query in sku.lower() or query in str(product["title"]).lower()
            ]
            return {"products": matches[: args.max_results]}

        if name == "commerce.quote":
            args = QuoteArgs.model_validate(arguments)
            product = PRODUCTS.get(args.sku)
            if product is None:
                return {"available": False, "reason": "SKU not found"}
            subtotal = product["price"] * args.quantity
            tax = (subtotal * Decimal("0.075")).quantize(Decimal("0.01"))
            shipping = Decimal("4.99")
            return {
                "available": True,
                "sku": args.sku,
                "subtotal": str(subtotal),
                "tax": str(tax),
                "shipping": str(shipping),
                "total": str(subtotal + tax + shipping),
            }

        raise ValueError(f"Unknown tool: {name}")

    def handle_jsonrpc(self, request: dict[str, Any]) -> dict[str, Any]:
        request_id = request.get("id")
        try:
            method = request["method"]
            params = request.get("params", {})
            if method == "tools/list":
                result = {"tools": self.list_tools()}
            elif method == "tools/call":
                result = self.call_tool(params["name"], params.get("arguments", {}))
            else:
                raise ValueError(f"Unsupported method: {method}")
            return {"jsonrpc": "2.0", "id": request_id, "result": result}
        except (KeyError, ValueError, ValidationError) as exc:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32602, "message": str(exc)},
            }


def main() -> None:
    server = CommerceToolServer()
    for line in sys.stdin:
        response = server.handle_jsonrpc(json.loads(line))
        print(json.dumps(response), flush=True)


if __name__ == "__main__":
    main()

