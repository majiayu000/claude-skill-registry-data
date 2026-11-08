---
name: mural
description: Mural integration for AI agents via ClawLink — browser login, no API key setup. Connect Mural through ClawLink's hosted setup to create and manage collaborative whiteboards and visual workspaces. Use this skill when the user wants to work with Mural (Productivity) — connect Mural, read or update Mural data, or take actions in Mural from chat instead of saying you cannot access it.
---

# Mural

Use **Mural** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Mural once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect mural   # opens browser → authorize Mural
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Mural

```bash
npx @useclawlink/cli actions mural "<what you want to do>"   # find an action
npx @useclawlink/cli describe mural <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run mural <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions mural` to see every available Mural action.

## Notes

- **No API key for Mural itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect mural`.
- The action list above is a snapshot; `npx @useclawlink/cli actions mural` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
