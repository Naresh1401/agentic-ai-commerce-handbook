from fastapi.testclient import TestClient

from partner_poc.adapters import PartnerRegistry, RetryPolicy, ShopifyLikeAdapter, UcpLikeAdapter
from partner_poc.main import WEBHOOK_SECRET, app
from partner_poc.security import sign_webhook

client = TestClient(app)


def test_registry_lists_supported_partner_adapters() -> None:
    assert PartnerRegistry().partner_ids() == ["shopify_like", "ucp_like"]


def test_shopify_like_adapter_normalizes_product() -> None:
    product = ShopifyLikeAdapter().normalize_product(
        {
            "id": "gid://shopify/Product/1",
            "title": "Commerce Mug",
            "vendor": "Naresh Lab",
            "variants": [{"sku": "mug-001", "price": "9.50"}],
        }
    )

    assert product.sku == "mug-001"
    assert str(product.price) == "9.50"
    assert product.attributes["vendor"] == "Naresh Lab"


def test_ucp_like_adapter_normalizes_offer() -> None:
    product = UcpLikeAdapter().normalize_product(
        {
            "merchantSku": "coffee-001",
            "displayName": "Cincinnati Coffee",
            "offers": [{"price": {"amount": "12.99", "currency": "USD"}, "availability": "in_stock"}],
        }
    )

    assert product.partner_id == "ucp_like"
    assert product.attributes["journey"] == "discovery_to_checkout"


def test_webhook_requires_valid_signature() -> None:
    body = b'{"event":"product.updated"}'
    valid_signature = sign_webhook(WEBHOOK_SECRET, body)

    accepted = client.post(
        "/v1/webhooks/shopify_like",
        content=body,
        headers={"X-Partner-Signature": valid_signature, "Content-Type": "application/json"},
    )
    rejected = client.post(
        "/v1/webhooks/shopify_like",
        content=body,
        headers={"X-Partner-Signature": "bad-signature", "Content-Type": "application/json"},
    )

    assert accepted.status_code == 200
    assert rejected.status_code == 401


def test_retry_policy_retries_transient_timeout() -> None:
    calls = {"count": 0}

    def flaky_operation() -> str:
        calls["count"] += 1
        if calls["count"] < 2:
            raise TimeoutError("partner timeout")
        return "ok"

    assert RetryPolicy(attempts=2).run(flaky_operation) == "ok"
    assert calls["count"] == 2
