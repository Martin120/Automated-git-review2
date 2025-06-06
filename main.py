from fastapi import FastAPI
from app.git_context import router as git_context_router
from app.review_action import router as review_action_router
from app.middleware import BodySizeLimitMiddleware

app = FastAPI(title="Automated Code Review API")

app.add_middleware(BodySizeLimitMiddleware, max_size=10000000)  # 10MB limit

app.include_router(git_context_router, prefix="/context/git")
app.include_router(review_action_router, prefix="/action/review")

@app.get("/")
def root():
    return {"message": "MCP server started..."}