---
name: runtime-verification
description: Use for user-facing web behavior, browser bugs, remote assets, API proxies, responsive UI, or any change that cannot be proven from static tests; require real browser/network evidence and critical-flow execution before completion.
---
# Runtime Verification

Read `docs/RUNTIME_VERIFICATION.md` when the task is substantial.

## Minimum web gate
1. Start the actual application using a real command from `.ai/COMMANDS.json`.
2. Exercise the changed critical user journey in a real browser engine.
3. Capture mobile and desktop screenshots.
4. Capture console errors, uncaught page errors, request failures, and HTTP 4xx/5xx.
5. Inspect loading/error/empty/success/degraded states relevant to the change.
6. For remote media/APIs/fonts/demo assets, scan then probe critical dependencies.
7. Treat unexplained 403/404/5xx as failures, even if the page appears mostly usable.
8. Record generic render/network smoke as `runtime-browser` evidence.
9. Execute the changed critical user flow and record it separately as `critical-flow` evidence. A smoke-only pass cannot complete a user-facing feature.
10. If critical remote runtime resources exist, set the task trait `external_runtime_dependencies=true` and record an `external-probe` check.
11. Write browser artifacts to a fresh output directory (`--fresh-output`) so an old screenshot/report cannot masquerade as current evidence.
12. For async durable state, observe a monotonic signal before/after the action, reload, and prove restoration; a fixed sleep is not completion evidence.
13. Assert horizontal overflow and known fragile overlap regions on mobile, then visually review both mobile and desktop screenshots.

A plan, source-code review, generated test, or screenshot of the editor is not runtime evidence.

Prefer project-native Playwright/Cypress/e2e tests. `browser_smoke.mjs` is a generic baseline, not a substitute for task-specific user-flow assertions. When no project e2e test exists, create a small declarative flow spec and run `.ai/scripts/browser_flow.mjs --spec <file> --out <dir> --fresh-output`; use its durable-attribute, reload, overflow, and overlap actions instead of arbitrary JavaScript eval.
