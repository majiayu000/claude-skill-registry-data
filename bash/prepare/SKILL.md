---
name: prepare
description: Use to prepare a feature, plan the next feature ahead of time, or add an entry to the roadmap without starting it.
---

# Prepare

## Overview

Prepares one feature without opening it: the brainstorm, the codename and the bump
type confirmed once, the plan written phase by phase, and one line appended to the
roadmap. It creates no branch and no state file, so it runs while another feature is
in progress on another branch. `implement:feature` later offers it as a start.

**Preflight:** when this text opens on a `Preflight: passed` line, the check already
ran before the text was loaded: skip it. Otherwise run
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/preflight.sh"` as the first action. A non-zero
exit stops the skill: print its output verbatim and do nothing else.

**Announce at start:** "I am using implement:prepare to plan this ahead." Speak to
the user in the user's language; write every artifact in English.

---

## The Iron Rule

```
NEVER create a branch, switch branch or touch the working tree of the current one
NEVER stage or commit anything in local mode
```

The absence of `IMPLEMENTATION.md` is what makes a prepared feature recognisable.
Writing one here would turn it into a feature already under way, which nothing
would then be running.

---

## Preconditions

```bash
# Each bash block is its own shell; derive rather than inherit.
MODE=$(python3 -c 'import json,os; print(json.load(open(".implement.json")).get("artifacts","local") if os.path.exists(".implement.json") else "local")')
if [ "$MODE" = committed ]; then
  if git check-ignore -q docs/features/probe || git check-ignore -q ROADMAP.md; then
    echo "docs/features and ROADMAP.md must not be ignored in committed mode"; exit 1
  fi
elif ! git check-ignore -q docs/features/probe || ! git check-ignore -q ROADMAP.md; then
  echo "docs/features and ROADMAP.md must be ignored in local mode: add them to the excludes, or set artifacts to committed in .implement.json"; exit 1
fi
echo "artifacts $MODE"
```

Both paths are tested one by one, because this skill writes to both: the design and
the plan under `docs/features/`, one line in `ROADMAP.md` at the root. An unignored
roadmap in `local` mode leaves a dirty tree behind, which `implement:feature` and
`implement:close` then refuse. In `committed` mode the test inverts rather than
being skipped: neither path may be ignored there. The guard reads
`docs/features/probe`, not `docs/features`: before the directory exists,
`check-ignore` on the bare path reads not ignored, while the inner path is matched by
every form the pattern takes.

The branch does not matter here and is not read: whatever is checked out stays
checked out, dirty or clean.

---

## Step 1 — Brainstorm

`superpowers:brainstorming`, architectural path. Its output is the design of the
prepared feature, and the only source of its title.

---

## Step 2 — The one question

One question, asked once, carrying three proposed values: the **codename**
(kebab-case, derived from the title), the **title**, and the **bump** type
(`major`, `minor`, `patch` or `none`). **WAIT** for the confirmation or the
corrections. The branch type is not asked here: it is chosen when the feature is
actually started, and asking for it now buys an answer that nothing reads.

Then write the design to `docs/features/<codename>/DESIGN.md`.

---

## Step 3 — Plan

`superpowers:writing-plans` on `DESIGN.md`, output under
`docs/features/<codename>/plan/`: `INDEX.md` and one `phase-NN-<slug>.md` per
phase. Same shape as a started feature, because it becomes one unchanged.

---

## Step 4 — The roadmap line

Append one line to `ROADMAP.md` at the repository root, creating the file when it
is absent:

```
- <codename> — <title> (<bump>)
```

One line per prepared feature, nothing else. In `local` mode neither `ROADMAP.md`
nor anything under `docs/features/` is staged; in `committed` mode they join the
repository through the commit of whoever starts the feature, not through this skill.

---

## Stops

| Situation | The one line |
|---|---|
| `docs/features` or `ROADMAP.md` is not ignored in local mode | `docs/features and ROADMAP.md must be ignored in local mode: add them to the excludes, or set artifacts to committed in .implement.json` |
| Either of them is ignored in committed mode | `docs/features and ROADMAP.md must not be ignored in committed mode` |
| The user has not answered the one question | wait; a codename nobody confirmed becomes a path nobody recognises |
| A directory already holds that codename | `<codename> already exists: pick another codename, or start it with implement:feature` |

---

## Report

```
branch:    untouched, <the branch that was checked out>
commits:   none
files:     docs/features/<codename>/DESIGN.md, plan/INDEX.md, plan/phase-NN-*.md, ROADMAP.md
gate:      not run here, no code is written
checks:    the roadmap line matches the codename, the title and the bump type
deviations: what departs from what the user confirmed, and why
open questions: what the design leaves for a phase to settle
status:    done|blocked|question — <one line>
```

---

## Quick Reference

```
1. Preflight, then MODE and the check-ignore guard on both paths. No branch is read
2. superpowers:brainstorming, architectural path, for the design and the title
3. The one question: codename, title, bump type. WAIT. No branch type
4. superpowers:writing-plans on DESIGN.md, output under plan/
5. Append "- <codename> — <title> (<bump>)" to ROADMAP.md
6. Write no IMPLEMENTATION.md, create no branch, commit nothing in local mode
```
