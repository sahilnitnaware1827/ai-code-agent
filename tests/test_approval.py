from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver


def approval_node(state):

    decision = interrupt(
        "Do you approve this operation?"
    )

    return {
        "approved": decision
    }


builder = StateGraph(dict)

builder.add_node("approval", approval_node)

builder.add_edge(START, "approval")
builder.add_edge("approval", END)

checkpointer = MemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)


config = {
    "configurable": {
        "thread_id": "approval-test-1"
    }
}


result = graph.invoke(
    {},
    config=config # type: ignore
)

print("Graph paused:")
print(result)

decision = input("Approve? (y/n): ").strip().lower()

result = graph.invoke(
    Command(resume=decision == "y"),
    config=config, # type: ignore
)

print("\nGraph resumed:")
print(result)
