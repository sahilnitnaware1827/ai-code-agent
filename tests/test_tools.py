# test tool.py file 

from app.tools import list_directory
from app.tools import read_file

result = list_directory("workspace/sample_project")

print("\n Files", result)


print("\n\n main.py >>> ")
print(read_file("workspace/sample_project/main.py"))
