from langchain_mcp_adapters.client import MultiServerMCPClient

mcp_client = MultiServerMCPClient({
    "customer_support_server": {
        "transport": "sse",
        "url": "http://127.0.0.1:8765/sse"
    }
})
