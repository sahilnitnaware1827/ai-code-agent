from app.llm import llm

from app.tools.filesystem import(
    list_directory,
    read_file
)

from app.tools.search import(
    search_files,
    find_file
)

tools = [
    list_directory,
    read_file,
    search_files,
    find_file
]

llm_with_tools = llm.bind_tools(tools)
