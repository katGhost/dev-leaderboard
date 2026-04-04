import os
import requests
import json
import re

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_next_projects(user_activity_summary):
    prompt = f"""
You are an expert senior software engineer and developer mentor.

Your task is to analyze a developer profile and generate personalized project recommendations to help them improve.

## Developer Profile
- Experience Level: {user_activity_summary.get('experience_level', 'unknown')}
- Primary Languages: {', '.join(user_activity_summary.get('languages_used', []))}
- Weekly Activity: {user_activity_summary.get('commits_last_week', 0)}
- Strengths: {user_activity_summary.get('total_commits', 0)}
- Weaknesses / Gaps: {user_activity_summary.get('total_commits', 0) + user_activity_summary.get('commits_last_week', 0) - user_activity_summary.get('total_commits', 0)}

## Instructions
Based on the profile:

1. Suggest EXACTLY 3 projects tailored to this developer.
2. Projects must be realistic, practical, and appropriate for their level.
3. Avoid generic ideas (e.g., "build a todo app" unless justified and upgraded).
4. Focus on improving their weaknesses while leveraging strengths.

## Output Format (STRICT)
Return ONLY this structure:

[
  {
    "title": "Project Title",
    "description": "Simple 1-3 sentence explanation of the project",
    "learning_outcome": "What the developer will learn from this project"
  }
]

## Quality Guidelines
- Keep descriptions concise and clear
- Make projects feel like real-world applications
- Ensure increasing difficulty across the 3 projects
- Tailor suggestions to the developer’s languages and activity level
"""

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                # free and actively available on OpenRouter -> have to pay $5
                # free not available -> no endpoints reached
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
            }
        )

        data = response.json()
        print('MODEL RAW RESPONSE:', json.dumps(data, indent=2))
        content = data["choices"][0]["message"]["content"].strip()

        # strip markdown code fences if model wraps response in them
        content = re.sub(r"```json|```", "", content).strip()

        suggestions = json.loads(content)

        # guard against model returning something other than a list
        if not isinstance(suggestions, list):
            raise ValueError("Response is not a list")

        return suggestions

    except Exception as e:
        print(f"AI generation error: {e}")
        # always return a list so the template loop does not break
        return [
            {
                "title": "Could not load suggestions",
                "description": "There was an issue generating your roadmap. Try again later.",
                "learning_outcome": ""
            }
        ]








# completion=client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are an expert florist helpdesk assistant"
#         },
#         {
#             "role": "user",
#             "content": "Are Lilys the best flowers for a wedding?"
#         }
#     ]
# )

# res = completion.choices[0].message.content
# print(res)

# def suggest_projects(user):
#     suggestions = {
#         "Python": [
#             "Build a Flask REST API",
#             "Contribute to a Python open-source repo",
#             "Create a CLI tool"
#         ],
#         "JavaScript": [
#             "Build a React app",
#             "Contribute to a JS repo",
#             "Create a browser extension"
#         ]
#     }

#     return suggestions.get(user, ["Explore open source projects"])