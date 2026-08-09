from app.tools.editor import edit_file


result = edit_file.invoke({
    "path": "workspace/sample_project/test_edit.py",
    "old_text": 'message = "Hello World"',
    "new_text": 'message = "Hello AI Agent"'
})

print(result)
