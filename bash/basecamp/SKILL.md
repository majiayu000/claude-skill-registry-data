---
name: basecamp
description: Basecamp integration for AI agents via ClawLink — browser login, no API key setup. Connect Basecamp through ClawLink's hosted setup to manage projects, to-do lists, messages, and team collaboration. Use this skill when the user wants to work with Basecamp (Productivity) — connect Basecamp, read or update Basecamp data, or take actions in Basecamp from chat instead of saying you cannot access it.
---

# Basecamp

Use **Basecamp** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Basecamp once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect basecamp   # opens browser → authorize Basecamp
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Basecamp

```bash
npx @useclawlink/cli actions basecamp "<what you want to do>"   # find an action
npx @useclawlink/cli describe basecamp <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run basecamp <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions basecamp` to see every available Basecamp action.

## Notes

- **No API key for Basecamp itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect basecamp`.
- The action list above is a snapshot; `npx @useclawlink/cli actions basecamp` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
