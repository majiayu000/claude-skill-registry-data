---
name: prisma
description: Prisma integration for AI agents via ClawLink — browser login, no API key setup. Connect Prisma through ClawLink's hosted setup to manage database schemas, migrations, and queries. Use this skill when the user wants to work with Prisma (Developer Tools) — connect Prisma, read or update Prisma data, or take actions in Prisma from chat instead of saying you cannot access it.
---

# Prisma

Use **Prisma** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Prisma once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect prisma   # opens browser → authorize Prisma
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Prisma

```bash
npx @useclawlink/cli actions prisma "<what you want to do>"   # find an action
npx @useclawlink/cli describe prisma <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run prisma <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions prisma` to see every available Prisma action.

## Notes

- **No API key for Prisma itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect prisma`.
- The action list above is a snapshot; `npx @useclawlink/cli actions prisma` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
