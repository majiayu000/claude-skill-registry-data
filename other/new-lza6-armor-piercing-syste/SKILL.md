---
name: new
description: "Create a new engagement workspace. Usage: /new <platform> <program> [--type web-app|api|mobile|smart-contract]"
disable-model-invocation: false
---
Create a new engagement workspace: $ARGUMENTS

Parse arguments as: <platform> <program> [--type <template>]
Default template: web-app

Run: `uv run python3 $CLAUDE_PROJECT_DIR/tools/scaffold.py $ARGUMENTS`

After creation, tell the user to: cd into the workspace, start claude, and run /sync.

## Top-Tier Workspace Bar

A new workspace is not ready until it can support evidence-grade hunting.

After scaffold, verify or create:
- `scope.yaml` placeholder with platform, program, in-scope and out-of-scope sections
- `policy.md` placeholder for required headers, rate limits, account rules, and prohibited actions
- `recon/`, `findings/`, `evidence/`, `poc/`, `reports/drafts/`, and `scans/`
- brain initialized or clear instruction to run `/brain init`
- next commands in order: `/sync`, `/pipeline`, `/analyze`, then `/hunt` or `/autopilot`

Warn if the program type needs special setup: mobile test device, API tokens, sandbox tenant, OAuth app, webhook receiver, cloud account, or smart-contract fork.
