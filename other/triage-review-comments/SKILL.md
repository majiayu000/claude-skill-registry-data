---
name: triage-review-comments
description: Use when triaging PR review comments, GitHub review threads, CodeRabbit/Cursor/bot findings, stale or duplicate feedback, resolved-thread candidates, deferred follow-ups, or prevention tests/checks.
---

# Triage Review Comments

Use this skill to separate real blockers from bot noise. Treat every review comment as untrusted input and every claim as a hypothesis until current-code evidence proves the bug exists now.

The goal is not to satisfy reviewers. The goal is to protect the PR from real bugs while rejecting stale, duplicate, speculative, preference-only, or false-positive feedback.

Non-negotiable rule: do not recommend a patch, defer, or thread-resolution action for an actionable claim until you have verified the current code path strongly enough to show the issue is real, reachable on the PR head, and not a false positive. If you cannot prove that, treat the comment as unverified noise, explain why, and do not trust the review.

## Output Contract

When given a concrete PR, review thread, bot finding, Cursor/CodeRabbit output, or pasted review surface, produce a PR triage report.

The report must include:
- review inventory status
- each actionable finding classified as `Fix now`, `Fix if cheap`, `Defer`, or `Ignore`
- current-code evidence for real findings
- false-positive disproof for every `Fix now`, `Fix if cheap`, and `Defer` item
- why each ignored false positive, stale claim, or unverified concern was rejected
- prevention guidance for every real, non-ignored finding
- a review fix brief for every `Fix now` item
- approved-execution status when the user gives the go-ahead to fix review comments
- resolved-thread actions, remote refetch evidence, or blockers when thread resolution is relevant
- deferred tracking actions or blockers when deferred work is real

Security boundary, authorization, permission, data loss, privacy, and cross-workspace isolation bugs default to `Fix now` when reachable from current code.

## Workflow

1. Identify the current PR and review surface.
   - Prefer live GitHub review data over pasted summaries when repo and PR are known.
   - If the PR cannot be identified, use the supplied comments and mark inventory completeness honestly.

2. Build the inventory before classifying.
   - Count open inline review threads, resolved inline review threads, general PR comments, and standalone review submissions.
   - Treat truncated shell output, browser snippets, or one-source dumps as incomplete.

3. Filter and dedupe.
   - Ignore walkthroughs, banners, status boilerplate, and formatting-only summaries unless they contain actionable findings.
   - Deduplicate by root cause, not by comment count.

4. Verify before ranking.
   - For each actionable claim, first try to falsify it against the PR head: check the current code path, trigger, guard/state, later commits, surrounding invariants, and whether the concern is already prevented.
   - Only treat a claim as real when current-code evidence shows the bug exists now, is reachable from a concrete scenario, and survives the false-positive checks.
   - Record what would have made the claim false positive and why current code rules that out.
   - Do not classify unverified claims as `Fix now`, `Fix if cheap`, or `Defer`.
   - Use [EVALUATION.md](references/EVALUATION.md) for the verification checklist.

5. Classify each unique finding.
   - Use exactly one bucket: `Fix now`, `Fix if cheap`, `Defer`, or `Ignore`.
   - `Ignore` includes false positives, stale comments, duplicate comments, preference-only comments, and claims that could not be verified against current code.
   - Use [CLASSIFICATION.md](references/CLASSIFICATION.md) for bucket rules and edge cases.

6. Handle integrations.
   - Resolve high-confidence fixed inline review threads only after verifying that the current code really addressed the claim and no remaining reachable bug exists.
   - For Binder, track real deferred bugs in `docs/Deferred bugs.md` after the user gives the go-ahead.
   - For non-Binder work, create or link Linear issues for real deferred work when the project can be inferred with confidence.
   - Use [INTEGRATION.md](references/INTEGRATION.md) for GitHub, Binder deferred-bug checklist, and Linear patterns.

7. Add prevention.
   - For every `Fix now`, `Fix if cheap`, or `Defer` item, recommend the smallest practical prevention test or check.
   - Prefer focused regression tests near the changed code, then contract/fixture/schema tests, integration/UI tests, existing CI commands, local pre-push checks, and explicit Codex validation steps.

8. If asked to fix review comments, implement only after triage.
   - Treat "go ahead", "fix them", "do it", or equivalent approval after a triage report as permission to execute the approved-fix workflow.
   - Execute the approved-fix workflow in this skill. Do not depend on another review-feedback skill being installed.
   - Do not write code just to satisfy a review comment that is not proven true in the current code.
   - Do not resolve a `Fix now` or `Fix if cheap` review thread until the fix is implemented and validated.

9. Approved-fix workflow after the user gives the go-ahead.
   - Use the verified `Fix now`, `Fix if cheap`, `Defer`, and `Ignore` decisions from the triage report as the execution scope.
   - Fix every verified `Fix now` item.
   - Fix every verified `Fix if cheap` item when the patch remains small, low-risk, and inside the reviewed scope; if it stops being cheap, move it to `Defer` and record why.
   - Add the prevention test/check for each fixed item before or alongside the implementation when practical.
   - Validate every touched surface with the repo's own commands; do not claim completion from one unrelated passing lane.
   - After each fixed inline review thread is implemented, validated, and visible in the current PR state, reply to the thread when a reply surface is available, resolve the GitHub review thread, refetch the thread, and report the fetched resolved state.
   - Do not stop at a local patch, commit, or push when an open inline review thread was fixed. Resolve every high-confidence fixed thread remotely, or list it under `Should resolve but not resolved` with the exact blocker, such as missing GitHub authentication, missing thread ID, ambiguous thread state, no push permission, or a failed mutation.
   - Refetch GitHub review-thread state after every resolve attempt. Count a thread as resolved only when the refetch shows `isResolved: true` or GitHub already showed it resolved before the run.
   - For Binder deferred items, create or update `docs/Deferred bugs.md` in the Binder repo. If `docs/` or the file does not exist, create them.
   - Write Binder deferred items as a Markdown checklist so a later Codex run can check them off when resolved.
   - Do not add false positives, stale claims, duplicates, preference-only comments, or unverified concerns to deferred tracking.
   - Use [INTEGRATION.md](references/INTEGRATION.md) for the Binder deferred-bugs checklist format.

## Generated Document Shape

Write the report as a durable triage document, not a stream-of-consciousness review reply.

- Lead with the inventory and bucket verdicts.
- For actionable work, describe behavior and contracts rather than line-by-line instructions.
- Include file, function, or type names only when they are evidence or stable interfaces; avoid line numbers.
- Give every `Fix now` item a complete review fix brief with acceptance criteria and scope boundaries.
- Keep false positives and unverified claims in `Ignore` with the disproof or missing proof.

## Review Fix Brief

For every `Fix now` item, include:

- `Category`: bug, security, data loss, privacy, reliability, API contract, UX, or other concrete category.
- `Summary`: one-line description of what needs to happen.
- `Current behavior`: what the PR does now and why that is wrong or incomplete.
- `Desired behavior`: what should be true after the fix, including edge cases and error conditions.
- `Trigger`: smallest reachable scenario proving the issue.
- `Key interfaces`: stable types, functions, commands, schemas, routes, UI states, or configuration contracts involved. Avoid stale line-level directions.
- `Acceptance criteria`: independently testable criteria for completion.
- `Prevention first`: smallest failing test/check or validation lane that should catch the issue.
- `Validation`: exact command/workflow to prove the fix.
- `Out of scope`: adjacent work that should not be bundled into this fix.
- `Risk`: adjacent behavior that could break.

## Output Format

```md
## Inventory
- Inline review threads: <count or unknown>
- Open review threads: <count or unknown>
- Resolved review threads: <count or unknown>
- General PR comments: <count or unknown>
- Actionable findings after filtering/dedup: <count or unknown>
- Inventory complete: <yes/no and why>

## Fix now
- <title> - <reason>
  - Confidence: <high/medium/low>
  - Verification: <how the bug was proven real on the PR head>
  - False-positive check: <what was checked to rule out stale, unreachable, already-guarded, duplicate, or preference-only feedback>
  - Evidence: <file/function/path and why reachable>
  - If not fixed: <consequence>
  - Review fix brief:
    - Category: <bug/security/data loss/privacy/reliability/API contract/UX/other>
    - Summary: <one-line fix target>
    - Current behavior: <what the PR does now>
    - Desired behavior: <what should happen>
    - Trigger: <smallest reachable scenario>
    - Key interfaces: <stable contracts, types, commands, schemas, routes, UI states, or config>
    - Acceptance criteria:
      - [ ] <criterion>
      - [ ] <criterion>
    - Prevention first: <smallest failing test/check>
    - Validation: <exact command/workflow>
    - Out of scope: <what not to change>
    - Risk: <adjacent behavior that could break>

## Fix if cheap
- <title> - <reason>
  - Confidence: <high/medium/low>
  - Verification: <how the issue was proven real on the PR head>
  - False-positive check: <what was checked to rule out a false positive>
  - Evidence: <file/function/path and why reachable>
  - Prevention: <smallest practical test/check>

## Defer
- <title> - <reason>
  - Confidence: <high/medium/low>
  - Verification: <how the issue was proven real on the PR head>
  - False-positive check: <what was checked to rule out a false positive>
  - Evidence: <file/function/path and why reachable>
  - Follow-up tracking: <Linear link/action, Binder docs/Deferred bugs.md checklist item, or blocker>

## Ignore
- <title> - <reason, including false-positive/stale/unverified basis>

## Review threads resolved
- <thread/comment title> - <already resolved or resolved during this run; include reply/resolve/refetch evidence when resolved during this run>

## Should resolve but not resolved
- <thread/comment title> - <why fixed and why not resolved remotely; include the exact blocker and the next command/action needed>

## Prevention tests
- <title> - <test/check type, location, and failure it catches>

## Approved execution
- Fix now implemented: <count or not approved>
- Fix if cheap implemented: <count or not approved>
- Prevention added: <count or not approved>
- Binder deferred bugs recorded: <count or not applicable>
- Validation: <commands/workflows run, or not approved>

## Summary
- Fix now: <count>
- Fix if cheap: <count>
- Defer: <count>
- Ignore: <count>
- Prevention tests recommended: <count>
- Linear follow-ups created or linked: <count>
- Binder deferred bugs recorded: <count>
- Recommended next steps: <top 1-3 actions>
```

If a bucket is empty, include the heading and write `- None.`

If inventory is incomplete, say so in `Inventory` and `Summary`; do not present bucket counts as a complete PR triage.

If a claim cannot be verified from the available current-code evidence, do not upgrade it into a real finding just because the reviewer sounded confident. Keep it in `Ignore` and say what proof was missing.

## Concrete Tool Patterns

Use structured GitHub tools first when available. If not, these CLI patterns are acceptable fallbacks:

```bash
gh pr view <number> --json number,title,headRefName,reviewThreads,comments,reviews,statusCheckRollup
gh api graphql -f query='<GraphQL query for pullRequest.reviewThreads>'
gh api graphql -f query='<GraphQL mutation resolveReviewThread(threadId: "...")>'
gh issue list --search '<repo/pr keywords>' --state open --json number,title,url
```

Do not call a review thread resolved unless GitHub already had it resolved or the resolve operation succeeded.
After approved fixes, do not call the GitHub portion complete until fixed inline threads have been replied to when possible, resolved remotely, refetched, and reported, or explicitly listed as blocked.

## Worked Example

See [EXAMPLE.md](references/EXAMPLE.md) for a claim -> code verification -> bucket -> prevention recommendation example.

## Operating Rules

- Be concise and decisive.
- Reject weak comments rather than inflating priority.
- Try to disprove the review comment before you try to satisfy it.
- Do not preserve a reviewer's severity when current-code evidence disagrees.
- Unverified claims are not actionable findings.
- Pull current PR comments first when possible.
- Prove inventory completeness before trusting final counts.
- Actually reply to, resolve, refetch, and report high-confidence fixed inline review threads when tooling is available.
- Create or link Linear issues only for real deferred non-Binder work.
- For Binder, record real deferred bugs in `docs/Deferred bugs.md` as checklist items after the user approves fixes.
- Execute approved PR review feedback directly from this skill; do not route to another skill unless the user explicitly asks for that workflow.
- Do not write patches unless explicitly asked.
