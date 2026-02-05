---
name: backend-rust
description: Rust/WASM backend in api-rust/. High-performance alternative using workers-rs, utoipa for OpenAPI, and Supabase REST API. Port 9999 for local dev. 10-100x faster than Python.
---

# Skill: Backend Rust

High-performance Rust backend development for Cloudflare Workers.

## Routing Logic

Analyze the user's intent and route to the appropriate workflow:

**Route Development** → `workflows/create-route.md`
- "Create a Rust endpoint for [feature]"
- "Add a route handler for [resource]"
- "Implement [endpoint] in Rust"

**Model Development** → `workflows/create-model.md`
- "Create a Rust struct for [entity]"
- "Add serde model for [data]"
- "Define types for [feature]"

**Database Operations** → `workflows/database.md`
- "Query Supabase from Rust"
- "Use the Supabase REST client"

**Authentication** → `workflows/auth.md`
- "Protect Rust endpoint"
- "Validate JWT in Rust"

**Configuration Questions** → `context/config.md`
- "How do I build the Rust backend?"
- "What's the binary size?"
- "How to optimize WASM?"

## Workflows

- `workflows/create-route.md` - Create new API endpoints
- `workflows/create-model.md` - Define Rust structs
- `workflows/database.md` - Supabase REST operations
- `workflows/auth.md` - JWT authentication

## Context

- `context/config.md` - Build and deployment config
- `context/structure.md` - Directory structure
- `context/patterns.md` - Common Rust patterns
