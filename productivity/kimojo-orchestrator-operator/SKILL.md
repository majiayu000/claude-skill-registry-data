---
name: kimojo-orchestrator-operator
description: Controla Kimojo Orchestrator/Symphony desde sus superficies canónicas. Usa esta skill cuando el usuario quiera bootstrappear un repo piloto, validar readiness, probar tracker/orchestrator, hacer dry-run o dispatch real, inspeccionar validation/handoff, o demostrar runtime truth en Kimojo.
---

# Kimojo Orchestrator Operator

Use this skill when the task is about operating Kimojo as an orchestration system rather than using Kimojo as a normal coding session UI.

## Use this when

- The user wants to onboard or harden a repo pilot for Orchestrator/Symphony
- The user wants readiness, tracker, dispatch, validation, or review-handoff truth
- The user wants to inspect or prove the runtime control plane
- The user wants to drive Kimojo through its canonical operator surfaces instead of through ad hoc UI clicks

## Do not use this as the default for

- Normal `kimojo` or `kimojo session` coding work
- `/ui/*` feature work that is not about orchestration truth
- `/operate/kanban` work, which is persisted plan state rather than the Symphony runtime

## Control hierarchy

Use the strongest truthful surface available for the task:

1. `mix orchestrator.*` for setup, repo pilot bootstrap, readiness, tracker checks, dry-runs, and diagnostics
2. Daemon IPC (`kimojo serve` + `kimojo attach`) for controller/observer ownership and live session control
3. `/api/orchestrator/*` for machine-readable runtime truth
4. `/operate/orchestrator` for visual runtime proof
5. Browser automation over `/operate/*` only when the user needs screenshots, demos, or visible operator validation

Do not treat `/ui/*` or `/operate/kanban` as the canonical Symphony control plane.

## Default workflow

### 1. Orient to the control surface

- If the user needs repo pilot setup or diagnostics, start with `mix orchestrator.*`
- If the user needs live session control, use daemon IPC semantics
- If the user needs JSON or integration output, prefer `/api/orchestrator/*`
- If the user needs proof screenshots or UX validation, use `kimojo serve --web` and inspect `/operate/orchestrator`

### 1.5. External repo pattern

When the repo being operated is not the Kimojo repo itself, prefer surfaces that take an explicit
workspace path:

- `mix orchestrator.readiness --workspace /path/to/repo`
- `kimojo serve --path /path/to/repo`
- `kimojo attach --path /path/to/repo`

Treat Mix tasks that do not accept `--workspace` as current-workspace tools. Do not assume they
can safely target an arbitrary external repo unless the runtime explicitly supports that mode.

### 2. For repo pilot bootstrap or hardening

Prefer this order:

1. Inspect `.kimojo/config.json` and `.kimojo/WORKFLOW.md` in the target repo if they exist
2. Run `mix orchestrator.readiness --workspace /path/to/repo`
3. If the repo still needs initial seeding, seed `.kimojo/config.json` and `.kimojo/WORKFLOW.md`, or run `mix orchestrator.init` when the active Kimojo workspace supports that bootstrap flow
4. Run tracker checks only when the active workspace is the one whose tracker config is being exercised, or when the command supports an explicit workspace target
5. Use `mix orchestrator.dispatch dry-run` before any live dispatch only when the dispatch surface is targeting the intended workspace

Notes:

- `mix orchestrator.readiness --workspace ...` is the safest explicit repo-pilot check because it separates dispatch readiness from validation readiness
- When a Mix task does not accept `--workspace`, only use it when the current Kimojo workspace is the intended target of the operation
- Never assume validation passed because an agent summary said so; use runner-owned validation truth only

### 3. For live orchestration validation

When the user wants to prove behavior end to end:

1. Confirm readiness first
2. Run the live dispatch or manual tick requested by the user
3. Verify:
   - worktree created
   - tracker comment posted
   - validation reported as `passed`, `failed`, or `unavailable`
   - review handoff reported as `allowed` or `blocked`
4. If visuals are required, use the web surface and capture `/operate/orchestrator`

### 4. For daemon and session control

Use daemon IPC semantics when the task is really about live session ownership:

- Start daemon: `kimojo serve`
- Attach as controller: `kimojo attach`
- Attach read-only: `kimojo attach --observer <session_id>`

Respect controller versus observer ownership. Do not assume a browser tab or a second client can silently take control.

## Guardrails

- If the user asks for explanation, comparison, or planning only, answer directly before running commands
- Keep `dispatch readiness` and `validation readiness` separate
- Distinguish `validation passed`, `validation failed`, and `validation unavailable`
- Never claim review handoff should happen just because the agent completed work
- Use `/operate/orchestrator` as the visual control plane, not `/operate/kanban`
- Use browser automation for proof, not as the primary source of orchestration truth
- If a repo pilot uses machine-readable validation, treat shell-chained validation commands as contract-invalid unless Kimojo explicitly supports them

## On-demand references

Set `KIMOJO_REPO` to the local `kimojo-elixir-cli` checkout before opening these references.

Read these only when needed:

- Surface map:
  `$KIMOJO_REPO/ai_docs/orchestrator/ORCHESTRATOR_SURFACE_MAP.html`
- Operate architecture:
  `$KIMOJO_REPO/ai_docs/OPERATE_PRODUCT_ARCHITECTURE_MAP.md`
- Validation semantics:
  `$KIMOJO_REPO/ai_docs/OPERATE_VALIDATION_RUNBOOK.md`
- Daemon runbook:
  `$KIMOJO_REPO/ai_docs/demo_runbooks/KIMOJO_SERVE_DAEMON_RUNBOOK.md`
- Web runbook:
  `$KIMOJO_REPO/ai_docs/demo_runbooks/KIMOJO_SERVE_WEB_RUNBOOK.md`

## Output expectations

When reporting results, prefer this structure:

- chosen control surface
- readiness state
- action taken
- validation truth
- review handoff outcome
- evidence path or screenshot path if applicable
