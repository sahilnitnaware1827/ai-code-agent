# test tool.py file 

from app.tools import list_directory, read_file, search_file

result = list_directory("workspace/sample_project")

print("\n Files", result)


print("\n\n main.py >>> ")
print(read_file("workspace/sample_project/main.py"))


print("\n\n Search Result >>> ")
print(search_file("workspace/sample_project", "calculate_total"))
