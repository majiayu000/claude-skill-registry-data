---
name: jotform
description: Jotform integration for AI agents via ClawLink — browser login, no API key setup. Connect jotform through ClawLink's hosted setup. Use this skill when the user wants to work with Jotform (Productivity) — connect Jotform, read or update Jotform data, or take actions in Jotform from chat instead of saying you cannot access it.
---

# Jotform

Use **Jotform** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Jotform once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect jotform   # opens browser → authorize Jotform
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Jotform

```bash
npx @useclawlink/cli actions jotform "<what you want to do>"   # find an action
npx @useclawlink/cli describe jotform <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run jotform <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `jotform_clone_form` | Tool to clone a single form in Jotform. Creates a complete copy of the form with all its questions and settings. Use when you need to duplicate an existing form. |
| `jotform_create_label` | Tool to create a new label for organizing forms in Jotform. Use when you need to categorize or group forms with a named label. |
| `jotform_delete_label` | Tool to delete a label along with all its sublabels. Use when you need to remove a label from the account. |
| `jotform_get_label` | Tool to retrieve details of a label by its ID, including name and color. Use when you need to fetch information about a specific label. |
| `jotform_get_label_resources` | Tool to get a list of assets (forms) in a label and their associated information. Use when you need to retrieve forms organized under a specific label. |
| `jotform_get_system_plan` | Tool to retrieve details of a specific system plan. Use when you need to check limits and pricing of a plan. |
| `jotform_get_user_details` | Tool to retrieve details of the authenticated user, including account and usage info. Use after confirming valid API key. |
| `jotform_get_user_folders` | Tool to retrieve a list of labels (folders replacement) for the authenticated user. Uses the GET /user/labels endpoint per Jotform's migration from folders to labels. |
| `jotform_get_user_forms` | Tool to retrieve a list of forms created by the authenticated user. Use after setting up API key authentication. |
| `jotform_get_user_history` | Tool to fetch user activity history records. Use when auditing or filtering user actions by type or date. |
| `jotform_get_user_reports` | Tool to retrieve list of report URLs for all forms in the account. Includes Excel, CSV, printable charts, and embeddable HTML tables. |
| `jotform_get_user_settings` | Tool to retrieve the settings of the authenticated user. Use after confirming a valid API key. |

## Notes

- **No API key for Jotform itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect jotform`.
- The action list above is a snapshot; `npx @useclawlink/cli actions jotform` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
