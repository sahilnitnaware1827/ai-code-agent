from pathlib import Path

from langchain_core.tools import tool

from app.tools.executor import WORKSPACE


@tool
def edit_file(
    path: str,
    old_text: str,
    new_text: str,
) -> str:
    """
    Preview an exact text replacement inside a workspace file.

    This tool does NOT modify the file.

    The old_text must exist exactly once.
    """

    file = Path(path).resolve()

    try:
        file.relative_to(WORKSPACE)
    except ValueError:
        return "Error: file is outside the allowed workspace"

    if not file.exists():
        return "Error: file does not exist"

    if not file.is_file():
        return "Error: path is not a file"

    try:
        content = file.read_text(
            encoding="utf-8"
        )
    except UnicodeDecodeError:
        return "Error: file is not a UTF-8 text file"

    occurrences = content.count(old_text)

    if occurrences == 0:
        return "Error: old_text was not found"

    if occurrences > 1:
        return "Error: old_text appears multiple times"

    return (
        "EDIT PREVIEW\n"
        f"File: {path}\n\n"
        "OLD:\n"
        f"{old_text}\n\n"
        "NEW:\n"
        f"{new_text}\n\n"
        "Approval required before applying this change."
    )


@tool
def apply_file_edit(
    path: str,
    old_text: str,
    new_text: str,
) -> str:
    """
    Apply an approved exact text replacement
    to a workspace file.
    """

    file = Path(path).resolve()

    try:
        file.relative_to(WORKSPACE)
    except ValueError:
        return "Error: file is outside the allowed workspace"

    if not file.exists():
        return "Error: file does not exist"

    if not file.is_file():
        return "Error: path is not a file"

    try:
        content = file.read_text(
            encoding="utf-8"
        )
    except UnicodeDecodeError:
        return "Error: file is not a UTF-8 text file"

    if content.count(old_text) != 1:
        return "Error: old_text must occur exactly once"

    updated_content = content.replace(
        old_text,
        new_text,
        1,
    )

    file.write_text(
        updated_content,
        encoding="utf-8",
    )

    return f"Successfully applied edit to {path}"

