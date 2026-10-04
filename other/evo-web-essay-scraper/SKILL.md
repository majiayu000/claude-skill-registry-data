---
name: evo-web-essay-scraper
description: Scrapes and extracts clean text from Paul Graham essays on paulgraham.com. Handles legacy table-based HTML, character encoding, and text chunking for TTS APIs.
---

# evo-web-essay-scraper

Scrapes Paul Graham essays and prepares text for TTS consumption.

## Key Functions

- `scrape_pg_essay(url)` - Fetches and extracts clean text from a PG essay URL
- `clean_text(text)` - Cleans text artifacts, encoding issues, nav boilerplate
- `chunk_text(text, max_chars=4000)` - Splits text into API-safe chunks by sentence boundaries

## Essay URLs
- "Do Things that Don't Scale": `http://www.paulgraham.com/ds.html`
- "Founder Mode": `http://www.paulgraham.com/foundermode.html`

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-web-essay-scraper/scripts')
from utils import scrape_pg_essay, clean_text, chunk_text

text = scrape_pg_essay('http://www.paulgraham.com/ds.html')
chunks = chunk_text(text, max_chars=4000)
```

## Technical Notes
- PG site uses table-based HTML layout, text in `<font>` tags inside `<table width="435">` or similar
- Encoding: use `response.apparent_encoding` to handle smart quotes/em-dashes
- Remove nav boilerplate like "Want to start a startup?"
- Chunk at sentence boundaries, max 4000 chars for OpenAI TTS (limit is 4096)
