---
name: timely
description: Timely integration for AI agents via ClawLink — browser login, no API key setup. Connect Timely through ClawLink's hosted setup to automatically track time and manage projects. Use this skill when the user wants to work with Timely (Productivity) — connect Timely, read or update Timely data, or take actions in Timely from chat instead of saying you cannot access it.
---

# Timely

Use **Timely** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Timely once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect timely   # opens browser → authorize Timely
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Timely

```bash
npx @useclawlink/cli actions timely "<what you want to do>"   # find an action
npx @useclawlink/cli describe timely <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run timely <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions timely` to see every available Timely action.

## Notes

- **No API key for Timely itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect timely`.
- The action list above is a snapshot; `npx @useclawlink/cli actions timely` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
