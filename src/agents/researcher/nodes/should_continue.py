from typing import Literal
from langgraph.graph import END
from src.agents.researcher.states.research_agent_state import ResearchAgentState


def should_continue(state: ResearchAgentState) -> Literal["tool_executor", END]:
    """
    """
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "tool_executor"

    return END