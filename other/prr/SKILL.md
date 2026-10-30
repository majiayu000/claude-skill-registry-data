---
name: prr
description: PR review mechanics. Weigh unresolved review findings by severity, verify each against source, reply before you resolve, and check the merge gate on one head SHA.
---

# prr: review threads and the merge gate

`auto` calls this skill. Use it alone when only the review loop is needed.

## Blocking threshold

Each repository's gate tool (`ws-pr-gate` or `tools.pr_merge_gate`) computes the unresolved review threshold from literal `severity:` tags (`high`, `medium`/`middle`, `low`; unlabelled counts as `middle`):
- **Weighted score** (`ws-pr-gate` and `tools.pr_merge_gate`): `high = 1.0`, `middle = 0.5`, `low = 0.25`. A total of `1.0` or more blocks the merge (`AGENTS.md`). Two middles or four lows block like one high.

Read the literal `severity:` tag; do not infer severity from tone. Let the repository's gate tool compute the verdict rather than estimating manually. Reviewer platform errors, timeouts, or unparseable reviews warn and do not block.

## Thread rules

1. **Read the source.** The GitHub diff can redact text: `Bearer {token}` appears as `Bearer ******`. Check the local file before you judge a report.
2. **Reply, then resolve.** The reply cites evidence: a commit SHA, a test command, or a line link. "Fixed" alone is not a reply.
3. **Resolve only what you verified** as fixed or obsolete. Never resolve an actionable, ambiguous, or unverified thread.
4. **Turn a false report into a test.** Add a falsifiable invariant test that guards the concern. Do not only dismiss it.

## Merge gate

- Checks, review, and merge refer to the same head SHA. A result from an older head does not count.
- Every check marked `blocks_merge: true` ends in success. Pending, skipped, cancelled, and unreadable all count as unmet.
- Let the gate tool compute the decision. Do not read a check table by eye.
- Run `ws-pr-gate` (see `AGENTS.md`). Use the exit code only. Do not grep the output text.
