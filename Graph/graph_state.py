
from typing_extensions import TypedDict, Annotated
from langgraph.graph import add_messages


class State(TypedDict):
    ticket_input: str
    messages: Annotated[list, add_messages]
