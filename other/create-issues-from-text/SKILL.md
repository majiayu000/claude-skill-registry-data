---
name: create-issues-from-text
description: Use when break down assignment into multiple structured issues
license: MIT
metadata:
  author: Petr Král (pekral.cz)
---

## Constraints
- Preserve original assignment (store in parent or first issue)
- Do not implement code
- Assign all issues to current user
- Use CLI tools

---

## Execution

### 1. Analyze Assignment
- Understand scope and dependencies
- Identify logical implementation steps

### 2. Propose Breakdown
- List steps with short descriptions
- Proceed directly to step 3; do not gate on a confirmation round when the breakdown is unambiguous

### 3. Create Issues
- One issue per step
- Ensure each is independently deliverable
- For every issue created — flat breakdown, EPIC parent, and sub-issues alike — select and apply the single most relevant existing label per `@rules/compound-engineering/tracker.md` *Label tracker issues, and keep the labels true*; this is additive to, and independent of, the structural `EPIC` label from *EPIC parent & sub-issues* below

### 4. Output
- Return list of created issues with URLs

---

## Issue Structure

Use the template defined in `templates/issue-structure.md`.

---

## EPIC parent & sub-issues

Use this when the assignment is a **cross-cutting mix of requirements spanning multiple parts of the application** (e.g. backend + frontend + mobile, or schema + API + UI). Instead of a flat list of peer issues, build a parent → children tree so the whole effort is trackable from one place.

> **A human approves the tree before any of it is created (L2).** Present one confirmation package first — the parent's title and scope, one line per proposed sub-issue, the dependencies, and the resolve order — and wait for the user to approve it in words. Only that approval permits the writes below, and only for the pieces it names. Silence is not approval, the original request is not approval, and an approval given for one package does not carry to a changed split. Without it, report the proposed breakdown and stop: the pieces are in the report, so nothing is lost. A **flat** list of peer issues is outside this gate and keeps its existing consent (`@rules/compound-engineering/backlog.md` *Decomposition mode*).

1. **Pick (or create) the parent.** When the assignment already has a tracker item, that item becomes the EPIC parent. When the assignment is a described task with no tracker item, create the parent issue first, carrying the full original assignment in its body.
2. **Label the parent `EPIC`.** Apply the `EPIC` label to the parent. Create the label once if the repository does not have it yet (`gh label create EPIC --description "Tracks a cross-cutting effort split into sub-issues" --color 5319e7`), then ignore the "already exists" outcome on subsequent runs.
3. **Create one sub-issue per application area.** Each sub-issue is an independently deliverable assignment (same `templates/issue-structure.md` structure) scoped to a single area; do not bundle two areas into one sub-issue.
4. **Link every sub-issue back to the parent (both directions).**
   - In each sub-issue body, reference the parent with `Part of #<parent>` so the relationship is visible from the child.
   - In the parent body, keep a checkable task list of the children — `- [ ] #<child>` per sub-issue — under a `## Sub-issues` heading, so the parent shows the full breakdown and progress.
5. **Order.** Fill each sub-issue's `## Dependencies` so a resolving run (e.g. `splinter`) can pick a dependency-aware order — dependencies before dependents.
6. **Output.** Return the `EPIC`-labelled parent URL plus the list of linked sub-issue URLs and the planned resolve order.

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
