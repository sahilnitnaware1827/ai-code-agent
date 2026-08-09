from langchain_core.messages import HumanMessage
from langgraph.types import Command

from app.graph import graph


config = {
    "configurable": {
        "thread_id": "approval-test-final"
    }
}


edit_request = {
    "path": "workspace/sample_project/bug.py",
    "old_text": "return price * quantity",
    "new_text": "return price * quantity",
}


state = {
    "messages": [
        HumanMessage(
            content="Test file edit approval."
        )
    ],
    "iteration": 0,
    "approved": False,
    "edit_request": edit_request,
    "edit_tool_call_id": "edit-test-1"
}


print("=" * 60)
print("AI CODE AGENT - FILE EDIT APPROVAL TEST")
print("=" * 60)


result = graph.invoke(
    state, # type: ignore
    config=config, # type: ignore
)


print("\nGRAPH PAUSED:")
print(result)


if "__interrupt__" not in result:

    print(
        "\nERROR: Graph did not pause for approval."
    )

    raise SystemExit(1)


print("\nAPPROVAL REQUEST RECEIVED.")


decision = input(
    "\nApprove edit? (y/n): "
).strip().lower()


approved = decision == "y"


result = graph.invoke(
    Command(
        resume=approved
    ),
    config=config, # type: ignore
)


print("\n" + "=" * 60)
print("GRAPH RESUMED")
print("=" * 60)


print(result)

