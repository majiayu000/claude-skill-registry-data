---
name: Diff Summary
description: "Summarize a git diff into a senior-engineer PR description: intent, key changes grouped by surface (api/frontend/infra/docs), risks, and test coverage. Triggers on 'summarize diff', 'write PR description', 'what changed'. Produces Markdown ready to paste into a PR body."
model: inherit
---

## Purpose

Convert raw `git diff` output into a structured, reviewer-friendly PR description grouped by surface, with risk callouts and a test-coverage note. Reduces the "what is this PR doing?" overhead on large diffs.

## When to Invoke

- Before opening a PR with a non-trivial diff.
- When backfilling a PR description for a stacked branch.
- When drafting release notes for a batch of merges.

## When NOT to Invoke

- For single-file trivial changes (typo, lint fix).
- For merge commits or rebase-only diffs.
- For generated diffs (lockfiles, OpenAPI regens) as the sole content — the summary will be noise.

## Inputs

- **range**: git ref range (default `origin/main...HEAD`).
- **audience** (optional): `engineer` (default) or `pm`.

## Procedure

1. Run `git diff --stat <range>` to get file-level change footprint.
2. Classify files into surfaces: `api`, `frontend`, `infra`, `docs`, `tests`, `generated`.
3. For each non-generated file, extract the top-level symbols added/removed (functions, classes, components).
4. Identify risk signals: migrations, feature flag adds/removes, auth middleware, PII-adjacent fields, dependency upgrades.
5. Check for corresponding tests under `api/tests/`, `frontend/tests/`, or `__tests__/` in the same diff.
6. Emit the Markdown PR body.

## Outputs

```markdown
## Intent
One-paragraph summary of why this change exists.

## Changes by surface
### API
- `api/src/services/opportunity_service.py`: adds `close_opportunity()` and audit log entry.
- Alembic: `2026_04_07_add_closed_at.py` adds nullable `closed_at` column.

### Frontend
- `OpportunityCard.tsx`: shows "Closed" badge when `closed_at` is present.

## Risks
- Migration adds a nullable column (safe to deploy before code).
- New audit log path — confirm it writes to the FedRAMP audit sink.

## Test coverage
- `test_opportunity_service.py`: +2 tests
- No frontend unit test added — consider adding a Storybook story.
```

## Safety

- Read-only.
- Never invents intent; if the diff doesn't support a claim, labels it "unclear — author should clarify".
- Flags PII-adjacent columns explicitly (names ending in `_email`, `_ssn`, `_ein`, etc.).
- Never pastes secrets or `.env` content into the summary.

## Examples

**Example 1 — Full-stack feature.** Groups API + frontend + migration under one PR body.

**Example 2 — Infra-only.** Emits a concise Terraform-only summary with FedRAMP boundary reminder.

**Example 3 — PM audience.** Rewrites "Intent" and "Changes" without file paths, focused on user-visible impact.

## Related

- `.cursor/agents/pr-preparation.md` — the deeper PR prep flow.
- `.cursor/skills/skill-impact-analysis/` — for cross-service risk.
- `.cursor/agents/changelog-generator.md` — for release notes.
