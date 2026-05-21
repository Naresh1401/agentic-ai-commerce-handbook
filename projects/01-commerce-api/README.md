# Project 01: Partner-Ready Commerce API

This project demonstrates the core JD responsibilities:

- Secure REST APIs
- API-first request/response contracts
- Auth scopes and tenant checks
- Quote and checkout orchestration
- Idempotency for write operations
- MCP-style tool exposure for agents

Run:

```bash
uvicorn commerce_api.main:app --reload --app-dir projects/01-commerce-api
```

Try:

```bash
curl -H "Authorization: Bearer naresh-partner-token" http://127.0.0.1:8000/v1/products
```

