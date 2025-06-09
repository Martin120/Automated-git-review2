from flask import Flask, request, jsonify
from agents.code_review import CodeReviewAgent
from utils.github import fetch_diff, post_comment, fetch_pr_metadata, convert_github_url_to_api



app = Flask(__name__)
agent = CodeReviewAgent()

app.config['DEBUG'] = True


@app.route("/mcp", methods=["POST"])
def mcp_entrypoint():
    try:    
        context = request.json
        result = agent.run(context)
        return jsonify(result), 200
    except Exception as e:
        print("MCP ERROR:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/review", methods=["POST"])
def github_review():
    try:
        context = request.json
        repo = context["repo"]
        pr_number = context["pr_number"]

        result = agent.run(context)

        comment = f"""### 🤖 AI Code Review

**Summary**  
{result.get('summary')}

**Detected Issues**  
{result.get('issues')}

**Style Feedback**  
{result.get('style')}
"""

        post_comment(repo, pr_number, comment)
        return jsonify({"status": "comment posted"}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@app.route("/fetch-pr", methods=["POST"])
def fetch_pr():
    try:
        payload = request.json
        pr_url = payload.get("url")

        if not pr_url:
            return jsonify({"error": "Missing PR URL"}), 400

        api_url = convert_github_url_to_api(pr_url)
        data = fetch_pr_metadata(api_url)
        return jsonify(data), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    

#For automation combined endpoint, expose this to ngrok and set as GitHub webhook URL    
@app.route("/webhook", methods=["POST"])
def webhook_auto_review():
    try:
        payload = request.json
        web_url = payload.get("pull_request", {}).get("html_url")

        if not web_url:
            return jsonify({"error": "No pull request URL found"}), 400

        # Convert to API URL
        api_url = convert_github_url_to_api(web_url)
        context = fetch_pr_metadata(api_url)
        result = agent.run(context)

        comment = f"""### 🤖 AI Code Review

**Summary**  
{result.get('summary')}

**Detected Issues**  
{result.get('issues')}

**Style Feedback**  
{result.get('style')}
"""

        post_comment(context["repo"], context["pr_number"], comment)

        return jsonify({"status": "AI review completed"}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
