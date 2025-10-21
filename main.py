from llm import generate_quiz
from input import get_topic, get_difficulty, get_level
from quiz import get_answers, calculate_score, show_answers, persist_results

def main():
    topic = get_topic()
    difficulty = get_difficulty()
    level = get_level()
    quiz = generate_quiz(topic, difficulty, level)

    if not quiz:
        print("Failed to generate quiz. Exiting")
        return

    print("Quiz generated successfully!")
    print(f"Topic: {quiz.get('topic', 'N/A')}")
    
    # Get the questions from the quiz
    questions = quiz.get('questions', [])

    # Prompt the user to answer each question and record responses
    user_answers = get_answers(questions)

    # Calculate and display the score
    score = calculate_score(questions, user_answers)
    print(f"\nFinal score: {score}/{len(questions)}")

    # Show correct answers and explanations
    show_answers(questions, user_answers)

    # Save results to CSV
    persist_results(questions, user_answers, topic, difficulty, level, score)


if __name__ == "__main__":
    main()