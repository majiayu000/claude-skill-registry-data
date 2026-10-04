---
name: go
description: "End-to-end verification skill — make Claude actually prove its work instead of claiming success. Use as a suffix on ANY build/fix/refactor prompt ('build the login page /go', 'fix the checkout bug /go', 'refactor the auth module /go'), or standalone after long-running work when you return and want confirmation the code works. Selects the right verification surface automatically: bash for backend/CLI/library code (starts the server, hits the endpoints, runs the tests, reads the logs), browser automation for frontend (Playwright MCP / Claude Chromium extension — navigates, clicks, takes screenshots, checks console), and computer-use for desktop apps. After verification passes, chains into /simplify to delete any bloat introduced. Triggers on '/go', 'verify', 'check it works', 'kiểm tra chạy được chưa', 'test end to end', 'prove it works'."
---
# /go — Verify Then Simplify

You are closing the loop on the work that was just done. Your job is to **prove the code works end-to-end** (not just that it compiles, not just that unit tests pass) and then run `/simplify` to remove any bloat the implementation introduced.

Based on the Anthropic guidance that giving Claude a way to verify its own work yields a **2-3x improvement** in output quality — this skill is the mechanism.

## 🎯 Prime Rule — Actual Execution, Not Claimed Execution

> You have NOT verified the code if you have only read it, only type-checked it, or only said "this should work."

You have verified the code when you have:

- **Backend / CLI / library** → run the thing with real inputs and observed real outputs (HTTP response bodies, CLI stdout, log lines, DB rows).
- **Frontend** → loaded the page in a real browser, interacted with it, and read the DOM / console / network.
- **Desktop / native** → opened the app, performed the action, and observed the result.

If you cannot do any of the above (sandbox prohibits it, dependencies missing, etc.), **say so explicitly in the report** — do not pretend verification succeeded.

## 🚫 Hard Boundaries

1. **Do not skip verification** because "the code looks right." That's the failure mode this skill exists to prevent.
2. **Do not mock the thing you are trying to verify.** If the goal is to verify the API, hit the real API. If the goal is to verify the button, click the real button.
3. **Do not change the code during verification.** If a test fails, report it — do not silently patch to make it pass. (The /simplify pass, which runs AFTER a PASS, is where code changes happen.)
4. **Do not run destructive commands** against production databases, live APIs, or the user's real accounts. Use dev/staging/local only. If unsure, ask.
5. **Do not run /simplify if verification FAILED.** Fix first, verify again, then simplify.

## 📋 Workflow

### Step 1 — Identify the Verification Surface

Determine *what kind* of thing was built/changed. Inspect the diff and the project structure to pick exactly one primary surface (you may pick more than one if the change spans layers).

| Signal in recent diff / project | Surface | Tool |
|---|---|---|
| Routes, controllers, handlers, `server.listen`, API endpoints, `app.get/post`, FastAPI/Flask/Express/Nest/Fastify/Rails/Django | **Backend HTTP** | Bash (start server → curl / httpie) |
| CLI entry point, `bin/`, `#!/usr/bin/env ...`, `argparse`, `commander`, `cobra`, `clap` | **CLI** | Bash (invoke with args, read stdout/exit code) |
| Pure library/package (exports but no entry) | **Library** | Bash (run the project's test suite; write a tiny eval script if no tests cover the change) |
| `.tsx` / `.vue` / `.svelte` / React components / Next.js pages / route files under `app/` or `pages/` | **Web frontend** | Claude Chrome MCP (preferred) → Playwright MCP (fallback) — see Step 3d |
| Electron, Tauri, native iOS/Android, native macOS/Windows app | **Desktop / native** | computer-use MCP |
| DB migration, schema change | **Database** | Bash (apply migration to dev DB, run a SELECT to confirm shape) |
| Smart contract | **Blockchain** | Bash (hardhat/foundry test + local-chain deploy) |

If the diff spans multiple surfaces (e.g., backend + frontend for a full-stack feature), verify **each** in turn — you are not done until every surface passes.

### Step 2 — Prepare the Verification Environment

Before running anything:

1. Read `package.json` / `Cargo.toml` / `pyproject.toml` / `go.mod` / `Makefile` / `README` to find the project's declared way to run/test.
2. Check whether a dev server / DB is already running (`lsof -iTCP:<port>`, `ps`, `docker ps`). Reuse if so — do not start a duplicate.
3. Identify the **minimum command set** to prove the change. Do not run the whole test suite if a targeted test exists for the exact change.
4. If `.env.example` exists and `.env` does not, warn the user and stop — verification will fail silently without config.

### Step 3 — Execute Verification (choose based on Step 1)

#### 3a — Backend HTTP

1. Start the server in the background (`Bash` with `run_in_background: true`). Record the background process handle.
2. Poll the health endpoint (or the port) until ready. Do not sleep blindly — poll.
3. Hit the endpoint(s) touched by the diff with realistic payloads (use `curl -s -w '\n%{http_code}\n'`). At minimum: one happy path, one error path (bad input → expect 4xx), one auth path (if auth is involved).
4. Read the response body AND the status code. A 200 with `{"error": ...}` is still a failure.
5. Tail the server logs for stack traces that didn't surface in the response.
6. Stop the background server before exiting (do not leak processes).

#### 3b — CLI

1. Run the command with realistic args. Capture stdout, stderr, exit code.
2. Run with `--help` — does the help text reflect what was actually built?
3. Run the error path (missing required arg, bad value) — does the CLI fail gracefully, not crash?

#### 3c — Library

1. Run the project's test command scoped to the changed module if possible.
2. If there is no test covering the exact change, write a minimal eval script under `/tmp/verify-<timestamp>.<ext>` that imports the library and exercises the new surface. Delete the script after.

#### 3d — Web frontend

**Pick the browser tool by strict priority:**

1. **Claude Chrome MCP** (`mcp__Claude_in_Chrome__*`) — PREFERRED. Drives the user's real browser via the Claude Chromium extension. Check availability via `ToolSearch { query: "Claude_in_Chrome", max_results: 20 }`. If matches return and the extension is connected, use this tier.
2. **Playwright MCP** (`mcp__plugin_playwright_playwright__browser_*`) — FALLBACK only if Tier 1 is unavailable (extension not installed / not connected), or if the verification must be headless and independent of the user's session.

Once a tool is selected, run:

1. Start the dev server (`npm run dev` / `pnpm dev` / framework equivalent) in the background.
2. Navigate to the affected route.
3. Take a snapshot (accessibility tree / DOM) — confirm the changed component renders.
4. Interact with it: click the button that was added, fill the form that was changed, trigger the state that was fixed.
5. Take a screenshot and read the console messages and network log (tool-specific: `browser_console_messages` / `browser_network_requests` in Playwright MCP; Chrome MCP equivalents via its batch tools).
6. If the change is cross-viewport, resize (desktop 1440, mobile 375) and re-check.
7. Flag any console errors, failed network requests, or visual regressions.

**Record which tier was used in the evidence line** (e.g., `[PASS] frontend (chrome-mcp) — /checkout submit — ...`) so the report reflects whether verification ran against a real user session or a headless instance.

#### 3e — Desktop / native

Use computer-use MCP. Request access to the specific app, then drive it end-to-end. Take screenshots as evidence at each step.

#### 3f — Database

Apply the migration on a local/dev DB. Run `\d <table>` / `DESCRIBE <table>` / equivalent to confirm the schema shape. Run a representative query.

### Step 4 — Record Evidence

For every verification step, keep a compact line of evidence. Format:

```
[PASS|FAIL] <surface> — <what was checked> — <concrete evidence>
```

Examples:
- `[PASS] backend — POST /api/login happy path — 200 {"token":"eyJ..."} in 84ms`
- `[FAIL] frontend — /checkout submit — console error: "Cannot read property 'id' of undefined" at line 42`
- `[PASS] cli — mytool --format=json — exit 0, valid JSON on stdout`

Evidence must be **specific**. "Looks good" is not evidence. A status code, a log line, or a screenshot path is evidence.

### Step 5 — Decision Gate

After collecting evidence:

- **All surfaces PASS** → proceed to Step 6 (run /simplify).
- **Any surface FAILS** → stop. Do NOT run /simplify. Report the failure with evidence and the exact reproduction command so the specialist/user can fix it. A failing /go is not an error — it is the skill doing its job.

### Step 6 — Chain Into /simplify

Only reached on PASS. Invoke the `simplify` skill, passing the list of files that were verified as the explicit blast radius (so it does not wander).

`/simplify` will:
- Re-read the diff
- Apply its 8 simplification lenses
- Apply edits and re-run type check / lint / tests
- Return its own mini-report

Compose its report into yours.

### Step 7 — Final Report

Output exactly this shape:

```
🟢 /go verification report
  Surfaces checked : <list>
  Evidence         :
    [PASS|FAIL] <line>
    ...
  Overall verify   : PASS / FAIL
  /simplify        : RAN / SKIPPED (verify failed) / SKIPPED (nothing to simplify)
    Net lines     : -<X>
    Type/Lint/Test: P/P/P
  Next action      : <"ship" | "fix <specific issue>" | "re-run /go">
```

## 🔁 Interaction With /work Workflow

`/go` is **cross-cutting** — it can be appended to any prompt, inside or outside a /work sprint.

- **Inside /work**: run /go as the closing step of a task BEFORE QA sign-off. It does not replace google-qa-engineer's sprint QA — it gives the implementing specialist a fast self-check before handoff.
- **Outside /work**: run /go as a standalone smoke test on whatever was just changed in the working directory.

Either way, /go never spawns agents or modifies project scope. It only verifies and simplifies what already exists.

## ❌ When NOT to Run /go

- **Nothing changed** in the working directory — no diff means no target to verify.
- **User explicitly asked for a plan only** — /go is for executed work, not proposed work.
- **The project is in a half-broken refactor state** where verification requires completing work that was not part of the request. Ask the user first.
- **Destructive side effects required** (prod DB write, real payment, email blast) that cannot be mocked safely. Report that verification is impossible in this surface and suggest a staging environment.

## 🧭 Philosophy — Why This Exists

Anthropic's guidance: *"make sure Claude has a way to verify its work. This has always been a way to 2-3x what you get out of Claude, and with 4.7 it's more important than ever."*

The failure mode without /go:
1. Claude writes code
2. Claude says "Done — the feature works"
3. User comes back 2 hours later, runs it, it doesn't work
4. The whole turnaround loop is lost

The fix is not a smarter model. The fix is a mandatory step where the model actually runs the thing and observes the result before declaring victory. That is this skill.
