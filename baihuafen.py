"""
百化分背诵程序

题库中的百化分随机出题，转化为小数，辅助记忆

另外包括一些平方数与立方数的计算

"""

import random

# 百分数题库
percentage_questions = {
    "50.0%": "2",
    "33.3%": "3",
    "25.0%": "4",
    "20.0%": "5",
    "16.7%": "6",
    "14.3%": "7",
    "12.5%": "8",
    "11.1%": "9",
    "10.0%": "10",
    "9.1%": "11",
    "8.3%": "12",
    "7.7%": "13",
    "7.1%": "14",
    "6.7%": "15",
    "6.2%": "16",
    "5.9%": "17",
    "5.6%": "18",
    "5.3%": "19",
    "5.0%": "20",
    "42.0%": "2.4",
    "40.0%": "2.5",
    "37.0%": "2.7",
    "28.6%": "3.5",
    "22.2%": "4.5",
    "18.2%": "5.5",
    "15.4%": "6.5",
    "13.3%": "7.5",
    "11.8%": "8.5",
    "10.5%": "9.5",
    "9.5%": "10.5"
}

# 幂运算题库
power_questions = {
    "11²": "121",
    "12²": "144",
    "13²": "169",
    "14²": "196",
    "15²": "225",
    "16²": "256",
    "17²": "289",
    "18²": "324",
    "19²": "361",
    "21²": "441",
    "22²": "484",
    "23²": "529",
    "24²": "576",
    "25²": "625",
    "26²": "676",
    "27²": "729",
    "28²": "784",
    "29²": "841",
    "1.2³": "1.73",
    "1.3³": "2.2",
    "1.4³": "2.74",
    "1.2⁴": "2.07",
    "1.3⁴": "2.86",
    "1.4⁴": "3.84"
}

def percentage_to_decimal():
    question, answer = random.choice(list(percentage_questions.items()))
    return question, answer

def power_calculation():
    question, answer = random.choice(list(power_questions.items()))
    return question, answer

def get_practice_count():
    while True:
        try:
            count = input("请输入题目数量：1-54 ( 'quit'或'q' 退出): ").strip()
            if count.lower() == 'quit' or count.lower() == 'q':
                return None
            count = int(count)
            if 0 < count < 55:
                return count
            else:
                print("小于0或超出题库范围!")
        except ValueError:
            print("请输入有效的数字!")


def main():
    print("欢迎使用练习程序!")
    print("=" * 35)
    #print(len(percentage_questions)+len(power_questions))

    while True:
        # 获取练习次数
        practice_count = get_practice_count()
        if practice_count is None:
            print("Bye!")
            break

        correct_count = 0
        wrong_answers = []

        # 创建当前练习会话的题库副本，避免重复出题
        percentage_pool = list(percentage_questions.items())
        power_pool = list(power_questions.items())

        # 随机打乱题库顺序
        random.shuffle(percentage_pool)
        random.shuffle(power_pool)

        for i in range(practice_count):
            print(f"\n第 {i + 1}/{practice_count} 题")

            # 选择题目类型
            is_percentage = random.random() < 0.8 and percentage_pool
            question_pool = percentage_pool if is_percentage else power_pool

            # 如果没有题目可用，尝试使用另一种类型
            if not question_pool:
                question_pool = power_pool if is_percentage else percentage_pool
                if not question_pool:
                    print("所有题目都已出完!")
                    break

            # 获取题目
            question, answer = question_pool.pop()
            question_type = "百分数转分数" if is_percentage else "幂运算"

            # 处理题目
            if is_percentage:
                print(f"题目类型: {question_type}")
                print(f"问题: {question} = ? (只填写分母n即可)")
                user_input = input("你的答案: 1/").strip()
            else:
                print(f"题目类型: {question_type}")
                print(f"问题: {question} = ?")
                user_input = input("你的答案: ").strip()

            # 检查是否退出
            if user_input.lower() in ('quit', 'q'):
                print("练习退出!")
                break

            # 检查答案
            is_correct = False
            if is_percentage:
                is_correct = user_input == answer
                if not is_correct:
                    wrong_answers.append([question, f"1/{answer}"])
            else:
                try:
                    is_correct = abs(float(user_input) - float(answer)) < 0.03
                    if not is_correct:
                        wrong_answers.append([question, answer])
                except ValueError:
                    wrong_answers.append([question, answer])

            # 更新计数和显示结果
            if is_correct:
                print("✓ 正确!")
                correct_count += 1
            else:
                correct_answer = f"1/{answer}" if is_percentage else answer
                print(f"✗ 错误! 正确答案是: {correct_answer}")

            print("=" * 35)

        # 显示本次练习结果
        if practice_count > 0:
            accuracy = (correct_count / practice_count) * 100
            print(f"\n本次练习结果: {correct_count}/{practice_count} 正确 ({accuracy:.1f}%)")
            if wrong_answers:
                print("\n错误项与正确答案:")
                for question, answer in wrong_answers:
                    print(f"  {question} = {answer}")
            print("=" * 35)

        # 询问是否继续练习
        continue_choice = input("是否继续练习? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("感谢使用，再见!")
            break

if __name__ == "__main__":
    main()