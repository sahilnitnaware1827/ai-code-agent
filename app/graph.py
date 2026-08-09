from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from app.agent import llm_with_tools, tools


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    iteration: int


def call_model(state: AgentState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response],
        "iteration": state["iteration"] + 1,
    }


tool_node = ToolNode(tools)


def should_continue(state: AgentState):

    if state["iteration"] >= 10:
        return END

    last_message = state["messages"][-1]

    if last_message.tool_calls: # type: ignore
        return "tools"

    return END


builder = StateGraph(AgentState)

builder.add_node("agent", call_model)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END,
    }
)

builder.add_edge("tools", "agent")

graph = builder.compile()

