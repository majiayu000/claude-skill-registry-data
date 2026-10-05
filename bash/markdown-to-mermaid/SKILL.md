---
name: markdown-to-mermaid
description: Convert structured markdown (lists, steps, timelines, state transitions) into Mermaid diagrams. Use when asked to generate a flowchart, sequence diagram, state diagram, gantt, mindmap, or convert markdown to mermaid.
---

# Markdown to Mermaid

## Overview
Convert markdown outlines or process notes into Mermaid diagrams. The script auto-detects a diagram type and falls back to a flowchart if uncertain.

## Quick Start

```bash
./scripts/md2mermaid.sh \
  --input flow.md \
  --output flow.mmd \
  --type auto \
  --embed
```

## Supported Conversions
- Flowchart: nested bullet lists and headings
- Sequence: numbered steps with optional "Actor: action" lines
- State: lines with "A -> B" transitions
- Gantt: lines containing YYYY-MM-DD ranges
- Mindmap: headings + bullets

## Detection Heuristics
- Dates present: gantt
- Numbered steps: sequence
- Arrow transitions: state
- Nested bullets: flowchart
- Otherwise: mindmap

## Script

### md2mermaid.sh

```bash
./scripts/md2mermaid.sh \
  --input plan.md \
  --output diagram.mmd \
  --type flowchart
```

Options:
- --type auto|flowchart|sequence|state|gantt|mindmap
- --embed (wrap output in ```mermaid fence)
- --title "Custom Title"

## Notes
- If detection fails, the script falls back to a basic flowchart.
- For large or complex diagrams, prefer the repo-svg-sourcemap skill.
