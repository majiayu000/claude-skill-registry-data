---
name: ticktick
description: Ticktick integration for AI agents via ClawLink — browser login, no API key setup. Connect Ticktick through ClawLink's hosted setup to manage tasks, habits, calendars, and to-do lists. Use this skill when the user wants to work with Ticktick (Productivity) — connect Ticktick, read or update Ticktick data, or take actions in Ticktick from chat instead of saying you cannot access it.
---

# Ticktick

Use **Ticktick** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Ticktick once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect ticktick   # opens browser → authorize Ticktick
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Ticktick

```bash
npx @useclawlink/cli actions ticktick "<what you want to do>"   # find an action
npx @useclawlink/cli describe ticktick <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run ticktick <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions ticktick` to see every available Ticktick action.

## Notes

- **No API key for Ticktick itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect ticktick`.
- The action list above is a snapshot; `npx @useclawlink/cli actions ticktick` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
