# Project 03: Partner Integration POC

This project shows how to operationalize third-party integrations without brittle point-to-point code.

It includes:

- Partner adapter interface
- Shopify-like and UCP-like adapters
- Normalized internal commerce product model
- HMAC webhook signature verification
- Retry policy for transient partner failures
- Partner onboarding API

Run:

```bash
uvicorn partner_poc.main:app --reload --app-dir projects/03-partner-integration-poc --port 8001
```

