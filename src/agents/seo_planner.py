from openai import OpenAI
import json
import os

client = OpenAI(
    model="gemini-2.5-flash", # Or 'gemini-1.5-pro'
    api_key=os.getenv("LITELLM_KEY"),
)

PLANNER_PROMPT = """
You are a query planner for SEO audit data.

Allowed fields:
- url
- protocol
- title_length
- meta_description
- indexability
- meta_missing
- meta_duplicate

Allowed operations:
- filter (eq, neq, gt, lt)
- group_by
- aggregate (count, percentage)

Output a VALID JSON plan.
Do not explain.
"""

def generate_plan(query: str) -> dict:
    resp = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": query}
        ]
    )

    return json.loads(resp.choices[0].message.content)
