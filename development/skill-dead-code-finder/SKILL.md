---
name: Dead Code Finder
description: Identify unreferenced exports, unused React components, orphaned Python modules, and stale fixtures in the monorepo. Triggers on 'find dead code', 'cleanup unused', 'orphan check'. Produces a candidates list with confidence scores; never deletes.
---

## Purpose

Surface likely-dead code with enough context that a human can delete it safely. The skill is conservative: it reports candidates with an evidence trail, not a deletion list.

## When to Invoke

- During periodic tech-debt sweeps.
- After a major feature removal or refactor.
- Before a release where bundle size or API surface reduction is a goal.

## When NOT to Invoke

- On hot branches (false positives against in-flight changes).
- On code paths reachable only via feature flags currently OFF (use `/skill-feature-flag-audit` first).
- On public API handlers (they have external callers).

## Inputs

- **scope**: `frontend`, `api`, or `all` (default `all`).
- **path** (optional): restrict to a subdirectory.
- **include-tests** (optional): default `false`.

## Procedure

1. For frontend: run `ts-prune` (or equivalent) under `frontend/`; filter out entries re-exported or referenced via dynamic import strings.
2. For api: build an import graph from `api/src/` and list modules with zero inbound references; cross-check against `api/src/api/` route registrations.
3. Cross-reference all candidates against feature-flag config (`infra/` SSM keys, env templates) — skip anything gated by a flag that could be OFF in some env.
4. For each candidate, collect: file path, symbol name, last `git log` touch, inbound references (should be zero or only self).
5. Rank by confidence: `high` (no refs, no flag gating, > 90 days untouched), `medium`, `low`.
6. Emit the report. Do not delete.

## Outputs

```
Dead Code Finder — scope=all

HIGH confidence (7)
  frontend/src/utils/legacyDateFormat.ts  legacyDateFormat  last touched 2024-09-03  refs: 0
  api/src/services/v0_opportunity_service.py  V0OpportunityService  last touched 2024-07-11  refs: 0
  ...

MEDIUM confidence (12)
  frontend/src/components/Banner.tsx  Banner  refs: 1 (storybook only)
  ...

LOW confidence (23)  -- review manually
```

## Safety

- Never deletes files.
- Never flags exports referenced by string (e.g. dynamic imports, route registries) unless the registry has also been audited.
- Excludes feature-flag-gated code by default.
- Excludes generated files, migrations, and `__init__.py` re-exports.
- FedRAMP: never flags audit log or security middleware as dead without a manual review reminder.

## Examples

**Example 1 — Post-v0 removal.** 7 high-confidence orphans including the v0 opportunity service. Developer reviews, deletes in a scoped PR.

**Example 2 — Frontend-only sweep.** 12 orphan components; 4 referenced only by Storybook — medium confidence, human decides whether to keep stories.

**Example 3 — Flag-gated skip.** A module gated by `feature_new_search` is skipped because the flag is OFF in prod.

## Related

- `.cursor/skills/skill-feature-flag-audit/` — run first to separate flag-off code from truly dead code.
- `.cursor/skills/skill-bundle-size-check/` — confirm removals shrink the bundle.
