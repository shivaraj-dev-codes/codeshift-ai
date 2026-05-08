"""
Repository management endpoints
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.engine import get_db
from app.database.models import Repository, RepositoryStatus, User
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


class RepositoryCreate(BaseModel):
    """Repository creation request."""
    name: str
    description: Optional[str] = None


class RepositoryResponse(BaseModel):
    """Repository response."""
    id: str
    name: str
    description: Optional[str]
    status: str
    progress_percentage: int
    indexed_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/upload", response_model=Dict[str, Any])
async def upload_repository(
    name: str,
    db: AsyncSession = Depends(get_db),
):
    """Upload and ingest a repository."""
    
    repo = Repository(
        user_id="test_user",
        name=name,
        status=RepositoryStatus.PENDING,
        size_bytes=0,
        file_count=0,
    )
    
    db.add(repo)
    await db.commit()
    await db.refresh(repo)
    
    logger.info(f"Repository uploaded: {repo.id}")
    
    return {
        "id": repo.id,
        "status": repo.status.value,
        "message": "Repository uploaded successfully. Indexing started..."
    }


@router.get("/{repository_id}/status", response_model=RepositoryResponse)
async def get_repository_status(
    repository_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get repository status and indexing progress."""
    
    stmt = select(Repository).where(Repository.id == repository_id)
    result = await db.execute(stmt)
    repo = result.scalars().first()
    
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found"
        )
    
    return RepositoryResponse(
        id=repo.id,
        name=repo.name,
        description=repo.description,
        status=repo.status.value,
        progress_percentage=repo.progress_percentage,
        indexed_at=repo.indexed_at,
        created_at=repo.created_at,
    )


@router.get("", response_model=List[RepositoryResponse])
async def list_repositories(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """List user repositories."""
    
    stmt = select(Repository).offset(skip).limit(min(limit, settings.MAX_PAGE_SIZE))
    result = await db.execute(stmt)
    repos = result.scalars().all()
    
    return [RepositoryResponse.model_validate(repo) for repo in repos]


@router.delete("/{repository_id}", response_model=Dict[str, str])
async def delete_repository(
    repository_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete a repository."""
    
    stmt = select(Repository).where(Repository.id == repository_id)
    result = await db.execute(stmt)
    repo = result.scalars().first()
    
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found"
        )
    
    await db.delete(repo)
    await db.commit()
    
    logger.info(f"Repository deleted: {repository_id}")
    
    return {"message": "Repository deleted successfully"}
