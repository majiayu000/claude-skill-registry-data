---
name: make
description: Make integration for AI agents via ClawLink — browser login, no API key setup. Connect Make through ClawLink's hosted setup to manage organizations, teams, scenarios, users, and monitor operations from your Make account. Use this skill when the user wants to work with Make (Developer Tools) — connect Make, read or update Make data, or take actions in Make from chat instead of saying you cannot access it.
---

# Make

Use **Make** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Make once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect make   # opens browser → authorize Make
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Make

```bash
npx @useclawlink/cli actions make "<what you want to do>"   # find an action
npx @useclawlink/cli describe make <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run make <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `make_list_organizations` | List organizations you belong to |
| `make_create_organizations` | Create a new organization |
| `make_list_teams` | List teams in an organization |
| `make_get_users_me` | Get current user profile |
| `make_get_current_authorization` | Get current authorization and scopes |
| `make_get_operations` | Get daily operations usage |
| `make_get_cashier_products` | List available subscription products |
| `make_get_cashier_prices` | Get pricing details |
| `make_get_enums_imt_regions` | List Make regions |
| `make_get_enums_llm_models` | List available LLM models |
| `make_get_enums_module_types` | List module types |
| `make_list_enums_countries` | List supported countries |
| `make_ping_api` | Ping Make API to verify connectivity |

## Notes

- **No API key for Make itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect make`.
- The action list above is a snapshot; `npx @useclawlink/cli actions make` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
