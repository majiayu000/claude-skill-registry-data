---
name: conversation-export
description: This skill should be used when the user asks to "save the conversation", "export chat", "save chat history", "save our discussion", "export this conversation", "save dialogue", "save this session", "export as markdown", "export as HTML", "summarize and save", "append to chat", "continue saving", "search conversations", "find in chats", "list saved chats", "clean old chats", "export to notion", "export to feishu", "setup chat-saver", "configure chat-saver", "initialize chat-saver", "raw export", "export raw data", "export JSONL", "export session data", "export session file", "设置 chat-saver", "配置 chat-saver", "初始化 chat-saver", "保存对话", "导出对话", "保存聊天记录", "导出聊天", "保存会话", "追加对话", "搜索对话", "查找聊天", "列出对话", "清理对话", "导出到飞书", "导出到Notion", "导出原始数据", "原始导出", "导出 JSONL", "导出 session", "导出会话数据", or wants to preserve, manage, search, configure, or export Claude Code conversations.
version: 0.6.0
---

# Conversation Export

## Overview

Provide the ability to export Claude Code conversation content to structured documents. Support multiple output formats (Markdown, plain text, HTML) and content scopes (full conversation, summary).

## Settings Loading

Before any operation, load user settings from `.claude/chat-saver.local.md` following `references/settings-loading.md`.

Supported settings: `default_format`, `default_scope`, `save_dir`, `stop_hook`, `stop_hook_threshold`, `custom_header`, `custom_footer`. See `references/settings-schema.md` for full schema.

Users can run `/chat-saver:setup` to interactively initialize or update the configuration file.

## Output Formats

Three output formats are supported. For complete templates with full markup, see `references/format-templates.md`.

**IMPORTANT: Every exported document MUST include the plugin attribution footer.** The footer contains the plugin name "chat-saver" and the GitHub repository link. See `references/format-templates.md` for the exact footer text per format. Do NOT omit the footer under any circumstances unless the user has configured a `custom_footer` in settings.

### Markdown (default)

Use YAML frontmatter for metadata (date, project, working directory) to ensure compatibility with tools like Obsidian, Jekyll, and Hugo. Use heading-based structure with `## User` / `## Assistant` sections separated by `---`. Preserve code blocks with original language tags and inline code formatting.

### Plain Text

Use `[User]` / `[Assistant]` labels with `========` separators. Strip all Markdown formatting. Indent code blocks with 4 spaces. Clean and portable format.

### HTML

Generate self-contained HTML with embedded CSS. Use `.user` (blue tint) and `.assistant` (gray tint) styled containers. Wrap code in `<pre><code>` tags with dark theme. Escape HTML entities in code content.

## Content Scope

### Full Export

Export the entire conversation history as-is. Include all user messages and assistant responses. Preserve tool call results when they contain meaningful output. Omit internal tool call metadata (tool names, parameters) unless relevant to understanding.

### Summary Export

Generate a structured summary that captures the essential value:

1. **Topic** — One-line description of the conversation subject
2. **Key Decisions** — Bullet list of decisions made during the conversation
3. **Code Changes** — List of files modified/created with brief descriptions
4. **Insights** — Important findings, patterns discovered, or lessons learned
5. **Action Items** — Any follow-up tasks identified but not completed
6. **Key Code Snippets** — Important code blocks worth preserving (with file paths)

Target length: 20-30% of the original conversation.

## Selective Export

In addition to scope (full/summary), support filtering by conversation range:

- **Last N turns** (`--last N`) — Export only the most recent N turns
- **From keyword** (`--from "keyword"`) — Export from the first turn containing the keyword to the end

These filters apply before scope processing. A summary of the last 5 turns will first filter to 5 turns, then summarize those.

## Topic Extraction

To determine the conversation topic for the filename:

1. Identify the primary task or subject discussed
2. Extract 2-4 keywords in kebab-case
3. Prefer specific terms over generic ones

Examples:
- Auth implementation discussion → `auth-implementation`
- Bug fix for login timeout → `fix-login-timeout`
- Database schema design → `db-schema-design`
- Code review of payment module → `review-payment-module`

## File Naming

Generate filenames in the format: `YYYY-MM-DD-<topic>.<ext>`

- Date: Use current date from system
- Topic: Extracted from conversation (see above)
- Extension: `.md`, `.txt`, or `.html` based on format
- On filename collision: Append `-2`, `-3`, etc. (e.g., `2024-01-15-auth-implementation-2.md`)

## Save Location

Default save directory: `./chats/` relative to the current working directory (configurable via `save_dir` setting).

1. Check if the save directory exists; if not, create it
2. Check for filename collision; if exists, append counter suffix
3. Write the file to `<save_dir>/<filename>`
4. Report the full path to the user

Edge cases:
- Empty conversation: Inform the user there is nothing to save
- Directory creation failure: Report the error and suggest an alternative path

## Append Semantics

When using `--append` mode, the conversation is appended to an existing saved file instead of creating a new one:

1. **File Discovery** — Use Glob to search `<save_dir>/*-<topic>.*` for matching files
2. **Multiple Matches** — If multiple files match, use AskUserQuestion to let the user choose which file to append to
3. **No Match** — If no existing file matches, inform the user and fall back to creating a new file
4. **Continuation Separator** — Insert a format-appropriate separator before the appended content (see `references/format-templates.md` for separator templates)
5. **Content Generation** — Generate content the same way as a new save, but without the document header (title, metadata)
6. **Write Mode** — Read the existing file, concatenate separator + new content, then write the combined result

## Batch Management

### List Conversations

Scan the save directory and display all saved conversation files in a formatted table with date, topic, format, line count, and file size. Support sorting by date, size, or name, and filtering by format. After listing, offer follow-up actions (read, search, clean).

### Clean Conversations

Remove old or unwanted saved files with mandatory user confirmation. Support three cleaning modes:
- **By date** (`--before YYYY-MM-DD`) — Delete files older than a specified date
- **Keep recent** (`--keep N`) — Retain only the N most recent files
- **Manual selection** — Let the user pick files to delete interactively

Safety rules:
- Always confirm before deletion via AskUserQuestion
- Delete files individually (one `rm` command per file, no wildcards)
- Support `--dry-run` to preview without deleting

## Search Behavior

Search through saved conversation files using real-time Grep (no indexing). Support:
- **Keyword search** — Case-insensitive content matching with 2 lines of context
- **Date filtering** — Filter files by exact date (`--date`) or date range (`--from`/`--to`)
- **Result grouping** — Display matches grouped by file with context snippets
- **Follow-up** — After showing results, offer to read matching files in full

File filtering uses filename date prefixes for date-based searches, avoiding the need to open and parse each file.

## MCP Export

Export conversations to external platforms via MCP (Model Context Protocol) integration. **This plugin does not ship its own MCP servers** — it auto-detects servers already configured in the user's environment. See `references/mcp-export-guide.md` for setup instructions.

### Supported Platforms

- **Notion** — auto-detect tools matching `mcp__*notion*`
- **Feishu (飞书)** — auto-detect tools matching `mcp__*feishu*` or `mcp__*lark*`

### Export Flow

1. Auto-detect available MCP tools for the target platform
2. Generate conversation content in Markdown (universal intermediate format), **including the mandatory plugin attribution footer**
3. Create a new document on the target platform via detected MCP tools
4. Return the document URL to the user

### Fallback

If no matching MCP tools are detected, inform the user with setup instructions (add to project or global `.mcp.json`) and offer to save locally instead.

## Raw Export

Raw export reads conversation data directly from Claude Code's JSONL session files via bash/jq, bypassing the model entirely. This guarantees **complete and faithful** data export — no content is lost or rewritten.

**When to use raw export vs save-chat:**

| | `/raw-export` | `/save-chat` |
|---|---|---|
| Data source | JSONL session file | Model memory |
| Completeness | 100% of records | Limited by context window |
| Accuracy | Exact original data | May be rephrased |
| Content | Raw messages + tool calls | Curated conversation |
| Best for | Archiving, debugging, long sessions | Readable documentation, summaries |

Use `/chat-saver:raw-export` to invoke. Supports `--format` (md/html/jsonl/json), `--full` (include all record types), `--list` (browse sessions), and `--session <id>` (target specific session).

## Additional Resources

### Reference Files

For detailed format templates, content processing rules, and message filtering guidelines:
- **`references/format-templates.md`** — Complete templates for each output format with CSS, content processing rules, and message filtering guidelines
- **`references/settings-loading.md`** — Shared settings loading procedure used by all commands
- **`references/settings-schema.md`** — Settings schema and configuration file format
- **`references/mcp-export-guide.md`** — MCP export setup and usage guide for Notion and Feishu
