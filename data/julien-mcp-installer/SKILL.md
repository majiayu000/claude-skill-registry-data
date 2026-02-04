---
name: julien-mcp-installer
description: Interactive MCP server installer. Lists all available MCPs by category and installs the user's choice into .mcp.json
triggers:
  - install mcp
  - add mcp server
  - mcp installer
  - setup mcp
  - configure mcp
  - ajouter mcp
  - installer mcp
  - which mcp
  - list mcp servers
  - available mcp
  - mcp marketplace
---

# MCP Server Installer

Interactive installer for MCP (Model Context Protocol) servers. Browse by category, select, and install.

## Usage

When user asks to install an MCP or wants to see available options:

1. **Use AskUserQuestion** to let user select category
2. **Use AskUserQuestion** to let user select specific MCP
3. **Install** by merging config into `.mcp.json`

## Available MCP Servers

### Category: Office (5)

| MCP | Package | Description |
|-----|---------|-------------|
| **excel** | `@anthropic/mcp-excel` | Excel spreadsheet manipulation |
| **excel-win32com** | `mcp-server-excel` (uvx) | Excel via Win32COM (Windows) |
| **word** | `@anthropic/mcp-word` | Word document manipulation |
| **word-uvx** | `mcp-server-word` (uvx) | Word via python-docx |
| **powerpoint** | `@anthropic/mcp-powerpoint` | PowerPoint manipulation |
| **powerpoint-uvx** | `mcp-server-pptx` (uvx) | PowerPoint via python-pptx |
| **pdf-reader** | `@anthropic/mcp-pdf-reader` | PDF text extraction |

### Category: Browser (3)

| MCP | Package | Description |
|-----|---------|-------------|
| **playwright** | `@playwright/mcp@latest` | Browser automation |
| **chrome-devtools** | `@anthropic/mcp-chrome-devtools` | Chrome DevTools Protocol |
| **brave** | `@anthropic/mcp-brave` | Brave Search API |

### Category: APIs (6)

| MCP | Package | Description |
|-----|---------|-------------|
| **notion** | `@suekou/mcp-notion-server` | Notion workspace integration |
| **notion-pro** | `notion-mcp` (uvx) | Advanced Notion features |
| **notion-internal** | Custom | Internal Notion API |
| **github-http** | `@anthropic/mcp-github` | GitHub API via HTTP |
| **github-docker** | `mcp/github` (Docker) | GitHub API via Docker |
| **gmail** | `@anthropic/mcp-gmail` | Gmail integration |
| **outlook** | `@anthropic/mcp-outlook` | Outlook integration |

### Category: AI/LLM (4)

| MCP | Package | Description |
|-----|---------|-------------|
| **codex-cli** | `@anthropic/mcp-codex` | OpenAI Codex integration |
| **context7** | `@anthropic/mcp-context7` | Context management |
| **taskmaster** | `@anthropic/mcp-taskmaster` | Task orchestration |
| **serena** | `serena-mcp` (uvx) | Serena AI assistant |

### Category: Utilities (8)

| MCP | Package | Description |
|-----|---------|-------------|
| **basic-memory** | `@anthropic/mcp-memory` | Persistent memory storage |
| **desktop-commander** | `@anthropic/mcp-desktop` | Desktop automation |
| **jina** | `@anthropic/mcp-jina` | Jina AI embeddings |
| **puremd** | `@anthropic/mcp-puremd` | Markdown processing |
| **veyrax** | `veyrax-mcp` (uvx) | Veyrax integration |
| **webmind** | `webmind-mcp` (uvx) | Web intelligence |
| **youtube-info** | `@anthropic/mcp-youtube` | YouTube metadata |

## Installation Flow

### Step 1: Ask Category

```
Use AskUserQuestion with options:
- Office (Excel, Word, PowerPoint, PDF)
- Browser (Playwright, Chrome DevTools, Brave)
- APIs (Notion, GitHub, Gmail, Outlook)
- AI/LLM (Codex, Context7, Taskmaster)
- Utilities (Memory, Desktop, YouTube)
```

### Step 2: Ask Specific MCP

Based on category choice, present specific MCPs with descriptions.

### Step 3: Install

1. Read existing `.mcp.json` or create new
2. Add selected MCP config to `mcpServers`
3. Write updated `.mcp.json`
4. Inform user to restart Claude Code

## MCP Configurations

### NPX-based MCPs (most common)

```json
{
  "mcp-name": {
    "command": "cmd",
    "args": ["/c", "npx", "-y", "@package/name"]
  }
}
```

### UVX-based MCPs (Python)

```json
{
  "mcp-name": {
    "command": "cmd",
    "args": ["/c", "uvx", "package-name"]
  }
}
```

### With Environment Variables

```json
{
  "mcp-name": {
    "command": "cmd",
    "args": ["/c", "npx", "-y", "@package/name"],
    "env": {
      "API_KEY": "${API_KEY}"
    }
  }
}
```

## Full Configurations Reference

### Office

```json
"excel": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@anthropic/mcp-excel"]
}

"word": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@anthropic/mcp-word"]
}

"powerpoint": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@anthropic/mcp-powerpoint"]
}

"pdf-reader": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@anthropic/mcp-pdf-reader"]
}
```

### Browser

```json
"playwright": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@playwright/mcp@latest"]
}

"chrome-devtools": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@anthropic/mcp-chrome-devtools"]
}

"brave": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@anthropic/mcp-brave"],
  "env": {
    "BRAVE_API_KEY": "${BRAVE_API_KEY}"
  }
}
```

### APIs

```json
"notion": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@suekou/mcp-notion-server"],
  "env": {
    "NOTION_API_TOKEN": "${NOTION_API_TOKEN}",
    "NOTION_MARKDOWN_CONVERSION": "true"
  }
}

"github": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@anthropic/mcp-github"],
  "env": {
    "GITHUB_TOKEN": "${GITHUB_TOKEN}"
  }
}

"gmail": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@anthropic/mcp-gmail"],
  "env": {
    "GMAIL_CREDENTIALS": "${GMAIL_CREDENTIALS}"
  }
}
```

### AI/LLM

```json
"codex-cli": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@anthropic/mcp-codex"]
}

"taskmaster": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@anthropic/mcp-taskmaster"]
}
```

### Utilities

```json
"basic-memory": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@anthropic/mcp-memory"]
}

"youtube-info": {
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@anthropic/mcp-youtube"]
}
```

## Environment Variables by MCP

| MCP | Required Env Vars |
|-----|-------------------|
| notion | `NOTION_API_TOKEN` |
| github | `GITHUB_TOKEN` |
| brave | `BRAVE_API_KEY` |
| gmail | `GMAIL_CREDENTIALS` |
| outlook | `OUTLOOK_CREDENTIALS` |

## Post-Installation

After installation:
1. **Restart Claude Code** to load the new MCP
2. **Set environment variables** if required
3. **Test** with a simple command

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `npx` not found | Install Node.js |
| `uvx` not found | `pip install uv` |
| MCP not loading | Check `.mcp.json` syntax |
| Auth errors | Verify environment variables |
| Timeout | Check network connectivity |

## Skill Chaining

- **Replaces**: All 28 individual `julien-mcp-*` skills
- **Tools Used**: AskUserQuestion, Read, Edit, Write
- **Output**: Configured `.mcp.json`
