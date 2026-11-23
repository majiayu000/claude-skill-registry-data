---
name: break-into-issues
description: >
  Break a plan, spec, or the current conversation into small end-to-end issues, each one a vertical slice that names the issues blocking it, then publish them to the project's issue tracker after the user approves the breakdown. Use on request only: "break this into issues", "turn this plan into tickets", "split this up so agents can pick it up". For writing the plan first, use the plan-change skill.
license: MIT
metadata:
  upstream: mattpocock/skills@49dd158d skills/engineering/to-tickets
---

# Break into issues

Break a plan, spec, or conversation into a set of **issues**: tracer-bullet vertical slices, each declaring the issues that **block** it.

## Process

### 1. Gather context

Work from whatever is already in the conversation. If the user passes a reference (a spec path, an issue number or URL), fetch it and read its full body and comments.

### 2. Explore the codebase

If you have not already explored the codebase, do so to understand the current state of the code. Issue titles and descriptions use the project's own vocabulary (its `GLOSSARY.md` if it has one) and respect the ADRs in the area you are touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** issues.

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer.
- A completed slice is demoable or verifiable on its own.
- Each slice is sized to fit in a single fresh agent session.
- Any prefactoring comes first.

Give each issue its **blocking edges**: the other issues that must complete before it can start. An issue with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose blast radius fans across the whole codebase, so a single edit breaks every call site at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own issue blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in an issue blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify issue; green is promised only there.

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each issue, show:

- **Title**: short descriptive name
- **Blocked by**: which other issues (if any) must complete first
- **What it delivers**: the end-to-end behaviour this issue makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each issue depend only on issues that genuinely gate it?
- Should any issues be merged or split further?

Iterate until the user approves the breakdown. Publish nothing before that.

### 5. Publish the issues

Publishing creates issues other people can see, so do it only after the user approved the breakdown in step 4. Find the tracker in this order:

1. **The project says where issues live** (its `AGENTS.md`, `CLAUDE.md` or `CONTRIBUTING.md`): use that.
2. **The repo is on GitHub and the `gh` CLI is signed in**: create one issue per slice with `gh issue create`.
3. **Another tracker you have a tool for** (Linear, Jira): use that tool.
4. **None of these**: write one file per issue in `.scratch/<feature-slug>/issues/`, named `<NN>-<slug>.md`, and tell the user where they are.

Publish in dependency order, blockers first, so each issue's blocking edges can reference real identifiers. Use the tracker's native blocking relationship where it has one; otherwise list the blockers under "Blocked by". If the source was an existing issue, make each new issue its sub-issue where the tracker supports it, or link back to it under "Parent". Follow the project's own labels and title conventions; invent none.

Do NOT close or modify any parent issue.

Issue body:

```md
## Parent

A reference to the parent issue, if the source was an existing issue. Otherwise omit this section.

## What to build

The end-to-end behaviour this issue makes work, from the user's perspective, not a layer-by-layer implementation list.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking issue, or "None (can start immediately)". Omit this section when blockers were set as native edges.
```

For local files, number from `01` in dependency order, one issue per file and never a single combined file, with the same sections under a `# <NN>: <title>` heading.

Avoid specific file paths or code snippets in an issue: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (a state machine, a reducer, a schema, a type shape), inline it and note that it came from a prototype. Trim to the decision-rich parts.
