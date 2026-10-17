---
name: greploop
description: >
  Runs the Greptile CLI on the current local branch. Triages every finding against the actual
  code, fixes what survives, and reviews again, until a fresh review surfaces nothing real or a
  hard cap of three reviews is reached. Use when the user says "greploop", asks to iterate on
  Greptile feedback until the review is clean, wants a branch polished before pushing or opening
  a PR, or wants local review findings fixed and re-reviewed automatically.
license: MIT
metadata:
  author: greptileai
  minCliCompat: 3.3.0
allowed-tools:
  - 'Bash(greptile *)'
  - 'Bash(git *)'
---

# Greploop

Run a Greptile review on the local branch, fix what survives triage, review again.

**Stop when a fresh review yields zero findings that survive triage. Hard cap: 3 reviews by
default; the user can name a different cap up front (e.g. "greploop, up to 10 reviews"), and
the loop extends past the cap only when the user confirms (Step 4).** The confidence score is
informational only: record it (write `n/a` when it is `null`) and report it. It is never a
reason to edit: every change in this loop is justified by a triaged finding, so a low score
with nothing to fix gets reported, not coded away. Reviews of well-written code still draw a
few advisory comments at 4/5, so "no comments at any cost" is not the goal; a review whose
findings are all rejected or deferred is a clean result. A **low score is the exception**: 3
or below with nothing surviving triage means the comments probably under-represent the
reviewer's concerns, and Step 4 says what to do.

This is the local CLI loop. No PR, nothing pushed. Command and output details are in the
`greptile-cli` skill.

Run the steps below yourself, once per iteration. Never drive this with `watch(1)`: it never
exits, nothing triages or fixes anything between ticks, so it re-bills the same review of the
same commit forever, and it is not installed on macOS. The triage and the fix between reviews
are the entire point, and only you can do them.

## Loop

Copy this checklist and check items off as you go:

```
Greploop progress:
- [ ] Step 0: Preflight
- [ ] Step 1: Start from a clean worktree
- [ ] Step 2: Review (N of cap)
- [ ] Step 3: Triage every finding
- [ ] Step 4: Check exit conditions
- [ ] Step 5: Fix and commit, then back to Step 2
- [ ] Step 6: Report
```

### Step 0: Preflight

```bash
git rev-parse --show-toplevel   # must be a git repo with a remote
command -v greptile             # must be installed
greptile whoami                 # check the OUTPUT, not the exit code
```

This skill ships with the Greptile CLI, so `greptile` missing means a broken install or `PATH`
problem: stop and report it to the user.

`greptile whoami` **exits `0` even when signed out**, printing `Not signed in. …` to stdout, so
gate on its text:

```bash
greptile whoami | grep -q '^Not signed in' && echo "needs login"
```

If it needs a login, stop and tell the user to run `greptile login` themselves. It is an
interactive browser flow; do not attempt it yourself.

### Step 1: Start from a clean worktree

`greptile review` reviews **committed** changes against the branch base, and this loop commits
once per iteration, so it needs a clean tree to begin with.

```bash
git status --porcelain     # must be empty before you start
```

If anything is listed, **stop and hand it back to the user.** Ask them to commit or stash it,
and say why: once the loop starts, any file it edits gets staged whole, so a change they had in
that file would be swept into a commit labelled as review feedback. Do not commit or stash on
their behalf, and do not proceed because the dirty files look unrelated; the loop only learns
which files it will touch after the first review.

### Step 2: Review

```bash
greptile review --json > review.json
```

Always `--json`, and capture it. A review takes on the order of a minute; do not wrap it in a
short timeout, and do not start a second one while one is running. Pass `-b <branch>` when the
user named a base; otherwise omit it and let the CLI resolve the repository default. Increment
the review counter: **this loop runs at most the capped number of reviews (3 unless the user
set or extended it).**

A zero exit with findings is the normal case; `greptile review` exits `0` whatever it finds. A
**non-zero** exit means the CLI did not deliver a result, but the review often completed
server-side anyway (a slow backend times the client out). Before giving up, try to recover it:

```bash
greptile review status --json    # exit 3 = still running: wait 30s and retry
greptile review show <runId> --json > review.json   # runId from the status output
```

If recovery fails too, report the stderr message and stop. Several failure causes never clear
by looping: detached HEAD, a diff over 3 MB, a base sharing no
history with HEAD, or every changed file held back as sensitive.

### Step 3: Triage every finding

Take each finding in `comments` in this order: `securityIssue: true`, then `P0`, `P1`, `P2`.
Ignore `category` and `verifiedEvidence`; on the `--json` path they are always `"comment"` and
`null`. Record every verdict in the ledger (format in Step 4) before editing anything.

**Screen advisory comments first.** A finding that asserts no concrete failure (style, naming, structure
preference, "consider adding X" product suggestions like rate limiting, documentation requests)
or that needs a product decision is **DEFERRED**: record it, report it, never fix it. A finding
that asks for something the user already rejected this session is **REJECTED**, with the
rejection as the evidence.

For findings that do assert a concrete failure, attempt to reject them with two checks. A
finding is **REJECTED** the moment either check produces citable evidence against it; otherwise
it is marked **FIX**:

**1. Fact check: is the claim true of the code as written?** Read the file at `path` from
before `startLine` to past `endLine`, enough to see the whole function or block. `hunk.before`
is a snippet without surrounding control flow; the file is the ground truth. When `side` is
`"old"` the finding anchors to the pre-change file: read that version, not the working tree.
Rejected when the code already does what the finding says is missing, the described construct
is not there, or the finding misreads control flow.

**2. Reachability check: does the described failure actually occur?** Construct the concrete
failure: which input or state, entering through which caller, produces the wrong behavior. Read
the callers when the answer depends on them. Rejected when every path to the flagged code
already excludes the failing input, or the described behavior is what this change intends, as
stated by the user, the commit messages, or the tests.

**The evidence standard.** A rejection must cite its evidence (the lines read, the call path
traced) in one line. "Looks fine" and "probably intentional" are not rejections. For a
concrete-failure finding, uncertainty is not rejection: if both checks produce no evidence, it
gets fixed. Deferring advisory comments, not the evidence rule, is what keeps style
preferences from being treated as bugs.

### Step 4: Check exit conditions

Maintain this ledger in your response every iteration, carrying prior iterations forward so
repeat appearances stay visible:

```
Review 2 of 3: confidence 4/5 (informational), 3 findings
  src/auth.ts:45  P1 security  FIX (seen 1x)
  src/db.ts:112   P2           REJECTED (fact): index exists in migration 0043
  src/api.ts:9    P2           DEFERRED: naming preference, no failure asserted
```

Two findings are the same finding when they have the same `path`, overlapping spans after
adjusting for your own edits, and describe the same issue. When in doubt, treat them as the
same; that moves the loop toward stopping instead of churning.

**Stop the loop when any of these is true:**

- `comments` is empty. Clean review; go to Step 6.
- Zero findings are marked FIX (everything rejected or deferred) **and** `confidence` is `4`,
  `5`, or `n/a`. That is the termination; go to Step 6. Do not run another review to confirm
  it: re-reviewing an unchanged commit returns no new information, and some backends suppress
  repeat comments on a previously reviewed commit, so the empty-looking confirmation would be
  an effect of that suppression, not a verdict.
- Zero findings are marked FIX but `confidence` is `3` or lower. The score and the comments
  disagree, and the comment list can under-report the reviewer's concerns: read `summary` and
  `confidenceReasoning`. If they describe a concrete failure the comments never raised, treat
  it as a finding and triage it through Step 3. If they do not, go to Step 6 and report the
  discrepancy plainly instead of calling the branch clean.
- This was the last review the cap allows. Triage its findings. If any are marked FIX and no
  stop signal fired, ask the user whether to run more reviews, and continue to Step 5 only
  when they confirm; never extend the cap on your own. If they decline, or nothing is marked
  FIX, report and fix nothing: a fix no review will ever re-check cannot be credited as a fix.
- A stop signal fired (below). Stop and report it as a deliberate early stop: not a failure,
  not a success.

**Stop signals.** Each of these means the loop has stopped making progress, and more
iterations would make the branch worse, not better:

- A finding you fixed, gone from one review, is back in a later one. The fix and the reviewer
  disagree; a third opinion will not settle it.
- A finding marked FIX sits on lines one of this loop's own fixes added. Reconsider that fix
  first: undo its hunks by hand rather than stacking a patch on the patch. If the same finding
  then survives a second fix attempt, stop.
- The number of findings marked FIX did not decrease from the previous review.

`confidence` appears nowhere in this list, on purpose. Record it each iteration; do not let it
start, stop, or extend the loop.

### Step 5: Fix and commit

Fix only findings marked FIX, in the same severity order. Make the smallest fix that resolves
the failure you confirmed in the reachability check; you already traced the failing path, so
fix its root cause rather than patching the symptom line. If the fix changes a signature or a
shared helper, read the callers before editing; a fix that is correct at the flagged line and
wrong at a call site is how the next review inherits a worse finding.

Do not apply `suggestion` fields blindly. Each is a proposal: read it, confirm it fits the
surrounding code, then apply. Never disable a rule, add a suppression comment, or weaken a test
to make a finding go away; if a finding can only be cleared that way, mark it DEFERRED and
report it. Do not touch rejected or deferred findings "while you're in there", and do not make
improvements no finding asked for: every line you add is new code for the next review to
comment on.

Stage **only the files you edited**, by explicit path:

```bash
git add -- src/auth.ts src/db.ts        # the paths you actually changed
git commit -m "address greptile review feedback"
```

Never `git add -A` or `git add .`. This loop runs unattended for minutes, and a catch-all stage
sweeps in whatever else appeared in the worktree and buries it in a commit labelled as review
feedback. Staging by path is only safe if those files still contain exactly what you wrote, so
confirm each path before staging:

```bash
git diff -- src/auth.ts     # every hunk here should be one you made
```

If a file changed underneath you, **stop the loop** and tell the user which file and why; list
this iteration's fixes as applied but unverified in the report. If `git status --porcelain`
shows changes in files you did **not** edit, leave them alone and note them in the report.

Return to **Step 2**. Do not push; this loop stays local unless the user asks otherwise.

### Step 6: Report

```
Greploop complete after 2 reviews.
  Confidence:   4/5 (informational, not a stop condition)
  Fixed:        3 findings, each confirmed gone by a later review
  Rejected:     1    Deferred: 1

Deferred (reported, not fixed):
  - src/api.ts:9 (P2) "Consider renaming this handler": no failure asserted
Rejected:
  - src/db.ts:112 (P2) "Missing index on user_id" (fact: index exists in migration 0043)
```

When the loop stopped at the review cap or on a stop signal, say so plainly and lead with what remains:

```
Greploop stopped: fixed finding returned at review 3.
  Confidence:   4/5
  Fixed:        5 (one now back: src/retry.ts:88)
  Rejected:     2    Deferred: 1

Recommend: review the src/retry.ts fix by hand; the reviewer and the fix disagree.
```

Report the state you actually reached: every rejection ships with its one-line evidence, every
fix is confirmed gone by a later review, listed as remaining, or listed as applied but
unverified. A loop that hit the review cap with findings still marked FIX is unfinished work; never describe it
as complete, and never round the confidence up.
