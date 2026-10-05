---
name: decisions-composio
description: Use Composio Connect MCP (Tool Router) for authenticated SaaS actions — Gmail, Slack, Notion, Jira, Linear, GitHub, and 1000+ other apps. Rube is deprecated; do not use it.
---

# Composio Connect MCP

**Rube is deprecated and off the market.** Decisions only merges **Composio Connect** at `https://connect.composio.dev/mcp`.

Composio exposes SaaS tools over MCP via meta-tools that search, connect, and execute across apps.

## Workflow

1. **COMPOSIO_SEARCH_TOOLS** — discover tools + plan hints for the request.
2. **COMPOSIO_MANAGE_CONNECTIONS** — if a toolkit has no active connection; show the auth link and wait.
3. **COMPOSIO_CREATE_PLAN** — for medium/hard multi-app workflows (when search says to).
4. **COMPOSIO_MULTI_EXECUTE_TOOL** — run independent tool calls in parallel (up to limits).
5. **COMPOSIO_REMOTE_WORKBENCH** / **COMPOSIO_REMOTE_BASH_TOOL** — only when output is in remote files or bulk scripting is needed.

Never invent toolkit slugs or tool names — only use values returned by search.

## API key

Set your Composio project API key in **Decisions → Settings → API Keys → Composio**. Decisions encrypts it and injects it into the `composio` MCP entry on harness recalibrate.

## Do not use Composio for

| Job | Use instead |
|-----|-------------|
| Public Twitter/Reddit/YouTube research | `decisions-agent-reach` |
| Library/framework API docs | `context7` / `docs-lookup` |
| YouTube download / subtitles | `decisions-yt-dlp` or workflow `ytdlp` |
| UI reference screens | `decisions-design-references` |
| Browser QA in repo | `decisions-playwright` |

## Do not use

- **Rube** (`rube.app`, `rube.composio.dev`, `@composio/rube-mcp`) — deprecated; removed from Composio's product line.
