---
name: weekly-review
description: Produce a short weekly synthesis of authored commits with highlights by bugfix, tech debt, and net-new work.
source: https://github.com/shaneholloman/cursor-plugins/tree/main/cursor-team-kit/skills/weekly-review
license: MIT
disable-model-invocation: true
---

# Weekly Review

Use for weekly recap of shipped work — status updates, retros, planning.

## Workflow

1. Current git user email from repo config.
2. Review window: default last 7 days; 7-10 only to cover work week.
3. Collect authored commits, exclude merges.
4. Inspect diffs only enough to avoid overstating vague messages.
5. Group into 2-5 concise bullets.
6. Classification paragraph: bug fixes, tech debt, net-new.

## Guardrails

- Short, executive-readable.
- Claims based on commit history + inspected diffs only.
- Git email missing → ask user to set before proceeding.
- Uncommitted work only when explicitly asked.

## Output

- Date range used.
- 2-5 bullet weekly summary.
- Brief classification: bugfix, tech debt, net-new.
