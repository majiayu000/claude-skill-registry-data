---
name: linkhut
description: Linkhut integration for AI agents via ClawLink — browser login, no API key setup. Connect Linkhut through ClawLink's hosted setup to save, organize, and share bookmarks and links. Use this skill when the user wants to work with Linkhut (Social Media) — connect Linkhut, read or update Linkhut data, or take actions in Linkhut from chat instead of saying you cannot access it.
---

# Linkhut

Use **Linkhut** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Linkhut once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect linkhut   # opens browser → authorize Linkhut
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Linkhut

```bash
npx @useclawlink/cli actions linkhut "<what you want to do>"   # find an action
npx @useclawlink/cli describe linkhut <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run linkhut <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions linkhut` to see every available Linkhut action.

## Notes

- **No API key for Linkhut itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect linkhut`.
- The action list above is a snapshot; `npx @useclawlink/cli actions linkhut` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
