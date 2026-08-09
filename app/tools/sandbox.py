from pathlib import Path
import subprocess

from langchain_core.tools import tool


WORKSPACE = Path("workspace/sample_project").resolve()


@tool
def run_python_sandbox(path: str) -> str:
    """
    Execute a Python file inside an isolated Docker container.
    """

    file = Path(path).resolve()

    # Make sure the file is inside the allowed workspace
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

    command = [
        "docker",
        "run",
        "--rm",
        "--network", "none",
        "--memory", "256m",
        "--cpus", "0.5",
        "--pids-limit", "64",
        "--read-only",
        "-v",
        f"{WORKSPACE.as_posix()}:/app:ro",
        "python:3.11-slim",
        "python",
        f"/app/{file.relative_to(WORKSPACE).as_posix()}",
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
        )

    except subprocess.TimeoutExpired:
        return "Execution stopped: timeout exceeded."

    except FileNotFoundError:
        return "Error: Docker is not available."

    except Exception as exc:
        return f"Execution error: {exc}"

    output = []

    if result.stdout:
        output.append(f"STDOUT:\n{result.stdout}")

    if result.stderr:
        output.append(f"STDERR:\n{result.stderr}")

    output.append(f"EXIT CODE: {result.returncode}")

    return "\n".join(output)

