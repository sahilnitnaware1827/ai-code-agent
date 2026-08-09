from app.llm import llm

from app.tools.filesystem import(
    list_directory,
    read_file
)

from app.tools.search import(
    search_files,
    find_file
)


from langchain_core.messages import ToolMessage, HumanMessage

from app.tools.editor import edit_file

from app.tools.executor import run_python


tools = [
    list_directory,
    read_file,
    search_files,
    find_file,
    edit_file,
    run_python
]

tool_registry = {
    tool.name: tool for tool in tools
}

llm_with_tools = llm.bind_tools(tools)




def execute_tool(tool_call):
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    tool = tool_registry.get(tool_name)

    if tool is None:
        return f" Error Unknown Tool '{tool_name}' "

    return tool.invoke(tool_args)





def run_agent(user_input: str, max_iterations: int = 10):

    messages = [
        HumanMessage(content=user_input)
    ]

    for _ in range(max_iterations):

        response = llm_with_tools.invoke(messages)

        messages.append(response) # type: ignore

        if not response.tool_calls:
            return response.content

        for tool_call in response.tool_calls:

            result = execute_tool(tool_call)

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                ) # type: ignore
            )

    return "Agent stopped because the maximum number of iterations was reached."
