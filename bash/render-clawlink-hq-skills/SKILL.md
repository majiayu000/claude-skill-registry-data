---
name: render
description: Render integration for AI agents via ClawLink — browser login, no API key setup. Connect Render through ClawLink's hosted setup to manage services, deployments, environments, and metrics. Use this skill when the user wants to work with Render (Developer Tools) — connect Render, read or update Render data, or take actions in Render from chat instead of saying you cannot access it.
---

# Render

Use **Render** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Render once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect render   # opens browser → authorize Render
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Render

```bash
npx @useclawlink/cli actions render "<what you want to do>"   # find an action
npx @useclawlink/cli describe render <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run render <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `render_get_cpu` | Retrieve CPU usage metrics for Render resources |
| `render_get_memory` | Get memory usage metrics for Render resources |
| `render_get_disk_usage` | Retrieve disk usage metrics |
| `render_get_instance_count` | Get instance count metrics |
| `render_add_headers` | Add a custom HTTP header rule to a service |
| `render_add_or_update_secret_file` | Add or update a secret file for a service |
| `render_add_resources_to_environment` | Add resources to a Render environment |
| `render_add_route` | Add redirect or rewrite rules to a service |

## Notes

- **No API key for Render itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect render`.
- The action list above is a snapshot; `npx @useclawlink/cli actions render` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
