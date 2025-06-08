from fastapi import FastAPI
from app2.git_context import router as git_context_router
from app2.review_action import router as review_action_router
from app2.middleware import BodySizeLimitMiddleware

app2 = FastAPI(title="Automated Code Review API")

app2.add_middleware(BodySizeLimitMiddleware, max_size=10000000)  # 10MB limit

app2.include_router(git_context_router, prefix="/context/git")
app2.include_router(review_action_router, prefix="/action/review")

@app2.get("/")
def root():
    return {"message": "MCP server started..."}