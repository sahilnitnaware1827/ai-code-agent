from app.tools.sandbox import run_python_sandbox


result = run_python_sandbox.invoke({
    "path": "workspace/sample_project/bug.py"
})

print(result)

