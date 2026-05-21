# Interview Playbook

## Tell Me About Yourself

I am a backend and AI integration developer focused on secure APIs, orchestration, and agentic workflows. My experience includes REST APIs, OAuth/JWT-style authorization, third-party integrations, MCP-style tool exposure, and production hardening. This role is exciting because it combines API-first engineering, commerce integration, and agentic AI into one pod.

## Explain An Agentic Commerce Architecture

An agentic commerce system has an agent-facing layer, a contract layer, and deterministic backend services. The agent may ask for product discovery, quote, or checkout, but the backend validates every request using schemas, auth scopes, tenant checks, idempotency, and approval rules. The commerce orchestrator composes product, inventory, pricing, payment, fulfillment, and partner systems into one stable workflow.

## How Would You Design A Partner-Ready Checkout API?

I would design versioned endpoints for quote and checkout. Quote is read or low-risk and returns price, tax, shipping, and availability. Checkout is a write operation and needs an idempotency key, stronger scope, payment token, and clear error responses. Downstream calls would go through adapters so partner-specific code does not leak into the API contract.

## How Would You Build An MCP Server For Existing APIs?

I would start with safe read-only tools such as `catalog.search` and `commerce.quote`. Each tool gets a name, description, JSON input schema, output schema, required scopes, and side-effect level. The server validates input, calls the existing API/orchestrator, and returns structured results. Write tools such as checkout require stricter scopes and human approval.

## How Would You Test Agentic Workflows?

I would test deterministic boundaries first: schemas, scopes, tenant isolation, idempotency, and partner contracts. Then I would add evals for agent behavior: correct tool selection, valid arguments, refusal of unsafe requests, prompt-injection resistance, and approval-gate enforcement for side-effecting actions.

## How Would You Move A Partner POC To Production?

I would add contract tests, authentication, rate limits, retry/timeout policies, idempotency, webhook verification, structured logging, metrics, traces, secrets management, CI/CD, and runbooks. I would also document the onboarding steps so the next partner is faster.

## Questions To Ask The Interviewer

- Which commerce flows are first priority: discovery, quote, checkout, post-purchase, or partner onboarding?
- Are you building MCP servers directly or shim layers in front of existing APIs?
- What identity provider and API gateway patterns are standard in the environment?
- Which partner ecosystems are most important for the first POCs?
- How does the pod define POC success versus production readiness?
- What is the current testing strategy for agentic variability and tool calls?

