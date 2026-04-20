"""Graph definition for the main corporate researcher agent.

This module defines the state graph for the full multi agent researcher,
including the main workflow and node connections.
"""

# from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from src.agents.corporate_researcher.nodes import (
    clarify_with_user,
    final_report_generation,
    write_research_brief,
)
from src.agents.corporate_researcher.states import AgentInputState, AgentState
from src.agents.research_supervisor.graph import supervisor_agent

# ===== GRAPH CONSTRUCTION =====

# Build the full research workflow
corporate_researcher_builder = StateGraph(AgentState, input_schema=AgentInputState)

# Add workflow nodes
corporate_researcher_builder.add_node("clarify_with_user", clarify_with_user)
corporate_researcher_builder.add_node("write_research_brief", write_research_brief)
corporate_researcher_builder.add_node("supervisor_subgraph", supervisor_agent)
corporate_researcher_builder.add_node(
    "final_report_generation", final_report_generation
)

# Add workflow edges
corporate_researcher_builder.add_edge(START, "clarify_with_user")
corporate_researcher_builder.add_edge("write_research_brief", "supervisor_subgraph")
corporate_researcher_builder.add_edge("supervisor_subgraph", "final_report_generation")
corporate_researcher_builder.add_edge("final_report_generation", END)

# Compile the workflow
corporate_researcher_agent = corporate_researcher_builder.compile(
    # checkpointer=InMemorySaver()
)
