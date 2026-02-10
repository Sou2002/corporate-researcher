from langchain_community.tools import DuckDuckGoSearchRun

tools = [
    DuckDuckGoSearchRun()
]

tools_by_name = {
    tool.name: tool for tool in tools
}