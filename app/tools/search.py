# to search the file 

from pathlib import Path
from langchain_core.tools import tool


''' Find which files contain this code/text. '''
@tool
def search_files(directory: str, query: str) -> list[str]:
    '''
        search for a text pattern inside files under a dictionary
    '''

    root = Path(directory)

    if not root.exists():
        return ["Error: Directory does not exist"]

    if not root.is_dir():
        return ["Error: Path is not a dorectory "]

    result = []

    for file in root.rglob("*"):

        if not file.is_file():
            continue

        try:
            content = file.read_text(encoding="utf-8")

        except (UnicodeDecodeError, PermissionError):
            continue

        if query.lower() in content.lower():
            result.append(str(file))

    return result




''' Find where this filename exists '''
@tool
def find_file(directory: str, filename: str) -> list[str]:
    """
    Find files with a specific filename inside a directory recursively.
    """

    root = Path(directory)

    if not root.exists():
        return ["Error: directory does not exist"]

    if not root.is_dir():
        return ["Error: path is not a directory"]

    results = []

    for file in root.rglob("*"):

        if not file.is_file():
            continue

        if file.name.lower() == filename.lower():
            results.append(str(file))

    return results        
