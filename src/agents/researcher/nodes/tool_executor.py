from langchain.messages import ToolMessage
from src.agents.researcher.states.research_agent_state import ResearchAgentState
from src.agents.researcher.tools import tools_by_name


def tool_executor_node(state: ResearchAgentState) -> ResearchAgentState:
    """
    Executes the tool calls in the last message and returns the result.

    Args:
        state (ResearchAgentState): The state of the research agent.

    Returns:
        ResearchAgentState: The state of the research agent after executing the tool calls.
    """
    result = []

    for tool_call in state["messages"][-1].tool_calls:

        tool = tools_by_name[tool_call["name"]]

        observation = tool.invoke(tool_call["args"])

        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))

    return {
        "messages": result
    }
