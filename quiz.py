from huggingface_hub import InferenceClient
import json

SYSTEM = "You are a strict quiz generator that returns only valid JSON."
USER_TMPL = """Topic: {topic}
Please return exactly 5 MCQs with 4 options (A–D) and one correct answer.
JSON schema:
{{
  "topic": "<string>",
  "questions": [
    {{
      "question": "<string>",
      "options": {{"A":"<string>","B":"<string>","C":"<string>","D":"<string>"}},
      "answer": "<A|B|C|D>"
    }}
  ]
}}
No explanations. JSON only.
"""

def generate_quiz_hf(topic: str, model="Qwen/Qwen2.5-7B-Instruct", hf_token=None):
    client = InferenceClient(model=model, token=hf_token)
    prompt = USER_TMPL.format(topic=topic)
    # Simple chat turn for instruct models:
    resp = client.chat_completion(
        messages=[{"role":"system","content":SYSTEM},{"role":"user","content":prompt}],
        max_tokens=1200, temperature=0.7
    )
    text = resp.choices[0].message["content"].strip()
    data = json.loads(text)
    # (optional) same validations as above…
    return data

if __name__ == "__main__":
    quiz = generate_quiz_hf("Cell Biology (High School)")
    print(json.dumps(quiz, indent=2, ensure_ascii=False))