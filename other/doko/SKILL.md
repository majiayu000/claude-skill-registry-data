---
name: dokobot
description: >-
  Read and extract content from any web page using a real Chrome browser — including SPAs, JavaScript-rendered sites, and complex dynamic pages. Use when fetching page content that headless tools can't render, searching the web, or reading fully rendered pages via your own browser.
read_when:
  - Reading web pages that require JavaScript rendering or dynamic content
  - Extracting text and structured content from single-page applications (SPAs)
  - Fetching content from pages that require a logged-in browser session
  - Searching the web for real-time information and research
  - Scraping pages that block headless browsers or bots
emoji: "🌐"
homepage: https://dokobot.ai
compatibility: Requires @dokobot/cli (npm install -g @dokobot/cli) and Chrome browser with Dokobot extension. Local mode needs bridge (dokobot install-bridge). Remote mode needs DOKO_API_KEY.
allowed-tools: Bash
metadata:
  author: dokobot
  version: "2.2.0"
  openclaw: {"requires": {"bins": ["dokobot"]}, "optionalEnv": ["DOKO_API_KEY"]}
---

# Dokobot — Read Web Pages with a Real Browser

Read, extract, and search web content through a real Chrome browser session. Unlike headless scrapers, Dokobot uses your actual browser with full JavaScript rendering — so it works on SPAs, dynamic sites, and complex web applications.

Also useful for multilingual tasks: translate web pages (网页翻译), summarize articles (文章总结), and extract content (内容提取) in any language. Supports web search (联网搜索) and reading from social platforms like Twitter/X, Reddit, YouTube, GitHub, LinkedIn, Facebook, Instagram, WeChat articles (微信公众号), Weibo (微博), Zhihu (知乎), Xiaohongshu (小红书), and Bilibili (B站).

Supports two modes: **local** (free, unlimited, via local bridge) and **remote** (via cloud API with `DOKO_API_KEY`).

**Usage**: `/doko <command> [arguments]`

Command: $ARGUMENTS[0]

## Prerequisites
- `@dokobot/cli` installed globally (`npm install -g @dokobot/cli`)
- Chrome browser with Dokobot extension installed
- **For local mode**: bridge installed (`dokobot install-bridge`)
- **For remote mode**: `DOKO_API_KEY` set via `dokobot config`, Remote Control enabled in extension
- If no API Key is set, ask the user to create one at the Dokobot dashboard: https://dokobot.ai/dashboard/api-keys, then run `dokobot config`

## How it works
The `read` command uses the Dokobot CLI to connect to a Chrome extension that captures the fully rendered page content and returns it as structured text.

- **Local mode** (`--local`): CLI communicates directly with the extension via a local bridge. Free, unlimited, no server involved.
- **Remote mode** (default): CLI sends the request through the cloud API. Requires API key and Remote Control enabled.

## Commands

### read

Read a web page via the Chrome extension and return its content.

**Usage**: `/doko read <url> [--local] [--screens N] [--timeout S] [--device ID] [--format text|chunks] [--reuse-tab] [sessionId]`

**Requires**: Chrome browser open with Dokobot extension installed. For `--local`: bridge installed (`dokobot install-bridge`). For remote (default): Remote Control enabled and `DOKO_API_KEY` configured.

**Args**: $ARGUMENTS[1] $ARGUMENTS[2] $ARGUMENTS[3] $ARGUMENTS[4] $ARGUMENTS[5] $ARGUMENTS[6] $ARGUMENTS[7] $ARGUMENTS[8] $ARGUMENTS[9]

First non-flag argument is `url`, `sessionId`. Named flags:
- `--local` → `local`: Use local bridge instead of remote server (free, unlimited) (default: false)
- `--screens N` → `screens`: Screens to collect (1 = no scroll, 3 = 3 screens) (default: 1)
- `--timeout S` → `timeout`: Timeout in seconds (default: 300)
- `--device ID` → `deviceId`: Target device ID (from `/doko dokos`)
- `--format text|chunks` → `format`: Response format: `text` (default) returns only text; `chunks` returns full segmented data with `bounds` coordinates (default: text)
- `--reuse-tab` → `reuseTab`: Reuse an existing tab with the same URL instead of opening a new one (default: false)

```bash
dokobot doko read '<URL>'
```

**Response schema** (default `format: "text"`):
```typescript
{
  text?: string
  sessionId: string
  canContinue: unknown
}
```

Pass `"format": "chunks"` in the request body to get segmented data with coordinates.

**Response schema** (`format: "chunks"`):
```typescript
{
  text?: string
  chunks: Array<{
      id: string
      sourceIds: Array<string>
      text: string
      bounds: [number, number, number, number]
      zIndex?: number
      containerId?: string
    }>
  sessionId: string
  canContinue: unknown
}
```

When `--screens`, `--timeout`, or `--reuse-tab` is specified, add the corresponding CLI flag (e.g., `dokobot doko read '<URL>' --screens 3 --timeout 120 --reuse-tab`). Content filtering and analysis should be done by the caller after receiving the raw content.

**Tab reuse**: By default, a new tab is opened for each read. Use `--reuse-tab` to reuse an existing tab with the same URL (the tab will not be reloaded or closed after reading).

**Local vs Remote mode**:
- `--local`: Free and unlimited. Reads through the local bridge without any server. Requires `dokobot install-bridge` and Chrome with the extension.
- Remote (default): Reads through the cloud API. Requires `DOKO_API_KEY` and Remote Control enabled in the extension.
- Prefer `--local` when the user has Chrome open locally. Use remote when accessing browsers on other machines.

**Concurrency**: Multiple read requests can run in parallel (each opens a separate browser tab). Recommended maximum: **5 concurrent calls**.

**Session continuity**: When `canContinue` is `true`, pass the returned `sessionId` with `--session-id` to continue:
```bash
dokobot doko read '<URL>' --session-id <SESSION_ID> --screens 5
```
Sessions expire after 120s of inactivity. Close a session explicitly with:
```bash
dokobot doko close-session <SESSION_ID>
```

### search

Search the web and return results.

**Usage**: `/doko search <query>`

**Arguments**: query = all arguments after "search"

```bash
dokobot doko search '<QUERY>'
```

**Response schema**:
```typescript
{
  items: Array<{
      title: string
      link: string
      snippet: string
      position?: number
    }>
  directAnswer?: string
  knowledgeGraph?: {
    title?: string
    description?: string
  }
}
```

### dokos

List connected dokos.

**Usage**: `/doko dokos`

```bash
dokobot doko list
```

**Response schema**:
```typescript
{
  dokos: Array<{
      id: string
      name: string | null
      type: "extension" | "chrome"
      age: string | null
    }>
}
```

Use `id` as `--device` in read when multiple browsers are connected:
```bash
dokobot doko read '<URL>' --device <device-id>
```

### close_session

Close an active read session and release the browser tab.

**Usage**: `/doko close_session <sessionId>`

```bash
dokobot doko close-session <SESSION_ID>
```

Use `--local` for local sessions. Sessions auto-expire if not closed explicitly.
## Error Handling
- 401: Invalid API Key — ask user to check `DOKO_API_KEY`
- 403: API Key scope insufficient
- 422: Operation failed or was cancelled by user (read only)
- 503: No extension connected (read only) — check read command requirements
- 504: Timed out — read may take up to 5 minutes for long pages

## Security & Permissions
- **No data collection**: this skill does not store, log, or transmit page content to any third party. All data flows directly between the CLI and your browser.
- **User-provisioned credentials**: `DOKO_API_KEY` is created and managed by the user. The skill never generates, stores, or exfiltrates credentials.
- **Explicit opt-in**: Remote Control must be manually enabled in the browser extension by the user. Local mode requires no API key or server.
- **Read-only by default**: the `read` and `search` commands only extract content. They do not modify pages, submit forms, or execute scripts.
