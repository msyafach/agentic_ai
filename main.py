from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from model import llm
from tools import data_tools
from db_dev import doc_tools
import asyncio

# pdf_tool = doc_tools(r"C:\Gabut\Undangan_Lowongan_Kerja_Palsu.pdf")
# docs = asyncio.run(pdf_tool.pdf_loader())
chat = llm("gemini-2.0-flash")
tools = [data_tools(r"C:\Gabut\Undangan_Lowongan_Kerja_Palsu.pdf").check_tool]
chat_with_tools = chat.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def assistant(state: AgentState):
    return {
        "messages": [chat_with_tools.invoke(state["messages"])],
    }

builder = StateGraph(AgentState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)

builder.add_edge("tools", "assistant")
syafa = builder.compile()

messages = [HumanMessage(content="Tell me about this document")]
response = syafa.invoke({"messages": messages})

print(response['messages'][-1].content)