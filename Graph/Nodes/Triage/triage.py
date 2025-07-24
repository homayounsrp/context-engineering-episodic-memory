
from langchain.chat_models import init_chat_model
from Graph.Nodes.Triage.output_parser import Router
from config import get_openai_api_key
from Graph.graph_state import State
from langgraph.types import Command
from typing import Literal
from prompt_templates import triage_system_prompt, triage_user_prompt
from Graph.Nodes.Triage.prompts import prompt_instructions
from langgraph.graph import END
from helpers import format_few_shot_examples
llm = init_chat_model("openai:gpt-4o-mini")
llm_router = llm.with_structured_output(Router)
# ================
def triage_router(state: State, config: dict, store) -> Command[
    Literal["response_agent", "__end__"]
]:

    # get few shot examples from memory
    namespace = (
        "customer_support",
        config['configurable']['user_id'],
        "few_shot_examples"
    )

    examples = store.search(
        namespace, 
        query=str({"ticekt": state['ticket_input']}),
        limit=2
    ) 
    examples=format_few_shot_examples(examples)

    system_prompt = triage_system_prompt.format(
    triage_returns_refunds=prompt_instructions["triage_rules"]["Returns & Refunds"],
    triage_billing=prompt_instructions["triage_rules"]["billing"],
    triage_general=prompt_instructions["triage_rules"]["general"],
    examples=examples
    
    )
    user_prompt = triage_user_prompt.format(
        customer_name=state['ticket_input']['from'], 
        subject=state['ticket_input']['subject'], 
        ticket_description= state['ticket_input']['ticket_description']
    )




    # calling triage model to classify the email
    result = llm_router.invoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    # if triage classification is "Returns & Refunds", "billing", or "general", route to the appropriate agent
    if result.classification == "Returns & Refunds":
        print("🔄 Classification: RETURNS & REFUNDS - Route to returns/refunds agent")
        goto = "response_agent"
        update = {
            "messages": [
                {
                    "role": "user",
                    "content": f"Handle returns/refunds for ticket: {state['ticket_input']}",
                }
            ]
        }
    elif result.classification == "billing":
        print("💳 Classification: BILLING - Route to billing agent")
        goto = "billing_agent"
        update = {
            "messages": [
                {
                    "role": "user",
                    "content": f"Handle billing for ticket: {state['ticket_input']}",
                }
            ]
        }
    elif result.classification == "ignore":
            print("📋 Classification: Ignore")
            update = None
            goto = END
    else:
        raise ValueError(f"Invalid classification: {result.classification}")
    return Command(goto=goto, update=update)