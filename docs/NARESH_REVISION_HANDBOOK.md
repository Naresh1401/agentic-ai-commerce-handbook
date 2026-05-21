# Naresh Revision Handbook

This handbook is written in first person so I can revise it quickly before interviews and before joining the pod.

## My Role Narrative

I am a backend and AI integration developer who can build secure API-first systems, integrate third-party platforms, and expose business capabilities to AI agents through structured tool contracts. This job is asking for the same intersection: production-grade REST APIs, commerce orchestration, enterprise auth, partner integrations, MCP interfaces, and quality engineering for agentic workflows.

My strongest positioning:

- I can build RESTful APIs with clear OpenAPI contracts.
- I understand OAuth/JWT-style access patterns, RBAC, scopes, API keys, and tenant isolation.
- I have worked with multi-service integration and orchestration patterns.
- I understand agentic workflows where agents call tools/APIs and need schemas, guardrails, and observability.
- I can move from POC to production by adding tests, telemetry, auth, deployment practices, and repeatable integration patterns.

## Skill Stack I Need To Revise

### 1. API-First Backend Engineering

What I should know:

- REST resource modeling: products, carts, quotes, orders, payments, fulfillments.
- HTTP methods: `GET`, `POST`, `PATCH`, `DELETE`.
- Status codes: `200`, `201`, `202`, `400`, `401`, `403`, `404`, `409`, `422`, `429`, `500`.
- OpenAPI contracts, examples, versioning, and deprecation.
- Pagination, filtering, idempotency, error models, correlation IDs.

How I explain it:

> API-first means the contract is not an afterthought. I define request and response schemas, auth requirements, error models, examples, and lifecycle expectations so partners and agents can consume the service predictably.

### 2. Authentication And Authorization

What I should know:

- Authentication proves who the caller is.
- Authorization decides what the caller can do.
- OAuth 2.0 client credentials is common for server-to-server partner access.
- JWTs carry claims such as `sub`, `iss`, `aud`, `exp`, `tenant_id`, and `scope`.
- API keys may identify partners but usually need stronger controls for sensitive flows.
- RBAC is role-based; ABAC uses attributes such as tenant, region, risk, or partner tier.

How I explain it:

> For partner APIs, I validate the token, confirm issuer and audience, enforce scopes at endpoint level, enforce tenant boundaries at object level, and log enough context for audits without leaking secrets.

### 3. Orchestration And Composition

What I should know:

- Orchestration centralizes business flow logic.
- Composition hides multiple downstream calls behind one stable API.
- Checkout may call catalog, inventory, pricing, payment, fulfillment, loyalty, and tax services.
- Failures must be planned: timeout, retry, fallback, compensation, outbox, and idempotency.

How I explain it:

> A partner should not need to call seven services to complete a business action. The orchestration layer owns the workflow and returns a cohesive business response.

### 4. MCP And Agent Tool Interfaces

What I should know:

- MCP connects AI applications to external systems through tools, data, and workflows.
- A safe tool has a narrow name, clear description, JSON schema, side-effect declaration, and authorization requirement.
- Read-only tools are safer than write tools.
- Payment, refund, cancellation, and account update tools need approval gates.
- Tool outputs should be structured, not prose-only.

How I explain it:

> I treat MCP tools like API endpoints exposed through an agent interface. The same security, validation, observability, and least-privilege rules apply.

### 5. Agentic Commerce, UCP, And AP2 Concepts

What I should know:

- Agentic commerce means AI agents help shoppers discover, decide, buy, and receive support.
- UCP is positioned as a common language for agents, businesses, and payment providers across the shopping journey.
- AP2 focuses on secure agent-performed payments using mandates, receipts, and verifiable authorization.
- In agentic payment flows, deterministic code must verify important claims even when an agent participates.

How I explain it:

> I do not need to memorize every protocol detail to contribute. I need to understand the architecture: agents need standardized commerce objects, merchants need verifiable intent, payment providers need proof of authorization, and APIs need strong contracts.

### 6. Third-Party Integration Patterns

What I should know:

- Adapter pattern isolates partner-specific formats and errors.
- Webhooks need signature verification, replay protection, idempotency, and event storage.
- Partner onboarding should be repeatable: sandbox credentials, contract tests, runbooks, rate limits.
- Avoid point-to-point integrations that spread partner logic everywhere.

How I explain it:

> I create a stable internal port and one adapter per partner. That lets the product flow remain stable while partner APIs evolve.

### 7. Quality Engineering For Agentic Systems

What I should know:

- Deterministic tests still matter: schemas, auth, idempotency, error handling, and adapter contracts.
- Agentic evals test tool selection, valid arguments, blocked unsafe actions, prompt injection attempts, and approval requirements.
- Golden path tests should be paired with adversarial tests.

How I explain it:

> I test the deterministic boundary around non-deterministic agents. Agents can vary wording, but they cannot bypass schemas, scopes, approvals, or side-effect policies.

## Commerce Vocabulary

- Catalog: product data and attributes.
- Product feed: structured product data shared with channels.
- Cart: selected items before checkout.
- Quote: price, tax, shipping, availability, and estimated total.
- Payment authorization: hold or approval from payment provider.
- Capture: actual movement of funds.
- Fulfillment: pick, pack, ship, deliver, or pickup.
- RMA: return merchandise authorization.
- Webhook: partner sends event to my API.
- Reconciliation: verifying internal records match partner/payment records.

## My Daily Revision Drill

1. Explain quote to checkout orchestration in two minutes.
2. Explain OAuth scopes and tenant checks in two minutes.
3. Draw an MCP tool contract for `commerce.quote`.
4. Explain how I would onboard a new partner.
5. Name five tests needed before production.
6. Review one project in this repo and run its tests.

