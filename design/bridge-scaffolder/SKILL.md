---
name: bridge-scaffolder
description: "Use when creating or changing a feature that spans both the Django API and the Next.js frontend. Trigger phrases include full-stack feature, add endpoint and UI, wire frontend to backend, project dashboard change, and bridge serializer to frontend types."
---

# Bridge Scaffolder Skill

Use this skill when a change genuinely crosses the backend and frontend boundary.

## Rules

- **Django Side:** Follow the existing patterns in `core/api.py`, `core/api_urls.py`, and `core/serializers.py`.
- Most nested resources should stay project-scoped under `/api/v1/projects/{project_id}/...`.
- Keep business logic out of viewsets. Use `core/tasks.py`, `core/pipeline.py`, `core/newsletters.py`, `core/plugins/`, or nearby helpers for real workflow logic.
- **Next.js Side:** Update `frontend/src/lib/types.ts`, `frontend/src/lib/api.ts`, and the relevant pages, components, or route handlers under `frontend/src/app/`.
- Preserve the existing `snake_case` payload shape unless the backend contract is intentionally changing.

## Implementation Guidance

- Check `core/api_urls.py` for the current route topology and `core/api.py` for the schema helper patterns.
- Keep serializer validation aligned with project scoping and cross-project relationship rules.
- If the frontend consumes the new field or endpoint, reflect it in `frontend/src/lib/types.ts` and the corresponding API helpers.
- Update docs when the feature changes a core workflow or user-facing behavior.

## Related Guidance

- Use `project-api-patterns` when the backend portion is primarily a new or changed DRF resource.
- Use `coverage-auditor` immediately after scaffolding to add targeted backend and frontend tests.
