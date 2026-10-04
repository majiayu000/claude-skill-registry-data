---
name: "scrapling"
description: "CLI-first web scraping & content extraction with optional MCP server. Use when you have target URLs and need clean, selector-based outputs (html/md/txt)."
---

# Scrapling Skill (VCO)

Scrapling is a Python-based web scraping / extraction toolkit that exposes:
- a **CLI** (`scrapling ...`) for fetching + extracting content into files
- an **optional MCP server** (`scrapling mcp`) so an agent can call structured scraping tools

This skill is **CLI-first**. Prefer it when you already have URLs and need reliable, repeatable extraction (CSS selector → file).

## When to use

Use `scrapling` when you need:

- Extract **specific parts** of a web page (CSS selector / XPath) into `.txt` / `.md` / `.html`
- Run **repeatable scraping jobs** (batch URLs with a small wrapper script)
- Reduce token usage by extracting only the relevant DOM region before passing to the LLM
- Provide a local MCP endpoint for scraping tools (agent → MCP → scrapling)

## Boundaries (vs Playwright / Search)

### vs `playwright`
- `scrapling`: best for “get URL → extract selector → write file” workflows; simpler, faster iteration
- `playwright`: best for interactive UI flows (login, multi-step navigation, downloads, complex JS actions, stateful sessions)

If you must *navigate* or *click through* a UI, use `playwright`.
If you can directly fetch the target page and just need extraction, use `scrapling`.

### vs search tools
- Search tools are for discovering sources/URLs (query → result list → choose URLs).
- `scrapling` is for acquisition + extraction once you already know the URL(s).

A common pipeline:
1) Search → find candidate URLs
2) Scrapling → extract focused content from chosen URLs
3) LLM → summarize / transform / analyze extracted outputs

## Prerequisite check (required)

1) Python version (Scrapling requires Python >= 3.10):
```powershell
python --version
```

2) Scrapling CLI availability:
```powershell
scrapling --help
```

## Installation (recommended)

Scrapling’s CLI and MCP features are enabled via extras.

Recommended (CLI + MCP + fetchers):
```powershell
python -m pip install "scrapling[ai]"
```

If you only want CLI fetch/extract without MCP:
```powershell
python -m pip install "scrapling[fetchers]"
```

If you use browser-based fetchers, you may need browser binaries:
```powershell
# Option A: via Scrapling helper (after install)
scrapling install

# Option B: directly via Playwright
python -m playwright install
```

## Wrapper script (Windows convenience)

This skill ships a thin PowerShell wrapper:
- `C:/Users/羽裳/.codex/skills/scrapling/scripts/scrapling.ps1`

It checks whether `scrapling` exists and prints install hints if missing.

## Common CLI patterns

### 1) Extract full page body (to Markdown)
```powershell
scrapling extract get "https://example.com" out.md
```

### 2) Extract a specific element (CSS selector) to text
```powershell
scrapling extract get "https://example.com" out.txt --css-selector "main article"
```

### 3) Extract HTML for downstream parsing
```powershell
scrapling extract get "https://example.com" out.html --css-selector "#content"
```

### 4) Use browser-backed fetcher mode (when simple GET is blocked / dynamic)
```powershell
scrapling extract fetch "https://example.com" out.md --css-selector "main"
```

Tip: keep outputs in files and only feed the smallest relevant snippet to the LLM.

## MCP server relationship (optional)

Scrapling can run as an MCP server. This is useful when:
- the agent needs tool-style scraping calls
- you want scraping results to be structured and deterministic

Start MCP server (stdio transport by default):
```powershell
scrapling mcp
```

Optional: run MCP server with HTTP transport:
```powershell
scrapling mcp --http --host 127.0.0.1 --port 8765
```

### Example MCP server config snippet

```json
{
  "servers": {
    "scrapling": {
      "mode": "stdio",
      "command": "scrapling",
      "args": ["mcp"],
      "required": false,
      "note": "Requires: python -m pip install \"scrapling[ai]\""
    }
  }
}
```

## Safety & ops notes

- Prefer selector-based extraction to minimize data volume.
- Treat scraping as an external dependency: handle timeouts, retries, and failures explicitly.
- For aggressive bot protection, consider switching fetchers or using `playwright`.
