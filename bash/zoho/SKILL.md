---
name: zoho
description: Zoho integration for AI agents via ClawLink — browser login, no API key setup. Connect Zoho through ClawLink's hosted setup for unified access to Zoho suite apps and business tools. Use this skill when the user wants to work with Zoho (Productivity) — connect Zoho, read or update Zoho data, or take actions in Zoho from chat instead of saying you cannot access it.
---

# Zoho

Use **Zoho** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Zoho once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect zoho   # opens browser → authorize Zoho
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Zoho

```bash
npx @useclawlink/cli actions zoho "<what you want to do>"   # find an action
npx @useclawlink/cli describe zoho <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run zoho <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions zoho` to see every available Zoho action.

## Notes

- **No API key for Zoho itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect zoho`.
- The action list above is a snapshot; `npx @useclawlink/cli actions zoho` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
