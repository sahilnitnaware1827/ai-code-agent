from app.agent import llm_with_tools

response = llm_with_tools.invoke(
    "List all files inside workspace/sample_project"
)

print("\n Response >>> ")
print(response.content)

print("\n\n Tool Call >>> ")
print(response.tool_calls)
