from src.agents.researcher.states.research_agent_state import ResearchAgentState
from langchain_groq import ChatGroq
from src.utils.get_api_key import get_groq_api_key


def research_manager_node(state: ResearchAgentState) -> ResearchAgentState:
    """
    """
    model = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=get_groq_api_key()
    )

    return {
        "messages": [model.invoke(state["messages"])]
    }