from langchain_groq import ChatGroq
from langchain.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
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

    system_msg = SystemMessage("""
        You are a very helpful research assistant.
        
        Your task is to research the topic with your knowledge as well as the tools that are provided to you.

        Also generate a detailed report as output.
    """)

    prompt = ChatPromptTemplate.from_messages([
        system_msg,
        MessagesPlaceholder(variable_name="messages"),
    ])

    model = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=get_groq_api_key()
    ).bind_tools(
        tools=tools
    )

    chain = prompt | model

    return {
        "messages": [chain.invoke({"messages": state["messages"]})]
    }
