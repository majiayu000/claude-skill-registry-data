---
name: github
description: GitHub integration for AI agents via ClawLink — browser login, no API key setup. Connect github through ClawLink's hosted setup. Use this skill when the user wants to work with GitHub (Developer Tools) — connect GitHub, read or update GitHub data, or take actions in GitHub from chat instead of saying you cannot access it.
---

# GitHub

Use **GitHub** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect GitHub once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect github   # opens browser → authorize GitHub
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using GitHub

```bash
npx @useclawlink/cli actions github "<what you want to do>"   # find an action
npx @useclawlink/cli describe github <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run github <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `github_abort_repository_migration` | Tool to abort a repository migration that is queued or in progress. Use when you need to cancel an ongoing migration operation. |
| `github_accept_repository_invitation` | Accepts a PENDING repository invitation that has been issued to the authenticated user. |
| `github_add_a_repository_collaborator` | Adds a GitHub user as a repository collaborator, or updates their permission if already a collaborator; `permission` applies to organization-owned repositories (personal ones default to 'push' and ignore this field), and an invitation may be created or permissions updated directly. |
| `github_add_app_access_restrictions` | Adds GitHub Apps to the list of apps allowed to push to a protected branch. The branch must already have protection rules with restrictions enabled. This endpoint only works for organization repositories, not personal repositories. Apps must be installed on the repository with 'contents' write permissions. |
| `github_add_assignees_to_an_issue` | Adds assignees to a GitHub issue. This action only adds users - it does not remove existing assignees. Changes are silently ignored if the authenticated user lacks push access to the repository. |
| `github_add_email_address_for_authenticated_user` | Adds one or more email addresses (which will be initially unverified) to the authenticated user's GitHub account; use this to associate new emails, noting an email verified for another account will error, while an existing email for the current user is accepted. |
| `github_add_field_to_user_project` | Tool to add a custom field to a user-owned GitHub Projects V2 project. Use when you need to add fields like status, priority, or custom data to organize project items. |
| `github_add_item_to_user_project` | Tool to add an issue or pull request to a user-owned GitHub project. Use when you need to add existing repository items to a project board. |
| `github_add_labels_to_an_issue` | Adds labels (provided in the request body) to a repository issue; labels that do not already exist are created. |
| `github_add_or_update_team_membership_for_user` | Adds a GitHub user to a team or updates their role (member or maintainer), inviting them to the organization if not already a member; idempotent, returning current details if no change is made. |
| `github_add_or_update_team_project_permissions` | Adds a classic project to a team or updates the team's permission on it. This endpoint grants or updates permissions for a team on a specific classic project (not Projects V2). The authenticated user must have admin permissions for the project. Both the team and project must belong to the same organization. Requirements: - The project must be a classic project (not GitHub Projects V2) - The authenticated user must have admin permissions on the project - The team and project must be in the same organization - Requires 'admin:org' scope for the authentication token Returns HTTP 204 No Content on success, 403 if project is not an org project, or 404 if the organization, team, or project is not found. |
| `github_add_or_update_team_repository_permissions` | Sets or updates a team's permission level for a repository within an organization; the team must be a member of the organization. |

## Notes

- **No API key for GitHub itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect github`.
- The action list above is a snapshot; `npx @useclawlink/cli actions github` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
