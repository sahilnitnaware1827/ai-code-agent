# to search the file 

from pathlib import Path

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
        