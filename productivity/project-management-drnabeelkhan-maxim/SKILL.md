---
skill_id: project-management
name: Project Management
description: "Plan and track delivery — plan, sprint, project, timeline, milestone, task breakdown, backlog, Kanban, RACI, changelog governance. The COO office's workflow coordination domain."
version: 1.0.0
category: project-management
office: COO
lead_agent: planner
triggers:
  - plan
  - sprint
  - project
  - delivery
  - timeline
  - milestone
  - task breakdown
  - backlog
  - Kanban
  - RACI
  - release coordination
  - workflow optimization
collaborates_with:
  - experiment-tracker
  - project-shipper
  - sprint-prioritizer
  - workflow-optimizer
  - knowledge-base-curator
  - changelog-writer
  - tool-evaluator
  - implementer
  - release-manager
  - tester
  - security-analyst
---

# Project Management -- Domain Dispatcher

> Office: COO | Lead: planner
> Sub-skills: 3 | Frameworks: RICE, MoSCoW, Shape Up, Kanban, Scrum

## Purpose

Sprint planning, delivery tracking, experiment management, knowledge management, and changelog governance. The COO's primary domain for workflow coordination across all Maxim offices and delivery phases. Orchestrators (planner, implementer, reviewer, tester, release-manager) use this domain for cross-domain coordination.

## Sub-Skill Routing

| Task Signal | Routes To | SKILL.md Path |
|---|---|---|
| A/B testing management, experiment design, result analysis | experiment-tracker | project-management/experiment-tracker/SKILL.md |
| Project delivery, release coordination, timeline management | project-shipper | project-management/project-shipper/SKILL.md |
| Sprint planning, backlog prioritization, sprint goals, velocity | sprint-prioritizer | project-management/sprint-prioritizer/SKILL.md |

## Activation

This domain activates when:
- User invokes `/mxm-coo`
- Task contains keywords: plan, sprint, project, delivery, timeline, milestone, task breakdown, backlog prioritization, Kanban, RACI, Stage-Gate, OKRs, sprint retrospective, release coordination, workflow optimization, changelog, tool evaluation

## Behavioral Layer

- Confidence: 🟢 HIGH
- Compliance: reads project-manifest.json
- Handoff: writes .mxm-skills/agents-handoff.md
- Frameworks: RICE, MoSCoW, Shape Up, Kanban, Scrum, RACI, Stage-Gate

## External Sources

- Primary: community-packs/claude-skills-library/project-management/
- Merge rule: Maxim ALWAYS WINS -- behavioral science + proactive triggers + confidence tagging non-negotiable

---
*Maxim Project Management Skill -- Version 1.0.0*
*Maxim behavioral layer: ACTIVE | External merge: project-management ABSORBED | Confidence: 🟢 HIGH*

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
