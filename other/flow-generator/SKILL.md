---
name: flow-generator
description: Drafts screen-level flow definitions from a selected solution direction
version: 1.0.0
author: Mattermost Design Team
tags: [ux-spec, flows, phase-5, ai-draft]
allowed-tools: Read, Grep, Glob
---

# Flow Generator

Translates one Phase 4 solution direction plus its PRD user stories into a
screen-level flow definition set: screens, transitions, and decision points,
expressed as Mermaid decision-tree source.

## Inputs

- Direction id (one entry from `gates.phase_4.carried_forward[]`)
- That direction's `solution_direction` content
- PRD user stories from `artifacts.prd` relevant to the direction

## Output

One flow-definition set per invocation, labeled `[AI DRAFT]`.

## Rules

- One direction per invocation. `flow-agent` composes this skill once per entry
  in `gates.phase_4.carried_forward[]` — never combine directions in one call.
- Never invent requirements not present in the PRD. A flow step that seems
  needed but isn't backed by a PRD requirement is flagged `[VERIFY WITH PM]`,
  not assumed or fabricated.
- If the designer has supplied their own flow definitions for a direction, this
  skill is NOT invoked for that direction — the designer's flows are audited
  instead of a generated set.
- Emit the flow as Mermaid decision-tree source in a fenced ```mermaid block
  inside the markdown flow definition (renders in GitHub-flavored markdown;
  Confluence Cloud shows the source unless a Mermaid macro is configured).
