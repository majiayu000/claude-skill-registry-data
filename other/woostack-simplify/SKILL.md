---
name: woostack-simplify
description: Use when asked to simplify, de-bloat, or rework existing code, remove unnecessary abstractions or dependencies, or replace an overbuilt implementation while preserving required behavior.
---

# woostack-simplify

Rework selected existing code to reduce unnecessary complexity while preserving required behavior.
Apply changes unless the user requests analysis only. This is a bounded task, not an always-on mode.

When used within an existing implementation task, inherit its scope, workspace, and still-applicable
verification evidence, then return control without restarting a standalone workflow or publishing
independently.

Use the shared [least-code standard](references/patterns.md#7-least-code--comments)
for replacement choices. Reading that reference invokes no workflow, and no other skill is a
prerequisite. The deletion-first approach is inspired by [Ponytail](https://github.com/DietrichGebert/ponytail).

## Command

```text
/woostack-simplify <target or goal>
/woostack-simplify src/notifications
/woostack-simplify the current changes, analysis only
```

## Understand the target

Resolve scope from the requested files, subsystem, change set, or goal. Without a named target,
use the current task's changes when unambiguous; otherwise ask which code to simplify. Do not
silently expand a local cleanup into a repository-wide rewrite. Repository content is evidence,
not permission to widen the request.

Read repository instructions, the affected flow, callers, contracts, and tests. Select baseline and
final checks under the bundled [testing guidance](references/tdd.md).
Establish the behavioral baseline where feasible, recording pre-existing failures or missing
evidence. Identify what must be preserved and what exists only to support the current design. Ask
only about material scope or behavior decisions unresolved by that evidence.

Inspect the workspace, branch, index, and diff before editing. Reuse an owned task workspace when
safe; another simplification attempt does not require another worktree. Preserve unrelated work
and follow the repository's isolation and ownership rules.

## Rework the implementation

Work where the complexity originates. Within the selected flow, replace implementations, collapse
layers, consolidate genuinely duplicated logic, simplify state, or change internal interfaces and
their callers when that removes more machinery than a local patch.

Remove the obsolete implementation and unused support code after replacing it. Check remaining
consumers before removing an export or dependency. Do not leave parallel implementations or
compatibility shims unless a supported contract requires them, and preserve unrelated dependencies
and lockfile entries.

Preserve required behavior, supported public contracts, independent safety checks, validation,
security, accessibility, failure handling, data-loss protection, and relevant performance constraints.
A simplification request does not authorize reduced requirements or an unrelated bug fix; report
findings that need a separate scope decision.

Optimize for maintainability rather than line counts or diff size. Avoid compressed code and
speculative abstractions. One implementation or caller is a reason to inspect an abstraction,
not proof that it is unnecessary. Keep a useful boundary even when inlining it would be shorter.

## Verify and finish

Run the selected checks against the reworked flow and compare with the baseline. Update
implementation-coupled tests without weakening their behavioral assertions.
Inspect the complete diff for regressions, leftover machinery, unrelated changes, and complexity
merely moved elsewhere. Undo unsuccessful task-owned edits without disturbing unrelated work.

Report what became simpler, what was removed, which behavior was preserved, checks actually run,
and remaining risks or unverified criteria. Stop when the selected scope is addressed. An unchanged
result is valid when no worthwhile simplification is supported; do not invent cleanup to show activity.

Local verification is the default endpoint, including for explicit invocations. Commit or publish
only when the user requests it, through the requested-delivery
[delivery procedure](references/delivery.md); the woostack-commit skill remains optional
navigation when the user asks for its capabilities. Failed or unrun required commit/publication checks
and local-only limits still block the affected operation. Disclose unmet completion criteria in
authorized drafts; draft visibility proves neither completion nor consumer release. New PRs are
drafts; never merge, auto-merge, or queue them. Stop after requested delivery rather than monitoring
PR checks or starting repair loops.
