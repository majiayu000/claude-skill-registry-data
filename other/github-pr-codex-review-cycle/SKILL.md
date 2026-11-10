---
name: github-pr-codex-review-cycle
description: Use only when the user explicitly invokes `$github-pr-codex-review-cycle`, names `github-pr-codex-review-cycle`, or requests the full `github-issue-delivery` workflow for named issues.
---

# GitHub PR Codex Review Cycle

## Scope

Use this orchestration skill to run the normal end-to-end cycle after an
implementation is ready: publish the current work as a pull request, request
Codex review, wait for the actual review output, address worthwhile AI review
feedback, then commit, push, reply, and resolve the handled review threads.

This skill intentionally composes existing skills. Do not copy their detailed
workflows here.

Required sub-skills:
- `github-pr-publish`
- `github-pr-review-request`
- `github-pr-ai-review-followup`

Use `github:gh-address-comments` whenever thread-level review state, inline
context, replies, or resolution matters.

This skill is not for:
- implementing feature work before publication
- Copilot review requests unless the user separately asks
- human review sweeps
- merging pull requests
- deleting branches or worktrees
- force pushing, rebasing, amending, or history rewriting

## Approval Model

An explicit invocation of this cycle, or an explicit request for the full
`github-issue-delivery` workflow for named issues, selects this cycle on the
requested feature branches. Delegated calls follow
[Delegated Authorization](../delivery-common/SKILL.md#delegated-authorization);
the exact target is the requested feature branches. Honor stricter applicable
approval instructions. Within those rules, treat the explicit request as
approval for the normal, non-destructive cycle:

- verification required by `github-pr-publish`
- ordinary commit of the requested implementation work
- normal push of the current feature branch
- pull request creation or reuse
- posting the `@codex review` trigger comment
- applying worthwhile Codex or Copilot review fixes
- ordinary commit and normal push for review-follow-up fixes
- short GitHub replies to the latest AI review threads
- resolving latest AI review threads with dispositions that clearly close them:
  `applied`, `stale`, `duplicate`, or fully answered `explained`

Still stop and ask before:
- publishing from the default branch
- staging secret-like files, credentials, local config, or unrelated changes
- force push, rebase, amend, reset, merge, branch deletion, or worktree removal
- dependency manifest or lockfile edits unless already explicitly part of the
  requested work
- resolving `needs-human-decision`, ambiguous, conflicting, risky, or still
  reasonably disputed review feedback
- broad formatting, generator, or snapshot changes not required for the review

## Workflow

1. Resolve the target branch or worktree.
   - Resolve and process targets under `github-pr-publish` step 1, across the
     whole cycle.
   - On resume, revalidate any supplied PR/head/trigger and follow-up record.
     Reuse verified completed operations and enter the earliest incomplete phase.
     If a trigger already awaits output for the same published head, resume step
     4 rather than posting another request. If matching output already completed,
     continue with Prepare or the pending publication/Writeback phase. Evidence
     for an older head does not satisfy a review of the current head.
2. Use `github-pr-publish`.
   - Preserve that skill's verification, staging, commit, push, and PR rules.
   - Capture the PR number, PR URL, branch, push remote, commit, and
     verification result.
3. Use `github-pr-review-request` with provider `codex` for the resolved PR.
   - Treat `Codex request posted but not acknowledged` as a blocker unless the
     user explicitly asks to continue waiting or retry.
4. Wait for Codex review completion.
   - Codex posts a summary comment starting with
     `<!-- codex-pull-request-review-summary -->` and edits it in place. Read
     its `<!-- codex-review-state:v1 {...} -->` JSON only when the comment's
     `updated_at` is later than the trigger comment's `created_at`; an older
     marker belongs to an earlier request. Track only `code_review`; this cycle
     requests no security review.
   - Review completion requires actual Codex review output after the trigger:
     a review, review threads, or inline comments; or a marker whose
     `code_review.status` is `completed` and whose `code_review.commit_sha`
     equals the full published head SHA.
   - A marker with `code_review.status` `running`, `null`, or missing, or with
     another `commit_sha`, is not completion; keep waiting.
   - A completed marker with `has_any_findings: false` means no actionable
     feedback: continue at step 8. With findings, wait for the review threads
     before step 5.
   - If no summary comment has the marker or its JSON does not parse, fall back
     to a review summary/comment that indicates the run finished, and report
     that completion was inferred without the marker.
   - Poll the PR comments/reviews/thread state at reasonable intervals and keep
     the user updated during long waits.
   - If no actual review output appears within a practical bound, report the PR,
     trigger comment, acknowledgement state, and last checked time. Do not run
     review follow-up against stale or absent output.
5. Use only the **Prepare** phase of `github-pr-ai-review-followup` on the
   latest Codex review feedback.
   - Forward any earlier dispositions and assessment defaults the caller supplied.
   - Capture its prepared record, including per-thread dispositions, verification,
     proposed replies, and pending publication. Do not reply or resolve yet,
     even though this cycle authorizes later writeback.
6. If review fixes changed files, commit and push the verified fixes.
   - Reuse Prepare's successful verification if no relevant files changed after
     it; otherwise run the smallest relevant verification for the changed files.
   - Stage only review-follow-up changes.
   - Stop and report `<branch>` unless it is a **safe branch name**: run
     `node <script> -- '<branch>'`, where `<script>` is
     [`check-branch-name.mjs`](../delivery-common/scripts/check-branch-name.mjs)
     resolved from this skill's directory, and continue only on exit 0. Write a
     name into this or any command only when it uses solely ASCII letters,
     digits, `/`, `.`, `_`, and `-`; any other name is not safe, without running
     the check.
   - Use a normal commit, then push with
     `git push <remote> <branch>:refs/heads/<branch>`. `<remote>` is the push
     remote captured in step 2, used as is. On resume without it, resolve
     `<remote>` by the push target rule in `github-pr-publish` step 2: run
     `node <push-script> resolve --github '<host>' '<owner>/<repo>'` with the
     PR URL's host and the PR's head repository
     (`gh pr view --json headRepository,headRepositoryOwner`), writing the
     host into the command only when it uses solely ASCII letters, digits,
     `.`, and `-`, optionally followed by `:` and digits, and `<owner>/<repo>`
     only when it uses solely ASCII letters, digits, `.`, `_`, `-`, and one
     `/` (otherwise stop and report), where `<push-script>` is
     [`check-push-target.mjs`](../delivery-common/scripts/check-push-target.mjs)
     resolved from this skill's directory, and use line 1 on exit 0.
     Otherwise stop before the push and ask the user to confirm or name the
     remote; use a remote the user names as given. The explicit remote and
     refspec keep `branch.<branch>.pushRemote` or `remote.pushDefault` from
     sending the fixes away from the PR head.
   - If verification is unsuccessful or unavailable, stop before commit or push.
     If verification, commit, or push fails, stop the cycle and report; do not
     enter step 7.
   - Add the published commit to the prepared record.
7. Use only the **Writeback** phase of `github-pr-ai-review-followup`.
   - Pass the prepared record, publication evidence, and existing authorization
     for clearly closed latest AI review items under the Approval Model.
   - Delegate target revalidation, replies, resolutions, and writeback verification
     to that phase. Do not reapply fixes or duplicate its writeback procedure.
8. Verify final PR state when possible.
   - Re-read thread state after writeback.
   - Report unresolved, skipped, ambiguous, or human-decision items.

## Completion Criteria

The cycle is complete only when one of these is true:

- Codex review output was inspected, worthwhile fixes were handled, verification
  passed, needed commits/pushes were done, and clearly closed threads were
  replied to and resolved.
- Codex produced no actionable feedback, and final thread/comment state was
  checked.

If a blocker prevents completion, report `Blocked`, or `Partial` when only some
targets or writebacks completed, with the exact next approval or external state
needed. Reporting a blocker does not make the cycle complete.

## Final Report

Use this structure:

```markdown
**Cycle Status: <Complete | Blocked | Partial>**
- Branch: `<branch>`
- PR: <url>
- Publish: `<commit, no new commit, or blocked>`; verification `<command and actual result>`
- Codex: `<acknowledged/completed/blocked summary>`
- Follow-up: `<applied/explained/skipped/pre-existing/stale/duplicate counts>`
- Not applied: one line per item not `applied`, from the prepared record:
  `<thread>`: <finding> - `<reviewer label>` - `<triage class>` - `<disposition>`: <reason>; or "None"
- Review fix commit: `<sha>` or "No review-fix commit needed"
- Writeback: `<replied/resolved counts>`

**Open Items**
- <unresolved or human-decision items, or "None">
```
