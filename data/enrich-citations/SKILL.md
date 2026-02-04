---
name: enrich-citations
description: Find and add authoritative source links for all facts, citations, and references in markdown documents
---

# Enrich Citations

Enhance markdown documents by finding and adding authoritative source links for mentioned facts, tools, products, research, and references.

## Usage

Use the `enrich_citations.py` script to process markdown documents:

```bash
# Use default output location (~/tmp/citation_enriched.md - allows overwrite)
python scripts/enrich_citations.py --document-file /path/to/document.md

# Specify custom output location (cannot overwrite existing files)
python scripts/enrich_citations.py --document-file /path/to/document.md --output /path/to/output.md
```

## What It Does

The script automatically:
- Identifies all references (tools, research, products, organizations, people, standards)
- Performs web search to find authoritative sources
- Adds markdown hyperlinks with proper spacing: `[Reference](URL)`
- Verifies all URLs are valid and accessible
- Preserves all original content (only adds hyperlinks, no text changes)
- Prioritizes official sources and documentation

## Options

- `--document-file` (required) - Path to the markdown document to enrich
- `--output` (optional) - Custom output path (default: `~/tmp/citation_enriched.md`)

## Output Behavior

- **Default location**: `~/tmp/citation_enriched.md` - Allows overwrite
- **Custom location**: Cannot overwrite existing files (raises error if file exists)

## Reference Types Identified

- External sources and research papers
- Tools, software, frameworks, libraries
- Products and services
- Organizations and institutions
- Technical concepts and standards (RFC, W3C, APIs)
- People and experts

## Requirements

- Python 3.11+
- Claude CLI must be installed and accessible
- Internet connection (for web searches)
- Document file must exist at specified path
