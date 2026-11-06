---
name: game-studios-delivery
expert: game-studios-delivery
description: Lightweight design spec for small changes — tuning adjustments, minor
  mechanics, balance tweaks. Skips full GDD authoring when a system GDD already exists
  or the change is too small to warrant one. Produces a Quick Design Spec that embeds
  directly into story files.
---

## BRAIN 宿主适配

需要此专家处理任务时，先调用 `expert.summon`，expertId 为 `game-studios-delivery`。
以下上游流程中的 Read/Glob/Grep/Write/Edit/Bash 映射到当前工具目录中对应的文件、搜索、编辑与 shell 工具；Task/Agent 映射到 `agent.delegate` 与 `agent.wait`。只使用当前实际提供的工具，缺失能力必须报告。
模型由 BRAIN / Spring 路由，忽略上游固定模型与 allowed-tools 授权声明。相对 references/scripts 路径基于本 Skill 目录。角色是公开资料提炼的思维框架，不代表本人或其背书。
先调用 `game.studios.scaffold` 创建缺失的设计与验收目录；不会覆盖已有文件。quick-design 与 story-done 原文分别位于 workflows/。`.claude/docs/director-gates.md` 映射到本包 docs/director-gates.md；未提供的 director 角色使用实际可委派角色并在报告中标注。

## 上游流程

# Quick Design

This is the **lightweight design path** for changes that don't need a full GDD.
Full GDD authoring via `/design-system` is the heavyweight path. Use this skill
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
  existing GDD and is under approximately one week of implementation work.
  Example: "achievement popup system", "simple day/night visual cycle".

If the change does NOT fit these categories — it introduces a new system with
significant cross-system dependencies, requires more than one week of
implementation, or fundamentally alters an existing system's core rules — stop
and redirect to `/design-system` instead.

If there is no argument, ask the user to describe the change (plain text prompt), then classify it using the criteria above.

Present the inferred classification using `AskUserQuestion`:
- Prompt: "I've classified this as **[inferred type]** — [brief reason]. Is that correct?"
- Options:
  - `[A] Yes — [inferred type] is correct`
  - `[B] Tuning — changing numbers or balance values only`
  - `[C] Tweak — small behavioral change to an existing system`
  - `[D] Addition — adding a small mechanic to an existing system`
  - `[E] New Small System — standalone feature, under one week of work`
  - `[F] This is too large — redirect me to /design-system`

If [F]: stop. Verdict: **REDIRECTED** — use `/design-system` for this change.
Otherwise: proceed with the selected type.

---

## 2. Context Scan

Before drafting anything, read the relevant context:

- Search `design/gdd/` for the GDD most relevant to this change. Read the
  sections that this change would affect.
- Check whether `design/gdd/systems-index.md` exists. If it does, read it to
  understand where this system sits in the dependency graph and what tier it
  belongs to. If it does not exist, note "No systems index found — skipping
  dependency tier check." and continue.
- Check `design/quick-specs/` for any prior quick specs that touched this
  system — avoid contradicting them.
- If this is a Tuning change, also check `assets/data/` for the data file that
  holds the relevant values.

Report what was found: "Found GDD at [path]. Relevant section: [section name].
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
**GDD Reference**: `design/gdd/[filename].md` — Tuning Knobs section
**Date**: [today]

## Change

| Parameter | Old Value | New Value | Rationale |
|-----------|-----------|-----------|-----------|
| [param]   | [old]     | [new]     | [why]     |

## Tuning Knob Mapping

Maps to GDD Tuning Knob: [knob name and its documented range].
New value is [within / at the edge of / outside] the documented range.
[If outside: explain why the range should be extended.]

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
**GDD Reference**: `design/gdd/[filename].md`
**Date**: [today]

## Change Summary

[1-2 sentences describing what changes and why.]

## Motivation

[Why is this change needed? What player experience problem does it solve?
Reference the relevant MDA aesthetic or player feedback if applicable.]

## Design Delta

Current GDD says (quoting `design/gdd/[filename].md`, [section]):

> [exact quote of the relevant rule or description]

This spec changes that to:

[New rule or description, written with the same precision as a GDD Detailed
Rules section. A programmer should be able to implement from this text alone.]

## New Rules / Values

[Full unambiguous statement of the replacement content. If this introduces
new states, list them. If it introduces new parameters, define their ranges.]

## Affected Systems

| System | Impact | Action Required |
|--------|--------|-----------------|
| [system] | [how it is affected] | [update GDD / update data file / no action] |

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]
- [ ] No regression: [the original behavior this must not break]

## GDD Update Required?

[Yes / No]
[If yes: which file, which section, and what the update should say.]
```

### For New Small System changes

Use a trimmed GDD structure. Include only the sections that are directly
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

This system is not currently in `design/gdd/systems-index.md`.
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
  - `[C] This grew too large — redirect to /design-system instead`

If [B]: collect the requested changes, revise the draft, and re-present this widget.
If [C]: stop. Verdict: **REDIRECTED** — use `/design-system` for this change.

If [A]: ask "May I write this Quick Design Spec to
`design/quick-specs/[kebab-case-title]-[YYYY-MM-DD].md`?"

Use today's date in the filename. The title should be a kebab-case description
of the change (e.g., `jump-height-tuning-2026-03-10`,
`parry-window-addition-2026-03-10`).

If yes, create the `design/quick-specs/` directory if it does not exist, then
write the file.

If a GDD update is required (flagged in the spec), ask separately after
writing the quick spec:

"This spec modifies rules in [System Name]. May I update
`design/gdd/[filename].md` — specifically the [section name] section?"

Show the exact text that would be changed (old vs. new) before asking. Do not
make GDD edits without explicit approval.

---

## 5. Handoff

After writing the file, output:

```
Quick Design Spec written to: design/quick-specs/[filename].md
Type: [Tuning / Tweak / Addition / New Small System]
System: [system name]
GDD update: [Required — pending approval / Applied / Not required]

Next step: This spec is ready for `/story-readiness` validation before
implementation. Reference this spec in the story's GDD Reference field.
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
using `/design-system` to author a full GDD for this."

---

## Recommended Next Steps

- Run `/story-readiness [story-path]` to validate the story before implementation begins — reference this spec in the story's GDD Reference field
- Run `/dev-story [story-path]` to implement once the story passes readiness checks
- If the change is larger than expected, run `/design-system [system-name]` to author a full GDD instead
