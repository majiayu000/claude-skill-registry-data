---
name: boldsign
description: Boldsign integration for AI agents via ClawLink — browser login, no API key setup. Connect Boldsign through ClawLink's hosted setup to send, sign, and manage electronic documents and agreements. Use this skill when the user wants to work with Boldsign (Productivity) — connect Boldsign, read or update Boldsign data, or take actions in Boldsign from chat instead of saying you cannot access it.
---

# Boldsign

Use **Boldsign** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Boldsign once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect boldsign   # opens browser → authorize Boldsign
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Boldsign

```bash
npx @useclawlink/cli actions boldsign "<what you want to do>"   # find an action
npx @useclawlink/cli describe boldsign <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run boldsign <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions boldsign` to see every available Boldsign action.

## Notes

- **No API key for Boldsign itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect boldsign`.
- The action list above is a snapshot; `npx @useclawlink/cli actions boldsign` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
