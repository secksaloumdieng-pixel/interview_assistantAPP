import json
from openai import OpenAI


def generate_questions(cv_text, jd_text=""):
    client = OpenAI(timeout=30.0)

    prompt = f"""
You are an expert interview coach.

Candidate CV:
{cv_text[:4000]}

Job Description:
{jd_text[:4000]}

Generate 20 interview questions based on the candidate's profile and the job description.

Rules:
- Mix behavioral, technical, and situational questions
- Make them realistic and professional
- Return only valid JSON
- Use this format:
{{
  "questions": [
    "Question 1",
    "Question 2"
  ]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You generate interview questions and return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )

    content = response.choices[0].message.content
    data = json.loads(content)

    return data["questions"]
