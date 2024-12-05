from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        custom_header = request.headers.get('X-Custom-Header')
        if request.url.path.startswith('/docs') or request.url.path.startswith('/openapi.json') or request.url.path.startswith('/redoc'):
            response = await call_next(request)
            return response
        if not custom_header or custom_header != "Token123":
            return Response("Invalid or missing custom header", status_code=400)
        response = await call_next(request)
        response.headers['X-Custom-Header'] = custom_header
        return response
        