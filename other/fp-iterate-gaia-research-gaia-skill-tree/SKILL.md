---
name: fp-iterate
description: >-
  Phase 4 of the feature-pipeline suite. Use this after /fp-review has posted
  a sandbox review comment — it reads the outstanding checkbox items, applies
  fixes, then watches CI until green (or exits cleanly so you can retry).
  Trigger phrases: "address review items", "fix review feedback", "resolve
  review checklist", "watch CI", "poll CI", "check if CI is green", "iterate on
  PR", "fp-iterate", "Phase 4", "after review comment", "fix the review issues
  and watch CI". Always bounded — max 10 poll rounds, never loops forever.
  Exits with a clear status: green (hands off to /fp-drift), still-pending
  (re-invoke), or failed (diagnose before touching anything).
version: 3.0.0
---

# fp-iterate — Phase 4: Address Review & Watch CI

Fix the outstanding `[ ]` items from the Phase 3 review comment, push the
commits, then poll CI until it resolves. This skill is intentionally bounded:
it always exits, which keeps you in control of what happens next.

## Why bounded?

Unbounded CI loops can burn tokens and obscure stalled checks. Instead,
ci-poll.sh runs a fixed number of rounds and hands control back — you decide
whether to retry, escalate, or investigate.

## Setup

Load the state written by earlier pipeline phases:

```bash
STATE=".agents/skills/feature-pipeline/scripts/state.sh"
branch=$($STATE get branch)
pr=$($STATE get prNumber)
reviewUrl=$($STATE get reviewCommentUrl)
ciRound=$($STATE get ciRound)
```

Switch to the feature branch so your fixes land in the right place:

```bash
git checkout "$branch"
```

## Step 1 — Read and address review items

Fetch the review comment body:

```bash
gh api "$reviewUrl" --jq '.body'
```

For each `- [ ] <description>` item under "Issues found":

1. Understand the issue before touching code — a misread fix creates a second review cycle.
2. Apply the fix.
3. Commit with context so future reviewers understand the change:
   `fix(<scope>): <description> (per review)`
4. Push.
5. Print: `  ✓ Fixed: <description>`

If a review item is genuinely ambiguous or requires architectural input, do not
guess. Leave it unchecked, note the ambiguity, and surface it in the stop hook
message so the human can decide.

## Step 2 — Bounded CI poll

```bash
.agents/skills/fp-iterate/scripts/ci-poll.sh "$pr" --max 10 --interval 30
poll_exit=$?
```

Increment the round counter so escalation logic knows how many attempts have run:

```bash
$STATE set ciRound $(( ciRound + 1 ))
```

### Exit 0 — CI green

```bash
$STATE set ciStatus "green"
$STATE set phase 6
```

Remove `in-progress` label, add `ready-for-review`, and undraft the PR via
`mcp__github__update_pull_request`. Then print the M4 stop hook and end your turn:

```
╔══ STOP HOOK M4 ══════════════════════════════════════════════════════════════╗
║  CI green ✅  PR #<N> ready for review                                       ║
║  Run /fp-drift for the final drift check and summary.                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Exit 1 — still pending after 10 rounds

```bash
$STATE set ciStatus "pending"
```

Print and end your turn. Do not improvise another polling loop — re-invoking is
the designed retry path:

```
⏱ CI still pending after round <ciRound>. Re-run /fp-iterate to check again.
```

### Exit 2 — CI failed

```bash
$STATE set ciStatus "failed"
```

Fetch the failure log to give the human actionable context:

```bash
gh run view --log-failed 2>/dev/null | head -60
```

Print the diagnosis (root cause, file, line when identifiable) and end your
turn. Do not push a blind fix — the failure may indicate a problem the human
needs to decide on. Wait for explicit confirmation before acting.

If the same check has failed across 3 or more consecutive runs
(`ciRound >= 3` and `ciStatus == "failed"`), include the full log excerpt in
your message before suggesting any fix. Repeated silent attempts waste context
and can mask a systemic issue.

## Constraints

- `ci-poll.sh` is the only CI mechanism. A manual sleep loop bypasses the exit
  code contract and breaks the retry/escalation logic downstream.
- No force-pushes.
- Re-invoking `/fp-iterate` is the intended path for exit code 1 — do not
  extend the poll window by hacking the `--max` flag to compensate.
