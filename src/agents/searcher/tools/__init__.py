from langchain_community.tools import DuckDuckGoSearchResults

tools = [
    DuckDuckGoSearchResults(output_format="list")
]

tools_by_name = {
    tool.name: tool for tool in tools
}