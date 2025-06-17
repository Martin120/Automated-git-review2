from mcp.core import MCPAgent
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CodeReviewAgent(MCPAgent):
    def __init__(self):
        super().__init__("CodeReviewAgent")

    def _ask(self, prompt: str) -> str:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()

    def run(self, context: dict) -> dict:
        diff = context.get("diff", "")[:10000]  # trim to avoid token overflow
        title = context.get("title", "")
        files = context.get("files", [])
        commits = context.get("commits", [])

        prompt_prefix = f"""PR Title: {title}
    Changed files: {', '.join(files[:10])}
    Commits: {', '.join(commits[:3])}

    Diff:
    {diff}
    """

        return {
            "summary": self._ask(f"Summarize this PR:\n{prompt_prefix}"),
            "issues": self._ask(f"List any bugs/security issues:\n{prompt_prefix}"),
            "style": self._ask(f"Enforce universal best coding standards with updated code \n{prompt_prefix}"),
        }
