---
name: javascript
description: "JavaScript: ESM/CJS, closures, event loop, async/promises, runtime validation for external data, monorepo/packaging awareness."
---

# javascript

ESM-first modern JavaScript: explicit async, validated boundaries, workspace-aware packaging.

## Activate when

- Writing, reviewing, or testing JavaScript (Node or browser); module, async, or packaging decisions.

## Do NOT activate for

- Type-level design (see languages/typescript); framework specifics (see frameworks/*).

## Procedure

1. Version: detect Node + package manager from package.json/engines/lockfiles; research in https://developer.mozilla.org/ and https://nodejs.org/docs/latest/ for those versions.
2. Modules: ESM for new code; CJS interop deliberate and documented; no extensionless-deep-import fragility.
3. Async: promises/async-await with explicit error paths; no floating promises; timers/resources cleaned up.
4. Boundaries: runtime validation (Zod or equivalent) for all external data — types don't exist at runtime.
5. Packaging: workspace layout respected; dependency ranges deliberate; lockfile committed.
6. Verify: tests green on pinned Node, lint clean, no unhandled rejections (fail a probe on purpose to confirm handling).

## References
- Registry: `../../research/documentation-search/references/framework-registry.yaml` (javascript, nodejs, npm, pnpm, bun, zod).
