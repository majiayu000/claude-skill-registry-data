---
name: apaleo
description: Apaleo integration for AI agents via ClawLink — browser login, no API key setup. Connect Apaleo through ClawLink's hosted setup to manage hotel reservations, rates, and property operations. Use this skill when the user wants to work with Apaleo (CRM & Sales) — connect Apaleo, read or update Apaleo data, or take actions in Apaleo from chat instead of saying you cannot access it.
---

# Apaleo

Use **Apaleo** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Apaleo once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect apaleo   # opens browser → authorize Apaleo
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Apaleo

```bash
npx @useclawlink/cli actions apaleo "<what you want to do>"   # find an action
npx @useclawlink/cli describe apaleo <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run apaleo <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions apaleo` to see every available Apaleo action.

## Notes

- **No API key for Apaleo itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect apaleo`.
- The action list above is a snapshot; `npx @useclawlink/cli actions apaleo` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
