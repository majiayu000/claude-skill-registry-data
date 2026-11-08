---
name: gemini-web-search
description: Search the live web through Gemini's Google Search grounding and get an answer with its cited sources — better than a generic web-search tool for local, fresh-market and trade-press questions (who operates what in a city, current prices, recent news). Use when you need to "Google something", look up businesses, competitors, buyers, prices or news, or verify a fact against live sources before it goes into a report. Needs a GEMINI_API_KEY.
compatibility: >-
  Python 3 with google-genai. Calls the Gemini API with the user's own GEMINI_API_KEY.
metadata:
  network-hosts: "generativelanguage.googleapis.com"
  network-purpose: "grounded Google Search answers with cited sources"
---

# Gemini grounded web search

Gemini queries live Google and returns an answer grounded in cited pages. For "what / who /
how much, right now, in this city" questions it routinely beats a plain search tool, and the
sources come back as structured `{title, uri}` you can carry into a report.

## Call it

```bash
pip install google-genai
export GEMINI_API_KEY=...
python3 scripts/gemini_search.py "Who are the active brewery taproom operators in <city>?"
```

Prints the answer, then `--- SOURCES ---` as `title: uri`.

```python
from gemini_search import grounded
answer, sources = grounded("median sale price, small multifamily, <city> 2025")
```

`grounded()` falls back through a list of models; set `GEMINI_SEARCH_MODELS="a,b,c"` when
model names change.

## When not to use it

- **You already have the URL.** Fetch it; search is for finding, not retrieving.
- **The answer has to be a number you will publish.** Use the search to *find* the primary
  source, then read the number off that source. A grounded summary can still misquote it.

## Rules

- Carry the `sources` into whatever you write. A claim without a URL behind it does not ship.
- The grounding URIs are often Google redirect links (`vertexaisearch...`). Resolve them
  (follow the redirect) before citing.
- Ask one question per call. Compound questions get a blended answer with sources that each
  cover half of it.
