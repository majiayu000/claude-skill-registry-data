---
name: trello
description: "Organize Trello boards and cards, configure Butler automation or Power-Ups, and perform scoped REST updates."
category: productivity
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["trello", "kanban", "boards", "butler", "productivity", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Trello Kanban Boards AI Skill Guide

## Overview & Engine Architecture

Trello is a card-and-list kanban system. Boards hold lists; cards carry checklists, labels, due dates, attachments, and members. Butler (automation) and Power-Ups extend behavior; the REST API moves cards and mirrors data elsewhere. Agents keep list counts small, use labels consistently, and prevent Butler from creating card ping-pong.

```
Workspaces
   -> Boards
       -> Lists -> Cards (checklists, labels, due dates)
       -> Butler rules / Power-Ups
API tokens -> integrations and mirrors
```

## When to use this skill

- Standing up lightweight team kanban boards
- Writing Butler rules for triage and due-date nudges
- Automating card create/move via API
- Migrating from messy free-form boards to a clear WIP flow

## Operational directives

1. Cap WIP: fewer lists (`Backlog`, `Doing`, `Review`, `Done`) beat elaborate stage maps.
2. Labels need a legend on the board description; retire unused colors.
3. Butler: one clear trigger per rule; avoid move-on-label that also sets the same label.
4. Archive Done periodically; giant Done lists slow boards.
5. Protect API keys; use read-only tokens for dashboards.

## API sketch

```bash
# Create a card
curl -s -X POST "https://api.trello.com/1/cards" \
  -d "idList=$LIST_ID" \
  -d "name=Fix checkout tax rounding" \
  -d "desc=Repro in staging; see issue APP-42" \
  -d "key=$TRELLO_KEY" \
  -d "token=$TRELLO_TOKEN"
```

## Butler hygiene

| Smell | Better approach |
| --- | --- |
| Auto-move + auto-comment on every attachment | Comment only on member join or due date |
| Cards bouncing between lists | Single source rule; disable overlapping Power-Ups |
| Checklist templates never completed | Shorter Definition of Done checklist |
| Personal boards for shared work | Team board with explicit membership |

## Best practices

- Card titles state the outcome; first comment or description holds context links.
- Use due dates for external commitments, not every internal micro-step.
- Mirror engineering work to Jira/GitHub when audit trails matter; keep Trello for lightweight coordination.
- Prefer board copy from a template over recreating lists each quarter.

## Limitations

- Enterprise permissions, Butler quotas, and Power-Up availability vary by plan.
- API rate limits apply; batch with care.
- Advanced reporting is weaker than Jira/Asana analytics - export or integrate if needed.

## Related skills

- `@asana` - richer tasks, fields, and dependencies
- `@jira` - formal software delivery workflows
- `@zapier` - connect Trello to Slack/email without code
