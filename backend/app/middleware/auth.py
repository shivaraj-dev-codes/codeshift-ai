"""
Authentication middleware
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import jwt

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for token validation and user context."""

    async def dispatch(self, request: Request, call_next):
        public_paths = ["/", "/docs", "/redoc", "/openapi.json", "/api/v1/health", 
                       "/api/v1/auth/login", "/api/v1/auth/register"]
        
        if request.url.path in public_paths:
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization", "")
        
        if not auth_header.startswith("Bearer "):
            return await call_next(request)
        
        token = auth_header.replace("Bearer ", "")
        
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
            user_id = payload.get("sub")
            request.state.user_id = user_id
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
        except jwt.JWTError as e:
            logger.warning(f"Invalid token: {str(e)}")
        
        response = await call_next(request)
        return response
