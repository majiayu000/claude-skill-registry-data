---
name: caido-shift
description: Replicate Caido Shift Agents-style passive proxy passes inside the existing caido-replay/caido-idor flow (T3.6). Stub — wraps micro-agents for open-redirect, IDOR-by-id-rotation, and JS-asset map inside the Caido MCP wrapper at bin/caido-mcp.py. Run when caido-capture has populated the project history.
---

# caido-shift

## Purpose
Caido Shift Agents (the commercial product) ships micro-agents that
auto-classify proxy traffic and surface targeted bug classes. We
replicate three of the highest-yield ones inside the existing
`bin/caido-mcp.py` so they trigger automatically on every captured
request without buying Shift.

## Status
**Stub.** The skill scaffold is in place; the micro-agent
implementations are queued under `bin/caido-mcp.py` extension —
see "Implementation TODO".

## Inputs
- `bin/caido-mcp.py` running with project scoped to current target.
- `caido-capture` populated `caido_history` with ≥1 request.

## Steps (when implemented)
1. For each captured request that matches an in-scope host, dispatch
   to the relevant micro-agent:
   - **open_redirect_agent** — every URL/Location header param;
     enumerates `?next=`, `?redirect=`, `?return_to=`, etc., and
     replays with attacker-controlled value to detect 30x to
     external host.
   - **idor_id_rotation_agent** — every numeric/UUID path segment
     gets rotated to a borrowed ID from the `caido-idor` role
     matrix; flag 200 OK on borrowed IDs.
   - **js_asset_map_agent** — every JS response gets diffed against
     the previous capture for the same asset; new endpoints +
     handlers in the diff feed `js-harvest`.
2. Each finding writes to
   `targets/<name>/findings/shift_<agent>_<request_id>/draft.json`
   with `auto_submit: false, requires_user_review: true`.

## Implementation TODO
- New MCP tools in `bin/caido-mcp.py`:
  - `caido_shift_open_redirect_sweep(scope_id)`
  - `caido_shift_idor_rotation_sweep(scope_id, role_matrix_id)`
  - `caido_shift_js_asset_diff(asset_url)`
- Per-agent regex/tax id list under `bin/shift_agents/<agent>.py`.

## Outputs
- `targets/<name>/findings/shift_<agent>_<request_id>/draft.json`
- `status.json.phases.caido_shift`

## Failure modes
- Caido project not scoped → out-of-scope hosts flagged + skipped.
- Mass IDOR rotation triggers WAF / 429 → respect `caido-replay`
  rate-limit; back off.
- Open-redirect agent on a single-page app with hash-based routing
  → false-positive prone; gate by checking `Location` header is
  present.

## Result block
```json
"phases": { "caido_shift": {
    "status": "stub|done", "ts": "<iso>",
    "agents_run": [...],
    "drafts_written": N } }
```
