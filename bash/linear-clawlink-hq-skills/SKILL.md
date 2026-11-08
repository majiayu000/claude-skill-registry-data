---
name: linear
description: Linear integration for AI agents via ClawLink — browser login, no API key setup. Connect linear through ClawLink's hosted setup. Use this skill when the user wants to work with Linear (Developer Tools) — connect Linear, read or update Linear data, or take actions in Linear from chat instead of saying you cannot access it.
---

# Linear

Use **Linear** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Linear once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect linear   # opens browser → authorize Linear
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Linear

```bash
npx @useclawlink/cli actions linear "<what you want to do>"   # find an action
npx @useclawlink/cli describe linear <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run linear <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `linear_create_attachment` | Creates a new attachment and associates it with a specific, existing Linear issue. |
| `linear_create_comment_reaction` | Tool to add a reaction to an existing Linear comment. Use when you want to programmatically react to a comment on an issue. |
| `linear_create_linear_comment` | Creates a new comment on a specified Linear issue. This action modifies shared workspace data and is not reversible — confirm the target issue and comment content before executing. |
| `linear_create_linear_issue` | Creates a new issue in a specified Linear project and team, requiring team_id and title, and allowing optional properties like description, assignee, state, priority, cycle, and due date. All UUID parameters (state_id, assignee_id, cycle_id, label_ids, project_id) must belong to the same team as team_id. The created issue's id is returned in data.id — capture it for use as parent_id in sub-issues or follow-up operations. No template_id field exists; expand templates manually into title and description before calling. |
| `linear_create_linear_issue_relation` | Create a relationship between two Linear issues using the issueRelationCreate mutation. Use this to establish connections like 'blocks', 'duplicate', or 'related' between issues. |
| `linear_create_linear_label` | Creates a new label in Linear for a specified team, used to categorize and organize issues. Label names must be unique within each team. If a label with the same name already exists, the existing label will be returned. Both new and existing labels return the same object structure; check the label's `createdAt` or compare IDs to determine if creation occurred. |
| `linear_create_linear_project` | Creates a new Linear project with specified name and team associations. |
| `linear_create_project_milestone` | Tool to create a project milestone in Linear with a name and optional target date and sort order. Use when you need to add milestones to track progress within a project. |
| `linear_create_project_update` | Tool to create a project status update post for a Linear project. Use when you need to post progress updates, status reports, or announcements for a project. |
| `linear_delete_linear_issue` | Archives an existing Linear issue by its ID, which is Linear's standard way of deleting issues; the operation is idempotent. Archiving is permanent with no built-in undo — confirm the issue identifier and title with the user before executing, especially in bulk operations. |
| `linear_get_attachment` | Downloads a specific attachment from a Linear issue; the `file_name` must include the correct file extension. |
| `linear_get_current_user` | Gets the currently authenticated user's ID, name, email, and other profile information — this is the account behind the API token, which may be a bot or service account rather than a human user. Use the returned `id` field (nested under `data.viewer`) for downstream Linear operations requiring user ID filtering. To search or compare other workspace members, use LINEAR_LIST_LINEAR_USERS instead. |

## Notes

- **No API key for Linear itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect linear`.
- The action list above is a snapshot; `npx @useclawlink/cli actions linear` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
