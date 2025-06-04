from app.config import GITHUB_TOKEN
import httpx

headers = {
  "Authorization": f"Bearer {GITHUB_TOKEN}",
  "Accept": "application/vnd.github.v3+json"
}

def fetch_pr_metadata(owner: str, repo: str, pr_number: int):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    response = httpx.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_diff(owner: str, repo: str, pr_number: int):
    pr_url = f"https://github.com/{owner}/{repo}/pull/{pr_number}.diff"
    
    # Switch to raw diff domain
    pr_url = pr_url.replace("github.com", "patch-diff.githubusercontent.com/raw")
    
    response = httpx.get(pr_url, headers=headers, follow_redirects=True)
    response.raise_for_status()
    return response.text

def post_pr_comment(owner: str, repo: str, pr_number: int, comment_body: str, github_token: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }
    json_payload = {"body": comment_body}
    response = httpx.post(url, headers=headers, json=json_payload)
    response.raise_for_status()
    return response.json()