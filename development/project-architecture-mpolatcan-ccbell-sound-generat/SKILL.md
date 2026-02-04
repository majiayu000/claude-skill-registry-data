---
name: project-architecture
description: Explain the codebase architecture, project structure, how components work together, API endpoints, data flow. Use when explaining code, understanding structure, or learning about the project.
allowed-tools: Read, Grep, Glob
---

# CCBell Sound Generator Architecture

AI-powered notification sound generator for the Claude Code plugin "ccbell", deployed on HuggingFace Spaces.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    HuggingFace Spaces                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                 Docker Container                       │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │           FastAPI Backend (Python)              │  │  │
│  │  │  ┌─────────────┐  ┌──────────────────────────┐  │  │  │
│  │  │  │ Static      │  │ API Routes               │  │  │  │
│  │  │  │ Files       │  │ /api/generate            │  │  │  │
│  │  │  │ (React)     │  │ /api/models              │  │  │  │
│  │  │  └─────────────┘  │ /api/themes              │  │  │  │
│  │  │                   │ /api/hooks               │  │  │  │
│  │  │  ┌─────────────┐  └──────────────────────────┘  │  │  │
│  │  │  │ WebSocket   │  ┌──────────────────────────┐  │  │  │
│  │  │  │ Progress    │  │ Audio Service            │  │  │  │
│  │  │  └─────────────┘  │ (Stable Audio Open)      │  │  │  │
│  │  │                   └──────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
ccbell-sound-generator/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── api/
│   │   │   ├── routes.py        # REST API endpoints
│   │   │   └── websocket.py     # WebSocket for progress
│   │   ├── core/
│   │   │   ├── config.py        # Settings (pydantic-settings)
│   │   │   ├── logging.py       # Loguru configuration
│   │   │   └── models.py        # Pydantic models
│   │   ├── services/
│   │   │   ├── audio.py         # Audio generation logic
│   │   │   ├── github.py        # GitHub releases integration
│   │   │   └── model_loader.py  # ML model loading
│   │   └── data/
│   │       ├── themes.py        # Theme presets (Sci-Fi, Retro, etc.)
│   │       └── hooks.py         # Claude Code hook definitions
│   ├── pyproject.toml           # Python dependencies
│   └── uv.lock                  # Reproducible lockfile
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── hooks/               # Custom React hooks
│   │   ├── lib/                 # API client, utilities
│   │   ├── types/               # TypeScript types
│   │   ├── App.tsx              # Main app component
│   │   └── main.tsx             # Entry point
│   ├── package.json
│   └── vite.config.ts           # Vite bundler config
├── .claude/
│   ├── commands/                # Slash commands
│   └── skills/                  # Auto-triggered skills
├── .github/workflows/
│   ├── ci.yml                   # Lint, build checks
│   └── deploy.yml               # HuggingFace deployment
└── Dockerfile                   # Multi-stage production build
```

## Key Components

### Backend Services

1. **Audio Service** (`backend/app/services/audio.py`)
   - Wraps Stable Audio Open models
   - Handles generation with progress callbacks
   - Manages job queuing and status

2. **Model Loader** (`backend/app/services/model_loader.py`)
   - Lazy loads ML models to manage memory
   - Supports both Small (341M) and 1.0 (1.1B) models
   - Caches loaded models

3. **Config** (`backend/app/core/config.py`)
   - Environment variable management with `CCBELL_` prefix
   - Pydantic settings validation

### Frontend Components

- **ThemeSelector**: Choose audio generation themes
- **HookSelector**: Select Claude Code hook type
- **GenerateButton**: Trigger generation with progress
- **AudioPlayer**: Play generated sounds
- **SoundLibrary**: Manage generated sounds (Zustand state)

### API Flow

```
User Request → POST /api/generate
    ↓
Create Job → Return job_id
    ↓
WebSocket /api/ws/{job_id}
    ↓
Model loads (if needed)
    ↓
Audio generation with progress updates
    ↓
GET /api/audio/{job_id} → Download WAV
```

## Key Files to Understand

- `backend/app/main.py` - App initialization, middleware, routes
- `backend/app/api/routes.py` - All REST endpoints
- `backend/app/services/audio.py` - Core generation logic
- `frontend/src/lib/api.ts` - API client
- `frontend/src/App.tsx` - Main UI composition
