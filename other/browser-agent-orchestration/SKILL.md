---
name: browser-agent-orchestration
description: >
  Orchestrates web browser agent tasks with strict token economy: OAuth verification,
  dashboard checks, URL flows, and external console navigation. Use when the user needs
  to verify OAuth callbacks, open URLs in browser, check Mercado Libre/Cloud Run config,
  validate dashboard functionality, or resolve web-flow issues. Structures browser
  tasks as minimal, goal-directed steps to avoid exploratory browsing.
---

# Browser Agent Orchestration

Coordinates with the cursor-ide-browser MCP to perform web verification and flow completion. **Token economy is critical**: each snapshot and interaction costs tokens. Structure tasks as explicit, minimal steps.

## When to Use

| Scenario | Use Browser | Alternative |
|----------|-------------|-------------|
| OAuth redirect verification | Yes — open `/auth/ml/start`, check callback URL in address bar | curl for JSON endpoints |
| Mercado Libre error page | Yes — snapshot to read error text | User screenshots |
| Dashboard UI check | Yes — navigate, snapshot, verify elements | curl for API only |
| Config sync (Cloud Run vars) | No — use gcloud/scripts | — |
| Health/status endpoints | No — use curl | — |

## Token-Economy Rules

1. **One goal per browser session** — Don't chain unrelated navigations.
2. **Snapshot only when needed** — After navigation to verify content; not before every click.
3. **Prefer short waits** — 1–3s with snapshot checks; avoid single long waits.
4. **Lock before interactions** — `browser_lock` after `browser_navigate`; `browser_unlock` when done.
5. **No exploratory browsing** — Have the exact URL or flow before starting.

## Task Structure Template

```
Goal: [Single sentence — e.g. "Verify OAuth callback URL in auth request"]
Steps:
  1. browser_navigate → [exact URL]
  2. browser_snapshot → extract [specific field/element]
  3. [If needed] browser_click/type on [element ref from snapshot]
  4. browser_snapshot → verify [expected outcome]
  5. browser_unlock
```

## Common Flows

### OAuth Start Verification

**Goal:** Confirm Cloud Run uses production redirect_uri, not localhost.

1. `browser_navigate` → `https://SERVICE.run.app/auth/ml/start?mode=json`
2. Parse response (or snapshot body) for `authUrl`
3. Extract `redirect_uri` from authUrl query string
4. **Expected:** `https://SERVICE.run.app/auth/ml/callback` (not localhost)

### Dashboard Functional Check

**Goal:** Verify dashboard loads and key elements render.

1. `browser_navigate` → `http://localhost:3847/viewer/`
2. `browser_snapshot` → get structure
3. Check for nav items, main content area
4. **No deep exploration** — one snapshot suffices for "loads OK"

### Mercado Libre Error Diagnosis

**Goal:** Read error message when ML OAuth fails.

1. `browser_navigate` to user-provided or last-known URL
2. `browser_snapshot` → extract visible error text
3. Map: "Tenemos un problema" = ML outage; "redirect_uri" = config mismatch

## Instructions for the Agent

When delegating to the browser:

1. **State the goal first** — "Verify that /auth/ml/start returns production redirect_uri."
2. **Provide exact URLs** — No placeholders; use real SERVICE.run.app or localhost:PORT.
3. **Specify extraction target** — "Extract the `redirect_uri` value from the authUrl."
4. **Define success/failure** — "Success: redirect_uri contains .run.app. Failure: contains localhost."
5. **Stop when done** — Unlock and report; do not continue browsing.

## Anti-Patterns

- **Don't** open browser for curl-able endpoints (`/health`, `/auth/ml/status`).
- **Don't** take multiple snapshots of the same page without a new action.
- **Don't** navigate without a clear next step.
- **Don't** leave browser locked after completing the task.

## Reference

For browser MCP tool schemas and lock/unlock workflow, see [reference.md](reference.md).
