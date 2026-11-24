---
name: release-cycle
description: 'Run the whole Senzing Bootcamp plugin release cycle, from open issues to a published release, as one resumable run: find (the four finding skills other than /dry-run in draft mode, duplicates merged), refine, build, exercise (/dry-run, optionally with a simulated Bootcamper), settle (/review-invariants) and ship (/release, the manual test, /propagate-to-public). It stops only at the kickoff and five checkpoints, or where a skill it runs stops by its own rules, and records the run in one specs/IMPLEMENTED.md entry when it stops. Use when the maintainer wants to run the release cycle, do a full cycle, or go from issues to a release in one pass. Slash-only, because it follows three slash-only skills. Maintainer tool — not part of the bootcamper experience.'
argument-hint: "[run to resume, e.g. 2026-10-14] (omit to choose: resume an unfinished run, or start one)"
disable-model-invocation: true
---

# Release Cycle

A **maintainer** tool for developing the Senzing Bootcamp Claude Plugin (SBCP). Never invoked
during a bootcamp. It runs the development cycle listed in
[`docs/development.md`](../../../docs/development.md), from finding issues to publishing, as
one run with two build passes and five checkpoints, so the maintainer
no longer carries one skill's output into the next by hand (#573).

⛔ **(INV-300) Each skill's own file governs it, and this one restates none of their rules.**
This file says which skill runs when, with which arguments, and where the run stops. What a
skill does once it runs, and every gate inside it, is in that skill's file.

The mechanical half is [`cycle.py`](cycle.py) beside this file, whose docstring states it: the
run state, the next step, each step's exact invocation, the stage-1 merge, the checkpoint
verdicts, the filing order, and the run's ledger entry. Run it from the repository root as
`python3 .claude/skills/release-cycle/cycle.py`. It reads and changes the drafts manifest only
through [`drafts.py`](../feedback-to-issues/drafts.py), whose docstring is the one statement of
`--draft <run-dir>`, `--file <run-dir>` and the manifest (INV-368).

## The stages

| Stage | Runs | Checkpoint |
|---|---|---|
| 0 Kickoff | the costly choices, asked in one batch | one batch of answers |
| 1 Find | `/feedback-to-issues`, `/retrofit-from-public`, `/delegate-to-mcp-server` and `/production-readiness-audit`, each with `--draft <run-dir>`, against one baseline SHA; duplicates merged | **A**: approve the drafts as one list, then each skill runs with `--file <run-dir>` |
| 2 Refine | `refine-github-issue` *(user level)* in batch mode, on every open issue | **B**: the pooled questions, then the edits and labels as one list |
| 3 Build | `/unattended-issue-loop` *(user level)*, then `/implement-github-issue` *(user level)* for each leftover | only for the leftovers |
| 4 Exercise | `/dry-run all <module> --simulated <persona> --draft <exercise-dir>`, or `/dry-run 1,2 --draft <exercise-dir>` (phases 1 and 2) when the kickoff declined the simulated walk, where `<exercise-dir>` is the run directory's `exercise` subdirectory, against a fresh baseline SHA; then stages 2 and 3 again for what it filed | **C**: approve the drafts as one list |
| 5 Settle | the held after-filing steps; `/review-invariants`; then the user-level `update-blueprint` only if the BLUEPRINT.md header SHA is behind `main` | **D**: the invariant verdicts |
| 6 Ship | `/release`, the maintainer's manual test, `/propagate-to-public` | **E**: the version bump, the manual test, and the public repo's commit and push |

`cycle.py`'s `STEPS` splits these stages into the steps it records, and `cycle.py args <run-dir>
<step>` prints what each one runs.

## How each skill runs

- **Invoked as a skill:** `/dry-run`, the four finding skills other than `/dry-run`, `/release`,
  `/propagate-to-public`, `/review-invariants` and the user-level `update-blueprint`.
- **Followed from its file.** `refine-github-issue`, `unattended-issue-loop` and
  `implement-github-issue` *(user level, all three)* set `disable-model-invocation: true`, so a
  skill cannot invoke them. This skill reads and follows each one's
  `~/.claude/skills/<name>/SKILL.md` in the main session, with the arguments `cycle.py args`
  prints, as `unattended-issue-loop` already does for `implement-github-issue`. The maintainer's
  `/release-cycle` invocation is the explicit invocation each of them requires, which is why
  this skill is slash-only too, and every gate inside each of them still applies.
- **In a subagent:** the four finding skills other than `/dry-run`, and `/dry-run` itself. Each
  is given arguments that answer every question it would otherwise ask, from the kickoff
  answers, and returns when its `--draft` run ends: `/feedback-to-issues` gets the feedback file
  as its path argument. A subagent never asks the maintainer anything.
- **In the main session:** the kickoff, every checkpoint, and every skill that asks a question:
  `refine-github-issue`, the leftovers' `implement-github-issue`, `/review-invariants`,
  `/release` and `/propagate-to-public`. `/unattended-issue-loop` *(user level)* starts its own
  worker agents, as it always does.

## Starting, and resuming

1. **The argument.** A run name resumes that run. With no argument, run `cycle.py kickoff
   .claude/release-cycle/runs` and ask whether to resume the unfinished run it lists or start
   one; never start or resume costly work from silence (INV-333).
2. **The kickoff (stage 0)**, asked in one message: whether to run the simulated walk, and
   if so which persona and which start module (`kickoff` prints the last run's; recommend a
   later one); whether `unattended-issue-loop` merges or runs with `--no-merge`; the refine
   threshold, showing the standing 0.7 the maintainer chose on 2026-10-13 for them to confirm
   or change, which is the threshold "given in this session" refine requires; and, only when
   `kickoff` prints an `ASK` line because more than one feedback file exists, which one
   `/feedback-to-issues` triages. With one feedback file or none, nothing is asked about it.
   Then record the answers, and the baseline SHA, which is HEAD:
   `cycle.py init .claude/release-cycle/runs/<YYYY-MM-DD> --simulated yes|no [--persona P
   --module M] --merge yes|no --threshold P [--feedback PATH]`. `init` refuses a missing answer.
3. **Then repeat until the run finishes or stops:** `cycle.py next <run-dir>` names the first
   unfinished step and prints what it runs; run that; record it with `cycle.py mark <run-dir>
   <step> done` (or the command `next` names for it). On a resumed run, `next` says which step
   it resumes at; say so to the maintainer.

⛔ **(INV-375) A finished step is never run again, and a record that carries an issue number is never filed again.** `cycle.py mark` refuses a step already `done`, `clean` or `skipped`, and refuses
one whose earlier steps are unfinished. `drafts.py` skips a record already filed. When a
skill's `--file` was started and not finished, `cycle.py file-next` prints a tracker search for
each approved record still without a number: run it, and `drafts.py record-filed` any match
before filing again, since a stop between `gh issue create` and `record-filed` leaves an issue
with no number written back. A merge is kept in `state.json`, so `merge-drafts` never merges a
draft twice, and a pull request `unattended-issue-loop` merged has closed its issue, so the loop
never sees it again.

## Stage 1: Find, and checkpoint A

1. Run the four `SUBAGENT` lines `cycle.py next` prints, in parallel, then `cycle.py mark
   <run-dir> find-draft done`. With no drafts at all, `mark` records the step `clean` and skips
   stage 1's checkpoint, filing and build pass.
2. `cycle.py merge-drafts <run-dir>` merges the drafts that cite the same sites into one record
   that lists every source skill, and prints the numbered list, each item with the skills that
   found it, and an `OVERLAP` line for each pair whose sites overlap but differ.
3. **Checkpoint A.** Ask for one yes for the whole list shown in one message (INV-314,
   2026-10-13 note), under the conditions in `.claude/skills/feedback-to-issues/drafts.py` →
   "The batch yes". Each draft is at the path the list prints, and the `OVERLAP` pairs are
   shown side by side for the maintainer to settle. An `UPSTREAM` draft is not on the list:
   show it apart, and say this cycle never sends it.
4. `cycle.py verdicts <run-dir> --strike <numbers|none>` sets each item's status with
   `drafts.py set`. It refuses when a draft changed after the list was shown, or a draft was
   added that the list did not show: show the list again.
5. **Filing.** `cycle.py file-next <run-dir>` names the next skill and prints its `/<skill>
   --file <run-dir>`; run it in the main session, since the skill asks for its yes; then
   `cycle.py filed <run-dir> <skill>`. Repeat until `file-next` says every skill has filed.
   ⛔ **(INV-375) Hold each skill's after-filing step until stage 5.** `/feedback-to-issues` Step 9 and
   `/delegate-to-mcp-server` Step 9 write tracked files ("Stopping, and the ledger entry" says
   which), and stage 3 needs a clean tree. `drafts.py after` prints the same
   lines then as now. `file-next` prints a `HOLD` line for each such skill and records the hold,
   so file that skill's records and stop before its after-filing step.
   A merged draft rides on its record: `file-next` writes the record's issue number onto it,
   so its own skill skips it and its after-filing step names that issue.

If `main` moved since the baseline, `--file` refuses (#572). Before anything is filed,
`cycle.py redraft <run-dir> --sha <HEAD>` sets the old drafts aside and stage 1 drafts again at
the new HEAD; once something is filed, finish filing at the baseline instead.

## Stages 2 and 3: Refine and Build

- **Stage 2, checkpoint B.** Follow `refine-github-issue`'s batch mode with the arguments
  `cycle.py args <run-dir> refine` prints. Its questions and its approval are checkpoint B.
- **Stage 3.** `git status --porcelain` must be empty first: if it is not, `cycle.py mark
  <run-dir> build-loop stopped --note "<the files>"`, name the files, and stop; the run resumes
  there once the tree is clean. Then follow `unattended-issue-loop` with the arguments `cycle.py
  args` prints. If its preflight fails, report the allow rule it names, mark the step stopped,
  and stop. Then follow `implement-github-issue` for each issue its handoff leaves open; the
  run stops wherever that skill waits for the maintainer.

## Stage 4: Exercise, and checkpoint C

Run the `SUBAGENT` line `cycle.py next` prints, then `cycle.py mark <run-dir> exercise-draft
done --sha <HEAD>`; the fresh baseline's drafts go to `<exercise-dir>`, a manifest of its own.
With a simulated walk the line is `/dry-run all <module> --simulated <persona> --draft
<exercise-dir>`; when the kickoff declined the walk it is `/dry-run 1,2 --draft <exercise-dir>`,
`/dry-run`'s phases 1 and 2 with no walk.
Report the walk as `/dry-run` reports it (INV-369), including the module a stalled walk reached.
Then `merge-drafts`, checkpoint C, `verdicts` and the filing as in stage 1, each with `--stage
exercise`, and stages 2 and 3 again for the issues stage 4 filed (`exercise-refine`,
`exercise-build-loop`, `exercise-build-leftovers`). With no drafts, `mark` records the stage
clean and skips its build pass.

## Stages 5 and 6: Settle and Ship

- **The held after-filing steps.** Before checkpoint D, `cycle.py next` prints, for each skill
  whose after-filing step was held at its `--file`, `drafts.py after <drafts> --skill <skill>` and
  that skill's after-filing step: run both, then `cycle.py after-filed <run-dir> <skill>`, which
  refuses a step already run, so a resumed run never runs one twice. A stop before stage 5
  lists each held step, with its lines, in the run's ledger entry.
- **Checkpoint D.** Invoke `/review-invariants`; its verdicts are the maintainer's. Then
  `cycle.py args <run-dir> blueprint` says whether the user-level `update-blueprint` runs, from
  BLUEPRINT.md's header SHA.
- **Checkpoint E.** Invoke `/release` with no argument, so it asks for the bump. Ask the
  maintainer for the manual test, and mark its outcome. Invoke `/propagate-to-public`, which
  stops at the public working tree.

## Guardrails

- It never signs off an invariant: the verdicts are the maintainer's, at checkpoint D (INV-365).
- It never chooses the version bump: `/release` asks (INV-333).
- It never commits or pushes the public repo: `/propagate-to-public` stops at its working tree, and the maintainer commits and pushes it.
- It never sends `submit_feedback`. An upstream draft is recorded as not sent.
- It never applies `unattended-ok` outside refine's approved batch (INV-318, 2026-10-13 note).
- It never merges unless the kickoff answer says to: a "no" runs `unattended-issue-loop` with
  `--no-merge`.
- Each record it creates is created by the skill that owns it, under that skill's gate (INV-314).
- It never answers a gate on the maintainer's behalf. A skill waiting for the maintainer is
  where the run waits, and it never edits permission settings.

## Stopping, and the ledger entry

⛔ **(INV-375) This skill writes nothing under `specs/` before stage 5 (the held after-filing steps and
checkpoint D), and its own entry only at a stop.** This is the one statement of where a run
writes; every other site cites it (INV-300).

- **The kickoff and stages 1, 2 and 4** write only the gitignored run directory, which holds every outcome and
  draft, and `/dry-run`'s disposable scratch project, the one write outside it that INV-368
  allows. A simulated walk's sandbox is that scratch project, removed when the walk ends, and
  its reports go to the run directory.
- **Stage 3**, and its second pass after stage 4, starts on a clean tree, for
  `unattended-issue-loop`'s preflight. Each issue's
  commits, its own ledger entry among them, are on its issue branch, written by the skill
  that builds it under that skill's file.
- **Stage 5** runs the held after-filing steps (`/feedback-to-issues` Step 9 archives under
  `feedback/`; `/delegate-to-mcp-server` Step 9 appends to `specs/mcp-coverage.jsonl`), then
  checkpoint D's `/review-invariants`, which edits `specs/INVARIANTS.md` and the ledger, and
  `update-blueprint` if it runs. Stage 6's skills write what their
  own files say.
- **At a stop**, this skill writes its one entry, as below.

When the run stops (the maintainer ends it, or a step is marked stopped) or finishes, write its
one entry: `cycle.py ledger <run-dir> --write
specs/IMPLEMENTED.md`. It records each step's outcome and every unresolved draft, marked **not
filed** (INV-317's 2026-10-13 note), replaces the run's entry if one is there, and is left
uncommitted for the maintainer (INV-310). On a resumed run, `next` first prints `ledger --withdraw`:
run it, since the entry is regenerated from `state.json` at the next stop. It refuses an entry
that was edited or committed, which then stays.
