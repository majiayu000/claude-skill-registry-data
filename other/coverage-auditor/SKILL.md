---
name: coverage-auditor
description: "Use when adding or updating tests for Django, DRF, Celery, admin, serializer, plugin, or Next.js code, or when closing a coverage gap. Trigger phrases include add tests, improve coverage, pytest, vitest, missing branch, serializer test, admin test, and route handler test."
---

# Coverage Auditor Skill

Use this skill to add the smallest effective tests around the changed behavior.

## Rules

- **Backend:** Use `pytest` with the existing patterns in `core/tests/` and `tests/`.
- **Frontend:** Use `vitest` with colocated `*.test.ts` and `*.test.tsx` files beside the route, page, or component under `frontend/src/`.
- Mock external integrations such as feed parsing, Reddit, email providers, Qdrant, or LLM calls instead of relying on live services.
- Prefer focused behavior tests over broad snapshot-style tests.
- For defensive branches that are intentionally unreachable, document exclusions explicitly with `# pragma: no cover` or `/* v8 ignore next */` only when justified.

## Testing Guidance

- Analyze the changed file first and cover the real branch points: validation failures, access control, empty states, duplicate handling, service failures, and success paths.
- For backend work, add tests near the closest existing module, such as:
  - `core/tests/test_serializers.py`
  - `core/tests/test_admin.py`
  - `core/tests/test_tasks.py`
  - `core/tests/test_newsletters.py`
  - `core/tests/test_pipeline.py`
- For frontend work, add or extend the nearest colocated `*.test.ts` or `*.test.tsx` file beside the owning route, page, or component.
- When adding new frontend tests, keep imports sorted to satisfy the repo's ESLint import-order rules. If you hit `Run autofix to sort these imports!`, fix the import block or run file-scoped ESLint before moving on.
- After changing tests, run the narrowest relevant validation command first.
- For Provider/Wrapper components, do not test state or initialization. Instead, render a consumer child component and assert that the context values or library configurations (like QueryClient options) match the expected project defaults.
- For Server Components, prioritize unit testing exported helper functions (like deriveSourceStatus) for logic, and use integration tests to verify that API data is mapped correctly to the UI components (badges, tables, etc.). Mock all library API calls using vi.mock.
- Out of Scope: Root layouts, static metadata, font configurations, and pure "pass-through" providers.
- In Scope: Layouts with conditional rendering, breadcrumb logic, or role-based access checks.

## References

- Backend commands are captured in `justfile` as `just backend-test`, `just backend-test-coverage`, and `just backend-lint`.
- Frontend commands are captured in `frontend/package.json` and the repo `justfile` as `npm run test`, `npm run test:coverage`, and `just frontend-lint`.
- Use `python manage.py check` after Django-side structural changes.
