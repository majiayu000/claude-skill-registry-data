---
name: verify-change
description: >-
  Prove a change works before calling it done: pick checks from what the diff touched (core, content, brand,
  ui, pwa, assistant, api, tools, .claude), run them fastest first, look at screenshots on phone viewports,
  get a review, and report verified vs not verified. Use before committing or a PR, or for "does it work?",
  "run the checks", "test it".
---

# Verify a change

The rule: **say only what you ran.** The dev server never proves the service worker, offline or install. Axe
never proves screen-reader support. The report separates "verified" from "not verified".

## 1. What changed

```bash
git status --porcelain
git diff --stat main...HEAD        # plus uncommitted: git diff --stat
```

If the working tree holds the user's unrelated work in progress, verify only your paths and say so.

## 2. Pick the checks (fastest first; stop at the first failure and fix it)

| Touched                                                                       | Run                                                                                                                       |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `packages/core/**`                                                            | `pnpm exec turbo run typecheck test:unit --filter=@mobywatel/core --filter=@mobywatel/pwa`                                |
| `packages/content/**`                                                         | the same for `@mobywatel/content`, plus the scenario tests in core; `pnpm run audit:guardrails`                           |
| `packages/brand/**`                                                           | `--filter=@mobywatel/brand --filter=@mobywatel/ui --filter=@mobywatel/pwa` (the contrast test lives in brand)             |
| `packages/ui/**`                                                              | `--filter=@mobywatel/ui --filter=@mobywatel/pwa`, then the UI checks below                                                |
| `apps/pwa/src/features/**`, screens                                           | typecheck + unit for the app, then the UI checks below                                                                    |
| `apps/pwa/vite.config.ts`, `src/pwa/**`, manifest, `public/**`, `vercel.json` | the PWA checks below                                                                                                      |
| assistant (`packages/core/src/assistant`, `features/assistant`)               | scenario + golden-format tests; injection cases; the assistant E2E flow offline                                           |
| `apps/pwa/api/**`                                                             | typecheck, unit tests with mocked fetch; `grep` the built `dist/` for the key's env name (must be absent)                 |
| `apps/pwa/messages/**`                                                        | every locale has the same keys; ICU parses (a unit test in the app); the `plain-polish` skill checklist                   |
| `tools/**`                                                                    | `node --test tools/__tests__/*.test.mjs`                                                                                  |
| `.claude/**`, `CLAUDE.md`, `AGENTS.md`                                        | `pnpm run audit:harness`, tool tests; confirm an edited agent or skill shows in the session list (the `ai-harness` skill) |
| any asset, persona, document view                                             | `pnpm run audit:guardrails` and a look at it against the `prototype-guardrails` skill                                     |

Across workspaces at once: `pnpm exec turbo run typecheck test:unit --affected`.

### UI checks

1. `pnpm run build && pnpm preview` (port 4173).
2. Playwright flow for the screen or matter (`pnpm --filter @mobywatel/pwa test:e2e -- <spec>`), with axe
   (zero violations) in light, dark and senior mode.
3. Screenshots at **390×844** and **360×800** (and senior mode on). Save them to the session scratchpad and
   **look at them**: clipping, overlap, contrast, disclaimer visible, focus ring.
4. Keyboard pass of the changed flow. Use the `accessibility` skill for anything beyond that.

### PWA checks

1. Build + preview. DevTools › Application: the manifest has no errors, the SW is activated, and the precache
   includes new assets or content.
2. The offline flow (`e2e/offline.spec.ts`, or manually: offline, reload, finish a matter).
3. The update prompt appears after a rebuild.
4. Lighthouse mobile on the preview: performance ≥ 90, accessibility 100, installable. Note the numbers.

## 3. The full gate

Before pushing: `pnpm run ci:quality` (format, lint, typecheck, unit, build, tool tests, harness and
guardrails audits). Before a submission deploy, also `pnpm run test:e2e` (the `competition-submission` skill).

## 4. Review

Run the `code-reviewer` agent on the diff; add the `accessibility-auditor` agent for UI changes. Fix
**blocking** findings and re-run the affected checks.

## 5. Report

```
Verified:      typecheck, unit (core 42, pwa 18), audit:guardrails, ci:quality
               preview: offline reload + meldunek flow (Playwright, webkit iPhone 13), axe 0
               screenshots 390x844 / 360x800, senior on: <scratchpad paths>
Not verified:  real iPhone install; VoiceOver pass; Lighthouse
Review:        code-reviewer: no blocking (1 nit fixed); accessibility-auditor: 1 should-fix open
```

Never write "works" for a layer you did not exercise.
