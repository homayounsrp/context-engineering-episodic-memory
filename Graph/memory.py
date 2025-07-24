from langgraph.store.memory import InMemoryStore
from dotenv import load_dotenv
load_dotenv()

store = InMemoryStore(
    index={"embed": "openai:text-embedding-3-small"}
)

