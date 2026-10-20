---
name: apply-small-fix-to-version
description: >-
  Load this skill when patching an already-implemented version of a planned app: a small,
  non-feature change made after that version was built (bug fix, copy or config tweak, validation
  tightening, dependency bump). Records the change as a patch ITER_NN.md so the plan stays truthful,
  then implements only the touched sections. Trigger on "patch this version", "small change to the
  shipped version", "non-feature fix". Not for anything that adds or changes a feature (use
  plan-fullstack-app), and not for the version bump or release (use ceh-git-workflow:release).
argument-hint: "[what-to-patch]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Apply a Small Fix to a Version

Make a small change to a version that is already implemented, without inventing a new iteration's
worth of scope and without letting the plan artifacts drift from the code. Done means a patch
`ITER_NN.md` exists, only its `sections_changed` are implemented, and the release is handed off.

Read `${CLAUDE_PLUGIN_ROOT}/references/plan-schema.md` for the full schema before starting. File
naming, version families, `depends_on` resolution, and the `patch` marker rules there are
authoritative.

A patch is a **change below the size of a feature**. It rides as a normal `ITER_NN.md` that
carries `patch: true` in its frontmatter and may sit past the MVP terminator. It is the only
artifact allowed to.

## Procedure

### 1. Locate the plan family and its latest artifact

1. Find the plan files and the family being patched by "Locating plan files" in
   `${CLAUDE_PLUGIN_ROOT}/references/plan-schema.md`.
2. Identify the family's latest artifact: the `mvp: true` terminator if present, otherwise the
   highest `ITER_NN` reachable through `depends_on`. Any existing `patch: true` ITERs count: the
   latest one becomes the new patch's `depends_on` target.

### 2. Run the routing gate (patch or iteration?)

Classify the requested change **before writing anything**. This gate is the point of the skill.

**It is a feature** if the change:

- adds or changes a **data-model entity** or an **API route/endpoint** (i.e. touches §02
  Architecture, the data model or API surface), or
- adds a **new screen, page, or top-level component** (a §05 structural addition), or
- changes the **§01 Concept**, what the app does or its primary user flow, or
- is a **deferred item from the terminator's `## Out of MVP scope` block** that meets any of the
  above. Post-MVP _features_ are the iterative planner's job, not a patch.

The reliable tell: **if §02 changes, it is an iteration, not a patch.** Do not force a feature
through this skill. Stop, say so in one line, and point the user at `plan-fullstack-app`.

**It is a patch** if the change stays within the existing architecture. Continue here for:

- a bug fix, incorrect behavior corrected within an existing endpoint or screen,
- copy, labels, error messages, config values, defaults,
- validation tightening or loosening on an existing field,
- a styling or layout tweak on an existing screen,
- a dependency bump or small non-structural refactor,
- small post-MVP polish that adds no entity, route, screen, or concept change.

When genuinely on the line, prefer routing out: an over-scoped patch is worse than an iteration
planned properly.

### 3. Write the patch ITER

Create the next `ITER_NN.md` in the family, alongside the other plan files. Continue the family's
`NN` counter: a patch does not restart it. Frontmatter:

```yaml
---
artifact: ITER_NN # next number in the family
status: ready
created: YYYY-MM-DD
scope: <one line: the small change this patch makes>
patch: true # marks this as a patch; may follow the mvp terminator
sections_changed: [NN] # only the section(s) the change actually touches
sections_unchanged: [...] # everything else — pointers, resolved via depends_on
depends_on: [<latest artifact stem>] # the terminator, or the prior patch ITER
---
```

Write the changed section's body as a focused delta describing exactly the change (what the
behavior was, what it becomes), the same way an iteration describes its own delta. Everything else
stays a pointer.

### 4. Implement the patch

Implement only `sections_changed`, resolving pointers through `depends_on` for context. Because a
patch is small, implement it inline following the same discipline as `implement-from-plan`
(§04/§05 notes, stay within scope). Before implementing any backend or frontend code, read
`${CLAUDE_PLUGIN_ROOT}/references/implementation-gotchas.md` and avoid the applicable traps. If the
project has its own `implementation-gotchas.md`, read it as well. If the change is large enough to
warrant it, invoke `implement-from-plan` targeting the patch file by name instead.

### 5. Summarize and hand off

Report per Output, then hand off the release per Hands off to.

## Rules

- **`patch: true`** distinguishes a patch from a feature iteration and authorizes it to sit past
  the terminator. Never set `mvp` on a patch.
- **`sections_changed` lists only what the change touches**, usually §04 and/or §05 detail, not
  §02. If you find yourself listing §02, re-run the gate (step 2): it is probably an iteration.
- Keep the diff to the plan as small as the diff to the code.
- Do not implement any section outside `sections_changed`.
- Do not bump versions or tag. The version bump and release are not this skill's job: the release
  skill runs bump, changelog, and tag as one gated flow.

## Output

- The patch ITER created and the section(s) it changed.
- What changed in the code and any assumptions.
- Items the user should verify manually.

## Stop conditions

- The routing gate classifies the change as a feature → stop, say so in one line, and point the
  user at `plan-fullstack-app`.
- More than one plan family exists and the user named none → take the highest version, per
  "Locating plan files" in the plan schema, and say which.

## Hands off to

- State that this is a **SemVer PATCH** and point the user at `ceh-git-workflow:release` to bump,
  tag, and publish.
