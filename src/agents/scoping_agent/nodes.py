"""
Nodes for the scoping agent.

This module defines the core nodes for the scoping agent workflow. 
"""

from typing import Literal

from langsmith import Client
from langgraph.graph import END
from langgraph.types import Command
from langchain.chat_models import init_chat_model
from langchain_core.messages import (HumanMessage,
                                     AIMessage,
                                     get_buffer_string)

from src.agents.utils import get_today_str
from src.agents.scoping_agent.states import (AgentState,
                                        ClarifyWithUser,
                                        ResearchQuestion)


# Load the prompt from prompt hub
client = Client()
clarify_with_user_instructions = client.pull_prompt("clarify_with_user_instructions")
transform_messages_into_research_topic_prompt = client.pull_prompt("transform_messages_into_research_topic_prompt")

# Initialize model
model = init_chat_model(model="groq:openai/gpt-oss-20b", temperature=0.0)


def clarify_with_user(state: AgentState) -> Command[Literal["write_research_brief", "__end__"]]:
    """
    Determine if the user's request contains sufficient information to proceed with research.
    
    Uses structured output to make deterministic decisions and avoid hallucination.
    Routes to either research brief generation or ends with a clarification question.
    """
    # Set up structured output model
    structured_output_model = model.with_structured_output(ClarifyWithUser)

    # Invoke the model with clarification instructions
    response = structured_output_model.invoke([
        HumanMessage(content=clarify_with_user_instructions.format(
            messages=get_buffer_string(messages=state["messages"]), 
            date=get_today_str()
        ))
    ])
    
    # Route based on clarification need
    if response.need_clarification:
        return Command(
            goto=END, 
            update={"messages": [AIMessage(content=response.question)]}
        )
    else:
        return Command(
            goto="write_research_brief", 
            update={"messages": [AIMessage(content=response.verification)]}
        )
    

def write_research_brief(state: AgentState) -> AgentState:
    """
    Transform the conversation history into a comprehensive research brief.
    
    Uses structured output to ensure the brief follows the required format
    and contains all necessary details for effective research.
    """
    # Set up structured output model
    structured_output_model = model.with_structured_output(ResearchQuestion)
    
    # Generate research brief from conversation history
    response = structured_output_model.invoke([
        HumanMessage(content=transform_messages_into_research_topic_prompt.format(
            messages=get_buffer_string(state.get("messages", [])),
            date=get_today_str()
        ))
    ])
    
    # Update state with generated research brief and pass it to the supervisor
    return {
        "research_brief": response.research_brief,
        "supervisor_messages": [HumanMessage(content=f"{response.research_brief}.")]
    }