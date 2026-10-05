---
name: markdown-beautifier
description: Transform raw notes, analysis, or data into clean, readable Markdown with tables, ASCII box diagrams, code fences, and visual hierarchy. Use when asked to beautify, format nicely, create a pretty report, or make output presentation-ready.
---

# Markdown Beautifier

## Overview
Turn rough text or data into publication-ready Markdown with clear hierarchy, tables, and boxed callouts. Prefer concise structure over long prose.

## Quick Start

```bash
./scripts/generate_report.sh \
  --input notes.txt \
  --output report.md \
  --style technical
```

Styles:
- technical: metrics + code fence
- summary: short bullets + full content
- podcast: outline + raw notes

## Workflow
1) Identify the output goal (brief, technical, or narrative).
2) Normalize the input (trim noise, keep the useful lines).
3) Add a clear structure: title, summary, details.
4) Use tables for counts or comparisons.
5) Use ASCII boxes only for key callouts.

## Formatting Patterns

ASCII box:
```
+----------------------------------------------+
| NOTE: Keep the box short and skimmable.      |
+----------------------------------------------+
```

Table:
```markdown
| Category | Count | Status |
|:---------|------:|:------:|
| Alpha    |    42 |   ok   |
| Beta     |    17 |  warn  |
```

Callout:
```markdown
> Note: This section summarizes the core risks.
```

## Script

### generate_report.sh
- Reads a text or markdown file and writes a structured markdown report.
- Supports --style technical|summary|podcast and optional --title.

```bash
./scripts/generate_report.sh \
  --input data.txt \
  --output report.md \
  --style summary \
  --title "Weekly Update"
```
