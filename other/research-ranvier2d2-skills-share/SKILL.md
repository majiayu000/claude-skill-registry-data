---
name: research
description: Systematic research and feasibility analysis using local files and user-provided sources. Use when asked to research, investigate, look up, analyze, compare approaches, or deliver a structured research report with citations.
---

# Research

## Overview
Provide a repeatable workflow to gather evidence, synthesize findings, and deliver a structured report. Default to local/offline sources unless web tools are available in the current session.

## Workflow

### 1) Define scope and success criteria
- Restate the question in 1-2 sentences.
- Identify constraints (timeframe, domain, depth, deliverable).
- List 3-5 sub-questions that, once answered, will resolve the request.

### 2) Plan sources and strategy
- Prefer primary sources (official docs, specs, repo code).
- If web tools are unavailable, ask the user for URLs or files to analyze.
- Decide whether you need breadth (many sources) or depth (few authoritative sources).

### 3) Gather evidence
- For local repositories or folders, use the search script to collect citations:

```bash
python3 scripts/local_research.py --query "<topic>" --path . --output /tmp/research_hits.md
```

- If you have web-capable tools in this session, gather links first, then fetch only the pages you need.

### 4) Synthesize findings
- Use the report skeleton script, then fill it using the gathered evidence:

```bash
python3 scripts/report_skeleton.py --topic "<topic>" --out /tmp/research_report.md
```

### 5) Validate and present
- Cross-check critical claims across at least two sources when possible.
- Call out any gaps, stale sources, or assumptions explicitly.
- Keep a clear separation between facts and analysis.

## Scripts

### scripts/local_research.py
Search local files for a topic and generate a Markdown evidence bundle.

```bash
python3 scripts/local_research.py --query "Ralph Wiggum loop" --path . --context 2 --max-results 200 --output /tmp/research_hits.md
```

### scripts/report_skeleton.py
Generate a structured research report template for synthesis.

```bash
python3 scripts/report_skeleton.py --topic "Ralph Wiggum loop" --out /tmp/research_report.md
```
