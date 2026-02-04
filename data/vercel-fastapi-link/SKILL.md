---
name: vercel-fastapi-link
description: |
  Configure FastAPI for Vercel deployment.
  Bundled Resources: Includes 'vercel.json', CORSMiddleware, Python logging, Pydantic models, and personalization endpoints.
version: 1.4.0
inputs:
  github_pages_url:
    description: Your GitHub Pages URL for CORS configuration
    required: false
    default: "https://faiqahm.github.io"
    example: "https://username.github.io"
  extra_origins:
    description: Additional CORS origins (comma-separated)
    required: false
    default: ""
    example: "https://staging.example.com,https://preview.example.com"
  api_entry:
    description: Path to FastAPI main.py file
    required: false
    default: "api/main.py"
  project_name:
    description: Project name for API title
    required: false
    default: "Physical AI Book API"
  python_version:
    description: Python version for Vercel runtime
    required: false
    default: "3.11"
---

# Vercel FastAPI Link

Configure FastAPI for Vercel serverless deployment with CORS support for GitHub Pages frontend.

## Quick Setup

**Full automated setup with testing (recommended):**

```bash
.claude/skills/vercel-fastapi-link/scripts/setup.sh --github-pages https://faiqahm.github.io --test
```

**Basic setup:**

```bash
.claude/skills/vercel-fastapi-link/scripts/setup.sh
```

**With multiple CORS origins:**

```bash
.claude/skills/vercel-fastapi-link/scripts/setup.sh \
  --github-pages https://faiqahm.github.io \
  --extra-origins "https://staging.mysite.com,https://preview.mysite.com" \
  --test
```

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--github-pages URL` | GitHub Pages URL for CORS | `https://faiqahm.github.io` |
| `--extra-origins URLS` | Additional CORS origins (comma-separated) | - |
| `--api-entry PATH` | Path to FastAPI main.py | `api/main.py` |
| `--project-name NAME` | API project name | `Physical AI Book API` |
| `--python-version VER` | Python version for Vercel | `3.11` |
| `--skip-vercel-json` | Don't create vercel.json | off |
| `--skip-main` | Don't create main.py template | off |
| `--test` | Auto-test setup (starts server, hits /health) | off |
| `--deploy` | Deploy to Vercel after setup (agent-driven) | off |
| `--prod` | Deploy to production (use with --deploy) | off |
| `-h, --help` | Show help message | - |

## What It Does

### 1. Creates `runtime.txt`
Specifies Python version for Vercel deployment (e.g., `python-3.11`)

### 2. Creates `.env.example` and `.env`
Environment variable templates with:
- `GITHUB_PAGES_URL` - Primary CORS origin
- `EXTRA_CORS_ORIGINS` - Additional origins (comma-separated)
- Placeholders for database, auth, and API config

### 3. Creates `vercel.json`
Configures Vercel to:
- Use `@vercel/python` runtime
- Route `/api/*` requests to FastAPI
- Expose `/docs`, `/health`, and `/openapi.json`

### 4. Creates `api/main.py`
FastAPI application with:
- **Logging setup** for Vercel log debugging (configurable via `LOG_LEVEL` env var)
- **Pydantic models** for request/response validation and OpenAPI schema generation
- CORS middleware configured for GitHub Pages + extra origins
- Dynamic CORS from `EXTRA_CORS_ORIGINS` env var
- Health check endpoint at `/health`
- OpenAPI docs at `/docs`
- Example API routes with proper typing

### 5. Auto-Test (--test flag)
When `--test` is provided:
- Starts uvicorn on port 8765
- Hits `/health` endpoint
- Reports success/failure
- Catches import errors immediately

---

## Bundled Resources

### 1. Runtime Configuration

**File**: `runtime.txt`

```
python-3.11
```

### 2. Environment Template

**File**: `.env.example`

```bash
# GitHub Pages URL for CORS (required for production)
GITHUB_PAGES_URL=https://faiqahm.github.io

# Additional allowed origins (comma-separated, optional)
# EXTRA_CORS_ORIGINS=https://staging.example.com,https://preview.example.com

# Logging Configuration
# LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR
# Set to DEBUG for verbose output when debugging with Vercel logs

# Database (if needed)
# DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### 3. Vercel Configuration

**File**: `vercel.json`

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "api/main.py" },
    { "src": "/health", "dest": "api/main.py" },
    { "src": "/docs", "dest": "api/main.py" },
    { "src": "/openapi.json", "dest": "api/main.py" }
  ]
}
```

### 4. Logging Configuration

**File**: `api/main.py` (Logging section)

The template includes Python's standard logging configured for Vercel. Agents can read Vercel logs to debug issues.

```python
import logging

# Configure logging so agents can read Vercel logs for debugging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("physical-ai-book-api")

# Adjust log level from environment (DEBUG, INFO, WARNING, ERROR)
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logger.setLevel(getattr(logging, log_level, logging.INFO))

# Usage in endpoints:
logger.info(f"Fetching chapter with id={chapter_id}")
logger.warning(f"Chapter not found: id={chapter_id}")
logger.error(f"Unhandled exception: {exc}", exc_info=True)
```

### 5. Pydantic Models

**File**: `api/main.py` (Models section)

The template includes Pydantic models for request/response validation. This defines the "style" of data exchanged between frontend and backend.

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., example="healthy")
    service: str = Field(..., example="physical-ai-book-api")
    timestamp: str = Field(..., example="2024-01-01T12:00:00Z")

class ChapterSummary(BaseModel):
    """Summary of a chapter for listing."""
    id: int = Field(..., example=1)
    title: str = Field(..., example="Introduction to Physical AI")
    slug: str = Field(..., example="intro")

class ChapterDetail(BaseModel):
    """Full chapter details."""
    id: int
    title: str
    content: str = Field(..., example="Chapter content goes here...")
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class ChapterListResponse(BaseModel):
    """Response model for chapter listing."""
    chapters: List[ChapterSummary]
    total: int = Field(..., example=3)

class ErrorResponse(BaseModel):
    """Standard error response model."""
    detail: str = Field(..., example="Resource not found")
    error_code: Optional[str] = Field(None, example="NOT_FOUND")
```

### 6. CORS Middleware

**File**: `api/main.py` (CORS section)

```python
# Get GitHub Pages URL from environment or use default
GITHUB_PAGES_URL = os.getenv("GITHUB_PAGES_URL", "https://faiqahm.github.io")

# Base allowed origins
allowed_origins = [
    "http://localhost:3000",      # Local Docusaurus dev
    "http://localhost:8000",      # Local FastAPI dev
    GITHUB_PAGES_URL,             # Production GitHub Pages
]

# Add extra origins from environment variable (comma-separated)
extra_origins_env = os.getenv("EXTRA_CORS_ORIGINS", "")
if extra_origins_env:
    for origin in extra_origins_env.split(","):
        origin = origin.strip()
        if origin and origin not in allowed_origins:
            allowed_origins.append(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin"],
    max_age=600,
)
```

### 7. Personalization Endpoints

**File**: `api/main.py` (Personalization section)

The template includes personalization endpoints for user data, recommendations, learning paths, and settings.

#### GET /api/personalization/profile
Get or create user profile for personalization.

```bash
curl "http://localhost:8000/api/personalization/profile?user_id=user-123"
```

Response:
```json
{
  "user_id": "user-123",
  "preferences": {
    "preferred_language": "en",
    "difficulty_level": "beginner",
    "topics_of_interest": [],
    "learning_style": "visual",
    "session_duration_minutes": 30
  },
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### POST /api/personalization/profile
Update user profile.

```bash
curl -X POST "http://localhost:8000/api/personalization/profile" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user-123", "preferences": {"difficulty_level": "intermediate"}}'
```

#### GET /api/personalization/recommendations
Get AI-driven content recommendations.

```bash
curl "http://localhost:8000/api/personalization/recommendations?user_id=user-123"
```

Response:
```json
{
  "user_id": "user-123",
  "recommendations": [
    {
      "id": "rec-001",
      "title": "Introduction to Physical AI",
      "description": "Start your journey into Physical AI and robotics",
      "chapter_id": 1,
      "relevance_score": 0.95,
      "reason": "Recommended starting point for all learners"
    }
  ],
  "generated_at": "2024-01-01T12:00:00Z"
}
```

#### GET /api/personalization/learning-path
Get personalized learning path.

```bash
curl "http://localhost:8000/api/personalization/learning-path?user_id=user-123"
```

Response:
```json
{
  "user_id": "user-123",
  "path_id": "path-user-123",
  "title": "Physical AI Learning Journey",
  "items": [
    {
      "order": 1,
      "chapter_id": 1,
      "title": "Introduction to Physical AI & ROS 2",
      "status": "not_started",
      "progress_percent": 0,
      "estimated_duration_minutes": 60
    }
  ],
  "overall_progress_percent": 0,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### POST /api/personalization/apply
Apply personalization settings.

```bash
curl -X POST "http://localhost:8000/api/personalization/apply" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "preferences": {
      "preferred_language": "en",
      "difficulty_level": "intermediate",
      "topics_of_interest": ["robotics", "ai"],
      "learning_style": "hands-on"
    },
    "notifications_enabled": true,
    "theme": "dark"
  }'
```

Response:
```json
{
  "success": true,
  "message": "Personalization settings applied successfully for user user-123",
  "applied_at": "2024-01-01T12:00:00Z"
}
```

### 8. Input Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `github_pages_url` | No | `https://faiqahm.github.io` | Primary frontend URL |
| `extra_origins` | No | - | Additional CORS origins |
| `api_entry` | No | `api/main.py` | FastAPI entry point |
| `project_name` | No | `Physical AI Book API` | API title |
| `python_version` | No | `3.11` | Python version for Vercel |

## Usage Instructions

### Step 1: Run Setup with Test

```bash
.claude/skills/vercel-fastapi-link/scripts/setup.sh --test
```

### Step 2: Verify Created Files

```
project/
├── api/
│   ├── __init__.py
│   └── main.py          # FastAPI application
├── vercel.json          # Vercel configuration
├── runtime.txt          # Python version
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── .env                 # Local environment (gitignored)
└── .gitignore           # Updated with .env
```

### Step 3: Test Locally (if --test not used)

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn api.main:app --reload --port 8000

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

### Step 4: Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables
vercel env add GITHUB_PAGES_URL
vercel env add EXTRA_CORS_ORIGINS  # Optional
```

### Step 5: Update Frontend

In your Docusaurus site, configure the API URL:

```javascript
// src/config.js
export const API_URL = process.env.NODE_ENV === 'production'
  ? 'https://your-project.vercel.app'
  : 'http://localhost:8000';
```

## Verification Checklist

### Basic Setup
- [ ] `runtime.txt` exists with Python version
- [ ] `.env.example` documents all environment variables
- [ ] `.env` is gitignored
- [ ] `vercel.json` exists in project root
- [ ] `api/main.py` contains FastAPI app with CORS
- [ ] `requirements.txt` includes fastapi, uvicorn, pydantic
- [ ] `--test` flag passes health check

### Endpoint Testing (curl)
```bash
# Health check
curl http://localhost:8000/health

# Get user profile
curl "http://localhost:8000/api/personalization/profile?user_id=test-user"

# Get recommendations
curl "http://localhost:8000/api/personalization/recommendations?user_id=test-user"

# Get learning path
curl "http://localhost:8000/api/personalization/learning-path?user_id=test-user"

# Apply personalization
curl -X POST "http://localhost:8000/api/personalization/apply" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test-user","preferences":{"difficulty_level":"intermediate"},"notifications_enabled":true,"theme":"dark"}'
```

### Endpoint Testing (pytest)
```python
# tests/test_personalization.py
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_profile():
    response = client.get("/api/personalization/profile?user_id=test-user")
    assert response.status_code == 200
    assert response.json()["user_id"] == "test-user"

def test_get_recommendations():
    response = client.get("/api/personalization/recommendations?user_id=test-user")
    assert response.status_code == 200
    assert "recommendations" in response.json()

def test_get_learning_path():
    response = client.get("/api/personalization/learning-path?user_id=test-user")
    assert response.status_code == 200
    assert "items" in response.json()

def test_apply_personalization():
    response = client.post(
        "/api/personalization/apply",
        json={
            "user_id": "test-user",
            "preferences": {"difficulty_level": "intermediate"},
            "notifications_enabled": True,
            "theme": "dark"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] == True
```

### Deployment
- [ ] Vercel deployment successful
- [ ] Frontend can call API without CORS errors
- [ ] All personalization endpoints respond correctly

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **CORS error in browser** | Verify `allowed_origins` includes your GitHub Pages URL |
| **404 on Vercel** | Check `vercel.json` routes match your endpoints |
| **Module not found** | Ensure `requirements.txt` is in project root |
| **Wrong Python version** | Check `runtime.txt` matches your code requirements |
| **Cold start slow** | Normal for serverless; first request takes longer |
| **Environment variable not set** | Use `vercel env add VARIABLE_NAME` |
| **--test fails** | Check for import errors in api/main.py |
| **Multiple origins needed** | Use `--extra-origins` or set `EXTRA_CORS_ORIGINS` env var |

### Common CORS Issues

**Problem**: `Access-Control-Allow-Origin` header missing

**Solution**: Ensure the exact origin (including protocol) is in `allowed_origins`:
```python
# In Vercel Dashboard > Settings > Environment Variables:
GITHUB_PAGES_URL=https://username.github.io
EXTRA_CORS_ORIGINS=https://staging.example.com,https://preview.example.com
```

### Testing the --test Flag

```bash
# Run with test
.claude/skills/vercel-fastapi-link/scripts/setup.sh --test

# Expected output:
# ✓ Health check passed: {"status":"healthy","service":"physical-ai-book-api"}
# ✓ All tests passed! Your API is ready.
```

## Requirements

- Python 3.9+ (default: 3.11)
- FastAPI 0.100.0+
- Vercel account
- Vercel CLI (`npm i -g vercel`)

## Environment Variables

| Variable | Description | Where to Set |
|----------|-------------|--------------|
| `GITHUB_PAGES_URL` | Primary frontend URL for CORS | Vercel Dashboard |
| `EXTRA_CORS_ORIGINS` | Additional origins (comma-separated) | Vercel Dashboard |
| `LOG_LEVEL` | Logging verbosity: DEBUG, INFO, WARNING, ERROR | Vercel Dashboard |

## Changelog

### v1.4.0 (2026-01-01)
**Agent-Driven Deployment**

Added `--deploy` flag for automated Vercel deployment:

- **New Flags:**
  - `--deploy` - Deploy to Vercel after setup (requires vercel CLI)
  - `--prod` - Deploy to production environment (use with --deploy)

- **Deployment Features:**
  - Auto-installs Vercel CLI if not found
  - Supports `VERCEL_TOKEN` env var for non-interactive deployment
  - Extracts and displays deployment URL
  - Auto-tests deployed /health endpoint
  - Shows API docs and health check URLs

- **Usage:**
  ```bash
  # Preview deployment
  .claude/skills/vercel-fastapi-link/scripts/setup.sh --deploy

  # Production deployment
  .claude/skills/vercel-fastapi-link/scripts/setup.sh --deploy --prod

  # With token (for CI/CD or agent use)
  VERCEL_TOKEN=xxx .claude/skills/vercel-fastapi-link/scripts/setup.sh --deploy --prod
  ```

---

### v1.3.0 (2026-01-01)
**Personalization Endpoints**

Added complete personalization API for educational content:

- **New Pydantic Models:**
  - `UserPreferences` - Learning preferences (language, difficulty, topics, style, duration)
  - `UserProfile` - User profile with preferences and timestamps
  - `Recommendation` - Content recommendation with relevance score
  - `RecommendationsResponse` - List of recommendations
  - `LearningPathItem` - Single learning path item with progress tracking
  - `LearningPath` - Complete personalized learning path
  - `PersonalizationSettings` - Settings to apply
  - `PersonalizationApplyResponse` - Apply confirmation

- **New Endpoints:**
  - `GET /api/personalization/profile` - Get/create user profile
  - `POST /api/personalization/profile` - Update user profile
  - `GET /api/personalization/recommendations` - AI-driven content suggestions
  - `GET /api/personalization/learning-path` - Personalized learning path
  - `POST /api/personalization/apply` - Save personalization settings

- **Updated Verification Checklist:**
  - Added curl examples for all personalization endpoints
  - Added pytest test examples for all endpoints
  - Organized into Basic Setup, Endpoint Testing, and Deployment sections

- **Note:** Uses in-memory storage for demo; production needs database integration

---

### v1.2.0 (2026-01-01)
**Logging & Pydantic Models**

Added Python logging and Pydantic model examples:

- **Logging Setup:**
  - Standard Python logging configured for Vercel log debugging
  - Configurable via `LOG_LEVEL` environment variable (DEBUG, INFO, WARNING, ERROR)
  - Format: `%(asctime)s | %(levelname)s | %(name)s | %(message)s`
  - Agents can read Vercel logs to debug issues

- **Pydantic Models:**
  - `HealthResponse` - Health check response model
  - `ChapterSummary` - Summary for chapter listing
  - `ChapterDetail` - Full chapter details with content
  - `ChapterListResponse` - Paginated chapter list
  - `ErrorResponse` - Standard error response with error_code

- **Updated requirements.txt:** Added `pydantic` dependency

---

### v1.1.0 (2026-01-01)
**Enhanced Setup Script**

Added command-line options and auto-testing:

- **New Command Options:**
  - `--github-pages URL` - Specify GitHub Pages URL
  - `--extra-origins URLS` - Additional CORS origins (comma-separated)
  - `--api-entry PATH` - Custom FastAPI entry point
  - `--project-name NAME` - API project name
  - `--python-version VER` - Python version for Vercel
  - `--skip-vercel-json` - Skip vercel.json creation
  - `--skip-main` - Skip main.py template creation
  - `--test` - Auto-test setup (starts server, hits /health)
  - `-h, --help` - Show help message

- **Auto-Test Feature:**
  - Starts uvicorn on port 8765
  - Hits `/health` endpoint
  - Reports success/failure
  - Catches import errors immediately

- **Improved Output:** Colored terminal output with progress indicators

---

### v1.0.0 (2026-01-01)
**Initial Release**

Basic FastAPI + Vercel deployment setup:

- **Files Created:**
  - `runtime.txt` - Python version specification
  - `.env.example` - Environment variable template
  - `.env` - Local environment file (gitignored)
  - `vercel.json` - Vercel routing configuration
  - `api/main.py` - FastAPI application
  - `api/__init__.py` - Python package marker

- **Core Features:**
  - CORS middleware for GitHub Pages frontend
  - Dynamic CORS origins from `EXTRA_CORS_ORIGINS` env var
  - Health check endpoint at `/health`
  - OpenAPI docs at `/docs`
  - Example chapter API routes

- **Vercel Configuration:**
  - `@vercel/python` runtime
  - Routes for `/api/*`, `/health`, `/docs`, `/openapi.json`

---

## Related

- [Vercel Python Runtime Docs](https://vercel.com/docs/functions/runtimes/python)
- [FastAPI CORS Docs](https://fastapi.tiangolo.com/tutorial/cors/)
- [GitHub Pages Deployment](https://docs.github.com/en/pages)
- Skill: `github-pages-deploy` (for frontend deployment)
- ADR-001: Deployment Infrastructure Stack
