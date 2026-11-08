---
name: typeform
description: Typeform integration for AI agents via ClawLink — browser login, no API key setup. Connect Typeform through ClawLink's hosted setup to create and manage forms, collect responses, customize themes, and manage webhooks. Use this skill when the user wants to work with Typeform (Productivity) — connect Typeform, read or update Typeform data, or take actions in Typeform from chat instead of saying you cannot access it.
---

# Typeform

Use **Typeform** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Typeform once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect typeform   # opens browser → authorize Typeform
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Typeform

```bash
npx @useclawlink/cli actions typeform "<what you want to do>"   # find an action
npx @useclawlink/cli describe typeform <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run typeform <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `typeform_list_forms` | List all forms |
| `typeform_get_form` | Get form details and configuration |
| `typeform_create_form` | Create a new form |
| `typeform_update_form` | Update a form's configuration |
| `typeform_delete_form` | Delete a form |
| `typeform_get_form_responses` | Get form responses with filtering |
| `typeform_delete_responses` | Delete specific responses |
| `typeform_get_form_messages` | Get form UI messages |
| `typeform_update_form_messages` | Update form UI messages |
| `typeform_list_workspaces` | List all workspaces |
| `typeform_create_workspace` | Create a workspace |
| `typeform_list_themes` | List form themes |
| `typeform_create_theme` | Create a custom theme |
| `typeform_create_or_update_webhook` | Create or update a webhook |
| `typeform_list_webhooks` | List form webhooks |
| `typeform_get_about_me` | Get account info |

## Notes

- **No API key for Typeform itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect typeform`.
- The action list above is a snapshot; `npx @useclawlink/cli actions typeform` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
