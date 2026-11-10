---
name: review
description: Run the two blind pre-merge reviews from delivery rule 14 on a PR — a spec review blind to the rules and a code review blind to the issue, each by a fresh subagent reading only the inputs directory prepared for it — then have a third fresh subagent verify every blocking finding and sort the nits, and hand back a fixed report block. Never edits code. Use when the deliver orchestrator reaches review, or when someone says "review PR N" or "/review N".
---

# Review a change before it is marked ready

Rule 14 in `docs/internal/agent-rules/delivery.md` governs this skill: two
reviews, each blind to the other and to the implementer; every blocking
finding verified and either confirmed or rejected with a reason; nits
collected, never blocking; two rounds at most. Nobody in this skill edits
code. The reviewers find, the verifier confirms or rejects, the implementer
fixes.

**Why the blindness is load-bearing.** Every stage in this factory runs on the
same model (ADR 0004). A reviewer cannot catch what the implementer missed by
being a different, stronger model; it can only catch it by not sharing the
implementer's beliefs. So each reviewer sees exactly the files prepared for
it — never the implementer's session, the PR body (beyond its `Assumption:`
lines), commit messages, comments, or your opinion of the diff. Pass paths,
not summaries. Do not tell a reviewer what the change is for, what you
suspect, or what the other reviewer found. Their permissions back this up:
the spec reviewer cannot read outside its directory, and the code reviewer
cannot read the spec directory, run `gh`, or see commit messages.

**Flat by design.** You run this skill in your own session and start the
subagents with the `task` tool. Subagents never start subagents (OpenCode's
default nesting depth of 1 is kept on purpose), so every review is exactly one
level deep and nothing reaches a reviewer except what you hand it.

**Lean proving (ADR 0009).** CI runs the full `pnpm check` on every push; a
reviewer never does. The code reviewer proves a claim with the affected test
file only and makes at most three break-and-rerun probes, on its riskiest
claims. The verifier reproduces the same way.

**Severity (ADR 0009).** A finding is `blocking` — it breaks behaviour, leaks
data, or breaches a rule or the spec — or a `nit`. Only confirmed blocking
findings send the change back for another round. Nits are collected in the
report's Nits line; the orchestrator posts them once, as one follow-up
comment on the PR (or a `bug:new` issue when substantive).

Arguments: a PR number, optionally `round 2` and which review to re-run
(`spec`, `code`, or `both`). If the PR is not a delivery PR (a person's PR
the maintainer asked about), post the confirmed findings as one comment at
the end (step 5) and push nothing.

## 1. Gather the inputs

```bash
.agents/scripts/review-inputs.sh <PR>
```

It prints `SPEC=`, `CODE=`, `WORKTREE=`, `ISSUE=` and `KIND=`. It builds the
two directories from the issue, its parent, the ADRs under Decisions, the
rules under Rules in play, the house defaults (`defaults.md`, always), the PR
body's `Assumption:` lines, a bug's triage report, every agent rule, the ADR
index, and the diff — and a detached worktree of the PR head with
dependencies installed. Rules come from `main`, so a PR cannot rewrite the
rules it is judged by. Do not add anything to those directories.

- `KIND=adr-only` (every changed path is under `docs/internal/adr/`): the spec
  review alone, in its ADR form. No code review, no worktree.
- `KIND=no-spec` (the PR closes no issue): the code review alone; the spec
  review is skipped.

## 2. Run both reviews, in parallel

Call the `task` tool **in one message**, so they run in parallel and neither
sees the other: subagent `spec-reviewer` and subagent `code-reviewer` — and,
when the orchestrator has a simulator check for this PR, `mobile-verifier`
in that same message (the deliver skill builds its prompt). On `round 2`, run
only the review named. Each reviewer already carries its brief; the prompt is
only its inputs:

- `spec-reviewer`:
  `Specification and diff: <SPEC>. Mode: code` (or `Mode: adr-only`).
- `code-reviewer`:
  `Rules and diff: <CODE>. Repository: <WORKTREE>, checked out at the reviewed commit.`

Nothing else goes in either prompt. A reviewer that returns anything but
findings in the required form — narration, garbled text, an empty answer, or
"No findings." missing — has failed, whatever it says; usually the model
endpoint failed, not the reviewer. Run it again with the same prompt plus
"Report in the required form only.", and if that fails, a third time with the
original prompt alone. If the third run fails too, stop the review: report
`Spec needs: none`, the Fix line
`review: the <spec|code> reviewer returned no report three times`, and the
orchestrator parks the issue with that under Blocked on. Never pass a failed
report to the verifier, and never treat it as "No findings.".

## 3. Verify the findings

A finding is a claim, not a fact. Start subagent `review-verifier` with:

```
PR: #<PR>  Round: <1|2>  Kind: <KIND>
Spec inputs: <SPEC>  Code inputs: <CODE>  Worktree: <WORKTREE>
Spec review findings:
<the spec reviewer's lines, verbatim, or "skipped">
Code review findings:
<the code reviewer's lines, verbatim, or "skipped">
```

It reproduces each blocking finding's evidence in the worktree, confirms,
rejects or downgrades it, sorts the nits, and returns the report block
below. If both reviews said "No findings.", skip the verifier and write the
block yourself with Fix, Nits, Rejected and Spec needs set to "none". If the
reviews returned nits only, skip the verifier too: copy them under Nits.

Then remove the review worktree and the ref the script fetched:
`git worktree remove --force <WORKTREE>` and
`git update-ref -d refs/review/<PR>`.

## 4. Decide what runs again

A confirmed blocking finding changes the diff, so the review that raised it
runs again on the next round (the block's Rerun). Nits never cause a rerun.
After round 2 there is no third: a blocking finding still confirmed is
reported as open, and the orchestrator parks the issue.

Rounds count within one delivery run. When the maintainer restores a parked
issue to a ready label, the next run's first review is round 1 again, on the
branch as it then is; the rounds of an earlier run do not carry over.

## Report

The verifier's block is the result. End with exactly this block, nothing
after it:

```
PR: #M  Round: 1 | 2  Kind: code | adr-only | no-spec
Spec review: n findings (b blocking) | skipped  Code review: n findings (b blocking) | skipped
Fix: <one confirmed blocking finding per line, as `path:line what is wrong`, or "none">
Nits: <one per line, `path:line what could be better`, or "none">
Rejected: <one per line, `claim — reason`, or "none">
Spec needs: <the line the spec is missing, or "none">
Rerun: spec | code | both | none
```

The orchestrator pastes the Fix lines into the implementer's task, the
Rejected lines into the PR's `## Review` section, and the Nits lines into one
follow-up comment, so all three must stand alone.

## 5. A PR that is not a delivery PR

Post the findings as one comment, confirmed blocking ones under "Confirmed:",
nits under "Nits:" and rejected ones under "Rejected:", ending with
`_Written by an agent._`. Rule 12 applies: one line per finding, no
narration.
