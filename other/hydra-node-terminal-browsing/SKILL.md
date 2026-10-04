---
name: hydra-node-terminal-browsing
description: Use when HYDRA tasks need Node.js-first terminal browsing, deterministic page extraction, and evidence JSON output that can be routed into hydra swarm workflows.
---

# Hydra Node Terminal Browsing

## Overview

Use this skill for fast terminal-first web/repo browsing in HYDRA workflows when you need deterministic, auditable output instead of conversational browsing.

This skill is optimized for the HYDRA 3-gap surfaces:
- `hydra/browsers.py`
- `hydra/swarm_browser.py`
- `hydra/cli_swarm.py`

## When To Use

Trigger this skill when the user asks to:
- browse websites from terminal with Node.js
- collect page evidence in JSON for later agent decisions
- run HYDRA swarm tasks with explicit browser/LLM backend flags
- produce reproducible extraction artifacts (title, text excerpt, links, status)

Do not use this skill for deep JavaScript rendering correctness testing. For full rendering, use HYDRA Playwright backend directly.

## Quick Start

### 1) Deterministic terminal browse (Node)

```powershell
node C:\Users\issda\.codex\skills\hydra-node-terminal-browsing\scripts\hydra_terminal_browse.mjs --url "https://example.com" --out "artifacts\page_evidence.json"
```

Output is structured JSON with:
- `url`, `resolved_url`, `status`
- `title`
- `text_excerpt`
- `links[]`
- `metrics` and `fetched_at`

### 2) Run HYDRA swarm browser CLI

```powershell
python -m hydra.cli_swarm --status
python -m hydra.cli_swarm --dry-run "research SCBE-AETHERMOORE on GitHub"
python -m hydra.cli_swarm --provider local --backend playwright "navigate to example.com and summarize"
python -m hydra.cli_swarm --provider hf --model mistralai/Mistral-7B-Instruct-v0.3 "find latest PQC migration notes"
```

## Workflow Decision Tree

1. Need simple extraction only:
- Use `hydra_terminal_browse.mjs`.

2. Need multi-agent action execution (navigate/click/type/verify):
- Use `python -m hydra.cli_swarm ...`.
- Start with `--dry-run` before live browser actions.

3. Need repeatable research trail:
- Save extraction JSON with `--out`.
- Keep file path in your task notes for traceability.

## Output Contract (Recommended)

When using terminal browse for governance/evidence tasks, persist output in this shape:

```json
{
  "url": "https://...",
  "resolved_url": "https://...",
  "status": 200,
  "title": "...",
  "text_excerpt": "...",
  "links": ["https://..."],
  "metrics": {
    "html_chars": 0,
    "text_chars": 0,
    "link_count": 0,
    "truncated": false
  },
  "fetched_at": "2026-02-22T00:00:00Z"
}
```

## Safety And Quality Gates

- Default to read-only browsing for discovery.
- For HYDRA swarm runs, prefer `--dry-run` first.
- Keep extraction deterministic:
  - fixed timeout
  - fixed max chars
  - deduplicated links
- Never embed secrets/tokens in captured artifacts.

## Resources

### scripts/
- `hydra_terminal_browse.mjs`: Node CLI for deterministic terminal browsing and evidence JSON export.

### references/
- `hydra-browser-surfaces.md`: quick map of HYDRA browser-related modules and test targets.
