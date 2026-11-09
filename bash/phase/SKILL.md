---
name: phase
description: Use to run the plan's phases, continue a feature already branched and planned, or execute one phase by number.
---

# Phase

## Overview

Runs every phase of the plan that is not done, in order, without pausing between
them; given a number, that phase only, then stops and reports. Each sub-phase is
written here, inline: failing tests first, the code, the project's own gate, one
commit, then a check of what the commit range produced. Read-only search subagents
are welcome; the work itself is never handed to one.

**Preflight:** when this text opens on a `Preflight: passed` line, the check already
ran before the text was loaded: skip it. Otherwise run
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/preflight.sh"` as the first action. A non-zero
exit stops the skill: print its output verbatim and do nothing else.

**Announce at start:** "I am using implement:phase to run the plan." Speak to the
user in the user's language; write every artifact in English.

---

## Inputs

`implement:phase [N] [--docs <path>]`

- `N` — one phase, by its number in the state table. Without it: every phase not
  done, in order, to the end of the plan. `N` is written on two digits everywhere it
  is interpolated: `implement:phase 3` reads row `03` and `plan/phase-03-*.md`.
- `--docs <path>` — the feature directory. Without it the path is derived from the
  branch name (`feat/<codename>` or `fix/<codename>`). A worktree does not see an
  ignored directory of the main checkout: whoever starts the run there gives the
  path.

When `--docs <path>` was given, `export DOCS_OVERRIDE=<path>` before EVERY block
below, not only the first: each block is its own shell and inherits nothing from the
one before it.

When the `mcp__implement__state` tool is listed, one call replaces the derivation:
`get`, with `docs` set to the `--docs` path when one was given, answers the branch,
the codename, the artifacts path and mode, the ignore-guard verdict, the head,
whether the tree is clean, and the parsed state file with its next phase. A verdict
other than `ok` is the stop it names; `artifacts path given, ignore guard skipped`
is not a stop. `mark` (`phase`, `status`, `milestone: "HEAD"`) writes one row of the
table, resolving the sha itself: it replaces the hand edits of the loop below.
Without the tool, the blocks below are the path, and they compute the same values.

```bash
# Each bash block is its own shell; derive rather than inherit.
BRANCH=$(git branch --show-current) || exit 1
CODENAME=${BRANCH#*/}
DOCS=${DOCS_OVERRIDE:-docs/features/$CODENAME}
[ -f "$DOCS/IMPLEMENTATION.md" ] || { echo "no IMPLEMENTATION.md under $DOCS: run implement:feature first, or pass --docs <path>"; exit 1; }
MODE=$(python3 -c 'import json,os; print(json.load(open(".implement.json")).get("artifacts","local") if os.path.exists(".implement.json") else "local")')
if [ -n "${DOCS_OVERRIDE:-}" ]; then
  echo "artifacts path given, ignore guard skipped"
elif [ "$MODE" = committed ]; then
  if git check-ignore -q docs/features/probe || git check-ignore -q ROADMAP.md; then
    echo "docs/features and ROADMAP.md must not be ignored in committed mode"; exit 1
  fi
elif ! git check-ignore -q docs/features/probe || ! git check-ignore -q ROADMAP.md; then
  echo "docs/features and ROADMAP.md must be ignored in local mode: add them to the excludes, or set artifacts to committed in .implement.json"; exit 1
fi
echo "$CODENAME on $BRANCH, artifacts $MODE, state $DOCS/IMPLEMENTATION.md"
```

Both artifact paths are tested one by one, and the test inverts in `committed` mode
rather than being skipped there. An explicit `--docs <path>` skips it altogether:
the caller named a directory the repository's excludes know nothing about, and took
the responsibility for it. The guard reads `docs/features/probe`, not
`docs/features`: before the directory exists, `check-ignore` on the bare path reads
not ignored, while the inner path is matched by every form the pattern takes.

`IMPLEMENTATION.md` is the only source of truth for progress, in the method's
state-file shape: a header, then one row per phase, status `todo`, `doing` or `done`.
The milestone column carries a sha from the
moment a phase is under way: while the row is `doing` it holds the commit the
sub-phase being written started from, rewritten before each one, and when the row
turns `done` it holds the last commit of the phase. A `todo` row leaves it empty. A
run taken up again rebuilds the range it owes from that column rather than guessing
where the work began.

---

## The loop

Read the table. The phase to run is `N` when a number was given, else the first row
whose status is not `done`. Mark that row `doing` before anything else, so an
interrupted run resumes on the right phase. Read its file,
`<docs>/plan/phase-NN-<slug>.md`, in full before writing a line: it names the
sub-phases, the files, the tests and the definition of done.

Then, for each sub-phase of that file, in its order. Before the first line of one is
written, record where it starts: its row keeps the status `doing` and its milestone
column takes the current head. That sha is the base of the range step 5 checks, and
it is written before the work rather than after it so that a run taken up again
checks a sub-phase it did not itself begin.

```bash
# Each bash block is its own shell; derive rather than inherit.
BRANCH=$(git branch --show-current) || exit 1
CODENAME=${BRANCH#*/}
DOCS=${DOCS_OVERRIDE:-docs/features/$CODENAME}
git rev-parse --short HEAD   # this sub-phase's base, into "$DOCS/IMPLEMENTATION.md"
```

1. **Tests first.** `superpowers:test-driven-development`: the failing test is
   written and seen to fail before the code that makes it pass. A test that has
   never been red proves nothing.
2. **The code.** Only what the sub-phase names. A file the sub-phase does not name
   is scope drift, and drift is a decision, not an initiative: see Stops.
3. **The gate.** The commands the repository names, in this order of discovery: the
   check and test commands of its `CLAUDE.md`, else those of its `CONTRIBUTING.md`,
   else the tests covering the files just touched. Run each one synchronously, in
   the call that waits for it, and state it with its exit code. At most two fixes:
   a third red run stops the phase `blocked`.
4. **The commit.** Read the convention rather than impose one:

```bash
# Each bash block is its own shell; derive rather than inherit.
git log --format=%s -10
```

   A conventional prefix in those ten lines means the sub-phase uses one; plain
   imperative subjects mean plain imperative prose. A body only when the reason is
   not obvious from the subject. No trailer of any kind, whatever the convention.

5. **The check.** `implement:check <recorded sha>..HEAD --phase <N> --docs <path
   when given>`, where the recorded sha is the one the milestone column took when
   this sub-phase started and the path is the one `--docs` carried, when it carried
   one. A `FAIL` is repaired
   inline and re-checked once. A second `FAIL` stops the phase `blocked`, with the
   table and the verdict quoted in the report.

When the last sub-phase is green, close the phase: set its row to `done`, the
milestone column giving up the last base it held for the last commit of the phase.

```bash
# Each bash block is its own shell; derive rather than inherit.
BRANCH=$(git branch --show-current) || exit 1
CODENAME=${BRANCH#*/}
DOCS=${DOCS_OVERRIDE:-docs/features/$CODENAME}
MODE=$(python3 -c 'import json,os; print(json.load(open(".implement.json")).get("artifacts","local") if os.path.exists(".implement.json") else "local")')
git rev-parse --short HEAD   # the milestone to write into "$DOCS/IMPLEMENTATION.md"
echo "artifacts $MODE"
```

In `committed` mode, and only there, the updated state and the plan travel in one
commit `chore(<codename>): phase N gate — <title>` after the sub-phase commits. In `local` mode the
file is written and nothing under `docs/features/` is ever staged.

Then: with `N`, stop and report that phase. Without `N`, start the next row that is
not done, with no question and no progress narration in between. When no row is
left, say that `implement:close` is next.

---

## Stops

| Situation | The one line |
|---|---|
| No `IMPLEMENTATION.md` under the derived path | `no IMPLEMENTATION.md under <docs>: run implement:feature first, or pass --docs <path>` |
| `docs/features` or `ROADMAP.md` is not ignored in local mode | `docs/features and ROADMAP.md must be ignored in local mode: add them to the excludes, or set artifacts to committed in .implement.json` |
| Either of them is ignored in committed mode | `docs/features and ROADMAP.md must not be ignored in committed mode` |
| A gate still red after two fixes | `gate red after two fixes: <command> exit <code>` — status `blocked` |
| A second `FAIL` on the same sub-phase | `check failed twice on <sub-phase>: <the failing rows>` — status `blocked` |
| The plan does not settle a scope question | the question in one line, then wait — status `question` |
| An outward-facing or irreversible action is needed that no instruction calls for | name it and wait; it is not taken on the skill's own account |

Each stop asks once, in one line, and waits. No progress narration between
sub-phases, and no question whose answer is already in the plan.

---

## Report

Named sections, in this order, one report per phase:

```
branch:    <type>/<codename>, base <sha>
commits:   <short sha> <subject>   (one line per commit of the phase)
files:     <path>   (one line per file the phase touched)
gate:      <command> exit <code>   (one line per command, every run)
checks:    <sub-phase> PASS | FAIL: <rows>   (one line per implement:check run)
deviations: what departs from the plan file, and the line that justified it
open questions: what the plan does not settle, one line each
status:    done|blocked|question — <one line>
```

`done` when every sub-phase is green and its check passed, a deviation named under
`deviations`. `blocked` on a red gate or a twice-failed check. `question` on a scope
question the plan does not answer.

---

## The Iron Rule

```
NEVER dispatch a subagent to write code, tests or commits: the work is written here
NEVER report an exit code that was not read, or skip the gate because the change looks small
NEVER mark a phase done while its check is red or its gate is untested
```

Read-only search subagents are the one exception, and they read; they do not write.

With this plugin's hooks module loaded, the first line is also held at the call: a
subagent other than `Explore` runs only on the user's Allow, from this skill's start until
another implement skill starts, the turn is interrupted, or `/implement:release-guard`. A refusal is a stop to report, never a wall to go
around.

This skill's own steps end at the branch. A push and a draft pull request need no consent;
taking it out of draft and the merge follow the method's ready gate and consent rules.

---

## Red Flags

| Thought | Reality |
|---|---|
| "The change is small, the gate can wait" | An unrun gate is a red gate you have not seen yet. Run it. |
| "The test passes, no need to see it fail first" | A test never seen red proves the code, not the test. Write it failing. |
| "This neighbouring file obviously needs the same fix" | Drift. The plan names the files; anything else is a decision to bring back. |
| "The check is nearly green, the last row is cosmetic" | Rows are not weighted here. Repair it or report it, do not round it up. |
| "I will summarise the phases at the end" | The report is per phase, written when the phase closes. Later means never. |

---

## Quick Reference

```
1. Preflight, then derive BRANCH, CODENAME, DOCS, MODE (--docs exports DOCS_OVERRIDE)
2. IMPLEMENTATION.md: phase N, else the first row not done. Mark it doing, and record
   each sub-phase's starting sha in its milestone column before writing that sub-phase
3. Read plan/phase-NN-<slug>.md in full
4. Per sub-phase: failing test, code, gate with exit codes (two fixes at most)
5. Commit in the convention read from git log --format=%s -10, no trailer
6. implement:check <base>..HEAD --phase N --docs <path when given>; one fix, then stop
7. End of phase: row done, milestone = the phase's last commit; committed mode commits it
8. With N: stop and report. Without: the next row, no pause, no narration
9. No row left: implement:close is next
```
