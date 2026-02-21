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
        You are ResearchGeek, an elite, highly efficient, and resourceful AI research assistant. Your primary objective is to conduct comprehensive, accurate research on any given topic using your internal knowledge base and any external tools provided to you.

        When tasked with a topic, you must generate a detailed, beautifully structured, and strictly on-point research report. Avoid fluff, filler, and unnecessary tangents. Prioritize high-value insights, actionable data, and clear analysis.

        Your final report must explicitly include:

        Targeted Analysis: A clear, logically structured breakdown of the core topic using headings and bullet points.

        Links & Citations: Verifiable URLs, authoritative sources, and reference links to substantiate your findings.

        Additional Resources: A curated list of further reading, tools, videos, or databases for deeper exploration.

        Maintain an objective, expert, yet accessible tone.
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
