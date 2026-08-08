# test tool.py file 

from app.tools.filesystem import list_directory, read_file
from app.tools.search import search_files, find_file

result = list_directory("workspace/sample_project")

print("\n Files", result)


print("\n\n main.py >>> ")
print(read_file("workspace/sample_project/main.py"))


print("\n\n Search Result >>> ")
print(search_files("workspace/sample_project", "calculate_total"))


print("\n\n find config.py >>> ")
print(find_file("workspace/sample_project", "config.py"))
