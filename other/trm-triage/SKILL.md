---
name: trm-triage
description: Autonomous task card triage engine applying YAGNI evaluation, reversibility classification, and GitHub Issue promotion payloads.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: none
---

# TRM Triage

Autonomous task card triage engine applying YAGNI evaluation, reversibility classification, and GitHub Issue promotion payloads.

## Trigger

Run TRM task card triage on staged cards in `.harness/tasks/pending` or request backlog evaluation.

## Input Schema

- `rootDir`: Path to workspace root directory (default: `.`)
- `dryRun`: Whether to run in read-only analysis mode (default: `false`)

## Output Schema

- `totalCards`: Total count of scanned task cards
- `triagedCards`: Array of card triage objects including priority, status, YAGNI decision, and drafted issue payload

---

**For Setup, Requirements, Inputs/Outputs, Error Codes, Testing:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
