"""Graph definition for the research agent.

This module defines the state graph for the research agent,
including the main workflow and node connections.
"""

from langgraph.graph import END, START, StateGraph

from src.agents.research_agent.nodes import (
    compress_research,
    llm_call,
    should_continue,
    tool_node,
)
from src.agents.research_agent.states import ResearcherOutputState, ResearcherState

# ===== GRAPH CONSTRUCTION =====

# Build the agent workflow
researcher_agent_builder = StateGraph(
    ResearcherState, output_schema=ResearcherOutputState
)

# Add nodes to the graph
researcher_agent_builder.add_node("llm_call", llm_call)
researcher_agent_builder.add_node("tool_node", tool_node)
researcher_agent_builder.add_node("compress_research", compress_research)

# Add edges to connect nodes
researcher_agent_builder.add_edge(START, "llm_call")
researcher_agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    {
        "tool_node": "tool_node",  # Continue research loop
        "compress_research": "compress_research",  # Provide final answer
    },
)
researcher_agent_builder.add_edge(
    "tool_node", "llm_call"
)  # Loop back for more research
researcher_agent_builder.add_edge("compress_research", END)

# Compile the agent
researcher_agent = researcher_agent_builder.compile()
