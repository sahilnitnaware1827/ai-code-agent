from langchain_core.messages import HumanMessage

from app.graph import graph


result = graph.invoke({
    "messages": [
        HumanMessage(
            content=(
                "Inspect workspace/sample_project/bug.py, "
                "fix the bug, run it, and verify the result."
            )
        )
    ],
    "iteration": 0,
})


print("Final answer:")
print(result["messages"][-1].content)

print("\nIterations:")
print(result["iteration"])

