---
name: backend-python
description: FastAPI Python backend in api/. Covers routes, models, Supabase integration, authentication, R2 storage, and Cloudflare Workers deployment. Port 9999 for local dev. OpenAPI docs at /docs.
---

# Skill: Backend Python

Comprehensive backend development support for the Python/FastAPI API.

## Routing Logic

Analyze the user's intent and route to the appropriate workflow:

**Route Development** → `workflows/create-route.md`
- "Create an endpoint for [feature]"
- "Add a [method] route for [resource]"
- "Implement the [endpoint_name] API"

**Model Development** → `workflows/create-model.md`
- "Create a model for [entity]"
- "Add Pydantic schema for [data]"
- "Define types for [feature]"

**Database Operations** → `workflows/database.md`
- "Query [table] from Supabase"
- "Insert data into [table]"
- "Add RLS-aware database call"

**Authentication** → `workflows/auth.md`
- "Protect this endpoint"
- "Get current user"
- "Validate JWT token"

**R2 Storage** → `workflows/r2-storage.md`
- "Upload file to R2"
- "Read from storage bucket"
- "List objects in R2"

**Configuration Questions** → `context/config.md`
- "What port is the backend on?"
- "How do I start the dev server?"
- "Where are environment variables?"

## Workflows

- `workflows/create-route.md` - Create new API endpoints
- `workflows/create-model.md` - Define Pydantic models
- `workflows/database.md` - Supabase database operations
- `workflows/auth.md` - Authentication and authorization
- `workflows/r2-storage.md` - R2 object storage operations

## Context

- `context/config.md` - Project configuration
- `context/structure.md` - Directory structure
- `context/patterns.md` - Common patterns
