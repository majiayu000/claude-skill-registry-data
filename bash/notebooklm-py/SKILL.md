---
metadata:
  name: notebooklm-py
  class: toolboxes
  type: skill
  version: '1.0'
  schema_version: '1.0'
  freshness:
    status: active
    sync_count: 0
    last_synced_by: daemon
    last_synced: '2026-06-27T00:00:00'
credentials:
  maturity: "battle-tested"
  description: "Full programmatic access to Google NotebookLM via reverse-engineered RPC calls."
  when_to_use: "Use this skill when the task involves notebooklm py"
  triggers: ["notebooklm", "notebook", "upload source", "generate audio", "generate podcast", "generate quiz", "generate mindmap"]
  inputs: ["sources (URLs, PDFs, text)", "notebook_id", "generation instructions"]
  outputs: ["audio", "video", "quiz JSON", "flashcards JSON", "slide deck PDF/PPTX", "infographic", "mind map JSON", "query answer"]
---

# notebooklm-py Skill

## Source
- **Repo**: https://github.com/teng-lin/notebooklm-py
- **PyPI**: `pip install notebooklm-py`
- **Version**: v0.4.0 (May 2026)
- **License**: MIT

## What It Does
Full programmatic access to Google NotebookLM via reverse-engineered RPC calls (NOT browser automation). Uses your existing Pro plan session — zero extra cost.

## Setup (One-Time)
```bash
# Install
pip install "notebooklm-py[browser]"
playwright install chromium

# Authenticate (opens browser once, saves session cookies)
notebooklm login
```

## Core CLI Commands
**CRITICAL:** Always use relative portable paths to execute the OS Engine so the workspace can be ported to new machines without breaking:

```bash
# Notebook management
.\.venv\Scripts\python.exe -m notebooklm create "My Research"
.\.venv\Scripts\python.exe -m notebooklm use <notebook_id>

# Add sources
.\.venv\Scripts\python.exe -m notebooklm source add "https://example.com"
.\.venv\Scripts\python.exe -m notebooklm source add "./document.pdf"

# Query
.\.venv\Scripts\python.exe -m notebooklm ask "What are the key themes?"

# Generate content
.\.venv\Scripts\python.exe -m notebooklm generate audio "make it engaging" --wait
.\.venv\Scripts\python.exe -m notebooklm generate video --style whiteboard --wait
.\.venv\Scripts\python.exe -m notebooklm generate cinematic-video "documentary-style" --wait
.\.venv\Scripts\python.exe -m notebooklm generate quiz --difficulty hard
.\.venv\Scripts\python.exe -m notebooklm generate flashcards --quantity more
.\.venv\Scripts\python.exe -m notebooklm generate slide-deck
.\.venv\Scripts\python.exe -m notebooklm generate infographic --orientation portrait
.\.venv\Scripts\python.exe -m notebooklm generate mind-map
.\.venv\Scripts\python.exe -m notebooklm generate data-table "compare key concepts"

# Download artifacts
.\.venv\Scripts\python.exe -m notebooklm download audio ./podcast.mp3
.\.venv\Scripts\python.exe -m notebooklm download video ./overview.mp4
.\.venv\Scripts\python.exe -m notebooklm download quiz --format json ./quiz.json
.\.venv\Scripts\python.exe -m notebooklm download flashcards --format json ./cards.json
.\.venv\Scripts\python.exe -m notebooklm download slide-deck ./slides.pdf        # or .pptx
.\.venv\Scripts\python.exe -m notebooklm download infographic ./infographic.png
.\.venv\Scripts\python.exe -m notebooklm download mind-map ./mindmap.json
.\.venv\Scripts\python.exe -m notebooklm download data-table ./data.csv
```

## Python API (for scripted pipelines)
```python
import asyncio
from notebooklm import NotebookLMClient

async def main():
    async with await NotebookLMClient.from_storage() as client:
        nb = await client.notebooks.create("Research")
        await client.sources.add_url(nb.id, "https://example.com", wait=True)
        result = await client.chat.ask(nb.id, "Summarize this")
        print(result.answer)
        status = await client.artifacts.generate_audio(nb.id, instructions="make it engaging")
        await client.artifacts.wait_for_completion(nb.id, status.task_id)
        await client.artifacts.download_audio(nb.id, "podcast.mp3")

asyncio.run(main())
```

## Features Available Beyond the Web UI
- Download quiz/flashcards as structured JSON
- Download slide decks as editable PPTX
- Export mind maps as hierarchical JSON
- Export data tables as CSV
- Batch download all artifacts of a type
- Retrieve full indexed text of any source
- Save chat Q&A to notebook notes
- Switch between multiple Google accounts (profiles)
