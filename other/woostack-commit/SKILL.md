---
name: woostack-commit
description: Commit the current authorized outcome and, when requested, publish or update its pull request. Use for a local-only commit, a requested draft PR, or a commit from an established task that already names its issue.
---

# woostack-commit

Commit the changes belonging to the current authorized outcome and deliver them as far as the
caller requested. An explicit `/woostack-commit` publishes; a natural-language commit-only request
or `--no-pr-update` stops after the local commit. Issues are optional: no issue, Project,
assignment, lifecycle record, or attribution trailer is required to commit or update a PR.

This skill mutates Git state and, for requested PR delivery or maintenance, GitHub PR metadata.
It never merges, enables auto-merge, queues a PR, amends unrelated commits, or stages unrelated
work. It never discovers work from recent activity or creates an issue or Project implicitly.

## Invocation

```text
/woostack-commit [message]
/woostack-commit --no-pr-update [message]
/woostack-commit --issue <issue> [--issue <issue> ...] [message]
```

`message` is optional. An inaccurate supplied message is corrected, not obeyed.

`--issue` accepts an issue number, an issue URL, or an unambiguous issue already named in the
request or the established task context, and repeats for every related issue this delivery covers.
It is shorthand, not a required input shape, and it never selects the work: resolve the actual
repository and issue before associating it, and ask when identity or intent is genuinely
ambiguous. Branch text, PR text, a title, an issue key, and search results are evidence, not
authorization. Issue context alone grants no publication authority, and it never selects a parent
just because the task names a child.

## Workflow

1. **Inspect and prepare.** Git resolves the inspection state from any directory inside the
   worktree; no particular location is required. Follow the delivery
   [prepare and verify](references/delivery.md#prepare-and-verify) procedure: inspect the branch,
   intended base, index, and diff to classify the change against the authorized outcome; block on
   unresolved conflicts, a detached head, a competing writer on this worktree, protected-primary
   work, or a changed path that genuinely cannot be classified. Reuse observed results from the
   existing worker result, handoff, plan, or verification summary only after independently
   assessing applicability under
   [When evidence still applies](references/tdd.md#when-evidence-still-applies), and handle slow
   checks, missing capability, timeouts, and other unverified requirements under
   [Slow checks](references/tdd.md#slow-checks-bounded-diagnosis-no-waiver). Required hooks and the
   configured `commit.command` run when nonempty regardless of reused test results. An unresolved
   required commit-check failure or an out-of-scope correction stops the commit; never skip required
   checks or weaken assertions. Missing implementation acceptance remains unmet but does not block
   an authorized draft unless it is an explicit commit or publication gate. Disclose unmet criteria.
   For metadata-only maintenance or
   readiness, reuse the existing commits and skip preparation, staging, commit, and push when no
   ref change is needed.

2. **Stage and commit.** Follow the delivery
   [select and commit](references/delivery.md#select-and-commit) procedure: stage explicit paths or
   hunks, keep the user's unrelated staged and unstaged work untouched, and commit exactly the
   reviewed selection. Require no new file, schema, receipt, hash inventory, or cache subsystem.

3. **Publish when requested.** With `--no-pr-update`, stop here: no push, PR, stack, or issue
   write, and no remote read is required. Keep known PR evidence without claiming a read that did
   not happen, and report remote identity as unverified rather than claiming absence or successful
   delivery. Otherwise follow the delivery
   [publish and read back](references/delivery.md#publish-and-read-back) procedure: publish the
   task branch, reuse the matching open PR or create a new draft, apply its title/body,
   issue-reference, and requested-note rules, and register
   [native stack membership](references/source-control.md#native-stack-membership) only when the
   request or repository workflow requires it. Rewrites require explicit maintenance scope.

4. **Verify delivery.** Confirm the procedure's read-back with your own eyes: the published ref is
   the intended head, the PR is the intended one with the intended base, and the title and body are
   present as written. Preserve existing readiness unless its change was requested. Recheck
   whatever a step changed or left uncertain, and read nothing further than that decision needs.
   After an unknown write, discover what actually happened and resume from the first unproved
   step. Never repeat a commit, push, PR update, stack link, or comment because a response was
   lost.

## Requested PR maintenance and readiness

Explicit published-PR rebase/restack requests authorize scoped rewrites, publication, base changes,
and native membership reconciliation; readiness-only requests work without a new commit. Ordinary
commits and comment corrections do not authorize restacking unrelated PRs; restacking alone does
not authorize readiness. Identify selected PRs, intended bottom-to-top order, heads, bases, and
affected stack members from evidence; state scope and order before writing. Ask only about material
unresolved choices or collateral effects, not for another approval packet.

Keep original heads recoverable, each PR identity and intended change intact, and unselected
branches, members, and local edits untouched. Follow the
[scoped lease safeguard](references/source-control.md#published-head-safeguard) and supported
native membership operations. Existing membership and non-top parents require planning, not
refusal; resolve any whole-stack effect on unselected members before writing. Re-read partial or
uncertain results; report genuine provider or permission limits.

Inspect each complete PR diff against its intended base and the combined stack diff against trunk:
retain predecessor changes without unrelated commits or dropped work. Read back heads, bases,
native order/membership, and requested readiness; refresh checks on new heads. New PRs default
to draft; existing readiness is unchanged absent a request. Ready does not prove checks or grant
approval or merge authority. Never change protections, credentials, or standing policy for maintenance.

## Report

Report the commit subject and SHA, the canonical PR URL or an explicit local-only result, the
verification actually observed, and any unresolved work. Add branch, path, stack, or note detail
only when it helps review or continuation. Never claim a commit, remote write, check, or reference
that was not independently read back.
