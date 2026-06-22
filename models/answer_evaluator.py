import json
from openai import OpenAI


def evaluate_answers(qa_list):
    client = OpenAI(timeout=30.0)

    prompt = f"""
You are an expert interview evaluator.

Below is a list of interview questions and candidate answers:

{json.dumps(qa_list, indent=2)}

Evaluate each answer.

Rules:
- Give each answer a score out of 100
- Give short and useful feedback for each answer
- Give one overall score out of 100
- Return only valid JSON
- Use this format:

{{
  "overall_score": 85,
  "answers": [
    {{
      "q": "question text",
      "a": "answer text",
      "score": 80,
      "feedback": "Clear answer but could be more specific."
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You evaluate interview answers and return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content
    print("Evaluation raw response:", content)

    data = json.loads(content)
    return data