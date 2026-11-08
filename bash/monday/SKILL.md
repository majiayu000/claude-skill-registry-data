---
name: monday
description: Monday integration for AI agents via ClawLink — browser login, no API key setup. Connect Monday through ClawLink's hosted setup to manage boards, items, teams, workspaces, and automations from your Monday.com account. Use this skill when the user wants to work with Monday (Productivity) — connect Monday, read or update Monday data, or take actions in Monday from chat instead of saying you cannot access it.
---

# Monday

Use **Monday** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Monday once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect monday   # opens browser → authorize Monday
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Monday

```bash
npx @useclawlink/cli actions monday "<what you want to do>"   # find an action
npx @useclawlink/cli describe monday <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run monday <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `monday_add_subscribers_to_board` | Add users as subscribers to a Monday board |
| `monday_add_users_to_board` | Add users to a Monday board with a specified role |
| `monday_add_users_to_team` | Add users to a Monday team |
| `monday_archive_board` | Archive a Monday board |
| `monday_archive_item` | Archive a Monday item |
| `monday_create_board` | Create a new Monday board |
| `monday_create_item` | Create a new item on a Monday board |
| `monday_create_update` | Create an update on a Monday item |

## Notes

- **No API key for Monday itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect monday`.
- The action list above is a snapshot; `npx @useclawlink/cli actions monday` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
