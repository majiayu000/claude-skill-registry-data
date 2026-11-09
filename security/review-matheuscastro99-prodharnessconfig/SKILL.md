---
name: review
description: Block C of the harness workflow. Reviews a finished change at its handed-off commit with the red-team, triages findings and comments, and brings one report to the owner (gate G2). Invoke as /review <issue> in a fresh Opus session; on the Small tier the main session runs it when the forked build returns.
argument-hint: <issue-number>
---

# Review: Block C (gate G2)

Issue: `$ARGUMENTS`. This session runs on Opus: on Standard a fresh one (`claude --model opus`); on Small the main session that ran plan mode, never the forked build (D22).

## 1. Check the input (refuse on failure)

- **First, if PR monitoring (Auto-fix) is on for the PR, turn it off,** before anything else. A push after the handoff would move the head this review checks.
- **Both tiers:**
  - Read `.harness/work/<n>/handoff.md`. On another machine, read the handoff comment on the issue instead, and save it to that path.
  - Run `node .claude/scripts/handoff-check.cjs .harness/work/<n>/handoff.md --verify-head`.
  - Exit 1 (invalid), 3 (BLOCKED, or the PR head moved) or 2 (error): stop and report why. Don't review a moving target.

If the handoff passes but is too thin to triage against, read the PR's commit log with `git log --stat` yourself, not the diff: the red-team reads the diff. Note in the G2 report what the handoff lacked.

## 2. Red-team

Brief the `red-team` in the background with:

- **Goal:** the issue, the plan's acceptance criteria, and its invariants.
- **Target:** the PR **and the SHA** from the handoff.
- **Constraints:** the plan's "Out of scope" and the docs it expected to change.
- **Error-handling lens (T4, D24),** when the change touches error handling, validation or fallbacks: hunt silent failures too. Empty or broad catches, errors logged and then ignored, a default or success returned on failure, and errors that reach the user without saying what went wrong.

**Security pass (T5),** when the issue touches auth, sessions, secrets, permissions or access to user data: check that `git rev-parse HEAD` is the handoff's SHA, then run the built-in `security-review` skill. Its findings go into the G2 table.

Don't read the full diff yourself; it goes to the red-team.

Meanwhile, collect review comments on the PR: `gh pr view <pr> --comments`, and inline comments via `gh api repos/{owner}/{repo}/pulls/<pr>/comments`.

## 3. Triage

For each finding and each comment, answer three questions:

- Can it be reached in this project today?
- Does it genuinely affect the people who use it?
- Is the cost of the fix justified?

Recommend **fix** or **decline**, with the reason, and name what would make a declined finding real. Verify a claim before relying on it.

**Source** names what found each one: `red-team`, `red-team T4`, `security-review T5`, `PR comment` or `reviewOnReady`. The trial register (research/10, D24) counts by it.

## 4. G2 report (one message; the owner decides everything in one reply)

```
## G2: #<n> · PR <url> · reviewed SHA <sha> · CI on <sha>: <status>
### Findings and comments
| # | Source | Finding | Priority | Blocking | Recommendation |
### Acceptance criteria
- [x]/[ ] … · Not verifiable here: …
### Docs
<docs diff summary; acks>
### Optional owner steps
<e.g. a local MAUI run; CI's build is the required check; the UI screenshots in .harness/work/<n>/ui/ (T6)>
### Decisions for you
1. <one per open decision: each finding to fix or decline, each follow-up issue, each item only the owner can change>
```

**Number every open decision under "Decisions for you" (D25)**, so one reply can answer them all ("1, 2 fix; 3 decline; 4 open the issue"). Ask nothing anywhere else in the report.

**A blocking finding** (security, data integrity, correctness) **can't go to a follow-up issue** unless the owner explicitly accepts it. Record that acceptance in the report.

## 5. After the owner decides

1. **Apply the approved fixes.** One commit per fix group: `fix: <summary> (#<n>)`. The hooks and gates apply as in Block B.
2. **Push.** Wait for CI on the new head. Record the new SHA.
3. **Narrow re-review:** brief the `red-team` with the previous findings, the new SHA and the changed lines only. **Only one re-review.** What remains after it goes to a follow-up issue, unless the owner asks for another round. A blocking finding still needs the owner's explicit acceptance.
4. **Reply to each review comment** with its fix or the reason it was declined, as the owner decided at G2.
5. **Ready to merge.**
   - Mark the PR ready: `gh pr ready <pr>`.
   - **If `.claude/harness.json` has `reviewOnReady`**, a CI reviewer runs now, after G2:
     - Find its run: `gh run list --workflow <workflow> --branch <branch> -L 1`.
     - Wait for it, up to `timeoutMin` (default 15): `gh run watch <id>`.
     - Read the comments it left on the PR since the run started, and triage them as in step 3.
     - A blocking or fix-worthy comment goes back to the owner as a short **G2 addendum**, and nothing is marked ready to merge until the owner decides. The rest are noted in the ready-to-merge note.
     - If the run times out or fails, say so in the note. It isn't a required check.
   - Post the note: "ready to merge at `<sha>`. Reviewed SHA = PR head = the SHA CI passed on."
   - If the branch is behind the base, say so. Updating it creates a new head, which needs CI and a re-review again.
   - **The owner merges.** Then the owner runs `/close <n>`.

## Never

- Never review a SHA other than the handed-off head.
- Never merge, approve your own PR, or disable a check.
- Never post an unfixed security finding publicly. Report it to the owner directly.
