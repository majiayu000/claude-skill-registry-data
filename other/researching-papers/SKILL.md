---
name: researching-papers
description: >-
  Searches academic databases (arXiv, Crossref, PMC, Semantic Scholar, Open Library,
  Stanford Encyclopedia of Philosophy) for papers matching a research query, downloads
  PDFs, and converts them to markdown. Use when grounding fictional science in real
  research, finding citations for existing content, or when user says "find papers",
  "search for research", "download papers", "what does real science say about",
  "ground this in research", "find citations", or "look up [scientific concept]".
  Does NOT map research onto canon formalism — use /integrating-research for that.
model: sonnet
effort: medium
---

# Researching Papers

Search open-access academic sources, download PDFs, and convert to markdown.

## Tool

All commands use `tools/research-tool.py`:

```bash
# Search default sources (arXiv + Crossref + PMC + Unpaywall)
python3 tools/research-tool.py search "quantum time operator"
python3 tools/research-tool.py search "percolation theory" --source arxiv --max 10

# Search humanities (Semantic Scholar + Open Library + SEP + PhilPapers)
python3 tools/research-tool.py search "autopoiesis" --source humanities
python3 tools/research-tool.py search "structural realism" --source sep --download

# Search everything
python3 tools/research-tool.py search "recursive epistemology" --source all

# Download specific paper
python3 tools/research-tool.py download 2301.12345
python3 tools/research-tool.py download https://arxiv.org/pdf/2301.12345.pdf --title "Title"

# Fetch SEP entry by slug
python3 tools/research-tool.py fetch-sep structural-realism

# Convert PDF to markdown
python3 tools/research-tool.py convert _source/research/papers/paper-name.pdf
python3 tools/research-tool.py convert-all

# List and index
python3 tools/research-tool.py list
python3 tools/research-tool.py list --topic "collapse"
python3 tools/research-tool.py index
```

## File Organization

- `_source/research/papers/` — original PDFs
- `_source/research/markdown/` — converted markdown
- `_source/research/sep-entries/` — Stanford Encyclopedia entries
- `_source/research/INDEX.md` — catalog
- `_source/research/last-search-results.json` — most recent results

## Domain Strategies

**Physics/Chemistry/Biology:** Default sources. Prefer recent papers (2020+).
Prioritize experimental results.

**Philosophy/Foundations:** Use `--source humanities`. Domains: philosophy
of science, formal epistemology, systems theory, cognitive science.

## Process

1. Identify the gap or concept needing grounding
2. Search appropriate sources
3. Read converted markdown in `_source/research/markdown/` or `sep-entries/`
4. Present findings with relevance assessment
5. Hand off to /integrating-research for canon formalization

## Citations

[Author, Year] inline with ## References section. Each entry includes a
one-sentence annotation. Cited science is canon science — no disclaimers.

## Configuration

Set your contact email for polite API access:
```bash
export RESEARCH_TOOL_EMAIL="your-email@example.com"
```

Requires `pdftotext` (poppler-utils) or `pypdf` for PDF conversion.

## Out of Scope

Does NOT map research onto canon formalism (use /integrating-research).
Does NOT write science files (use /writing-science).
Does NOT audit existing citations (use /auditing-canon).
