from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("testing changes")