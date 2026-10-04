---
name: OpenAPI Sync
description: "Detect drift between the API OpenAPI spec and frontend TypeScript clients, then guide regeneration. Triggers on phrases like 'openapi sync', 'regenerate types', 'api types out of date', or when `api/openapi.generated.yml` or `frontend/src/types/` changes. Reports added/removed/changed endpoints and schemas with file:line citations and an exact regeneration command."
---

## Purpose

Keep `api/openapi.generated.yml` and the frontend's generated types in sync without forcing engineers to memorize the regeneration toolchain. The skill identifies the diff, explains what changed, and prints the exact commands to run.

## When to Invoke

- A PR touches `api/src/api/**/*_schemas.py` or `api/src/api/**/*_routes.py`.
- A PR touches `api/openapi.generated.yml`.
- A frontend developer hits a TypeScript error referencing a missing field on an API type.
- Before tagging a release that includes API surface changes.

## When NOT to Invoke

- For changes confined to API internals (services, repositories) with no schema impact.
- For documentation-only edits to OpenAPI descriptions.
- As a substitute for contract tests — pair with `skill-api-contract-test`.

## Inputs

- **base_ref** (optional): git ref to compare against (default: `origin/main`).
- **scope** (optional): `endpoints`, `schemas`, or `all` (default).

## Procedure

1. Run `git diff <base_ref>...HEAD -- api/openapi.generated.yml frontend/src/types/`. If empty, report "in sync" and exit.
2. Parse the OpenAPI YAML diff:
   - Added paths
   - Removed paths
   - Changed request/response schemas (track field additions, removals, type changes)
   - Added/removed components
3. For each changed endpoint, locate the corresponding frontend fetcher under `frontend/src/services/fetch/fetchers/` and the type under `frontend/src/types/`.
4. Classify each change:
   - **BREAKING** removed field, removed endpoint, type narrowed, required→optional reversed
   - **ADDITIVE** new optional field, new endpoint
   - **DOC** description-only change
5. For each BREAKING, list affected frontend call sites via `rg -l` against the type name.
6. Emit the regeneration command appropriate to the project (default: `make openapi-sync` or `cd frontend && npm run generate:api-types`; verify which exists in `Makefile` and `frontend/package.json`).
7. Cross-reference `documentation/rules/openapi.mdc` for naming and version constraints.
8. Emit the Output Format. Do not modify files.

## Outputs

```
OpenAPI Sync — base=origin/main
Spec status: drift detected

Endpoint changes (3):
  + POST  /v1/opportunities/{id}/bookmark           ADDITIVE
  ~ GET   /v1/opportunities/search                  BREAKING (removed `legacyStatus` from response)
  - GET   /v1/opportunities/{id}/legacy-summary     BREAKING (removed)

Schema changes (2):
  ~ OpportunityResponse        BREAKING — field `legacyStatus` removed
  + BookmarkRequest            ADDITIVE

Frontend impact:
  frontend/src/types/opportunity.ts                   regenerate
  frontend/src/services/fetch/fetchers/opportunityFetcher.ts  update call site
  frontend/src/components/search/ResultsList.tsx      uses removed field (L83)

Regeneration:
  $ make openapi-sync
  (alternatively: cd frontend && npm run generate:api-types)

Block merge: yes (2 BREAKING)
Suggested next: /skill-api-contract-test
```

## Safety

- Read-only. Never runs the regeneration command itself.
- Never edits `frontend/src/types/` (treat as generated).
- Never invents endpoints or schemas; reports only what is in the diff.
- Defers semver / release-note decisions to the changelog generator.

## Examples

**Example 1 — Pure additive**
A new optional `bookmarked` boolean. Skill reports ADDITIVE and prints the regen command. No call site changes required.

**Example 2 — Field rename**
`postedDate` → `posted_at`. Skill flags both directions as BREAKING, lists 4 affected components.

**Example 3 — In sync**
No diff under the watched paths. Skill returns "in sync" and exits 0.

## Related

- `.cursor/skills/skill-api-contract-test/` — generate contract tests after sync.
- `.cursor/skills/skill-impact-analysis/` — locate downstream consumers.
- `documentation/rules/openapi.mdc` — naming, versioning, deprecation policy.
