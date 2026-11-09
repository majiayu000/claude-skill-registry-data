---
name: check
description: Use to check a delivery, verify a phase, or check a commit range against the plan and the design.
---

# Check

## Overview

Verifies one delivery against the plan and the design on a commit range: seven
verifications, each carrying the evidence that produced it, then one table and one
verdict. It re-runs the project's gate itself rather than believing a report of it.
It edits nothing: a defect is named here and repaired elsewhere.

**Preflight:** when this text opens on a `Preflight: passed` line, the check already
ran before the text was loaded: skip it. Otherwise run
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/preflight.sh"` as the first action. A non-zero
exit stops the skill: print its output verbatim and do nothing else.

**Announce at start:** "I am using implement:check to verify this delivery against
its plan." Speak to the user in the user's language; write every artifact in English.

---

## The Iron Rule

```
NEVER edit, stage or commit anything: this skill reads and reports
NEVER guess an exit code: a command that did not run is a FAIL row
NEVER pass a row whose evidence was not read in this run
```

A verification with no output quoted was not done. A claim with no evidence is a
`FAIL`, not a doubt — `superpowers:verification-before-completion` states the same
rule for the work this skill reads.

With this plugin's hooks module loaded, an edit, a `git add` and a `git commit` are
also refused at the call from this skill's start until its verdict line is written
under the table, its turn ends, or the user speaks.

---

## Inputs

`implement:check <base>..<head> [--phase N] [--docs <path>]`

- `<base>..<head>` — the range under review. Required: without it there is nothing
  to read. `HEAD` on both sides of a sub-phase is the common case.
- `--phase N` — the phase whose file is the reference for checks 3, 5 and 7. Without
  it, the reference is every phase file the range touches. `N` is written on two
  digits everywhere it is interpolated: `--phase 3` reads row `03` and
  `plan/phase-03-*.md`.
- `--docs <path>` — the feature directory. Without it the path is derived from the
  branch name (`feat/<codename>` or `fix/<codename>`).

Two values travel by the environment rather than by a positional argument, because
each bash block below is its own shell and inherits nothing from the one before it:
`export RANGE=<base>..<head>` before the blocks below, and, when `--docs <path>` was
given, `export DOCS_OVERRIDE=<path>` before EVERY block below, not only the first.

When the `mcp__implement__state` tool is listed, one call replaces the derivation:
`get`, with `docs` set to the `--docs` path when one was given, answers the branch,
the codename, the artifacts path and mode, the ignore-guard verdict, the head,
whether the tree is clean, and the parsed state file with its next phase. A verdict
other than `ok` is the stop it names; `artifacts path given, ignore guard skipped`
is not a stop. The range is still exported for verification 2. Without the tool, the
blocks below are the path, and they compute the same values.

```bash
# Each bash block is its own shell; derive rather than inherit.
BRANCH=$(git branch --show-current) || exit 1
CODENAME=${BRANCH#*/}
DOCS=${DOCS_OVERRIDE:-docs/features/$CODENAME}
[ -d "$DOCS/plan" ] || { echo "no plan under $DOCS: pass --docs <path>"; exit 1; }
echo "checking $CODENAME from $DOCS"
```

The phase file is `<docs>/plan/phase-NN-<slug>.md`, the design is `<docs>/DESIGN.md`,
the state is `<docs>/IMPLEMENTATION.md`. A delivery with no plan is not checkable:
stop on the line the block prints.

---

## The seven verifications

Run the seven in this order: a delivery is read before it is compared, compared
before the gate is re-run, and the design is the last word. Each produces one row
of the report, with the command or the quotation that is its evidence.

### 1. The delivery is not truncated

Read the report or the commit list under review to its end. It ends with the last
item it announces: a list of five sub-phases ends on the fifth, a table of rows ends
on the row the header promises. **FAIL** when it stops mid-item, when a count in the
prose disagrees with what follows it, or when the text ends on an unclosed fence.

### 2. The git range says what is claimed

```bash
# Each bash block is its own shell; derive rather than inherit.
RANGE=${RANGE:-}
[ -n "$RANGE" ] || { echo "give me a range: implement:check <base>..<head>"; exit 1; }
git log --format='%h %s' "$RANGE"
git diff --stat "$RANGE"
git diff --name-only "$RANGE"
```

**FAIL** when a commit the delivery claims is absent from the log, when a file it
claims to have written is absent from the diff, when the range is empty, or when a
commit message carries a trailer the repository's convention does not use.

### 3. Plan compliance, sub-phase by sub-phase

Read the phase file, then take the sub-phases the delivery claims: the ones its
report names, or, when it carries no report, the ones the commits since the recorded
base answer. For each one: every deliverable it names is present in the diff, and
nothing the delivery claims is absent from it. Quote the plan line beside the file
that answers it. **FAIL** on a deliverable with no file, on a step marked done with
no commit, or on a test the plan requires and the diff does not add. A sub-phase of
the file this delivery does not claim has not been delivered yet, and is not a row
here.

### 4. The gate, re-run here

The commands are the ones the repository names: read `CLAUDE.md`, else
`CONTRIBUTING.md`, else run the tests covering the files the diff touches. Run each
one synchronously and read its exit code; state the command and the code side by
side. **FAIL** on any non-zero code. A command that cannot run at all — a missing
tool, a missing dependency — is its own `FAIL` row naming what is missing, never a
guess and never a skip.

### 5. Scope drift

Every path of `git diff --name-only <base>..<head>` is either named by the phase
file or is a direct consequence it states. **FAIL** on a file outside that list: name
the path and the phase file it is absent from. A formatting sweep over untouched
files, a dependency bump nobody asked for and a neighbouring fix are all drift.

### 6. Design coherence

Read what the diff does, then read the sentences of `DESIGN.md` it implements. They
agree or they do not. **FAIL** when the code answers a different problem, when it
contradicts a decision the design records, or when a decision the design leaves open
was closed here without a line saying so.

### 7. Design-contract coverage

Every interface the design names for this phase — a command and its arguments, a
file shape, a table header, an exit code, a state key — exists in the diff with the
stated spelling. The reference is the same as verification 3, the sub-phases the
delivery claims: a contract a sub-phase still to come will carry is not missing from
this range. Quote the design line and the line of the diff that answers it. **FAIL**
on a contract that is absent, renamed or narrowed.

---

## Report

This skill's report is its table, its verdict line and its status; the named
sections of the other four do not apply here.

One row per verification, the evidence in the row, then the verdict and the status.

```
| check | evidence | result |
|---|---|---|
| 1 truncation | the report ends on sub-phase 5 of 5 | PASS |
| 2 git range | 3 commits, 7 files, all claimed | PASS |
| 3 plan compliance | every deliverable of 4.1 to 4.3 present | PASS |
| 4 gate | bash tests/run-tests.sh exit 0 | PASS |
| 5 scope drift | README.md touched, absent from the phase file | FAIL |
| 6 design coherence | D2 honoured: no version touched here | PASS |
| 7 contract coverage | --docs and --phase both present | PASS |

FAIL: 5
status: done — row 5 is cosmetic, named under deviations
```

The verdict is one line: `PASS`, or `FAIL: <the numbers of the failing rows>`. The
status line follows the method: `done` on a clean `PASS`, or when every failing row
is cosmetic and named; `blocked` when the gate or the plan compliance fell;
`question` when the design and the delivery disagree on something the design does
not settle.

---

## Stops

| Situation | The one line |
|---|---|
| No plan under the derived path | `no plan under <docs>: pass --docs <path>` |
| No range given | `give me a range: implement:check <base>..<head>` |
| A gate command cannot run | a `FAIL` row naming the missing tool, and the run continues |
| The design is absent | checks 6 and 7 are `FAIL` rows naming it, never silent passes |

Each stop says its line once and waits. This skill never repairs what it finds and
never asks whether it should continue.

---

## Quick Reference

```
1. Preflight, then export RANGE; derive BRANCH, CODENAME, DOCS (--docs exports
   DOCS_OVERRIDE)
2. Read the plan file of the phase and DESIGN.md
3. 1 truncation   — the delivery ends on the item it announces
4. 2 git range    — log, diff --stat, diff --name-only against what is claimed
5. 3 plan         — every deliverable present, nothing claimed that is absent
6. 4 gate         — re-run it here, every command with its exit code
7. 5 drift        — files outside the phase file's list
8. 6 design       — the diff against the sentences it implements
9. 7 contracts    — every named interface, with its spelling
10. The table, the verdict line, the status. Edit nothing.
```
