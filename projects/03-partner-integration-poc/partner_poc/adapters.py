from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal
from time import sleep
from typing import Any

from pydantic import BaseModel, Field


class NormalizedProduct(BaseModel):
    partner_id: str
    sku: str
    title: str
    price: Decimal
    currency: str = "USD"
    attributes: dict[str, Any] = Field(default_factory=dict)


class PartnerAdapter(ABC):
    partner_id: str

    @abstractmethod
    def normalize_product(self, payload: dict[str, Any]) -> NormalizedProduct:
        raise NotImplementedError


class ShopifyLikeAdapter(PartnerAdapter):
    partner_id = "shopify_like"

    def normalize_product(self, payload: dict[str, Any]) -> NormalizedProduct:
        variant = payload["variants"][0]
        return NormalizedProduct(
            partner_id=self.partner_id,
            sku=variant["sku"],
            title=payload["title"],
            price=Decimal(str(variant["price"])),
            attributes={"vendor": payload.get("vendor"), "source_product_id": payload.get("id")},
        )


class UcpLikeAdapter(PartnerAdapter):
    partner_id = "ucp_like"

    def normalize_product(self, payload: dict[str, Any]) -> NormalizedProduct:
        offer = payload["offers"][0]
        return NormalizedProduct(
            partner_id=self.partner_id,
            sku=payload["merchantSku"],
            title=payload["displayName"],
            price=Decimal(str(offer["price"]["amount"])),
            currency=offer["price"].get("currency", "USD"),
            attributes={"availability": offer.get("availability"), "journey": "discovery_to_checkout"},
        )


class PartnerRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, PartnerAdapter] = {
            "shopify_like": ShopifyLikeAdapter(),
            "ucp_like": UcpLikeAdapter(),
        }

    def adapter_for(self, partner_id: str) -> PartnerAdapter:
        return self._adapters[partner_id]

    def partner_ids(self) -> list[str]:
        return sorted(self._adapters)


@dataclass(frozen=True)
class RetryPolicy:
    attempts: int = 3
    delay_seconds: float = 0.01

    def run(self, operation: Callable[[], Any]) -> Any:
        last_error: Exception | None = None
        for attempt in range(1, self.attempts + 1):
            try:
                return operation()
            except TimeoutError as exc:
                last_error = exc
                if attempt < self.attempts:
                    sleep(self.delay_seconds)
        raise last_error or TimeoutError("operation failed")


class PartnerOnboardingRequest(BaseModel):
    partner_id: str
    contact_email: str
    auth_type: str = Field(pattern="^(oauth_client_credentials|api_key|mtls)$")
    sandbox_base_url: str
    target_flows: list[str] = Field(default_factory=lambda: ["catalog", "quote"])


class PartnerOnboardingRecord(BaseModel):
    partner_id: str
    status: str
    checklist: list[str]


class PartnerOnboardingService:
    def onboard(self, request: PartnerOnboardingRequest) -> PartnerOnboardingRecord:
        return PartnerOnboardingRecord(
            partner_id=request.partner_id,
            status="sandbox_ready",
            checklist=[
                "Collect sandbox credentials",
                "Validate auth handshake",
                "Map product and offer schema",
                "Configure webhook signing secret",
                "Run contract tests",
                "Document rate limits and retry rules",
            ],
        )

