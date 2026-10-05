---
name: build-work-memory
description: Guided first-run workflow for importing a user's existing work context into Friday Memory from local files, DingTalk documents/wiki, DingTalk AI minutes, and selected DingTalk data through dws. Use when the user wants to initialize Memory, connect work context, import DingTalk knowledge, seed Memory from documents or meetings, or prepare Memory for daily work.
---

# Build Work Memory

Import the user's existing work context into Friday Memory.

Run with Codex, Friday Memory MCP, and the `dws` DingTalk Workspace CLI. Do not require the `memory-connector` repository, Neo4j, Friday admin UI, local backend services, or project-local scripts. Use local file access only when the user explicitly chooses local documents.

## Preflight

Before asking import questions, verify:

- Friday Memory MCP is available and exposes `document_upload`.
- `dws` is installed and authenticated.

If Friday Memory MCP is missing, tell the user to open `https://friday.stardust.ai`, sign in, generate the Memory MCP / Agent install command, and send that command to Codex. Do not invent install commands or tokens.

If `dws` is missing, ask the user for the approved installation source or internal installer. Do not invent a download URL. After installation, verify with:

```bash
dws --help
dws profile list --format json
```

## Experience Contract

Do not ask the user for a project or topic first. This skill is for first-time work-context initialization.

Do not default-scan anything. Only import ranges the user explicitly describes.

Do not require per-item confirmation. Collect scope, summarize the planned read and upload range, and ask once for explicit confirmation before reading private content or uploading to Memory.

Do not expose `graph_id`, `user_id`, `document_upload`, `ingest_mode`, entity extraction, relation extraction, or internal queue details to the user.

Do not run recall validation. Graph extraction is asynchronous and may take time.

## Opening Message

Start with:

```text
我会帮你把已有工作上下文导入 Memory。流程分 4 步：

1. 本地文档
2. 钉钉知识库 / 钉钉文档
3. 钉钉 AI 听记 / 会议纪要
4. 其他钉钉数据

每一步我都会问你想导入的范围。收集完范围后，我会在正式读取和上传前汇总一次；你确认后我再执行。不会默认扫描你的全部资料。
```

## Scope Collection

Ask in order:

1. Local documents: paths, folders, file types, keywords, or time range.
2. DingTalk documents/wiki: workspace, folder, document links, keywords, owner, or time range.
3. DingTalk AI minutes: meeting keywords, time range, participants, links, or IDs.
4. Other DingTalk data: ask whether any specific category and range should be included.

For other DingTalk data, present the supported categories:

- AI search / people lookup
- AI tables
- Attendance
- Calendar
- Chat / IM
- Contacts / departments
- DING messages
- DingTalk drive
- Live sessions
- Mail
- OA approvals
- Reports / daily or weekly logs
- Online sheets
- Todos
- Wiki spaces and members
- Developer docs / error-code docs
- PAT / authorization diagnostics, excluding tokens or secrets

If the user gives an overly broad range, ask them to narrow it before reading. Examples: all company wiki, all meetings, all chats, all drive files, all data from a full year.

## Confirmation

After collecting scope, summarize:

```text
我将按以下范围读取资料并导入 Memory：

- 本地文档：...
- 钉钉知识库 / 文档：...
- 钉钉 AI 听记：...
- 其他钉钉数据：...

请确认是否开始读取并上传这些范围内的内容。
```

Proceed only after the user confirms.

## DingTalk Rules

Use only `dws` for DingTalk data. Use `--format json`.

If command syntax is uncertain, inspect it first with `dws <service> --help` or `dws schema <path>`.

Route sources through:

- `dws doc` for DingTalk documents
- `dws wiki` for wiki spaces/containers
- `dws minutes` for AI minutes
- `dws chat`, `calendar`, `mail`, `drive`, `report`, `todo`, `sheet`, `aitable`, `contact`, `aisearch` for selected optional data

## Memory Ingest Format

Convert every imported source into Markdown before upload. Add provenance at the top:

```md
# <title>

source_type: <local_file | dingtalk_doc | dingtalk_wiki | dingtalk_minutes | dingtalk_chat | dingtalk_calendar | dingtalk_mail | dingtalk_drive | dingtalk_report | dingtalk_todo | dingtalk_sheet | dingtalk_aitable | dingtalk_contact | other>
source_id: <id if available>
source_url: <url if available>
source_path: <folder/wiki/path if available>
source_time: <original created/updated/meeting time if available>
participants: <participants if available>
imported_from: <local | dws doc | dws wiki | dws minutes | ...>

---

<content>
```

Use original source time for `uploaded_at` when available. Add a concise `summary` and `background` when possible.

Split long sources by natural boundaries: headings, wiki sections, agenda items, speaker/time segments, dates, table views, or logical chapters. Keep provenance in every split part.

## Upload Rules

For each prepared document, call Friday Memory MCP `document_upload` with:

- `filename`
- `content_base64`
- `mime_type`
- `uploaded_at`
- `source_kind`: `system_auto_fetch` for DingTalk, `user_upload` for local files
- `summary`
- `background`
- `ingest_mode`: `graph`
- `wait_for_processing`: `false`

Never pass `user_id`, `graph_id`, or `graph_ids`.

Treat upload success as "submitted to Memory processing," not "fully extracted."

## Final Response

End with:

```text
已提交到 Memory：

- 本地文档：N 份
- 钉钉知识库 / 文档：N 份
- 钉钉 AI 听记：N 份
- 其他钉钉数据：N 份

失败：N 项
后台处理中：N 项

这些资料会继续在后台抽取实体和关系。大型资料可能需要一段时间后才能完整召回。
```

List failed items with short reasons and the next retry action.
