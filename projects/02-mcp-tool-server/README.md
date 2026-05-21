# Project 02: MCP-Style Tool Server

This project demonstrates how to front commerce capabilities with a small MCP-style JSON-RPC server boundary.

It intentionally avoids a heavy SDK so the interview concept is clear:

- List tools
- Validate tool arguments
- Enforce side-effect policy
- Return structured results
- Keep agent-facing contracts narrow

Run:

```bash
python projects/02-mcp-tool-server/mcp_server/server.py
```

Example JSON-RPC line:

```json
{"jsonrpc":"2.0","id":"1","method":"tools/list","params":{}}
```

