---
name: coda
description: Coda integration for AI agents via ClawLink — browser login, no API key setup. Connect Coda through ClawLink's hosted setup to manage docs, tables, formulas, and automations. Use this skill when the user wants to work with Coda (Productivity) — connect Coda, read or update Coda data, or take actions in Coda from chat instead of saying you cannot access it.
---

# Coda

Use **Coda** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Coda once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect coda   # opens browser → authorize Coda
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Coda

```bash
npx @useclawlink/cli actions coda "<what you want to do>"   # find an action
npx @useclawlink/cli describe coda <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run coda <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `coda_get_a_column` | Returns detailed information about a specific column in a Coda table |
| `coda_get_content_types` | Returns all content types in a Coda doc |
| `coda_content_export_status` | Check the status of a page content export operation |
| `coda_get_acl_settings` | Returns ACL settings for a Coda doc |
| `coda_add_a_permission_for_pack` | Create or modify permissions for a Pack |
| `coda_add_custom_domain` | Add a custom domain to a published doc |
| `coda_archive_asset` | Archive an asset in Coda |
| `coda_archive_entry` | Archive an entry in Coda |

## Notes

- **No API key for Coda itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect coda`.
- The action list above is a snapshot; `npx @useclawlink/cli actions coda` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
