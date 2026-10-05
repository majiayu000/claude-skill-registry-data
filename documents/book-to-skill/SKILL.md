---
name: book-to-skill
description: Use when convert technical books and documents (PDF, EPUB, DOCX, HTML,
  Markdown, RTF, MOBI) into structured agent skills with frameworks, mental models,
  chapter references, and decision rules. Includes full extraction pipeline. Use when
  the user wants to turn a book or document collection into a reusable agent skill
  for study and reference.
domain: core
author: mahipal, virgiliojr94
license: MIT
subdomain: tooling
tags:
- documentation
- skill-generation
- knowledge-management
- pdf
- epub
- conversion
- learning
- extraction
version: 1.0.0
category: core
---
## Overview

This skill converts technical books and documents — PDF, EPUB, DOCX, HTML, Markdown, RTF, MOBI — into structured agent skills with frameworks, mental models, chapter references, and decision rules. Use it when a knowledge source should become reusable operational guidance. It includes the full extraction and structuring pipeline.



persona:
  name: "Virgilio Jr."
  title: "The Knowledge Distiller — Book-to-Skill Pipeline Maintainer"
  expertise: ['Document Extraction', 'Knowledge Structuring', 'Agent Skill Design', 'Pipeline Engineering']
  philosophy: "Books contain crystallized expertise. Extract structure, not summaries."
  credentials: ['Creator of book-to-skill (MIT)', 'Open-source maintainer']
  principles: ['Structure over summary', 'Preserve author precision', 'Layer depth appropriately', 'Privacy-first: all processing local']

# Book-to-Skill Converter

Transform written knowledge into actionable agent skills by extracting frameworks, principles, techniques, and anti-patterns — not producing summaries.

**Upstream repo:** [github.com/virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill)  
**Upstream author:** [@virgiliojr94](https://github.com/virgiliojr94)  
**This integration:** Full extraction pipeline vendored into `core/book-to-skill/`  
**License:** MIT  
**Format support:** PDF, EPUB, DOCX, TXT, Markdown, reStructuredText, AsciiDoc, HTML, RTF, MOBI/AZW/AZW3

---

## Process

Convert a knowledge source into a structured, loadable skill by following the extraction pipeline.

1. **Ingest** — load the source in its native format (PDF, EPUB, DOCX, HTML, Markdown, RTF, MOBI) and confirm all chapters/sections are readable.
2. **Extract structure** — pull frameworks, mental models, chapter references, and decision rules into the skill's working sections.
3. **Author the skill** — write frontmatter (name, description, domain), a workflow, and at least one concrete code example grounded in the source.
4. **Validate** — run the repo's lint and test gates; fix section or frontmatter gaps.
5. **Install and verify** — load the skill in your agent harness and run one real task against it.

## When to Use

**Trigger phrases:**
- "turn this book into a skill"
- "book-to-skill"
- "convert this PDF to an agent skill"
- "generate a skill from this document"
- "study this book with my agent"

**Use when:**
- You want your agent to reference a technical book while coding
- You have a collection of docs/papers you constantly re-read
- You need structured access to a book's content without dumping the whole PDF into context
- You own a book PDF and want it as an on-demand agent skill

**Don't use for:**
- Fiction / narrative books (the tool works technically but the output isn't useful)
- Books you don't own (copyright compliance — you must own the source)
- Simple web articles (use web extraction instead; full pipeline is overkill)

---



## Verification

- Convert one book (e.g. a PDF) and confirm the output skill has frontmatter (name, description, domain), a workflow section, and at least one concrete example.
- Spot-check that chapter-level frameworks and mental models from the source appear in the output, not just a summary.
- Verify the skill loads in your agent harness (skill discovery finds it, sections parse).
- Confirm license/attribution is preserved if the source book requires it.

## Anti-Rationalization Table

| Excuse | Reality | Rule |
|--------|---------|------|
| "I'll just read the book" | Reading ≠ actionable skill; skills need frameworks, not summaries | Extract mental models, decision rules, and code patterns |
| "One skill per book" | Books contain multiple transferable frameworks | Split into atomic skills by framework/model |
| "PDF extraction is enough" | PDFs lose structure; need chapter, section, diagram mapping | Parse structure first, then content |


**Trigger phrases:**
- "turn this book into a skill"
- "book-to-skill"
- "convert this PDF to an agent skill"
- "generate a skill from this document"
- "study this book with my agent"

**Use when:**
- You want your agent to reference a technical book while coding
- You have a collection of docs/papers you constantly re-read
- You need structured access to a book's content without dumping the whole PDF into context
- You own a book PDF and want it as an on-demand agent skill

**Don't use for:**
- Fiction / narrative books (the tool works technically but the output isn't useful)
- Books you don't own (copyright compliance — you must own the source)
- Simple web articles (use web extraction instead; full pipeline is overkill)

---

## How It Works

```
PDF / EPUB / DOCX / HTML / Markdown / RTF / MOBI
    │
    ▼
Extract text → Detect structure (chapters, headings)
    │
    ▼
LLM analyzes: frameworks, principles, techniques, anti-patterns
    │
    ▼
Generate structured skill:
  ├── SKILL.md          (core mental models + chapter index, ~4K tokens)
  ├── chapters/ch*.md   (one per chapter, ~1K tokens each, loaded on-demand)
  ├── glossary.md       (key terms with chapter refs, ~1.5K tokens)
  ├── patterns.md       (techniques, algorithms, design patterns, ~2K tokens)
  └── cheatsheet.md     (decision tables, quick-reference rules, ~1K tokens)
```

Chapter files are **loaded on-demand** — they don't count against the skill budget until queried.

---

## Pipeline Location

The full extraction pipeline lives at `core/book-to-skill/` in this repo:

```
core/book-to-skill/
├── SKILL.md           ← This file (skill definition + instructions)
├── book_to_skill/     ← Python extraction package
│   ├── __init__.py
│   ├── cli.py         ← CLI entrypoint
│   ├── config.py      ← Extensions, paths, dependency constants
│   ├── dependencies.py← Optional-dep probing + --check
│   ├── exceptions.py  ← ExtractionError (per-source failures)
│   ├── sanitize.py    ← Text sanitization
│   ├── utils.py       ← CLI parsing, multi-source resolution, chapter detection
│   └── parsers/
│       ├── pdf.py     ← PDF extraction (pdftotext / pypdf / pdfminer / docling)
│       ├── epub.py    ← EPUB extraction (ebooklib / zipfile)
│       ├── docx.py    ← DOCX extraction (python-docx / zipfile)
│       ├── html.py    ← HTML extraction (beautifulsoup4 / html.parser)
│       ├── rtf.py     ← RTF extraction (striprtf / regex)
│       ├── text.py    ← TXT/MD/RST/AsciiDoc (built-in)
│       └── calibre.py ← MOBI/AZW/AZW3 (Calibre ebook-convert)
├── scripts/
│   └── extract.py     ← Thin entrypoint wrapper
├── tools/
│   ├── validate_skill.py   ← Check generated SKILL.md against host rules
│   ├── scan_generated_skill.py ← Scan output structure
│   └── discovery_tax.py    ← Measure token cost vs context-dump
├── tests/             ← pytest suite
├── docs/              ← Documentation
├── pyproject.toml     ← Python project config
├── README.md          ← Upstream README
└── LICENSE.md         ← MIT license
```

---

## Installation

```bash
# From repo root
cd core/book-to-skill

# Check what extractors are available
python3 -m book_to_skill --check

# Install deps based on your formats
pip3 install pypdf beautifulsoup4 python-docx ebooklib striprtf
sudo apt install poppler-utils   # for pdftotext (text-heavy PDFs, instant)

# For technical books with tables/code blocks
pip3 install docling              # ~1.5s/page, preserves markdown tables
```

---

## Usage

### Run the pipeline

```bash
cd core/book-to-skill

# Check setup
python3 -m book_to_skill --check

# Single file → skill
python3 -m book_to_skill /path/to/book.pdf my-book-slug

# Multiple files → one unified skill
python3 -m book_to_skill paper1.pdf notes.txt research-dir/ unified-research

# Analyze only (no skill generation)
python3 -m book_to_skill --analyze /path/to/book.pdf

# Update existing skill with new content
python3 -m book_to_skill new-chapter.pdf ~/.claude/skills/<existing-skill>/
```

### After generation

The skill lands in your agent's skills directory:
- `~/.claude/skills/<slug>/` for Claude Code
- `~/.copilot/skills/<slug>/` for Copilot CLI
- `~/.agents/skills/<slug>/` for cross-agent

Query it like any skill:

```
/my-book-slug                          # load core mental models
/my-book-slug replication              # find + explain a topic
/my-book-slug ch05                     # dive into chapter 5
/my-book-slug "what chapters exist?"   # browse structure
```

### Processing within an agent session

1. Verify the file exists and is a supported format
2. Ask if it's **technical** (tables, code) or **text-heavy** (prose) — this picks the extractor
3. Run `cd core/book-to-skill && python3 -m book_to_skill <path> <slug>`
4. Confirm the generated skill is loadable
5. Load it with the skill's slug

---

## Modes of Operation

| Mode | Flag | What it does |
|------|------|-------------|
| **Full conversion** | *(default)* | One or more paths → complete skill |
| **Analyze only** | `--analyze` | Extract and report structure without generating skill |
| **From prior analysis** | `--from-analysis <file>` | Skip extraction, use existing notes |
| **Update / fold-in** | *(target existing dir)* | Point at existing skill folder to merge new content |

---

## Technical Notes

### Dependencies by format

| Format | Recommended tool | Install | Notes |
|--------|-----------------|---------|-------|
| PDF (text-heavy) | `pdftotext` | `sudo apt install poppler-utils` | Instant, good for prose |
| PDF (technical) | `docling` | `pip3 install docling` | Preserves tables + code blocks |
| PDF fallback | `pypdf` / `pdfminer.six` | `pip3 install pypdf` | Built-in fallback chain |
| EPUB | `ebooklib` + `beautifulsoup4` | `pip3 install ebooklib beautifulsoup4` | Best quality |
| DOCX | `python-docx` | `pip3 install python-docx` | |
| HTML | `beautifulsoup4` | `pip3 install beautifulsoup4` | |
| RTF | `striprtf` | `pip3 install striprtf` | |
| MOBI/AZW | Calibre `ebook-convert` | calibre-ebook.com | External app |
| TXT/MD/RST/AsciiDoc | Built-in | None | No deps needed |

### Performance

- 244-page tech book: ~165s (Docling) or 0.1s (pdftotext)
- Typical one-pass LLM cost: ~$0.90–$1.40 on Claude Sonnet 4.5
- Generated skill: ~4K tokens core + ~1K tokens per chapter
- **24×–51× fewer tokens** vs dumping the full book into context per question

### Privacy

All extraction runs locally. Your files are never uploaded by the pipeline. Only the LLM structuring call goes to your provider.

---

## Copyright & Fair Use

book-to-ship ships **no book content**. It's a converter you point at files you already own.

- Processing is local
- Generated skill is a structured derivative (framework names, definitions) — not a reproduction
- Do NOT redistribute generated skills of copyrighted works
- Keep skills of third-party books private

---

## Verification Checklist

- [ ] Source file exists and format is supported
- [ ] Extractors for target format are installed (`--check` to verify)
- [ ] User confirmed technical vs text-heavy (for PDFs)
- [ ] Skill generated without errors
- [ ] Generated SKILL.md has valid frontmatter
- [ ] Chapter files load on-demand when queried
- [ ] User aware of copyright limitations for redistribution
