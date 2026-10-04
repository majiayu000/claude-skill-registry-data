---
name: ax-extract-workflow
description: Use when reconstructing how a shipped feature, commit, date, or artifact was produced from local ax session evidence.
---

# ax Extract Workflow

## Overview

Reconstruct the workflow behind a shipped artifact from local ax data. Resolve an anchor, find the relevant sessions, inspect turns, tools, skills, commits, and delegations, then write a compact account of what happened.

This skill assumes `ax` is installed, session data has been ingested, and the local ax database is reachable.

## When to Use

Use this skill when the user asks for:
- How a feature, PR, demo, or artifact was shipped
- What made a past result work
- The workflow around a date, commit, topic, or repository event
- The sessions, tools, skills, or decisions that led to an artifact
- A repeatable recipe based on prior local agent work

## Do not use

Do not use this skill for:
- Generic recent activity summaries
- New implementation planning before past evidence is inspected
- Project status reports not tied to a concrete artifact, date, or commit
- Reconstructing work when local ax data is unavailable

## Instructions

1. Identify the anchor:
   - Commit SHA: use it directly.
   - Date: use a small window around that date.
   - Topic or artifact name: search commits first.
   - Current repo, recent work: inspect recent sessions for the repo.
2. Resolve candidate sessions:

```bash
ax recall "<topic>" --sources=commit --json
ax sessions near <sha> --json
ax sessions around <date> --days=3 --json
ax sessions here --days=14 --json
```

3. Pick up to five sessions. Prefer sessions with high turn counts, matching commits, related files, or relevant tool and skill usage.
4. Inspect each selected session:

```bash
ax sessions show <id> --json
ax sessions show <id> --by-role
ax sessions show <id> --expand=<subagent-uuid>
```

5. If ax cannot connect to its database, tell the user to start ax services and stop. Do not invent evidence.
6. Write the reconstruction from evidence:
   - Ordered workflow arc: what happened first, next, and last.
   - Skill/tool role: what each important skill or tool contributed.
   - Key decisions: user steering points or tradeoffs that changed the work.
   - Repeatable recipe: how to run a similar workflow again.

## Output

Return Markdown with:
- A one-paragraph summary
- An ordered workflow timeline
- Key evidence with session ids, commits, or commands
- A short reproducible recipe when enough evidence exists

Keep the tone factual. Cite local evidence. Mark unknowns instead of filling gaps.
