---
name: manus-tasks
description: "Use the Manus Tasks Addon inside Manus to create, update and find tasks, read task history, send task messages, create or update Projects, and obtain a temporary Manus API key for scripts."
compatibility: opencode
---

# Manus Tasks Addon

Use the MCP server named exactly `manus-tasks` in a Manus chat, on cloud Sandbox or Manus Desktop. This skill describes the addon's tools and temporary script access, not how to configure API keys or OAuth for external integrations.

## Choose the execution path

The eight task/Project management tools below need no user confirmation or `get_access` call and do not install API credentials. Use each tool's input schema. For supported script-based HTTP operations, call `get_access` first; its first call asks the user to allow script API access for this chat. Wait for that decision rather than asking for a second verbal confirmation. Denial of script access does not disable the direct tools, but never use them to contradict a refusal of the underlying action.

Only the main conversation agent may call these tools, including `get_access`. Child/workflow subagents and detached executions must return the API work to their main-session coordinator. A tool error is not success. If script approval is pending or rejected, do not read or use credentials or retry automatically. An older host reporting an unsupported direct tool needs updating; do not automatically request script access as a fallback.

## Task management

| User intent | Direct MCP tool | Workflow |
| --- | --- | --- |
| Find tasks or inspect a Project's tasks | `list_tasks` | For a specific Project, pass both `scope: "project"` and `project_id`; retain returned task IDs for later calls. |
| Read another task's conversation or results | `list_task_messages` | Use its `task_id`; read relevant history before summarizing results or sending a context-dependent follow-up. |
| Continue a task or send it instructions | `send_task_message` | Send `message.content` to the existing `task_id`; do not create a replacement task. |
| Rename a task or change its visibility/sharing | `update_task` | Omit `task_id` for the current task; use an explicit ID for another task. Provide only the requested settings. |
| Start an independent job | `create_task` | Supply a self-contained first message; omit `project_id` to inherit the current Project; set an ID or an empty string only to override it. |

Resolve a task from an explicit ID or `list_tasks`; if several tasks match, ask which one before sending a message. Follow `next_cursor` when the requested task/history is not on the first page. A partial page is not the entire history, and an accepted message does not mean the task has finished.

**Continue in the current task by default.** Create a separate user-visible task only when the user explicitly asks for one or accepts a new-task suggestion; do not ask for another confirmation after that. A request to continue, implement, test, deploy, or work in parallel does not request a new task. Keep the requested outcome and its necessary follow-up work here, using internal subagents/workflow where appropriate. Standalone value, duration, complexity, parallelism, a new phase, or easier progress tracking alone do not justify creating or suggesting another task. Proactively suggest one only when the conversation establishes a separate user goal outside the current request and a concrete need to manage it independently; otherwise continue here or finish without a suggestion.

New tasks default to the current device, working directory, Project and agent profile, including the Max thinking level. Set `agent_profile` only when the user asks for a mode: `lite`, `standard`, `max`, or `max-medium` / `max-high` / `max-extra` / `max-ultra` for a Max thinking level. They also inherit the current Skill, Connector and Addon selection, including connector_mcp Addons and disabled selections. Explicit nonempty message.connectors replaces the Connector/Addon selection; message.enable_skills replaces the Skill selection; message.force_skills augments it. Credentials are resolved again for the new task. Omit `execution_environment` unless the user specifies another target. `kind: "device"` requires an inherited device or an explicit authorized `device_id`. `working_directory` also requires a device; if the current task uses a sandbox, supply `device_id` as well. Its optional `device_id` and `working_directory` override the selection; changing devices without a directory uses the target device's default workspace, never the source machine's path. `kind: "sandbox"` selects a fresh sandbox and cannot be combined with device or directory fields. Tasks on the same device and directory share its files; no Git worktree is created automatically. A new task remains independent and receives its own runtime credentials. Report unavailable environments or permissions; do not silently switch devices.

For `create_task`, omit `title` so Manus generates it unless the user explicitly supplies a title. Leave `hide_in_task_list` unset or false unless the user asks to hide it. The new task does not inherit this chat's full conversation or copy files from an isolated sandbox: put the needed context in the first message or use supported `message.task_references`. Report the returned task ID/link after success; by default, do not poll or wait for it. After a timeout with an unknown outcome, inspect task/history results before retrying a create or send that may already have succeeded.

## Project management

A Manus Project groups tasks with reusable instructions and shared connector/skill defaults; it is not a webdev project or a separate agent identity. Use a task for one-off work and a Project for persistent behavior shared by multiple tasks.

| User intent | Direct MCP tool | Workflow |
| --- | --- | --- |
| Find or reuse a Project | `list_projects` | Takes no arguments and returns all accessible project summaries; use the returned ID, not a guessed name-derived ID. |
| Create a Project | `create_project` | Provide `name` and optional `instruction`; use `update_project` for other shared settings. |
| Change a Project | `update_project` | Provide `project_id` and only the settings the user wants to change. |

For work in a named Project, find it with `list_projects`. To list its tasks, call `list_tasks` with `{"scope":"project","project_id":"<returned ID>"}`: `project_id` alone is ignored because the default scope is `all`. For `create_task`, pass the Project ID when overriding the current Project. Ask for a choice when the target is ambiguous. If the user wants a new Project, create it and use the returned ID for subsequent tasks. Creating a Project does not create a task, and creating a task inherits the current Project when `project_id` is omitted; an explicit empty string creates it outside a Project.

**Update shared settings deliberately.** Use `name` or `description` for organization, `instruction` for persistent behavior, and `connector_ids` / `skill_ids` for shared resource defaults. A one-task preference belongs in that task's message, not shared Project settings. Omitted or null fields stay unchanged; empty text clears a description/instruction, and empty resource arrays clear those defaults.

Resource arrays replace the complete set, not append/remove individual IDs. Project summaries do not provide the full configuration. Before adding/removing a resource, obtain the current set through `project.detail` if script access is already available, or from the user; do not guess or drop existing IDs. A user-specified complete replacement does not require reading unrelated settings. Do not request script access merely to use a direct MCP tool.

Connector assignment does not grant authorization. Personal skills must first be copied/imported into the Project. Clearing defaults does not delete skill content or member overrides. Report permission or resource failures rather than silently dropping requested resources.

## Script API access

Call `get_access` with `{}`. After it returns `ready: true`, read `MANUS_API_BASE_URL`, `MANUS_API_KEY`, and `MANUS_API_KEY_EXPIRES_AT` from the terminal environment without printing their values. If it returns `ready: false`, stop and report that script access is unavailable. Send HTTP requests to the injected base URL with the key in the `x-sandbox-token` header; do not hardcode a production or dev endpoint. Supported HTTP operations, including `task.create` and `agent.create`, need no per-create confirmation.

The host installs the temporary key before reporting readiness, in both cloud Sandbox and Manus Desktop. On Desktop, use the terminal bound to this chat's workspace; credentials are not installed in global environment variables or shared with other chats. The host manages a session environment file named `env`; the terminal loads updated credentials before the next command without restarting the shell. Do not locate, source, or edit this file yourself. Already-running processes keep their inherited environment.

On older Desktop hosts that report a terminal restart after a credential change, restore shell-local setup and retry the unexecuted command. Do not call `get_access` again just to recover that terminal.

Availability: session/project context requires the updated Manus Tasks addon and host to be deployed together. Older installations may omit these fields. Missing `project_id` is not the same as `null`; if a required ID is absent, report that context is unavailable and request an updated installation or an explicit ID—never guess it.

`get_access` also returns `session_id` and `project_id` for the current chat. These values come from the host; `project_id` is `null` when the chat is not in a Manus Project. It is not a webdev project ID. Use these returned fields when an operation needs the current chat or project; do not infer them from token contents, file paths, or terminal session names. They describe the current context, not additional authorization. New tasks inherit the current Project by default.

Access tokens expire after 30 minutes. `MANUS_API_KEY_EXPIRES_AT` is a Unix timestamp in seconds. Call `get_access` again shortly before expiry, after the environment has lost its API credentials (not merely restarted a shell), or once after an API authentication failure. The authorization is remembered for this session, so refreshing or reacquiring access does not require another confirmation. A new session requires its own authorization. If access is rejected, stop the current attempt and do not retry unless the user asks again. If a refresh fails, stop and report the failure.

The temporary API key supports only these HTTP endpoints:

- Tasks: `task.create`, `task.list`, `task.sendMessage`, `task.listMessages`, `task.stop`
- Agents: `agent.create`, `agent.list`, `agent.detail`
- Projects: `project.detail`, `project.update`

Stay within these endpoints. Access approval covers API use in this chat, but does not expand the user's requested scope. Before creating a reusable agent, sending, or stopping a task, ensure the current request calls for it. The Task management lifecycle guidance above also applies to script-created tasks. Never print, echo, log, or repeat credential values.

For a task waiting on a normal question, use `send_task_message`. An action confirmation is different: `task.confirmAction` is not available through this addon, so ask the user to complete it in Manus. File upload, connector/skill discovery, webhooks, and other unlisted HTTP operations are not enabled by the temporary key.

## API endpoint details

MCP input schemas are the authority for direct tool arguments; using those tools does not require the `manus-api` skill. For script-based API v2 request/response schemas and integration guidance, use the separate `manus-api` skill when available. This addon does not bundle or install it. If it is unavailable and required endpoint details are unknown, report the missing reference rather than inventing parameters.

When using a temporary key from `get_access`, keep this skill's injected base URL, `x-sandbox-token` header, expiry, and endpoint limits. The API skill's external API-key/OAuth examples and broader endpoint catalog do not change this runtime access contract or authorize additional operations.
