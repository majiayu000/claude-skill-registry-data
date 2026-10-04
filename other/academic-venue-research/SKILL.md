---
name: academic-venue-research
description: "Research target venue requirements and writing style for CS/AI/ML papers. Produces venue-brief.md with submission requirements and detailed writing style analysis. Use when: researching target journal/conference requirements, analyzing writing style of target venue, generating venue brief for paper writing, checking submission guidelines. Triggers on: venue research, 期刊调研, 目标期刊, writing style analysis, 写作风格分析, venue requirements, submission guidelines, 投稿要求, journal style, conference format."
---

# Academic Venue Research

将此 skill 视为"期刊调研代理"，负责调研目标期刊/会议的投稿要求和写作风格。

## Router Protocol

1. Read `manifest.yaml`. It declares `always_load` files, `axes`, and `references.on_demand`.
2. Read every file listed under `always_load`. These are the skill's binding rules — not reference material.
3. Apply the loaded material as constraints:
   - `stance.md` defines core rules, source hierarchy, and scope.
   - `red-lines.md` defines absolute prohibitions. Do not negotiate these.
   - `output-contract.md` defines deliverables per mode.
4. Detect the mode using the manifest's `mode` axis: `full-venue-research`, `requirements-only`, or `style-only`. Source hierarchy rule: official guidelines > template docs > accepted paper observations > agent knowledge. If ambiguous, ask one concise question.
5. Echo the selected mode to the user before executing.
6. Reach for `references/` only when the manifest's `references.on_demand` condition is satisfied.

## Modes

| Mode | Use when |
|---|---|
| `full-venue-research` | Venue + local style papers or full brief request |
| `requirements-only` | Venue name only, no style analysis needed |
| `style-only` | Local style reference library, no requirements research |

## Agent Dispatch

`agents/venue-research-agent.md` is dispatched by the orchestrator at Step 4. The agent returns Venue Brief Markdown content; it must not write files directly during orchestrated use. File writes are owned by the orchestrator.

## Independent Use

| Input | Mode | Priority | Behavior |
|---|---|---|---|
| Venue + local style corpus | full-venue-research | 1 (explicit) | Full 4-step workflow |
| Venue only | requirements-only | 2 (single feature) | Requirements only |
| Local style corpus only | style-only | 3 (path trigger) | Style analysis only |

| Scenario | Recommended |
|---|---|
| Just researching venue | This skill (standalone) |
| Using results for paper writing | academic-paper-writer orchestrator |
