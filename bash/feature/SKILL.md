---
name: feature
description: Use to start a feature, begin implementing something new, or turn a prepared feature into a branch with a plan.
---

# Feature

## Overview

Starts one feature: a brainstorm that produces its design, one question that settles
its codename, title, branch type and bump type, a branch cut from the main branch,
and a plan written phase by phase. It ends on a planned branch with the state file
every later command reads. No code is written here.

**Preflight:** when this text opens on a `Preflight: passed` line, the check already
ran before the text was loaded: skip it. Otherwise run
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/preflight.sh"` as the first action. A non-zero
exit stops the skill: print its output verbatim and do nothing else.

**Announce at start:** "I am using implement:feature to open this feature." Speak to
the user in the user's language; write every artifact in English.

---

## The Iron Rule

```
NEVER write code here: this skill stops at a planned branch
NEVER start from a dirty tree, or from a branch other than the main one
NEVER stage or commit anything under docs/features in local mode
```

---

## Preconditions

```bash
# Each bash block is its own shell; derive rather than inherit.
MAIN=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##'); MAIN=${MAIN:-$(git branch --show-current)}
BRANCH=$(git branch --show-current) || exit 1
[ "$BRANCH" = "$MAIN" ] || { echo "start from $MAIN, not from $BRANCH"; exit 1; }
[ -z "$(git status --porcelain -- . ':!docs/features' ':!ROADMAP.md')" ] || { echo "the tree is not clean"; exit 1; }
MODE=$(python3 -c 'import json,os; print(json.load(open(".implement.json")).get("artifacts","local") if os.path.exists(".implement.json") else "local")')
if [ "$MODE" = committed ]; then
  if git check-ignore -q docs/features/probe || git check-ignore -q ROADMAP.md; then
    echo "docs/features and ROADMAP.md must not be ignored in committed mode"; exit 1
  fi
elif ! git check-ignore -q docs/features/probe || ! git check-ignore -q ROADMAP.md; then
  echo "docs/features and ROADMAP.md must be ignored in local mode: add them to the excludes, or set artifacts to committed in .implement.json"; exit 1
fi
find docs/features -mindepth 1 -maxdepth 1 -type d 2>/dev/null | while read -r d; do [ -f "$d/IMPLEMENTATION.md" ] || echo "prepared: $(basename "$d")"; done
```

The clean-tree test excludes the two artifact paths: a prepared feature leaves a
design, a plan and a roadmap line on disk, and refusing to start over them would
make `implement:prepare` unusable. Both paths are tested for the ignore rule one by
one, and the test inverts in `committed` mode rather than being skipped there. The
guard reads `docs/features/probe`, not `docs/features`: before the directory exists,
`check-ignore` on the bare path reads not ignored, while the inner path is matched by
every form the pattern takes.

The last line lists the prepared features: a directory with a design and a plan and
no state file is one `implement:prepare` left ready. The listing is reached whether
`docs/features` is absent or empty, because a shell that refuses an unmatched glob
(zsh, the session's shell) prints `no matches found` in both cases, and a guard on
the directory's existence covered only the first.

---

## Step 1 — A prepared feature?

When the block listed one or more, show the list and ask which one to start, or
`new` for a fresh brainstorm. **WAIT.** On a name: its design and its plan already
exist, so read its `DESIGN.md`, then go straight to Step 3 with the codename it
already carries. Three things are skipped because their output is already on disk:
the brainstorm of Step 2, the design write of Step 3 and the plan generation of
Step 5. What remains is the one question, the branch, the state file, the summary.

Its line in `ROADMAP.md` goes too: the roadmap lists what is prepared and not yet
started, and this feature is being started now.

```bash
# Each bash block is its own shell; derive rather than inherit.
CODENAME=<the prepared feature the user named>
[ -f ROADMAP.md ] && { TRIMMED=$(mktemp); grep -v "^- $CODENAME " ROADMAP.md > "$TRIMMED"; mv "$TRIMMED" ROADMAP.md; }
[ -s ROADMAP.md ] || rm -f ROADMAP.md
```

On `new`, or on an empty list, go to Step 2.

---

## Step 2 — Brainstorm

`superpowers:brainstorming`, architectural path. What applies is its content: the
questions, the approaches, and the design presented section by section with an
approval on each. What does not: this skill writes that design itself at Step 3, to
`docs/features/<codename>/DESIGN.md`, and the file the brainstorm would otherwise
save under `docs/superpowers/specs` is not written at all; and nothing is committed
here, since local mode stages nothing and committed mode commits once, at Step 7.

Nothing else happens in this step: no branch, no directory, no file.

---

## Step 3 — The one question

One question, asked once, carrying four proposed values:

- **codename** — kebab-case, derived from the title, the name every path and every
  branch uses from here on;
- **title** — derived here from the heading of the design, the brainstorm having
  settled none of its own;
- **branch** type — `feat` or `fix`;
- **bump** type — `major`, `minor`, `patch` or `none`, which `implement:close` reads
  and which alone decides whether a version file is ever touched.

Show the four proposed values together, in one message, and **WAIT**. The user
confirms them or corrects any of them. Asked once: a second round of confirmation
is the user's time spent on what they already answered.

Then create the feature's directory and write the design into it. The codename is
known only now, which is why the brainstorm came first, and the directory is made
here rather than at Step 4 so the design has somewhere to land:

```bash
# Each bash block is its own shell; derive rather than inherit.
CODENAME=<the confirmed codename>
mkdir -p "docs/features/$CODENAME"
```

The design goes to `docs/features/<codename>/DESIGN.md`. A prepared feature skips
this write: its design is already there, unchanged.

---

## Step 4 — Branch

```bash
# Each bash block is its own shell; derive rather than inherit.
MAIN=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##'); MAIN=${MAIN:-$(git branch --show-current)}
CODENAME=<the confirmed codename>
git checkout -b <feat-or-fix>/"$CODENAME" "$MAIN"
mkdir -p "docs/features/$CODENAME/plan"
```

---

## Step 5 — Plan

`superpowers:writing-plans` on `DESIGN.md`. What applies is its decomposition and
the content it gives each unit: the sub-phases, the files, the tests and the
definition of done.

What does not. Its mandatory plan header, the one naming a REQUIRED SUB-SKILL and
`superpowers:subagent-driven-development`, is omitted, and so is its execution
handoff, the closing question offering that same choice: `implement:phase` writes
every sub-phase inline, and its Iron Rule forbids handing that writing to a
subagent. Its output goes under `docs/features/<codename>/plan/` — `INDEX.md`
listing the phases, and one `phase-NN-<slug>.md` per phase — never under
`docs/superpowers/plans`. Its commit example does not apply either: the convention
is read from `git log` at commit time, in `implement:phase`.

`implement:phase` reads those files and nothing else.

---

## Step 6 — State

Write `docs/features/<codename>/IMPLEMENTATION.md` in the method's state-file shape
(`references/plan.md` of `method:lifecycle`), exactly: `implement:phase` and
`implement:close` parse it, so the spelling is the contract.

One row per phase of `plan/INDEX.md`, in its order, `NN` on two digits, status
`todo`, milestone empty. The base is the head the branch was cut from, which the
new branch still points at:

```bash
# Each bash block is its own shell; derive rather than inherit.
BRANCH=$(git branch --show-current) || exit 1
CODENAME=${BRANCH#*/}
git rev-parse --short HEAD          # the Base line: nothing is committed yet
ls "docs/features/$CODENAME/plan"   # the rows to write, one per phase file
```

---

## Step 7 — Committed mode

Only when the artifacts mode read in the preconditions is `committed`: one commit
`Start <title>` carrying the design, the plan, the state file and `ROADMAP.md` when
it exists — a feature started with `new` never had one. In the convention read from
`git log --format=%s -10`, with no trailer. In `local` mode this step does nothing:
the files stay on disk and nothing under `docs/features/` is ever staged.

---

## The summary

Close on it, in the user's language: the codename, the branch, the number of phases
and the title of the first one, the artifacts mode, and the next command,
`/implement:phase`. Nothing is pushed: the branch is local until the user says
otherwise, and this skill never says it for them.

---

## Stops

| Situation | The one line |
|---|---|
| The current branch is not the main one | `start from <main>, not from <branch>` |
| The tree is dirty | `the tree is not clean` |
| `docs/features` or `ROADMAP.md` is not ignored in local mode | `docs/features and ROADMAP.md must be ignored in local mode: add them to the excludes, or set artifacts to committed in .implement.json` |
| Either of them is ignored in committed mode | `docs/features and ROADMAP.md must not be ignored in committed mode` |
| The user has not answered the one question | wait; nothing is derived from a value they did not confirm |
| The design has no heading to derive a title from | ask for the title in one line, then wait |

---

## Report

```
branch:    <type>/<codename>, cut from <main> at <sha>
commits:   none in local mode; one "Start <title>" in committed mode
files:     docs/features/<codename>/DESIGN.md, plan/INDEX.md, plan/phase-NN-*.md, IMPLEMENTATION.md
gate:      not run here, no code is written
checks:    the state table matches plan/INDEX.md row for row
deviations: what departs from what the user confirmed, and why
open questions: what the design leaves for a phase to settle
status:    done|blocked|question — <one line>
```

---

## Quick Reference

```
1. Preflight, then the preconditions block (main branch, clean tree, MODE, prepared list)
2. A prepared feature? WAIT for a name or "new"
3. superpowers:brainstorming, architectural path, for the design and the title
4. The one question: codename, title, branch type, bump type. WAIT. Asked once
5. git checkout -b <type>/<codename> from the main branch
6. superpowers:writing-plans on DESIGN.md, output under plan/
7. IMPLEMENTATION.md in the exact shape: six header lines, one row per phase, todo
8. committed mode only: one commit "Start <title>", no trailer
9. Summary, then /implement:phase. Write no code, push nothing
```
