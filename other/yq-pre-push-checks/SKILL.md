---
name: yq-pre-push-checks
description: 推送或宣称就绪前，选择与变更风险匹配的最小验证。
---

# Pre-Push Checks

Establish relevant evidence once before a push or readiness claim. This skill does not authorize committing, pushing, changing PR state, bypassing hooks, or rewriting history; those actions require the user's request or existing task scope.

The normal order is inspect scope, validate, commit if authorized, push if authorized, then verify the remote and CI. A stack-management tool that rebases and publishes several branches as one indivisible operation is the exception: record the pre-state, run it only when authorized, validate every rewritten layer immediately afterward, and block merge until the evidence passes.

## Inspect the outgoing change

1. Confirm the repository, branch, worktree, and dirty state.

```sh
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
```

2. Read applicable repository instructions and discover what hooks, package scripts, task runners, CI jobs, generated artifacts, and test frameworks actually exist.
3. Verify the live PR base, upstream, or stack parent from current remote state. Fetch the exact ref when needed; do not guess `main`, `master`, or an old local tracking ref.
4. Inspect the complete outgoing scope: committed changes from the resolved merge base plus staged, unstaged, and relevant untracked files. Use the repository's change-scope tool when it has one; otherwise combine `git merge-base`, `git diff --name-status`, `git diff --cached`, and `git ls-files --others --exclude-standard`.

After a base merge or rebase, recompute the scope. Reuse only evidence whose covered behavior and inputs were not invalidated.

## Map risk to evidence

Every behavior change needs the narrowest available check that would fail for its regression. Add broader checks only for surfaces the diff can credibly affect.

- **Local implementation:** run the owning unit or integration tests and the repository's type, compile, lint, or static checks that cover the changed language and package.
- **Shared contract or public API:** add adjacent consumer tests, schema/API compatibility checks, and a built-entry or package smoke when callers consume compiled output.
- **Persistence, migrations, queues, or durable formats:** test forward behavior, failure/rollback, compatibility, and recovery against the real migration or serialization path.
- **Asynchronous, worker, subprocess, or resource-owning lifecycle:** test success plus cancellation/failure, restoration after a failed transition, a negative control for leaked or duplicate work, concurrent-owner isolation where relevant, and teardown to quiescence. Exercise the real worker/process entry path when in-process fakes cannot prove ownership or cleanup.
- **Build, manifests, exports, bins, workers, packaging, or deployment configuration:** run the build plus the artifact, install, startup, or deployment-config smoke that proves the produced surface.
- **Documentation, examples, generated catalogs, or linked comments:** run the repository's generator/sync, link, example, localization, and documentation checks as applicable.
- **CLI-, UI-, model-, or protocol-visible output:** exercise the real entry path and run the focused snapshot or behavioral assertion that owns the output.
- **External provider or environment behavior:** run the smallest real integration/e2e scenario when credentials and authority are available; redact secrets and distinguish simulated evidence from real service evidence.
- **Security or permission boundaries:** run the relevant policy, negative, and abuse-path checks rather than relying on a happy-path test.

Inspect what each check proves. A command finishing successfully is not evidence for behavior it never exercised.

### Coverage must follow affected source

Test selection and coverage selection are separate. A test filter chooses which tests run; many tools otherwise measure a default or repository-wide source set. When focused coverage matters, name both the owning tests and the affected source files or package using the framework's supported include mechanism.

Do not use no-test-success flags, lower thresholds, broad exclusions, or artificially narrow coverage globs to turn missing evidence green. If one focused test does not cover the affected scope, add the other owning tests or narrow the source scope only when the excluded modules cannot be affected.

Dependency-based test discovery is a nomination tool. It misses configuration, dynamic loading, reflection, subprocesses, workers, generated code, built artifacts, network providers, and string-addressed events; select those checks explicitly.

## Decide whether a full rehearsal is warranted

Run the complete local suite or production-like rehearsal when the user requests it, a CI failure is being diagnosed, the change is repository-wide, or no narrower set credibly covers the blast radius. Use current repository scripts and CI as the inventory rather than recreating an obsolete aggregate command.

Do not repeat a passing expensive check merely because commit or push follows. Inspect whether hooks will change files or add distinct evidence. After a formatting or generation hook changes content, review the resulting diff and rerun only checks invalidated by that change.

## Protect rewritten history

Before an authorized standalone rebase or force-push:

1. fetch the current remote branch;
2. record its exact object ID;
3. verify the worktree and branch target;
4. publish with an exact `--force-with-lease=<branch>:<observed-oid>` or the stack tool's documented equivalent.

Raw `--force` discards concurrency protection. After a rewritten push, fetch the live heads and recheck review threads, approvals, mergeability, and CI. Old commit hashes, approvals tied to commits, and inline-comment anchors are not current evidence.

### Tools that rewrite and publish a stack

When a stack operation cannot place validation between rewrite and publication:

1. require a clean worktree and record the official stack order, bases, and exact remote heads;
2. run the authorized operation;
3. re-query every live branch head and stack relationship;
4. inspect each rewritten layer against its current base;
5. run the evidence selected by this skill for every affected layer;
6. keep merge/readiness status pending until all selected checks pass.

If post-publication evidence fails, leave the lease-protected heads in place and block readiness. Repair, validate, and republish only when those actions are already authorized by the task; otherwise report the exact failure and required next action. Do not call the stack ready merely because synchronization succeeded.

## Handle failures honestly

If a relevant check fails before an ordinary push, stop the push. Repair and revalidate only when fixing is already in scope; otherwise report the blocker. If a post-publication stack check fails, block merge and follow the authorization-aware path above.

For an environment-specific failure, record:

- the exact command and failing assertion or step;
- platform, runtime, dependency, and configuration differences relevant to the failure;
- the non-platform evidence that still passed;
- why CI or another environment is expected to differ, with evidence.

Prefer fixing cross-platform nondeterminism when the check is required. Bypass a hook only with explicit authorization, and report exactly what was bypassed and why.

## Complete an authorized push

1. Run the selected relevant checks once and record their exact results.
2. Commit only when authorized. Inspect files changed by fixers, formatters, generators, or hooks before proceeding.
3. Push normally, or use the recorded lease for an authorized history rewrite.
4. Verify the remote branch resolves to the intended local commit.
5. Inspect CI and required checks. Report queued or pending work as pending; inspect failures before attributing them to infrastructure.

On GitHub, `gh pr checks` and `gh pr view --json mergeable,mergeStateStatus` can distinguish missing runs from a conflicting PR. When a PR is conflicting, absent `pull_request` workflow runs may be a mergeability signal rather than a lost push event. Confirm the conflict from current refs; do not generate empty commits or toggle draft state to manufacture CI.

Report the verified base and head, outgoing scope, risk mapping, commands run, pass/fail/pending results, hooks or generated changes, remote-ref verification, CI state, and anything not covered. Never summarize a partial validation set as “all checks passed.”
