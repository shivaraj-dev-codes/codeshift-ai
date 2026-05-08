"""
Code analysis endpoints
"""

from typing import Dict, Any
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.engine import get_db
from app.database.models import Repository, AnalysisResult
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


class AnalysisRequest(BaseModel):
    """Analysis request."""
    repository_id: str


class AnalysisResponse(BaseModel):
    """Analysis response."""
    id: str
    type: str
    status: str
    confidence_score: float
    findings: Dict[str, Any]
    recommendations: Dict[str, Any]
    created_at: datetime


@router.post("/architecture", response_model=AnalysisResponse)
async def analyze_architecture(
    request: AnalysisRequest,
    db: AsyncSession = Depends(get_db),
):
    """Analyze repository architecture."""
    
    stmt = select(Repository).where(Repository.id == request.repository_id)
    result = await db.execute(stmt)
    repo = result.scalars().first()
    
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found"
        )
    
    analysis = AnalysisResult(
        repository_id=repo.id,
        analysis_type="architecture",
        result_data={"status": "processing"},
        confidence_score=0.0,
    )
    
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)
    
    logger.info(f"Architecture analysis started for repo {repo.id}")
    
    return AnalysisResponse(
        id=analysis.id,
        type="architecture",
        status="processing",
        confidence_score=0.0,
        findings={},
        recommendations={},
        created_at=analysis.created_at,
    )


@router.post("/security", response_model=AnalysisResponse)
async def analyze_security(
    request: AnalysisRequest,
    db: AsyncSession = Depends(get_db),
):
    """Analyze repository for security issues."""
    
    stmt = select(Repository).where(Repository.id == request.repository_id)
    result = await db.execute(stmt)
    repo = result.scalars().first()
    
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found"
        )
    
    analysis = AnalysisResult(
        repository_id=repo.id,
        analysis_type="security",
        result_data={"status": "processing"},
        confidence_score=0.0,
    )
    
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)
    
    logger.info(f"Security analysis started for repo {repo.id}")
    
    return AnalysisResponse(
        id=analysis.id,
        type="security",
        status="processing",
        confidence_score=0.0,
        findings={},
        recommendations={},
        created_at=analysis.created_at,
    )
