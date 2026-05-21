from mcp_server.server import CommerceToolServer


def test_list_tools_includes_schema_and_side_effect_policy() -> None:
    tools = CommerceToolServer().list_tools()
    names = {tool["name"] for tool in tools}

    assert "catalog.search" in names
    assert "commerce.quote" in names
    assert all("input_schema" in tool for tool in tools)
    assert all(tool["side_effects"] == "none" for tool in tools)


def test_call_quote_tool_returns_structured_quote() -> None:
    result = CommerceToolServer().call_tool(
        "commerce.quote",
        {"sku": "coffee-001", "quantity": 2, "destination_zip": "45202"},
    )

    assert result["available"] is True
    assert result["total"] == "32.92"


def test_jsonrpc_rejects_invalid_agent_arguments() -> None:
    response = CommerceToolServer().handle_jsonrpc(
        {
            "jsonrpc": "2.0",
            "id": "bad-args",
            "method": "tools/call",
            "params": {
                "name": "commerce.quote",
                "arguments": {"sku": "coffee-001", "quantity": 0, "destination_zip": "45202"},
            },
        }
    )

    assert "error" in response
    assert response["error"]["code"] == -32602

