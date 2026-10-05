---
name: mk:jira
description: 'Routing skill — recommends the correct mk:jira-* leaf for any Jira task. Triggers: ''jira'', ''jira ticket'', ambiguous Jira intent. NOT an executor — every actual operation forks via a leaf skill.'
phase: on-demand
source: local
keywords:
  - jira
  - jira-router
  - routing-hub
  - atlassian
  - mk-jira
  - ticket
when_to_use: Use when user has a Jira intent but the specific leaf isn't clear. NOT for direct execution — forward to mk:jira-{specific}.
user-invocable: true
owner: jira
criticality: medium
status: active
runtime: claude-code
requires_external_service: ["jira"]
default_enabled: false
dependency_edges:
  - id: mk:confluence
    type: peer
  - id: mk:cook
    type: peer
  - id: mk:intake
    type: peer
  - id: mk:jira-admin
    type: peer
  - id: mk:jira-agile
    type: peer
  - id: mk:jira-analyst
    type: peer
  - id: mk:jira-bulk
    type: peer
  - id: mk:jira-collaborate
    type: peer
  - id: mk:jira-dev
    type: peer
  - id: mk:jira-estimator
    type: peer
  - id: mk:jira-evaluator
    type: peer
  - id: mk:jira-fields
    type: peer
  - id: mk:jira-issue
    type: peer
  - id: mk:jira-jsm
    type: peer
  - id: mk:jira-lifecycle
    type: peer
  - id: mk:jira-ops
    type: peer
  - id: mk:jira-relationships
    type: peer
  - id: mk:jira-search
    type: peer
  - id: mk:jira-time
    type: peer
  - id: mk:planning-engine
    type: peer
  - id: mk:ship
    type: peer
---

# mk:jira — Routing Skill

This skill is a **pure routing layer**. Its sole purpose: identify the right `mk:jira-*` leaf for the user's Jira task, then point at it. **No execution.**

## Routing Table

| User intent                                  | Leaf skill              |
| -------------------------------------------- | ----------------------- |
| Get/create/update/delete a single issue      | `mk:jira-issue`         |
| Find issues by criteria; export; filters     | `mk:jira-search`        |
| Transition through workflow; assign; resolve | `mk:jira-lifecycle`     |
| Comments, attachments, watchers, notify      | `mk:jira-collaborate`   |
| Issue links, blockers, dependencies          | `mk:jira-relationships` |
| Worklogs, time tracking, time reports        | `mk:jira-time`          |
| Epics, sprints, backlog, story points        | `mk:jira-agile`         |
| Custom field discovery + configuration       | `mk:jira-fields`        |
| Bulk ops (10+ issues, dry-run mandatory)     | `mk:jira-bulk`          |
| Service Management (queues, SLAs, customers) | `mk:jira-jsm`           |
| Project/user/group/scheme administration     | `mk:jira-admin`         |
| Git/PR/branch-name integration               | `mk:jira-dev`           |
| Cache + project-context discovery            | `mk:jira-ops`           |
| Evaluate ticket complexity + inconsistencies | `mk:jira-evaluator`     |
| Estimate story points (heuristic)            | `mk:jira-estimator`     |
| Analyze ticket context + media; RCA          | `mk:jira-analyst`       |

## Setup

See `references/install-and-auth.md` for one-time setup (`.claude/scripts/bin/setup-workflow` installs `jira-as` into `.claude/skills/.venv`; populate `.meowkit/.env` with the 3 `MEOW_JIRA_*` vars).

## Shared Resources (used by leaves)

- `scripts/jira-as.sh` — env-translating wrapper (`MEOW_JIRA_*` → `JIRA_*`, sets `JIRA_OUTPUT=json`)
- `scripts/jql-sanitize.sh` — JQL escaping for user-derived terms
- `scripts/requirements.txt` — pip dependency manifest auto-discovered by `.claude/scripts/bin/setup-workflow`
- `references/install-and-auth.md` — setup, exit codes, DC/mTLS caveats
- `references/cli-idioms.md` — verified jira-as syntax + `jq` projection rules
- `references/safety-framework.md` — 4-tier safety model
- `references/evaluation-rubric.md` — used by `mk:jira-evaluator`
- `references/estimation-guide.md` — used by `mk:jira-estimator`
- `../jira-fields/references/field-discovery.md` — used by `mk:jira-fields` (moved from `jira/references/`)

## Handoff

- `mk:intake` → recommends `mk:jira-*` leaf based on triage
- `mk:cook` (build pipeline) → may invoke `mk:jira-issue` to create implementation tickets
- `mk:ship` (ship pipeline) → may invoke `mk:jira-dev` for branch-name + PR-description
- `mk:planning-engine` → consumes Jira tickets via this hub for sprint planning analysis (`mk:jira-evaluator` / `mk:jira-estimator` outputs enrich the planning report)
- `mk:confluence` → sister hub for Confluence Cloud; `mk:planning-engine` accepts both Jira tickets (`--tickets`) and Confluence specs (`--spec <report-path>`) as input

## Gotchas

- mk:jira itself never executes; if you're in this skill thinking about jira-as commands, you're in the wrong place — forward to a leaf.
- Escape hatch: if jira-as is unusable (mTLS, multi-profile), users may invoke Atlassian MCP directly per `references/install-and-auth.md`. The router does NOT auto-fallback.
