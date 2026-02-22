from langchain.messages import AIMessage
from src.agents.research_manager.states.research_manager_state import ResearchManagerState
from src.agents.searcher.graph import create_searcher_graph
from src.agents.analyst.graph import create_analyst_graph


def call_research_subgraphs(state: ResearchManagerState) -> ResearchManagerState:
    """
    """
    searcher_agent = create_searcher_graph()
    analyst_agent = create_analyst_graph()

    searcher_output = searcher_agent.invoke({
        "task": state["messages"][-1].content
    })

    analyst_output = analyst_agent.invoke({
        "task": searcher_output["task"],
        "search_results": searcher_output["search_results"]
    })

    return {
        "messages": [analyst_output["analysis"]]
    }