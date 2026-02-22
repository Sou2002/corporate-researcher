from typing import TypedDict, Annotated
from langchain.messages import AIMessage
import operator


class SearchAgentState(TypedDict):
    """
    """
    task: str
    search_queries: AIMessage
    search_results: Annotated[list[dict], operator.add]
    