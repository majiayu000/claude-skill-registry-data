---
name: Bundle Size Check
description: "Analyze the Next.js production build output for regressions in JS bundle size and flag oversize imports. Triggers on 'bundle size', 'bundle check', 'why is the bundle big', or after adding a new dependency to frontend/package.json. Produces a per-route delta report with offending modules and remediation hints."
model: inherit
---

## Purpose

Prevent bundle-size regressions from shipping by giving developers a fast local report on Next.js route bundle sizes, per-dependency weight, and the top offending imports, with concrete remediation (dynamic import, lighter alternative, tree-shake config).

## When to Invoke

- After adding or upgrading a dependency in `frontend/package.json`.
- Before merging a PR that touches `frontend/src/` and changes imports.
- When the Next.js build reports a route crossing the 200 KB first-load budget.
- As part of the pre-release performance sweep.

## When NOT to Invoke

- For backend-only changes.
- During active development (noise); reserve for pre-push or pre-merge.
- For storybook-only changes.

## Inputs

- **baseline**: git ref to compare against (default `origin/main`).
- **budget** (optional): KB first-load JS budget per route (default 200).
- **routes** (optional): restrict to a subset, e.g. `/search,/opportunity/[id]`.

## Procedure

1. Run `npm --prefix frontend run build` (or reuse the last build if `.next/` is fresh).
2. Parse `.next/build-manifest.json` and `.next/app-build-manifest.json` for per-route chunk lists.
3. Compute first-load JS per route from chunk sizes.
4. Check out `baseline`, repeat, then diff.
5. Run `npx --prefix frontend source-map-explorer` (or `@next/bundle-analyzer` JSON output) on the largest route to identify top offending modules.
6. Cross-reference `frontend/package.json` adds/upgrades against the diff.
7. Emit the report below.

## Outputs

```
Bundle Size Check — baseline origin/main @ abc123
Budget: 200 KB first-load JS

Route                 Current   Baseline   Delta     Budget
/search               218 KB    187 KB     +31 KB    OVER
/opportunity/[id]     192 KB    188 KB     +4 KB     OK
/                     156 KB    156 KB     0         OK

Top offenders on /search:
  lodash (full)         +28 KB   Use lodash-es + named imports
  moment                +12 KB   Replace with date-fns or native Intl
```

## Safety

- Read-only. Never edits `package.json` or source.
- Never installs new dependencies; uses the existing lockfile.
- Never runs a production build in a FedRAMP-tagged env; only in the developer sandbox.
- Falls back cleanly if `.next/` is absent — reports "baseline build missing" rather than guessing.

## Examples

**Example 1 — Post-dependency add.** Developer adds `chart.js`. Skill reports `/dashboard` +47 KB, recommends `react-chartjs-2` tree-shaking config or dynamic import.

**Example 2 — Route budget breach.** CI flagged `/search` over budget. Skill pinpoints a `lodash` full-import in a newly added util file and suggests the fix.

**Example 3 — No-op check.** Pre-release sweep returns "all routes within budget; no deltas > 5 KB", safe to ship.

## Related

- `.cursor/agents/performance-audit.md` — deeper runtime perf pass.
- `.cursor/skills/skill-dead-code-finder/` — often follows up with removable imports.
