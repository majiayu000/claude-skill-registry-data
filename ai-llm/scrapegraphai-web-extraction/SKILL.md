---
name: scrapegraphai-web-extraction
description: "Use ScrapeGraphAI for AI-powered web scraping and structured information extraction from websites and documents. Prefer it when a task requires extracting structured data from one or multiple web pages."
risk: medium
source: official
upstream_repo: https://github.com/ScrapeGraphAI/Scrapegraph-ai
upstream_version: "2.2.4"
date_added: "2026-09-25"
---

# ScrapeGraphAI — AI-Powered Web & Document Extraction

[ScrapeGraphAI](https://github.com/ScrapeGraphAI/Scrapegraph-ai) is the official
open-source Python library (`scrapegraphai`, MIT license) that uses an LLM plus a
graph-based pipeline to extract structured data from websites and local documents
(HTML, XML, JSON, Markdown). You describe *what* you want in plain English; the
library handles fetching, cleaning, chunking, and LLM-based extraction.

> There is no separate official "Agent Skill" package published by ScrapeGraphAI —
> this skill was authored directly from the upstream repository's README/AGENTS.md
> (commit `c75c8084`) so agents in this workspace can discover and use the library
> without duplicating unofficial third-party wrappers.

## When to Use

Prefer this skill when the task involves:
- **Structured extraction** from one webpage given a natural-language prompt (`SmartScraperGraph`).
- **Multi-page scraping** across a list of URLs with one shared prompt (`SmartScraperMultiGraph`).
- **Search-based extraction** — pulling structured info from the top-N results of a search engine (`SearchGraph`).
- Extracting data from **HTML, XML, JSON, or Markdown** sources (local files or URLs).
- **Generating a reusable scraping script** (Python) instead of running the extraction inline (`ScriptCreatorGraph` / `ScriptCreatorMultiGraph`).
- **JavaScript-rendered pages** that need a real browser (Playwright/Chromium) rather than a plain HTTP fetch.
- Research/data-collection workflows that need many small structured facts pulled from the web, normalized into JSON.

Do **not** use this skill for simple single static-page HTML fetches with no
structuring needed — a plain `fetch` (the `web` MCP server) is cheaper and faster.
Reserve headless-browser rendering (`headless: True/False`, Playwright) only for
sites that actually require JS execution.

## Prerequisites

- **Isolated runtime** (already installed — see Environment below). Do not use the
  system/global Python for this library.
- **An LLM credential**, provided via environment variable — never hard-code keys.
  This skill does not mandate a specific provider; pick one already configured in
  this environment or ask the user which to use:
  | Provider | Env var (conventional) |
  |----------|-------------------------|
  | OpenAI | `OPENAI_API_KEY` |
  | Groq | `GROQ_API_KEY` |
  | Azure OpenAI | `AZURE_OPENAI_API_KEY` / `AZURE_OPENAI_ENDPOINT` |
  | Google Gemini | `GOOGLE_API_KEY` |
  | Mistral | `MISTRAL_API_KEY` |
  | Ollama (local, no key) | none — requires `ollama pull <model>` locally |
- Optional: `SCRAPEGRAPHAI_TELEMETRY_ENABLED=false` to opt out of anonymous usage telemetry.
- Optional (only for the *managed* ScrapeGraphAI cloud API/MCP, not the OSS library): `SGAI_API_KEY`.

## Environment (already provisioned, global, reusable)

A dedicated, isolated virtual environment was created so this library never
pollutes the system Python or any project's dependencies:

```
~/Developer/AI-Dev-Team/environments/scrapegraphai-env/   (Python 3.12, uv-managed)
```

Always invoke it explicitly:

```bash
~/Developer/AI-Dev-Team/environments/scrapegraphai-env/bin/python your_script.py
```

Installed: `scrapegraphai==2.2.4`, `playwright==1.63.0` (+ Chromium browser binary
already downloaded via `playwright install chromium`).

To refresh/upgrade later:
```bash
cd ~/Developer/AI-Dev-Team/environments
uv pip install --python scrapegraphai-env/bin/python -U scrapegraphai
./scrapegraphai-env/bin/python -m playwright install chromium
```

## Workflow

```
Task Progress:
- [ ] Step 1: Confirm which pipeline fits the task (Smart/Search/Script/Multi)
- [ ] Step 2: Confirm which LLM + env var the user wants to use
- [ ] Step 3: Write a small script using the scrapegraphai-env python
- [ ] Step 4: Run it with the isolated interpreter, review structured JSON output
- [ ] Step 5: Summarize results / persist output as needed
```

### Step 1: Pick the pipeline

| Pipeline | Use case |
|----------|----------|
| `SmartScraperGraph` | Single page, one prompt |
| `SmartScraperMultiGraph` | Multiple pages, one shared prompt |
| `SearchGraph` | Extract from top-N search engine results |
| `SpeechGraph` | Single page → generates an audio summary |
| `ScriptCreatorGraph` / `ScriptCreatorMultiGraph` | Generate a standalone Python scraping script instead of running inline |

### Step 2: Minimal example (single page)

```python
from scrapegraphai.graphs import SmartScraperGraph
import os

graph_config = {
    "llm": {
        "api_key": os.environ["OPENAI_API_KEY"],
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": True,  # set False only if you need to watch the browser
}

scraper = SmartScraperGraph(
    prompt="Extract the page title and main heading",
    source="https://example.com",
    config=graph_config,
)

result = scraper.run()
print(result)
```

For local models with no API key, use Ollama instead:
```python
graph_config = {"llm": {"model": "ollama/llama3.2", "model_tokens": 8192, "format": "json"}, "verbose": True, "headless": True}
```

### Step 3: Multi-page / search variants

Swap `SmartScraperGraph` for `SmartScraperMultiGraph` (pass `source` as a list of
URLs) or `SearchGraph` (pass a search `prompt` plus `max_results`) — same
`graph_config` shape.

### Step 4: Run & verify

```bash
~/Developer/AI-Dev-Team/environments/scrapegraphai-env/bin/python script.py
```

Playwright-rendered fetches require the Chromium browser installed above; if a
"browser not found" error appears, re-run
`./scrapegraphai-env/bin/python -m playwright install chromium`.

## Notes / Boundaries

- This is the **self-hosted open-source library**, not the managed ScrapeGraphAI
  cloud API. The managed API/MCP server (`scrapegraph-mcp`,
  `https://mcp.scrapegraphai.com/mcp`, requires a paid `SGAI_API_KEY`) was
  evaluated per the global MCP routing policy and intentionally **not**
  auto-installed — it would duplicate the `web`/`browser` MCP servers already
  registered for fetching/rendering, and needs a separate paid credential. Ask
  the user explicitly before adding it if hosted crawling/scheduling is needed.
- Respecting `robots.txt` and site terms is the caller's responsibility — use
  responsibly and only on content you have rights to extract.
