---
name: harvest
description: Harvest integration for AI agents via ClawLink — browser login, no API key setup. Connect Harvest through ClawLink's hosted setup to track time, manage projects, and invoice clients. Use this skill when the user wants to work with Harvest (Productivity) — connect Harvest, read or update Harvest data, or take actions in Harvest from chat instead of saying you cannot access it.
---

# Harvest

Use **Harvest** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Harvest once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect harvest   # opens browser → authorize Harvest
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Harvest

```bash
npx @useclawlink/cli actions harvest "<what you want to do>"   # find an action
npx @useclawlink/cli describe harvest <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run harvest <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions harvest` to see every available Harvest action.

## Notes

- **No API key for Harvest itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect harvest`.
- The action list above is a snapshot; `npx @useclawlink/cli actions harvest` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
