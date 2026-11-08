---
name: webex
description: Webex integration for AI agents via ClawLink — browser login, no API key setup. Connect Webex through ClawLink's hosted setup to schedule and manage meetings, calls, and team messaging. Use this skill when the user wants to work with Webex (Communication) — connect Webex, read or update Webex data, or take actions in Webex from chat instead of saying you cannot access it.
---

# Webex

Use **Webex** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Webex once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect webex   # opens browser → authorize Webex
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Webex

```bash
npx @useclawlink/cli actions webex "<what you want to do>"   # find an action
npx @useclawlink/cli describe webex <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run webex <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions webex` to see every available Webex action.

## Notes

- **No API key for Webex itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect webex`.
- The action list above is a snapshot; `npx @useclawlink/cli actions webex` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
