---
name: manus-api
description: "Manage tasks, projects, and other data through the Manus API; build OAuth2 Open Apps and third-party integrations; create Manus tasks programmatically; or install and use the official Manus API skill for services and workflows that need agentic capabilities."
compatibility: opencode
---

# Manus API Integration Guide

Use this skill when building or troubleshooting integrations that call the Manus API, automate Manus agents, retrieve generated results, manage projects/files/webhooks/connectors/agents/usage, request structured JSON outputs, publish websites created by Manus tasks, or implement OAuth2 authorization for third-party apps.

This file is the **routing and decision guide**. Keep implementation details in the embedded official docs under `docs/`. When a user asks for exact request bodies, response schemas, validation rules, rate limits, or endpoint-specific edge cases, open the relevant `docs/v2/*.mdx` file instead of relying on this overview.

**Version policy.** Use **API v2** for all new work. Use `docs/v1/` only when the user is maintaining an existing v1 integration, because v1 is deprecated.

**Base URL and authentication.** Send requests to `https://api.manus.ai`. Use `x-manus-api-key: <key>` for your own integrations and scripts, or `Authorization: Bearer <access_token>` for an Open App acting on behalf of a user. Successful responses use an `ok: true` envelope; failures use `ok: false` with `error.code`, `error.message`, and `request_id`. Standard OAuth tokens are scoped and cannot access full-access-only endpoints. Tokens issued to a `Trusted team client` or `Trusted public client` bypass scope restrictions. Open the endpoint document to confirm its supported authentication methods.

---

## 1. Documentation Routing

Prefer reading the smallest relevant document before answering detailed implementation questions. For endpoint-specific parameters, open `docs/v2/<endpoint>.mdx`; for the full schema, inspect `docs/v2/openapi_v2.json`. For task skill selection, read the `Message.enable_skills` and `Message.force_skills` field descriptions in that schema.

| User intent | Read first |
| --- | --- |
| Create, continue, stop, delete, or inspect tasks | `docs/v2/task-lifecycle.mdx`, then the relevant `task.*.mdx` file |
| Let the agent read earlier tasks from a new message | `docs/v2/task-references.mdx` |
| Require JSON output that an application can parse | `docs/v2/structured-output.mdx` |
| Publish or manage a website built by an agent | `docs/v2/website.mdx`, then the relevant `website.*.mdx` file |
| Upload, download, or reference user files | `docs/v2/file.upload.mdx`, `docs/v2/file.detail.mdx`, `docs/v2/file.delete.mdx` |
| List generated task artifacts | `docs/v2/artifacts.mdx`, then `docs/v2/artifact.list.mdx` |
| Configure real-time callbacks | `docs/v2/webhooks-overview.mdx`, `docs/v2/webhooks-security.mdx` |
| Add durable instructions/persona | `docs/v2/project.create.mdx`, `docs/v2/project.list.mdx` |
| Use connectors, skills, agents, or browser clients | `docs/v2/connectors.mdx`, `docs/v2/connector.list.mdx`, `docs/v2/skill.list.mdx`, `docs/v2/agents-overview.mdx`, `docs/v2/browser.onlineList.mdx` |
| Inspect usage, quotas, or logs | `docs/v2/usage.list.mdx`, `docs/v2/usage.teamStatistic.mdx`, `docs/v2/usage.teamLog.mdx`, `docs/v2/rate-limits.mdx` |
| Build an Open App or authorize on behalf of users | `docs/v2/open-app.mdx`, `docs/v2/authentication.mdx` |
| Send or read hidden application context | `docs/v2/hidden-application-context.mdx` |
| Resolve file or website references in task messages | `docs/v2/attachments.mdx` |
| Identify the user behind an API key or OAuth token | `docs/v2/user.me.mdx` |
| Install the website-hosted Manus API skill | `docs/v2/manus-api-skill.mdx` |

---

## 2. Endpoint Map

Use this map for orientation only. Open the endpoint file for concrete request/response details.

| Group | Purpose | Representative endpoints |
| --- | --- | --- |
| **User** | Identify the user associated with the current credential. | `user.me` |
| **Tasks** | Agent task lifecycle and multi-turn conversation. | `task.create`, `task.sendMessage`, `task.listMessages`, `task.confirmAction`, `task.stop` |
| **Projects** | Durable shared instructions and organization. | `project.create`, `project.list` |
| **Files** | Upload, inspect, download, and delete files used by tasks. | `file.upload`, `file.detail`, `file.delete` |
| **Artifacts** | List generated task outputs across the user's Library. | `artifact.list` |
| **Webhooks** | Production-grade task lifecycle notifications. | `webhook.create`, `webhook.list`, `webhook.delete`, `webhook.publicKey` |
| **Connectors and Skills** | Control third-party app access and skill availability. | `connector.list`, `skill.list` |
| **Agents** | List, inspect, and update custom IM agents. | `agent.list`, `agent.detail`, `agent.update` |
| **Usage** | Retrieve usage records and team statistics. | `usage.list`, `usage.teamStatistic`, `usage.teamLog` |
| **Website** | Inspect, publish, version, and update websites built by Manus tasks. | `website.status`, `website.listCheckpoints`, `website.publish`, `website.update` |

---

## 3. Core Integration Decisions

**Choose the right authentication method.** Use an API key for first-party integrations and scripts. Use OAuth2 when building an Open App that acts on behalf of users. Standard `team` clients are restricted by configured scopes: `create_task`, `manage_all_tasks`, `create_project`, `use_connectors`, and `use_my_browsers`. The `create_task` scope only exposes tasks created by the same client. Standard OAuth tokens can call `skill.list` with `create_task` or `manage_all_tasks`. They cannot access `agent.*`, `webhook.create`, `webhook.list`, `webhook.delete`, or `usage.*`, but can access `user.me`, `webhook.publicKey`, and `website.*` without an endpoint-specific scope. A `Trusted team client` or `Trusted public client` bypasses standard endpoint scope restrictions like an API key. Hidden text content is an additional `Trusted public client` capability. Open App creation and standard authorization require a Team account. `Trusted public client` access is partner-only. Read `docs/v2/open-app.mdx` before implementing OAuth2.

**Limit skill discovery by caller.** `skill.list` returns only skills owned by the current Open App for standard OAuth clients. API Keys receive the user's available skills; trusted OAuth clients also receive their App skills. Only API Keys and trusted OAuth clients can pass `project_id`. Listing a skill does not enable it. Read `docs/v2/skill.list.mdx` for the exact response scope.

**Resolve the authenticated user through the API.** Call `user.me` after OAuth token exchange when the integration needs the stable Manus user ID. Do not parse undocumented claims from the access token. The endpoint accepts API keys and OAuth tokens without an additional OAuth scope, and it does not modify user data.

**Choose the right task flow.** For a new independent job, call `task.create`. For an ongoing thread or conversation, store the `task_id` and call `task.sendMessage` on later turns. For direct messaging to the default IM agent, `task.sendMessage` supports the shortcut `task_id: "agent-default-main_task"`.

**Use projects for durable behavior.** If the integration needs a persistent persona, formatting rule, or reusable instruction, create or reuse a Project and pass `project_id` when creating tasks. Do not duplicate large system-style instructions into every user message if a project is the cleaner abstraction.

**Use webhooks for production result delivery.** Polling `task.listMessages` is acceptable for scripts and prototypes, but production systems should prefer webhooks and verify signatures with the webhook public key. Still implement idempotency and retries because webhook delivery can be repeated by clients or infrastructure.

**Do not treat the first stopped Agent status as task completion.** When polling, pair `task.listMessages` with `task.detail`. `status` and `agent_status` describe the main Agent, while optional `has_running_background_jobs` reports pending, queued, or running non-blocking background work. A `true` value means work remains; an omitted value is unknown and must not be treated as `false`. For both cases, stop at a bounded application deadline and report the completion state as unknown. Read `docs/v2/task-lifecycle.mdx` for the complete rule.

**Handle waiting states correctly.** If the agent asks the user a normal question, answer with `task.sendMessage`. For action confirmation, read `waiting_for_event_id` and `confirm_input_schema`. Fetch a missing tool target with `task.listMessages` using `verbose=true` and `start_event_id=waiting_for_event_id`, then review its `tool_used.params` and optional `tool_used.result`. Build the confirmation input according to the schema and submit it through `task.confirmAction`. Configuration and OAuth targets are not tool targets; do not use the start-event lookup for them because it returns `Event not found`. Use their dedicated UI or authorization flow. `confirmed: false` means the input was not consumed and the task remains waiting. Do not invent input for unrecognized event types; skip them by sending an ordinary message through `task.sendMessage`, or direct the user to open the task in Manus. Read `task-lifecycle.mdx` and `task.confirmAction.mdx` before automating confirmations.

**Pick agent profile intentionally.** `task.create` and `task.sendMessage` accept the stable `agent_profile` values `standard`, `lite`, and `max`, plus `max-medium`, `max-high`, `max-extra`, and `max-ultra` to choose a Max thinking level; deeper levels use more credits. Omitting the field on `task.create` defaults to `standard`; omitting it on `task.sendMessage` keeps the task's current profile and thinking level, while passing a value overrides the current and subsequent turns. Versioned profile names are compatibility aliases, not independent model selections. Use the endpoint docs for their accepted format.

**Attach tools through message fields.** Use `message.connectors` for connector IDs, `message.enable_skills` to control available skills, and `message.force_skills` when a skill must be invoked. Use `connector.list` and `skill.list` to discover IDs.

**Download uploaded attachments through `file.detail`.** After uploading bytes, use this endpoint to obtain a temporary GET link for content validation before creating a task. Download fields are optional. Links expire; read `docs/v2/file.detail.mdx` for availability and refresh rules.

**Follow artifact pagination until `has_more` is false.** Keep the user, credential scope, filters, and page size unchanged. Short or empty pages can still have a next cursor; retry transient failures with the same cursor. The server deduplicates IDs and Addon resources across one traversal. Apply a cursor replay as a replacement for that page. Cursors expire after 5 minutes idle or 15 minutes total; restart on an expired cursor. Deduplicate by `resource_uri` when present, otherwise by `id`, when merging separate traversals. Use the returned `type` for classification; do not infer it from the filename or platform. Read `docs/v2/artifacts.mdx` for categories and live-list semantics.

**Respect artifact source visibility.** Sources identify the creation task rather than the latest editor. A missing `source` does not imply UI creation. Credential-filtered lists may omit older artifacts without indexed source metadata. Restricted `create_task` OAuth clients always have an implicit filter for their own app; omitting source filters cannot recover those historical artifacts. Historical source metadata is not backfilled as part of this release.

**Resolve output attachments from message context.** `task.listMessages` returns original message content without rewriting file paths or Manus protocols. Render HTTP/HTTPS normally. Match file destinations to `attachments[].path`, and resolve `manus-webdev://<version_id>` through `website.listCheckpoints` for the same task. If the required context is absent or another non-HTTP protocol is unsupported, remove that link or image node in the client while preserving surrounding text. See `docs/v2/attachments.mdx`.

**Reference existing tasks to reuse prior work.** Pass `message.task_references` (task IDs) on `task.create` or `task.sendMessage` so the agent can browse those tasks' conversation and files on demand instead of you re-sending their content. References accumulate across turns and cannot be cleared. Access is checked when the agent reads, except that a `create_task`-scope OAuth client may reference only its own tasks. Read `docs/v2/task-references.mdx` for validation rules and limits.

**Hidden context requires a Trusted public client.** Only text parts may use `visibility: "hidden"`, and every create/send message must retain a valid visible part. User-facing history omits hidden text; a Trusted public client with task access can read it through `task.listMessages?verbose=true`. See `docs/v2/hidden-application-context.mdx` for the contract.

---

## 4. Structured Output Guidance

Use **Structured Output** when the integration needs machine-parseable JSON rather than human-facing prose. Before writing schemas or code, read `docs/v2/structured-output.mdx`.

Remember only the routing-level behavior here: pass `structured_output_schema` to `task.create` or `task.sendMessage`; extraction runs after the agent finishes; schemas are **arm once, fire once** and can be re-armed on later turns; results appear in `task.listMessages` as `structured_output_result` or in webhooks as `task_stopped.task_detail.structured_output`. Always check `success` before trusting `value`.

---

## 5. Operational Limits

Confirm limits in the relevant endpoint document before relying on them because they may change.

- User text is limited to approximately **5,000 estimated tokens per request**. This applies to v1 task prompts, OpenAI-compatible Responses input, and v2 `task.create` / `task.sendMessage`; multipart input is estimated across all text parts combined, while file parts do not count.
- `file.upload` accepts files up to **512 MB** and enforces **10 GB** total storage per account. Exceeding either limit returns `QuotaExceededError`. Its upload URL expires after **3 minutes**, uploaded files are deleted after **48 hours**, and executable or script file types are prohibited.
- A task attachment using `file_id` inherits the `file.upload` limit. Direct `file_url` and decoded `file_data` attachments are limited to **20 MB**; 20 MB of decoded data is approximately 26.7 MB of base64 text. There is no hard limit on the number of attachments per message.
- `message.task_references` accepts up to **20** task IDs per request on `task.create` and `task.sendMessage`; entries must be bare 22-character task IDs (a full task URL or the `agent-default-main_task` shortcut is rejected with `InvalidArgument`), and the cap is checked before duplicates are removed. References accumulate across turns; a task that accumulates more than 20 keeps the 20 most recently referenced.

---

## 6. Minimal Implementation Pattern

A typical closed-loop integration follows this sequence: upload files if needed with `file.upload`; create or reuse a project for durable instructions; call `task.create`; deliver results through webhooks or poll `task.listMessages`; continue with `task.sendMessage` if the conversation needs another turn; and use `task.confirmAction` only for explicit action confirmations.

For structured-output tasks, add a post-task step that reads either the `structured_output_result` event or the webhook `structured_output` field.

---

## References

Open these files for authoritative details:

| Topic | File |
| --- | --- |
| Full OpenAPI specification | `docs/v2/openapi_v2.json` |
| Task lifecycle and polling | `docs/v2/task-lifecycle.mdx`, `docs/v2/task.listMessages.mdx` |
| Task references | `docs/v2/task-references.mdx` |
| Task creation and follow-up turns | `docs/v2/task.create.mdx`, `docs/v2/task.sendMessage.mdx` |
| Structured output | `docs/v2/structured-output.mdx` |
| Website publishing | `docs/v2/website.mdx`, `docs/v2/website.status.mdx`, `docs/v2/website.publish.mdx`, `docs/v2/website.listCheckpoints.mdx`, `docs/v2/website.update.mdx` |
| Webhooks | `docs/v2/webhooks-overview.mdx`, `docs/v2/webhooks-security.mdx` |
| File upload and download | `docs/v2/file.upload.mdx`, `docs/v2/file.detail.mdx` |
| Generated artifacts | `docs/v2/artifacts.mdx`, `docs/v2/artifact.list.mdx` |
| Projects, connectors, skills, agents | `docs/v2/project.create.mdx`, `docs/v2/connector.list.mdx`, `docs/v2/skill.list.mdx`, `docs/v2/agents-overview.mdx` |
| OAuth2 and Open Apps | `docs/v2/open-app.mdx`, `docs/v2/authentication.mdx` |
| Hidden application context | `docs/v2/hidden-application-context.mdx` |
| Message attachments | `docs/v2/attachments.mdx` |
| Authenticated user identity | `docs/v2/user.me.mdx` |
| Website-hosted skill installation | `docs/v2/manus-api-skill.mdx` |
