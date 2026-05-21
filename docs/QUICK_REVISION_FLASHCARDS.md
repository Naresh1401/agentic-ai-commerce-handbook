# Quick Revision Flashcards

Q: What is API-first development?
A: Define the contract, schemas, errors, auth, and lifecycle before or alongside implementation so consumers can integrate predictably.

Q: What is orchestration?
A: A business flow layer that composes multiple downstream services into one cohesive operation.

Q: What is idempotency?
A: A guarantee that repeating the same request with the same key does not duplicate side effects.

Q: What is MCP?
A: A standard way for AI applications to connect to tools, data, and workflows exposed by external systems.

Q: What makes an MCP tool safe?
A: Narrow scope, schema validation, required auth, side-effect declaration, structured output, logging, and approval for risky actions.

Q: What is UCP?
A: A Universal Commerce Protocol concept for giving agents, businesses, and payment providers a common commerce language across the shopping journey.

Q: What is AP2?
A: Agent Payments Protocol, focused on secure agent-performed payments using authorization mandates and receipts.

Q: What is BOLA?
A: Broken object level authorization, where one caller can access another user's object by changing an identifier.

Q: How do I avoid brittle integrations?
A: Use stable internal ports, partner adapters, contract tests, retry/timeout policies, and onboarding playbooks.

Q: How do I test agentic variability?
A: Test deterministic boundaries and run eval cases for tool selection, argument validity, unsafe prompt resistance, and approval gates.

