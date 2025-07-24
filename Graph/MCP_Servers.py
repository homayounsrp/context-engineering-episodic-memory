
from mcp.server.fastmcp import FastMCP
from langmem import create_manage_memory_tool, create_search_memory_tool
from dotenv import load_dotenv
load_dotenv()
from memory import store
# Create the MCP server
mcp = FastMCP(
    name="customer_support_server",
    host="127.0.0.1",   # optional—defaults to 127.0.0.1 in many versions
    port=8765           # ← set your WebSocket port here
)

@mcp.tool()
def respond_ticket(to: str, subject: str, content: str) -> str:
    """Write and send a response to a support ticket."""
    # Placeholder response - in a real app, this would send a ticket response
    return f"Ticket response sent to {to} with subject '{subject}'"



@mcp.tool()
def schedule_callback(
    attendees: list[str],
    subject: str,
    preferred_day: str
) -> str:
    """Schedule a callback or follow-up meeting with the customer."""
    # Placeholder response - in a real app, this would schedule a callback
    return f"Callback '{subject}' scheduled for {preferred_day} with {len(attendees)} attendees"


@mcp.tool()
def check_ticket_status(ticket_id: str) -> str:
    """Check the current status of a support ticket."""
    # Placeholder response - in a real app, this would query the ticket system
    return f"Status of ticket {ticket_id}: Open"


@mcp.tool()
async  def manage_memory(user_id: str):
    """use this tool to save the memory about customer."""
    manage_memory = create_manage_memory_tool(
        namespace=("email_assistant", user_id, "collection"),
        store=store
    )
    return manage_memory

@mcp.tool()
async  def search_memory(user_id: str):
    """use this tool to retrieve memory about customer."""
    search_memory = create_search_memory_tool(
        namespace=("email_assistant", user_id, "collection"),
         store=store

    )
    return search_memory




if __name__ == "__main__":
    mcp.run(transport="sse")