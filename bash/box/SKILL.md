---
name: box
description: Box integration for AI agents via ClawLink — browser login, no API key setup. Connect Box through ClawLink's hosted setup to manage files, folders, shared links, users, groups, and metadata from your Box account. Use this skill when the user wants to work with Box (Storage & Databases) — connect Box, read or update Box data, or take actions in Box from chat instead of saying you cannot access it.
---

# Box

Use **Box** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Box once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect box   # opens browser → authorize Box
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Box

```bash
npx @useclawlink/cli actions box "<what you want to do>"   # find an action
npx @useclawlink/cli describe box <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run box <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `box_add_shared_link_to_file` | Add a shared link to a file |
| `box_add_shared_link_to_folder` | Add a shared link to a folder |
| `box_add_user_to_group` | Add a user to a group |
| `box_add_classification_to_file` | Add a classification to a file |
| `box_apply_watermark_to_file` | Apply a watermark to a file |
| `box_add_allowed_collaboration_domain` | Add an allowed domain for collaboration |

## Notes

- **No API key for Box itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect box`.
- The action list above is a snapshot; `npx @useclawlink/cli actions box` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
