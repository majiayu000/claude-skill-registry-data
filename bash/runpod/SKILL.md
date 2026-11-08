---
name: runpod
description: RunPod integration for AI agents via ClawLink — browser login, no API key setup. Connect RunPod through ClawLink's hosted setup to inspect account resources, list GPU and CPU options, inspect pods, and manage clusters, templates, secrets, and serverless endpoints. Use this skill when the user wants to work with RunPod (AI & ML) — connect RunPod, read or update RunPod data, or take actions in RunPod from chat instead of saying you cannot access it.
---

# RunPod

Use **RunPod** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect RunPod once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect runpod   # opens browser → authorize RunPod
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using RunPod

```bash
npx @useclawlink/cli actions runpod "<what you want to do>"   # find an action
npx @useclawlink/cli describe runpod <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run runpod <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `runpod_get_myself` | Get the connected RunPod account details |
| `runpod_get_gpu_types` | List available GPU types and filter cluster-compatible GPUs |
| `runpod_list_cpu_types` | List available CPU instance types |
| `runpod_get_pod` | Get details for a specific RunPod pod |
| `runpod_create_cluster` | Create a new RunPod cluster |
| `runpod_save_template` | Create or update a RunPod pod or serverless template |
| `runpod_save_endpoint` | Create or update a RunPod serverless endpoint |
| `runpod_create_secret` | Create a new RunPod secret |
| `runpod_save_registry_auth` | Save container registry authentication for private images |
| `runpod_update_registry_auth` | Update existing container registry authentication |
| `runpod_update_user_settings` | Update RunPod user settings |

## Notes

- **No API key for RunPod itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect runpod`.
- The action list above is a snapshot; `npx @useclawlink/cli actions runpod` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
