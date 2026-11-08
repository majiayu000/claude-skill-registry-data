---
name: gong
description: Gong integration for AI agents via ClawLink — browser login, no API key setup. Connect Gong through ClawLink's hosted setup to record, analyze, and gain insights from sales conversations. Use this skill when the user wants to work with Gong (Communication) — connect Gong, read or update Gong data, or take actions in Gong from chat instead of saying you cannot access it.
---

# Gong

Use **Gong** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Gong once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect gong   # opens browser → authorize Gong
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Gong

```bash
npx @useclawlink/cli actions gong "<what you want to do>"   # find an action
npx @useclawlink/cli describe gong <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run gong <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions gong` to see every available Gong action.

## Notes

- **No API key for Gong itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect gong`.
- The action list above is a snapshot; `npx @useclawlink/cli actions gong` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
