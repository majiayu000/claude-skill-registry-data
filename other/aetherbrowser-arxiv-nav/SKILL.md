---
name: aetherbrowser-arxiv-nav
description: "Navigate arXiv papers and topic searches through AetherBrowser for research extraction workflows. Use when collecting abstracts, paper metadata, and evidence snapshots from arxiv.org."
---

# AetherBrowser ArXiv Nav

## Workflow

1. Route to UM research lane.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\browser_chain_dispatcher.py --domain arxiv.org --task research --engine playwriter`

2. Open search or direct paper.
- Search: `https://arxiv.org/search/?query=<topic>&searchtype=all`
- Paper: `https://arxiv.org/abs/<id>`

3. Verify page and extract headline context.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task title`
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task snapshot`

4. Persist evidence in artifacts.
- Ensure assignment packet exists in `artifacts/agent_comm/github_lanes/cross_talk.jsonl`.

## Rules

- Prefer abstract pages over PDF for fast metadata reads.
- Keep extraction deterministic: title, authors, abstract, categories, date.
- If blocked, route fallback through standard fetch pipeline.
