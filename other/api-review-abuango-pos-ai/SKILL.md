---
name: api-review
description: Review API design for consistency, naming conventions, versioning, and best practices. Use when designing APIs, reviewing endpoints, or when user mentions "API review", "API design", "endpoint review", "REST API", "API conventions", or "API consistency".
allowed-tools: Read, Glob, Grep, Bash
---

# API Review Skill

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

You are reviewing API design for consistency, correctness, and adherence to REST best practices. APIs are contracts — once published, they're hard to change.

## Process

### Step 1: Discover Endpoints

1. **Find route files** — Look for:
   - Laravel: `routes/api.php`, `routes/web.php`
   - Express/Fastify: `routes/`, `src/routes/`
   - Next.js: `app/api/`, `pages/api/`
2. **List all endpoints** — Method, path, controller, middleware
3. **Check for API versioning** — `/api/v1/`, `/api/v2/` patterns

### Step 2: Review Naming Conventions

Check every endpoint against these rules:

- [ ] **Nouns, not verbs** — `/users` not `/getUsers`
- [ ] **Plural resources** — `/users` not `/user`
- [ ] **Kebab-case for multi-word** — `/user-preferences` not `/userPreferences`
- [ ] **Nested resources for relationships** — `/users/{id}/orders` not `/user-orders`
- [ ] **Consistent ID parameter naming** — `{id}` or `{userId}` but not mixed
- [ ] **No trailing slashes** — `/users` not `/users/`
- [ ] **No file extensions** — `/users` not `/users.json`

### Step 3: Review HTTP Methods

- [ ] **GET** — Read only, no side effects, cacheable
- [ ] **POST** — Create new resource, returns 201 + Location header
- [ ] **PUT** — Full update (replace), idempotent
- [ ] **PATCH** — Partial update, only changed fields
- [ ] **DELETE** — Remove resource, returns 204 or 200

Common mistakes:
- POST for updates (should be PUT/PATCH)
- GET with side effects (should be POST)
- DELETE that returns the deleted resource without the client needing it

### Step 4: Review Response Format

Check for consistent response structure:

```json
// Success (single resource)
{
  "data": { "id": "...", "type": "user", ... }
}

// Success (collection)
{
  "data": [...],
  "meta": { "total": 100, "page": 1, "per_page": 20 }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable message",
    "details": [{ "field": "email", "message": "Required" }]
  }
}
```

Check:
- [ ] **Consistent envelope** — All responses use the same wrapper structure
- [ ] **Pagination** — Collections return total count, page, per_page
- [ ] **Error format** — All errors use the same structure with machine-readable codes
- [ ] **HTTP status codes** — Correct codes (200, 201, 204, 400, 401, 403, 404, 409, 422, 500)

### Step 5: Review Authentication & Authorization

- [ ] **Auth middleware applied** — All non-public routes require authentication
- [ ] **Authorization checked** — Users can only access their own resources
- [ ] **Rate limiting** — Applied to public and sensitive endpoints
- [ ] **CORS** — Configured correctly for expected origins

### Step 6: Review Query Patterns

- [ ] **Filtering** — `?status=active&role=admin` (not POST body for filters)
- [ ] **Sorting** — `?sort=created_at&order=desc` (consistent parameter names)
- [ ] **Pagination** — `?page=1&per_page=20` (with sensible defaults and max limits)
- [ ] **Field selection** — `?fields=id,name,email` (optional, for performance)
- [ ] **Search** — `?q=search+term` or `?search=term` (consistent naming)

## Review Output Format

```markdown
# API Review: {PROJECT}

**Date:** {DATE}
**Endpoints Reviewed:** {count}
**API Version:** {version}

## Summary

**Status:** CONSISTENT | NEEDS_CHANGES | MAJOR_ISSUES

## Endpoint Inventory

| Method | Path | Auth | Status |
|--------|------|------|--------|
| GET | /api/v1/users | Yes | OK |
| POST | /api/v1/users | Yes | OK |

## Naming Issues

| Endpoint | Issue | Recommendation |
|----------|-------|----------------|
| GET /api/getUsers | Verb in path | Rename to GET /api/v1/users |

## Response Consistency

{Are all endpoints using the same response envelope?}

## Missing Endpoints

{Standard CRUD operations that should exist but don't}

## Security Concerns

{Auth/authz issues found}

## Recommendations

1. {Priority fix}
2. {Improvement}
```

## Save Review

Save to: `{teams_dir}/{team}/projects/{project}/reviews/api-{date}.md`

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
