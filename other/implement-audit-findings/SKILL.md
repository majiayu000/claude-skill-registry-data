---
name: implement-audit-findings
description: Implement confirmed Ergopti AHK or Hammerspoon audit findings in the dedicated worktree, one local commit with regression coverage per fix. Use for "implémente l'audit", "corrige l'audit AHK", or "corrige l'audit Hammerspoon"; do not use to run a new audit.
---

# Implement driver audit findings

Turn a validated audit manifest into independently reviewable local commits.
The manifest is the queue; do not create a second narrative plan unless the user
asks for one. Never push, merge, stash, clean, reset, move a worktree, or modify
the main checkout's unrelated files.

## Select and validate the audit

Use the report the user named, otherwise the newest strict dated directory for
the requested scope:

```text
node tools/audit/workflow.cjs validate-report --report <findings.json>
node tools/audit/workflow.cjs preflight --scope <ahk|hammerspoon>
node tools/audit/workflow.cjs status --report <findings.json>
```

Canonical worktrees are sibling directories named from the repository:
`<repo>-fix-ahk` and `<repo>-fix-hs`. `preflight` recognizes an already
registered worktree and reports it as resumable. It never creates or modifies
one. If the canonical path is absent but another active worktree owns a branch
for that scope, stop; do not create a duplicate or migrate it implicitly.

When `preflight` returns `missing`, first verify that its exact `expected_path`
is absent and that the intended branch name does not already exist. Then create
that one worktree from the manifest's `audited_sha` with an OS-neutral Git
command:

```text
git worktree add -b fix/<ahk|hammerspoon>-audit-<YYYY-MM-DD> <expected_path> <audited_sha>
```

Run `preflight` again and continue only when it reports `ready`. An existing
branch, directory, competing worktree, or different base is user state: inspect
and stop rather than deleting, resetting, force-creating, or silently reusing
it.

An existing dirty canonical worktree is not disposable clutter. Inspect its
branch and diffs and map them to a finding before editing. If ownership is
ambiguous or changes span findings, report that state and stop. Never use stash
as a shortcut: stashes are repository-global and these worktrees are active.

## Implement one finding

Read `windows-toolchain`, `verify-change`, `ship-fix`, `commit-and-push`, and the
matching driver skill. Add `cross-driver-parity`, `i18n`, `logger`, or
`meta-test` only when the finding touches those surfaces.

For the next open finding:

1. Extract only that record with `workflow.cjs extract`; do not repeatedly load
   the complete report.
2. Reproduce and re-derive it against current code and tests. The audit severity
   is not proof. Record a refutation instead of forcing a stale fix.
3. Add the narrow regression test first and observe it fail for the claimed root
   cause before changing production. If resumed dirty source already contains a
   partial fix, do not rewrite or stash it merely to manufacture fail-before
   evidence; state the evidence gap explicitly.
4. Fix the root cause and every sibling site governed by the same invariant.
5. Run the failing test again, then every gate selected by `verify-change`.
6. Stage exact paths and commit exactly this finding plus its regression test.
   Use an English Conventional Commit message and one trailer:

   ```text
   Audit-Finding: AHK-001
   ```

7. Run `workflow.cjs verify-commit --report <...> --id <...> --commit HEAD`.
   Then refresh `status`, which derives completion from Git rather than editing
   the audit manifest.

Repeat sequentially. One agent owns one worktree; do not parallelize commits or
let multiple agents mutate the same branch. Durable new knowledge goes in
`docs/memory/`; final documentation or audit retirement is a separate commit.

## Completion boundary

Stop after all still-valid findings have a verified commit and the selected
gates pass. Report refuted/stale findings, environment deferrals, and real-driver
validation still required. Leave commits local. Do not push or merge even when
the queue is empty.
