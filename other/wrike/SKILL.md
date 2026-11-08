---
name: wrike
description: Wrike integration for AI agents via ClawLink — browser login, no API key setup. Connect Wrike through ClawLink's hosted setup to manage projects, tasks, and team workflows at scale. Use this skill when the user wants to work with Wrike (Productivity) — connect Wrike, read or update Wrike data, or take actions in Wrike from chat instead of saying you cannot access it.
---

# Wrike

Use **Wrike** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Wrike once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect wrike   # opens browser → authorize Wrike
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Wrike

```bash
npx @useclawlink/cli actions wrike "<what you want to do>"   # find an action
npx @useclawlink/cli describe wrike <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run wrike <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions wrike` to see every available Wrike action.

## Notes

- **No API key for Wrike itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect wrike`.
- The action list above is a snapshot; `npx @useclawlink/cli actions wrike` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
