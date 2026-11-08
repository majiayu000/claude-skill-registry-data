---
name: gitlab
description: GitLab integration for AI agents via ClawLink — browser login, no API key setup. Connect gitlab through ClawLink's hosted setup. Use this skill when the user wants to work with GitLab (Developer Tools) — connect GitLab, read or update GitLab data, or take actions in GitLab from chat instead of saying you cannot access it.
---

# GitLab

Use **GitLab** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect GitLab once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect gitlab   # opens browser → authorize GitLab
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using GitLab

```bash
npx @useclawlink/cli actions gitlab "<what you want to do>"   # find an action
npx @useclawlink/cli describe gitlab <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run gitlab <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `gitlab_archive_project` | Tool to archive a project. Use when you need to mark a project read-only after finishing active development. Call after confirming no further changes are required. |
| `gitlab_create_group` | Tool to create a new group in GitLab. Use when you need to establish a new group for projects or collaboration. |
| `gitlab_create_project` | Tool to create a new project in GitLab. Implements POST /projects endpoint. |
| `gitlab_create_project_issue` | Tool to create a new issue in a GitLab project. Use when you need to report a bug, request a feature, or track a task within a specific project. |
| `gitlab_create_repository_branch` | Tool to create a new branch in a project. Use when you need to create a new branch from an existing branch or a specific commit in a GitLab project. |
| `gitlab_delete_project` | Tool to delete a GitLab project by its ID. Use when you need to remove a project, either by marking it for later deletion or deleting it immediately. |
| `gitlab_download_project_avatar` | Tool to download a project's avatar image. Use when you need the raw avatar bytes after confirming the project exists. |
| `gitlab_erase_job` | Tool to erase the content of a specified job within a project. Use when you need to remove job artifacts and logs. |
| `gitlab_get_commit_refs` | Tool to get all references (branches or tags) a commit is pushed to. Use when you need to find out which branches or tags a specific commit belongs to in a GitLab project. |
| `gitlab_get_commit_sequence` | Tool to get the sequence number of a commit in a project by following parent links from the given commit. Use when you need to determine the order of a commit in the project's history. |
| `gitlab_get_group` | Tool to retrieve information about a specific group by its ID. Use when you need to get details of a GitLab group. |
| `gitlab_get_group_member` | Tool to retrieve details for a specific group member. Use when you need to fetch membership information for a user in a group after you know both group ID and user ID. |

## Notes

- **No API key for GitLab itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect gitlab`.
- The action list above is a snapshot; `npx @useclawlink/cli actions gitlab` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
