---
name: bug-fix
description: Use when a bug, regression, or unexpected behaviour is reported and the user wants it fixed end to end — "why is X broken", "this stopped working after Y", "fix this crash". Also use when a symptom is known but its cause is not. Not for building new behaviour, and not for a change whose cause is already proven.
argument-hint: "[the bug report]"
---

# Bug Fix

## Overview

Carries a bug from report to validated fix by chaining specialists:
**investigate → decide → plan → implement**. You are the conductor. Investigation
and implementation each go to a specialist wherever one is available, and this
skill owns the seams and the evidence bar between them.

**Core principle:** no fix is planned until the root cause is proven with
`file:line` evidence, and no plan is written until the open questions are
answered. **Do not guess.** A plausible fix for an unproven cause is worse than
no fix: it consumes the report, closes the ticket, and leaves the bug live.

## When NOT to use

- **Building new behaviour** — that is `superb:craft` then `superb:pipeline`.
- **A change whose cause is already proven** — skip to the fix; the
  investigation exists to establish a cause, not to ceremonially confirm one.
- **A whole feature's worth of bugs** — that is a phase of `superb:pipeline`,
  which has the fix loop, the findings ledger and the convergence rule.
- **You only want to know what is wrong** — that is `superb:bug-investigate`,
  which runs this skill's Step 1 and stops. Reach for it when the decision to
  fix has not been made, or when naming the cause is the whole deliverable.

## Step 0 — Assemble the report

The investigator needs five things. The invocation argument usually supplies one
or two:

| Field | Example |
| ----- | ------- |
| Symptom | "uploads over ~5MB fail silently" |
| Reproduction | the steps, or `unknown` |
| Error text | stack trace, log line, or `none surfaced` |
| Affected surface | endpoint, screen, command, job |
| Last known good | a date, a release, a commit, or `never worked` |

**Ask the user for whatever is missing before dispatching** — one batched
question, not five. `unknown` is a fine answer and belongs in the brief; a
silently empty field is not, because the investigator will fill it with a guess.
If the symptom itself is unclear, stop: there is nothing to investigate yet.

## Step 1 — Investigate

**The investigation must not modify anything.** It establishes a cause and
reports it; deciding what to change is Step 2's job and Step 3's. A step that
both diagnoses and fixes destroys the evidence the plan is built on.

Take the first branch that applies:

| Condition | What to do |
| --------- | ---------- |
| A subagent mechanism is available **and** `superb:bug-investigator` appears in your available agent types | Dispatch **`superb:bug-investigator`** with the Step 0 report. |
| A subagent mechanism, but that agent is not in your list | Dispatch a general subagent. Its brief is the text **between the `SHARED BRIEF` markers** in `references/investigator.md` — those markers exist to keep this skill's packaging notes out of the brief. Append the Step 0 report. |
| No subagent mechanism at all | Follow that same bracketed brief **yourself**, inline, including its "modify no files" rule, and produce its report format before continuing. |

Check your actual agent list rather than assuming. On harnesses with no
bundled-agent support the second branch is the normal path, not a failure.

**Always name the agent `superb:bug-investigator`, with the prefix.** A bare
`bug-investigator` resolves to whatever personal agent the user happens to have,
possibly written for a different stack, and the result will look like it worked.

Do **not** substitute `superpowers:systematic-debugging` here. Its four phases
run through hypothesis-testing and implementation, so it would complete the fix
and return no report for Step 2 to read.

**If the investigation cannot pin the root cause**, relay what it ruled out and
ask the user for more repro detail. Do not proceed to planning on a hypothesis —
that is the one failure this skill exists to prevent.

## Step 2 — Decide, and write the cause down

**Persist the investigation report to a file, and commit it** before planning.
Put it where the repo already keeps working notes; if it has no such place,
`docs/bug-fix/` is a reasonable default, and creating one directory is not a
structural change worth asking about.

**Committing it is not optional bookkeeping.** Both executors work in a fresh
git worktree, and an untracked file does not follow them there — an uncommitted
report leaves Step 3's `Spec:` path dangling at the moment the implementers need
it. Commit it on its own, before the fix exists.

Then decide whether anything is genuinely the user's call:

- More than one viable fix, with different trade-offs
- The intended behaviour is ambiguous — code is only wrong once you know what
  right was
- The fix is broader than the symptom (a targeted patch versus a refactor)
- It touches regulated or personal data, a data migration, an external contract,
  a public API, or anything with a blast radius past this repo

If any apply, ask — with `AskUserQuestion` where the harness has it, as a plain
numbered question where it does not — and **lead with your recommendation.**
Otherwise go straight to planning. Do not manufacture questions.

## Step 3 — Plan

**REQUIRED SUB-SKILL:** use `superpowers:writing-plans`, giving it the Step 2
file as its `Spec:` path plus the agreed fix direction.

The plan must include a **regression test that fails before the fix and passes
after**, and the test must be **its own task, ordered before the fix task** —
that ordering is what makes the failure observable, because once the fix is
committed there is nothing left to stash. State the expected failure explicitly:
for a bug in existing code it is a wrong value or a raised error, **not**
"function not defined", which is what the plan template's own example assumes.

The plan's **last task is the verification below.** Put it in the plan rather
than saving it for afterwards — both executors finish by invoking
`finishing-a-development-branch`, which merges the branch and removes the
worktree, so anything you intended to check "after the executor returns" would
be checked on work that is already merged and gone.

If the bug genuinely cannot be covered by a test, the plan must say so and why.

**Commit conventions come from the repository, not from here.** Read its
`CLAUDE.md`, `AGENTS.md`, or contributing guide and follow its subject-line
rules and ticket prefixes. Two rules hold regardless, because they are the
user's rather than the project's:

- **Never add a `Co-Authored-By` or any attribution trailer.**
- **Never put a session link, session id, or assistant-generated URL anywhere**
  in a commit message, code, or documentation.

## Step 4 — Implement

`writing-plans` stamps every plan with an executor header naming
`subagent-driven-development` or `executing-plans`, and asks the user which they
want. **Follow whatever the plan ends up carrying** — it is the instruction the
plan was written against, and overriding it means the implementers read one
thing and you intended another. If the choice is still open when you get there,
prefer `superpowers:subagent-driven-development` where a subagent mechanism
exists, so the fix is reviewed by something that did not write it.

The verification is the plan's last task, so the executor runs it while the
branch still exists:

1. **The test task went red before the fix task ran.** That is the evidence, and
   it is captured when the test task executes — not reconstructed afterwards by
   stashing, which cannot work once the fix is committed. If the test passed on
   its own task, it is not testing the bug: go back to Step 3.
2. It passes once the fix task lands.
3. The original reproduction from Step 0 no longer reproduces. **Skip this only
   if Step 0 recorded the reproduction as `unknown`**, and say so in the result
   rather than silently omitting it.
4. The repo's own gates — full suite, linters, build — are green.
5. The commits carry no attribution trailer and no session link.

**The fix is not done until step 1 has actually been observed.** A green suite
that never covered the bug is the same false signal as a green gate over
unchecked code.

## Red flags — STOP

- About to edit code before an investigation has reported → stop, investigate.
- About to plan on a "probably this" cause with no `file:line` evidence → stop,
  finish the investigation.
- Writing `bug-investigator` without the `superb:` prefix → you are about to
  dispatch someone else's agent and trust the result.
- Reaching for `systematic-debugging` as the investigator → it implements, and
  you will have no report.
- Handing `writing-plans` a spec you only said out loud → the implementers read
  the file, not your context.
- About to call it done having only re-run the repro → the failing-first test is
  the deliverable that outlives you, and you have not watched it fail.
- Planning to verify "after the executor returns" → it returns from a merged
  branch with the worktree deleted. Verification is the plan's last task.
- About to hand over a `Spec:` path you have not committed → it will not exist
  inside the implementer's worktree.
- About to write a ticket prefix you did not read out of the repo's own rules →
  you are carrying another project's conventions into this one.
