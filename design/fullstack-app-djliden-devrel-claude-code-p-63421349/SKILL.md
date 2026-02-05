---
name: fullstack-app
description: Guidance for building fullstack apps with Vite (React + TypeScript) frontend and FastAPI backend. Use when demos need a web UI beyond what Streamlit provides.
allowed-tools: Read, Bash, Glob, Write, Edit
---

# Fullstack App Development (Vite + FastAPI)

## When to Use This vs Streamlit

**Use Streamlit if:**
- App is read-only (displaying charts/tables)
- User is you or colleagues (internal tool)
- State doesn't matter (page refresh resets inputs = fine)

**Use Vite + FastAPI if:**
- Need login/auth
- Need to save user data (CRUD)
- UI must feel responsive (Streamlit lags on every click)
- Showing to non-technical stakeholders (Shadcn looks polished)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Vite + React + TypeScript |
| Styling | Tailwind CSS + Shadcn UI |
| Backend | FastAPI (Python) |
| Package Manager | pnpm |
| The Glue | OpenAPI (FastAPI auto-generates it) |

---

## Project Setup

### 1. Initialize Structure

```bash
mkdir my-app && cd my-app

# Frontend
pnpm create vite@latest frontend --template react-ts
cd frontend
pnpm install

# Add Tailwind v4 (uses Vite plugin, NOT tailwind.config.js)
pnpm add tailwindcss @tailwindcss/vite
# Replace src/index.css contents with: @import "tailwindcss";

# Initialize Shadcn (use explicit flags to avoid interactive prompts)
pnpm dlx shadcn@latest init -y --base-color neutral

cd ..

# Backend
mkdir backend
cd backend
uv init
uv add fastapi uvicorn pydantic
```

### 2. Configure vite.config.ts (Tailwind v4)

**IMPORTANT:** Tailwind v4 uses a Vite plugin. Do NOT create a `tailwind.config.js` file.

```typescript
// frontend/vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### 3. Configure CORS (backend/main.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Alternative: Vite Proxy (avoids CORS entirely)**

Instead of CORS middleware, you can proxy API requests through Vite. Add to `vite.config.ts`:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, ''),
    },
  },
},
```

Then use `/api/analyze` instead of `http://localhost:8000/analyze` in your frontend fetch calls.

---

## The OpenAPI Workflow (Critical)

**The biggest risk:** Frontend guessing what backend built.

**The solution:** Use FastAPI's auto-generated OpenAPI spec as the contract.

### Workflow:

1. **Build backend first** with proper Pydantic models
2. **Run backend**: `uv run uvicorn main:app --reload`
3. **Check the contract**: Visit `http://localhost:8000/openapi.json`
4. **Build frontend against the contract** - Reference the spec, don't guess

### Frontend Typing Pattern

```typescript
// Define types matching your Pydantic models
interface AnalyzeRequest {
  text: string;
}

interface AnalyzeResponse {
  score: number;
  explanation: string;
}

// Type-safe fetch
async function analyzeText(data: AnalyzeRequest): Promise<AnalyzeResponse> {
  const res = await fetch('http://localhost:8000/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return res.json();
}
```

---

## Shadcn UI Rules

**Critical:** Shadcn components must be installed before use.

```bash
# Correct - install first
pnpm dlx shadcn@latest add button
# Then import
import { Button } from "@/components/ui/button"

# WRONG - this package doesn't exist
import { Button } from "shadcn-ui"
```

### Common components to install:
```bash
pnpm dlx shadcn@latest add button card input form dialog
```

### Project structure:
- `/components/ui/` - Shadcn base components (CLI puts them here)
- `/components/features/` - Your composed components using Shadcn

---

## Architecture Rules

### Frontend = Display Only
- No complex data manipulation in JS
- Use React.useState for UI toggles
- Use React.useEffect for data fetching
- Keep business logic in Python

### Backend = Logic & State
- All heavy lifting in Python
- Use Pydantic models for ALL request/response bodies
- This ensures frontend gets correct types

---

## Running the App

```bash
# Terminal 1: Backend
cd backend
uv run uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
pnpm run dev
# Opens at http://localhost:5173
```

---

## Leveling Up (For Complex Apps)

For simple demos (1-2 endpoints), the patterns above are sufficient.

For more complex apps:

| Need | Tool |
|------|------|
| Auto-generate TypeScript client | `npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client` |
| Caching, loading states, refetching | TanStack Query (React Query) |

These add complexity - only use if the demo genuinely needs them.
