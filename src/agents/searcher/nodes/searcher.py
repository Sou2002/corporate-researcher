from langchain_groq import ChatGroq
from langchain.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from src.utils.get_api_key import get_groq_api_key
from src.agents.searcher.states.searcher_agent_state import SearchAgentState
from src.agents.searcher.tools import tools


def searcher_node(state: SearchAgentState) -> SearchAgentState:
    """
    """

    system_msg = SystemMessage("""
        You are a Search Planning Agent with access to a web search tool.

        Your ONLY job is to gather information for a downstream Analyst Agent.
        You do NOT produce the final answer for the user.

        When you receive a user query:

        1. Analyze the request and determine what information must be searched.
        2. Break the request into one or more precise web search queries.
        3. Use the web search tool to retrieve relevant information.
        4. Always perform multiple searches to cover all aspects of the request.

        Guidelines:
        - Search whenever external or up-to-date information may be needed.
        - Prefer multiple focused searches over one vague search.
        - Do not guess when information should be searched.
        - Do not explain reasoning to the user.
        - Do not produce a final answer.
        - Only gather and return relevant information for the Analyst Agent.

        Your output should consist of multiple tool calls only.
                               
        The Analyst Agent will rely entirely on the information you gather.
        If information may be useful, search for it.
        Err on the side of over-searching rather than under-searching.
    """)

    prompt = ChatPromptTemplate.from_messages([
        system_msg,
        ("human", "{task}"),
    ])

    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=get_groq_api_key()
    ).bind_tools(
        tools=tools,
        tool_choice="any"
    )

    chain = prompt | model

    return {
        "search_queries": chain.invoke({
            "task": state["task"]
        })
    }
