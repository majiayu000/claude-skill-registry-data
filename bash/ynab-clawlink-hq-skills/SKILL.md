---
name: ynab
description: YNAB integration for AI agents via ClawLink — browser login, no API key setup. Connect YNAB through ClawLink's hosted setup to manage budgets, track expenses, and plan finances. Use this skill when the user wants to work with YNAB (Payments & Finance) — connect YNAB, read or update YNAB data, or take actions in YNAB from chat instead of saying you cannot access it.
---

# YNAB

Use **YNAB** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect YNAB once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect ynab   # opens browser → authorize YNAB
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using YNAB

```bash
npx @useclawlink/cli actions ynab "<what you want to do>"   # find an action
npx @useclawlink/cli describe ynab <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run ynab <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions ynab` to see every available YNAB action.

## Notes

- **No API key for YNAB itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect ynab`.
- The action list above is a snapshot; `npx @useclawlink/cli actions ynab` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
