from fastapi import APIRouter, Request, HTTPException
import json
from app.openai_client import ask_llm
from app.prompt_templates import PR_SUMMARY_PROMPT, CODE_ISSUE_PROMPT, STYLE_FEEDBACK_PROMPT
from app.github_api import post_pr_comment
from app.config import GITHUB_TOKEN

router = APIRouter()

@router.post("/")
async def review_action(request: Request):
    try:
        body = await request.json()
        metadata = body["metadata"]
        diff = body["diff"]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    metadata_str = json.dumps(metadata, indent=2)

    #extract owner, repo, pr_number from metadata
    try:
        owner = metadata["head"]["repo"]["owner"]["login"]
        repo = metadata["head"]["repo"]["name"]
        pr_number = int(metadata["number"])
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required metadata field: {str(e)}")
    

    summary = ask_llm(PR_SUMMARY_PROMPT.format(metadata=metadata_str, diff=diff))
    issues = ask_llm(CODE_ISSUE_PROMPT.format(diff=diff))
    style_feedback = ask_llm(STYLE_FEEDBACK_PROMPT.format(diff=diff))

    # Compose GitHub PR comment body
    comment_body = f"""## 🤖 Automated Code Review

### Summary:
{summary}

### Issues Detected:
{issues}

### Style Feedback:
{style_feedback}
"""
    
# Post comment to GitHub PR
    try:
        post_pr_comment(owner, repo, pr_number, comment_body, GITHUB_TOKEN)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to post comment: {e}")


    return {
        "status": "success",
        "summary": summary,
        "issues": issues,
        "style_feedback": style_feedback,
        "comment_posted": True
    }