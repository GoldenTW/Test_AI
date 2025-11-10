import os

relative_path = 'Lesson8/assets/names.txt'
absolute_path = os.path.abspath(relative_path)


with open(absolute_path, 'r', encoding='utf-8') as f:
    content = f.read()

names_list = content.split(',')

print(names_list)