from fastapi import APIRouter, Request, HTTPException
from app.github_api import fetch_pr_metadata, fetch_diff
import httpx

router = APIRouter()

@router.post("/load")
async def load_context(request: Request):
    try:
        data = await request.json()
        pr_url = data["pull_request"]["html_url"]
        owner = data["repository"]["owner"]["login"]
        repo = data["repository"]["name"]
        pr_number = data["pull_request"]["number"]

        metadata = fetch_pr_metadata(owner, repo, pr_number)
        diff = fetch_diff(owner, repo, pr_number)

        # Trigger review automatically by calling the /action/review/ endpoint
        payload = {
            "metadata": metadata,
            "diff": diff
        }

        # Use httpx to call your own server
        async with httpx.AsyncClient() as client:
            review_response = await client.post(
                "http://localhost:8000/action/review/",  # Use your ngrok URL in production
                json={"metadata": metadata, "diff": diff}
            )

        # Optionally return review result back to GitHub or for logging
        return review_response.json()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing the PR: {str(e)}"
        )