from app.agent import run_agent


response = run_agent(
    """
    Inspect workspace/sample_project/bug.py.
    Find the bug, fix it, run the program,
    and verify that it works.
    """
)

print("AI:", response)
