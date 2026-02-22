from pydantic import BaseModel, Field
from typing import Literal


class ResearchManagerOutput(BaseModel):
    """
    """
    answer: str | None = Field(
        description="Answer from the research manager if needed"
    )
    next_agent: Literal["research", "__end__"] = Field(
        description="Determines which agent to call next or end the loop"
    )
    task: str | None = Field(
        description="If research agent is called then this should specify the user task"
    )
