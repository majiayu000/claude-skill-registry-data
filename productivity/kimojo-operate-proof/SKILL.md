---
name: kimojo-operate-proof
description: Prueba y demuestra la superficie visual de Kimojo Orchestrator. Usa esta skill cuando el usuario quiera validar `/operate/orchestrator`, sacar screenshots, hacer smoke tests del web control plane, o comprobar que la UI visible coincide con runtime truth.
---

# Kimojo Operate Proof

Use this skill when the task is about visible proof of the Kimojo orchestration surfaces rather than low-level control.

## Use this when

- The user wants screenshots or visible evidence from `/operate/orchestrator`
- The user wants a web smoke test for `kimojo serve --web`
- The user wants to validate auth, token flow, assets, or UI/runtime consistency
- The user wants browser automation over the Operate control plane

## Do not use this as the default for

- Repo bootstrap or readiness as the primary source of truth
- Daemon controller ownership questions
- Kanban product work unrelated to orchestrator runtime

## Primary surfaces

1. `kimojo serve --web`
2. `/auth`
3. `/operate/orchestrator`
4. `/api/orchestrator/*`

## Default workflow

### 1. Start the web surface

- Prefer `kimojo serve --web --path /path/to/workspace`
- Use `--open` only when the user wants an interactive browser opened automatically
- If the repo is external, always pass `--path`

### 2. Authenticate correctly

- Read the token from `.kimojo/daemon.token`
- Enter through `/auth`
- Confirm the browser session is attached to the intended workspace

### 3. Validate the control plane

Prefer this order:

1. confirm `/operate/orchestrator` loads
2. confirm the key runtime sections render
3. if needed, cross-check `/api/orchestrator/status`
4. only then capture screenshots or demo evidence

### 4. Interpret proof carefully

- A pretty screen is not enough; the point is that visible state matches runtime truth
- If assets fail to load, treat that as a Kimojo web/runtime issue, not as repo-pilot truth
- `/operate/kanban` and `/ui/*` are adjacent surfaces, not the canonical Symphony control plane

## Guardrails

- If the user asks for explanation or comparison only, do not launch the web surface; answer directly
- Use `/operate/orchestrator` as the main proof surface
- Cross-check API/runtime truth when the UI is ambiguous
- Distinguish UI rendering bugs from orchestration bugs
- Do not claim validation passed just because the UI looks healthy
- Prefer browser automation only when the user wants visible evidence or reproducible web smoke coverage

## On-demand references

Set `KIMOJO_REPO` to the local `kimojo-elixir-cli` checkout before opening these references.

- `$KIMOJO_REPO/ai_docs/demo_runbooks/KIMOJO_SERVE_WEB_RUNBOOK.md`
- `$KIMOJO_REPO/ai_docs/orchestrator/ORCHESTRATOR_SURFACE_MAP.html`
- `$KIMOJO_REPO/ai_docs/OPERATE_PRODUCT_ARCHITECTURE_MAP.md`
- `$KIMOJO_REPO/lib/kimojo_web/api/orchestrator_controller.ex`
- `$KIMOJO_REPO/lib/kimojo_web/live/orchestrator_live/components.ex`

## Output expectations

When reporting results, include:

- workspace path
- served URL
- proof surface used
- runtime/API cross-check result
- screenshot or artifact path when applicable
- any UI/runtime mismatch found
