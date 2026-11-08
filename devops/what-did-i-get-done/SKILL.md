---
name: what-did-i-get-done
description: Summarize authored commits over a user-specified time period into a concise status update.
source: https://github.com/shaneholloman/cursor-plugins/tree/main/cursor-team-kit/skills/what-did-i-get-done
license: MIT
disable-model-invocation: true
---

# What Did I Get Done

Use when user asks for short, high-signal work summary for a specific time range (yesterday, last 3 days, last week).

## Workflow

1. Resolve requested time window to concrete dates.
2. Read commits authored by current git user email in range.
3. Exclude merges and uncommitted changes unless explicitly requested.
4. Inspect diffs only when messages too vague for factual summary.
5. Synthesize most important changes into concise status update.
6. Include actual date range.

## Guardrails

- Extremely concise, information-dense.
- Prioritize substantial behavior, architecture, infrastructure, workflow changes.
- Omit cosmetic-only changes unless main work.
- Don't infer intent/motivation; describe changes functionally.
- Git email missing → ask user to set before proceeding.

## Output

- One short status summary.
- Real date range.
- Optional 2-5 bullets for major changes.
