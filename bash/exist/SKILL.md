---
name: exist
description: Exist integration for AI agents via ClawLink — browser login, no API key setup. Connect Exist through ClawLink's hosted setup to track and analyze personal health, fitness, and lifestyle data. Use this skill when the user wants to work with Exist (Health & Fitness) — connect Exist, read or update Exist data, or take actions in Exist from chat instead of saying you cannot access it.
---

# Exist

Use **Exist** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Exist once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect exist   # opens browser → authorize Exist
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Exist

```bash
npx @useclawlink/cli actions exist "<what you want to do>"   # find an action
npx @useclawlink/cli describe exist <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run exist <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions exist` to see every available Exist action.

## Notes

- **No API key for Exist itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect exist`.
- The action list above is a snapshot; `npx @useclawlink/cli actions exist` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
