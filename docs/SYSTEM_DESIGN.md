# CodeShift AI — System Design Document

## Executive Summary

CodeShift AI is an enterprise-grade SaaS platform that leverages advanced AI/ML technologies to understand, analyze, and assist in migrating legacy codebases to modern architectures. The system combines:

- **Multi-agent AI orchestration** for specialized code analysis
- **Retrieval-Augmented Generation (RAG)** for context-aware responses
- **AST-based code parsing** for syntax-aware analysis
- **Semantic vector search** for intelligent code discovery
- **Enterprise-grade architecture** for scalability and security

---

## 1. Architecture Overview

### 1.1 High-Level Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Layer                             │
│  Browser (Next.js Frontend) + Mobile (Future)              │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              API Gateway Layer (FastAPI)                    │
│  • JWT Authentication & Authorization                      │
│  • Rate Limiting & Quota Management                        │
│  • Request/Response Validation                             │
│  • CORS & Security Headers                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐  ┌─────▼──────┐  ┌───▼──────┐
   │ Service │  │ AI Service │  │ Analytics│
   │ Layer   │  │ (Agents)   │  │ Service  │
   └────┬────┘  └─────┬──────┘  └───┬──────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐  ┌─────▼──────┐  ┌───▼──────┐
   │PostgreSQL│ │ Redis Cache│ │ Qdrant   │
   │Database  │ │            │ │ Vector DB│
   └──────────┘  └────────────┘  └──────────┘
```

### 1.2 Microservices (or Modular Monolith) Architecture

While CodeShift AI can start as a modular monolith, it's designed for easy decomposition into microservices:

#### Service Boundaries:

1. **Authentication Service**
   - JWT token generation/validation
   - OAuth2 GitHub integration
   - User session management
   - RBAC enforcement

2. **Repository Service**
   - Repository upload/ingestion
   - Metadata management
   - File extraction
   - Dependency tracking

3. **Code Analysis Service**
   - AST parsing and analysis
   - Code metrics calculation
   - Pattern detection
   - Vulnerability scanning

4. **Embedding Service**
   - Code chunk generation
   - Semantic embedding creation
   - Vector normalization
   - Batch processing optimization

5. **Vector Search Service**
   - Qdrant integration
   - Semantic search queries
   - Similarity scoring
   - Result ranking

6. **AI Agent Service**
   - LangChain orchestration
   - Multi-agent coordination
   - LLM invocation
   - Response streaming

7. **Chat Service**
   - Conversation management
   - Message persistence
   - Context window assembly
   - Source citation tracking

8. **Documentation Service**
   - Document generation
   - Format conversion
   - Export handling
   - Template management

9. **Analytics Service**
   - Usage tracking
   - Performance metrics
   - User behavior analysis
   - Billing/metering

---

## 2. AI Architecture in Detail

### 2.1 Multi-Agent System

#### Agent Specialization

```python
class CodeShiftAgents:
    
    # Architecture Analysis Agent
    architecture_agent = ArchitectureAgent(
        llm=ChatOpenAI(model="gpt-4"),
        tools=[dependency_graph, code_metrics, pattern_detector],
        system_prompt="You are an expert software architect..."
    )
    
    # Security Analysis Agent
    security_agent = SecurityAgent(
        llm=ChatOpenAI(model="gpt-4"),
        tools=[vulnerability_scanner, credential_detector, sast_analyzer],
        system_prompt="You are a security expert..."
    )
    
    # Refactoring Agent
    refactoring_agent = RefactoringAgent(
        llm=ChatOpenAI(model="gpt-4"),
        tools=[code_smell_detector, design_pattern_matcher, refactoring_suggester],
        system_prompt="You are a code refactoring expert..."
    )
    
    # Documentation Agent
    documentation_agent = DocumentationAgent(
        llm=ChatOpenAI(model="gpt-4"),
        tools=[doc_generator, markdown_formatter, diagram_creator],
        system_prompt="You are a technical documentation expert..."
    )
    
    # Testing Agent
    testing_agent = TestingAgent(
        llm=ChatOpenAI(model="gpt-4"),
        tools=[test_generator, edge_case_finder, mock_creator],
        system_prompt="You are a testing expert..."
    )
```

### 2.2 RAG (Retrieval-Augmented Generation) Pipeline

#### Step 1: Repository Ingestion
```
Upload ZIP → Extract Files → Parse with Tree-sitter → Generate AST
```

#### Step 2: Smart Chunking
```
AST → Identify Classes, Methods, Modules → Create Semantic Units
↓
Each Chunk:
  - Source code
  - File path & line numbers
  - Dependencies
  - Context metadata
  - Language info
```

#### Step 3: Embedding Generation
```
Chunk Text → OpenAI Embedding API → 1536-dimensional vector
↓
Stored in Qdrant with metadata
```

#### Step 4: Query Processing
```
User Query → Embedding → Semantic Search in Qdrant
↓
Top K results (ranked by cosine similarity) → Retrieve chunks
↓
Assemble context window (respecting token limits)
```

#### Step 5: LLM Generation with Context
```
Context + Query → LangChain Agent → GPT-4/Gemini
↓
Generate response with source citations
↓
Stream to client via WebSocket
```

### 2.3 Smart Code Chunking Strategy

#### Chunk Types

1. **Class-Level Chunks**
   - One chunk per class definition
   - Includes class members and methods
   - Maintains class-level context
   - Size: ~1-5KB typically

2. **Method-Level Chunks**
   - One chunk per method/function
   - Includes method signature and body
   - Links to parent class
   - Size: ~0.5-2KB typically

3. **Module-Level Chunks**
   - One chunk per file
   - High-level overview
   - All imports and exports
   - Size: ~2-10KB typically

4. **Dependency Chunks**
   - Cross-file relationships
   - Import/export relationships
   - API contracts
   - Size: ~0.5-1KB typically

#### Metadata Per Chunk
```json
{
  "chunk_id": "uuid",
  "repository_id": "uuid",
  "file_path": "src/auth/jwt_handler.py",
  "chunk_type": "class",
  "language": "python",
  "start_line": 45,
  "end_line": 120,
  "class_name": "JWTHandler",
  "method_names": ["encode", "decode", "validate"],
  "imports": ["jwt", "datetime"],
  "exports": ["JWTHandler"],
  "dependencies": ["uuid_module.py", "config.py"],
  "complexity_score": 3,
  "test_coverage": 0.85,
  "last_modified": "2024-01-15",
  "embedding": [0.123, 0.456, ...] // 1536 dimensions
}
```

### 2.4 Hallucination Reduction Strategies

1. **Source Citation**
   - Every claim references specific code chunks
   - Include file paths and line numbers
   - Link to exact source locations

2. **Confidence Scoring**
   - Retrieve similarity scores from vector search
   - Tag responses with confidence levels
   - Flag low-confidence assertions

3. **Verification Chain**
   ```
   Query → Retrieve Chunks → Verify Chunks Exist
         → Verify Semantically Related
         → Check Cross-References
         → Generate with Citations
   ```

4. **Context Grounding**
   - Always include original code in response
   - Show retrieval ranking
   - Transparent about uncertainty

---

## 3. Database Schema

### 3.1 Core Tables

#### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    avatar_url VARCHAR(512),
    github_id VARCHAR(255) UNIQUE,
    github_username VARCHAR(255),
    auth_provider ENUM('github', 'email'),
    password_hash VARCHAR(255), -- if using email auth
    is_active BOOLEAN DEFAULT true,
    role ENUM('user', 'admin', 'enterprise_admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_github_id ON users(github_id);
```

#### Repositories Table
```sql
CREATE TABLE repositories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    language VARCHAR(50), -- 'python', 'java', 'javascript', etc.
    primary_language VARCHAR(50),
    supported_languages TEXT[], -- ARRAY of languages detected
    repository_type ENUM('uploaded', 'github_imported') DEFAULT 'uploaded',
    github_url VARCHAR(512),
    size_bytes BIGINT,
    file_count INT,
    indexed_at TIMESTAMP,
    status ENUM('pending', 'processing', 'indexed', 'error', 'archived') DEFAULT 'pending',
    error_message TEXT,
    progress_percentage INT DEFAULT 0,
    metadata JSONB, -- Additional data (tags, custom fields, etc.)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_repositories_user_id ON repositories(user_id);
CREATE INDEX idx_repositories_status ON repositories(status);
```

#### Code Chunks Table (RAG Index)
```sql
CREATE TABLE code_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repository_id UUID NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    file_path VARCHAR(512) NOT NULL,
    chunk_type ENUM('class', 'method', 'module', 'function') NOT NULL,
    chunk_text TEXT NOT NULL,
    start_line INT,
    end_line INT,
    language VARCHAR(50),
    symbol_name VARCHAR(255), -- class or method name
    parent_class VARCHAR(255), -- for methods
    imports TEXT[], -- array of imports
    exports TEXT[], -- array of exports
    dependencies JSONB, -- {"files": [...], "classes": [...], "functions": [...]}
    complexity_score INT, -- cyclomatic complexity
    test_coverage FLOAT, -- 0.0 to 1.0
    is_public BOOLEAN DEFAULT true,
    is_deprecated BOOLEAN DEFAULT false,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_code_chunks_repository ON code_chunks(repository_id);
CREATE INDEX idx_code_chunks_file_path ON code_chunks(file_path);
CREATE INDEX idx_code_chunks_symbol ON code_chunks(symbol_name);
```

#### Chat Messages Table
```sql
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repository_id UUID NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    conversation_id UUID, -- for grouping related messages
    role ENUM('user', 'assistant') NOT NULL,
    content TEXT NOT NULL,
    tokens_used INT,
    sources JSONB, -- [{"chunk_id": "...", "relevance": 0.95, "file": "..."}]
    response_time_ms INT,
    model_used VARCHAR(100), -- 'gpt-4', 'gemini-pro', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chat_messages_repository ON chat_messages(repository_id);
CREATE INDEX idx_chat_messages_user ON chat_messages(user_id);
CREATE INDEX idx_chat_messages_conversation ON chat_messages(conversation_id);
```

#### Analysis Results Table
```sql
CREATE TABLE analysis_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repository_id UUID NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    analysis_type ENUM('architecture', 'security', 'refactoring', 'testing', 'documentation') NOT NULL,
    title VARCHAR(255),
    description TEXT,
    result_data JSONB NOT NULL, -- Structured analysis results
    confidence_score FLOAT, -- 0.0 to 1.0
    findings TEXT[], -- array of key findings
    recommendations JSONB, -- structured recommendations
    execution_time_ms INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_analysis_results_repository ON analysis_results(repository_id);
CREATE INDEX idx_analysis_results_type ON analysis_results(analysis_type);
```

#### Audit Logs Table
```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(255) NOT NULL, -- 'upload', 'analyze', 'chat', etc.
    resource_type VARCHAR(100), -- 'repository', 'analysis', etc.
    resource_id VARCHAR(255),
    details JSONB, -- extra context
    ip_address VARCHAR(45),
    user_agent TEXT,
    status ENUM('success', 'error') DEFAULT 'success',
    error_message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
```

### 3.2 Vector Database (Qdrant) Schema

```json
{
  "collection_name": "code_embeddings",
  "vectors": {
    "size": 1536,
    "distance": "Cosine"
  },
  "payload_schema": {
    "chunk_id": {"type": "keyword"},
    "repository_id": {"type": "keyword"},
    "file_path": {"type": "text"},
    "chunk_type": {"type": "keyword"},
    "language": {"type": "keyword"},
    "symbol_name": {"type": "keyword"},
    "start_line": {"type": "integer"},
    "end_line": {"type": "integer"},
    "complexity_score": {"type": "integer"},
    "test_coverage": {"type": "float"},
    "created_at": {"type": "integer"} // Unix timestamp
  },
  "indexes": [
    {"field": "repository_id", "type": "keyword"},
    {"field": "language", "type": "keyword"},
    {"field": "chunk_type", "type": "keyword"}
  ]
}
```

---

## 4. API Design

### 4.1 Authentication Endpoints

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}

Response 200:
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "user": {"id": "...", "email": "...", "name": "..."}
}
```

```http
GET /api/v1/auth/github/callback?code=github_code&state=state_value

Response 302 Redirect:
Location: http://localhost:3000?token=eyJhbGc...
```

### 4.2 Repository Management

```http
POST /api/v1/repositories/upload
Content-Type: multipart/form-data
Authorization: Bearer {token}

FormData:
  file: repository.zip
  name: "my-legacy-app"
  description: "Old monolithic application"

Response 201:
{
  "id": "uuid",
  "status": "processing",
  "progress_percentage": 0
}
```

```http
GET /api/v1/repositories/{id}/status
Authorization: Bearer {token}

Response 200:
{
  "id": "uuid",
  "name": "my-legacy-app",
  "status": "indexed",
  "progress_percentage": 100,
  "indexed_at": "2024-01-15T10:30:00Z",
  "file_count": 1245,
  "size_bytes": 5242880,
  "languages": ["python", "javascript"],
  "chunk_count": 3456
}
```

### 4.3 Chat & Query API

```http
POST /api/v1/chat/{repository_id}/message
Content-Type: application/json
Authorization: Bearer {token}

{
  "message": "Explain the authentication flow",
  "conversation_id": "uuid" // optional, for multi-turn
}

Response 200 (Streaming via SSE):
event: start
data: {"status": "processing"}

event: token
data: "The authentication"

event: token
data: " flow uses JWT tokens"

event: sources
data: [{"file": "auth.py", "lines": "45-120", "relevance": 0.98}]

event: end
data: {"total_tokens": 245, "response_time_ms": 1234}
```

### 4.4 Analysis API

```http
POST /api/v1/analysis/architecture
Content-Type: application/json
Authorization: Bearer {token}

{
  "repository_id": "uuid"
}

Response 200:
{
  "analysis_id": "uuid",
  "type": "architecture",
  "status": "completed",
  "findings": [
    {
      "title": "Tight Coupling Detected",
      "severity": "high",
      "description": "...",
      "affected_modules": ["auth", "payment"],
      "recommendation": "Extract shared interfaces"
    }
  ],
  "decomposition_suggestions": [
    {
      "service_name": "auth-service",
      "modules": ["auth", "jwt"],
      "external_api": "/auth"
    }
  ],
  "confidence_score": 0.92
}
```

---

## 5. Security Architecture

### 5.1 Authentication Flow

```
User Login → Verify Credentials → Generate JWT (access + refresh)
           → Store refresh token in secure HTTP-only cookie
           → Return access token to client
```

### 5.2 Authorization

- **RBAC Levels**: user, admin, enterprise_admin
- **Resource-Level Permissions**: User can only access own repositories
- **API Scopes**: read:repo, write:repo, admin:org

### 5.3 Rate Limiting

```python
# Token bucket algorithm via Redis
Rate Limits:
  - API: 1000 requests/hour per user
  - Upload: 10 uploads/day per user
  - Chat: 100 messages/hour per user
  - Analysis: 50 analyses/day per user
```

### 5.4 File Upload Security

```python
Validations:
  - Max file size: 500MB
  - Allowed formats: .zip only
  - Scan for malware (ClamAV)
  - Extract to isolated container
  - Verify no path traversal attacks
  - Remove executable files
```

### 5.5 Secret Detection

```python
Scans for:
  - AWS keys and credentials
  - API keys and tokens
  - Database connection strings
  - Private SSH keys
  - Slack/Discord tokens
  - Database passwords
```

---

## 6. Scalability & Performance

### 6.1 Horizontal Scaling Strategy

```
Load Balancer (Azure LB or Nginx)
    ↓
  ┌─┴─┬─────┬─────┐
  │   │     │     │
  API-1 API-2 API-3
    └─┬─┴─────┴─────┘
      │
  PostgreSQL (primary)
    + Replicas
    + Connection Pool
      │
  Distributed Redis Cluster
```

### 6.2 Database Optimization

```sql
-- Connection pooling with PgBouncer
Connections: 500 (production)

-- Key indexes for query performance
CREATE INDEX idx_code_chunks_repo_file ON code_chunks(repository_id, file_path);
CREATE INDEX idx_chat_messages_repo_time ON chat_messages(repository_id, created_at DESC);
CREATE INDEX idx_audit_logs_user_time ON audit_logs(user_id, timestamp DESC);

-- Partitioning for large tables
PARTITION code_chunks BY RANGE (created_at)
PARTITION audit_logs BY RANGE (timestamp)
```

### 6.3 Caching Strategy

```python
Redis Cache Layers:
  1. Session Cache: user::{user_id} → 24 hours
  2. Repository Metadata: repo::{repo_id}:metadata → 12 hours
  3. Analysis Results: analysis::{analysis_id} → 24 hours
  4. Query Results: query::{hash} → 1 hour
  5. Rate Limit Counters: rate_limit::{user_id} → 1 hour
```

### 6.4 Streaming & Real-Time Features

```python
# Server-Sent Events (SSE) for streaming AI responses
GET /api/v1/stream/chat/{message_id}

Response: text/event-stream
  - Tokens streamed as generated
  - Source citations as retrieved
  - Completion status when finished

# WebSocket option for bi-directional communication
WS /ws/chat/{conversation_id}
```

---

## 7. Deployment Architecture

### 7.1 Local Development

```bash
docker-compose up -d
# Spins up: Postgres, Redis, Qdrant, Backend, Frontend
```

### 7.2 Azure Deployment

```
Azure Container Registry (ACR)
  ↓
Azure Container Apps (Backend)
  ↓
Azure Database for PostgreSQL
+ Azure Cache for Redis
+ Qdrant Cloud
  ↓
Azure Static Web Apps (Frontend)
  ↓
Azure API Management (Rate limiting, gateway)
  ↓
Azure CDN (Static asset delivery)
```

### 7.3 CI/CD Pipeline (GitHub Actions)

```yaml
Trigger: Push to main

Jobs:
  1. Test Backend (pytest)
  2. Lint Backend (flake8, mypy)
  3. Build Backend Docker Image
  4. Push to ACR
  5. Test Frontend (Jest, Playwright)
  6. Build Frontend
  7. Deploy to Azure
  8. Run Integration Tests
  9. Health Check
  10. Notify Slack
```

---

## 8. Monitoring & Observability

### 8.1 Logging

```python
# Structured logging with JSON output
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "backend",
  "action": "chat_message_processed",
  "user_id": "uuid",
  "repository_id": "uuid",
  "response_time_ms": 1234,
  "tokens_used": 245,
  "status": "success"
}
```

### 8.2 Metrics

- API response times (p50, p95, p99)
- Token usage per user/repository
- AI model costs tracking
- Cache hit rates
- Database query performance
- Vector search latency

### 8.3 Alerting

- Error rate > 1%
- Response time > 5s
- API rate limit violations
- Database connection pool exhaustion
- Vector DB unavailability
- API key quota warnings

---

## 9. Cost Optimization

### 9.1 LLM Costs

```
Estimated Monthly Costs (at scale):
  - GPT-4: ~$0.08/1K tokens → $2400/month at 30M tokens
  - Embeddings: ~$0.0001/1K tokens → $20/month at 200M tokens
```

Optimizations:
- Batch embeddings for new repositories
- Cache embeddings in Qdrant
- Use GPT-3.5 for simple queries
- Implement token budgets per user

### 9.2 Infrastructure Costs

```
Azure Estimates:
  - Container Apps (Backend): $150-300/month
  - PostgreSQL (5GB, standard): $100-150/month
  - Redis Cache (1GB): $20-50/month
  - Static Web Apps (Frontend): Free tier available
  - CDN: $0.20/GB bandwidth
```

---

## 10. Security Compliance

### 10.1 Compliance Standards

- **SOC2 Type II**: Audit logging, access controls, encryption
- **GDPR**: Data deletion, user consent, privacy policy
- **HIPAA**: (if handling medical data) Encryption at rest/transit
- **PCI-DSS**: (if handling payments) Secure token storage

### 10.2 Data Privacy

- Repositories encrypted at rest (AES-256)
- TLS 1.3 for all network communication
- No storing of API keys in plaintext
- Regular security audits
- Penetration testing (quarterly)

---

## Conclusion

CodeShift AI is designed as a production-grade, enterprise-scale platform that leverages cutting-edge AI technologies while maintaining security, performance, and scalability. The architecture supports both immediate deployment and long-term growth through microservices decomposition.
