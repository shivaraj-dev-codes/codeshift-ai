# CodeShift AI — Enterprise Legacy Code Migration Copilot

> **An AI-powered platform for understanding, analyzing, and migrating enterprise legacy codebases.**

## 🚀 Overview

CodeShift AI is a production-grade SaaS platform that helps enterprises:

- **Understand** large legacy codebases through AI-powered analysis
- **Detect** architecture problems, dead code, security risks
- **Generate** technical documentation automatically
- **Plan** migration strategies (monolith → microservices)
- **Refactor** code with AI-powered recommendations
- **Generate** unit tests and integration tests
- **Chat** with your codebase using natural language

Built with enterprise-grade architecture, advanced AI engineering, and real-world developer workflows in mind.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Frontend: Next.js 15 + React + TypeScript + Tailwind CSS   │
├─────────────────────────────────────────────────────────────┤
│ API Gateway: FastAPI (Python) + Rate Limiting + JWT Auth   │
├─────────────────────────────────────────────────────────────┤
│ AI Core:                                                    │
│  • LangChain Multi-Agent Orchestration                     │
│  • LlamaIndex Retrieval-Augmented Generation (RAG)        │
│  • OpenAI/Gemini Integration                              │
│  • AST-Based Code Parsing                                 │
│  • Smart Semantic Chunking                                │
├─────────────────────────────────────────────────────────────┤
│ Data Layer:                                                 │
│  • PostgreSQL: Metadata, User Data, Audit Logs           │
│  • Redis: Caching, Session Management                     │
│  • Qdrant: Vector Search & Semantic Retrieval             │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Core Features

### 1. Repository Ingestion & Analysis
- Upload ZIP repositories or connect GitHub repositories
- Support for Python, Java, JavaScript, TypeScript, C#, Node.js
- Automatic AST parsing and dependency graph generation
- Real-time indexing progress tracking

### 2. AI Code Understanding
- Explain project architecture and design patterns
- Generate interactive dependency graphs
- Detect anti-patterns, dead code, tight coupling
- Identify security risks and performance bottlenecks

### 3. AI-Powered Chat Interface
Natural language queries on your codebase:
- "Explain the authentication flow"
- "Where is the payment processing logic?"
- "Find API security vulnerabilities"
- "Which files affect the login system?"

### 4. AI Architecture Migration Planner
- Monolith → Microservices decomposition
- Service boundary recommendations
- API redesign suggestions
- Database splitting strategies
- Azure cloud migration paths

### 5. AI Refactoring Engine
- Modern architecture recommendations
- Code quality improvements
- Async/await conversions
- Framework modernization suggestions

### 6. AI Test Generation
- Unit test generation from source code
- Integration test scenarios
- API endpoint tests
- Edge case identification

### 7. Documentation Generation
- Auto-generated README files
- Architecture documentation
- API reference docs
- Onboarding guides

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **UI Library**: React 19 with TypeScript
- **Styling**: Tailwind CSS + Framer Motion
- **Components**: ShadCN UI
- **Code Editor**: Monaco Editor
- **State Management**: TanStack Query + Zustand

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy with async drivers
- **Validation**: Pydantic v2
- **Task Queue**: Celery with Redis

### AI & ML
- **Orchestration**: LangChain with multi-agent support
- **RAG Framework**: LlamaIndex
- **LLM Models**: OpenAI GPT-4, Gemini API
- **Vector DB**: Qdrant
- **Code Parsing**: Tree-sitter (AST extraction)

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **CI/CD**: GitHub Actions
- **Cloud**: Azure

---

## 🚀 Quick Start

### Prerequisites
```bash
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+
```

### Local Development

```bash
# Clone repository
git clone https://github.com/shivaraj-dev-codes/codeshift-ai.git
cd codeshift-ai

# Start services
docker-compose up -d

# Frontend
cd frontend
npm install
npm run dev

# Backend (in new terminal)
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Qdrant UI: http://localhost:6333/dashboard

---

## 🤖 AI Architecture

### Multi-Agent System

**Architecture Agent**: System design analysis and decomposition  
**Security Agent**: Vulnerability detection and compliance  
**Refactoring Agent**: Code quality and modernization  
**Documentation Agent**: Technical doc generation  
**Testing Agent**: Test generation and coverage  

### RAG Pipeline

```
User Query → Embedding → Vector Search → Context Assembly → LLM → Response
```

### Smart Code Chunking

Chunks by:
- Classes and methods
- Modules and packages
- Logical boundaries
- Maintains context and dependencies

---

## 📚 Documentation

- [Architecture Details](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Database Schema](docs/DATABASE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [System Design](docs/SYSTEM_DESIGN.md)

---

## 🔐 Security

✅ JWT Authentication + OAuth2 GitHub  
✅ Role-Based Access Control (RBAC)  
✅ Rate Limiting (Token Bucket)  
✅ Input Validation (Pydantic)  
✅ TLS/HTTPS Encryption  
✅ Audit Logging  
✅ Secret Detection  
✅ SAST Code Scanning  

---

## 📈 Scalability

✅ Stateless API design  
✅ Horizontal scaling support  
✅ Database connection pooling  
✅ Redis distributed caching  
✅ Qdrant clustering  
✅ Async/await throughout  
✅ Streaming responses  
✅ Background task queue  

---

## 🌐 Deployment

### Local
```bash
docker-compose up -d
```

### Azure
```bash
cd deployment/azure
./deploy.sh --environment production
```

### GitHub Actions
Automated CI/CD pipeline on every push.

---

## 📄 License

MIT License — See [LICENSE](LICENSE)

---

## 🏆 Enterprise Features

✅ Multi-tenant architecture  
✅ Advanced RBAC and audit logging  
✅ Compliance-ready (SOC2, GDPR)  
✅ Enterprise SSO integration  
✅ Custom AI model fine-tuning  
✅ On-premise deployment option  
✅ 24/7 support and SLA guarantees  

---

**Built for Enterprise. Powered by AI. Ready for Scale.**
