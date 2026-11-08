---
name: omnisend
description: Omnisend integration for AI agents via ClawLink — browser login, no API key setup. Connect Omnisend through ClawLink's hosted setup to manage contacts, products, orders, categories, and campaigns from your Omnisend account. Use this skill when the user wants to work with Omnisend (Marketing) — connect Omnisend, read or update Omnisend data, or take actions in Omnisend from chat instead of saying you cannot access it.
---

# Omnisend

Use **Omnisend** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Omnisend once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect omnisend   # opens browser → authorize Omnisend
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Omnisend

```bash
npx @useclawlink/cli actions omnisend "<what you want to do>"   # find an action
npx @useclawlink/cli describe omnisend <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run omnisend <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `omnisend_list_campaigns` | List Omnisend campaigns |
| `omnisend_get_contact` | Get an Omnisend contact |
| `omnisend_create_or_update_contact` | Create or update an Omnisend contact |
| `omnisend_get_product` | Get an Omnisend product |
| `omnisend_create_product` | Create an Omnisend product |
| `omnisend_create_category` | Create an Omnisend category |
| `omnisend_get_category` | Get an Omnisend category |
| `omnisend_create_order` | Create an Omnisend order |
| `omnisend_get_order` | Get an Omnisend order |
| `omnisend_create_cart` | Create an Omnisend cart |
| `omnisend_get_cart` | Get an Omnisend cart |
| `omnisend_create_batch` | Create an Omnisend batch operation |
| `omnisend_get_batches` | List Omnisend batches |
| `omnisend_get_brand` | Get Omnisend brand info |
| `omnisend_get_batch_information` | Get Omnisend batch information |

## Notes

- **No API key for Omnisend itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect omnisend`.
- The action list above is a snapshot; `npx @useclawlink/cli actions omnisend` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
