---
name: tally
description: Tally integration for AI agents via ClawLink — browser login, no API key setup. Connect tally through ClawLink's hosted setup. Use this skill when the user wants to work with Tally (Productivity) — connect Tally, read or update Tally data, or take actions in Tally from chat instead of saying you cannot access it.
---

# Tally

Use **Tally** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Tally once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect tally   # opens browser → authorize Tally
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Tally

```bash
npx @useclawlink/cli actions tally "<what you want to do>"   # find an action
npx @useclawlink/cli describe tally <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run tally <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `tally_create_form` | Tool to create a new form. Use after preparing block definitions and optional settings. |
| `tally_create_webhook` | Tool to create a new webhook for a form. Use after confirming you have the form ID and the callback URL. |
| `tally_delete_form` | Tool to delete a specific form identified by its ID. Use after confirming the form should be permanently removed. |
| `tally_delete_webhook` | Tool to delete a specific webhook. Use after confirming the webhook ID. |
| `tally_get_form_details` | Tool to retrieve details of a specific form. Use when you need comprehensive form metadata by ID. Use after confirming the form ID to fetch its full configuration, blocks, and stats. |
| `tally_get_form_responses` | Tool to retrieve the responses of a specific form. Use after confirming the form ID and when paginated data is needed. |
| `tally_get_user_info` | Tool to retrieve information about the authenticated user. Use when you need to confirm account-level details before proceeding. Returns account/workspace context only — not form-level access; follow up with TALLY_LIST_FORMS to verify form access. Confirm the returned workspace and user context match the intended account before creating or modifying resources, as acting on the wrong context places resources in an unintended account. Do not expose sensitive response fields (e.g., tokens) in user-visible output. |
| `tally_get_webhook_events` | Tool to list events associated with a specific webhook. Use when you need to inspect delivery history after creating or listing a webhook. |
| `tally_get_workspace` | Tool to retrieve a single workspace by its ID with associated members. Use when you need to get detailed information about a specific workspace. |
| `tally_list_form_questions` | Tool to retrieve all questions from a specific form. Use when you need to list all questions and their structure after obtaining the form ID. |
| `tally_list_forms` | Tool to retrieve a paginated list of forms. Use when you need to list all forms accessible to the authenticated user. |
| `tally_list_organization_invites` | Tool to retrieve all pending invites in your organization. Use when you need to view or manage organization invitation status. |

## Notes

- **No API key for Tally itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect tally`.
- The action list above is a snapshot; `npx @useclawlink/cli actions tally` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
