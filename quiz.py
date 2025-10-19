import csv
from datetime import datetime



def get_answers(questions):
    user_answers = []
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question.get('question', 'N/A')}")
        choices = question.get('choices', [])
        for j, choice in enumerate(choices):
            print(f"  {chr(65+j)}. {choice}")

        ans_index = None
        while True:
            resp = input("Your answer (A-D or 1-4): ").strip().upper()
            if not resp:
                print("Please enter A-D or 1-4.")
                continue
            if resp in ("A", "B", "C", "D"):
                ans_index = ord(resp) - 65
            elif resp in ("1", "2", "3", "4"):
                ans_index = int(resp) - 1
            else:
                print("Invalid input. Enter A, B, C, D or 1-4.")
                continue

            if 0 <= ans_index < len(choices):
                break
            else:
                print("Choice out of range. Try again.")

        user_answers.append(ans_index)
    return user_answers


def calculate_score(questions, user_answers):
    score = 0
    for q, ua in zip(questions, user_answers):
        correct = q.get('correct_index', 0)
        if ua == correct:
            score += 1
    return score


def show_answers(questions, user_answers):
    print("\nCorrect answers and explanations:")
    for i, (q, ua) in enumerate(zip(questions, user_answers), 1):
        correct = q.get('correct_index', 0)
        choices = q.get('choices', [])
        user_letter = chr(65 + ua) if 0 <= ua < len(choices) else "N/A"
        correct_letter = chr(65 + correct) if 0 <= correct < len(choices) else "N/A"
        user_choice = choices[ua] if 0 <= ua < len(choices) else "N/A"
        correct_choice = choices[correct] if 0 <= correct < len(choices) else "N/A"

        print(f"\nQuestion {i}: {q.get('question', 'N/A')}")
        print(f"  Your answer: {user_letter}. {user_choice}")
        print(f"  Correct answer: {correct_letter}. {correct_choice}")
        print(f"  Explanation: {q.get('explanation', 'N/A')}")


def persist_results(questions, user_answers, topic, difficulty, level, score):
    timestamp = datetime.now().isoformat(timespec="seconds")
    filename = f"quiz_results_{datetime.now().strftime('%Y%m%d')}.csv"

    fieldnames = [
        "timestamp", "topic", "difficulty", "level", "question_index",
        "question", "user_answer", "correct_answer", "is_correct", "explanation", "total_score", "total_questions"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for idx, q in enumerate(questions):
            # extract fields robustly from various possible quiz formats
            q_text = q.get("question") if isinstance(q, dict) else str(q)
            correct = q.get("answer") if isinstance(q, dict) else q.get("correct") if isinstance(q, dict) else ""
            if isinstance(q, dict):
                correct = q.get("answer", q.get("correct", q.get("correct_answer", "")))
            explanation = q.get("explanation", "") if isinstance(q, dict) else ""

            # support list or dict user_answers
            user_ans = ""
            if isinstance(user_answers, dict):
                # try numeric index keys and string keys
                user_ans = user_answers.get(idx, user_answers.get(str(idx), ""))
            elif isinstance(user_answers, (list, tuple)):
                user_ans = user_answers[idx] if idx < len(user_answers) else ""

            is_correct = str(user_ans).strip().lower() == str(correct).strip().lower()

            writer.writerow({
                "timestamp": timestamp,
                "topic": topic,
                "difficulty": difficulty,
                "level": level,
                "question_index": idx,
                "question": q_text,
                "user_answer": user_ans,
                "correct_answer": correct,
                "is_correct": is_correct,
                "explanation": explanation,
                "total_score": score,
                "total_questions": len(questions)
            })