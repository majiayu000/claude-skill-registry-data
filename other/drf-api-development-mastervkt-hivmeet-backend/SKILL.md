---
name: drf-api-development
description: 'Design, implement, and harden Django REST Framework endpoints for HIVMeet backend. Use for ViewSet/APIView work, URL conventions, status codes, pagination, filtering, and API contract compliance.'
argument-hint: 'Describe endpoint(s), method(s), expected payload/response, auth requirements, and app name.'
user-invocable: true
---

# DRF API Development

## Purpose
Ship backend endpoints that match API contract exactly and remain stable across frontend integrations.

## Use When
- Creating or modifying endpoints in authentication, profiles, matching, messaging, subscriptions, or resources
- Adding custom actions in ViewSets
- Fixing status code/response shape mismatches
- Implementing pagination/filtering behavior

## Mandatory Workflow

### 1. Contract-First Definition
- Start from docs/API_DOCUMENTATION.md and project API rules
- Confirm URL shape: /api/v1/{resource}/{action}/
- Confirm method, auth, permissions, request schema, response schema, error schema

### 2. Select Endpoint Pattern
- Use ModelViewSet for CRUD-oriented resources
- Use APIView/function view for single-purpose actions
- Keep views thin; move business logic to services.py

### 3. Implement Serializer-Led IO
- Validate all request inputs through serializers
- Avoid direct request.data assignment to models
- Return serializer data for success paths

### 4. Enforce Status Code Discipline
- 200 for successful reads/updates
- 201 for creation/actions producing new resources
- 204 for successful delete/no-content operations
- 4xx/5xx mapped to uniform error payload format

### 5. Add Filtering/Pagination Deterministically
- Query params in snake_case
- Resource IDs in path, not query for retrieve/detail actions
- Stable ordering and safe defaults for list endpoints

### 6. Security and Privacy Gate
- Require IsAuthenticated where endpoint is protected
- Apply object-level permissions where needed
- Ensure sensitive fields are not exposed to unauthorized users

### 7. Non-Regression Validation
- Verify happy path and expected failures (400/401/403/404 at minimum)
- Validate endpoint contract from request to response shape
- Run impacted tests before completion

### 8. Output Contract
1. Endpoint(s) implemented/audited
2. Files changed
3. Contract alignment evidence
4. Status code and error mapping summary
5. Tests executed and residual risks

## Quality Gates
- No endpoint without explicit permission strategy
- No undocumented response shape changes
- No direct model writes from unvalidated request payload

## Notes
- Keep behavior backward compatible unless explicit version change is requested.
