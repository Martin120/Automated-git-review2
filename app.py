from git_utils import connect_to_repo
from flask import Flask, jsonify
from protocol import Context
from github_api import fetch_pull_requests, fetch_pull_request_diff, fetch_commit_metadata

app = Flask(__name__)

REPO_URL = "https://github.com/Martin120/Automated-git-review2.git"
OWNER = "Martin120"
REPO_NAME = "Automated-git-review2"

@app.route('/analyse', methods=['GET'])
def analyse():
    repo = connect_to_repo(REPO_URL)

    prs =  fetch_pull_requests(OWNER, REPO_NAME)
    if not prs:
        return jsonify({"status": "No pull requests found"})
    
    pr = prs[0]
    pr_number = pr["number"]

    diff = fetch_pull_request_diff(OWNER, REPO_NAME, pr_number)
    commits = fetch_commit_metadata(OWNER, REPO_NAME, pr_number)

    context = Context(REPO_URL, pr_number)


    return jsonify({
        "status": "success",
        "pull_request": pr,
        "diff": diff[:500],
        "commits": commits
    })

if __name__ == "__main__":
    app.run(debug=True)