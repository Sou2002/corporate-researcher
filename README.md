# Corporate Researcher

Corporate Researcher is a modular multi-agent research framework built with `langgraph`, `langchain`, and Ollama. It is designed to transform user prompts into an end-to-end research workflow that clarifies intent, generates a research brief, dispatches parallel research agents, and synthesizes a final report.

## Key Features

- Clarifies ambiguous user research requests before starting work
- Generates structured research briefs from conversation history
- Uses a supervisor agent to coordinate parallel research tasks
- Launches specialized researcher agents that can call tools and compress findings
- Produces a polished final research report from aggregated notes

## Architecture Overview

### `src/agents/corporate_researcher`

This package contains the main orchestration graph for the full research workflow.

- `graph.py`: Builds the overall state graph and composes the workflow.
- `nodes.py`: Defines core workflow nodes:
  - `clarify_with_user`
  - `write_research_brief`
  - `final_report_generation`
- `states.py`: Defines the input, state, and output schemas used by the workflow.

### `src/agents/research_supervisor`

Implements a supervisor pattern that manages multi-agent research delegation.

- `graph.py`: Builds the supervisor graph.
- `nodes.py`: Implements supervisor logic and tool execution.
- `states.py`: Defines supervisor state, research progress tracking, and note aggregation.
- `tools.py`: Contains tools used by the supervisor, including researcher dispatch.

### `src/agents/research_agent`

Implements the individual research agent that performs iterative research.

- `graph.py`: Builds the researcher agent graph.
- `nodes.py`: Handles LLM decisions, tool execution, and research compression.
- `states.py`: Defines researcher state and output payloads.
- `tools.py`: Contains research tools such as web search and thinking utilities.

### `src/agents/services.py`

Configures LLM models and the web search client used across agents.

### `src/agents/prompts.py`

Loads prompt templates from LangSmith prompt hub for the research workflow.

### `src/agents/utils.py`

Provides shared utility helpers used by multiple agents.

## Requirements

- Python 3.12+
- `langchain>=1.2.13`
- `langchain-classic>=1.0.3`
- `langchain-ollama>=1.0.1`
- `langgraph>=1.0.10`
- `python-dotenv>=1.0.1`
- `tavily-python>=0.7.23`

## Installation

Create and activate a virtual environment using [uv](https://docs.astral.sh/uv/), then install dependencies:

```bash
git clone https://github.com/Sou2002/corporate-researcher.git
cd corporate-researcher
uv venv
uv sync
langgraph dev
```

If you maintain a local requirements file:

```bash
pip install -r requirements.txt
```

## Configuration

This project expects the following capabilities:

- The current implementation is tied to the `ollama:gemma4:e4b` model in `src/agents/services.py`
- If you want to use another model, prompts and prompt handling must be updated accordingly
- A Tavily web search client available through `tavily-python`
- LangSmith prompt hub access for loading prompt templates in `src/agents/prompts.py`

Make sure any required environment variables or service credentials are configured before running the system.

## Usage Example

You can invoke the main research agent programmatically.

```python
from src.agents.corporate_researcher.graph import corporate_researcher_agent
from src.agents.corporate_researcher.states import AgentInputState
from langchain_core.messages import HumanMessage

input_state = AgentInputState(messages=[HumanMessage(content="Research recent trends in sustainable corporate finance.")])
result = corporate_researcher_agent.invoke(input_state)
print(result.get("final_report"))
```

## Development

This project is under active development, and formal test cases are not ready yet.

## Project Structure

```text
src/agents/
  prompts.py
  services.py
  utils.py
  corporate_researcher/
    graph.py
    nodes.py
    states.py
  research_agent/
    graph.py
    nodes.py
    states.py
    tools.py
  research_supervisor/
    graph.py
    nodes.py
    states.py
    tools.py
```

## Notes

- The README is intentionally focused on architecture and usage because the prompt logic lives in external LangSmith prompt templates.
- The system is built for modular research orchestration rather than a single command-line tool.

## License

This project is released under the MIT License.
