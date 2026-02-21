import chainlit as cl
from langchain.messages import HumanMessage
from langgraph.config import RunnableConfig
from src.agents.researcher.graph import create_researcher_graph


@cl.on_message
async def on_message(msg: cl.Message):

    config = {"configurable": {"thread_id": cl.context.session.id}}
    cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")

    graph = create_researcher_graph()
    
    for ai_msg, metadata in graph.stream(
        input={
            "messages": [HumanMessage(content=msg.content)]
        }, 
        stream_mode="messages", 
        config=RunnableConfig(callbacks=[cb], **config)
    ):
        if (
            ai_msg.content
            and not isinstance(ai_msg, HumanMessage)
            and metadata["langgraph_node"] == "research_manager"
        ):
            await final_answer.stream_token(ai_msg.content)

    await final_answer.send()
