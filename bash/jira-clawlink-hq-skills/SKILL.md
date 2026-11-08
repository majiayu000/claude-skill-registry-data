---
name: jira
description: Jira integration for AI agents via ClawLink — browser login, no API key setup. Connect Jira through ClawLink's hosted setup to create and manage issues, projects, sprints, and workflows. Use this skill when the user wants to work with Jira (Developer Tools) — connect Jira, read or update Jira data, or take actions in Jira from chat instead of saying you cannot access it.
---

# Jira

Use **Jira** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Jira once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect jira   # opens browser → authorize Jira
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Jira

```bash
npx @useclawlink/cli actions jira "<what you want to do>"   # find an action
npx @useclawlink/cli describe jira <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run jira <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `jira_fetch_bulk_issues` | Bulk fetch multiple Jira issues by IDs or keys |
| `jira_find_users2` | Find users in Jira by query or account ID |
| `jira_get_all_groups` | Retrieve all groups from the Jira instance |
| `jira_check_permissions` | Check user permissions for Jira operations |
| `jira_add_attachment` | Upload and attach a file to a Jira issue |
| `jira_add_comment` | Add a comment to an existing Jira issue |
| `jira_add_users_to_project_role` | Add users to a Jira project role |
| `jira_add_user_to_group` | Add a user to a Jira group |
| `jira_create_jql_autocompletedata` | Retrieve JQL autocomplete reference data |
| `jira_evaluate_jira_expression` | Evaluate Jira expressions using the enhanced search API |

## Notes

- **No API key for Jira itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect jira`.
- The action list above is a snapshot; `npx @useclawlink/cli actions jira` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
