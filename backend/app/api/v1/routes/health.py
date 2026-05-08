"""
Health check endpoints
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.database.engine import get_db
from app.core.logging import get_logger
from app.core.config import settings

logger = get_logger(__name__)
router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Basic health check."""
    return {
        "status": "healthy",
        "service": "CodeShift AI API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }


@router.get("/health/detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Detailed health check including database."""
    health_status = {
        "status": "healthy",
        "services": {
            "api": "up",
            "database": "unknown",
        },
    }

    try:
        await db.execute(text("SELECT 1"))
        health_status["services"]["database"] = "up"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["services"]["database"] = "down"
        logger.error(f"Database health check failed: {str(e)}")

    return health_status


@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Readiness check for Kubernetes."""
    try:
        await db.execute(text("SELECT 1"))
        return {"ready": True}
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return {"ready": False, "error": str(e)}
