# Deployment Guide

## Overview

Legality AI is deployed on two platforms:
- **Frontend**: Vercel (React app)
- **Backend**: Railway (FastAPI)

## Frontend Deployment (Vercel)

### Prerequisites
- GitHub account with repo access
- Vercel account (free tier available)

### Step 1: Connect Repository to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Sign in or create account
3. Click "Add New" → "Project"
4. Select your GitHub repo: `bhavi-321/safe_legal_ai`
5. Click "Import"

### Step 2: Configure Build Settings

Vercel should auto-detect, but verify:

- **Framework**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### Step 3: Set Environment Variables

In Vercel dashboard:

1. Go to Project Settings → Environment Variables
2. Add variable:
   ```
   Name: VITE_API_URL
   Value: https://your-backend.railway.app
   ```
3. Click "Save"

### Step 4: Deploy

1. Click "Deploy"
2. Wait for build to complete (~2-5 minutes)
3. Visit your URL: `https://your-project.vercel.app`

**Auto-deployment**: Every push to `main` branch auto-deploys

## Backend Deployment (Railway)

### Prerequisites
- GitHub account
- Railway account (free tier with $5/month)

### Step 1: Connect Repository to Railway

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "Create New Project"
4. Select "Deploy from GitHub repo"
5. Authorize GitHub access
6. Select your repo: `bhavi-321/safe_legal_ai`
7. Click "Deploy"

### Step 2: Configure Build Settings

In Railway dashboard:

1. Click on your service
2. Go to Settings tab
3. Set "Root Directory": `backend`
4. Set "Build Command": `pip install -r requirements.txt`
5. Set "Start Command": `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variables

In Railway dashboard:

1. Go to Variables tab
2. Add each variable:

```
OPENROUTER_API_KEY = your_key_here
HF_TOKEN = your_token_here
ENVIRONMENT = production
FRONTEND_URL = https://your-frontend.vercel.app
```

**Optional** (for observability):
```
LANGFUSE_PUBLIC_KEY = your_key
LANGFUSE_SECRET_KEY = your_key
USE_LANGFUSE = true
```

### Step 4: Configure Networking

1. Go to "Networking" tab
2. Enable "Public URL"
3. Note the generated URL (e.g., `https://legality-ai-prod.railway.app`)
4. Update frontend `VITE_API_URL` variable in Vercel

### Step 5: Deploy

1. Click "Deploy"
2. Monitor deployment in Railway dashboard
3. Check logs for errors
4. Test API: `curl https://your-backend.railway.app/health`

**Auto-deployment**: Every push to `main` branch auto-deploys

## Post-Deployment

### Verify Frontend

1. Visit frontend URL
2. Check browser console for errors
3. Verify API connection works

### Verify Backend

1. Test health endpoint:
   ```bash
   curl https://your-backend.railway.app/health
   ```

2. Check API docs:
   ```
   https://your-backend.railway.app/docs
   ```

3. Test contract analysis (with valid PDF)

### Configure CORS

Update backend `main.py` with production frontend URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Development
        "https://your-frontend.vercel.app"  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Monitoring & Logs

### Vercel Logs

1. Dashboard → Project → Deployments
2. Click deployment → Logs
3. View build and runtime logs

### Railway Logs

1. Dashboard → Service → Logs
2. Real-time streaming of application logs
3. Filter by log level

## Troubleshooting

### Frontend Build Fails

**Error: `npm ERR! 404`**
```
- Check package.json versions
- Ensure dependencies are correct
- Try: rm -rf node_modules && npm install
```

### Backend Build Fails

**Error: `ModuleNotFoundError`**
```
- Ensure requirements.txt in backend/ root
- Check Python version (3.11+)
- Verify all packages listed
```

**Error: `Port already in use`**
```
- Railway uses $PORT environment variable
- Backend must use: --port $PORT
```

### API Connection Fails

**Error: `CORS error`**
```
- Update CORS origins in backend
- Check frontend URL in environment variables
- Ensure API URL matches in frontend
```

**Error: `SSL certificate error`**
```
- Vercel/Railway provide free SSL
- Should be automatic
- Check for custom domain issues
```

### Model Loading Times Out

**Problem: Request times out during model download**
```
- First deploy can take 10+ minutes
- Model is ~500MB
- Don't cancel deployment
- Subsequent requests will be faster (cached)
```

**Solution:**
```
- Pre-download model in a separate build step
- Or increase Railway timeout settings
```

## Custom Domain Setup

### Vercel Custom Domain

1. Dashboard → Settings → Domains
2. Click "Add"
3. Enter your domain
4. Follow DNS instructions
5. Update frontend URL everywhere

### Railway Custom Domain

1. Service → Networking
2. Click "Add Domain"
3. Enter your domain
4. Configure DNS records
5. Update API URL in Vercel environment variables

## CI/CD Pipeline

Automated with GitHub Actions (see `.github/workflows/`):

```
Push to main
    ↓
GitHub Actions
    ├─ Run tests
    ├─ Lint code
    ├─ Build frontend
    └─ On success:
        ├─ Deploy frontend to Vercel
        └─ Deploy backend to Railway
```

## Rollback

### Vercel Rollback

1. Dashboard → Deployments
2. Find previous deployment
3. Click → "Redeploy"

### Railway Rollback

1. Dashboard → Deployments
2. Find previous version
3. Click "Redeploy"

## Environment-Specific Configuration

Manage across environments:

```
Development (localhost)
├── Frontend: http://localhost:5173
├── Backend: http://localhost:8000
└── API Key: Development key

Production (Deployed)
├── Frontend: https://your-domain.vercel.app
├── Backend: https://your-domain.railway.app
└── API Key: Production key
```

## Security Checklist

- [ ] API keys not in version control
- [ ] Environment variables set in deployment platform
- [ ] HTTPS enabled (automatic)
- [ ] CORS configured correctly
- [ ] Database credentials secure (when added)
- [ ] Rate limiting enabled
- [ ] Error messages don't expose internals

## Performance Optimization

### Frontend
- Frontend assets cached via Vercel CDN
- Image optimization
- Code splitting via Vite

### Backend
- Model caching after first load
- Connection pooling
- Response compression

## Cost Estimation (Free Tier)

- **Vercel**: Free for public repos
- **Railway**: $5/month free credit
  - Typical usage: ~$2-3/month

## Next Steps

1. ✅ Frontend deployed
2. ✅ Backend deployed
3. 📊 Set up monitoring (Langfuse)
4. 📈 Monitor costs
5. 🔄 Set up backups
