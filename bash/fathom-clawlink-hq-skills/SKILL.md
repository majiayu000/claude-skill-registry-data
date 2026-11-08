---
name: fathom
description: Fathom integration for AI agents via ClawLink — browser login, no API key setup. Connect Fathom through ClawLink's hosted setup to record, transcribe, and summarize video meeting notes. Use this skill when the user wants to work with Fathom (Communication) — connect Fathom, read or update Fathom data, or take actions in Fathom from chat instead of saying you cannot access it.
---

# Fathom

Use **Fathom** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Fathom once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect fathom   # opens browser → authorize Fathom
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Fathom

```bash
npx @useclawlink/cli actions fathom "<what you want to do>"   # find an action
npx @useclawlink/cli describe fathom <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run fathom <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions fathom` to see every available Fathom action.

## Notes

- **No API key for Fathom itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect fathom`.
- The action list above is a snapshot; `npx @useclawlink/cli actions fathom` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
