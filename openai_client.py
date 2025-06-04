from app.config import OPENAI_API_KEY
from openai import OpenAI

# Initialize the client with the API key
client = OpenAI(api_key=OPENAI_API_KEY)

def ask_llm(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a code reviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content
