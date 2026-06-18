# Makefile for Legality AI Development

.PHONY: help install dev test lint format clean deploy

help:
	@echo "Legality AI - Available Commands"
	@echo "================================="
	@echo ""
	@echo "Development:"
	@echo "  make dev              - Start both frontend and backend"
	@echo "  make backend-dev      - Start backend only (port 8000)"
	@echo "  make frontend-dev     - Start frontend only (port 5173)"
	@echo ""
	@echo "Installation:"
	@echo "  make install          - Install all dependencies"
	@echo "  make install-backend  - Install backend deps"
	@echo "  make install-frontend - Install frontend deps"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test             - Run all tests"
	@echo "  make test-backend     - Run backend tests"
	@echo "  make test-frontend    - Run frontend tests"
	@echo "  make lint             - Lint all code"
	@echo "  make format           - Format all code"
	@echo "  make type-check       - Run type checking"
	@echo ""
	@echo "Evaluation:"
	@echo "  make eval             - Run gold standard accuracy evaluation"
	@echo "  make eval-metrics-test- Unit test the metric math (no model needed)"
	@echo ""
	@echo "Building:"
	@echo "  make build            - Build frontend for production"
	@echo "  make build-frontend   - Build frontend only"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            - Remove build artifacts and cache"
	@echo "  make clean-backend    - Clean backend cache"
	@echo "  make clean-frontend   - Clean frontend cache"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy-frontend  - Deploy frontend to Vercel"
	@echo "  make deploy-backend   - Deploy backend to Railway"
	@echo ""

install: install-backend install-frontend

install-backend:
	@echo "Installing backend dependencies..."
	cd backend && python -m venv venv
	. backend/venv/bin/activate && pip install -r backend/requirements.txt
	@echo "✅ Backend dependencies installed"

install-frontend:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ Frontend dependencies installed"

dev:
	@echo "Starting development environment..."
	@echo "Backend will run on: http://localhost:8000"
	@echo "Frontend will run on: http://localhost:5173"
	@echo ""
	@echo "Opening two terminals..."
	@echo "Run these commands in separate terminals:"
	@echo "  Terminal 1: make backend-dev"
	@echo "  Terminal 2: make frontend-dev"

backend-dev:
	@echo "Starting backend..."
	cd backend && . venv/bin/activate && uvicorn app.main:app --reload

frontend-dev:
	@echo "Starting frontend..."
	cd frontend && npm run dev

test: test-backend

test-backend:
	@echo "Running backend tests..."
	cd backend && . venv/bin/activate && pytest -v

test-frontend:
	@echo "Running frontend tests..."
	cd frontend && npm run test

eval:
	@echo "Running gold standard evaluation against backend/dataset/synthetic_gold_standard_with_nli.json..."
	cd ml/evaluation && pip install -r requirements.txt --break-system-packages && python test_gold_standard.py

eval-metrics-test:
	@echo "Unit testing the metric math (precision/recall/F1/NDCG/MRR) -- no model or network required..."
	cd ml/evaluation && pip install -r requirements.txt --break-system-packages && pytest test_metrics.py -v

lint: lint-backend lint-frontend

lint-backend:
	@echo "Linting backend code..."
	cd backend && . venv/bin/activate && flake8 app/ && pylint app/

lint-frontend:
	@echo "Linting frontend code..."
	cd frontend && npm run lint

format: format-backend format-frontend

format-backend:
	@echo "Formatting backend code..."
	cd backend && . venv/bin/activate && black app/

format-frontend:
	@echo "Formatting frontend code..."
	cd frontend && npm run format

type-check:
	@echo "Running type checking..."
	cd backend && . venv/bin/activate && mypy app/

build: build-frontend

build-frontend:
	@echo "Building frontend for production..."
	cd frontend && npm run build
	@echo "✅ Frontend build complete (output: frontend/dist)"

clean: clean-backend clean-frontend

clean-backend:
	@echo "Cleaning backend cache..."
	find backend -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find backend -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find backend -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/.coverage backend/htmlcov
	@echo "✅ Backend cleaned"

clean-frontend:
	@echo "Cleaning frontend cache..."
	rm -rf frontend/node_modules frontend/dist frontend/.vite
	@echo "✅ Frontend cleaned"

.PHONY: help install install-backend install-frontend dev backend-dev frontend-dev
.PHONY: test test-backend test-frontend eval eval-metrics-test lint lint-backend lint-frontend
.PHONY: format format-backend format-frontend type-check build build-frontend
.PHONY: clean clean-backend clean-frontend
