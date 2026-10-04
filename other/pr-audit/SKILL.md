---
name: pr-audit
description: Audit a specified PR or PR-ready branch for submission or post-revision readiness. Bind the exact base/head, review commits and net changes, run safe project checks and inspect applicable CI. An audit alone does not authorize fixes, history changes or publication.
---

# PR verification

Audit the requested PR or branch, not necessarily the current checkout. Keep
review-only requests read-only apart from safe diagnostic artifacts. If the
user also requested fixes, implement confirmed in-scope defects and re-audit
the changed revision. Do not push, merge, rebase, create a PR, post a review,
rerun CI or change shared settings without the corresponding authority.
Do not invoke a branch-completion menu merely because another plugin exists.

Parallelize independent checks when supported, after binding their common
base/head and tested artifact. Subagents return evidence, not independent
permission to mutate the branch. Reading or auditing this skill does not
request a real PR audit or authorize account operations.

Use `code-audit` for defect review not tied to PR readiness, `design-audit` for
architecture, and `diagnose` for a specific tooling/workflow incident. A request
to run one known check does not need this full workflow.

## Bind scope and revisions

Record the requested repository/forge, PR identity if any, intended base,
full head SHA, and whether the target is committed code or an explicitly
included working-tree proposal. Inspect branch, remotes, index and dirty paths;
preserve unrelated changes and do not treat them as part of the PR.

For GitHub, use the mandated service route and an explicit PR identifier plus
repository, for example after resolving both variables:

```bash
gh pr view "$PR_NUMBER" --repo "$PR_REPO" --json url,state,baseRefName,baseRefOid,headRefName,headRefOid,headRepository,headRepositoryOwner,isCrossRepository
```

Validate the returned URL, base repository and fork/head identity against the
request. Bare `gh pr view` selects the checkout's PR; it is not sufficient when
a URL, fork or another revision was requested. See the
[CLI fields](https://cli.github.com/manual/gh_pr_view).
For another forge, use its supported equivalent rather than inventing gh fields.

Without a PR, determine the intended integration branch from the request or
repository policy. A tracking upstream can be the topic branch itself; it is
not automatically the merge target. Neither `origin` nor a cached default-branch
symbolic ref proves the intended target. Resolve safely from existing evidence;
ask only if the remaining choice materially changes the audit.

Fetch only relevant refs from verified remotes when permitted, preserving the
current checkout and index. Do not clone an unrequested repository. Freeze and
record full `BASE_SHA` and `HEAD_SHA` plus freshness evidence before comparisons.
If a ref moves, distinguish the frozen audit from the newer state. Missing
objects, unavailable network or unknown base remain explicit evidence gaps.

Use different comparisons for different questions:

- Select branch commits with `git log "$BASE_SHA..$HEAD_SHA"`.
- Find all merge bases with `git merge-base --all "$BASE_SHA" "$HEAD_SHA"`.
  For one merge base, bind `MERGE_BASE_SHA` and review the net PR patch with
  `git diff --find-renames "$MERGE_BASE_SHA" "$HEAD_SHA"` (equivalently the
  three-dot diff of the frozen base/head). An endpoint two-dot diff can include
  changes made only on the newer base. Missing or multiple merge bases require
  explicit handling; do not turn command failure or an arbitrary choice into
  an empty/complete review. See [Git diff semantics](https://git-scm.com/docs/git-diff).
- Treat staged/unstaged changes separately if explicitly in scope. They are not
  evidence about the committed head until the reviewed artifact is identified.

## Review commits and final changes

Read every selected commit's full patch, not just its stat or a truncated tool
response. For merges, inspect the relevant parents explicitly; for example
`git show --diff-merges=separate --stat --patch --find-renames COMMIT_SHA`.
Ordinary combined output can omit files or resolution hunks; per-parent views
also contain inherited changes, so attribute them correctly rather than calling
every displayed hunk newly introduced. See [merge formats](https://git-scm.com/docs/git-show).

Check scope, correctness, omissions, accidental duplication and commit-message
accuracy against the project's conventions. Review the complete final net
patch as well: individually plausible commits can compose incorrectly.
Confirm code, docs and tests describe the same final behavior. For restructured
history, compare against the saved pre-rewrite revision when available; do not
invent an earlier baseline or rewrite history to satisfy a cosmetic preference.

Inspect the PR for unintended generated/debug/temp artifacts, file modes,
symlink changes, binary files and accidentally included sensitive data. Legitimate
logging, fixtures or commented examples are not defects merely because a keyword
search found them. Follow secret-handling rules before credential inspection;
report locations and risk, never credential values or private payloads.
Run `git diff --check "$MERGE_BASE_SHA" "$HEAD_SHA"` for the identified net patch;
keep any working-tree whitespace check separately scoped. Preserve intentional
literal whitespace/line-ending requirements rather than applying blanket cleanup.

## Verify the actual artifact

Discover project checks and their effects from instructions, manifests, build
files and CI. Inspect commands before executing them: test/install hooks and
so-called dry runs can write shared state, use credentials or delete files.
Do not execute untrusted scripts, install dependencies or invoke services merely
because a PR names them. Use authorized local checks and explicit isolated
fixtures; unavailable or unsafe checks are not run, not passed.

Bind each result to the exact tested revision/tree and environment. A passing
dirty checkout does not prove the committed PR head passes. When isolation is
needed, use an owned checkout/worktree at the configured outside-Drive location,
after checking checkout hooks/filters and other effects; preserve the user's
checkout/index. Include dependencies and relevant generated inputs in the
provenance. Clean up only owned artifacts. If exact-revision testing is not
possible, report that gap instead of borrowing results from a nearby commit.

Run the documented build/type/lint checks and full applicable test suite when
safe and feasible. Apply `elisp-conventions` for Elisp verification instead of
inventing a batch-compile command or affecting a live Emacs profile. Record
commands, exit status, meaningful counts and warnings. Passing a static check
is not proof of user-visible behavior; directly cover the changed requirement
where applicable, within the task's authority.

Classify baseline failures only with comparable evidence, such as the same
check on the base under the same environment. A warning's age or a failure's
plausible infrastructure explanation is not proof it predates the PR. Preserve
uncertainty and do not hide failures by weakening checks or changing runtimes.

## Check integration and CI

Assess integration against the frozen current base and applicable repository
policy. Being behind the base is not inherently a blocking defect: strict
checks, loose checks and merge queues have different requirements. Record
conflicts, policy requirements and freshness gaps separately. Do not merge or
rebase the user's branch as an audit step. If mergeability is unknown, say so;
ancestry alone does not establish conflict-free integration.

If CI configuration changed, check supported syntax and semantics: actual
commands, dependencies/runtimes, matrix entries, trigger/path filters, required
check names, permissions and secret exposure. YAML parsing or a local dry run
alone does not prove the workflow will trigger or pass remotely.

For an existing pushed revision, use `post-push-ci` in its read-only observation
mode with explicit repository, SHA, event and run attempt. Bind PR merge-ref or
merge-queue checks to the actual tested commit and its relationship to this
head/base; an old green run or unrelated push workflow does not cover this PR.
Include expected required checks and non-Actions checks, not merely returned
rows. Keep pending, failed, skipped/neutral, not applicable and unknown distinct;
platform acceptance of a skip does not prove the work executed. No push or
workflow dispatch is authorized just to obtain missing evidence.

Inspect failing jobs and exact-attempt logs safely. Follow requested monitoring
with bounded, responsive checks; ordinary pending state is not an infrastructure
failure. Distinguish confirmed PR regressions from demonstrated baseline or
external failures without claiming an unknown cause is environmental. A
review-only finding stays a finding; repair and publication require scope.

## Verdict

Lead with ready for the audited scope, not ready, or inconclusive. Tie that
verdict to the exact target and required gates; no blanket ready-to-merge claim
when approvals, policy or required CI remain unknown. Distinguish failed,
pending, not run and genuinely not applicable checks in the audit evidence.

Give actionable findings first, then material evidence gaps and the concise
check results needed to understand the conclusion. Keep a complete per-check
record without forcing a seven-section reply; use private artifacts when
needed, never unsolicited project session logs. Do not offer an unsolicited
publication menu. If fixes were authorized, perform them within scope and
verify the new revision before updating the verdict.
