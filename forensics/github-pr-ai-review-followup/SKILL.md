---
name: github-pr-ai-review-followup
description: Use when the user wants to follow up on GitHub Copilot or Codex review feedback on a pull request, including AI review threads that may need code fixes, explanations, or resolution.
---

# GitHub PR AI Review Follow-Up

## Scope

This skill covers GitHub Copilot and Codex review feedback and the decision record for each AI review thread. It is not for human review sweeps, generic bot spam, unattended GitHub writeback, PR publishing, or merge handling.

## Phase Selection

Use two phases: **Prepare** for inspection, local fixes, verification, and a
writeback preview; **Writeback** for approved GitHub replies and resolutions.
Run Prepare by default. A caller can request Prepare only even when writeback
is already authorized; authorization does not bypass publication prerequisites.
Run Writeback only when requested or approved and its prerequisites below hold.
For a Writeback-only handoff, consume the prepared record without reapplying fixes.
This skill does not commit or push; the user or an orchestration skill owns publication.

## Prepare

1. Resolve the current-repo PR from a provided number/URL or the current branch; ask if ambiguous.
2. Fetch PR metadata and AI review comments with the GitHub plugin.
3. When inline context, resolution state, stale/outdated state, or GitHub writeback matters, follow `github:gh-address-comments`; flat comment reads are insufficient.
4. Identify the latest Copilot or Codex review feedback. If the source is ambiguous, say so instead of guessing. When the caller supplies earlier dispositions or assessment defaults, apply them; an item already dispositioned earlier is a `duplicate` of that item unless new evidence changes the assessment.
5. Split feedback into actionable, explanation-only, pre-existing, stale/resolved/duplicate/non-actionable, and ambiguous/conflicting/risky items. Classify `pre-existing` under [Triage classes](../delivery-common/references/local-review.md#triage-classes); for a PR, the merge-base is that of its head and base branch.
6. Apply only the worthwhile local fixes. Skip speculative churn, style-only noise, and anything likely to cause regression. Defer minor and pre-existing items by default; a `material` item under [Triage classes](../delivery-common/references/local-review.md#triage-classes) is never minor. When fixing an item, fix other instances of the same bug class in the PR diff in the same round.
7. Run the smallest relevant verification for local fixes and record its result.
   If it fails or cannot run, report the cause and leave the fixes unpublished;
   do not represent them as verified or ready for writeback.
8. Assign a disposition to every latest AI feedback item, even when no code changed.
   Also give every item a triage class under
   [Triage classes](../delivery-common/references/local-review.md#triage-classes),
   whatever its disposition.
9. Return a prepared record with the repository/PR, inspected head commit,
   review/comment/thread IDs, per-item disposition, triage class (step 8),
   reviewer label (`none` when the reviewer gives none, `unknown` when it
   cannot be read), and supporting evidence,
   changed files, verification result, proposed replies, resolve candidates,
   open items, and any publication still needed. Mark dispositions based on
   local changes as pending publication, including `stale` or `duplicate` when
   their justification depends on those changes.
10. For Prepare-only calls, stop here without GitHub writes. Otherwise enter
    Writeback only if authorized and all prerequisites are satisfied.

## Dispositions

- `applied`: Addressed by local code or tests. Draft a short response and mark as a resolve candidate.
- `explained`: Needs explanation, not code. Resolve only if the explanation fully closes the point.
- `skipped`: Intentionally not applied. Include the technical reason. Leave open if reasonable disagreement remains.
- `pre-existing`: Its triage class is `pre-existing`. Draft a note proposing separate follow-up and leave open unless the user approves resolving it.
- `stale`: No longer applies to the current diff. Draft a stale note and mark as a resolve candidate.
- `duplicate`: Covered elsewhere. Reference the covering item and mark as a resolve candidate.
- `needs-human-decision`: Ambiguous, conflicting, policy-sensitive, or risky. Draft the question or tradeoff and leave open.

## Writeback

1. Require a prepared record identifying the exact PR and feedback items.
   If it is missing, reconstruct it from read-only evidence or report what is
   missing. A Writeback-only request does not authorize new local fixes.
2. For any item whose reply or resolution depends on local fixes, require
   successful relevant verification and confirmation that the fixes are in the
   remote PR head. A local commit or an attempted push is insufficient. If
   verification or publication failed, leave writeback pending and report it.
   Explanation-only items need no new commit when their evidence already holds
   in the published PR.
3. Re-read the remote PR head and target thread/comment state. If intervening
   changes invalidate a prepared disposition or reply, return that item to
   Prepare. Skip already-completed replies/resolutions on resume.
4. Perform only authorized replies and resolutions using the rules below,
   then verify and report their actual outcomes. Preserve per-item partial
   success so a retry does not repeat successful writes.

- Approval to inspect or fix AI review feedback is not approval to write to GitHub.
- Prefer the specific review thread or comment. Use a top-level PR comment only when no thread target exists.
- Keep comments short: outcome, reason, and verification.
- Resolve only unresolved, thread-aware review threads whose disposition clearly closes the feedback: usually `applied`, `stale`, or `duplicate`.
- Do not resolve `needs-human-decision`. Do not resolve `skipped` unless the skip reason fully answers the feedback and the user approved resolving it.
- After writeback, verify the resulting thread state when possible.

Comment shapes:
- `Addressed. Changed <file or behavior>. Verification: <command or not run reason>.`
- `Not changed. Reason: <technical reason>. Leaving open for maintainer decision.`
- `Stale after the latest changes. This no longer applies to the current diff.`

## Guardrails

- Do not reply on GitHub, resolve threads, or submit a review unless the user explicitly asks for that write action or approves the writeback preview.
- Do not treat flat PR comments as a full representation of thread state when thread context matters.
- Do not resolve a thread unless thread-aware data confirms the target and current resolution state.
- Do not assume every Copilot or Codex suggestion should be applied.
- Do not assume cross-repository PRs. This skill is current-repo only.
- If auth, rate limits, or missing PR context block review inspection, stop and report the blocker.
