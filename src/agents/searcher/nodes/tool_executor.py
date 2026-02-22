from src.agents.searcher.states.searcher_agent_state import SearchAgentState
from src.agents.searcher.tools import tools_by_name


def tool_executor_node(state: SearchAgentState) -> SearchAgentState:
    """
    """
    results = []

    for tool_call in state["search_queries"].tool_calls:

        tool = tools_by_name[tool_call["name"]]

        observation = tool.invoke(tool_call["args"])

        results.extend(observation)

    return {
        "search_results": results
    }
