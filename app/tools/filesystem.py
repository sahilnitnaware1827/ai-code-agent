# to list directiry and read content from file 

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



def read_file(path: str) -> str:
    """
        Read and return content of a text file 
    """

    file = Path(path)

    if not file.exists:
        return "Error: File does not Exist"

    if not file.is_file():
        return "Error: Path is not a file"

    try:
        return file.read_text(encoding="utf-8")

    except UnicodeDecodeError:
        return "Error: file is not a utf-8 text file"

