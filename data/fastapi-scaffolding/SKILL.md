---
name: FastAPI Scaffolding
description: Generate and maintain the FastAPI backend structure for the RAG chatbot with proper project organization.
---

# FastAPI Scaffolding

## Instructions

1. Create or update the backend folder structure with these directories:
   - app/
     - main.py (entry point with health endpoint)
     - routers/ (for API endpoints)
     - services/ (for business logic)
     - schemas/ (for Pydantic models)
     - deps/ (for dependency injection)

2. Generate main.py with:
   - FastAPI app initialization
   - Health check endpoint at GET /health
   - CORS middleware configuration
   - Include routers setup

3. Create a chat router placeholder in routers/chat.py
   - Include basic route registration
   - Setup for POST /chat endpoint

4. Ensure proper Uvicorn configuration in requirements.txt and startup command
   - Include uvicorn, fastapi in dependencies
   - Provide proper startup command: uvicorn app.main:app --host 0.0.0.0 --port 7860

5. Follow deterministic, clean Python code standards
   - Use proper type hints
   - Follow PEP 8 style guidelines
   - Include proper error handling

## Examples

Input: "Create FastAPI backend structure"
Output: Creates the complete directory structure with main.py containing:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat

app = FastAPI(title="Physical AI & Humanoid Robotics RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(chat.router, prefix="/api/v1")
```