---
name: "speckit-correct-course"
description: "Handle an intent that changed mid-implementation: work out which requirements, tasks and tests the change invalidates, write it as a Spec Delta proposal, and only then edit anything. Use when the user changes their mind during a feature, when a discovery makes a requirement wrong, or when the spec and the code have started disagreeing."
argument-hint: "What changed, in a sentence. Or a requirement id, to see what rests on it."
compatibility: "Node 18+. Read-only until you approve the proposal."
metadata:
  author: "speckit-demo"
  source: "adapted from BMAD's bmad-correct-course"
user-invocable: true
disable-model-invocation: false
model: fable
---

## User Input

```text
$ARGUMENTS
```

## Why this exists

A requirement changes mid-flight and the cheapest thing to do is edit `spec.md`
and carry on. Nothing in this repository stopped that. `.claude/scripts/spec-drift.mjs`
checks that code and spec move *together*; it cannot notice that a requirement
quietly changed meaning, that three tasks now implement something nobody asked
for, or that a test still asserts the old behaviour and passes.

BMAD names the step: assess the change, produce an impact analysis, then decide.
The analysis comes before the edit, not after.

## Phase 1 — state the change as a difference

Write two lines, no more:

- **Was:** the requirement as it stands, quoted from `spec.md`.
- **Is now:** what it should say.

If you cannot write the first line, the intent did not change — something was
never specified, and that is `/speckit-clarify`, not this.

## Phase 2 — measure what rests on it

```bash
node .claude/scripts/impact.mjs FR-004 FR-007       # the requirements you named
node .claude/scripts/impact.mjs --all               # the whole feature
```

For each requirement that returns: the spec line, every task citing it (and
whether it is already checked), every test carrying its token, the capability
holding it, and any feature that already superseded it.

Three readings decide the work:

- **A checked task citing it** is work already done against the old intent.
  Say whether it is wasted, partly reusable, or has to be reverted.
- **A test carrying its token** asserts the old behaviour and is currently
  green. It has to change before the implementation does — the red-first gate
  is not a formality here, it is the only thing that will tell you the new
  behaviour actually landed.
- **A capability that holds it** means the requirement is already merged truth.
  Changing it is a `Modifies` in a delta, never an edit to the capability file.

## Phase 3 — write the proposal, then stop

Write it into the feature's `## Spec Delta`, in the format
`node .claude/scripts/capabilities.mjs validate` accepts:

```markdown
### Capability: `cli-tasks`

- **Modifies**: `002-FR-004` → `FR-012`
- **Removes**: `002-FR-007` — the flag it describes is gone
```

Then present, in one short block:

1. Was / Is now.
2. Requirements affected, and for each: tasks to reopen, tests to rewrite.
3. What this costs — including work already done that this discards.
4. What you recommend, and the alternative you rejected.

**Stop there.** The point of a named step is that the decision is visible. An
impact analysis you act on before anyone reads it is a diff with extra prose.

## Phase 4 — apply, in this order

Only after approval, and only in this order, because each step is what makes the
next one honest:

1. Edit `spec.md`: the requirement text and the `## Spec Delta`.
2. Reopen the affected tasks in `tasks.md`, and add any new ones.
3. Rewrite the affected tests **first** and prove them red.
4. Implement.
5. `node .claude/scripts/impact.mjs --all` again — every affected requirement should now
   name a test.
6. Commit as one chunk: `fix: correct <feature>'s FR-XXX after <what changed>`.
   The spec-drift gate requires `specs/` in the same commit as `apps/*/src` and `libs/*/src`,
   which is exactly right here.

## When this is the wrong command

- Nothing was ever specified → `/speckit-clarify`.
- The work is larger than the feature → `/speckit-size`, then a new feature.
- The feature is finished and the spec is merely out of date → `/speckit-retro`
  records the divergence, `/speckit-archive` merges the correction.
