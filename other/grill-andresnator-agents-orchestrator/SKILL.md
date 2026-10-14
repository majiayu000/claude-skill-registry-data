---
name: grill
description: "Trigger: grill me, grill with docs, grill me sdd, grill code, grill docs open, entrevistame, entrevistame sdd. Relentless interview router for plain, docs, or neutral planning."
license: MIT
metadata:
  author: Matt Pocock
  adapted_by: andresnator
  source: https://github.com/mattpocock/skills
  status: testing
  version: "6.0.0"
---

## Modes

| Trigger | Mode | Result |
| --- | --- | --- |
| `grill me`, `grill code`, `entrevistame` | plain | `grilling` interview |
| `grill with docs`, `grill docs open` | docs | interview plus approved domain notes |
| `grill me sdd`, `entrevistame sdd` | plan | one approved neutral plan |

## Rules

- Ask each open-ended question directly in normal chat, one at a time, then stop. Add `Recommendation: ...` only when useful.
- Use the `question` tool only for closed confirmations, modes, ratings, or enumerated choices.
- Explore discoverable answers instead of asking. Preserve the user's language; artifacts default to English.
- Plan mode is planning-only: no code edits, builds, installs, tests, commits, or push. The approved plan is the only write.

## Flow

- Plain: load `grilling`; interview until the decision is clear.
- Docs: also load `domain-modeling`; write notes only with approval.
- Plan: confirm a kebab-case slug and collision handling. Interview Outcome, Scope, Behavior, Approach, Work groups, Dependencies, Verify, Risks, and Execution guidance. Load `execution-plan` and `implementation-skill-routing`; never load implementation skill bodies. Record the result for every work group. Ask once to write one neutral plan. Use `.ai/deep-planner/plans/<slug>.md` when the active primary owns that path; otherwise return the complete draft and direct the user to `deep-planner`. On refusal, keep the draft in chat.

Return the current question or conclusion, write status, path, and unresolved decisions. Missing skills are reported, never silently skipped.

## Attribution

Inspired by Matt Pocock's grilling skills at <https://github.com/mattpocock/skills>.
