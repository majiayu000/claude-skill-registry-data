---
name: kimojo-daemon-session-driver
description: Controla sesiones vivas de Kimojo a través del daemon local e IPC. Usa esta skill cuando el usuario quiera iniciar `kimojo serve`, adjuntarse con `kimojo attach`, validar controller/observer ownership, enviar mensajes a una sesión viva, o depurar permisos y attach semantics.
---

# Kimojo Daemon Session Driver

Use this skill when the task is about driving or debugging live Kimojo sessions through the local daemon rather than operating repo-pilot orchestration.

## Use this when

- The user wants to start or inspect `kimojo serve`
- The user wants to attach as controller or observer
- The user wants to validate controller ownership, rehydration, or permission flows
- The user wants to debug daemon token, socket, or attach behavior

## Do not use this as the default for

- Repo readiness or validation contracts
- Tracker dispatch and review-handoff policy
- Kanban or persisted work-state questions

## Primary surfaces

1. `kimojo serve`
2. `kimojo attach`
3. Daemon token and socket files under `.kimojo/`
4. Daemon RPC semantics and controller status

## Default workflow

### 1. Establish the workspace

- Use `--path /path/to/workspace` whenever the target workspace is not the current directory
- Confirm `.kimojo/` exists before trying to start or attach

### 2. Start or inspect the daemon

Preferred commands:

- `kimojo serve --dry-run --path /path/to/workspace`
- `kimojo serve --path /path/to/workspace`
- `kimojo serve --web --path /path/to/workspace` when the user also wants the browser surface

Verify:

- socket path
- token file path
- workspace root
- whether the daemon is already running

### 3. Attach with the correct role

- Use `kimojo attach --path /path/to/workspace` for controller mode
- Use `kimojo attach --observer --path /path/to/workspace <session_id>` for read-only mode
- Use `kimojo attach --who --path /path/to/workspace` when controller ownership is unclear

Respect the single-controller rule. If a controller is already active, do not pretend the new client owns the session.

### 4. Validate session-driving behavior

When the task is interactive:

1. confirm attach succeeded
2. confirm the role is `controller` or `observer`
3. verify the correct session id
4. if permissions are involved, verify the daemon is the authority that resolves them
5. if rehydrating, confirm the session comes back before sending messages

## Guardrails

- If the user asks for explanation only, do not start the daemon or attach; answer directly
- There is at most one controller client at a time
- Observer mode is read-only
- Token and socket are workspace-scoped, not global
- Do not infer daemon truth from browser state alone
- Use the daemon as the source of truth for controller ownership and permission lifecycle

## On-demand references

Set `KIMOJO_REPO` to the local `kimojo-elixir-cli` checkout before opening these references.

- `$KIMOJO_REPO/ai_docs/demo_runbooks/KIMOJO_SERVE_DAEMON_RUNBOOK.md`
- `$KIMOJO_REPO/lib/kimojo/daemon/protocol.ex`
- `$KIMOJO_REPO/lib/kimojo/daemon/server.ex`
- `$KIMOJO_REPO/lib/kimojo/cli/commands/serve.ex`
- `$KIMOJO_REPO/lib/kimojo/cli/commands/attach.ex`

## Output expectations

When reporting results, include:

- workspace path
- daemon status
- chosen role
- session id
- token/socket paths if relevant
- permission or ownership outcome
