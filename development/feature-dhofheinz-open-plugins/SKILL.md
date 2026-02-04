---
description: Implement production-ready features across database, backend, and frontend layers with incremental phased approach
argument-hint: <operation> [parameters...]
---

# Feature Implementation Router

Comprehensive feature implementation across the full stack with phased, incremental development approach. Routes feature implementation requests to specialized operations for different layers or full-stack implementation.

## Operations

- **implement** - Complete full-stack feature implementation across all layers (database, backend, frontend, integration)
- **database** - Database layer only (migrations, models, schemas, indexes)
- **backend** - Backend layer only (services, API endpoints, validation, tests)
- **frontend** - Frontend layer only (components, state, API integration, tests)
- **integrate** - Integration and polish phase (E2E tests, performance, security, documentation)
- **scaffold** - Scaffold feature structure and boilerplate across all layers

## Usage Examples

```bash
# Complete full-stack feature
/feature implement description:"user authentication with OAuth and 2FA" tests:"comprehensive"

# Database layer only
/feature database description:"user profiles table with indexes" migration:"add_user_profiles"

# Backend API only
/feature backend description:"REST API for product search with filters" validation:"strict"

# Frontend components only
/feature frontend description:"product catalog with infinite scroll and filters" framework:"react"

# Integration and polish
/feature integrate feature:"authentication flow" scope:"E2E tests and performance"

# Scaffold feature structure
/feature scaffold name:"notification-system" layers:"database,backend,frontend"
```

## Router Logic

Parse the first word of $ARGUMENTS to determine operation:

1. Extract operation from first word of $ARGUMENTS
2. Extract remaining arguments as operation parameters
3. Route to instruction file:
   - "implement" → Read `.claude/commands/fullstack/feature/implement.md` and execute
   - "database" → Read `.claude/commands/fullstack/feature/database.md` and execute
   - "backend" → Read `.claude/commands/fullstack/feature/backend.md` and execute
   - "frontend" → Read `.claude/commands/fullstack/feature/frontend.md` and execute
   - "integrate" → Read `.claude/commands/fullstack/feature/integrate.md` and execute
   - "scaffold" → Read `.claude/commands/fullstack/feature/scaffold.md` and execute

4. Pass extracted parameters to the instruction file
5. Return structured implementation

**Error Handling:**
- If operation is unrecognized, list available operations with examples
- If parameters are missing, request clarification with expected format
- If requirements are unclear, ask specific questions about scope and acceptance criteria
- Provide clear error messages with usage examples

**Security:**
- Validate all input parameters
- Ensure no hardcoded secrets in generated code
- Follow security best practices for each layer
- Include validation and sanitization in generated code

---

**Base directory:** `.claude/commands/fullstack/feature`
**Current Request:** $ARGUMENTS

Parse operation and route to appropriate instruction file now.
