---
name: context-api-contracts
description: |
  Frontend-backend API contracts, routes, clients, and type definitions.
  Handles API endpoint definitions, request/response types, route configuration, and cross-stack integration.
  Use when working with API endpoints, request/response types, route definitions, or frontend-backend integration,
  or when user mentions API design, adding endpoints, type mismatches, API contracts, REST endpoints,
  client integration, "404 Not Found" errors, "Type error" in API calls, or route configuration issues.
tags: [api, contracts, integration, cross-stack]
---

# API Contracts

Navigate frontend-backend API integration, routes, clients, and data flow.

## Overview

API contracts define frontend ↔ backend communication. Critical for cross-stack changes.

## Backend API Routes

- `backend/api/*.py` - API v1 endpoints
- `backend/api/v2/*.py` - API v2 endpoints
- `backend/api/analytics_api.py`
- `backend/api/brokerage_connections.py`
- `backend/api/accounts.py`
- `backend/api/securities.py`

## Frontend API Clients

- `frontend/src/services/analyticsApi.ts`
- `frontend/src/services/researchApi.ts`
- `frontend/src/lib/apiClient.ts` - Base API client

## TypeScript Contracts

- `supabase/types/database.types.ts` - Database types
- `frontend/src/types/**/*.ts` - Frontend types

## Backend Middleware

- `backend/middleware/*.py` - Auth, CORS, etc.

## Tests

- `backend/tests/integration/` - API integration tests
- `frontend/e2e/` - E2E API tests

## Documentation

- **Internal**: `docs/backend/API_CONTRACTS.md` (create if needed)

## Related Areas

- See `context-clerk-integration` for auth middleware
- See `context-testing-infrastructure` for API test patterns
