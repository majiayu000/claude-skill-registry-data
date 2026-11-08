---
name: slackbot
description: Slackbot integration for AI agents via ClawLink — browser login, no API key setup. Connect Slackbot through ClawLink's hosted setup to automate Slack workspace actions with bot-specific capabilities. Use this skill when the user wants to work with Slackbot (Communication) — connect Slackbot, read or update Slackbot data, or take actions in Slackbot from chat instead of saying you cannot access it.
---

# Slackbot

Use **Slackbot** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Slackbot once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect slackbot   # opens browser → authorize Slackbot
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Slackbot

```bash
npx @useclawlink/cli actions slackbot "<what you want to do>"   # find an action
npx @useclawlink/cli describe slackbot <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run slackbot <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions slackbot` to see every available Slackbot action.

## Notes

- **No API key for Slackbot itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect slackbot`.
- The action list above is a snapshot; `npx @useclawlink/cli actions slackbot` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
