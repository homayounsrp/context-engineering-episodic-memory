
from Graph.Nodes.Triage.prompts import prompt_instructions
from langgraph.prebuilt import create_react_agent
from prompt_templates import agent_system_prompt
from config import get_openai_api_key
from Graph.memory import store
from Graph.MCP_Client import mcp_client



def create_prompt(state):
    return [
        {
            "role": "system", 
            "content": agent_system_prompt.format(
                instructions=prompt_instructions["agent_instructions"]
                )
        }
    ] + state['messages']



async def react_agent(state, config):
    mcp_tools = await mcp_client.get_tools()
    agent = create_react_agent(
        "openai:gpt-4o-mini",
        tools=mcp_tools,
        prompt=create_prompt,
        store=store
    )
    return await agent.ainvoke(state, config)