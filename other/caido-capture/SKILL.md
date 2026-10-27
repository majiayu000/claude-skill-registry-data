---
name: caido-capture
description: Ensure Caido is running, create per-engagement project, route browser through Caido proxy. Use when starting any live-target session. Idempotent.
---

# caido-capture

## Purpose
All traffic to and from the live target should land in Caido for later
inspection, replay, and IDOR/BAC fuzzing. This skill wires the plumbing.

## Inputs
- `targets/<name>/status.json` (for target name).
- Caido GUI running locally with API enabled
  (Settings → Other → enable API).

## Steps
1. Probe Caido API:
   `caido_health()` via the `caido` MCP. If it errors, halt with
   instructions to open Caido and enable API.
2. Ensure project: `caido_project_ensure(name="<target>-<YYYYMMDD>")`.
   Creates if missing; selects current.
3. Set scope: `caido_scope_set(in=[scope.in...], out=[scope.out...])`.
4. Tell the chrome-devtools MCP to relaunch Chrome with the Caido
   proxy URL (default `http://127.0.0.1:8080`). Practical recipe:
   - Close current Chrome via chrome-devtools `close_page` then start
     a new one with `--proxy-server=http://127.0.0.1:8080` (we
     document this as a launch-flag the user keeps on their Chrome
     profile for bounty work — see `wiki/tools/browser/proxy-setup.md`).
5. Verify capture: navigate to a benign in-scope URL; query
   `caido_recent_requests(count=1)`; assert our request is there.

## Outputs
- Caido project populated as user browses.
- `targets/<name>/caido/project.json` (mirror of project metadata).
- updated `status.json.phases.caido_capture`.

## Failure modes
- Caido API disabled → halt with explicit GUI step list.
- Chrome refuses proxy (cert pinning, HSTS pre-loaded sites) → user
  must install Caido CA into Chrome trust store. Document one-time
  setup in `wiki/tools/caido/cert-trust.md`.
- Scope mismatch (browser tries to navigate out-of-scope) → Caido
  drops the request; we log to `status.json.caido_capture.dropped[]`.

## Result block
```json
"phases": { "caido_capture": { "status": "done", "ts": "<iso>",
  "project": "<target>-<YYYYMMDD>", "proxy_url": "...", "verified": true } }
```
