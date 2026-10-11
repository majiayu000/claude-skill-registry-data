---
name: setup
description: Set up Trigger.dev in a project, connect to a self-hosted instance, verify MCP connection, authenticate the CLI, or configure dev/staging/production environments. Use when the user asks to "set up trigger.dev", "init trigger project", "connect to self-hosted trigger", "verify trigger connection", "install trigger.dev", or "configure trigger environments".
---

# Trigger.dev Setup

Get Trigger.dev running in your project — self-hosted or cloud — and verify the connection.

## When to Use

- Adding Trigger.dev to an existing project
- Creating your first task
- Connecting to a self-hosted Trigger.dev v4 instance
- Verifying MCP or CLI connection
- Configuring environments (dev / staging / production)

## Prerequisites

- Node.js 18.20+ locally (deployed tasks run on the runtime set in `trigger.config.ts`; or Bun)
- TypeScript 5.0.4+
- A Trigger.dev account — cloud or self-hosted instance
- For self-hosted: running webapp + supervisor Docker Compose stacks

## Step 1: Install the SDK

```bash
npm install @trigger.dev/sdk
npm install -D trigger.dev   # pin the CLI to the same version as the SDK
```

The CLI, `@trigger.dev/sdk` and `@trigger.dev/build` must share one version. On self-hosted, use the version of the server (see the **deployment** skill).

## Step 2: Authenticate the CLI

### Cloud

```bash
npx trigger.dev@latest login
```

### Self-Hosted

```bash
npx trigger.dev@latest login -a https://trigger.example.com
```

The `-a` flag tells the CLI where your instance lives. The CLI remembers this URL for all subsequent commands.

### Multiple Instances (Profiles)

```bash
# Login with a named profile
npx trigger.dev@latest login -a https://trigger.example.com --profile self-hosted

# Use the profile for dev/deploy
npx trigger.dev@latest dev --profile self-hosted
npx trigger.dev@<version> deploy --profile self-hosted

# List all saved profiles
npx trigger.dev@latest list-profiles

# Switch between profiles
npx trigger.dev@latest switch self-hosted

# Verify who you're logged in as
npx trigger.dev@latest whoami
```

## Step 3: Initialize Project

```bash
npx trigger.dev@latest init
```

This creates:
- `trigger.config.ts` — project configuration
- `src/trigger/` directory — where your tasks live
- A sample task file

### Self-Hosted Init

```bash
npx trigger.dev@latest init -p <project-ref> -a https://trigger.example.com
```

The CLI has no self-hosted switch of its own on any command; a self-hosted instance is selected only by `-a, --api-url` (or `TRIGGER_API_URL`).

### Non-interactive init (agents, CI)

Without a TTY `init` refuses to run unless you pass `--yes` (it also needs `--project-ref`, or `--project-name` with `--org-name` for a new account):

```bash
npx trigger.dev@latest init --yes --project-ref proj_xxx -a https://trigger.example.com --no-browser
```

### Init Flags

| Flag | Description |
|------|-------------|
| `-p, --project-ref` | Project ref (proj_xxx) from dashboard |
| `-a, --api-url` | API URL for self-hosted |
| `-r, --runtime` | Runtime: `node`, `node-22`, `node-24`, `node-26`, `bun` (default `node-24`) |
| `-y, --yes` | Skip all prompts; requires `--project-ref`, or `--project-name` with `--org-name` |
| `--no-browser` | Do not open the browser during login; print the URL |
| `--project-name`, `--org-name` | Bootstrap a new project / organization non-interactively |
| `-t, --tag` | `@trigger.dev/sdk` version to install |
| `--pkg-args <args>` | Extra package-manager arguments (CSV) |
| `--skip-package-install` | Skip SDK install |
| `--override-config` | Overwrite an existing config file |
| `--javascript` | Use JavaScript instead of TypeScript |
| `--profile` | Login profile to use |

## Step 4: Configure trigger.config.ts

```ts
import { defineConfig } from "@trigger.dev/sdk";

export default defineConfig({
  project: "proj_xxxxx",  // From your dashboard
  dirs: ["./src/trigger"],
  maxDuration: 300,       // required: seconds, at least 5 (dev and deploy fail without it)
});
```

## Step 5: Create Your First Task

```ts
// src/trigger/my-task.ts
import { task } from "@trigger.dev/sdk";

export const myFirstTask = task({
  id: "my-first-task",
  run: async (payload: { name: string }) => {
    console.log(`Hello, ${payload.name}!`);
    return { message: `Processed ${payload.name}` };
  },
});
```

## Step 6: Start Dev Server

```bash
npx trigger.dev@latest dev
```

The dev server watches for file changes, registers tasks with the dev environment, and executes tasks locally. `dev` is a command group whose default sub-command is `start`; `-b/--branch <name>` selects a dev branch, and `dev archive` archives one. In an agent session prefer the MCP tool `start_dev_server`: a foreground `dev` blocks the shell.

## Step 7: Trigger Your Task

From your app code:

```ts
import { tasks } from "@trigger.dev/sdk";
import type { myFirstTask } from "./trigger/my-task";

await tasks.trigger<typeof myFirstTask>("my-first-task", {
  name: "World",
});
```

Or use the **Test** tab in the Trigger.dev dashboard.

## Environment Variables

| Variable | Description | Format |
|----------|-------------|--------|
| `TRIGGER_DEV_SECRET_KEY` | Dev environment secret key | `tr_dev_xxx` |
| `TRIGGER_STAGE_SECRET_KEY` | Staging environment secret key | `tr_dev_xxx` (different key) |
| `TRIGGER_PROD_SECRET_KEY` | Production environment secret key | `tr_prod_xxx` |
| `TRIGGER_API_URL` | Self-hosted instance URL | `https://trigger.example.com` |
| `TRIGGER_PROJECT_REF` | Project identifier from dashboard | `proj_xxxxx` |
| `TRIGGER_ACCESS_TOKEN` | Personal access token for CI/CD | `tr_pat_xxx` |

Each environment has its own secret key. The SDK itself reads `TRIGGER_SECRET_KEY`: set it to the key of the environment you are targeting (for example `TRIGGER_SECRET_KEY=$TRIGGER_PROD_SECRET_KEY`), or pass the per-environment key explicitly via `configure({ secretKey })`.

Set in `.env`:

```bash
TRIGGER_PROJECT_REF=proj_xxxxx
TRIGGER_DEV_SECRET_KEY=tr_dev_xxxxxxxxxxxxxx
TRIGGER_STAGE_SECRET_KEY=tr_dev_yyyyyyyyyyyyyy
TRIGGER_PROD_SECRET_KEY=tr_prod_zzzzzzzzzzzzzz
TRIGGER_API_URL=https://trigger.your-domain.com
```

For the full reference, see @references/environment-setup.md.

## MCP Server Setup

Trigger.dev provides an **official MCP server** shipped with the CLI (41 tools). The supported install flow is the `install-mcp` command:

```bash
# Install for a specific AI client (writes the client's MCP config for you)
npx trigger.dev@latest install-mcp --client claude-code

# Or — install into every supported client automatically
npx trigger.dev@latest install-mcp --yolo
```

Manual config:

```json
{
  "mcpServers": {
    "trigger": {
      "command": "npx",
      "args": ["trigger.dev@latest", "mcp"]
    }
  }
}
```

Common flag combinations:

```bash
# Dev-only — every tool rejects non-dev environments; deploy and list_preview_branches fail
npx trigger.dev@latest install-mcp --dev-only

# Scoped to one project, self-hosted API URL
npx trigger.dev@latest install-mcp --project-ref proj_abc123 -a https://trigger.example.com
```

### Read-only MCP

`--readonly` is a flag of `trigger.dev mcp` only; the installer command rejects it with `unknown option`. Put it in the server args:

```json
{
  "mcpServers": {
    "trigger": {
      "command": "npx",
      "args": ["trigger.dev@latest", "mcp", "--readonly"]
    }
  }
}
```

It hides 15 write tools server-side: `deploy`, `trigger_task`, `cancel_run`, `create_project_in_org`, `initialize_project`, the five prompt writers (`promote_prompt_version`, `create_prompt_override`, `update_prompt_override`, `remove_prompt_override`, `reactivate_prompt_override`), `start_agent_chat`, `send_agent_message`, `close_agent_chat`, `write_session_channel` and `submit_feedback`. It does **not** hide `start_dev_server`, `stop_dev_server` or `switch_profile`.

> **Production tip:** use `mcp --readonly` when wiring MCP into an agent that must not mutate a production instance. Hidden tools are never offered to the model, not just filtered by the client.

See https://trigger.dev/docs/mcp-introduction for the per-client config file locations. The docs page attributes `--readonly` to `install-mcp`; the CLI help of 4.7.2 shows it only on `mcp`.

## Agent Skills Installation

Agent rules were replaced by agent skills. The canonical command is `skills`; `install-rules` is only an alias for it.

```bash
# Interactive
npx trigger.dev@latest skills

# Non-interactive, specific targets (claude-code, cursor, vscode, agents.md)
npx trigger.dev@latest skills --target claude-code --target cursor -y
```

It installs five skills (trigger-authoring-tasks, trigger-realtime-and-frontend, trigger-authoring-chat-agent, trigger-chat-agent-advanced, trigger-cost-savings) into the agent's skills folder, for example `.claude/skills/`. `trigger dev` offers the install on its first run. The `@trigger.dev/sdk` package also ships version-exact `docs/` and `skills/` folders in `node_modules`.

## Verification Checklist

1. **CLI auth**: `npx trigger.dev@latest whoami` returns your user info
2. **Dev server**: `npx trigger.dev@latest dev` starts without errors
3. **Tasks registered**: Dashboard shows your tasks under the dev environment
4. **If MCP**: MCP tool `list_orgs` returns your organizations

## Self-Hosted v4 Health Check

```bash
# Check webapp services
cd trigger.dev/hosting/docker/webapp
docker compose ps

# Check supervisor
cd trigger.dev/hosting/docker/worker
docker compose ps

# View logs
docker compose logs -f webapp
docker compose logs -f supervisor
```

## Deeper Reference

- @references/project-structure.md — project layout conventions
- @references/environment-setup.md — complete environment and self-hosted configuration