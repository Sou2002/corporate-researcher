from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from src.agents.analyst.states.analyst_agent_state import AnalystAgentState
from src.agents.analyst.nodes.analyst import analyst_node


def create_analyst_graph() -> CompiledStateGraph[AnalystAgentState, None, AnalystAgentState, AnalystAgentState]:
    """
    """
    graph_builder = StateGraph(AnalystAgentState)

    graph_builder.add_node("analyst", analyst_node)

    graph_builder.add_edge(START, "analyst")
    graph_builder.add_edge("analyst", END)

    return graph_builder.compile()
