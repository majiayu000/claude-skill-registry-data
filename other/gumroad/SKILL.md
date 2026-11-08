---
name: gumroad
description: Gumroad integration for AI agents via ClawLink — browser login, no API key setup. Connect Gumroad through ClawLink's hosted setup to manage products, sales, subscribers, licenses, and webhooks. Use this skill when the user wants to work with Gumroad (E-commerce) — connect Gumroad, read or update Gumroad data, or take actions in Gumroad from chat instead of saying you cannot access it.
---

# Gumroad

Use **Gumroad** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Gumroad once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect gumroad   # opens browser → authorize Gumroad
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Gumroad

```bash
npx @useclawlink/cli actions gumroad "<what you want to do>"   # find an action
npx @useclawlink/cli describe gumroad <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run gumroad <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `gumroad_get_user` | Get the authenticated Gumroad user |
| `gumroad_list_products` | List all products for the Gumroad account |
| `gumroad_get_sales` | Retrieve all successful sales |
| `gumroad_verify_license` | Verify a Gumroad license key against a product |
| `gumroad_subscribe_to_resource` | Subscribe to a resource for webhooks |
| `gumroad_unsubscribe_from_resource` | Unsubscribe from a resource |
| `gumroad_get_resource_subscriptions` | List all active subscriptions for a resource |

## Notes

- **No API key for Gumroad itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect gumroad`.
- The action list above is a snapshot; `npx @useclawlink/cli actions gumroad` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
