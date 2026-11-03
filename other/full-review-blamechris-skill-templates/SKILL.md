---
description: "Run a complete review pipeline: agent-review first, then check-pr."
---

# /full-review

Run a complete review pipeline: agent-review first, then check-pr. The agent-review pass naturally fills the ~4 minute Copilot review delay, so check-pr starts with comments already waiting.

## Arguments

- `$ARGUMENTS` - PR number (optional, defaults to current branch's PR)

## Instructions

### Phase 1: Agent Review

Run the `/agent-review` skill on the PR with an independent subagent that did not implement the change. Record the reviewed head SHA. This is a deep expert review that:
- Reads CLAUDE.md and the full PR diff
- Reviews against project-specific code quality, architecture, and testing criteria
- Posts a review comment on the PR
- Creates follow-up issues for deferred suggestions
- Reconciles any from-review issues resolved by this PR

**Capture the results:** verdict, findings counts, issues created/closed. Recorded via
`review-result.py record --agent <id> --skill agent-review --pr ${PR_NUM}` (see agent-review
step 7) — full-review does not repeat that call, only relies on it having run.

### Phase 2: Check-PR

Carry any caller-supplied repair and budget limits into `/check-pr`, `/fix-ci` and fix-delta verification using the same durable run record. Before each correction round, check the remaining applicable allowance and record its consumption before the first edit; read-only triage does not consume a repair round. A restart or nested skill call does not create another allowance. If the allowance is exhausted or cannot be established, retain unresolved blocking findings as `request_changes`, report the limit and return control to the caller for independent work. Do not start another fixer to evade the cap.

After agent-review completes, run the `/check-pr` skill on the same PR. By now, Copilot review has typically arrived (~4 min). This skill:
- Checks posted Copilot review and uses supported waiting when it is still pending (Step 0); a required review remains a gate, while an optional unavailable review is recorded honestly
- Processes inline comments **and general review/issue-comment summaries**, including agent-review findings that have no inline thread
- Verifies each finding and its impact, fixes it, disproves it with evidence, or records an eligible nonblocking follow-up; replies at the original source
- Pushes all fixes and verifies every thread has a reply
- **Resolves verified dispositions via GraphQL**; unresolved blocking findings remain blocking. Replies and issue URLs alone do not establish a fix.
- Cross-references fixes against open from-review issues

**Capture the results:** comments processed, fixes committed, issues created/closed.

Before accepting either phase's verdict, verify each finding and classify its impact. Blocking correctness, security, data-integrity or promised-acceptance defects must be fixed, removed, or contained by an authorized fallback verified to preserve safety, correctness, required runtime/cost constraints and essential capability. Documented low-impact nonblocking findings, including minor findings introduced by this PR, may become follow-up issues when the rationale and evidence show the delivered feature remains acceptable. Do not force another CI cycle solely for those follow-ups. Effort, file count or an issue URL alone does not decide severity or discharge a blocking finding. With verified containment, track the underlying problem and continue; otherwise block this PR and advance independent authorized work.

### Phase 2.5: Verify Current-Head CI

If check-pr pushed any fix commits in Phase 2, CI needs to pass on the new HEAD before merge. Concurrency groups commonly cancel the in-progress run when fixes are pushed, leaving CI stale.

1. Read the current PR head and check results through the host's supported tools.
2. If a check failed or was cancelled, investigate through `/fix-ci` within the shared repair allowance; do not retrigger a healthy pending run.
3. After a fix or branch update, require fresh CI for the new head. With no new commits, verify that the existing results cover the current head.
4. Pending or unavailable CI stays pending. Use supported host continuation; do not substitute prohibited polling or claim that green CI was established.

**Capture the results:** CI status, any action taken (retrigger/fix/escalate).

### Phase 2.6: Fix-Delta Verify

Fix rounds get their own review. If Phase 2 or 2.5 pushed fix commits, adversarially verify the
**fix delta itself** — not just re-check the original diff. The characteristic escaped
defect is in the code written to fix the previous finding, and the test written alongside
a fix is often structurally blind to it (a fixture that cannot produce the failure it
guards; a test asserting only the case where the claim was already true; deletions the
suite never notices).

1. Diff all commits added since the Phase 1 reviewed SHA, including CI repairs (`git diff <reviewed-sha>..<current-head>`).
2. Spawn a verifier scoped to that delta's behavior changes, prompted to REFUTE the fixes.
   **Refute-stage cap: at most 3 refuters per finding, and the whole review — dimensions,
   refuters, verifiers — stays within the hard 20-agent workflow cap.** When findings are
   many, queue refutation rounds; never let finding count widen the fan-out past the cap.
3. Tell the verifier explicitly that **"nothing found" is a valid result** — it must not
   manufacture findings to justify the pass.
4. A real finding loops back through Phase 2 only while the shared correction allowance
   and workflow-agent cap permit it (fix → reply → resolve → re-verify the new delta).
   Classify new findings by the same impact rule before starting a correction round.
   At exhaustion, keep blocking findings blocked and return their evidence and consumed limits.
   "Nothing found" proceeds to the final acceptance/merge gates, not directly to merge.

If the head has not changed since Phase 1, skip (nothing new to verify). If further review fixes change it, repeat affected review and CI checks within the shared allowance.

**Capture the results:** verified/skipped, findings looped back (if any).

### Phase 3: Combined Summary

Check the current head against the PR's promised acceptance and all findings from both phases, including general summaries and any carried-forward deferrals. Reconcile the head SHA covered by the independent review, fix-delta verification and CI; any uncovered change requires its affected checks before declaring delivery gates passed. Declare a clean verdict only when every disposition has evidence and no blocking defect or promised-acceptance gap remains uncontained. Resolved threads, green CI and filed issues are necessary records where required, not substitutes for this check. Preserve the repository's merge authority and safety gates. For delegated implementation, return the verified verdict to the delivery workflow so it proceeds through merge and ledger recording without another routine approval in either ordinary or prime mode. A standalone review-only request ends with its review result.

Output a **single combined summary table** covering both phases. This is the PRIMARY output.

```markdown
| PR | Review | Check-PR | CI | Changes | Issues |
|----|--------|----------|----|---------|--------|
| #XX | Verdict (N critical, M suggestions) | P comments → Q fixed | PASS (after retrigger) | brief change 1, change 2 | Created: #A, #B. Closed: #C, #D |
```

**Column guide:**
- **Review:** Verdict + finding counts from agent-review
- **Check-PR:** `N comments → M fixed` (add `, X false pos` / `, Y deferred` if any)
- **CI:** Status at the recorded head from Phase 2.5: `PASS`, `PASS (after retrigger)`, `PASS (after fix)`, `PENDING`, `FAILED` or `UNKNOWN`.
- **Changes:** Comma-separated brief descriptions of what changed (2-5 words each, from check-pr fixes)
- **Issues:** Combined from both phases. `Created: #X` for new follow-ups. `Closed: #Y` for resolved issues. Deduplicate (agent-review may create issues that check-pr then closes).

Then below the table:
- Full commit hashes for each fix
- Reasons for any false positives
- URLs for all created/closed issues
- Reviewed head SHA, remaining gates and verdict for the delivery workflow

## Execution Notes

- **Sequential, not parallel.** Agent-review MUST complete before check-pr starts. This is by design — the delay lets Copilot review arrive.
- **Same branch.** Both skills operate on the same PR branch. Check-pr may commit fixes on top of the reviewed code.
- **Deduplication.** If agent-review creates a follow-up issue and check-pr's fixes resolve it, close the issue in Phase 2 with a PR cross-reference.
- **Findings verified before declaring done.** Check-pr's step 6b resolves supported dispositions. All required threads must be resolved before merge, and general-review findings must be accounted for even without a thread. Do not clear a defect by resolving its conversation.
- **Attribution.** Follow Zero Attribution Policy throughout — no AI mentions in commits, replies, or issues.
