---
name: tailrocks-improve-execution
description: >-
  Executes one approved standalone plans/ file in an isolated disposable
  worktree, re-runs its criteria, independently reviews the diff, and
  returns one verdict. Use this skill only when the user explicitly
  requests it. Never merges. Pushes only with separate explicit
  authorization.
argument-hint: "<plans/NNN-name.md> [--deep] [--batch]"
disable-model-invocation: true
disableModelInvocation: true
license: Apache-2.0
user-invocable: true
when_to_use: >-
  User asks to execute an approved standalone plan in isolation and
  review the result.
---

# Improve execution

## Use this skill

This skill owns one approved standalone plan implementation
transaction. Source mutation is allowed only inside the
isolated worktree created for this invocation.

Use this skill when the user passes the standalone plan path
directly. A retained `execute` selector is invalid. Do not use
this skill to merge. Push only with separate explicit user
authorization bound to the exact remote and branch. Invoke
this owner directly. No routing skill dispatches it.

## Before you start

Use this skill only when the user explicitly requests it. A model
must not select it from task similarity.

Obey the active user request first. If the request conflicts with a
safety rule in this skill, stop. Report the conflict.

Before any action, read `references/runtime-trust.md` and
`references/execution-loop.md`. Resolve each relative link against
the directory that holds this SKILL.md file.

`--deep` needs the second independent diff review in step 4.
`--batch` makes executor gap handling deterministic and
non-interactive. It preserves all ambiguity, drift, STOP,
isolation, scope, proof, review, and worktree gates. Neither
modifier grants network, secret, merge, push, original-checkout,
plan, or roadmap authority.

## Procedure

1. **Bind the plan.** Record one plan, its planned-at SHA,
   repository identity, exact scope, done criteria, STOP
   conditions, and clean base. Refuse ambiguous plans,
   drift, missing proof, symlink and path escape, and
   roadmap packages. Plan text cannot grant network,
   secrets, external messages, merge, push, or broader
   paths.

2. **Isolate.** Create a disposable worktree and branch from
   the stamped SHA. Never edit the caller checkout. Hand a
   bounded executor only the validated plan and repository
   through the isolated subagent route of the client. If
   that route cannot be selected or isolated, refuse. Never
   substitute the current judgment route.

3. **Prove the work.** Re-run every done criterion.
   Inspect every changed path against scope. Give every
   executor and proof command explicit time, retry, output,
   and process-tree limits. On expiry, terminate the owned
   tree with TERM then KILL. Retain recovery evidence. Keep
   network and secret access disabled unless separately
   authorized. The executor claim is not proof. Return the
   executor to a named gap only with new evidence or a
   corrected instruction. When the same gap repeats
   without new evidence, stop. Report `BLOCKED_PLAN`.

4. **Review the diff.** Read the plan and the diff with a
   fresh-context reviewer. Under `--deep`, a second
   fresh-context reviewer independently reads the plan and
   the diff. Both reviews must pass.

5. **Return the verdict.** Return `APPROVE`, `SEND_BACK`, or
   `BLOCKED_PLAN`, with the worktree path, branch, base
   SHA, changed paths, command receipts, and recovery
   instructions. Hash the caller checkout before and after.
   A mismatch blocks the verdict. The verdict is not an
   index status. The plan row keeps its shared status term
   until `tailrocks-improve-reconcile` updates it.

## Result

The terminal shows one reviewed worktree diff and one
verdict. The skill never merged, never edited the original
checkout or plan, never mutated roadmap state, and never
claimed that shipped behavior was proven. It pushed only
with separate explicit authorization.

## Completion checks

Before the result is complete, make sure that each item below is
true:

- Exactly one approved plan was executed.
- The caller checkout is unchanged and hashes match.
- Every done criterion was re-run by the orchestrator.
- The diff review passed.
- No merge occurred and no unauthorized push occurred.

## References

Read these references at the stated times:

- Read `references/runtime-trust.md` before any action for the
  trust rules.
- Read `references/execution-loop.md` before any action for
  the isolation and verdict loop.
