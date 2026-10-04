---
name: Explain Codebase Area
description: "Produce a senior-engineer walkthrough of a directory or subsystem: entry points, key modules, data flow, external dependencies, and owned rules. Triggers on 'explain this area', 'walk me through', 'tour of'. Output is a Markdown brief suited for onboarding or cross-team handoff."
model: inherit
---

## Purpose

Give a reader enough structure to navigate a subsystem without reading every file. The skill identifies entry points, traces the dominant data flow, names key types, and links to applicable convention rules and ADRs.

## When to Invoke

- An engineer is onboarding to a new area of the monorepo.
- A reviewer needs context on a PR touching an unfamiliar subsystem.
- Writing documentation for an owned subsystem.

## When NOT to Invoke

- For a single file (use `/skill-explain-pattern`).
- For architectural decisions (use the ADR agent).
- For the entire monorepo at once (too coarse).

## Inputs

- **path**: directory or glob (e.g. `api/src/services/opportunity/`).
- **depth** (optional): `overview` (default) or `deep`.

## Procedure

1. List files under the path; classify by role (entry point, service, model, util, test).
2. Identify public entry points (route handlers, exported components, CLI commands).
3. Trace the dominant data flow from entry to persistence (or API call) with 3–5 bullets.
4. Collect key types: Pydantic models, TypeScript interfaces, SQLAlchemy models.
5. List external dependencies (DB tables, S3 buckets, OpenSearch indexes, SSM parameters).
6. Link to applicable `documentation/rules/*.md` and any ADRs under `documentation/decisions/adr/` that reference symbols in the path.
7. Emit the Markdown brief.

## Outputs

```markdown
## Area: api/src/services/opportunity/

### Entry points
- `opportunity_service.py::OpportunityService` — used by route handlers in `api/src/api/opportunities_v1/`.

### Data flow
1. Route handler receives `OpportunitySearchRequest`.
2. Service calls `opportunity_search.query_opportunities` (OpenSearch).
3. Results hydrated with `OpportunityModel` rows from Postgres.
4. Audit entry written via `audit_log_service`.
5. Response serialized as `OpportunityResponse`.

### Key types
- `OpportunityModel` (SQLAlchemy)
- `OpportunityResponse` (Pydantic)

### External dependencies
- Postgres: `opportunity`, `opportunity_summary` tables
- OpenSearch: `opportunity-v2` index
- SSM: `/api/feature_flags/new_search`

### Governing rules / ADRs
- `documentation/rules/api-services.md`
- ADR-0021 (v1 opportunity search)
```

## Safety

- Read-only.
- Never invents data flow; if ambiguous, labels it "unclear".
- Never exposes credential references or environment values.
- FedRAMP: flags any mention of prod-only config as "requires team review before sharing".

## Examples

**Example 1 — Onboarding new engineer.** Tour of `api/src/services/opportunity/`.

**Example 2 — Cross-team handoff.** Deep brief on `frontend/src/services/search-client/`.

**Example 3 — Reviewer context.** Overview of `infra/api/` before reviewing a Terraform PR.

## Related

- `.cursor/skills/skill-explain-pattern/` — for single-file/idiom explanations.
- `.cursor/agents/contributor-onboarding.md` — the broader onboarding flow.
