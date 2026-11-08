---
name: shippo
description: Shippo integration for AI agents via ClawLink — browser login, no API key setup. Connect Shippo through ClawLink's hosted setup to generate shipping labels, track packages, and manage fulfillment. Use this skill when the user wants to work with Shippo (E-commerce) — connect Shippo, read or update Shippo data, or take actions in Shippo from chat instead of saying you cannot access it.
---

# Shippo

Use **Shippo** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Shippo once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect shippo   # opens browser → authorize Shippo
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Shippo

```bash
npx @useclawlink/cli actions shippo "<what you want to do>"   # find an action
npx @useclawlink/cli describe shippo <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run shippo <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions shippo` to see every available Shippo action.

## Notes

- **No API key for Shippo itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect shippo`.
- The action list above is a snapshot; `npx @useclawlink/cli actions shippo` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
