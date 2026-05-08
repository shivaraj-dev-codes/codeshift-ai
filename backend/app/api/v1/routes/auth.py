"""
Authentication endpoints
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.database.engine import get_db
from app.database.models import User, AuthProvider, UserRole
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginRequest(BaseModel):
    """Login request body."""
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    """Register request body."""
    email: EmailStr
    name: str
    password: str


class TokenResponse(BaseModel):
    """Token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    """User response."""
    id: str
    email: str
    name: Optional[str]
    avatar_url: Optional[str]
    role: str
    created_at: datetime


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(data: Dict[str, Any], expires_in_hours: int) -> str:
    """Create a JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=expires_in_hours)
    to_encode["exp"] = expire
    to_encode["iat"] = datetime.utcnow()
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Register a new user."""
    stmt = select(User).where(User.email == request.email)
    result = await db.execute(stmt)
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = User(
        email=request.email,
        name=request.name,
        password_hash=hash_password(request.password),
        auth_provider=AuthProvider.EMAIL,
        role=UserRole.USER,
        is_active=True,
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    logger.info(f"New user registered: {user.email}")
    
    access_token = create_jwt_token(
        {"sub": user.id, "email": user.email, "role": user.role.value},
        settings.JWT_EXPIRATION_HOURS
    )
    refresh_token = create_jwt_token(
        {"sub": user.id, "type": "refresh"},
        settings.REFRESH_TOKEN_EXPIRATION_DAYS * 24
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.JWT_EXPIRATION_HOURS * 3600,
    )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Login with email and password."""
    stmt = select(User).where(User.email == request.email)
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user or not verify_password(request.password, user.password_hash or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    user.last_login = datetime.utcnow()
    db.add(user)
    await db.commit()
    
    logger.info(f"User logged in: {user.email}")
    
    access_token = create_jwt_token(
        {"sub": user.id, "email": user.email, "role": user.role.value},
        settings.JWT_EXPIRATION_HOURS
    )
    refresh_token = create_jwt_token(
        {"sub": user.id, "type": "refresh"},
        settings.REFRESH_TOKEN_EXPIRATION_DAYS * 24
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.JWT_EXPIRATION_HOURS * 3600,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: Dict[str, str]):
    """Refresh access token using refresh token."""
    refresh_tok = request.get("refresh_token")
    
    if not refresh_tok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token required"
        )
    
    try:
        payload = jwt.decode(
            refresh_tok,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    access_token = create_jwt_token(
        {"sub": user_id},
        settings.JWT_EXPIRATION_HOURS
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_tok,
        expires_in=settings.JWT_EXPIRATION_HOURS * 3600,
    )
