import os
import random
import csv

def get_names(file_name):
    """讀取 assets 目錄下的檔案並回傳姓名列表（過濾空行）"""
    relative_path = os.path.join("assets", file_name)
    absolute_path = os.path.abspath(relative_path)
    try:
        with open(absolute_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return [name for name in content.split('\n') if name.strip()]
    except FileNotFoundError:
        print(f"檔案不存在: {absolute_path}")
        return []

def generate_student_scores(names, num=10):
    """隨機抽取 num 位學生並產生成績"""
    if num > len(names):
        print("人數超過可用姓名數量，請重新輸入。")
        return []
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

def save_file_csv(student_scores, file_name='students.csv'):
    key = student_scores[0].keys()
    relative_path = 'assets/' + file_name
    absolute_path = os.path.abspath(relative_path)

    with open(absolute_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=key)
        writer.writeheader()
        writer.writerows(student_scores)