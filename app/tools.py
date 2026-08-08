from pathlib import Path

def list_directory(path: str) -> list[str]:
    '''
        List files and directories inside the given path
    '''

    directory = Path(path)

    if not directory.exists():
        return [" Error: Directory does not exist"]

    if not directory.is_dir():
        return ["Error: Path is not a directory "]

    return [item.name for item in directory.iterdir()]

