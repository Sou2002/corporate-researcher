from typing import TypedDict, Annotated
from langchain.messages import AnyMessage
import operator


class ResearchAgentState(TypedDict):
    """
    """
    messages: Annotated[list[AnyMessage], operator.add]
    