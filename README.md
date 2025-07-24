# Episodic Memory: AI Customer Support Agent

## Overview

This project implements an AI-powered customer support agent that leverages large language models (LLMs) and memory-augmented reasoning to handle support tickets. The agent can triage incoming tickets, route them to the appropriate handler, and generate empathetic, context-aware responses. It is designed to:

- Categorize support tickets (e.g., Returns & Refunds, Billing, General)
- Use few-shot learning and memory to improve over time
- Respond to customer queries using advanced LLMs (OpenAI GPT-4o-mini)
- Integrate with external tools and memory stores for enhanced support

## Features
- **Automated Ticket Triage:** Classifies incoming tickets and routes them to the correct agent.
- **Few-Shot Learning:** Stores and retrieves example tickets to improve classification and response quality.
- **LLM-Powered Responses:** Uses OpenAI models to generate helpful, empathetic replies.
- **Extensible Tooling:** Integrates with external tools (e.g., scheduling callbacks, checking ticket status).

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management. Ensure you have Python 3.12+ installed.

1. **Install Poetry** (if you don't have it):
   ```bash
   pip install poetry
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Set up environment variables:**
   - Copy the provided `.env` file and add your OpenAI API key:
     ```env
     OPENAI_API_KEY=your-openai-key-here
     ```

## Running the MCP Server

Before running the agent or any client code, you must start the MCP (Memory-Centric Protocol) server. This server enables tool-based communication and memory management for the AI agent.

To start the MCP server, run the following command from the root of the Episodic_Memory project:

```bash
poetry run python Graph/MCP_Servers.py
```

This will start the MCP server on `localhost:8765` using SSE (Server-Sent Events) transport. The server exposes tools for ticket response, scheduling callbacks, checking ticket status, and managing/retrieving memory.

> **Note:** If you want to change the host or port, edit the `host` and `port` parameters in `Graph/MCP_Servers.py`.

## Usage Example

> **Before running the code below, make sure the MCP server is running as described above.**

You can interact with the agent via the provided Jupyter notebooks or by calling the main agent function in Python. Here is a minimal example:

```python
from graph import customer_support_agent
from Graph.memory import store
from Data import example1, example2
import uuid

# Store few-shot examples
store.put(("customer_support", "user1", "few_shot_examples"), str(uuid.uuid4()), example1)
store.put(("customer_support", "user1", "few_shot_examples"), str(uuid.uuid4()), example2)

ticket = {
    "from": "Alex Smith <alex@gmail.com>",
    "subject": "Returning an item",
    "ticket_description": "I want to return an item I purchased. Please advise."
}

config = {"configurable": {"user_id": "user1"}}
response = await customer_support_agent(input=ticket, config=config)

for message in response["messages"]:
    print(message)
```

Or, open `main.ipynb` for a step-by-step interactive demo.

## Project Structure
- `graph.py`: Main agent logic and workflow
- `Graph/Nodes/`: Triage and response agent nodes
- `Graph/memory.py`: In-memory store for few-shot examples
- `prompt_templates.py`: Prompt templates for LLMs
- `Data.py`: Example support tickets

## License
MIT License 