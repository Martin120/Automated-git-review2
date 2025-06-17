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
        ai_response = response.choices[0].message.content.strip()
        print("AI Response:", ai_response)  # Add debug output here
        return ai_response

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
        prompt = f"""
        You are an expert code reviewer.
        Below is a code snippet (diff). Please:
        1. Suggest improvements following best practices such as:
            - Improving readability and add clear and understandable comments for functions and complex logic
            - Ensuring code is modular and follows the DRY (Don't Repeat Yourself) principle
            - Error handling
            - Optimizing performance
            - Using appropriate variable and function names
            - Ensuring security best practices
        2. Provide a refactored version of the code based on the improvements above, following the best coding standards.
    
        Diff:
        {diff}
        """

        return {
            "summary": self._ask(f"Summarize this PR and its functionality:\n{prompt_prefix}"),
            "issues": self._ask(f"List any bugs, security issues, or code smells in the following code:\n{prompt_prefix}"),
            "updated_code": self._ask(prompt)  
        }
