"""
Graph definition for the scoping agent.

This module defines the state graph for the scoping agent, 
including the main workflow and node connections.
"""

from langgraph.graph import StateGraph, START, END

from src.agents.scoping_agent.states import AgentInputState, AgentState
from src.agents.scoping_agent.nodes import clarify_with_user, write_research_brief

# ===== GRAPH CONSTRUCTION =====

# Build the scoping workflow
scope_researcher_builder = StateGraph(AgentState, input_schema=AgentInputState)

# Add workflow nodes
scope_researcher_builder.add_node("clarify_with_user", clarify_with_user)
scope_researcher_builder.add_node("write_research_brief", write_research_brief)

# Add workflow edges
scope_researcher_builder.add_edge(START, "clarify_with_user")
scope_researcher_builder.add_edge("write_research_brief", END)

# Compile the workflow
scope_research = scope_researcher_builder.compile()