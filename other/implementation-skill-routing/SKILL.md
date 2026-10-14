---
name: implementation-skill-routing
description: "Trigger: plan Skills field, implementation skill routing, execution skill selection. Select the smallest implementation skill set for each work group."
license: MIT
metadata:
  author: andresnator
  version: "3.0.0"
  status: testing
---

# Implementation Skill Routing

Use this skill to draft or validate a plan work group's `Skills:` field.

## Contract

Every work group requires `Skills: <csv|none>`. Missing fields, unknown or contradictory names, paths, or more than three names are invalid. Split work by responsibility when a group needs more than three skills.

Planners select names without loading implementation skill bodies. Executors load only the selected bodies within their assigned scope.

## Source

- Read `.ai/atl/skill-registry.md` by its literal path when present. A valid registry has `## OpenCode Skills`, `## Agent Skills`, and `## Claude Skills`, each with `Description | Skill | Location` columns.
- Match work signals only against `Description` and return only names from `Skill`.
- Treat `Location` as diagnostic information only. Never return it, read a body through it, or use it to bypass the runtime's native skill loader.
- Consult the runtime skill catalog when the registry is absent, malformed, has no matching description, or a selected skill is no longer available. Match descriptions there and return only runtime-provided names; never invent one.
- Do not accept the legacy `## Skills` section or `Trigger` column.

## Selection

For each work group:

1. Derive direct signals from Behavior, tasks, `Files:`, and `Verify`.
2. Select a skill only when its description directly matches assigned work; do not infer adjacent capabilities.
3. Exclude skills for planning, discovery, review, delivery, or Git even when a description matches.
4. Remove duplicates and preserve source order. Return at most three names.
5. Use `none` when no eligible description matches.

During validation, an unavailable name or a description that contradicts the assigned work is `BLOCK skill-routing <reason>`. Never replace, ignore, or guess around it.

## Boundaries

- Selected skills cannot expand behavior, `Files:`, validation, Git ownership, or output contracts.
- Return names, never paths. Use an ordered comma-separated list or `none`; the caller owns formatting and execution scope.
