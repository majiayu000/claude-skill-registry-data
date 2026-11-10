---
name: local-runtime-port-isolation
description: Use whenever the user wants to run, debug, test, or start a local web service or other developer runtime and there is any chance multiple agents, worktrees, or local environments may be active at the same time. This skill prevents host-port collisions before startup by identifying the repository's real execution entry point, preferring repo-native port configuration when available, falling back to temporary overrides when necessary, and avoiding unnecessary interference when the runtime already auto-selects a free port. Also use it when the user mentions `docker compose`, dev servers, `npm run dev`, `uvicorn`, published ports, parallel development, coding agents, worktrees, local stacks, or startup failures caused by `address already in use`.
---

# Local Runtime Port Isolation

Use this workflow before starting a local runtime in a parallel development environment.

## Why this exists

Parallel coding agents often collide on host ports even when the repository itself is healthy. Some runtimes also have name-level collisions such as shared `docker compose` project names, explicit `container_name` values, or fixed state directories. This skill makes startup safer by isolating host ports before launch and by checking runtime-specific collision risks instead of assuming every project behaves like a single-process dev server.

## Inputs

- The repository task, such as starting the app, launching the stack, running tests, opening a debugger, or bringing up an E2E environment.
- The runtime entry point if the user provided one, otherwise infer it from repo docs and files.

## When Not to Use

- The task is not about starting or debugging a local runtime.
- The task is only to explain the compose setup, not to run anything.
- The runtime already auto-selects a free port and reports the resolved URL clearly, and there are no adjacent collision risks that still need handling.

## Workflow

1. Read the repository docs first. Prefer the documented startup path over inventing one.
2. Determine the actual runtime entry point before changing anything. Check files such as `compose.yaml`, `docker-compose.yml`, `.env`, example env files, helper scripts, `Makefile`, `justfile`, `Taskfile.yml`, `package.json`, language-specific manifests, and CI workflows.
3. Classify the runtime:
   - `docker compose` or similar multi-service container stack
   - single-process dev server such as `npm run dev`, `pnpm dev`, `uvicorn`, `rails s`, `next dev`, `vite`, `storybook`, or a framework wrapper
   - auto-port-aware runtime that already chooses a free port when the default is busy
4. Identify which host ports matter for the task:
   - HTTP application ports
   - API ports
   - debugger ports
   - admin UIs or test harness ports
   Ignore internal-only ports that are not bound on the host.
5. Check whether the repository already supports port overrides through CLI flags, env vars, or repo-specific wrapper scripts. If it does, prefer that path.
6. Avoid mutating shared repo state when parallel agents are involved. Do not casually rewrite committed runtime config files or a shared `.env` file just to change ports.
7. Detect blockers before startup:
   - Find currently bound TCP ports on the host.
   - Detect runtime-specific name collisions such as compose project names, explicit `container_name` values, or fixed resource names.
   - Detect fixed host paths or other assumptions that may break parallel runs.
8. Allocate replacement host ports for each fixed external port that could collide. Prefer stable, explicit free ports over ad-hoc guessing so the user can still open the app, attach debuggers, and run tests predictably.
9. Apply ports using the least invasive compatible method:
   - First choice: use repo-native CLI flags, env vars, or temporary env files.
   - Second choice: for compose or other generated config flows, create a temporary override file and layer it in.
   - Last resort: if neither path is safe and the repo requires direct edits, stop and ask before changing committed files.
10. Validate the resolved runtime configuration before startup. For `docker compose`, use `docker compose config`. For single-process servers, confirm the final command line or env assignment reflects the chosen ports.
11. Start the runtime with any needed isolation primitives, such as a unique compose project name for `docker compose`.
12. Report the final connection details clearly: runtime entry point, chosen host-port mapping, any temporary files created, any remaining collision risks, and the cleanup command.

## Preferred Isolation Strategy

Use this order unless the repo docs say otherwise:

1. Repo-native CLI flags or env overrides
2. Temporary env file or override file
3. Direct config edits only with user approval

This keeps the workflow aligned with the repository when possible while still handling repos that never parameterized their ports.

## Port Allocation Guidelines

- Allocate one host port per externally reachable port binding that can conflict.
- Keep a small mapping table so each service port remains understandable, for example `web 3000->43127`, `api 8080->43128`, `debug 9229->43129`.
- If a service publishes both HTTP and debugger ports, reassign both.
- If later steps need to know the port number, do not rely on opaque automatic assignment; choose explicit free ports and print them.
- Prefer checking actual listeners on the host instead of assuming common ports are free.
- Reuse the repository's original internal or container-side port unless there is a repo-specific reason to change it.

## Runtime-Specific Branches

### `docker compose`

- Identify published host ports from `ports:`. Ignore `expose` for collision purposes because it does not bind host ports.
- If the repo already supports env-based port overrides such as `${WEB_PORT:-3000}`, use that first.
- Otherwise, create a temporary override file instead of editing the main compose file.
- Choose a unique compose project name for the current run. Use `docker compose -p <name>` or `COMPOSE_PROJECT_NAME=<name>` so container, network, and volume names do not collide across agents or worktrees.
- Detect explicit `container_name` values, because those can still collide even with a unique compose project name.

### Single-process dev servers

- Prefer runtime-native flags or env vars such as `--port`, `-p`, `PORT=...`, framework-specific debug-port flags, or wrapper-script env passthrough.
- Keep the repo's documented launch command intact apart from the minimum port changes needed for isolation.
- If the script hard-codes a port internally and offers no flag or env override, inspect the wrapper script before deciding whether a temporary config file is possible. If not, ask before editing committed files.

### Auto-port-aware runtimes

- If the runtime already chooses a free port automatically and surfaces the resolved URL clearly, do not override just because you can.
- Still check for adjacent risks such as separate debugger ports, companion services, or fixed state directories that can collide.
- Report the resolved URL or port once the runtime starts so the user knows where to connect.

## Compose Override Guidance

When env-based port overrides are unavailable, create a temporary override file instead of editing the main compose file.

Good default location:

```text
.codex/docker-compose/<agent-or-worktree>/compose.override.yml
```

Guidelines:

- Only override the fields needed for isolation, usually `ports:` and occasionally `container_name`.
- Keep the base compose file untouched.
- If the repo already uses one or more override files, append yours rather than replacing them.
- Remove the temporary override when the run is over unless the user wants it kept for reuse.

## Temporary Env Guidance

If the repo already parameterizes ports with env vars, prefer a temporary env file or inline env assignment over modifying the shared `.env`.

Good examples:

```bash
WEB_PORT=43127 API_PORT=43128 docker compose -p myproj up -d
```

```bash
docker compose --env-file .codex/docker-compose/agent-1/run.env -p myproj up -d
```

Avoid this unless the user explicitly wants it:

```bash
sed -i ... .env
```

Shared `.env` edits are easy to race when multiple agents are active in the same repository.

## Validation Checklist

Before startup, verify these points:

- The resolved command or config shows the intended host ports.
- Any runtime-specific isolation primitive is set, such as a unique compose project name.
- No hard-coded names such as `container_name` will still collide.
- The user-facing endpoints and debugger ports are recorded.

If any of these checks fail, fix them before startup instead of hoping the stack will sort itself out.

## Output

- The chosen startup command and why it was selected.
- The runtime entry point and any isolation primitive used, such as a compose project name.
- The final host-port mapping for each published or externally reachable service port.
- The temporary env file or override file path, if one was created.
- Any remaining parallel-run risks such as hard-coded names or non-port resource collisions.

## Example Situations

**Example 1: Repo already supports env-based compose ports**

The compose file uses `${WEB_PORT:-3000}` and `${API_PORT:-8080}`. Pick free ports, write them to a temporary env file, run `docker compose config`, then start with a unique `-p` value.

**Example 2: Repo hard-codes compose ports**

The compose file publishes `3000:3000` and `5432:5432` with no env vars. Generate a temporary override file that changes only the host side of those bindings, validate it, then run `docker compose -f compose.yaml -f <temp-override> -p <name> up`.

**Example 3: Single-process dev server**

The documented command is `pnpm dev` and the underlying framework accepts `--port` or `PORT=...`. Keep the normal script, add only the minimum override needed for the HTTP port and any debugger port, then report the final URL.

**Example 4: Port isolation is not enough**

The compose file hard-codes `container_name: app`. Surface that risk before startup because `-p` does not rename explicit `container_name` values.

**Example 5: Runtime already handles it**

The runtime already picks the next free port automatically and prints the resolved URL. Do not build extra override machinery unless another fixed port, debugger, or companion service still needs isolation.
