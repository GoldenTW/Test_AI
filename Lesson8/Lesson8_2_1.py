

file_name ="/workspaces/Test_AI/Lesson8/assets/names.txt"

with open(file_name, 'r', encoding='utf-8') as f:
    content = f.read()

names_list = content.split('\n')

print(names_list)