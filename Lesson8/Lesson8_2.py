import os
import random

def get_names(file_name):

    relative_path = "assets/" + file_name
    absolute_path = os.path.abspath(relative_path)

    with open(absolute_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return content.split('\n')

def generate_student_scores(names, num=10):
    Names_randomN = random.sample(names, num)
    scores_list = []
    for name in Names_randomN:
        info = {"姓名": name,
                "國文": random.randint(60, 100),
                "數學": random.randint(60, 100),
                "英文": random.randint(60, 100)
            }
        scores_list.append(info)                        
    return scores_list


names = get_names("names.txt")
num = int(input("請輸入要產生幾位學生的成績資料: "))
students = generate_student_scores(names, num=num)

print(students)