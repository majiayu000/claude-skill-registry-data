---
name: project-api-patterns
description: "Use when adding or changing Django REST Framework serializers, viewsets, nested routes, schema docs, or project-scoped endpoints in core/api.py, core/api_urls.py, or core/serializers.py. Trigger phrases include project API, nested route, DRF viewset, serializer validation, project_id endpoint, and drf-spectacular docs."
---

# Project API Patterns Skill

Use this skill when changing the project-scoped REST API.

## Rules

- Treat `Project` as the isolation boundary.
- Top-level project resources live on the base router; most other resources are nested under `/api/v1/projects/{project_id}/...`.
- Reuse `ProjectOwnedQuerysetMixin` in `core/api.py` for nested resources.
- Pass `project` through serializer context and enforce cross-project relationship validation in serializers.
- Keep API field names in `snake_case` to match current serializers and frontend types.
- Update drf-spectacular metadata in `core/api.py` when the endpoint contract changes.

## Implementation Guidance

- Add or update serializers in `core/serializers.py`.
- Add or update viewsets and schema decorators in `core/api.py`.
- Register routes in `core/api_urls.py` using the existing nested router pattern.
- If the frontend consumes the API, update `frontend/src/lib/types.ts` and `frontend/src/lib/api.ts`.
- Add or update focused tests near the changed behavior, usually under `core/tests/`.

## References

- `core/api.py`
- `core/api_urls.py`
- `core/serializers.py`
- `frontend/src/lib/types.ts`
- `frontend/src/lib/api.ts`
