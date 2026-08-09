from app.agent import run_agent


response = run_agent(
    "Find main.py inside workspace/sample_project, "
    "read it, and tell me what functions it contains."
)

print("AI:", response)
