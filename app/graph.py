from typing import Annotated, Optional, TypedDict

from langchain_core.messages import AnyMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.types import interrupt

from app.agent import llm_with_tools, tools
from app.tools.editor import apply_file_edit, edit_file


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    iteration: int
    approved: bool
    edit_request: Optional[dict]
    edit_tool_call_id: Optional[str]


def call_model(state: AgentState):
    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response],
        "iteration": state["iteration"] + 1,
    }


tool_node = ToolNode(tools)


def start_router(state: AgentState):
    """
    Normal execution starts at the agent.

    Tests that provide an edit_request can start
    directly at the approval node.
    """

    if state.get("edit_request"):
        return "approval"

    return "agent"


def should_continue(state: AgentState):
    """
    Decide what the agent should do after an LLM response.
    """

    if state["iteration"] >= 10:
        return END

    last_message = state["messages"][-1]

    if not last_message.tool_calls:
        return END

    for tool_call in last_message.tool_calls:

        if tool_call["name"] == "edit_file":

            return "approval"

    return "tools"


def approval_node(state: AgentState):
    """
    Preview a file modification and ask the human
    for approval.

    IMPORTANT:
    The edit request is stored in state before the
    interrupt, so after resume we do NOT need to
    inspect the last message again.
    """

    edit = state.get("edit_request")

    tool_call_id = state.get(
        "edit_tool_call_id"
    )

    # ---------------------------------------------
    # Normal LLM-generated edit request
    # ---------------------------------------------

    if edit is None:

        last_message = state["messages"][-1]

        tool_call = None

        for call in last_message.tool_calls:

            if call["name"] == "edit_file":

                tool_call = call
                break

        if tool_call is None:

            return {
                "approved": False,
                "edit_request": None,
                "edit_tool_call_id": None,
            }

        edit = tool_call["args"]

        tool_call_id = tool_call["id"]

    # ---------------------------------------------
    # Generate edit preview
    # ---------------------------------------------

    preview = edit_file.invoke(
        {
            "path": edit["path"],
            "old_text": edit["old_text"],
            "new_text": edit["new_text"],
        }
    )

    # ---------------------------------------------
    # Human approval
    # ---------------------------------------------

    decision = interrupt(
        {
            "type": "file_edit_approval",
            "path": edit["path"],
            "old_text": edit["old_text"],
            "new_text": edit["new_text"],
            "preview": preview,
            "message": "Approve this file modification?",
        }
    )

    approved = bool(decision)

    # ---------------------------------------------
    # Apply approved edit
    # ---------------------------------------------

    if approved:

        result = apply_file_edit.invoke(
            {
                "path": edit["path"],
                "old_text": edit["old_text"],
                "new_text": edit["new_text"],
            }
        )

    else:

        result = (
            "Edit rejected by user. "
            "The file was not modified."
        )

    # ---------------------------------------------
    # Return tool result
    # ---------------------------------------------

    return {
        "messages": [
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call_id or "edit-approval",
            )
        ],
        "approved": approved,
        "edit_request": None,
        "edit_tool_call_id": None,
    }


def approval_router(state: AgentState):
    """
    After an approval operation:

    - Normal agent flow → return to agent.
    - Deterministic approval test → finish.
    """

    if state["iteration"] == 0:
        return END

    return "agent"


builder = StateGraph(AgentState)


# ---------------------------------------------
# Nodes
# ---------------------------------------------

builder.add_node(
    "agent",
    call_model,
)

builder.add_node(
    "tools",
    tool_node,
)

builder.add_node(
    "approval",
    approval_node,
)


# ---------------------------------------------
# START
# ---------------------------------------------

builder.add_conditional_edges(
    START,
    start_router,
    {
        "agent": "agent",
        "approval": "approval",
    },
)


# ---------------------------------------------
# Agent routing
# ---------------------------------------------

builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "approval": "approval",
        END: END,
    },
)


# ---------------------------------------------
# Tools → Agent
# ---------------------------------------------

builder.add_edge(
    "tools",
    "agent",
)


# ---------------------------------------------
# Approval routing
# ---------------------------------------------

builder.add_conditional_edges(
    "approval",
    approval_router,
    {
        "agent": "agent",
        END: END,
    },
)


# ---------------------------------------------
# Checkpointer
# ---------------------------------------------

checkpointer = MemorySaver()


graph = builder.compile(
    checkpointer=checkpointer
)
