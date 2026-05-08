"""
Chat and conversation endpoints
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.engine import get_db
from app.database.models import ChatMessage, Repository
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


class ChatMessageRequest(BaseModel):
    """Chat message request."""
    message: str
    conversation_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    """Chat message response."""
    id: str
    role: str
    content: str
    sources: Optional[Dict[str, Any]]
    created_at: datetime


@router.post("/{repository_id}/message", response_model=ChatMessageResponse)
async def send_chat_message(
    repository_id: str,
    request: ChatMessageRequest,
    db: AsyncSession = Depends(get_db),
):
    """Send a chat message to analyze repository."""
    
    stmt = select(Repository).where(Repository.id == repository_id)
    result = await db.execute(stmt)
    repo = result.scalars().first()
    
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found"
        )
    
    user_message = ChatMessage(
        repository_id=repository_id,
        user_id="test_user",
        role="user",
        content=request.message,
        conversation_id=request.conversation_id,
    )
    
    db.add(user_message)
    await db.commit()
    await db.refresh(user_message)
    
    logger.info(f"Chat message received for repo {repository_id}")
    
    return ChatMessageResponse(
        id=user_message.id,
        role="user",
        content=user_message.content,
        sources=None,
        created_at=user_message.created_at,
    )


@router.get("/{repository_id}/history", response_model=List[ChatMessageResponse])
async def get_chat_history(
    repository_id: str,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """Get chat history for a repository."""
    
    stmt = select(ChatMessage).where(
        ChatMessage.repository_id == repository_id
    ).order_by(ChatMessage.created_at.desc()).limit(limit)
    
    result = await db.execute(stmt)
    messages = result.scalars().all()
    
    return [
        ChatMessageResponse(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            sources=msg.sources,
            created_at=msg.created_at,
        )
        for msg in reversed(messages)
    ]
