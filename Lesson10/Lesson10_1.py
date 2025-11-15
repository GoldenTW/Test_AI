import os
from tools import gear


def main():
    names = gear.get_names("names.txt")
    if not names:
        print("無可用姓名，程式結束。")
        return
    try:
        num = int(input("請輸入要產生幾位學生的成績資料: "))
        if num < 1:
            print("人數需大於 0。")
            return
    except ValueError:
        print("請輸入有效的整數。")
        return
    students = gear.generate_student_scores(names, num=num)
    if students:
        gear.save_file_csv(students, file_name='students.csv')
        print(f"已產生 {num} 位學生的成績資料，並存成 students.csv 檔案")

if __name__ == '__main__':  #主執行檔
    main()