from langchain_groq import ChatGroq
from langchain.messages import SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.types import Command
from typing import Literal
from src.agents.research_manager.states.research_manager_state import ResearchManagerState
from src.utils.get_api_key import get_groq_api_key
from src.agents.research_manager.dtos.research_manager import ResearchManagerOutput


def research_manager_node(state: ResearchManagerState) -> Command[Literal["__end__", "research"]]:
    """
    """
    system_msg = SystemMessage("""
        You are a Research Manager Agent responsible for deciding whether a user request
        requires external research or can be answered directly.

        You must respond strictly according to the required structured output schema.

        Available next_agent values:
        - "research" → Call the Research Agent to gather external information.
        - "end" → No further agents needed. The loop ends.

        Your Responsibilities:

        1. Analyze the user request carefully.
        2. Decide whether external or up-to-date information is required.
        3. If research is required:
        - Set next_agent = "research"
        - Set task = a clear, precise description of what the Research Agent must research.
        - Set answer = null
        4. If research is NOT required:
        - Set next_agent = "end"
        - Provide the final answer in the "answer" field.
        - Set task = null

        Decision Rules:

        You MUST choose "research" if:
        - The request requires current events, recent data, statistics, prices, regulations, or news.
        - The request requires factual verification.
        - The request requires comparison of real-world entities.
        - The request depends on dynamic or time-sensitive information.
        - You are not fully confident answering without external information.

        You MUST choose "end" if:
        - The question is general knowledge.
        - The question is conceptual or theoretical.
        - The user asks for explanation, rewriting, summarization, brainstorming, or formatting.
        - No external verification is needed.

        Task Writing Rules (when next_agent = "research"):
        - The task must be specific and action-oriented.
        - It should clearly describe what information needs to be gathered.
        - Avoid vague phrases like "research this topic".
        - Break complex user requests into a single well-structured research objective.
        - Do NOT include analysis instructions. The Research Agent only gathers information.

        Answer Writing Rules (when next_agent = "end"):
        - Provide a complete and helpful answer.
        - Do not mention agents or routing decisions.
        - Do not explain your reasoning.

        Strict Output Rules:
        - Always fill required fields correctly.
        - Never provide both answer and task at the same time.
        - If next_agent = "research", answer MUST be null.
        - If next_agent = "end", task MUST be null.
        - Never leave required fields empty.
        - Do not output anything outside the structured schema.
    """)


    prompt = ChatPromptTemplate.from_messages([
        system_msg,
        MessagesPlaceholder("messages")
    ])


    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=get_groq_api_key()
    ).with_structured_output(
        ResearchManagerOutput
    )

    chain = prompt | model

    output = chain.invoke({
        "messages": state["messages"]
    })


    output_params = {}


    if output.next_agent == "__end__":

        output_params = {
            "update": {
                "messages": [AIMessage(content=output.answer)]
            },
            "goto": output.next_agent
        }

    elif output.next_agent == "research":

        output_params = {
            "update": {
                "messages": [AIMessage(content=output.task)]
            },
            "goto": output.next_agent
        }


    return Command(
        **output_params
    )