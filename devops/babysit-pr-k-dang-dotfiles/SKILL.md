---
name: babysit-pr
description: Monitor a pull request through review and CI. Use when the user asks to monitor, watch, or babysit a PR.
---

# Baby-sit PR

All the repos we work in have various AI review bots. They're helpful, even if they are not always right.

If your harness offers tools to monitor a PR, use them so you can respond when comments arrive. Otherwise, poll the PR for new comments and checks.

Only act on checks and comments newer than the latest push. Verify every bot findings against the source before changing code. Fix real findings and CI failures, distinguish repository failures from infrastructure flakes, and reply with a written reason when dismissing false positives.

If a review bot leaves feedback you believe is not worth addressing, reply and resolve the comment.

Do not let review feedback expand the PR beyond the user's original goal. Address real shortcomings, but avoid scope creep.

If nothing has changed, stay quiet rather than posting filler comments. Stop when the review bots and required checks are green on the latest commit.

Drive one open PR through this **merge gate**. Address valid feedback; do not obey it blindly. Never merge the PR.

## 1. Resolve the target

Use an explicit PR URL/number when supplied; otherwise resolve the PR for the current branch. Run:

```bash
python3 scripts/snapshot.py [PR]
```

Resolve `scripts/snapshot.py` relative to this skill directory.

Confirm:

- PR is open and local repository matches it.
- Current branch is its head branch and local `HEAD` matches the remote head. If not, safely fetch/check out the correct branch before editing.
- Working tree has no unrelated changes. If it does, stop and ask how to protect them.
- Whether the branch belongs to a stack. If stacked, load `gh-stack` before mutating branches.

Completion: one PR, repository, head SHA, base, stack position, and clean editing surface are known.

## 2. Start the watch

Use the stated duration. If none was given, ask for one focused duration. Do not invent an endless watch. Read [`WATCH.md`](WATCH.md) before continuing.

Run the merge-gate pass below immediately. Repeat it only when the snapshot changes.

Completion: watch deadline is explicit.

## 3. Set the scope fence and triage

Derive a **scope fence** from the issue/PRD acceptance criteria, PR title/body, and current diff. Feedback fits inside the fence only when needed to:

- satisfy the stated change
- fix a defect or security problem introduced or exposed by this diff
- add proof required for those behaviors

Pre-existing debt, adjacent enhancements, speculative abstractions, broad refactors, and reviewer preferences outside those goals stay outside. A concern may be valid and still not belong in this PR.

Account for every item in the snapshot:

- issue comments
- submitted reviews
- inline review comments and review threads
- requested changes and review decision
- failed, pending, cancelled, or skipped checks

Classify each item as:

- **actionable/in-scope** — correct and necessary inside the scope fence
- **valid/out-of-scope** — real concern, but not part of this block of work
- **already addressed** — current head proves it fixed
- **stale/duplicate** — superseded or repeats another item
- **informational** — status, assignment, praise, or bot noise
- **decision** — resolving it requires product, architecture, security, or scope expansion judgment

Use code, tests, repository instructions, and the scope fence as evidence. Never treat reviewer confidence as proof. Ask the user about **decision** items before editing. Do not expand the fence merely to satisfy a reviewer.

Give every finding produced by a review bot or AI reviewer a **quoted disposition**. Preserve the exact finding instead of replacing it with a paraphrase, then state its classification, response, evidence, and action. Keep separate findings in separate quote-response pairs:

```markdown
> Exact AI code-review finding

Classification. Response, evidence, and action taken.
```

Carry each quoted disposition into the final report, and into a PR reply only when section 6 calls for one.

Completion: scope fence is explicit; every feedback item and non-green check has one evidence-backed classification; every AI code-review finding has a quoted disposition; no item is silently skipped.

## 4. Clear actionable work

For each **actionable/in-scope** item:

1. Make the smallest correct code/test/docs change on the PR's branch.
2. Stop and reclassify as **decision** if the fix requires a new subsystem, migration, public contract, broad refactor, or materially larger diff. Do not smuggle scope expansion in as cleanup.
3. Fix branch-caused CI failures; rerun confirmed unrelated flakes once, then report them rather than changing code to appease them.
4. Run focused tests and relevant lint. Never add lint disables or package-todo entries to force green.
5. Inspect the resulting diff against the scope fence; remove unrelated changes.

Keep one writer. Read-only reviewers may run in parallel; edits, commits, rebases, and pushes may not.

Completion: every actionable/in-scope item is fixed locally, focused validation passes, and diff contains only intended changes.

## 5. Prove the current head

Check that PR title and body accurately explain the problem, solution, validation, and linked issue using the repository template. Repair stale metadata.

Review the PR diff against its actual base with fresh context along two angles in parallel. Give both reviewers the scope fence:

- correctness, regressions, and match to PR/issue intent
- test gaps, simplicity, and repository standards

Reuse a comprehensive review only when it covered the same head SHA. Dedupe findings and keep only high-confidence **actionable/in-scope** work; report valid out-of-scope findings without implementing them. Apply fixes with one writer, then review the new head again. Cap at three review rounds; always fix round-three findings, but report the final fixes as unverified rather than claiming clean.

Completion: metadata matches the current diff and a fresh round returns zero actionable/in-scope findings, or round three fixes are applied and explicitly marked unverified.

## 6. Publish and close the loop

Post a PR comment only for feedback you are **not** fixing in code. When a code change addresses a finding, the pushed commit and the resolved thread are the record - do not narrate the fix in a comment.

Reply when, and only when:

- you decline the finding (false positive, stale, duplicate) - give concise evidence
- the finding is **valid/out-of-scope** - acknowledge it, name the scope boundary, suggest follow-up
- the finding needs a **decision** you cannot make
- a reviewer explicitly asked a question

When you do reply to AI code-review feedback, post its quoted disposition. For other feedback, quote enough context to make the reply unambiguous.

When changes exist:

1. Commit normally; never amend or force-push unless explicitly authorized.
2. Push the branch. For a stack, put the fix on the correct layer, rebase affected upstack branches, and push through `gh-stack`.
3. Resolve the thread for each fixed finding once its fix is pushed. Do not comment on it. Do not resolve a genuine decision or disagreement as though it were fixed.
4. Refresh the snapshot. Re-run affected checks or wait for the new head's checks; never use the old head's green status.

Do not create a ticket or implement out-of-scope follow-up unless the user asks. Every fix you made lands in the final report of section 7, not in a running commentary on the PR.

Completion: remote head matches local head, replies describe reality, no comment narrates a fix, and every resolved thread is backed by the pushed head.

## 7. Evaluate the merge gate

Report exactly one state:

- **MERGE_READY** — no actionable feedback or unresolved change requests; proactive review clean; required checks green; required approvals satisfied; PR non-draft, conflict-free, and mergeable; local tree clean and synced.
- **AWAITING_REVIEW** — all agent-controlled work passes, but human approval or reviewer re-review remains.
- **BLOCKED** — a decision, external failure, conflict, permissions problem, dirty worktree, or review cap prevents proof.
- **WATCH_COMPLETE** — watch deadline reached; include underlying gate state and all events handled during the window.

List PR URL, scope fence, pushed commits, validation, every AI code-review quoted disposition, valid out-of-scope feedback with reasons, unresolved threads, checks, approvals, and blockers. Never call a PR merge-ready while any gate condition is unknown.

Completion: state is supported by a final snapshot of the current remote head.
