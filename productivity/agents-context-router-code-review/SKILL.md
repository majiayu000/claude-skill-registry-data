---
name: agents-context-router-code-review
description: Review an agents-context-router diff, branch, commit or PR for correctness, repository rules, requested behavior, affected consumers and cleanup. Use when reviewing changes or preparing a commit, push or pull request. Read-only unless fixes are requested.
---

Review one change in five independent passes. Read `docs/review.md` for this
repository's consumers and verification commands; load `docs/releasing.md` when
versions, manifests or workflows change. These docs own the repository rules.

## 1. Pin the scope

Inspect Git status and preserve unrelated edits. Refresh the remote base when
reviewing against it, then record the base SHA, head SHA and uncommitted paths.
With no target, review `git diff origin/main...HEAD` plus `git diff HEAD` and
task-owned untracked files. With a ref, use that ref as the base. For a PR,
retrieve its current head and review that code in an isolated checkout, not the
working branch. A path argument means review that file or directory whole.

Locate the originating issue, PR description or user request. If none is
available, report "no spec" for that pass rather than inventing requirements.
Trace definitions, callers, tests and every changed public concept before
reporting a finding.

## 2. Run five passes

Use independent subagents for separate passes when available; otherwise run them
sequentially. Give each the pinned diff, spec and relevant repository docs.

1. **Correctness:** wrong topic output, missed checks, broken errors, path escapes,
   symlink handling, encoding and Python 3.8 compatibility. Preserve fail-closed
   behavior and keep version output independent of router configuration.
2. **Rules:** documented scope, version agreement, release authorization, native
   platform contracts and verification requirements. Cite the actual rule.
3. **Spec:** missing or partial requirements, unintended behavior and scope
   expansion. Tie each finding to the request or spec.
4. **Consumers:** sweep the source script, routed fixture, templates, skill,
   README locales, native manifests, release configuration, workflow and tests
   for every changed concept. Report consumers that were missed.
5. **Cleanup:** duplicate mechanisms, unused code, extra dependencies or options,
   and fixes placed in one caller instead of shared code. Label judgment calls.

Each proposed finding needs a file and line plus a concrete input or state that
produces the wrong result. Style preferences alone are not findings.

## 3. Verify and report

Read every cited location and confirm the scenario, using the narrowest relevant
check where practical. Mark findings **confirmed** or **plausible** and state
what remains unknown; discard disproved and duplicate findings.

Report findings separately by pass, followed by executed checks and limitations.
Distinguish pre-existing issues from regressions. If fixes are authorized, apply
only confirmed in-scope fixes, add a focused regression check where practical,
and rerun the affected checks. Commit, push, public comments and publication
require the user's authorization; a review request alone is read-only.
