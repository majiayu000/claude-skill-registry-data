---
name: known-issues-batch
description: Plan the next small batch of bug fixes from docs/phases/known-issues.md — pick a few Open rows that need no decision (default 4), confirm them and the release with the owner, number it as the next undefined phase (or straight after the active one), then write docs/phases/phase-N.M.md in the style of Phases 52.1 and 52.2, add the ROADMAP row and section and the spec.md §13 entry, mark the rows Scheduled and log any open questions. Plans only; /next-phase builds it. Run with /known-issues-batch, optionally with a count or the rows to take.
disable-model-invocation: true
argument-hint: "[how many rows, default 4] [K-numbers or an area to focus on, e.g. \"K10 K13\" or \"import\" — optional]"
---

# Plan a batch of known-issues fixes

The known-issues log holds more open rows than one phase should take on.
This skill takes **a few** of them, the smallest that need no decision,
and plans a phase for them, as
[Phase 52.1](../../../docs/phases/phase-52.1.md) and
[Phase 52.2](../../../docs/phases/phase-52.2.md) did. Read both phase files,
and the commits that planned them, before step 4:

```bash
git show 1437026e --stat        # Phase 52.1: phase file for the known-issues quick wins
git show 59b5c448               # Plan Phase 52.2: the full diff to copy
```

This skill **plans only**: no `src/`, template or test changes. The owner
builds the phase afterwards with `/next-phase`. It is not `/hotfix` (one
broken thing in the last release, fixed and shipped at once) and not
`/issue-sweep` (finding and recording new issues).

Read `CLAUDE.md` (§11–§13 especially), the top of
`docs/phases/known-issues.md` and of `docs/phases/open-questions.md` first.

The upstream repository is **gwpreston16/Logbook**; `origin` is the fork
(gwpreston/Logbook) and `upstream` is gwpreston16. Pass
`-R gwpreston16/Logbook` to every `gh` command, and open PRs with
`--head gwpreston:<branch>`.

`$ARGUMENTS` may give a count (default **4**, never more than **6**: the
owner wants a few rows each time, not the 8–10 that 52.1 and 52.2 took),
named K-numbers to take, or an area to prefer.

## 1. Sync

```bash
git status --porcelain                 # must be empty; stop otherwise
git fetch upstream --tags && git fetch origin
git switch master && git merge --ff-only upstream/master
gh pr list -R gwpreston16/Logbook --state open
git branch -a --list '*phase-*'
```

Never read the ROADMAP or the logs before this: they change through PRs
merged on gwpreston16. If an open PR or branch already plans a
known-issues batch that isn't merged (`phase-*-plan`, `known-issues-batch-*`),
say so and stop: finish that one first.

## 2. Pick the rows

```bash
grep -n '| Open |' docs/phases/known-issues.md
grep -n 'Needs a decision' docs/phases/open-questions.md
```

A row is a **candidate** only if all of these hold:

- Its status is exactly *Open*. Not *Scheduled* (already given to a phase),
  *Fixed* or *Won't fix*.
- It doesn't wait on a choice: its text doesn't say "Needs a decision" or
  name an open question that is still *Needs a decision* (check the
  question's row, since a question may have been decided since). Such a
  row can be fixed only once its question is decided (CLAUDE.md §12).
- It is small: a fix in one or two places, one regression test, no
  migration, no new setting, no design pass across many pages. Rows that
  an earlier batch put under *Not in scope* as "larger" or "need a design
  pass" stay out (read the *Not in scope* of the last two batches). A row
  that says "Needs an eval" or "measure first" is not small.
- Its *Where* still exists. Open the file and line it names and check
  that the problem is still there. Code moves, and another phase may
  have fixed a row by the way. A row already fixed is marked *Fixed* in
  step 5 (naming the commit or phase), not planned; 52.1 did this for K23.
- A row under a "Not re-checked" heading is confirmed first (reproduce
  it, or find the line that causes it). If it can't be confirmed, leave
  it out and say so.

**Rank** the candidates by severity (HIGH, MEDIUM, LOW, as
`.claude/review-rules.md` §6), then by how small the fix is, then by age
(the lowest K-number first). Then **group**: prefer rows in one area or
one set of files, so the phase has a theme (52.2: "Parts polish"), even if
that means a LOW row in that area instead of a lone MEDIUM elsewhere.
Docs-only rows (wrong spec text, a missing question in the log) are
cheap: one may join a batch on top of the count. Rows named in
`$ARGUMENTS` are taken first, if they pass the checks above. If one
doesn't, say why.

Take the count. If fewer candidates pass, take what there is. If none
pass, report which rows block on which questions, offer to ask the owner
those questions now (step 3's format), and stop.

## 3. Ask the owner (a hard stop)

Before writing any file, use `AskUserQuestion` (up to four questions per
call):

1. **The rows.** The proposed batch, one line each (K-number, severity,
   what's wrong, in plain words), and the next two or three candidates
   that didn't make the cut, so the owner can swap or add (they added
   K31 and K68 to 52.2). Recommend the proposed batch.
2. **The release.** Ship on its own as a patch release (the last tag's
   patch number plus one, `git tag --sort=-v:refname | head -1`), or with
   the next phase that releases. 52.1 (#481) and 52.2 (#486) each asked
   this. Recommend a patch on its own unless the rows touch code that the
   next releasing phase is changing.
3. Any **choice a row turns out to need** while you read the code in
   step 2 (as #480 did for K7, #482 for K37). Give the options and a
   recommendation. If the owner would rather not decide now, drop that
   row from the batch.

The release question and any question from point 3 become open questions
in step 5: *Decided* with today's date if the owner answered, *Needs a
decision* if not.

## 4. Where it goes and its number

```bash
grep -n '^| \[' ROADMAP.md
ls docs/phases/ | sed 's/phase-//;s/\.md//' | sort -V
git branch -a --list '*phase-*'
gh pr list -R gwpreston16/Logbook --state open
```

A phase is **active** when its ROADMAP row is 🚧, or a `phase-N.M` branch
or open PR has work not yet on `upstream/master`.

- **No active phase:** the batch is simply the **next phase not yet
  defined**: the number after the last row in the ROADMAP table, and its
  row goes at the end of the table (after any 📋 rows). With 53.4 the
  last row, that is **53.5**. Planned phases are never renumbered or
  moved for a batch.
- **A phase is active:** the batch goes straight after the active
  phase's row, numbered with the next free number that sorts there
  (52 🚧 → 52.1; 41.6 🚧 → 41.7 if 41.7 isn't taken). If no free number
  sorts there (53.2 🚧 and 53.3 📋), fall back to the next phase not yet
  defined, as above.

Numbering, either way: after `N.m` the next is `N.(m+1)`; after a
whole-number `N` it is `N.1`. Check that neither `docs/phases/phase-N.M.md`
nor a ROADMAP row with that number exists. **Never a two-decimal number**
(`53.2.1`): task numbers inside a phase file already use `N.M.k`, and
commits name them ("Phase 53.2.1: …").

Then set the **Prerequisites** line: the phase straight before it in the
table, merged. If the release is on its own, the previous tag too. The
phase after it gets this phase as its prerequisite only if it named the
one before (keep `MarkdownLinksTest` passing: K66).

## 5. Write it

On a planning branch (52.2's plan was PR #119 from `phase-52.2-plan`):

```bash
git switch -c phase-N.M-plan
```

Copy the shape of commit `59b5c448`. These files change, and nothing else:

- **`docs/phases/phase-N.M.md`**, in 52.2's structure:
  - Title: `# Phase N.M — <theme> from the known-issues log` (plus
    ` + patch release` if it releases on its own). Under it, an italic
    one-line summary ("*Four open rows of the known-issues log closed:
    …*").
  - `Status: 📋 planned · file lives in docs/phases/` (with
    `· releases **vX.Y.Z**, a patch release` if decided).
  - A paragraph saying it is the next batch after the last one (link
    it), which rows it takes, and why it is numbered where it is. The
    *Read first* line: `CLAUDE.md`, the spec sections the rows touch,
    `open-questions.md`. The `**Prerequisites:**` line from step 4.
  - `## Goals`: one numbered item per row, `**Kn.**` then what is true
    once it's fixed, in the user's words. Group under `###` batch
    headings only if there are two themes.
  - `## Not in scope`: the candidates left out and why (waiting on #n, too
    large, another batch), so the next run doesn't re-plan them.
  - `## Decisions (and why)`: for each row, why the fix is the right one,
    usually "makes the code do what spec §x already says". Name any
    question the owner decided in step 3.
  - `## Tasks`: `### N.M.0 Start of phase` (read the logs, CLAUDE.md §12),
    then one `- [ ]` per row naming the class or template and the
    regression test, then `### N.M.k Finish`: rows *Fixed*, CHANGELOG,
    spec §13, ROADMAP, merge review, merge. A `### Release` section
    (VERSION, CHANGELOG, README status, tag) only if it releases.
  - `## Acceptance criteria`: each code row has a regression test that
    fails without its fix; `composer lint`, `composer analyse` and
    `bin/test-all-dbs.sh` pass on all four engines; `MarkdownLinksTest`
    passes; no migration; new strings in every catalogue in
    `translations/`.
  - `## Open questions`: the release question and any from step 3, each
    *Decided YYYY-MM-DD:* with the option chosen and the options not
    chosen, or *Needs a decision*.
- **`ROADMAP.md`**: the table row `| [N.M](docs/phases/phase-N.M.md) | <title> | 📋 |`
  in its slot, and a `## Phase N.M — <title>` section in the same place
  among the sections (an italic summary line, two or three bullets of
  what changes with the K-numbers, `→ [phase-N.M.md](docs/phases/phase-N.M.md)`,
  and `---` separators either side, as 52.2's).
- **`spec.md` §13**: a `- **Phase N.M — <title>** (planned).` entry in
  its place in the phase list, one sentence per row naming the spec
  section it touches and the K-number, ending
  `No migration. See [phase-N.M.md](docs/phases/phase-N.M.md).` If the
  owner decided a question that changes behaviour, update that spec
  section too (CLAUDE.md §12: spec first).
- **`docs/phases/known-issues.md`**: each chosen row's status becomes
  `Scheduled (Phase N.M)` (with `, after #n` if it waits on a question
  decided in step 3). A row found already fixed in step 2 becomes
  `Fixed (…)` with the commit or phase. Leave every other column alone.
- **`docs/phases/open-questions.md`**: one row per new question, in the
  table's format, with the next free number. Find it by searching the
  whole repository for the highest `#n`, not by reading the table's last
  row: a question can be cited elsewhere first (K81 cites #492, while the
  table's last row was #488).

  ```bash
  grep -rhoE '#[0-9]{3}\b' docs/phases spec.md | sort -t'#' -k2 -n | tail -1
  ```

  Update the log's intro paragraph if the questions were decided, in the
  style of the entries already there.

New K-numbers aren't made here. A new problem found while reading the
code is recorded with `/issue-sweep` (or a row in known-issues.md under a
`## Found while planning Phase N.M (date)` heading if it is plainly
real), and left out of the batch unless the owner adds it.

## 6. Check

```bash
vendor/bin/phpunit --filter MarkdownLinksTest
git diff --stat
```

Every link in the new phase file, ROADMAP and spec resolves; the diff
touches only the files in step 5. Read the phase file once more against
52.2's: same headings, same tone, no row without a test task.

## 7. Commit and PR (ask first)

Show the owner the batch, the slot and number, and `git diff --stat`, and
ask before committing. Committing, pushing and opening a PR are
outward-facing. On their yes, stage the files by name (never
`git add -A`: the owner keeps private files untracked in the repo root):

```bash
git add docs/phases/phase-N.M.md ROADMAP.md spec.md docs/phases/known-issues.md docs/phases/open-questions.md
git commit   # "Plan Phase N.M: <theme> from the known-issues log"
git push -u origin phase-N.M-plan
gh pr create -R gwpreston16/Logbook --base master --head gwpreston:phase-N.M-plan \
  --title "Plan Phase N.M: <theme> from the known-issues log" --body-file <scratchpad>/plan-N.M.md
```

The commit body, as 59b5c448's: the rows taken, the slot ("ROADMAP after
N.m"), spec §13, the questions logged, and the rows Scheduled. The commit
ends with the session's Co-Authored-By line and the PR body with its
attribution line.

## 8. Report

The rows taken and why (one line each), the ones left out and what they
wait on, the phase number and slot and why, the release decision, the
questions logged, the files changed, and the PR URL (or that it's still
uncommitted on `phase-N.M-plan`). End with: once the plan is merged,
run `/next-phase` to build it.
