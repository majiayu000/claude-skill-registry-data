---
name: attio
description: Attio integration for AI agents via ClawLink — browser login, no API key setup. Connect Attio through ClawLink's hosted setup to manage contacts, companies, deals, and lists in your CRM. Use this skill when the user wants to work with Attio (CRM & Sales) — connect Attio, read or update Attio data, or take actions in Attio from chat instead of saying you cannot access it.
---

# Attio

Use **Attio** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Attio once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect attio   # opens browser → authorize Attio
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Attio

```bash
npx @useclawlink/cli actions attio "<what you want to do>"   # find an action
npx @useclawlink/cli describe attio <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run attio <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions attio` to see every available Attio action.

## Notes

- **No API key for Attio itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect attio`.
- The action list above is a snapshot; `npx @useclawlink/cli actions attio` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
