from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import InMemorySaver
from src.agents.researcher.states.research_agent_state import ResearchAgentState
from src.agents.researcher.nodes.research_manager import research_manager_node
from src.agents.researcher.nodes.tool_executor import tool_executor_node
from src.agents.researcher.nodes.should_continue import should_continue


def create_researcher_graph() -> CompiledStateGraph[ResearchAgentState, None, ResearchAgentState, ResearchAgentState]:
    """
    """
    graph_builder = StateGraph(ResearchAgentState)

    graph_builder.add_node("research_manager", research_manager_node)
    graph_builder.add_node("tool_executor", tool_executor_node)

    graph_builder.add_edge(START, "research_manager")
    graph_builder.add_conditional_edges(
        "research_manager",
        should_continue
    )
    graph_builder.add_edge("tool_executor", "research_manager")

    return graph_builder.compile(checkpointer=InMemorySaver())