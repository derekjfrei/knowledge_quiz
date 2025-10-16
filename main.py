from llm import generate_quiz
from quiz import get_answers, calculate_score, show_answers, persist_results
from datetime import datetime
import csv

def main():
    # Generate the quiz
    topic = input("Enter a quiz topic (press Enter to use 'TCP vs UDP'): ").strip()
    if not topic:
        topic = "TCP vs UDP"

    difficulty = input("Difficulty (easy/medium/hard) [default: medium]: ").strip().lower()
    if difficulty not in ("easy", "medium", "hard"):
        difficulty = "medium"

    level = input("Level (undergrad/grad) [default: undergrad]: ").strip().lower()
    if level not in ("undergrad", "grad"):
        level = "undergrad"

    quiz = generate_quiz(topic, difficulty, level)

    if quiz:
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