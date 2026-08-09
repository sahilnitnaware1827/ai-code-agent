import subprocess
import sys
from pathlib import Path

from langchain_core.tools import tool


WORKSPACE = Path("workspace/sample_project").resolve()


@tool
def run_python(path: str) -> str:
    """
    Run a Python file inside the agent workspace and return its output or error.
    """

    file = Path(path).resolve()

    # Security check
    try:
        file.relative_to(WORKSPACE)
    except ValueError:
        return "Error: file is outside the allowed workspace"

    if not file.exists():
        return "Error: file does not exist"

    if not file.is_file():
        return "Error: path is not a file"

    if file.suffix != ".py":
        return "Error: only Python files can be executed"

    try:
        result = subprocess.run(
            [sys.executable, str(file)],
            capture_output=True,
            text=True,
            timeout=10
        )

    except subprocess.TimeoutExpired:
        return "Error: program exceeded the 10-second timeout"

    except Exception as exc:
        return f"Error while executing program: {exc}"

    output = []

    if result.stdout:
        output.append(f"STDOUT:\n{result.stdout}")

    if result.stderr:
        output.append(f"STDERR:\n{result.stderr}")

    output.append(f"EXIT CODE: {result.returncode}")

    return "\n".join(output)
