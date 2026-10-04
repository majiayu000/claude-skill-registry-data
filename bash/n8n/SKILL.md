---
name: n8n
description: Manage n8n workflows, executions and credentials via REST API
user-invocable: true
argument-hint: [workflow ID]
---

# /n8n

Connect to the n8n REST API to manage workflows, executions and credentials. Works with self-hosted n8n instances and n8n Cloud. Pure Ruby, zero gems — stdlib only.

## Structure

```
scripts/
├── auth.rb          # API key auth via X-N8N-API-KEY header + n8n_request helper (required by all scripts)
├── check_setup.rb   # Check if API key and host are configured (outputs OK or SETUP_NEEDED)
├── save_token.rb    # Save and validate API key + host URL
├── workflows.rb     # List all workflows
├── workflow.rb      # Get workflow details
├── activate.rb      # Activate a workflow
├── deactivate.rb    # Deactivate a workflow
├── executions.rb    # List executions (with optional filters)
├── execution.rb     # Get execution details
└── credentials.rb   # List credentials (no secrets shown)
```

## Setup (check before using)

```bash
ruby ~/.claude/skills/n8n/scripts/check_setup.rb
```

If the output is `OK`, proceed to the Flow section.

If the output is `SETUP_NEEDED`, guide the user step by step. Present ONE step at a time, wait for the user to confirm before moving to the next.

**Step 1** — Ask the user for their n8n host URL:

> What is the URL of your n8n instance?
>
> - Self-hosted: typically `http://localhost:5678`
> - n8n Cloud: `https://your-instance.app.n8n.cloud`
>
> Paste the base URL here (no trailing slash).

**Step 2** — Ask the user to create an API key:

> You need an n8n API key. Go to your n8n instance:
>
> 1. Open **Settings** → **API** (or navigate to `<your-host>/settings/api`)
> 2. Click **Create an API key**
> 3. Copy the key and paste it here
>
> If you don't see the API section, make sure the REST API is enabled in your n8n environment variables (`N8N_PUBLIC_API_ENABLED=true`).

**Step 3** — When the user provides both values, save them:

```bash
ruby ~/.claude/skills/n8n/scripts/save_token.rb 'API_KEY' 'HOST_URL'
```

If the script outputs an error, the API key or host is invalid. Ask the user to double-check and try again.

**If setup is not complete, DO NOT proceed to the Flow. Complete all steps first.**

## Flow

The argument `$ARGUMENTS` may contain a workflow ID.

### Step 1: List workflows

```bash
ruby ~/.claude/skills/n8n/scripts/workflows.rb
```

Present the workflows to the user. If `$ARGUMENTS` matches a workflow ID, use that workflow. Otherwise ask which workflow to work with.

### Step 2: Show workflow details

```bash
ruby ~/.claude/skills/n8n/scripts/workflow.rb WORKFLOW_ID
```

Present the workflow info (name, active status, nodes, connections) and ask what the user wants to do.

### Step 3: Actions

**Activate a workflow (requires user confirmation):**

Show the workflow name and current status first, then ask: "Do you want to activate this workflow?" Only execute after a "yes".

```bash
ruby ~/.claude/skills/n8n/scripts/activate.rb WORKFLOW_ID
```

**Deactivate a workflow (requires user confirmation):**

Show the workflow name and current status first, then ask: "Do you want to deactivate this workflow?" Only execute after a "yes".

```bash
ruby ~/.claude/skills/n8n/scripts/deactivate.rb WORKFLOW_ID
```

**List executions:**

```bash
ruby ~/.claude/skills/n8n/scripts/executions.rb
ruby ~/.claude/skills/n8n/scripts/executions.rb --workflowId WORKFLOW_ID
ruby ~/.claude/skills/n8n/scripts/executions.rb --status error
ruby ~/.claude/skills/n8n/scripts/executions.rb --workflowId WORKFLOW_ID --status success
```

**Get execution details:**

```bash
ruby ~/.claude/skills/n8n/scripts/execution.rb EXECUTION_ID
```

**List credentials (no secrets shown):**

```bash
ruby ~/.claude/skills/n8n/scripts/credentials.rb
```

## Notes

- **Pure Ruby, zero gems** — stdlib only (json, net/http, uri, fileutils)
- Auth via `X-N8N-API-KEY` header
- Config files: `~/.config/n8n/api_key` and `~/.config/n8n/host` (outside the repo, never commit)
- n8n can be self-hosted — the host URL is fully configurable (default: `http://localhost:5678`)
- Activating and deactivating workflows require explicit user confirmation
- The credentials endpoint only lists credential names and types — secrets are never exposed
