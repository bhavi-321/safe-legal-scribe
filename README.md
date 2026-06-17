# ⚖️ Legality AI - Contract Risk Detector

**Legality AI** is an end-to-end intelligent contract analysis platform designed to identify legal risks in contracts automatically. It uses a custom-trained Sentence Transformer model to detect risky clauses and generate safer alternatives.

🌐 **Live Demo**: [safe-legal-scribe.vercel.app](https://safe-legal-scribe.vercel.app)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Development](#-development)
- [Deployment](#-deployment)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)

---

## ✨ Features

- **📄 Automated PDF Analysis**: Upload any contract PDF; the system extracts and chunks text for analysis
- **⚠️ Risk Detection**: Vector similarity search compares contract clauses against a "Gold Standard" database of known legal risks
- **🤖 AI Suggestions**: Automatically generates safe, balanced rewrites for risky clauses using Mistral-7B
- **🛡️ Safety Guardrails**: Flags high-risk clauses (e.g., Liability Caps) as "Review Only" to prevent dangerous AI outputs
- **📊 Observability**: Full tracing of AI logic and latency using Langfuse (in-progress)
- **🎨 Professional UI**: Modern React/TypeScript frontend with Tailwind CSS and shadcn-ui components

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Vercel)                        │
│              React + TypeScript + Tailwind CSS              │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    HTTP API (REST)
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    Backend (Railway)                         │
│                  FastAPI + Python 3.11                       │
├──────────────────────────────────────────────────────────────┤
│  • PDF Processing (pdfplumber)                               │
│  • Text Chunking (langchain-text-splitters)                  │
│  • Vector Embeddings (Sentence Transformers)                 │
│  • Risk Detection (Cosine Similarity)                        │
│  • LLM Integration (OpenRouter)                              │
│  • Observability (Langfuse)                                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   HF Models        Gold Standard        LLM APIs
 (Sentence Trans)    Database         (OpenRouter)

```

**Flow:**
1. User uploads PDF → Backend extracts text
2. Text is chunked using langchain splitters
3. Chunks converted to vectors using custom Sentence Transformer model
4. Vectors compared against gold standard dataset
5. High-similarity clauses flagged as risks
6. Policy check: "Rewrite Allowed" or "Review Only"
7. If allowed, LLM generates safer version
8. Results returned to frontend

---

## 🛠️ Tech Stack

### **Backend**
| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Language | Python 3.11+ |
| ML Model | `sentence-transformers` / `bhavibhatt/legal_model` |
| LLM Engine | OpenRouter API (`mistralai/mistral-7b-instruct`) |
| Vector Search | Scikit-Learn (Cosine Similarity) |
| PDF Processing | `pdfplumber` & `langchain-text-splitters` |
| Observability | Langfuse |
| Deployment | Railway |

### **Frontend**
| Component | Technology |
|-----------|------------|
| Framework | React 18 |
| Language | TypeScript |
| Build Tool | Vite |
| Styling | Tailwind CSS + shadcn-ui |
| Package Manager | npm / bun |
| Deployment | Vercel |

### **Data & ML**
| Component | Description |
|-----------|-------------|
| Training Data | ~50k+ labeled legal clauses |
| Model | Custom Sentence Transformer fine-tuned on legal contracts |
| Gold Standard | Synthetic dataset with NLI annotations |

---

## 📁 Project Structure

```
legality-ai/
├── README.md                           # Main project documentation
├── .github/
│   └── workflows/                      # CI/CD pipelines
│       ├── test.yml                    # Run tests on PR
│       └── deploy.yml                  # Deploy on merge to main
│
├── data/                               # Data management
│   ├── README.md                       # Data documentation
│   ├── raw/                            # Raw datasets (not committed)
│   ├── processed/                      # Processed/cleaned data
│   ├── gold_standard/
│   │   └── synthetic_gold_standard_with_nli.json
│   ├── datasets/
│   │   ├── termination_full_data.csv
│   │   ├── liability_full_data.csv
│   │   ├── non_compete_full_data.csv
│   │   └── master_clauses.csv
│   └── scripts/
│       ├── synthesize_data.py          # Generate synthetic data
│       └── validate_data.py            # Data quality checks
│
├── ml/                                 # Machine Learning
│   ├── README.md                       # ML documentation
│   ├── requirements.txt                # ML dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   ├── embedder.py                 # Sentence Transformer wrapper
│   │   └── risk_detector.py            # Risk detection logic
│   ├── training/
│   │   ├── train.py                    # Training script
│   │   ├── evaluate.py                 # Model evaluation
│   │   └── config.yaml                 # Training hyperparameters
│   └── tests/
│       ├── test_embedder.py
│       └── test_detector.py
│
├── backend/                            # Backend API
│   ├── README.md                       # Backend documentation
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                    # Environment variables template
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI app entry point
│   │   ├── config.py                   # Configuration management
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── analyze.py              # /analyze-contract endpoint
│   │   │   └── health.py               # /health endpoint
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── pdf_processor.py        # PDF extraction
│   │   │   ├── risk_analyzer.py        # Risk analysis logic
│   │   │   └── llm_generator.py        # Clause rewriting
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py              # Pydantic schemas
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── logger.py               # Logging setup
│   │       └── errors.py               # Custom exceptions
│   ├── tests/
│   │   ├── test_api.py
│   │   ├── test_services.py
│   │   └── conftest.py
│   └── uvicorn_run.py                  # Server runner
│
├── frontend/                           # React frontend
│   ├── README.md                       # Frontend documentation
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── postcss.config.js
│   ├── index.html
│   ├── public/                         # Static assets
│   ├── src/
│   │   ├── main.tsx                    # React entry point
│   │   ├── App.tsx                     # Root component
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   └── Results.tsx
│   │   ├── components/
│   │   │   ├── FileUploader.tsx
│   │   │   ├── RiskCard.tsx
│   │   │   ├── Navbar.tsx
│   │   │   └── Footer.tsx
│   │   ├── services/
│   │   │   ├── api.ts                  # API client
│   │   │   └── types.ts                # TypeScript types
│   │   ├── hooks/
│   │   │   ├── useAnalysis.ts
│   │   │   └── useUpload.ts
│   │   ├── styles/
│   │   │   └── globals.css
│   │   └── utils/
│   │       └── helpers.ts
│   └── dist/                           # Build output
│
├── docs/                               # Documentation
│   ├── ARCHITECTURE.md                 # Detailed architecture
│   ├── API.md                          # API documentation
│   ├── SETUP.md                        # Local setup guide
│   ├── DEPLOYMENT.md                   # Deployment guide
│   ├── CONTRIBUTING.md                 # Contribution guidelines
│   └── MODELS.md                       # ML model documentation
│
├── .gitignore                          # Git ignore rules
├── .env.example                        # Global environment template
├── docker-compose.yml                  # Local development with Docker
├── Makefile                            # Common commands
└── LICENSE                             # MIT License
```

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.11+
- Node.js 18+
- Git

### **1. Clone the Repository**

```bash
git clone https://github.com/bhavi-321/safe_legal_ai.git
cd safe_legal_ai
```

### **2. Backend Setup**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template and fill in your keys
cp .env.example .env
# Edit .env with your API keys

# Run server
uvicorn app.main:app --reload
```

**Backend runs at**: `http://localhost:8000`

### **3. Frontend Setup**

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend runs at**: `http://localhost:5173`

### **4. Upload a Contract**

1. Navigate to http://localhost:5173
2. Upload a PDF contract
3. View detected risks and suggestions

---

## 👨‍💻 Development

### **Running Tests**

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests (if configured)
cd frontend
npm run test
```

### **Code Quality**

```bash
# Backend linting
cd backend
flake8 app/
pylint app/

# Frontend linting
cd frontend
npm run lint
```

### **Building for Production**

```bash
# Frontend build
cd frontend
npm run build
# Output: dist/

# Backend is run directly with uvicorn (see deployment)
```

---

## 🌐 Deployment

### **Frontend (Vercel)**

1. Connect your GitHub repo to Vercel
2. Set root directory to `frontend/`
3. Build command: `npm run build`
4. Output directory: `dist`
5. Deploy!

### **Backend (Railway)**

1. Connect your GitHub repo to Railway
2. Set root directory to `backend/`
3. Add environment variables from `.env.example`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed steps.

---

## 📡 API Reference

### `POST /analyze-contract`

Analyze a contract PDF for legal risks.

**Request:**
```bash
curl -X POST "http://localhost:8000/analyze-contract" \
  -F "file=@contract.pdf"
```

**Response:**
```json
{
  "filename": "contract.pdf",
  "status": "success",
  "risks": [
    {
      "risk_category": "Termination For Convenience",
      "chunk_text": "Party A may terminate at any time...",
      "similarity_score": 0.87,
      "severity": "high",
      "policy": "rewrite_allowed",
      "suggested_clause": "Party A may terminate with 30 days prior written notice..."
    }
  ],
  "total_risks": 1,
  "processing_time_ms": 2340
}
```

### `GET /health`

Check system health and model status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "api_connected": true,
  "version": "1.0.0"
}
```

See [API.md](docs/API.md) for full reference.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) first.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "feat: add your feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 👥 Contributors

- **Bhavyang** - ML & Backend
- **Sneha** - Frontend & Design
- **Vedant** - Data & Infrastructure

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 📞 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/bhavi-321/safe_legal_ai/issues)
- Check [Documentation](docs/)
- Email: your-email@example.com

---

**Made with ❤️ for legal professionals and developers**
