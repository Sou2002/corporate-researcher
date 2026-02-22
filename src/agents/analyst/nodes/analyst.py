from langchain.messages import SystemMessage
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.agents.analyst.states.analyst_agent_state import AnalystAgentState
from src.utils.get_api_key import get_groq_api_key


def analyst_node(state: AnalystAgentState) -> AnalystAgentState:
    """
    """

    system_msg = SystemMessage("""
        You are an expert market analyst. 
        Analyze the following raw search data to answer the user's task. 
        Extract key metrics, trends, and strictly cite your sources from the provided text.
        If the data is irrelevant, state that clearly.
    """)

    user_message = "TASK: {task}\n\nRAW SEARCH DATA:\n{raw_data}"

    prompt = ChatPromptTemplate.from_messages([
        system_msg,
        ("human", user_message),
    ])

    model = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=get_groq_api_key()
    )

    chain = prompt | model

    return {
        "analysis": chain.invoke({
            "task": state["task"],
            "raw_data": state["search_results"]
        })
    }