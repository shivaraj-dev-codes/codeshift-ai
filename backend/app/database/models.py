"""
SQLAlchemy ORM models for the application
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    JSON,
    Enum as SQLEnum,
    Index,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    """User role enumeration."""
    USER = "user"
    ADMIN = "admin"
    ENTERPRISE_ADMIN = "enterprise_admin"


class RepositoryStatus(str, enum.Enum):
    """Repository processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    INDEXED = "indexed"
    ERROR = "error"
    ARCHIVED = "archived"


class AuthProvider(str, enum.Enum):
    """Authentication provider."""
    GITHUB = "github"
    EMAIL = "email"


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    avatar_url = Column(String(512), nullable=True)
    github_id = Column(String(255), unique=True, nullable=True, index=True)
    github_username = Column(String(255), nullable=True)
    auth_provider = Column(SQLEnum(AuthProvider), default=AuthProvider.EMAIL)
    password_hash = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    repositories = relationship("Repository", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")


class Repository(Base):
    """Repository model."""
    __tablename__ = "repositories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    language = Column(String(50), nullable=True)
    primary_language = Column(String(50), nullable=True)
    supported_languages = Column(JSON, nullable=True)
    repository_type = Column(String(50), default="uploaded")
    github_url = Column(String(512), nullable=True)
    size_bytes = Column(Integer, nullable=True)
    file_count = Column(Integer, nullable=True)
    indexed_at = Column(DateTime, nullable=True)
    status = Column(SQLEnum(RepositoryStatus), default=RepositoryStatus.PENDING, index=True)
    error_message = Column(Text, nullable=True)
    progress_percentage = Column(Integer, default=0)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="repositories")
    code_chunks = relationship("CodeChunk", back_populates="repository", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="repository", cascade="all, delete-orphan")
    analysis_results = relationship("AnalysisResult", back_populates="repository", cascade="all, delete-orphan")


class CodeChunk(Base):
    """Code chunk for RAG indexing."""
    __tablename__ = "code_chunks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    repository_id = Column(String(36), ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True)
    file_path = Column(String(512), nullable=False)
    chunk_type = Column(String(50), nullable=False)
    chunk_text = Column(Text, nullable=False)
    start_line = Column(Integer, nullable=True)
    end_line = Column(Integer, nullable=True)
    language = Column(String(50), nullable=True)
    symbol_name = Column(String(255), nullable=True, index=True)
    parent_class = Column(String(255), nullable=True)
    imports = Column(JSON, nullable=True)
    exports = Column(JSON, nullable=True)
    dependencies = Column(JSON, nullable=True)
    complexity_score = Column(Integer, nullable=True)
    test_coverage = Column(Float, nullable=True)
    is_public = Column(Boolean, default=True)
    is_deprecated = Column(Boolean, default=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    repository = relationship("Repository", back_populates="code_chunks")


class ChatMessage(Base):
    """Chat message model."""
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    repository_id = Column(String(36), ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    conversation_id = Column(String(36), nullable=True, index=True)
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer, nullable=True)
    sources = Column(JSON, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    model_used = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    repository = relationship("Repository", back_populates="chat_messages")
    user = relationship("User", back_populates="chat_messages")


class AnalysisResult(Base):
    """Analysis result model."""
    __tablename__ = "analysis_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    repository_id = Column(String(36), ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True)
    analysis_type = Column(String(50), nullable=False, index=True)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    result_data = Column(JSON, nullable=False)
    confidence_score = Column(Float, nullable=True)
    findings = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    execution_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    repository = relationship("Repository", back_populates="analysis_results")


class AuditLog(Base):
    """Audit log model."""
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String(255), nullable=False)
    resource_type = Column(String(100), nullable=True)
    resource_id = Column(String(255), nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    status = Column(String(50), default="success")
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
