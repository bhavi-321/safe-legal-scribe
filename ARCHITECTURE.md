# System Architecture

## Overview

Legality AI is built as a modern, scalable full-stack application with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND LAYER                          │
│              (React + TypeScript + Vite)                     │
│                   [Vercel Deployment]                        │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                        │
│                    FastAPI + Python 3.11                     │
│                   [Railway Deployment]                       │
├─────────────────────────────────────────────────────────────┤
│  Authentication │ Rate Limiting │ Input Validation │ CORS   │
└────────┬────────────────────────────────────────────┬───────┘
         │                                            │
         ▼                                            ▼
┌─────────────────────────┐              ┌───────────────────────┐
│    SERVICE LAYER        │              │   ML/DATA LAYER       │
├─────────────────────────┤              ├───────────────────────┤
│ • PDF Processor         │              │ • Embedder Model      │
│ • Risk Analyzer         │◄─────────────┤ • Risk Detector       │
│ • LLM Generator         │              │ • Gold Standard DB    │
│ • Langfuse Tracer       │              │ • Transformers        │
└─────────────────────────┘              └───────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              EXTERNAL SERVICES LAYER                         │
├─────────────────────────────────────────────────────────────┤
│  • OpenRouter (LLM API)                                      │
│  • Hugging Face (Model Hosting)                              │
│  • Langfuse (Observability)                                  │
│  • AWS S3 / Database (Future)                                │
└─────────────────────────────────────────────────────────────┘
```

## Components Breakdown

### 1. Frontend Architecture

**Stack**: React 18 + TypeScript + Vite + Tailwind CSS

```
src/
├── pages/              # Page components (Home, Dashboard, Results)
├── components/         # Reusable UI components
├── services/           # API client & data fetching
├── hooks/              # Custom React hooks
├── utils/              # Helper functions
└── styles/             # Global styles
```

**Key Features**:
- Component-based architecture
- Type-safe with TypeScript
- Responsive design with Tailwind CSS
- shadcn-ui for consistent components
- Fast HMR with Vite

### 2. Backend Architecture

**Stack**: FastAPI + Python 3.11 + Uvicorn

```
app/
├── main.py             # FastAPI app initialization
├── config.py           # Configuration management
├── routes/             # API endpoints
├── services/           # Business logic
├── models/             # Pydantic schemas
└── utils/              # Utilities (logging, errors)
```

**Design Patterns**:
- **Dependency Injection**: Services injected into routes
- **Repository Pattern**: Data access abstraction
- **Error Handling**: Custom exceptions with proper HTTP codes
- **Logging**: Structured logging with context

### 3. ML Pipeline

**Architecture**:

```
Input PDF
   │
   ▼
[PDF Extraction]
   │
   ▼
[Text Chunking]
   │
   ▼
[Embedding Generation]
   │ (Sentence Transformer)
   ▼
[Vector Similarity Search]
   │ (Against Gold Standard)
   ▼
[Risk Detection]
   │
   ▼
[Policy Evaluation]
   │ (Rewrite Allowed?)
   ├─── YES ──► [LLM Rewrite]
   │              │
   │              ▼
   │        [Safe Suggestion]
   │
   └─── NO ──► [Review Only]
                  │
                  ▼
             [Final Result]
```

**Components**:

1. **PDF Processor**: Uses `pdfplumber` to extract text
2. **Text Chunker**: `langchain-text-splitters` for optimal chunking
3. **Embedder**: `sentence-transformers` with custom legal model
4. **Risk Detector**: Cosine similarity search against gold standard
5. **LLM Generator**: OpenRouter integration with Mistral-7B

### 4. Data Layer

**Data Organization**:

```
data/
├── raw/                # Original data sources
├── processed/          # Cleaned datasets
├── gold_standard/      # Risk reference database
│   └── synthetic_gold_standard_with_nli.json
└── datasets/           # Categorized training data
    ├── termination_full_data.csv
    ├── liability_full_data.csv
    ├── non_compete_full_data.csv
    └── master_clauses.csv
```

**Gold Standard Schema**:
```json
{
  "risks": [
    {
      "id": "risk_001",
      "category": "Termination For Convenience",
      "risk_text": "Party A may terminate at any time...",
      "severity": "high",
      "policy": "rewrite_allowed",
      "safe_template": "Party A may terminate with 30 days notice..."
    }
  ]
}
```

## Request Flow

### Contract Analysis Flow

```
1. USER ACTION
   └─► Upload PDF via frontend

2. FRONTEND PROCESSING
   └─► File validation
   └─► Progress indication
   └─► Send to backend

3. BACKEND INTAKE
   └─► Receive file
   └─► Validate file type (PDF)
   └─► Check file size

4. PDF EXTRACTION
   └─► Extract text using pdfplumber
   └─► Preserve document structure
   └─► Handle OCR if needed (future)

5. TEXT PROCESSING
   └─► Clean text
   └─► Split into chunks (500-1000 tokens)
   └─► Maintain context overlap

6. VECTORIZATION
   └─► Load Sentence Transformer model
   └─► Generate embeddings for each chunk
   └─► Cache embeddings for efficiency

7. RISK DETECTION
   └─► Load gold standard embeddings
   └─► Compute cosine similarity for each chunk
   └─► Filter by similarity threshold (0.75+)
   └─► Rank risks by severity

8. POLICY CHECK
   └─► Identify risk category
   └─► Look up rewrite policy
   └─► If "Review Only" → skip LLM
   └─► If "Rewrite Allowed" → proceed

9. LLM REWRITING (if allowed)
   └─► Call OpenRouter API with Mistral-7B
   └─► Provide context + risky clause
   └─► Generate safe alternative
   └─► Validate output

10. RESPONSE PREPARATION
    └─► Format results
    └─► Include metadata (scores, times)
    └─► Return to frontend

11. FRONTEND DISPLAY
    └─► Render risk cards
    └─► Show suggestions
    └─► Enable actions (copy, export)
```

## Security Considerations

### Frontend Security
- **HTTPS Only**: All communications encrypted
- **CORS**: Restricted to trusted origins
- **CSP Headers**: Prevent XSS attacks
- **Input Validation**: Client-side validation before send

### Backend Security
- **Input Validation**: All inputs validated with Pydantic
- **Rate Limiting**: Prevent abuse
- **API Keys**: Stored securely in environment variables
- **Error Handling**: Don't expose internal details
- **Logging**: Audit trail without sensitive data

### Data Security
- **File Upload**: Temporary storage only
- **API Keys**: Never logged or exposed
- **Model Weights**: Cached locally after first load

## Scalability Considerations

### Horizontal Scaling
- **Stateless Backend**: Can run multiple instances behind load balancer
- **Model Caching**: Local caching per instance
- **Async Processing**: FastAPI async endpoints

### Performance Optimization
- **Model Quantization**: Reduce model size (future)
- **Batch Processing**: Process multiple PDFs (future)
- **CDN**: Frontend assets via Vercel edge network
- **API Caching**: Cache gold standard embeddings

## Monitoring & Observability

### Logging
- Structured JSON logs with context
- Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Integration with Langfuse (in progress)

### Metrics
- Request latency
- Model inference time
- API error rates
- File processing success rate

### Tracing
- Request ID tracking
- Service call tracing
- ML model execution tracing

## Deployment Architecture

### Frontend Deployment (Vercel)
- Auto-deployment from main branch
- Global CDN distribution
- Serverless functions (if needed)
- SSL/TLS by default

### Backend Deployment (Railway)
- Docker containerization (future)
- Environment-based configuration
- Health checks
- Auto-scaling policies

### CI/CD Pipeline
```
Git Push
   │
   ▼
GitHub Actions
   ├─► Run tests
   ├─► Lint code
   ├─► Build frontend
   └─► Deploy on success
        ├─► Vercel (frontend)
        └─► Railway (backend)
```

## Technology Justification

| Layer | Choice | Why |
|-------|--------|-----|
| Frontend | React | Industry standard, large ecosystem, component reusability |
| Build | Vite | Fast, modern, excellent DX |
| Styling | Tailwind + shadcn-ui | Rapid development, consistent design system |
| Backend | FastAPI | Type-safe, async support, auto-generated API docs |
| ML Framework | Sentence Transformers | Production-ready, easy fine-tuning, active community |
| LLM | OpenRouter + Mistral | Cost-effective, no infrastructure, easy integration |
| Deployment | Vercel + Railway | Developer-friendly, auto-scaling, free tiers available |

## Future Architecture Improvements

1. **Database**: Add PostgreSQL for persistence
2. **Message Queue**: Redis/RabbitMQ for async jobs
3. **Caching**: Redis for model/embeddings caching
4. **Authentication**: OAuth2 + JWT tokens
5. **Microservices**: Separate ML service if needed
6. **Containerization**: Docker for consistent environments
7. **Monitoring**: Prometheus + Grafana dashboard
8. **Storage**: S3 for uploaded PDFs and results
