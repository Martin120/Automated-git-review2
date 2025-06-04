PR_SUMMARY_PROMPT = """
Summarize the following pull request and explain the purpose and risks:
---
PR Metadata:
{metadata}

Code Diff:
{diff}
"""

CODE_ISSUE_PROMPT = """
Analyze the following code diff for bugs, code smells, and security issues:
---
{diff}
"""

STYLE_FEEDBACK_PROMPT = """
Give feedback on code style, best practices, and potential improvements:
---
{diff}
"""
