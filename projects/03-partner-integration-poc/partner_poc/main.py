from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request

from partner_poc.adapters import (
    NormalizedProduct,
    PartnerOnboardingRecord,
    PartnerOnboardingRequest,
    PartnerOnboardingService,
    PartnerRegistry,
)
from partner_poc.security import verify_webhook_signature

app = FastAPI(
    title="Partner Integration POC",
    version="1.0.0",
    description="Adapter-based partner integration POC with webhook verification and onboarding.",
)

WEBHOOK_SECRET = "local-demo-secret"
registry = PartnerRegistry()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/partners")
def partners() -> dict[str, list[str]]:
    return {"partners": registry.partner_ids()}


@app.post("/v1/partners/onboard", response_model=PartnerOnboardingRecord)
def onboard_partner(request: PartnerOnboardingRequest) -> PartnerOnboardingRecord:
    return PartnerOnboardingService().onboard(request)


@app.post("/v1/partners/{partner_id}/normalize-product", response_model=NormalizedProduct)
def normalize_product(partner_id: str, payload: dict[str, Any]) -> NormalizedProduct:
    try:
        adapter = registry.adapter_for(partner_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Unknown partner") from exc
    return adapter.normalize_product(payload)


@app.post("/v1/webhooks/{partner_id}")
async def receive_webhook(
    partner_id: str,
    request: Request,
    x_partner_signature: str = Header(...),
) -> dict[str, str]:
    body = await request.body()
    if not verify_webhook_signature(WEBHOOK_SECRET, body, x_partner_signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    return {"status": "accepted", "partner_id": partner_id}

