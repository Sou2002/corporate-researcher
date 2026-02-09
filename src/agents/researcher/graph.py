from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from src.agents.researcher.states.research_agent_state import ResearchAgentState
from src.agents.researcher.nodes.research_manager import research_manager_node


def create_researcher_graph() -> CompiledStateGraph[ResearchAgentState, None, ResearchAgentState, ResearchAgentState]:
    """
    """
    graph_builder = StateGraph(ResearchAgentState)

    graph_builder.add_node("research_manager", research_manager_node)

    graph_builder.add_edge(START, "research_manager")
    graph_builder.add_edge("research_manager", END)

    return graph_builder.compile()