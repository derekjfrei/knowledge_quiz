import json
import requests


# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_quiz(topic, difficulty="medium", level="undergrad"):
    """Generate a quiz using Ollama"""
    
    prompt = f"""Generate a 5-question multiple choice quiz on "{topic}" with {difficulty} difficulty, {level} level.

Please format your response as JSON with the following structure:
{{
  "topic": "{topic}",
  "questions": [
    {{
      "question": "Your question here?",
      "choices": ["Option A", "Option B", "Option C", "Option D"],
      "correct_index": 0,
      "explanation": "Explanation of why this answer is correct"
    }}
  ]
}}

Make sure each question has exactly 4 choices and the correct_index is between 0-3. Generate exactly 5 questions."""

    payload = {
        "model": "llama3.2:3b",
        "prompt": prompt,
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
