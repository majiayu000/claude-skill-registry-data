---
name: quick-design
description: "Lightweight design spec for small changes — tuning adjustments, minor mechanics, balance tweaks. Skips full CDD authoring when a system CDD already exists or the change is too small to warrant one. Produces a Quick Design Spec that embeds directly into story files."
argument-hint: "[brief description of the change]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit
---

## User Guide

- When to use: Lightweight design spec for small changes — tuning adjustments, minor mechanics, balance tweaks. Skips full CDD authoring when a system CDD already exists or the change is too small to warrant one. Produces a Quick Design Spec that embeds directly into story files.
- Inputs: Command arguments: `/quick-design [brief description of the change]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before drafting a quick design:
- `design/cdd/game-concept.md` -> **[Game]** keep the lightweight game spec workflow for mechanics, tuning, balance tweaks, UX adjustments, and small content additions.
- `design/cdd/product-concept.md` -> **[Product]** draft a lightweight product spec for API tweaks, CLI flags, config changes, workflow adjustments, UI microcopy, validation rules, and small data/model changes.
- If unclear, ask whether this quick design targets a game mechanic/content item or a product feature/workflow.

Game quick-design examples remain. Product quick-spec examples are parallel additions.
# Quick Design

This is the **lightweight design path** for changes that don't need a full CDD.
Full CDD authoring via `/design-system` is the heavyweight path. Use this skill
for work under approximately 4 hours of implementation — tuning adjustments,
minor behavioral tweaks, small additions to existing systems, or standalone
features too small to warrant a full document.

**Output:** `design/quick-specs/[name]-[date].md`

**When to run:** Anytime a change is too small for `/design-system` but too
meaningful to implement without a written rationale.

---

## 1. Classify the Change

First, read the argument and determine which category this change falls into:

- **Tuning** — changing numbers or balance values in an existing system with no
  behavioral change (most minimal path). Example: "increase jump height from 5
  to 6 units", "reduce enemy patrol speed by 10%".
- **Tweak** — a small behavioral change to an existing system that introduces no
  new states, branches, or systems. Example: "make dash invincible on frame 1",
  "allow combo to cancel into roll".
- **Addition** — adding a small mechanic to an existing system that may introduce
  1-2 new states or interactions. Example: "add a parry window to the block
  mechanic", "add a charge variant to the basic attack".
- **New Small System** — a standalone feature small enough that it has no
  existing CDD and is under approximately one week of implementation work.
  Example: "achievement popup system", "simple day/night visual cycle".

**[Product] Product quick-spec categories:**
- **API tweak** — additive endpoint field, validation rule, response shape note, status code behavior, or compatibility-preserving contract change.
- **CLI tweak** — new flag, changed default, help text update, exit code rule, output formatting, or shell-composability improvement.
- **Workflow tweak** — small UI/admin flow change, onboarding step, empty/error state, notification, or user handoff adjustment.
- **Config/data tweak** — default config value, feature flag, permission rule, quota/rate limit, pricing-tier value, migration note, or seed-data adjustment.
- **Docs/example tweak** — SDK example, tutorial step, docs asset, release note, or template change that affects Product adoption.

If the change does NOT fit these categories — it introduces a new system with
significant cross-system dependencies, requires more than one week of
implementation, or fundamentally alters an existing system's core rules — stop
and redirect to `/design-system` instead.

**[Product] Redirect to `/design-system`** when the change creates a new public
module, breaks an API/CLI contract, changes auth or data ownership, requires a
non-trivial migration, changes deployment architecture, or affects multiple
critical workflow states.

Present the classification to the user and confirm it is correct before
proceeding. If there is no argument, ask the user to describe the change.

---

## 2. Context Scan

Before drafting anything, read the relevant context:

- Search `design/cdd/` for the CDD most relevant to this change. Read the
  sections that this change would affect.
- Check whether `design/cdd/module-index.md` exists. If it does, read it to
  understand where this system sits in the dependency graph and what tier it
  belongs to. If it does not exist, note "No systems index found — skipping
  dependency tier check." and continue.
- Check `design/quick-specs/` for any prior quick specs that touched this
  system — avoid contradicting them.
- If this is a Tuning change, also check `assets/data/` for the data file that
  holds the relevant values.

**[Product] Product context scan additions:**
- Read `design/cdd/product-concept.md` for Product principles, User Promise, JTBD, target workflows, and platform/stack intent.
- Read the relevant module CDD and UX spec for API/CLI/UI/data/config changes.
- Read `standards/technical-preferences.md` for language/framework, naming, testing, deployment, and Product language specialist routing.
- Read ADRs that own the affected API, CLI, schema, permission, migration, deployment, or public docs boundary.
- Check docs/examples/config/migrations/release notes for existing public surface commitments that the quick change must preserve.

Report what was found: "Found CDD at [path]. Relevant section: [section name].
No conflicting quick specs found." (or note any conflicts found.)

---

## 3. Draft the Quick Design Spec

Use the appropriate spec format for the change category.

### For Tuning changes

Produce a single table:

```markdown
# Quick Design Spec: [Title]

**Type**: Tuning
**System**: [System name]
**GDD Reference**: `design/cdd/[filename].md` — Tuning Knobs section
**Date**: [today]

## Change

| Parameter | Old Value | New Value | Rationale |
|-----------|-----------|-----------|-----------|
| [param]   | [old]     | [new]     | [why]     |

## Tuning Knob Mapping

Maps to CDD Tuning Knob: [knob name and its documented range].
New value is [within / at the edge of / outside] the documented range.
[When outside: explain why the range should be extended.]

## Acceptance Criteria

- [ ] [Parameter] reads [new value] from `assets/data/[file]`
- [ ] Behavior difference is observable in [specific context]
- [ ] No regression in [related behavior]
```

### For Tweak and Addition changes

```markdown
# Quick Design Spec: [Title]

**Type**: [Tweak / Addition]
**System**: [System name]
**GDD Reference**: `design/cdd/[filename].md`
**Date**: [today]

## Change Summary

[1-2 sentences describing what changes and why.]

## Motivation

[Why is this change needed? What player experience problem does it solve?
Reference the relevant MDA aesthetic or player feedback if applicable.]

## Design Delta

Current CDD says (quoting `design/cdd/[filename].md`, [section]):

> [exact quote of the relevant rule or description]

This spec changes that to:

[New rule or description, written with the same precision as a CDD Detailed
Rules section. A programmer should be able to implement from this text alone.]

## New Rules / Values

[Full unambiguous statement of the replacement content. If this introduces
new states, list them. If it introduces new parameters, define their ranges.]

## Affected Systems

| System | Impact | Action Required |
|--------|--------|-----------------|
| [system] | [how it is affected] | [update CDD / update data file / no action] |

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]
- [ ] No regression: [the original behavior this must not break]

## CDD Update Required?

[Yes / No]
[If yes: which file, which section, and what the update should say.]
```

### For New Small System changes

Use a trimmed CDD structure. Include only the sections that are directly
necessary — skip Player Fantasy, full Formulas, and Edge Cases unless the
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

## Tuning Knobs

| Knob | Default | Range | Category | Rationale |
|------|---------|-------|----------|-----------|
| [name] | [value] | [min–max] | [feel/curve/gate] | [why this default] |

All values must live in `assets/data/[appropriate-file].json`, not hardcoded.

## Acceptance Criteria

- [ ] [Functional criterion: does the right thing]
- [ ] [Functional criterion: handles the edge case]
- [ ] [Experiential criterion: feels right — what a playtest validates]
- [ ] [Regression criterion: does not break adjacent system]

## Systems Index

This system is not currently in `design/cdd/module-index.md`.
[If it should be added: suggest which layer and priority tier.]
[If it is too small to track: state "This system is below module-index
tracking threshold — quick spec is sufficient."]
```

### [Product] For API, CLI, workflow, config/data, and docs/example changes

```markdown
# Quick Product Spec: [Title]

**Type**: [API tweak / CLI tweak / Workflow tweak / Config-data tweak / Docs-example tweak]
**Module / Workflow**: [Module or workflow name]
**CDD Reference**: `design/cdd/[filename].md`
**Date**: [today]

## Change Summary

[1-2 sentences describing the user/developer-visible change and why it is small enough for a quick spec.]

## Product Motivation

[What user promise, JTBD, workflow friction, API/CLI ergonomics, operational need, or adoption blocker this change addresses.]

## Contract / Workflow Delta

Current source says (quote the relevant CDD, UX spec, ADR, API doc, CLI doc, or config reference):

> [exact quote]

This quick spec changes that to:

[New behavior, contract, default, wording, or workflow rule. Be precise enough that implementation does not require guessing.]

## Public Surface Impact

| Surface | Impact | Action Required |
|---------|--------|-----------------|
| API / CLI / UI / Data / Config / Docs | [how it changes] | [update docs / tests / examples / no action] |

## Compatibility and Migration

- **Backward compatibility**: [No impact / additive / breaking-risk / breaking]
- **Migration needed**: [No / Yes -- describe]
- **Rollback behavior**: [How to revert safely, if applicable]

## Acceptance Criteria

- [ ] [Functional criterion]
- [ ] [Contract or CLI behavior criterion]
- [ ] [Docs/example/config/migration criterion if applicable]
- [ ] No regression: [existing user workflow or public contract that must still work]

## CDD / ADR / Docs Update Required?

[Yes / No]
[If yes: exact file, section, and proposed update.]
```

---

## 4. Approval and Filing

Present the draft to the user in full. Then ask:

"May I write this Quick Design Spec to
`design/quick-specs/[kebab-case-title]-[YYYY-MM-DD].md`?"

Use today's date in the filename. The title should be a kebab-case description
of the change (e.g., `jump-height-tuning-2026-03-10`,
`parry-window-addition-2026-03-10`).

If yes, create the `design/quick-specs/` directory if it does not exist, then
write the file.

If a CDD update is required (flagged in the spec), ask separately after
writing the quick spec:

"This spec modifies rules in [System Name]. May I update
`design/cdd/[filename].md` — specifically the [section name] section?"

Show the exact text that would be changed (old vs. new) before asking. Do not
make CDD edits without explicit approval.

---

## 5. Handoff

After writing the file, output:

```
Quick Design Spec written to: design/quick-specs/[filename].md
Type: [Tuning / Tweak / Addition / New Small System]
System: [system name]
CDD update: [Required — pending approval / Applied / Not required]

Next step: This spec is ready for `/story-readiness` validation before
implementation. Reference this spec in the story's CDD Reference field.
```

### Pipeline Notes

Verdict: **COMPLETE** — quick design spec written and ready for implementation.

Quick Design Specs **bypass** `/design-review` and `/review-all-gdds` by
design. They are for small, low-risk, well-scoped changes where the cost of
the full review pipeline exceeds the risk of the change itself.

Redirect to the full pipeline if any of the following are true:
- The change adds a new system that belongs in the systems index
- The change significantly alters cross-system behavior or a system's
  contracts with other systems
- The change introduces new player-facing mechanics that affect the
  game's MDA aesthetic balance
- Implementation is likely to exceed one week of work

In those cases: "This change has grown beyond quick-spec scope. I recommend
using `/design-system` to author a full CDD for this."

---

## Recommended Next Steps

- Run `/story-readiness [story-path]` to validate the story before implementation begins — reference this spec in the story's CDD Reference field
- Run `/dev-story [story-path]` to implement once the story passes readiness checks
- If the change is larger than expected, run `/design-system [system-name]` to author a full CDD instead
