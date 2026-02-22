from typing import TypedDict


class AnalystAgentState(TypedDict):
    """
    """
    task: str
    search_results: list[dict]
    analysis: str