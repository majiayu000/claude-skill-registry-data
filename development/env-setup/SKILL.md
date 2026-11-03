---
name: env-setup
description: >-
  Explain, inspect, configure, and troubleshoot Cloud Agent development
  environments. Use when the user asks about environment setup,
  changing/improving the environment, or triggering/testing a build.
environments:
  - cloud
metadata:
  environments:
    - cloud
---
# Cloud Agent Environment Setup

Use this skill to teach users how Cloud Agent environments work and, when requested, to inspect or improve the current repository's setup. Match the response to the request: explain a concept, audit configuration, make a focused patch, or troubleshoot a failed setup.

## Resources

| Workflow | Reference |
| --- | --- |
| Create or fully set up an environment (snapshot, build-test when available, propose) | [Set up a new environment](references/create-environment.md) |
| Update a repository-managed environment | [Update a repository-managed environment](references/update-repo-managed-environment.md) |
| Update a DB-managed environment | [Update a DB-managed environment](references/update-db-managed-environment.md) |
| Migrate an existing environment to builds | [Migrate an environment to builds](references/migrate-to-builds.md) |

## Mental Model

A Cloud Agent starts in an isolated remote machine. Its environment has two layers:

1. **Base environment**: a saved snapshot, Dockerfile-built image, explicit image, or Cursor's default image supplies the operating system, system packages, and toolchains.
2. **Repository bootstrap**: after Cursor checks out the selected repository revision, `install` refreshes project dependencies and generated state. `start` and `terminals` then start services needed while the agent works.

Put slow, stable system dependencies in the Dockerfile. Put repository-dependent work in `install`, where it can see the checked-out source. Keep `install` idempotent because it can run repeatedly and against cached or partially prepared state.

With environment builds, `install` creates the baseline snapshot and is not rerun when a new pod boots from that build. Per-pod initialization therefore belongs in `start` or `terminals`. Without a build, setup may run `install` while preparing the agent.

Environment changes normally affect newly started agents. Do not imply that editing configuration rebuilds or migrates an already-running agent.

## Configuration Sources and Precedence

Cursor resolves environment configuration in this order:

1. `.cursor/environment.json` from the repository revision used to start the agent.
2. A personal saved environment for the repository.
3. A team saved environment for the repository.

The first available source wins. A committed `.cursor/environment.json` therefore overrides dashboard-managed personal and team environments. Before proposing a change, determine which source the current agent actually used. Prefer the Cloud Agent environment-info tool when available; otherwise inspect the repository and explain what cannot be confirmed.

Repository-defined environments are versioned with code and are best when the setup should follow branches and pull requests. Dashboard-managed environments are useful for interactive setup, secrets, and reusable saved snapshots without committing configuration to the repository.

## Common environment.json Fields

Use the current public schema instead of relying on a memorized exhaustive field list:

- Schema: https://cursor.com/schemas/environment.schema.json
- Setup guide: https://cursor.com/docs/cloud-agent/setup
- Environment settings: https://cursor.com/docs/cloud-agent/settings

Use the schema for validation, but do not add a `$schema` property to `.cursor/environment.json`; the current schema rejects undeclared fields.

Common fields:

| Field | Purpose |
| --- | --- |
| `name` | Human-readable environment name. |
| `user` | User that runs commands in the environment. It must exist in the image. |
| `build.dockerfile` | Dockerfile path, relative to the directory containing `environment.json`. |
| `build.dockerfileContents` | Inline Dockerfile used by supported dashboard-managed flows. Prefer a repository file for repo-managed environments. |
| `build.context` | Docker build context, also relative to that directory. It defaults to `.cursor`. |
| `image` | Explicit container image reference. |
| `snapshot` | Saved base-environment snapshot ID. |
| `install` | Idempotent repository bootstrap/update command run after source is available. |
| `start` | Command run when the environment starts; failure prevents a successful start. |
| `terminals` | Named persistent processes presented to the agent and run in tmux-backed terminals. |
| `ports` | Container ports to expose. |
| `repositoryDependencies` | Additional repositories that must be in the generated GitHub token's access scope. |
| `agentCanUpdateSnapshot` | Whether the agent may update a snapshot-backed environment. |
| `chromeExecutablePath` | Browser executable to use for computer-use flows. |
| `egressMode` and `egressAllowlist` | Network-policy inputs. Treat dashboard network settings and inherited policy as part of the effective result. |
| `mcpServerAllowlist` | MCP server URL or command entries permitted by the environment policy. |

Choose one base-image strategy: Dockerfile build, explicit image, or snapshot. Do not combine them and rely on implementation precedence. Check the live schema before adding less-common fields because product behavior can evolve faster than this skill.

## Search Current Documentation

When setup involves a third-party service, hosted platform, or a stack you are not deeply familiar with, look up the provider's current official documentation with web search and fetch tools when available instead of relying on memorized knowledge. Install methods, CLI names, package versions, local-development workflows, and auth flows change faster than any memorized snapshot:

- Supabase: check the current `supabase` CLI install method and local-stack (`supabase start`) requirements before writing install or start commands.
- Firebase, Stripe, and similar hosted services: confirm the current CLI, emulator, or local-proxy story rather than assuming one exists.

Prefer official provider documentation over secondhand sources. If web search or network access is unavailable in the current egress mode, say so, rely on what the repository itself pins (lockfiles, tool-version files, setup scripts), and avoid inventing provider-specific commands.

## Choosing install, start, or terminals

Classify each setup action by the lifetime of the state it creates:

| Location | Use it for | Expected behavior |
| --- | --- | --- |
| `install` | Durable repository setup tied to checked-out source: package installation, compilation, code generation, and local configuration that can be recreated. | Runs after source is available and may run again after changes or against cached state. It must be idempotent, non-interactive, and terminate successfully. No process started here should be expected to survive into a later boot. |
| `start` | Per-boot runtime initialization: starting system daemons, restoring ephemeral service state, or launching a supervised/background service required whenever the machine starts. | Runs every time the environment starts. It must tolerate restarts, avoid duplicate processes, and reach a clear success or failure state. |
| `terminals` | Long-running foreground processes the agent should see, inspect, restart, or read logs from: development servers, watchers, and workers. | Runs as named tmux-backed processes after startup. Commands may remain active for the lifetime of the environment. |

A development server does not belong in `install`: cached setup or a snapshot may preserve its files but not its process, and a foreground server can prevent installation from completing. Put it in `terminals` when the agent benefits from visible logs and direct restarts. Use `start` when a startup script launches or reconciles the service under a process manager, confirms readiness, and then returns.

Keep dependency installation and source-derived generation out of `start`. Running them on every boot increases startup time and hides failures that belong in repository setup. If runtime initialization depends on an artifact, produce that artifact in `install` and consume it in `start`.

### Diagnose misplaced work

When environment setup hangs, behaves differently after a snapshot, or loses services between agents:

1. Identify the phase and command from setup logs. Do not infer the failing phase from the script name alone.
2. Ask whether the command creates durable files or requires a live process.
3. If `install` launches a server, watcher, worker, Docker daemon, or other process that must still be running later, move that responsibility to `start` or `terminals`.
4. If `start` repeatedly installs packages, compiles the repository, or regenerates source-derived files, move that responsibility to `install`.
5. Make the destination idempotent:
   - `install` should converge without appending state or rewriting lockfiles unexpectedly.
   - `start` should detect an already-running service, clean up stale PID/socket files, and fail clearly when readiness is not reached.
   - `terminals` should use stable names, bind services to the intended interface and port, and emit useful logs.
6. Validate each phase independently, then reboot or start a fresh agent to prove runtime services return without rerunning one-time setup manually.

Typical signals:

- **Install never completes:** a foreground server or interactive command is running in `install`.
- **Files exist but the service disappears on a later boot:** the service was started during `install` and its process was not part of durable state.
- **Every boot is slow or changes the lockfile:** dependency setup is incorrectly running in `start`.
- **Start fails with “address already in use” or duplicate workers:** the start path is not idempotent.
- **A service starts but cannot serve requests:** add an explicit readiness check and verify its port is configured and bound correctly.

## Dockerfile and Build Context

`build.dockerfile` and `build.context` are resolved relative to the directory containing `.cursor/environment.json`:

- `"dockerfile": "Dockerfile"` means `.cursor/Dockerfile`.
- Omitting `context` uses `.cursor` as the build context.
- `"context": "."`, `"./"`, or `".."` makes the repository root available as the build context.

Cursor checks out the requested repository revision separately after preparing the base environment. Avoid copying the whole repository into the image: it creates stale duplicate source, weakens layer caching, and makes branch behavior confusing. Use the Dockerfile for operating-system packages and stable tool versions; use `install` for dependency installation tied to lockfiles and source.

### Minimal default-image setup

~~~json
{
  "name": "My project",
  "install": "npm ci"
}
~~~

### Custom Dockerfile

`.cursor/environment.json`:

~~~json
{
  "name": "My project",
  "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },
  "user": "ubuntu",
  "install": "./scripts/cloud-agent-install.sh"
}
~~~

`.cursor/Dockerfile`:

~~~dockerfile
FROM node:22-bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git build-essential python3 \
    && rm -rf /var/lib/apt/lists/* \
    && corepack enable

USER node
~~~

### Idempotent install script

~~~bash
#!/usr/bin/env bash
set -euo pipefail

corepack pnpm install --frozen-lockfile
corepack pnpm generate
~~~

This Node example assumes `package.json` pins pnpm with `packageManager` and defines a deterministic `generate` script. Adapt the image and commands to the repository. Prefer its pinned package manager and lockfile; avoid broad upgrades or lockfile rewrites during environment setup unless the user explicitly requests them.

## Choose the workflow

Read only the reference that matches the request:

- **Create or fully set up an environment:** [Set up a new environment](references/create-environment.md). When build tools are available, that reference includes snapshot → build with `environmentJson` snapshot + install/start → fresh-agent verify → propose with `buildId` before the user Saves.
- **Update a repository-managed environment:** after environment-info confirms a non-empty `environmentJsonPath`, use [Update a repository-managed environment](references/update-repo-managed-environment.md).
- **Update a DB-managed environment:** after environment-info confirms a null or absent `environmentJsonPath`, use [Update a DB-managed environment](references/update-db-managed-environment.md).
- **Migrate the current environment to prebuilt baselines:** use [Migrate an environment to builds](references/migrate-to-builds.md).

Do not infer the backing type merely from a local file. Use environment-info when available because it reports the effective source used by this run. If the tool is unavailable, inspect the repository, explain what cannot be confirmed, and avoid claiming that a dashboard or repository setting was changed.

For an explanation or audit, the references are usually unnecessary. Read the public setup documentation and current schema when field-level accuracy matters, inspect the effective configuration and referenced files, and explain the lifecycle and precedence directly.


### Build-tested setup and update flows

Environment builds are not enabled for every environment. Follow the matching reference below for whether and when to call `trigger-environment-build`. Do not trigger speculative rebuilds for unrelated questions.

In the create and repository-managed update references, a user request to set up, change, improve, build, or test the environment through this skill is the explicit build request for the MCP tool—do not wait for a second "please build" phrase. Other references (including DB-managed update and migrate-to-builds) keep their own trigger rules; follow those files rather than this summary when they differ.

After calling environment-info:

- If the user wants to migrate the current environment to builds, test that it will work with builds, or asks to use the build migration guide, read [Migrate an environment to builds](references/migrate-to-builds.md) and follow it.
- A non-empty `environmentJsonPath` means repository-managed. Read [Update a repository-managed environment](references/update-repo-managed-environment.md).
- A null or absent `environmentJsonPath` means DB-managed. Read [Update a DB-managed environment](references/update-db-managed-environment.md).

Update flows require an environment ID. For a greenfield create with no linked environment, follow [Set up a new environment](references/create-environment.md) and pass `environmentJson` with optional `snapshot`, `install`, and/or `start` to `trigger-environment-build` so it can create a personal transitional draft.

## Troubleshooting

Find the earliest failing layer:

1. **Image build**: Dockerfile syntax, unavailable packages, build context, architecture, or registry access.
2. **Provisioning and checkout**: repository access, selected ref, runtime user, disk, or network policy.
3. **Install**: non-idempotent scripts, missing lockfiles, private dependency authentication, or generated-file assumptions.
4. **Start and terminals**: commands that exit unexpectedly, bind the wrong interface or port, or depend on setup that did not complete.

Use setup or build logs as evidence. Reproduce the smallest safe failing command when possible, then rerun the relevant verification. Treat definitive credential, authorization, quota, or entitlement failures as blockers after confirming them once.

## Safety

- Never put tokens, passwords, private keys, or secret values in `environment.json`, Dockerfiles, committed scripts, logs, or chat output. Use supported environment secrets or build-secret mechanisms.
- Do not deploy, publish, apply infrastructure, or mutate production resources as part of environment setup.
- Keep Dockerfiles and install scripts deterministic, non-interactive, and narrowly scoped.
- Do not weaken network, certificate, or package-integrity controls merely to make setup pass.
- Avoid expensive rebuilds until static checks pass. Trigger a build only when the matching workflow reference says to; those references define what counts as explicit user intent for `trigger-environment-build`. Unrelated questions never do.

## Response

Lead with the outcome. Include only the sections relevant to the request:

- Effective configuration source and lifecycle.
- What was inspected or changed.
- Validation evidence.
- Draft-build and subagent evidence, when testing a build.
- Remaining manual action, uncertainty, or blocker.

Only include dashboard links when `environment-info` returns a non-empty environment `url`. Use a markdown hyperlink whose link text is the complete ID:

- Environment / environment dashboard (when directing the user to enable builds or review build status): `[<environmentPublicId>](https://cursor.com/dashboard/cloud-agents/environments/e/<environmentPublicId>)`
- Build: `[<buildId>](https://cursor.com/dashboard/cloud-agents/builds/<buildId>)`

Use the returned environment `url` for the environment link; builds belonging to that environment may use their build-detail URLs. If `url` is absent—including for a transitional greenfield draft—do not construct links from IDs. Do not append `#builds` — build settings and the builds list live on the default environment detail page.
