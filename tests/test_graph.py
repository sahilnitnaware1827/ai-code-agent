from langchain_core.messages import HumanMessage
from langgraph.types import Command

from app.graph import graph


config = {
    "configurable": {
        "thread_id": "test-edit-approval-1"
    }
}


print("=" * 60)
print("AI CODE AGENT - EDIT APPROVAL TEST")
print("=" * 60)


# --------------------------------------------------
# 1. Start the agent
# --------------------------------------------------

result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "Fix the bug in "
                    "workspace/sample_project/bug.py. "
                    "Inspect the file first, identify the problem, "
                    "and propose the required edit."
                )
            )
        ],
        "iteration": 0,
        "approved": False,
        "edit_request": None,
    },
    config=config, # type: ignore
)


# --------------------------------------------------
# 2. Check whether graph is waiting for approval
# --------------------------------------------------

if "__interrupt__" in result:

    print("\n" + "=" * 60)
    print("APPROVAL REQUIRED")
    print("=" * 60)

    interrupt_data = result["__interrupt__"]

    print(interrupt_data)

    decision = input(
        "\nApprove this edit? (y/n): "
    ).strip().lower()

    approved = decision == "y"

    # --------------------------------------------------
    # 3. Resume graph
    # --------------------------------------------------

    result = graph.invoke(
        Command(
            resume=approved
        ),
        config=config, # type: ignore
    )


# --------------------------------------------------
# 4. Final result
# --------------------------------------------------

print("\n" + "=" * 60)
print("FINAL RESULT")
print("=" * 60)

print(result)
