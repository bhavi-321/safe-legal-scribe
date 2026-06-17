# Local Development Setup Guide

## Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)
- **Bun (optional)** - [Download](https://bun.sh/) (faster package manager)

## Step 1: Clone the Repository

```bash
git clone https://github.com/bhavi-321/safe_legal_ai.git
cd safe_legal_ai
```

## Step 2: Backend Setup

### 2.1 Create Python Virtual Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On Windows (cmd):
venv\Scripts\activate.bat
```

### 2.2 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.3 Set Up Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your API keys
# vim .env  (or use your favorite editor)
```

**Required Variables:**
```env
# OpenRouter API (for LLM)
OPENROUTER_API_KEY=sk_live_...

# Hugging Face (for model download)
HF_TOKEN=hf_...

# Optional: Langfuse (observability)
LANGFUSE_PUBLIC_KEY=pk_...
LANGFUSE_SECRET_KEY=sk_...
LANGFUSE_HOST=https://cloud.langfuse.com
```

**How to Get API Keys:**

1. **OpenRouter**: https://openrouter.ai/keys
   - Sign up
   - Create API key
   - Add credits

2. **Hugging Face**: https://huggingface.co/settings/tokens
   - Create read-only token
   - Used to download models

3. **Langfuse (optional)**: https://cloud.langfuse.com
   - Used for AI observability
   - Optional, can skip for basic setup

### 2.4 Verify Backend Installation

```bash
# Test FastAPI app can start
python -c "from app.main import app; print('✅ Backend ready')"
```

### 2.5 Run Backend

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Backend will be available at:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs (interactive)
- ReDoc: http://localhost:8000/redoc (documentation)

## Step 3: Frontend Setup

### 3.1 Navigate to Frontend Directory

```bash
cd ../frontend  # Go back and then into frontend
# OR if in root:
cd frontend
```

### 3.2 Install Dependencies

```bash
# Using npm
npm install

# OR using bun (faster)
bun install
```

### 3.3 Create Environment File (if needed)

```bash
cp .env.example .env.local
```

Update API endpoint:
```env
VITE_API_URL=http://localhost:8000
```

### 3.4 Run Frontend

```bash
# Using npm
npm run dev

# OR using bun
bun run dev
```

**Frontend will be available at:**
- http://localhost:5173

## Step 4: Verify Everything Works

### 4.1 Test Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "api_connected": true
}
```

### 4.2 Test Frontend

1. Open browser: http://localhost:5173
2. You should see the Legality AI homepage
3. Try uploading a test PDF

### 4.3 Check API Documentation

1. Visit: http://localhost:8000/docs
2. Try out endpoints using Swagger UI

## Troubleshooting

### Backend Won't Start

**Error: `ModuleNotFoundError: No module named 'app'`**
```bash
# Make sure you're in backend directory
cd backend
# Reinstall dependencies
pip install -r requirements.txt
```

**Error: `OPENROUTER_API_KEY not found`**
```bash
# Make sure .env file exists and has API key
cat .env  # Check if file exists
# Update with your actual API key
```

**Error: Model download fails**
```bash
# Test HF token
huggingface-cli login
# Enter your HF token when prompted

# Then try downloading model manually
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('bhavibhatt/legal_model')"
```

### Frontend Won't Start

**Error: `Port 5173 already in use`**
```bash
# Use different port
npm run dev -- --port 3000
```

**Error: API connection fails**
```bash
# Check backend is running
curl http://localhost:8000/health

# Check CORS headers in backend
# Should allow localhost:5173
```

### Model Loading Takes Too Long

First-time model download can take 5-10 minutes:
- Sentence Transformer model: ~500MB
- Be patient, don't interrupt
- Check download progress in terminal

### PDF Upload Fails

**Error: `File too large`**
- Maximum file size is 50MB
- Try with smaller PDF

**Error: `Invalid PDF format`**
- Ensure PDF is text-based (not scanned image)
- Try opening in Adobe Reader first

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Backend changes: `backend/app/`
- Frontend changes: `frontend/src/`
- Data changes: `data/`

### 3. Run Tests

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests (if configured)
cd frontend
npm run test
```

### 4. Commit and Push

```bash
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature-name
```

### 5. Create Pull Request

On GitHub, create PR with description and link to related issues.

## Database Setup (Future)

When we add PostgreSQL:

```bash
# Start local PostgreSQL
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres

# Run migrations
alembic upgrade head
```

## Docker Setup (Future)

```bash
# Build and run with Docker
docker-compose up

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## Useful Commands

### Backend
```bash
# Format code
black backend/app/

# Lint code
flake8 backend/app/

# Run type checking
mypy backend/app/

# Run specific test
pytest backend/tests/test_api.py::test_health_check
```

### Frontend
```bash
# Format code
npm run format

# Lint code
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

## Next Steps

1. ✅ Backend running
2. ✅ Frontend running
3. 📝 Read [ARCHITECTURE.md](ARCHITECTURE.md) for system overview
4. 📖 Check [API.md](API.md) for endpoint documentation
5. 🚀 Read [DEPLOYMENT.md](DEPLOYMENT.md) when ready to deploy

## Need Help?

- Check existing [Issues](https://github.com/bhavi-321/safe_legal_ai/issues)
- Review documentation in `/docs`
- Ask in Pull Request discussions
