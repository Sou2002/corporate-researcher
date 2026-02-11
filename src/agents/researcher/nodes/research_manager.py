from langchain_groq import ChatGroq
from src.utils.get_api_key import get_groq_api_key
from src.agents.researcher.states.research_agent_state import ResearchAgentState
from src.agents.researcher.tools import tools


def research_manager_node(state: ResearchAgentState) -> ResearchAgentState:
    """
    Invokes the research manager model and returns the result.

    Args:
        state (ResearchAgentState): The state of the research agent.

    Returns:
        ResearchAgentState: The state of the research agent after invoking the research manager model.
    """
    model = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=get_groq_api_key()
    ).bind_tools(
        tools=tools
    )

    return {
        "messages": [model.invoke(state["messages"])]
    }
