---
name: manage-todo
description: "Read, update, validate, and report on the project roadmap (TODO.md). Use when asked to add tasks, mark tasks complete, check roadmap status, find what to work on next, triage deferred items into the roadmap, validate TODO.md format, reorder or renumber tasks, or edit milestone descriptions. Also use when the user mentions 'roadmap', 'TODO', 'backlog', 'milestone', 'task list', or asks 'what's next'. Do NOT use for architecture decisions, for changelog entries, for creating implementation plans from specs or managing Issue Trackers (Jira, GitHub, Linear, etc.)."
metadata:
  author: Serghei Iakovlev
  version: "1.0"
  category: roadmap
---

# Roadmap Management

Manage TODO.md - the sequenced project roadmap that drives all implementation work. TODO.md is the **sequencing authority**: milestones are deliberately ordered and each depends on the previous. Every mutation must preserve this invariant.

> **Authoritative format:** See [references/format-specification.md](references/format-specification.md) for the exact structural rules, naming conventions, line widths, indentation, and numbering scheme. Load this reference before any write operation.

## Running scripts bundled with this skill

Script paths in this document (e.g. `scripts/`) are resolved relative to **this** SKILL.md file, not to your current working directory. If a relative command fails to resolve, prefix it with the path your platform loaded this SKILL.md from.

**Fallback.** If `python3` cannot be located, analyze the script's purpose and logic and execute its intent with available tools, but warn the user that python is not available and the logic was executed with a fallback approach that may not be perfect.

## Operations

### Status - Progress Report

1. Read `TODO.md` completely.
2. For each milestone, count completed (`[x]`) vs total tasks.
3. Identify the **active milestone** - the first milestone with incomplete tasks.
4. Report:
   - Overall progress (completed / total tasks, percentage)
   - Per-milestone breakdown (completed / total)
   - Active milestone name and remaining tasks
   - Any tasks that appear blocked (reference other incomplete tasks)

### Next - Determine What to Work On

1. Read `TODO.md`.
2. Find the active milestone (first with incomplete tasks).
3. Within that milestone, find the first `- [ ]` task - this is the next task because milestones are sequential and tasks within them are ordered by dependency.
4. Return the task ID, description, and verify criteria.
5. If the task references architecture sections, note them so the implementer knows what to read first.

### Add - Insert a New Task

1. Read `TODO.md` and [references/format-specification.md](references/format-specification.md).
2. Determine the correct milestone based on the task's theme and dependencies. Fundamental infrastructure goes earlier; feature-specific work goes later.
3. Determine the next sequential task number within that milestone. If the last task is `N.M`, the new task is `N.(M+1)`. Never renumber existing tasks.
4. Write the task following the exact format:
   - Checkbox: `- [ ] N.M `
   - Description: imperative form, self-contained, wrapped at 90 characters
   - Continuation lines: 6-space indent
   - **Verify:** line describing how to confirm completion (tests, commands, or observable outcomes)
5. Insert after the last task in the target milestone, before the next milestone heading.
6. Validate the result (see Validate operation).

**Example - well-formed task:**

```markdown
- [ ] 6.14 Implement dispatch rate limiting: enforce a maximum number of
      dispatches per tick to prevent thundering herd on startup with large
      backlogs. Use `agent.max_dispatches_per_tick` from config (default: 5).
      See architecture Section 8.3.
      **Verify:** unit test confirms dispatch stops after limit is reached even
      when more eligible candidates exist. A second test confirms default value
      of 5 when config field is absent.
```

**Example - task that violates conventions (do NOT produce this):**

```markdown
- [ ] Add rate limiting
```

Why this fails: no task number, no milestone context, not self-contained, no verify criteria, description is vague.

### Update - Modify Existing Tasks

1. Read `TODO.md`.
2. Locate the task by its ID (e.g., `6.10`).
3. Apply the requested change:
   - **Mark complete:** Change `- [ ]` to `- [x]`. Do not modify the description or verify line.
   - **Edit description:** Preserve task number, checkbox state, and verify line structure. Wrap at 90 characters.
   - **Move task:** Only within the same milestone. Renumbering across milestones breaks external references (plans, specs, PRs).
4. Validate the result.

### Triage - Add Deferred Item from Review or Discussion

Triage applies three filters before adding. A concern that fails any filter is not added.

1. **Architecture conflict gate.** Read the relevant section of architecture documentation (if present). If the suggestion contradicts the spec's design intent, explain why and stop - do not add it.
2. **Redundancy check.** Scan TODO.md for an existing task that covers this concern. If found, note the task ID and stop - do not create duplicates.
3. **Roadmap horizon test.** Would this matter before the last defined milestone ships? If not, mention it as a future consideration but do not add it.

If all filters pass, follow the **Add** operation. Place the task in the milestone whose theme most closely relates to the concern.

### Validate - Check Structural Integrity

1. Run the validation script [scripts/validate_roadmap.py](scripts/validate_roadmap.py) with `TODO.md` as input
2. If `python3` is unavailable, verify manually against [references/format-specification.md](references/format-specification.md) using this checklist:
   - [ ] File starts with `# ` title
   - [ ] Every milestone uses `## Milestone N: Name` format
   - [ ] Every milestone has a description paragraph before tasks
   - [ ] Every task uses `- [x] N.M ` or `- [ ] N.M ` format
   - [ ] Task numbers are sequential within each milestone (no gaps, no duplicates)
   - [ ] Milestone numbers in task IDs match the milestone they appear under
   - [ ] Every task has a `**Verify:**` section
   - [ ] Continuation lines use exactly 6-space indent
   - [ ] No line exceeds 96 characters (target 90, hard limit 96; inline code exempt)
   - [ ] Tasks are self-contained - description alone is enough to implement
   - [ ] Ordering is fundamental-to-specific within each milestone
   - [ ] Completed tasks (`[x]`) precede incomplete tasks (`[ ]`) within a milestone (no interleaving)
3. Report all violations with line numbers and suggested fixes.
4. If no violations found, confirm the file is structurally sound.

## Constraints

- **Renumber only to close the gap a removal leaves.** External artifacts (plans, specs, PRs, commit messages) reference task IDs, and contiguous numbering is a hard validation error, so a removal and stable IDs cannot both hold. Search the repository and its history for the IDs that would move, renumber only when nothing references them, and report which IDs changed.
- **Never reorder milestones.** They encode a dependency chain. Reordering requires explicit user approval because it implies architectural replanning.
- **Remove a task only when its premise is gone** - the work is already done by other means, or the thing it described no longer exists. A task whose wording went stale gets rewritten in place; a task that was completed gets `[x]`. Removal is the user's call, not the agent's.
- **Never modify project documentation** based on roadmap work. The architecture doc is the upstream authority; the roadmap is downstream.
- **Append only within milestones.** New tasks go after the last existing task in the target milestone. Do not insert between existing tasks.
