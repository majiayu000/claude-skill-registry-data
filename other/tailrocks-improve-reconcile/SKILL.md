---
name: tailrocks-improve-reconcile
description: >-
  Reconciles the standalone plans/ backlog against current repository
  truth, optionally re-verifying every row, and updates only
  plans/README.md. Use this skill only when the user explicitly requests
  it. Never edits plans, source, or roadmap items.
argument-hint: "[--deep] [--batch] [repository path]"
disable-model-invocation: true
disableModelInvocation: true
license: Apache-2.0
user-invocable: true
when_to_use: >-
  User asks to reconcile the standalone plan backlog with current
  repository truth.
---

# Improve reconcile

## Use this skill

This skill synchronizes standalone plan status with repository
truth. The sole writable output is `plans/README.md`. The
index uses the shared status terms `TODO`, `IN_PROGRESS`,
`BLOCKED`, `STALE`, and `RETIRED`, the same terms as the plan
skill. Execution verdicts stay separate from index status.

Use this skill when the user passes only the optional
repository path and modifiers. A retained `sweep` selector is
invalid. Do not use this skill to edit plans, source, or
roadmap items. Roadmap items belong to `tailrocks-reconcile`.
Invoke this owner directly. No routing skill dispatches it.

## Before you start

Use this skill only when the user explicitly requests it. A model
must not select it from task similarity.

Obey the active user request first. If the request conflicts with a
safety rule in this skill, stop. Report the conflict.

Before any action, read `references/runtime-trust.md`. Read
`references/reconciliation.md` in steps 2 through 4. Resolve
each relative link against the directory that holds this
SKILL.md file.

`--deep` re-verifies every indexed row without sampling.
`--batch` makes status selection deterministic and
non-interactive. It preserves every evidence, command,
compare-and-swap, and no-change rule. Neither modifier grants
plan-body, source, roadmap, Git, or remote authority.

## Procedure

1. **Bind the backlog.** Record the root, the revision, the
   dirty state, index bytes, and every indexed plan. Refuse
   a roadmap item. `tailrocks-reconcile` owns those.

2. **Verify each row.** Verify plan existence, stamped SHA,
   current evidence, changed paths, dependencies, and
   status claim. Default coverage can inspect rows whose
   state or evidence changed. `--deep` re-verifies every
   row without sampling. Run target commands only with
   explicit authority and every control below:

   - A read-only target
   - Frozen inputs
   - Disabled network
   - Scrubbed secrets
   - External cache
   - Bounded processes
   - TERM-then-KILL cleanup
   - A post hash.

   Otherwise mark proof unavailable.

3. **Mark truth only.** Mark `TODO`, `IN_PROGRESS`,
   `BLOCKED`, `STALE`, or `RETIRED`. Missing evidence is
   not completion. A finding fixed independently becomes
   `RETIRED` with its fixing SHA. A defective plan becomes
   `BLOCKED`. It routes to a new `tailrocks-improve-plan`
   invocation. Never rewrite it here.

4. **Publish the index.** Reject symlinked and escaping
   paths. Compare-and-swap one updated `plans/README.md`
   atomically. Roll back only owned bytes. On drift, leave
   bytes unchanged. Report the conflict.

## Result

The terminal shows exactly one index update or a no-change
receipt. No plan body, source, roadmap, branch, commit,
remote, issue, or comment changed. Every row has current
evidence.

## Completion checks

Before the result is complete, make sure that each item below is
true:

- Only `plans/README.md` changed.
- Every row uses a shared status term.
- Every status change has current evidence.
- No plan body or source byte changed.
- Drift left bytes unchanged with a reported conflict.

## References

Read these references at the stated times:

- Read `references/runtime-trust.md` before any action for the
  trust rules.
- Read `references/reconciliation.md` in steps 2 through 4
  for row verification and index rules.
