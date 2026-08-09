from pathlib import Path

from langchain_core.tools import tool


WORKSPACE = Path("workspace/sample_project").resolve()


@tool
def edit_file(
    path: str,
    old_text: str,
    new_text: str,
    apply: bool = False,
) -> str:
    """
    Preview or apply an exact text replacement inside a workspace file.
    Set apply=True only when the change has been approved.
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
        content = file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "Error: file is not UTF-8 text"

    occurrences = content.count(old_text)

    if occurrences == 0:
        return "Error: old_text was not found"

    if occurrences > 1:
        return "Error: old_text appears multiple times"

    updated_content = content.replace(old_text, new_text, 1)

    if not apply:
        return (
            "EDIT PREVIEW\n\n"
            f"File: {path}\n\n"
            "OLD:\n"
            f"{old_text}\n\n"
            "NEW:\n"
            f"{new_text}\n\n"
            "Approval required before applying this change."
        )

    file.write_text(updated_content, encoding="utf-8")

    return f"Successfully edited {path}"