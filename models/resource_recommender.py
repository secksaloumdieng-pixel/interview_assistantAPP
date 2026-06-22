import json
from openai import OpenAI


def get_weak_topics(evaluation):
    weak_topics = []

    for item in evaluation.get("answers", []):
        score = item.get("score", 0)
        question = item.get("q", "").lower()
        feedback = item.get("feedback", "").lower()

        if score < 75:
            if "behavioral" in feedback or "behavioral" in question:
                weak_topics.append("behavioral")
            elif "technical" in feedback or "technical" in question:
                weak_topics.append("technical")
            elif "situational" in feedback or "situational" in question:
                weak_topics.append("situational")
            elif "leadership" in feedback or "team" in question:
                weak_topics.append("leadership")
            elif "communication" in feedback:
                weak_topics.append("communication")
            elif "time" in question or "schedule" in question:
                weak_topics.append("time_management")
            elif "safety" in question or "safety" in feedback:
                weak_topics.append("safety")
            else:
                weak_topics.append("technical")

    return list(set(weak_topics))


def get_local_resources(weak_topics):
    with open("models/resources.json", "r") as file:
        resources_data = json.load(file)

    recommendations = []

    for topic in weak_topics:
        if topic in resources_data:
            for resource in resources_data[topic]:
                recommendations.append({
                    "topic": topic,
                    "title": resource["title"],
                    "url": resource["url"],
                    "description": resource["description"],
                    "source": "local_library"
                })

    return recommendations


def get_ai_recommendations(evaluation):
    client = OpenAI(timeout=30.0)

    prompt = f"""
You are an interview coach.

Based on this interview evaluation:
{json.dumps(evaluation, indent=2)}

Suggest 3 useful learning resources for the candidate.

Return only valid JSON in this format:
{{
  "resources": [
    {{
      "topic": "behavioral",
      "title": "Resource title",
      "url": "https://example.com",
      "description": "Short explanation"
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You recommend interview preparation resources and return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
    )

    content = response.choices[0].message.content
    print("AI resource raw response:", content)

    try:
        data = json.loads(content)
        resources = data.get("resources", [])

        for resource in resources:
            resource["source"] = "ai"

        return resources
    except Exception:
        return []


def recommend_resources(evaluation):
    weak_topics = get_weak_topics(evaluation)
    local_resources = get_local_resources(weak_topics)
    ai_resources = get_ai_recommendations(evaluation)

    all_resources = local_resources + ai_resources
    unique_resources = []
    seen = set()

    for resource in all_resources:
        key = (resource.get("title", "").lower(), resource.get("url", "").lower())

        if key not in seen:
            seen.add(key)
            unique_resources.append(resource)

    return unique_resources