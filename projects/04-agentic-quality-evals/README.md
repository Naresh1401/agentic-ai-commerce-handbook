# Project 04: Agentic Quality Evals

This project demonstrates testing beyond deterministic API outputs.

It checks whether agent-generated tool calls:

- Use allowed tool names
- Include required arguments
- Avoid unsafe prompt-injection patterns
- Require approval for side-effecting actions
- Stay inside tool contracts

Run:

```bash
python projects/04-agentic-quality-evals/evals/run_evals.py
```

