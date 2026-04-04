from langchain.chat_models import init_chat_model
from tavily import TavilyClient


# Initialize model
model = init_chat_model(model="ollama:gemma4:e4b", num_ctx=20000, temperature=0.0)
summarization_model = init_chat_model(model="ollama:gemma4:e4b", num_ctx=20000, temperature=0.0)
compress_model = init_chat_model(model="ollama:gemma4:e4b", num_ctx=20000, num_predict=32000)

# Initialize web search client
web_search_client = TavilyClient()
