---
name: aiwf-ui-electrician
description: "Use when debugging the contract between backend APIs or model runtimes and visible UI state: FastAPI routes, Gradio callbacks, React or Vue clients, fetch, SSE, WebSockets, polling, request and response normalization, progress, cancellation, errors, telemetry, settings bootstrap, files, and output links."
---

# AIWF UI Electrician

## Core Rule

Trace one user action end to end. Compare the backend contract, transport, client parsing, state transition, rendered state, logs, and terminal cleanup before changing either side.

## Workflow

1. Read project guidance and identify the failing action, expected UI state, backend route or callback, transport, and current logs.
2. Create a debug-pass folder when the investigation spans independent lanes:

```powershell
python <this-skill>\scripts\scaffold_debug_pass.py --root <project-root> --slug <short-slug>
```

3. Read `references/middle-layer-checklist.md`. Read `references/debug-pass-protocol.md` before using subagents.
4. Capture the contract on both sides: request fields, defaults, enum values, response and error shapes, stream events, terminal states, file paths, and cache behavior.
5. Reproduce with the smallest endpoint, callback, or browser flow. Determine whether the fault is backend, transport, client normalization, stale cache, state ownership, or rendering.
6. Patch the owning layer and update generated/shared types or tests when the contract changes.
7. Verify API behavior, client build/tests, visible loading/error/empty states, cancellation, and cleanup.

## Lanes

- Request and response shape, aliases, defaults, status codes, and generated types.
- Job progress, streaming events, polling freshness, terminal state, and stale event cleanup.
- Cancellation, duplicate submit prevention, concurrency ownership, and failure recovery.
- Error propagation from backend logs to useful user-visible states.
- Runtime telemetry and settings/bootstrap synchronization.
- Upload, static, output, thumbnail, and download paths.
- Cache and proxy behavior for volatile endpoints.

## Guardrails

- Do not hide backend failures behind optimistic UI state or console-only errors.
- Do not duplicate request types when the repo has generated or shared contracts.
- Preserve auth, origin, and tenant boundaries while debugging.
- Keep subagents read-only issue reporters unless Shawn explicitly assigns write ownership.
- Add the focused FastAPI, Gradio, React, Vue/VitePress, TypeScript, JavaScript, or CSS skill for code in that layer.
- Avoid GPU-heavy generation when a mocked job, tiny prompt, fixture, or route probe can prove the connector.

## Output

Report the action traced, contract mismatch or root cause, files changed, endpoint and UI checks, visible states verified, and residual risk.
