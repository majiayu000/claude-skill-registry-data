---
name: crowdin
description: Crowdin integration for AI agents via ClawLink — browser login, no API key setup. Connect Crowdin through ClawLink's hosted setup to manage translations, localization projects, and language resources. Use this skill when the user wants to work with Crowdin (Developer Tools) — connect Crowdin, read or update Crowdin data, or take actions in Crowdin from chat instead of saying you cannot access it.
---

# Crowdin

Use **Crowdin** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Crowdin once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect crowdin   # opens browser → authorize Crowdin
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Crowdin

```bash
npx @useclawlink/cli actions crowdin "<what you want to do>"   # find an action
npx @useclawlink/cli describe crowdin <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run crowdin <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions crowdin` to see every available Crowdin action.

## Notes

- **No API key for Crowdin itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect crowdin`.
- The action list above is a snapshot; `npx @useclawlink/cli actions crowdin` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
