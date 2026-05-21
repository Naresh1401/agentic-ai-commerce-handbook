# Agentic AI Commerce Handbook And Project Portfolio

This repo is a revision handbook and hands-on project portfolio for Naresh Sampangi preparing for an **Agentic AI API Developer - Agentic Commerce & 3rd-Party Integrations** role.

It connects the resume proof points to the job description and gives runnable code projects for the skills the role expects:

- Secure RESTful commerce APIs
- API-first OpenAPI thinking
- OAuth/JWT-style scopes, tenant checks, and authorization boundaries
- API orchestration and composition across downstream services
- MCP-style tool server interfaces for agents
- Third-party partner integration patterns
- UCP/AP2-inspired agentic commerce concepts
- AI/agentic testing beyond deterministic unit tests
- POC to production hardening

## Repo Structure

```text
docs/
  NARESH_REVISION_HANDBOOK.md
  RESUME_TO_JD_SKILL_MAP.md
  INTERVIEW_PLAYBOOK.md
  QUICK_REVISION_FLASHCARDS.md
  30_60_90_DAY_PLAN.md
  RESOURCES.md
projects/
  01-commerce-api/              FastAPI commerce API + orchestration + MCP shim
  02-mcp-tool-server/           JSON-RPC MCP-style tool server
  03-partner-integration-poc/   Partner adapter, webhook, retry, onboarding POC
  04-agentic-quality-evals/     Agent tool-call eval and guardrail harness
```

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Run the commerce API:

```bash
uvicorn commerce_api.main:app --reload --app-dir projects/01-commerce-api
```

Run the partner POC API:

```bash
uvicorn partner_poc.main:app --reload --app-dir projects/03-partner-integration-poc --port 8001
```

Run the eval harness:

```bash
python projects/04-agentic-quality-evals/evals/run_evals.py
```

## How To Use This Repo

1. Read [Naresh Revision Handbook](docs/NARESH_REVISION_HANDBOOK.md).
2. Review [Resume To JD Skill Map](docs/RESUME_TO_JD_SKILL_MAP.md).
3. Run each project and read the code.
4. Practice the interview answers in [Interview Playbook](docs/INTERVIEW_PLAYBOOK.md).
5. Before interviews, skim [Quick Revision Flashcards](docs/QUICK_REVISION_FLASHCARDS.md).

## Demo Auth Tokens

The code uses local demo tokens for learning:

- `Bearer naresh-partner-token`: `catalog:read quote:write order:write tools:invoke`
- `Bearer naresh-analyst-token`: `catalog:read quote:write`

In production, replace this with OAuth 2.0/JWT validation through a real identity provider.

