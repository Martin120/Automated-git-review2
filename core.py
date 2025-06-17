class MCPAgent:
    def __init__(self, name: str):
        self.name = name

    def run(self, context: dict) -> dict:
        raise NotImplementedError("MCPAgent must implement run(context)")
