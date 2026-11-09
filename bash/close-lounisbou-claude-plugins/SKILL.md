---
name: close
description: Use to close a feature, finish a branch, or cut the release commit once every phase is done.
---

# Close

## Overview

Closes one feature on its branch: the project's full gate, the version bump the
feature declared, a summary of everything the branch carries, and the removal of the
local working notes. It refuses while a phase is not done or the tree is not clean.
What comes after the branch is the user's and is never done here.

**Preflight:** when this text opens on a `Preflight: passed` line, the check already
ran before the text was loaded: skip it. Otherwise run
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/preflight.sh"` as the first action. A non-zero
exit stops the skill: print its output verbatim and do nothing else.

**Announce at start:** "I am using implement:close to finish this branch." Speak to
the user in the user's language; write every artifact in English.

---

## The Iron Rule

```
NEVER delete a branch
NEVER close while a phase is not done, or while the tree is dirty
NEVER touch a version file when the bump type is none
```

This skill's own steps end at the branch. A push and a draft pull request need no consent;
taking it out of draft and the merge follow the method's ready gate and consent rules. Once
the pull request is open at its final head, run `/implement:review`: the review is made by
another session, never by this one.

---

## Preconditions

`implement:close [--docs <path>]`. Without it the path is derived from the branch
name (`feat/<codename>` or `fix/<codename>`). When `--docs <path>` was given,
`export DOCS_OVERRIDE=<path>` before EVERY block below, not only the first: each
block is its own shell and inherits nothing from the one before it.

When the `mcp__implement__state` tool is listed, one call replaces the derivation:
`get`, with `docs` set to the `--docs` path when one was given, answers the branch,
the codename, the artifacts path and mode, the ignore-guard verdict, the head,
whether the tree is clean, and the parsed state file with its next phase. A verdict
other than `ok` is the stop it names; `artifacts path given, ignore guard skipped`
is not a stop. The bump, the base and every row are in the state it returns. Without
the tool, the blocks below are the path, and they compute the same values.

```bash
# Each bash block is its own shell; derive rather than inherit.
BRANCH=$(git branch --show-current) || exit 1
CODENAME=${BRANCH#*/}
DOCS=${DOCS_OVERRIDE:-docs/features/$CODENAME}
[ -f "$DOCS/IMPLEMENTATION.md" ] || { echo "no IMPLEMENTATION.md under $DOCS: pass --docs <path>"; exit 1; }
[ -z "$(git status --porcelain)" ] || { echo "the tree is not clean"; exit 1; }
grep -qE '^\| *[0-9]+ *\|[^|]*\| *(todo|doing) *\|' "$DOCS/IMPLEMENTATION.md" && { echo "a phase is not done"; exit 1; }
BUMP=$(grep -E '^\*\*Bump\*\*:' "$DOCS/IMPLEMENTATION.md" | sed 's/^\*\*Bump\*\*: *//')
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
echo "$CODENAME ready to close, bump $BUMP, artifacts $MODE"
```

Both artifact paths are tested one by one, and the test inverts in `committed` mode
rather than being skipped there: this skill deletes under one of them and trims the
other, and it does that only where the repository agrees they are working notes. An
explicit `--docs <path>` skips the test altogether, the caller having taken the
responsibility for the directory it named. Step 4 derives `MODE` again, for the same
reason the path is re-exported: it runs in a shell of its own. The guard reads
`docs/features/probe`, not `docs/features`: before the directory exists,
`check-ignore` on the bare path reads not ignored, while the inner path is matched by
every form the pattern takes.

---

## Step 1 — The full gate

The whole project, not the files of one phase. The commands are the ones the
repository names, in this order of discovery: the check and test commands of its
`CLAUDE.md`, else those of its `CONTRIBUTING.md`, else its test suite as its own
documentation describes it. Run each one synchronously, in the call that waits for
it, and state it with its exit code.

A non-zero code stops here: name the command, its exit code and the first lines of
its output, and repair nothing. A feature is not closed over a red gate, and a gate
whose exit code was not read was not run.

---

## Step 2 — The version

Only when the bump type read above is not `none`. Detect the version file in this
order, and take the first one that exists:

```
VERSION
pyproject.toml
package.json
composer.json
.claude-plugin/plugin.json
```

The order is the contract: a repository holding several of them is bumped in the
first one, always the same one. Read the current version, then apply the bump —
`major` raises the first number and resets the two others to zero, `minor` raises
the second and resets the third, `patch` raises the third. Write it back in place:
`python3` for a JSON field or a TOML field, so the rest of the file is untouched;
`printf` for a plain `VERSION` file.

Run the full gate of Step 1 again, every command with its exit code. A non-zero
code stops here with the status `question` and one line:
`version written in <file>, gate red: <the first failing line>` — a repository that
mirrors its version elsewhere (a marketplace entry, a suite literal) says so through
its own gate, and aligning those places is the repository's decision, not this
skill's guess.

Then one commit, with no trailer, carrying the version file alone — and, in
`committed` mode, the feature's artifacts with it. Its subject takes the shape of
the repository's last release commit:

```bash
# Each bash block is its own shell; derive rather than inherit.
git log --format=%s -E --grep='^([a-z]+(\([^)]*\))?: )?[Rr]elease' -3
```

`chore: release pr-review 0.3.3` where that log reads `chore: release pr-review 0.3.2`, and
`chore: release <version>` where it holds no release subject at all.

A bump type other than `none` with none of the five files present stops the skill:
say which five were looked for and wait. Guessing a version file is how a version
lands in a file nothing reads.

---

## Step 3 — The summary

```bash
# Each bash block is its own shell; derive rather than inherit.
BRANCH=$(git branch --show-current) || exit 1
CODENAME=${BRANCH#*/}
DOCS=${DOCS_OVERRIDE:-docs/features/$CODENAME}
BASE=$(grep -E '^\*\*Base\*\*:' "$DOCS/IMPLEMENTATION.md" | sed 's/^\*\*Base\*\*: *//')
[ -n "$BASE" ] || { echo "no Base line in $DOCS/IMPLEMENTATION.md"; exit 1; }
git log --format='%h %s' "$BASE"..HEAD
git diff --stat "$BASE"..HEAD
```

The summary states, in the user's language: the branch, every commit since the base,
the version if one was written, and each gate command with its exit code. It ends on
one sentence, said once: this skill's steps end at the branch: a push and a draft pull request need no consent, and ready and merge follow the method's gate.

---

## Step 4 — The local files

In `local` mode, and only there, the feature's own working notes go: that directory
and no other, plus the feature's line in the roadmap when it has one.

```bash
# Each bash block is its own shell; derive rather than inherit.
BRANCH=$(git branch --show-current) || exit 1
CODENAME=${BRANCH#*/}
DOCS=${DOCS_OVERRIDE:-docs/features/$CODENAME}
MODE=$(python3 -c 'import json,os; print(json.load(open(".implement.json")).get("artifacts","local") if os.path.exists(".implement.json") else "local")')
[ "$MODE" = committed ] && { echo "committed mode: nothing is deleted"; exit 0; }
[ -d "$DOCS" ] && rm -r "$DOCS"
rmdir docs/features docs 2>/dev/null || true
[ -f ROADMAP.md ] && { TRIMMED=$(mktemp); grep -v "^- $CODENAME " ROADMAP.md > "$TRIMMED"; mv "$TRIMMED" ROADMAP.md; }
[ -s ROADMAP.md ] || rm -f ROADMAP.md
```

The directory is removed only when it is there: a second run of this skill, or a
close over a directory a caller had already taken away, is not an error. `rmdir`
takes each parent only when the removal emptied it, and says nothing when it did
not: a repository holding another feature, or holding documentation of its own under
`docs`, keeps both directories. The roadmap
goes the same way when the trim emptied it, since a file holding nothing is not a
roadmap.

In `committed` mode nothing is deleted: the design, the plan and the state are part
of the repository and stay in it.

---

## Stops

| Situation | The one line |
|---|---|
| No `IMPLEMENTATION.md` under the derived path | `no IMPLEMENTATION.md under <docs>: pass --docs <path>` |
| The tree is dirty | `the tree is not clean` |
| A row is still `todo` or `doing` | `a phase is not done` |
| `docs/features` or `ROADMAP.md` is not ignored in local mode | `docs/features and ROADMAP.md must be ignored in local mode: add them to the excludes, or set artifacts to committed in .implement.json` |
| Either of them is ignored in committed mode | `docs/features and ROADMAP.md must not be ignored in committed mode` |
| The state file carries no `Base` line | `no Base line in <docs>/IMPLEMENTATION.md` |
| A gate command came back non-zero | `<command> exit <code>` and the first lines of its output |
| A bump is asked and no version file exists | the five names looked for, in order, then wait |
| The gate is red on the run that follows the version write | `version written in <file>, gate red: <the first failing line>` — status `question` |

Each stop says its line once and waits. No answer to a stop turns it into an outward
action that no instruction calls for.

---

## Report

```
branch:    <type>/<codename>, base <sha>
commits:   <short sha> <subject>   (every commit since the base)
files:     the version file if one was written
gate:      <command> exit <code>   (one line per command: both runs when a
           version was written — the full gate of Step 1, then the same gate
           again — otherwise the one gate of Step 1)
checks:    every phase row done, tree clean before and after
deviations: what departs from the plan or the bump type the feature declared
open questions: what the branch leaves open
status:    done|blocked|question — <one line>
```

---

## Quick Reference

```
1. Preflight, then derive BRANCH, CODENAME, DOCS, BUMP, MODE, and guard both
   artifact paths (--docs exports DOCS_OVERRIDE and skips the guard)
2. Refuse on a dirty tree, a missing state file, or a row not done
3. Full-project gate, every command with its exit code. Red stops, nothing repaired
4. Bump none: skip. Otherwise the first of VERSION, pyproject.toml, package.json,
   composer.json, .claude-plugin/plugin.json, then the same gate again, then one
   commit in the shape the repository's last release subject gives
5. Summary: branch, commits since the base, version, gate codes, the closing sentence
6. local mode: delete the feature directory, the parents it empties and its roadmap
   line. committed: keep all
7. The steps end at the branch; ready and merge belong to the gate
```
