---
name: dub
description: Dub integration for AI agents via ClawLink — browser login, no API key setup. Connect Dub through ClawLink's hosted setup to create, manage, and track short links and analytics. Use this skill when the user wants to work with Dub (Marketing) — connect Dub, read or update Dub data, or take actions in Dub from chat instead of saying you cannot access it.
---

# Dub

Use **Dub** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Dub once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect dub   # opens browser → authorize Dub
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Dub

```bash
npx @useclawlink/cli actions dub "<what you want to do>"   # find an action
npx @useclawlink/cli describe dub <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run dub <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions dub` to see every available Dub action.

## Notes

- **No API key for Dub itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect dub`.
- The action list above is a snapshot; `npx @useclawlink/cli actions dub` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
