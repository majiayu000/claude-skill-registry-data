---
name: jira
description: "Query Jira with JQL, manage issue fields and workflows, and plan scoped REST updates for project operations."
category: productivity
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["jira", "jql", "agile", "workflows", "rest-api", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Jira Project Tracking AI Skill Guide

## Overview & Engine Architecture

Jira tracks work items (issues) through workflows with statuses, transitions, and fields. Boards and sprints organize delivery; JQL queries filter issues. Automation rules can react to events. Agents write precise JQL, avoid automation loops, keep workflows simple, and use the REST API carefully with least-privilege tokens.

```
Projects -> Issues (fields)
         -> Workflows (statuses/transitions)
         -> Boards / sprints
         -> Automation / REST API
```

## When to use this skill

- Building filters, boards, and saved JQL
- Designing lightweight workflows
- Bulk-updating issues via API during migrations
- Reviewing noisy automation rules

## Operational directives

1. Prefer fewer statuses; map real handoffs, not aspirational bureaucracy.
2. Name custom fields carefully; avoid duplicates (`Start Date` vs `Start date`).
3. Automation: guard with conditions; never create infinite ping-pong transitions.
4. JQL should be selective enough for humans and APIs (watch result caps).
5. Store API tokens as secrets; scope to needed permissions.

## Useful JQL

```text
project = APP AND status = "In Progress" AND assignee = currentUser()
ORDER BY updated DESC

project = APP AND sprint in openSprints() AND type in (Bug, Story)

project = APP AND resolution is EMPTY AND updated <= -14d
```

## REST sketch

```bash
# List issues via search (Cloud APIs evolve - verify current endpoint)
curl -s -u email:token \
  -H "Accept: application/json" \
  "$JIRA_BASE/rest/api/3/search?jql=project%3DAPP"
```

## Workflow hygiene

| Smell | Better approach |
| --- | --- |
| 15+ statuses | Collapse to Todo / Doing / Done + optional Blocked |
| Required fields on every transition | Require only at the gate that needs them |
| Automation comments on every edit | Filter to meaningful events |
| Everyone is admin | Role-based scheme permissions |

## Best practices

- Link issues to PRs/commits with clear keys in branch names (`APP-123-...`).
- Use components or labels consistently; document the taxonomy.
- Separate bug vs story workflows only if states truly differ.
- Archive stale projects instead of leaving eternal noise.

## Limitations

- Jira Cloud vs Data Center APIs and permissions differ.
- Advanced Roadmaps / Plans features depend on license.
- Marketplace apps add fields/behaviors this skill cannot fully cover.

## Related skills

- `@linear` - lighter issue tracking alternative
- `@confluence` - long-form docs linked from epics
- `@github-actions` - CI status next to issue keys
