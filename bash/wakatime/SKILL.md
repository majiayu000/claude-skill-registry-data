---
name: wakatime
description: WakaTime integration for AI agents via ClawLink — browser login, no API key setup. Connect WakaTime through ClawLink's hosted setup to track coding time, language stats, and developer productivity. Use this skill when the user wants to work with WakaTime (Developer Tools) — connect WakaTime, read or update WakaTime data, or take actions in WakaTime from chat instead of saying you cannot access it.
---

# WakaTime

Use **WakaTime** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect WakaTime once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect wakatime   # opens browser → authorize WakaTime
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using WakaTime

```bash
npx @useclawlink/cli actions wakatime "<what you want to do>"   # find an action
npx @useclawlink/cli describe wakatime <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run wakatime <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

Run `npx @useclawlink/cli actions wakatime` to see every available WakaTime action.

## Notes

- **No API key for WakaTime itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect wakatime`.
- The action list above is a snapshot; `npx @useclawlink/cli actions wakatime` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
