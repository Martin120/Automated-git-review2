import requests
import os

from dotenv import load_dotenv
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_diff(pr_url: str) -> str:
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    res = requests.get(pr_url, headers=headers)
    return res.text if res.status_code == 200 else ""

def post_comment(repo: str, pr_number: int, message: str):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    requests.post(url, json={"body": message}, headers=headers)

def fetch_pr_metadata(pr_url: str) -> dict:
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # PR object
    pr = requests.get(pr_url, headers=headers).json()
    repo = pr["base"]["repo"]["full_name"]
    number = pr["number"]

    # Diff
    diff_url = pr_url
    diff_headers = headers.copy()
    diff_headers["Accept"] = "application/vnd.github.v3.diff"
    diff = requests.get(diff_url, headers=diff_headers).text

    # Commits
    commits_url = f"https://api.github.com/repos/{repo}/pulls/{number}/commits"
    commits = requests.get(commits_url, headers=headers).json()
    commit_msgs = [c["commit"]["message"] for c in commits]

    # Files
    files_url = f"https://api.github.com/repos/{repo}/pulls/{number}/files"
    files = requests.get(files_url, headers=headers).json()
    changed_files = [f["filename"] for f in files]

    return {
        "repo": repo,
        "pr_number": number,
        "title": pr.get("title"),
        "author": pr.get("user", {}).get("login"),
        "diff": diff,
        "commits": commit_msgs,
        "files": changed_files
    }

def convert_github_url_to_api(pr_web_url: str) -> str:
    """
    Converts a PR URL like https://github.com/user/repo/pull/23
    to https://api.github.com/repos/user/repo/pulls/23
    """
    if "github.com" in pr_web_url and "/pull/" in pr_web_url:
        try:
            path = pr_web_url.replace("https://github.com/", "")
            user, repo, _, pr_number = path.split("/")[:4]
            return f"https://api.github.com/repos/{user}/{repo}/pulls/{pr_number}"
        except Exception as e:
            raise ValueError(f"Invalid GitHub PR URL format: {pr_web_url}")
    raise ValueError("Unsupported URL format")

