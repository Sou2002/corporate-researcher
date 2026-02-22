from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from src.agents.searcher.states.searcher_agent_state import SearchAgentState
from src.agents.searcher.nodes.searcher import searcher_node
from src.agents.searcher.nodes.tool_executor import tool_executor_node


def create_searcher_graph() -> CompiledStateGraph[SearchAgentState, None, SearchAgentState, SearchAgentState]:
    """
    """
    graph_builder = StateGraph(SearchAgentState)

    graph_builder.add_node("searcher", searcher_node)
    graph_builder.add_node("tool_executor", tool_executor_node)

    graph_builder.add_edge(START, "searcher")
    graph_builder.add_edge("searcher", "tool_executor")
    graph_builder.add_edge("tool_executor", END)

    return graph_builder.compile()
