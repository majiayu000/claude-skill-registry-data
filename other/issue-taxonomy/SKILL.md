---
name: issue-taxonomy
description: Classify GitHub issues with visible high-level type labels such as feature, bug, change, or chore in addition to agent-archetype routing labels. Use when creating or refining issues so both agents and human reviewers can understand the scope and nature of the work at a glance.
---

# Issue taxonomy

## Rule
Every issue should carry both:
- an agent-archetype or workflow-routing label where relevant
- a high-level issue-type label describing what kind of work it is

## Common issue-type labels
- `feature`
- `bug`
- `change`
- `chore`
- `docs`
- `investigation`
- `spike`

## Why it matters
Issue type labels help:
- human reviewers understand scope quickly
- agents reason about the expected workflow
- Orchestrator route work more consistently
- reporting and backlog slicing stay readable

## Guidance
- prefer one primary issue-type label
- if work changes shape materially, update the label
- do not rely on title wording alone when a label can make scope explicit
