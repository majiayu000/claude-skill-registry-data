---
name: mem0
description: Mem0 integration for AI agents via ClawLink — browser login, no API key setup. Connect mem0 through ClawLink's hosted setup. Use this skill when the user wants to work with Mem0 (AI & ML) — connect Mem0, read or update Mem0 data, or take actions in Mem0 from chat instead of saying you cannot access it.
---

# Mem0

Use **Mem0** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Mem0 once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect mem0   # opens browser → authorize Mem0
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Mem0

```bash
npx @useclawlink/cli actions mem0 "<what you want to do>"   # find an action
npx @useclawlink/cli describe mem0 <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run mem0 <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `mem0_add_member_to_project` | Adds an existing user to a project (identified by `project_id` within organization `org_id`), assigning a valid system role. |
| `mem0_add_new_memory_records` | Stores new memory records from a list of messages, optionally inferring structured content; requires association via `agent_id`, `user_id`, `app_id`, or `run_id`. |
| `mem0_add_organization_member` | Adds a new member, who must be a registered user, to an organization, assigning them a specific role. |
| `mem0_create_a_new_agent` | Creates a new agent with a unique `agent_id` and an optional `name`; additional metadata may be assigned by the system. |
| `mem0_create_a_new_agent_run` | Creates a new agent run in the mem0.ai system. |
| `mem0_create_a_new_application` | Creates a new application, allowing metadata to be passed in the request body (not an explicit field in this action's request model); ensure `app_id` is unique to avoid potential errors or unintended updates. |
| `mem0_create_a_new_organization_entry` | Creates a new organization entry using the provided name and returns its details. |
| `mem0_create_a_new_user` | Creates a new user with the specified unique `user_id` and supports associating `metadata` (not part of the request schema fields). |
| `mem0_create_memory_entry` | Lists/searches existing memory entries with filtering and pagination; critically, this action retrieves memories and does *not* create new ones, despite its name. |
| `mem0_create_project` | Creates a new project with a given name within an organization that must already exist. |
| `mem0_create_webhook` | Creates a new webhook for a specific project to receive real-time notifications. Use when you need to set up event-driven integrations that trigger on memory operations. |
| `mem0_delete_a_specific_memory_by_id` | Permanently deletes a specific memory by its unique ID; ensure the `memory_id` exists as this operation is irreversible. |

## Notes

- **No API key for Mem0 itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect mem0`.
- The action list above is a snapshot; `npx @useclawlink/cli actions mem0` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
