---
name: calendly
description: Calendly integration for AI agents via ClawLink — browser login, no API key setup. Connect Calendly through ClawLink's hosted setup to inspect events, invitees, availability schedules, webhook subscriptions, and create single-use scheduling links. Use this skill when the user wants to work with Calendly (Productivity) — connect Calendly, read or update Calendly data, or take actions in Calendly from chat instead of saying you cannot access it.
---

# Calendly

Use **Calendly** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Calendly once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect calendly   # opens browser → authorize Calendly
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Calendly

```bash
npx @useclawlink/cli actions calendly "<what you want to do>"   # find an action
npx @useclawlink/cli describe calendly <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run calendly <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `calendly_get_event` | Get a Calendly event by ID or URL |
| `calendly_list_events` | List Calendly scheduled events |
| `calendly_list_event_invitees` | List invitees for a Calendly event |
| `calendly_list_user_availability_schedules` | List Calendly availability schedules |
| `calendly_list_webhook_subscriptions` | List Calendly webhook subscriptions |
| `calendly_create_scheduling_link` | Create a single-use Calendly scheduling link |
| `calendly_create_invitee_no_show` | Mark a Calendly invitee as a no-show |

## Notes

- **No API key for Calendly itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect calendly`.
- The action list above is a snapshot; `npx @useclawlink/cli actions calendly` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
