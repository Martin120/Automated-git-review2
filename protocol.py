class Context:
    def __init__(self, repo_url, pr_id):
        self.repo_url = repo_url
        self.pr_id = pr_id

class Action:
    def execute(self, context: Context):
        raise NotImplementedError("Must implement in subclass")