from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request

class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_size: int):
        super().__init__(app)
        self.max_size = max_size  # Set the max request body size in bytes

    async def dispatch(self, request: Request, call_next):
        body = await request.body()  # Read the body content
        if len(body) > self.max_size:  # Check if the body size exceeds the limit
            return JSONResponse({"detail": "Request body too large"}, status_code=413)
        return await call_next(request)  # Proceed to the next middleware or request handler
