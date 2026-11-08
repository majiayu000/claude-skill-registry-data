---
name: sentry
description: Sentry integration for AI agents via ClawLink — browser login, no API key setup. Connect Sentry through ClawLink's hosted setup to monitor errors, manage projects, and inspect issues. Use this skill when the user wants to work with Sentry (Developer Tools) — connect Sentry, read or update Sentry data, or take actions in Sentry from chat instead of saying you cannot access it.
---

# Sentry

Use **Sentry** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Sentry once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect sentry   # opens browser → authorize Sentry
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Sentry

```bash
npx @useclawlink/cli actions sentry "<what you want to do>"   # find an action
npx @useclawlink/cli describe sentry <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run sentry <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `sentry_access_project_information` | Retrieve detailed information for a Sentry project |
| `sentry_fetch_alerts` | Retrieve a list of alerts for a Sentry organization |
| `sentry_fetch_issue_event_by_id` | Retrieve the latest or recommended event for a Sentry issue |
| `sentry_fetch_organization_alert_rules` | Retrieve active metric alert rules for an organization |
| `sentry_fetch_an_organizations_monitors` | Retrieve monitors for a Sentry organization |
| `sentry_add_a_symbol_source_to_a_project` | Add a custom symbol source to a Sentry project |
| `sentry_add_organization_member_via_email` | Invite a new member to a Sentry organization |
| `sentry_add_team_member_in_organization` | Add an existing member to a Sentry team |

## Notes

- **No API key for Sentry itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect sentry`.
- The action list above is a snapshot; `npx @useclawlink/cli actions sentry` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
