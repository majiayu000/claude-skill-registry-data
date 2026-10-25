---
name: saas-quick-design
description: "Lightweight spec for small changes — tuning adjustments, minor workflow tweaks. Embeds directly into stories; skips full PRD."
argument-hint: "[brief description of the change]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion, Bash(bash "*/.claude/skills/saas-quick-design/../../hooks/yaml-helper.sh" resolve_config *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,automation,workflow`



# Quick Design

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

This is the **lightweight design path** for changes that don't need a full PRD.
Full PRD authoring via `/saas-design-system` is the heavyweight path. Use this skill
for work under about one week of implementation — tuning adjustments, minor
behavioral tweaks, small additions to existing systems, or standalone features too
small to warrant a full document. Most tweaks are hours; the one-week ceiling is
the limit for a New Small System (see the categories below).

**Output:** `design/quick-specs/[name]-[date].md`

**When to run:** Anytime a change is too small for `/saas-design-system` but too
meaningful to implement without a written rationale.

---

Every `AskUserQuestion` call follows `.claude/docs/automation-modes.md`
(collaborative asks always · guided major-only · autonomous logs and proceeds;
`automation_always_ask` categories always prompt).

## 1. Classify the Change

First, read the argument and determine which category this change falls into:

- **Tuning** — changing numbers or balance values in an existing system with no
  behavioral change (most minimal path). Example: "increase jump height from 5
  to 10 seats", "increase API rate limit from 60 to 120 req/min".
- **Tweak** — a small behavioral change to an existing system that introduces no
  new states, branches, or systems. Example: "make dash invincible on frame 1",
  "allow combo to cancel into roll".
- **Addition** — adding a small feature or workflow tweak to an existing system that may introduce
  1-2 new states or interactions. Example: "add coupon discount validation to checkout",
  "add CSV export option to data table".
- **New Small System** — a standalone feature small enough that it has no
  existing PRD and is under approximately one week of implementation work.
  Example: "achievement popup system", "simple day/night visual cycle".

If the change does NOT fit these categories — it introduces a new system with
significant cross-system dependencies, requires more than one week of
implementation, or fundamentally alters an existing system's core rules — stop
and redirect to `/saas-design-system` instead. Verdict: **REDIRECTED** — use
`/saas-design-system` for this change.

If there is no argument, ask the user to describe the change (plain text prompt), then classify it using the criteria above.

Present the inferred classification using `AskUserQuestion`:
- Prompt: "I've classified this as **[inferred type]** — [brief reason]. Is that correct?"
- Options:
  - `[A] Yes — [inferred type] is correct`
  - `[B] Tuning — changing numbers or balance values only`
  - `[C] Tweak — small behavioral change to an existing system`
  - `[D] Addition — adding a small feature or workflow tweak to an existing system`
  - `[E] New Small System — standalone feature, under one week of work`
  - `[F] This is too large — redirect me to /saas-design-system`

If [F]: stop. Verdict: **REDIRECTED** — use `/saas-design-system` for this change.
Otherwise: proceed with the selected type.

---

## 2. Context Scan

Before drafting anything, read the relevant context. Read the PRD and the systems
index by section: check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise find the headings you need with the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Grep tool (pattern `^#`, content mode) and Read those ranges with offset and limit.

- Search `design/prd/` for the PRD most relevant to this change. Read the
  sections that this change would affect. If no PRD covers this system — usually
  the case at `workflow: minimal`, where `design/product-brief.md` and the stories are
  the design record — read the brief's lines for it and the story the change
  touches instead, report "No PRD for [system] — using the brief and [story
  path]", and give the brief as the spec's PRD Reference.
- Check whether `design/prd/features-modules-index.md` exists. If it does, read it to
  understand where this system sits in the dependency graph and what tier it
  belongs to. If it does not exist, note "No systems index found — skipping
  dependency tier check." and continue.
- Check `design/quick-specs/` for any prior quick specs that touched this
  system — avoid contradicting them.
- If this is a Tuning change, also check `assets/data/` for the data file that
  holds the relevant values.

Report what was found: "Found PRD at [path]. Relevant section: [section name].
Prior quick specs for this system: [each path, and whether it agrees or
conflicts with this change — or "none"]." Name a prior spec even when it
agrees — "no conflicts" alone reads the same as "no prior specs".

---

## 3. Draft the Quick Design Spec

Use the appropriate spec format for the change category.

### For Configuration / Parameter changes

Produce a single table:

```markdown
# Quick Design Spec: [Title]

**Type**: Configuration Tuning
**System**: [System name]
**PRD Reference**: `design/prd/[filename].md` — Configuration Parameters section
**Date**: [today]

## Change

| Parameter | Old Value | New Value | Rationale |
|-----------|-----------|-----------|-----------|
| [param]   | [old]     | [new]     | [why]     |

## Configuration Parameter Mapping

Maps to PRD Configuration Parameter: [parameter name and its documented range].
New value is [within / at the edge of / outside] the documented range.
[If outside: explain why the range should be extended.]

## Acceptance Criteria

- [ ] [Parameter] reads [new value] from `config/[file].json` or environment variables
- [ ] Behavior difference is observable in [specific context]
- [ ] No regression in [related behavior]
```

### For Tweak and Addition changes

```markdown
# Quick Design Spec: [Title]

**Type**: [Tweak / Addition]
**System**: [System name]
**PRD Reference**: `design/prd/[filename].md`
**Date**: [today]

## Change Summary

[1-2 sentences describing what changes and why.]

## Motivation

[Why is this change needed? What user experience problem does it solve?
Reference the relevant MDA aesthetic or user feedback if applicable.]

## Design Delta

Current PRD says (quoting `design/prd/[filename].md`, [section]):

> [exact quote of the relevant rule or description]

This spec changes that to:

[New rule or description, written with the same precision as a PRD Detailed
Rules section. A programmer should be able to implement from this text alone.]

## New Rules / Values

[Full unambiguous statement of the replacement content. If this introduces
new states, list them. If it introduces new parameters, define their ranges.]

## Affected Systems

| System | Impact | Action Required |
|--------|--------|-----------------|
| [system] | [how it is affected] | [update PRD / update data file / no action] |

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]
- [ ] No regression: [the original behavior this must not break]

## PRD Update Required?

[Yes / No]
[If yes: which file, which section, and what the update should say.]
```

### For New Small System changes

Use a trimmed PRD structure. Include only the sections that are directly
necessary — skip User Stories & Personas, full Formulas, and Edge Cases unless the
system specifically requires them.

```markdown
# Quick Design Spec: [Title]

**Type**: New Small System
**Scope**: [1-2 sentence description of what this system does and doesn't do]
**Date**: [today]
**Estimated Implementation**: [hours]

## Overview

[One paragraph a new team member could understand. What does this system do,
when does it activate, and what does it produce?]

## Core Rules

[Unambiguous rules for the system. Use numbered lists for sequential behavior
and bullet lists for conditions. Be precise enough that a programmer can
implement without asking questions.]

## Configuration Parameters

| Parameter | Default | Range / Format | Category | Rationale |
|-----------|---------|----------------|----------|-----------|
| [name]    | [value] | [min–max/type] | [quota/timeout/flag] | [why this default] |

All values must live in `config/[appropriate-file].json` or environment variables, not hardcoded.

## Acceptance Criteria

- [ ] [Functional criterion: does the right thing]
- [ ] [Functional criterion: handles the edge case]
- [ ] [Experiential criterion: delivers expected value — what a usability test validates]
- [ ] [Regression criterion: does not break adjacent system]

## Systems Index

This system is not currently in `design/prd/features-modules-index.md`.
[If it should be added: suggest which layer and priority tier.]
[If it is too small to track: state "This system is below systems-index
tracking threshold — quick spec is sufficient."]
```

---

## 4. Approval and Filing

Present the draft to the user in full. Then use `AskUserQuestion`:
- Prompt: "Here's the Quick Design Spec draft. How do you want to proceed?"
- Options:
  - `[A] Approve — write it as shown`
  - `[B] Revise — I'll describe what to change`
  - `[C] This grew too large — redirect to /saas-design-system instead`

If [B]: collect the requested changes, revise the draft, and re-present this widget.
If [C]: stop. Verdict: **REDIRECTED** — use `/saas-design-system` for this change.

If [A]: ask "May I write this Quick Design Spec to
`design/quick-specs/[kebab-case-title]-[YYYY-MM-DD].md`?"

Use today's date in the filename. The title should be a kebab-case description
of the change (e.g., `jump-height-tuning-2026-03-10`,
`coupon-validation-addition-2026-03-10`).

If yes, create the `design/quick-specs/` directory if it does not exist, then
write the file.

If a PRD update is required (flagged in the spec), ask separately after
writing the quick spec:

"This spec modifies rules in [System Name]. May I update
`design/prd/[filename].md` — specifically the [section name] section?"

Show the exact text that would be changed (old vs. new) before asking. Do not
make PRD edits without explicit approval.

---

## 5. Handoff

After writing the file, output:

```
Quick Design Spec written to: design/quick-specs/[filename].md
Type: [Tuning / Tweak / Addition / New Small System]
System: [system name]
PRD update: [Required — pending approval / Applied / Not required]

Next step: This spec is ready for `/saas-story-readiness` validation before
implementation (at `workflow: minimal`, go straight to `/saas-dev-story`). Reference this spec in the story's PRD Reference field.
```

### Pipeline Notes

Verdict: **COMPLETE** — quick design spec written and ready for implementation.

Quick Design Specs **bypass** `/saas-design-review` and `/saas-review-all-prds` by
design. They are for small, low-risk, well-scoped changes where the cost of
the full review pipeline exceeds the risk of the change itself.

Redirect to the full pipeline if any of the following are true:
- The change adds a new system that belongs in the systems index
- The change significantly alters cross-system behavior or a system's
  contracts with other systems
- The change introduces new user-facing workflows that affect the
  product's MDA aesthetic balance
- Implementation is likely to exceed one week of work

In those cases: "This change has grown beyond quick-spec scope. I recommend
using `/saas-design-system` to author a full PRD for this."

---

## Recommended Next Steps

- Run `/saas-story-readiness [story-path]` to validate the story before implementation begins (skip at `rigor: minimal` — `/saas-dev-story` directly) — reference this spec in the story's PRD Reference field
- Run `/saas-dev-story [story-path]` to implement once the story passes readiness checks
- If the change is larger than expected, run `/saas-design-system [system-name]` to author a full PRD instead
