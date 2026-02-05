---
name: agent-browser-prd-playbooks
description: Generates agent-browser command playbooks for each Daedalus PRD user story (enrich, extract, observe, scout, agent, billing) to guide UI walkthroughs and evidence capture.
---

# Agent-Browser PRD Playbooks

Use this skill to draft ready-to-run `agent-browser` command blocks for every Daedalus PRD user story in `prd.json` (US-001..US-007). It does **not** run the browser; it outputs scripts to execute manually.

## Prerequisites

1. `agent-browser --version` succeeds; if missing: `npm install -g agent-browser`
2. Chromium downloaded: `agent-browser install` (Linux: `agent-browser install --with-deps`)
3. App base URL known (e.g., `http://localhost:3000` or deployed URL)
4. Auth: choose one
   - Header-based: `--headers '{"Authorization":"Bearer <token>"}'`
   - Saved state: log in once then `agent-browser state save auth.json`; reuse with `state load auth.json`
5. Keep refs-first flow: always run `snapshot -i` before interacting; re-snapshot after navigation.

## Inputs

- `prdPath`: path to PRD JSON (default `prd.json` at repo root)
- `baseUrl`: app URL
- `authHeaders` or `authStatePath`: for authenticated areas
- Optional: feature flags or tenant identifiers per story

## Steps

1. Read `prdPath` and list `userStories` ids/titles.
2. For each story, set a dedicated session `--session <id>` to isolate cookies.
3. Login (if needed) once per session; then `state save` for reuse.
4. Build a refs-first command block: `open → snapshot -i → interactions → wait → verify (url/title/text) → screenshot --full`.
5. Prefer semantics (`find role/text/label`) when refs are unstable; avoid destructive actions (billing changes) unless explicitly approved.
6. Capture evidence: final URL, title, key text via `get text @eN`, and `screenshot --full <id>.png`.

## Command Playbooks per PRD Story

> Replace `<BASE_URL>` with your target, provide real selectors/refs from the latest `snapshot -i`, and fill any placeholders like `<CSV_PATH>`.

### US-001 – Enrich a CSV of leads (enrich batch)
```bash
agent-browser --session US-001 open <BASE_URL>/enrich/batch
agent-browser snapshot -i
# TODO: click upload control
agent-browser find role button click --name "Upload" || agent-browser click @e?
agent-browser snapshot -i
agent-browser fill @e? "<CSV_PATH>"  # if file picker not allowed, attach via UI flow manually
agent-browser snapshot -i
agent-browser click @e?  # Submit/process
agent-browser wait --text "Enrichment complete" || agent-browser wait --text "Processing"
agent-browser get url
agent-browser get title
agent-browser get text @e?  # Verify row count or success message
agent-browser screenshot --full US-001.png
```

### US-002 – Enrich a single lead (enrich single)
```bash
agent-browser --session US-002 open <BASE_URL>/enrich
agent-browser snapshot -i
agent-browser find label "Email" fill "demo@example.com" || agent-browser fill @e? "demo@example.com"
agent-browser find label "Name" fill "Demo User" || true
agent-browser find role button click --name "Enrich" || agent-browser click @e?
agent-browser wait --text "Enrichment complete" || agent-browser wait --text "Profile"
agent-browser get url
agent-browser get title
agent-browser get text @e?  # Verify role/company output
agent-browser screenshot --full US-002.png
```

### US-003 – Extract brand identity from a URL (extract)
```bash
agent-browser --session US-003 open <BASE_URL>/extract
agent-browser snapshot -i
agent-browser find label "Website" fill "https://example.com" || agent-browser fill @e? "https://example.com"
agent-browser find role button click --name "Extract" || agent-browser click @e?
agent-browser wait --text "Colors" || agent-browser wait --text "Fonts"
agent-browser get url
agent-browser get title
agent-browser get text @e?  # Verify brand attributes present
agent-browser screenshot --full US-003.png
```

### US-004 – Monitor critical pages for changes (observe)
```bash
agent-browser --session US-004 open <BASE_URL>/observe
agent-browser snapshot -i
agent-browser find label "URL" fill "https://example.com/pricing" || agent-browser fill @e? "https://example.com/pricing"
agent-browser find label "Frequency" fill "daily" || agent-browser select @e? "Daily"
agent-browser find role button click --name "Create monitor" || agent-browser click @e?
agent-browser wait --text "Monitor created" || agent-browser wait --text "Next run"
agent-browser get url
agent-browser get title
agent-browser get text @e?  # Verify monitor row appears
agent-browser screenshot --full US-004.png
```

### US-005 – Run scouts to discover new signals (scout)
```bash
agent-browser --session US-005 open <BASE_URL>/scout
agent-browser snapshot -i
agent-browser find label "Query" fill "site:news.ycombinator.com fintech" || agent-browser fill @e? "site:news.ycombinator.com fintech"
agent-browser find role button click --name "Run scout" || agent-browser click @e?
agent-browser wait --text "Results" || agent-browser wait --text "New findings"
agent-browser get url
agent-browser get title
agent-browser get text @e?  # Verify deduped results listed
agent-browser screenshot --full US-005.png
```

### US-006 – Run research sessions with agents (agent)
```bash
agent-browser --session US-006 open <BASE_URL>/agent
agent-browser snapshot -i
agent-browser find label "Prompt" fill "Summarize competitor positioning for Acme" || agent-browser fill @e? "Summarize competitor positioning for Acme"
agent-browser find role button click --name "Run" || agent-browser click @e?
agent-browser wait --text "Thinking" || agent-browser wait --text "Sources"
agent-browser get url
agent-browser get title
agent-browser get text @e?  # Verify answer section populated
agent-browser screenshot --full US-006.png
```

### US-007 – Manage plans, usage, and billing (platform/billing)
```bash
agent-browser --session US-007 open <BASE_URL>/billing
agent-browser snapshot -i
# Read-only unless explicitly approved; avoid purchasing/upgrading without consent
agent-browser get text @e?  # Current plan/limits
agent-browser screenshot --full US-007.png
```

## Session & Resilience

- Use `--session <id>` per story to keep cookies separate.
- After login in a session: `agent-browser state save auth-<id>.json`; preload with `state load auth-<id>.json`.
- On failure/timeouts: rerun `snapshot -i`, use `wait --text` or `wait --url`, then retry the action.
- If MFA/CAPTCHA blocks progress, stop and request human input.

## Outputs

- Per-story command block (above) tailored with real refs/selectors.
- Evidence per story: final URL, title, key text assertion, and screenshot path `<id>.png`.

## Verification

- Validate command syntax (no missing args; refs exist from latest snapshot).
- Confirm non-destructive intent (especially billing); abort upgrades/changes unless explicitly approved.
- Ensure auth method is scoped (headers per origin or session state file).
- Re-snapshot after each navigation before using `@e?` refs.
