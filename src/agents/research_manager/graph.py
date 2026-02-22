from langgraph.graph import StateGraph, START, END
from src.agents.research_manager.states.research_manager_state import ResearchManagerState
from src.agents.research_manager.nodes.research_manager import research_manager_node
from src.agents.research_manager.nodes.research_subgraphs import call_research_subgraphs


def create_reserach_manager_graph():
    """
    """
    graph_builder = StateGraph(ResearchManagerState)

    graph_builder.add_node("research_manager", research_manager_node)
    graph_builder.add_node("research", call_research_subgraphs)

    graph_builder.add_edge(START, "research_manager")
    graph_builder.add_edge("research", END)

    return graph_builder.compile()