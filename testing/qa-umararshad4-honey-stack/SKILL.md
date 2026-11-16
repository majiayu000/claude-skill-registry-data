---
name: qa
description: "Use to check a change in a real browser, QA a page or user flow, or when a UI change needs visual proof."
license: MIT
metadata:
  reviewed: "2026-11-14"
  sources: "tester-army/e2e 1d671f6786b1eff4b43718ddc413b0bfa21abbcb skills/e2e, skills/create-verification-skill, skills/migrate-to-e2e (Apache-2.0, entry filenames adapted; see references/tester-army/UPSTREAM.md); Chrome WebMCP and Playwright 1.64 docs (references/webmcp.md); garrytan/gstack 1.60.1.0 qa; MCT Post-Task Verification; emilkowalski/skills a81dbca07f2217b7103e510c0f13f8d5b017afc9 skills/break-ui/{SKILL.md,CATALOG.md}, skills/mobile-native/SKILL.md (MIT, adapted); vercel-labs/agent-browser 0.43.0 CLI help and evals/agent-browser benchmark (references/agent-browser.md)"
---

# QA with e2e

Use tester-army/e2e's actual CLI and project MCP server. Start with an existing matching test and the project's command; do not rebuild a working test setup. A check-only request produces findings and evidence. Change application code only when authorized. Respect an explicitly requested runner/browser or host-required tool and label that exception.

## Start with the smallest runnable scope

Map the request and changed files to cases and relevant viewports. Create a complete case matrix before the first full run. Keep cases independent so one failure cannot hide another requirement.

For worst-case data, overflow or localization stress tests, follow [UI stress testing](references/stress-ui.md). For phone/PWA issues, also use [mobile behavior](../frontend/references/mobile.md); emulator results are preliminary until the affected interaction runs on the target browser and a real device, and an unavailable device stays unverified. Motion review and frame profiling live in [motion review](../frontend/references/motion-review.md) and [motion performance](../frontend/references/motion-performance.md).

Reuse verified configuration, versions, sessions and dependency setup from this session. For a new target, inspect the package/lockfile, `e2e.config.*`, startup and auth; run `node --version`, `npx e2e --version`, and `npx e2e list`. Prove a deterministic smoke first; an existing matching test can serve as the smoke. A missing model provider blocks agent goals, not deterministic tests.

Load only the reference needed for the task. Prefer the installed version's `npx e2e guide <topic>` when it differs from the bundled snapshot.

| Need | Reference |
|---|---|
| Faster existing web QA, workers, reports, evidence cost | [fast QA](references/fast-qa.md) |
| Actual CLI commands and result handling | [command guide](references/e2e.md) |
| First-time setup or unfamiliar upstream workflow | [upstream workflow](references/tester-army/e2e/GUIDE.md) |
| Engine, app and provider setup | [setup](references/tester-army/e2e/references/setup.md) |
| Live inspection, locators and sessions | [MCP](references/tester-army/e2e/references/mcp.md) |
| Write a test | [writing tests](references/tester-army/e2e/references/writing-tests.md) |
| Agent goals, budgets and replay cache | [agent](references/tester-army/e2e/references/agent.md) |
| Run selection and CI | [running](references/tester-army/e2e/references/running.md) |
| Diagnose failures | [debugging](references/tester-army/e2e/references/debugging.md) |
| Bounded exploratory goal | [explore](references/tester-army/e2e/references/explore.md) |
| Broad bug bash | [bug bash](references/tester-army/e2e/references/bug-bash.md) |
| App-specific verification skill | [verification generator](references/tester-army/create-verification-skill/GUIDE.md) |
| Migrate an existing suite | [migration](references/tester-army/migrate-to-e2e/GUIDE.md) |
| Page-provided tools for eligible setup | [WebMCP](references/webmcp.md) |
| Agent steps through a page live (ad-hoc QA, repro, exploration) | [agent-browser](references/agent-browser.md) |

## Browser sandbox failures

If the browser rejects `file://` navigation or an artifact path outside its allowed workspace, use the project's existing HTTP dev server and the runner's permitted artifact directory. Read the error for the permitted root before retrying; report both the sandbox constraint and the saved artifact path. Do not repeat the blocked operation or disable the sandbox. If the host offers no permitted route, report the check as blocked.

## Run, then investigate only what needs it

- Use `screen`, `app`, `browser` and exact `expect` assertions. Do not mix raw Playwright configuration or locator signatures into e2e. `targets` owns the engine and app; `app.command` owns startup/cleanup. Keep user-owned servers and existing suites intact.
- Separate fixture setup from acceptance actions. Existing WebMCP tools can replace setup; `webmcpBatch` handles reviewed same-page fixture calls. Keep form, keyboard, search and visual acceptance checks on the real UI. Do not execute both setup paths or add an unrelated tool-contract demo. Missing optional WebMCP support falls back to e2e; an explicit WebMCP requirement remains failed/blocked.
- Preserve async readiness waits. After a real completion signal, compare an already-read value directly rather than polling it again. For a state transition, use the matching state option (such as `toBeChecked({ checked: false })`); negated locator matchers add a stability window. Keep that window when sustained absence is required. Never shorten waits or change an expectation merely to make a failure fast or green.
- Use bounded workers only when browser contexts, accounts and data are isolated. e2e schedules file/target units: group independent flows into a few files with shared helpers; keep dependent steps together. Shared accounts/data or constrained targets stay serial. The WebMCP launcher starts one browser per `--workers`. See fast QA before changing concurrency.
- Run the selected matrix once, read its native report, then narrow repairs to `file:line` or `--last-failed`. Keep verified goal names/params stable for cache reuse. After repairing an agent test, run it once with normal timeouts and `--no-cache` to prove the live path; deterministic tests need no model-based rerun.
- Use native JSON/Markdown reports instead of writing a converter for ordinary QA. Keep required failure screenshots and distinct visual-state evidence. Full traces/video and repeated screen dumps are diagnostic choices, not mandatory for every passing action. Preserve evidence before another run replaces it.

For live, agent-driven browsing with no matching test, prefer `agent-browser` when it is installed: it ties on wall time and the agent reads about 4.6× less snapshot text. If live MCP is needed, reuse its registration and session. New registration requires a new client session; a config edit alone does not prove tools loaded. Use `locate`/`run_code` and returned `Test line:` values. Close sessions when done. With the Playwright MCP plugin, save screenshots and files only under its allowed output directory (paths outside, including `/tmp`, are refused), and write `browser_run_code` as plain page code: `require`/`import` are unavailable, so read files with the agent's own tools. Native mobile uses its supported engine; desktop native apps have no e2e engine.

## Close with proof

Read the actual selected/passed/failed/flaky/skipped counts. Exit 0, an empty selection or a completed exploration alone does not prove the requested flow. Confirm each claimed bug with a failing repro; keep backend/persistence and permission checks where required. Do not suppress page errors.

Report the command, versions, case/viewport coverage, outcomes, cache/live status, artifact paths and untested scope. Separate WebMCP results from UI/backend proof. State worker and trace settings in speed comparisons, and measure matched repeated workloads before claiming a gain. Carry these boundaries into generated verification skills.

Done when every requested case has fresh evidence, cleanup is complete and all remaining failures or blockers are explicit.
