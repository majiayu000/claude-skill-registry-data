---
name: sop-generate
description: 'Generate a screenshot-backed business SOP (operating manual) for any deployed internal web app. Trigger phrases: generate business SOP, operating manual, sop-generate, write an operating procedure doc for this system. Distinguish this from a development-process SOP — this skill produces a manual for "how business staff operate this system," not a code/deployment procedure doc.'
argument-hint: "[project path] [deployed URL, optional — inferred from project docs/env if omitted]"
---

# sop-generate — Business SOP Generation

## Overview

Generate a business operating manual for an **already deployed, reachable** web app: who does what at which step, on which page, what the system does automatically, how to handle exceptions — backed by real screenshots and at least one reproducible usage example.

Core division of labor (modeled on Flaex/web-app-tutorial-generator): **scripts only handle screenshots and DOM/accessibility summaries; Claude only reads the summaries and writes the copy**. Never feed a full-page screenshot to the model for copywriting — it saves both tokens and time.

Hard rules (apply throughout; violating any means redoing the work):

1. **Credentials never go into the produced document, and never travel via command-line arguments.** The test account's username/password/token may only appear in your conversation with the user, a local `.env` read, or **environment variables** passed to the fallback script (`SOP_USER`/`SOP_PASS`). `docs/SOP-*.md`, `docs/sop-images/`, and any of their committed artifacts must **never contain real credentials**. When the manual mentions logging in, write "sign in with the test account" rather than an actual value. When calling `<this skill's base directory>/scripts/crawl.mjs`, credentials only travel via environment variables (`SOP_USER=... SOP_PASS=... node ...`), never via `--user`/`--pass` command-line flags — argv lands in shell history, is visible in `ps aux`'s process listing, and in the session transcript; the credentials leak into those places even if the script itself never writes them to a file.
2. **Explain business jargon the first time it appears** (e.g. project-internal terms like "flagged/unflagged").
3. **The page matrix must have full coverage** — every page and every feature you traverse must show up in the matrix; skipping something because "it doesn't look important" is not allowed.
4. **Examples must be walked through for real**, never fabricated — screenshots are the evidence.

## Technical approach

- **Preferred**: `microsoft/playwright-mcp` (Apache-2.0). Check whether it's already configured:
  ```
  claude mcp list | grep -i playwright
  ```
  If configured, use the MCP tools directly for navigation/snapshots/screenshots — no script needed.
- **Fallback**: when MCP isn't configured, use this skill's bundled native Playwright Node script `<this skill's base directory>/scripts/crawl.mjs` (three-stage: login → traverse → screenshot; call it with an absolute path, since the working directory at execution time is the target project's root, and the relative path `scripts/crawl.mjs` won't resolve). First use requires `npm install playwright` or an existing global install; the script self-checks and reports the install command for anything missing — it never installs silently. Credentials travel via environment variables (see Hard Rule 1), e.g.:
  ```
  SOP_USER='<test account>' SOP_PASS='<password>' node <this skill's base directory>/scripts/crawl.mjs --url <deployed URL> --out docs/sop-images
  ```
  **Capability gap**: this script only handles the first-pass static capture — one full-page screenshot plus an accessibility summary per page. It does not do the "before/after the key operation" pair of screenshots required by Step 3 — that needs the script to be aware of a specific click/form-submit action. The script supports an optional `--actions <json file>` parameter that takes an action list (`[{name, url, click}]`, with optional `before`/`after` fields used only as screenshot filename suffixes; the authoritative format is documented in the header comment of scripts/crawl.mjs) to capture a before/after pair for a given operation. Without it, before/after screenshots of key operations must be captured manually via MCP, or via a one-off Playwright snippet — `full.png` alone is not sufficient.
- **Anti-detection browsers** (browser-use/camoufox, etc.) were ruled out in the 2026-08-03 research pass: for deterministic traversal of an internal/already-authorized system, they're a net negative — not adopted.
- **Token-saving design** (borrowed from westpoint-io/mimik): each page produces two artifacts —
  - an accessibility snapshot or a trimmed DOM summary (interactive elements' role/name/position) → fed to Claude to write the operating instructions;
  - a screenshot file → stored on disk only, referenced by path with `![]()` in the final SOP — the full image is **never** uploaded to the model for copywriting.

## Five-step process

### 1. Input gathering

- Project root: read `HANDOVER.md` (if a handover doc bundle already produced one), `BUSINESS.md`, `REQUIREMENTS.md`, and extract the business processes and role list (who, at which step). If these docs don't exist, ask the user for business background.
- Deployed URL: prefer pulling it from `HANDOVER.md`/`DEPLOYMENT.md`, or `APP_URL`/`BASE_URL`-style variables in `.env`; ask the user if it can't be found.
- Test account: prefer reading it from the project's `.env` (locally, never forwarded elsewhere); if unavailable, ask the user for a dedicated test account and confirm with them "this is not a real business account." **Read it and use it immediately — never echo it into any written document**; when going through the fallback script, pass it via the `SOP_USER`/`SOP_PASS` environment variables, not command-line arguments (see Hard Rule 1).

### 2. Page inventory

- After logging in with the test account, enumerate every page from the navigation structure (top bar/sidebar menu, route table if readable).
- Cross-reference against the feature list distilled in Step 1 to produce a "page × feature" matrix (list it in a draft first; check it for full coverage at acceptance time).

### 3. Traverse and screenshot

- **Suggested pre-step**: if the `ui-sweep` plugin is installed, run a full-site interaction sweep first (systematically clicking every interactive element per screen) before the batch of screenshots — it surfaces interaction bugs early, so you don't unknowingly document a broken UI state. If it's not installed, skip this step; the rest of the process is unaffected.
- Screenshot each page/feature in turn, storing to `docs/sop-images/<page-slug>/` (use the page's route name for the slug — stick to ASCII; non-ASCII filenames get mangled by some tools).
- **Key operations** (form submissions, report exports, triggering batch jobs — anything with a side effect or a state change) get **before/after** screenshot pairs, filenames suffixed `-before` / `-after`.
- Alongside each screenshot, jot down one sentence summarizing the accessibility summary's key points for that page/state (used in Step 4 for copywriting — no need to keep the full summary verbatim).
- **Close when done**: once the screenshots are taken, close the agent-browser session used for them and any app process you started for the shots; close only what you started yourself, never processes that were already running.

### 4. Write it up

Produce `docs/SOP-<business-name>.md`, **organized by business process order, not page order** — the same business step may span multiple pages, and those should be merged into one section. Each business step includes:

- **Who** (role)
- **On which page** (link/route + screenshot)
- **What operation** (with screenshots, broken into steps)
- **What the system does automatically** (so readers don't think they need to manually do something that's actually automatic)
- **How to handle exceptions** (common errors, edge cases, who to escalate to)
- Every SOP needs **at least one real usage example** — a record of walking through the full business process with test data, with screenshots, proving the manual is reproducible

If an older SOP already exists (e.g. a project's "SOP - Full Reporting-System Workflow"), calibrate against it: the old version usually lacks **page screenshots** and **usage examples** — these two gaps must be filled in the new version. Other content (conventions, jargon glossary) can be referenced from the old version but must be reorganized into the new structure, not simply pasted in.

### 5. Acceptance self-check

After producing the document, self-check every item below; go back to the corresponding step for anything that fails:

- [ ] Page matrix has full coverage (every item in Step 2's matrix has a corresponding section in the body)
- [ ] Every feature has at least one screenshot; key operations have a before/after pair
- [ ] At least one usage example, and its steps are reproducible (walk through it yourself following the doc and get a consistent result)
- [ ] A full-text search confirms no real credentials remain (username/password/token/API key)
- [ ] Business jargon is explained the first time it appears
- [ ] UTF-8, no mangled characters

## Degraded delivery when the network is unreachable

If the target deployed URL is unreachable from the current environment (e.g. it needs Tailscale/an internal network, and the current session can't reach it):

1. Don't produce the SOP body — instead produce an **executable runbook**: `docs/SOP-<business-name>-runbook.md`, **filled in according to `<this skill's base directory>/references/runbook-template.md`** — content is "once the network is back, run this script/these steps to auto-generate the SOP draft," including the business-process skeleton already gathered (roles/steps/page list, whatever could be pulled from docs ahead of time) plus the pending traverse-and-screenshot commands. Don't hand-roll a different structure from scratch — that drifts from the template.
2. Clearly tell the user this is pending work, and list the trigger condition (e.g. "once Tailscale is connected, rerun `<this skill's base directory>/scripts/crawl.mjs`").
3. Don't fabricate screenshots or invent a page structure just to deliver something.

## Pilot strategy

On first use, prefer piloting on a **project that already has an old-style manual** — use the old version to calibrate the new version's level of detail and jargon-explanation granularity, then roll it out to projects without an old reference. If calibration surfaces a conflict between old and new conventions (e.g. some number/rule in the old version is stale), defer to the project's current documentation (`HANDOVER.md`/`DECISIONS.md`/the current state of the code) — the SOP should not carry forward the old version's stale claims.

## Common mistakes

| Mistake | Fix |
|---|---|
| Feeding a full-page screenshot to the model for copywriting | Only pass the accessibility/DOM summary; screenshots are stored and referenced, never uploaded |
| Organizing the SOP by page order ("here's what's on the homepage, here's what's on the reports page") | Must be organized by business-process order — when one step spans multiple pages, merge them into one section |
| Writing the test account's password into the SOP "for filling in later" | Never write it into any produced document — it only ever appears in the conversation or the local .env |
| Skipping the whole thing and producing nothing when the network is down | Produce a degraded runbook instead — pre-build the skeleton from whatever docs already exist |
| Using jargon (like "flagged") without explaining it | Explain it in one sentence the first time it appears |
| Only capturing "happy path" screenshots, no exception screenshots | Key operations need before/after pairs; exception handling needs at least a written explanation, screenshots are a bonus |
| An old SOP exists, so just copy it and reformat | The old version is only for calibrating detail/terminology granularity — screenshots and examples must be redone |
| Passing the password to crawl.mjs via `--user`/`--pass` for convenience | Use the `SOP_USER`/`SOP_PASS` environment variables instead — argv lands in shell history and `ps aux` even if the script never writes it to disk |
| Clicking "log out" while traversing navigation links | The script already filters by keyword/same-origin/protocol; if you hand-write traversal code yourself, do the same, or the session gets invalidated and every screenshot afterward is just the login page |
| Screenshotting a hash-routed SPA relying only on `domcontentloaded`/`networkidle` | Client-side route transitions don't fire native browser navigation events, so these two events pass almost instantly, while the page's data is fetched asynchronously by the frontend only after the route switches. In practice, every hash-internal navigation screenshot after the first real full-page load catches a "loading…" half-finished state. crawl.mjs already appends `waitForAppReady` (polling until "loading"-style copy disappears) after every `goto` as a backstop — do the same if you hand-write traversal code; don't rely on `networkidle` alone |
| Ignoring the login page (a standalone route like `/login`) in the matrix | By design, the traversal script won't walk the login page while already authenticated (it would just capture the "already logged in, auto-redirected" fake page) — the login page needs a separate screenshot taken with a fresh, cookie-less context, and must cover the failed-login/error state too, not just a sentence like "log in with an account" |
