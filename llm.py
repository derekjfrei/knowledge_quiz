import json
import requests
import wikipedia


# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"


def get_prompt(topic, difficulty="medium", level="undergrad"):
    context = get_context(topic)

    """Construct the prompt for the quiz generation."""
    prompt = (
        f"Generate a {difficulty} multiple-choice quiz on the topic '{topic}' with context: {context} "
        f"for {level} students. The quiz should contain 5 questions. "
        "Each question should have 4 answer choices (A, B, C, D) with one correct answer. "
        "Provide the correct answer index (0-3) and a brief explanation for each question. "
        "Format the output as a JSON object with 'questions' as a list of question objects, "
        "each containing 'question', 'choices', 'correct_index', and 'explanation'."
    )
    return prompt


def get_context(topic: str) -> str:
    try:
        return wikipedia.summary(topic, sentences=6)
    except Exception:
        return ""

def generate_quiz(topic, difficulty="medium", level="undergrad"):
    """Generate a quiz using Ollama"""
    
    payload = {
        "model": "llama3.2:3b",
        "prompt": get_prompt(topic, difficulty, level),
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Parse the JSON response
        quiz_data = json.loads(result['response'])
        return quiz_data
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama. Make sure Ollama is running with: ollama serve")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Raw response: {result.get('response', 'No response')}")
        return None
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return None
