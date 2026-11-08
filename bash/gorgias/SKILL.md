---
name: gorgias
description: Gorgias integration for AI agents via ClawLink — browser login, no API key setup. Connect Gorgias through ClawLink's hosted setup to manage customer support tickets for your e-commerce store. Use this skill when the user wants to work with Gorgias (Support) — connect Gorgias, read or update Gorgias data, or take actions in Gorgias from chat instead of saying you cannot access it.
---

# Gorgias

Use **Gorgias** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Gorgias once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect gorgias   # opens browser → authorize Gorgias
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Gorgias

```bash
npx @useclawlink/cli actions gorgias "<what you want to do>"   # find an action
npx @useclawlink/cli describe gorgias <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run gorgias <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions gorgias` to see every available Gorgias action.

## Notes

- **No API key for Gorgias itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect gorgias`.
- The action list above is a snapshot; `npx @useclawlink/cli actions gorgias` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
