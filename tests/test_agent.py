from app.agent import llm_with_tools, execute_tool


response = llm_with_tools.invoke(
    "List all files inside workspace/sample_project"
)

print("Tool calls:")
print(response.tool_calls)


if response.tool_calls:
    result = execute_tool(response.tool_calls[0])

    print("\nTool result:")
    print(result)