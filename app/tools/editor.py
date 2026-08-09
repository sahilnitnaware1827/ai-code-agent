from pathlib import Path

from langchain_core.tools import tool


@tool
def edit_file(path: str, old_text: str, new_text: str) -> str:
    """
    Replace an exact piece of text inside a file.
    The old_text must exist exactly once.
    """

    file = Path(path)

    if not file.exists():
        return "Error: file does not exist"

    if not file.is_file():
        return "Error: path is not a file"

    try:
        content = file.read_text(encoding="utf-8")

    except UnicodeDecodeError:
        return "Error: file is not a UTF-8 text file"

    occurrences = content.count(old_text)

    if occurrences == 0:
        return "Error: old_text was not found"

    if occurrences > 1:
        return "Error: old_text appears multiple times"

    updated_content = content.replace(old_text, new_text, 1)

    file.write_text(updated_content, encoding="utf-8")

    return f"Successfully edited {path}"