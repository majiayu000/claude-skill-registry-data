---
name: dialpad
description: Dialpad integration for AI agents via ClawLink — browser login, no API key setup. Connect Dialpad through ClawLink's hosted setup to manage business phone calls, messaging, and video conferences. Use this skill when the user wants to work with Dialpad (Communication) — connect Dialpad, read or update Dialpad data, or take actions in Dialpad from chat instead of saying you cannot access it.
---

# Dialpad

Use **Dialpad** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Dialpad once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect dialpad   # opens browser → authorize Dialpad
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Dialpad

```bash
npx @useclawlink/cli actions dialpad "<what you want to do>"   # find an action
npx @useclawlink/cli describe dialpad <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run dialpad <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions dialpad` to see every available Dialpad action.

## Notes

- **No API key for Dialpad itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect dialpad`.
- The action list above is a snapshot; `npx @useclawlink/cli actions dialpad` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
