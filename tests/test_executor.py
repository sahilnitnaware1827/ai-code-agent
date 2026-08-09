from app.tools.executor import run_python


result = run_python.invoke({
    "path": "workspace/sample_project/bug.py"
})

print(result)
