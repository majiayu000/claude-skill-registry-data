---
name: mk:confluence
description: 'Routing skill — recommends the correct mk:confluence-* leaf for any Confluence Cloud task. Triggers: ''confluence'', ''wiki page'', ''spec page'', ambiguous Confluence intent. NOT an executor — every actual operation forks via a leaf skill.'
phase: on-demand
source: local
keywords:
  - confluence
  - confluence-router
  - routing-hub
  - atlassian-wiki
  - wiki
  - spec-page
when_to_use: Use when user has a Confluence intent but the specific leaf isn't clear. NOT for direct execution — forward to mk:confluence-{specific}.
user-invocable: true
owner: confluence
criticality: medium
status: active
runtime: claude-code
requires_external_service: ["confluence"]
default_enabled: false
dependency_edges:
  - id: mk:confluence-bulk
    type: peer
  - id: mk:confluence-collaborate
    type: peer
  - id: mk:confluence-page
    type: peer
  - id: mk:confluence-search
    type: peer
  - id: mk:confluence-spec-analyst
    type: peer
  - id: mk:cook
    type: peer
  - id: mk:intake
    type: peer
  - id: mk:jira
    type: peer
  - id: mk:jira-issue
    type: peer
  - id: mk:planning-engine
    type: peer
---

# mk:confluence — Routing Skill

This skill is a **pure routing layer**. Its sole purpose: identify the right `mk:confluence-*` leaf for the user's Confluence task, then point at it. **No execution.**

## Routing Table

| User intent                                                            | Leaf skill                    |
| ---------------------------------------------------------------------- | ----------------------------- |
| Get/create/update/delete a single page or blog post; copy/move/version | `mk:confluence-page`          |
| Search pages with CQL; list spaces; export results                     | `mk:confluence-search`        |
| Deep spec analysis: requirements, gaps, suggested stories              | `mk:confluence-spec-analyst`  |
| Bulk ops on 10+ pages (label, move, delete) — dry-run mandatory        | `mk:confluence-bulk`          |
| Comments, attachments, labels, watchers (collaboration surface)        | `mk:confluence-collaborate`   |

## Disambiguation

- User says skill name verbatim → route immediately
- Numeric token (likely page ID) + verb → match verb to leaf
- Uppercase short token (likely space key) + read intent → `mk:confluence-search`
- CQL syntax (`=`, `AND`, `OR`, `currentUser()`) → `mk:confluence-search`
- 10+ items / `bulk` / `batch` / `mass` keyword → `mk:confluence-bulk`
- Spec analysis intent (`requirements`, `acceptance criteria`, `analyze the spec`) → `mk:confluence-spec-analyst`
- **Labels:** `mk:confluence-collaborate` owns label CRUD (add/remove/list). `mk:confluence-page` does NOT duplicate — if user says "label page X", route to collaborate.
- **Comments / attachments / watchers:** always `mk:confluence-collaborate`, even if scoped to a single page
- Truly ambiguous → ask user one clarifying question

## Setup

See `references/install-and-auth.md` for one-time setup (`.claude/scripts/bin/setup-workflow` installs `confluence-assistant-skills` into `.claude/skills/.venv` per `scripts/requirements.txt`; populate `.meowkit/.env` with the 3 `MEOW_CONFLUENCE_*` vars).

## Shared Resources (used by leaves)

- `scripts/confluence-as.sh` — env-translating wrapper (`MEOW_CONFLUENCE_*` → `CONFLUENCE_*`, sets `CONFLUENCE_OUTPUT=json`, refuses settings.local.json fallback, gates non-Cloud URLs)
- `scripts/cql-sanitize.sh` — CQL injection guard for user-derived input
- `scripts/adf-to-md.sh` + `scripts/adf_to_md.py` — macro-aware ADF→Markdown walker (panel, decisionList/Item, taskList/Item, expand, mention, media, inlineCard preserved with explicit labels)
- `scripts/requirements.txt` — pip dependency manifest auto-discovered by `.claude/scripts/bin/setup-workflow`
- `scripts/smoke-live.sh` — manual live-creds smoke test
- `references/install-and-auth.md` — env vars, setup, Cloud-only gate, escape hatch
- `references/cli-idioms.md` — wrapper invocation patterns + safe-invocation rules + conversion-helper idioms

## Handoff

- `mk:planning-engine` accepts `--spec <report-path>` flag pointing at an existing `mk:confluence-spec-analyst` report; user runs spec-analyst FIRST, then passes path
- `mk:intake` recognizes Confluence URL/page-id as a 5th source; fetches page content directly via wrapper, does NOT auto-invoke spec-analyst
- `mk:jira` → sister hub for Jira ticketing; spec-analyst report pairs with `mk:jira-issue create` to turn extracted user stories into tickets (manual review required, `--with-commands` is opt-in)
- No write-back from `mk:cook` — Confluence write paths are out of scope

## Gotchas

- mk:confluence itself never executes; if you're in this skill thinking about wrapper commands, you're in the wrong place — forward to a leaf.
- Binary name is `confluence-as` (NOT `confluence` despite some upstream README docs). The wrapper handles this; leaves call the wrapper.
- Cloud-only — wrapper exits 3 on non-`*.atlassian.net` URLs. For Server/DC, users invoke MCP Atlassian directly per `references/install-and-auth.md`. Hub does NOT auto-fallback.
