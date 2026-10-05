---
description: Use Obsidian vault as a structured state bus for active work, decisions and progress
---

# Obsidian State

Obsidian (`vault/`) is not generic memory. It is the operational state layer between agents and sessions.

## Always use it to:
- Find or create the active NID
- Store progress, decisions and blockers
- Maintain `repo_paths` and `services` tags
- Write session handoff state
- Keep retrieval surfaces clean and structured

## Never use Obsidian for:
- Storing raw code dumps
- Duplicating full docs already in repo
- Unstructured note spam
- Storing secrets or credentials

## Minimum required updates per task:
- `status` (queued → in_progress → done)
- `repo_paths` (files/dirs affected)
- `decisions` (ADR references)
- Next actions
- `updated_at`

## Vault Structure:
- `00-Inbox/` — Raw captures, unsorted notes
- `10-Queue/` — Triaged tasks with NIDs
- `20-Specs/` — BMAD specs linked to NIDs
- `30-Architecture/` — ADRs and architecture notes
- `40-Runbooks/` — Operational procedures and diagnoses
- `50-DB/` — Schema snapshots and migration notes
- `60-Observability/` — Session logs, monitoring notes
- `90-Index/` — Active NIDs, Decisions, Repo Map, By Service, Blocked Work

## Frontmatter Template:
```yaml
---
nid: YYYYMMDD-HHMM-short-slug
status: queued
area: []
repo_paths: []
decisions: []
related_commands: []
services: []
updated_at: ISO-8601
owner: opencode
---
```
