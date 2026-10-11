---
name: verify-delegated-edits
description: "Use when accepting a subagent's or worker's change: it reports all tests pass with no raw output, calls a new test or lint failure pre-existing, or one of its negative searches (no such file anywhere) proves wrong. Also when delegated work leaves stray or deleted files."
---

A worker reporting "all tests pass, verification PASS" is a claim, not evidence.
This is the checklist that turns it into evidence. Use it after any delegated
multi-file change, and any time a worker's summary is structured JSON with no
raw command output in it.

## 1. Read every changed hunk yourself

Non-negotiable and comes first. Read the actual lines, not the worker's
description of them. Most fabricated verification dies here.

## 2. Inventory the whole tree, not just the files you asked for

Reading the intended hunks proves those edits are right. It does **not** prove
nothing else moved. Get:

```
git status --porcelain=v1 --untracked-files=all
git diff --stat
```

Check three things:

- The touched set matches the intended set exactly. Anything extra is
  `UNEXPECTED` and needs its own diff.
- **Any `D ` or ` D` status.** Workers cleaning up temp files with `rm -f` have
  deleted untracked, never-committed repo files as collateral. An untracked
  file has no git copy — once gone it is gone.
- Scratch files the worker created (`*.log`, `*_result.txt`, stub scripts) are
  cleaned up, not left untracked in the root.

**Reconcile line counts.** If the tool reports "13 lines" but the quoted block
has 11 and the worker says "0 dropped", find the missing 2 before moving on.
Usually a CLI wrapper banner; sometimes two files it chose not to show.

## 3. Attribute every failure — never accept "pre-existing" on assertion

For each failing test or lint finding, demand the same proof:

```
git stash && <run the check> && git stash pop     # baseline
<run the check>                                   # working tree
```

Identical failure message on both sides = pre-existing. Anything else is yours.

Watch specifically for failures a worker will reflexively label unrelated but
which your edit plausibly caused:

- **Lint/format tests** — an added import can trip import-sort (`I001`); a new
  long line can trip max-len. Any file you touched is a live suspect.
- **Meta-tests that scan source text** — "every subprocess declares its codec",
  "no bare except", "no file over N lines". These fail on edits that look
  semantically innocent.
- **Baseline-constant tests** — `assert found <= BASELINE` with a hardcoded
  number. Confirm which number the test asserts against and whether the
  baseline was already stale, rather than reading the raw count as the verdict.

When a failure is yours: fix the cause. Do not add `noqa`, do not bump the
baseline constant, do not edit the test — unless the file already uses that
exact pattern for that exact rule.

## 4. Distrust the rest of a worker's negatives once one is wrong

A worker that searched `D:\` and missed a file in `D:\NightSmith\` reported "no
such file anywhere". If one negative search is provably wrong, **re-run all of
them** on a fresh session — a false negative on a search is indistinguishable
from a true one in the summary.

Insist on the verbatim refusal for anything that could not be run (permissions,
elevation, missing tool) rather than a claim of absence.

## 5. When the worker's response channel eats the raw output

Some workers return only a structured summary and drop the stdout you asked
for. Do not settle for the summary and do not re-ask twice.

- Read the transcript directly: `read history://<session>:-120` returns the
  literal text the worker saw and quoted.
- Or read the artifact tree / the file the command wrote.

## 6. Run the thing, don't just build it

Green typecheck catches a syntax slip, never a wrong flag or a dead branch. For
a launcher, CLI, or anything shelling out: execute it, including the failure
branch. A branch that prints advice the user cannot follow (`pass one by hand:
--foo X`) while `exit`-ing before that argument is ever read only shows up when
run.

## Reporting

State losses in the body of the summary, not in a footnote — an accidentally
deleted file, a reconstruction that is not byte-identical, a recovery avenue
left untried (e.g. shadow copies needing elevation). Distinguish clearly:
*recovered* (byte-identical) vs *reconstructed* (new content built from
surviving sources, gaps left empty rather than fabricated).
