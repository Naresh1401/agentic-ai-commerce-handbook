from fastapi.testclient import TestClient

from commerce_api.main import app

client = TestClient(app)


def headers(token: str = "naresh-partner-token") -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_products_require_authentication() -> None:
    response = client.get("/v1/products")
    assert response.status_code == 401


def test_quote_composes_catalog_inventory_pricing_tax_and_shipping() -> None:
    response = client.post(
        "/v1/quotes",
        headers=headers(),
        json={
            "customer_id": "cust_100",
            "items": [{"sku": "coffee-001", "quantity": 2}],
            "destination_zip": "45202",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["subtotal"] == "25.98"
    assert body["tax"] == "1.95"
    assert body["shipping"] == "4.99"
    assert body["total"] == "32.92"


def test_order_requires_write_scope() -> None:
    response = client.post(
        "/v1/orders",
        headers={**headers("naresh-analyst-token"), "Idempotency-Key": "no-write"},
        json={
            "customer_id": "cust_100",
            "items": [{"sku": "coffee-001", "quantity": 1}],
            "destination_zip": "45202",
            "payment_method": {"token": "tok_12345678"},
        },
    )
    assert response.status_code == 403


def test_order_is_idempotent() -> None:
    payload = {
        "customer_id": "cust_100",
        "items": [{"sku": "coffee-001", "quantity": 1}],
        "destination_zip": "45202",
        "payment_method": {"token": "tok_12345678"},
    }
    request_headers = {**headers(), "Idempotency-Key": "same-order-key"}
    first = client.post("/v1/orders", headers=request_headers, json=payload)
    second = client.post("/v1/orders", headers=request_headers, json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["order_id"] == second.json()["order_id"]


def test_mcp_quote_tool_exposes_schema_and_structured_result() -> None:
    manifest = client.get("/mcp/tools", headers=headers())
    assert manifest.status_code == 200
    assert manifest.json()["tools"][0]["side_effects"] == "none"

    response = client.post(
        "/mcp/invoke",
        headers=headers(),
        json={
            "name": "commerce.quote",
            "arguments": {
                "customer_id": "cust_100",
                "items": [{"sku": "mug-002", "quantity": 1}],
                "destination_zip": "45202",
            },
        },
    )
    assert response.status_code == 200
    assert response.json()["result"]["total"] == "15.20"

