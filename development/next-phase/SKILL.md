---
name: next-phase
description: Work out which Logbook phase is next (resume a 🚧 one, else the first 📋 row in ROADMAP.md whose prerequisites are met), clear its open questions with the owner, build it on a phase branch to CLAUDE.md's definition of done, open the PR into gwpreston16/Logbook and turn on autofix for it. Run with /next-phase, optionally naming the phase.
disable-model-invocation: true
argument-hint: "[phase number, e.g. 34.1 — optional, worked out from ROADMAP.md if left out]"
---

# Build the next phase

A phase is one row of the status table in `ROADMAP.md`, with its task list
in `docs/phases/phase-N.M.md` and its summary in `spec.md` §13. Phases are
built in table order, one branch and one PR each. Read `CLAUDE.md` (all of
it, especially §11 and §12) before step 3.

The upstream repository is **gwpreston16/Logbook**; `origin` is the fork
(gwpreston/Logbook) and `upstream` is gwpreston16. Pass
`-R gwpreston16/Logbook` to every `gh` command, and open PRs with
`--head gwpreston:<branch>`, even if something else names the fork.

`$ARGUMENTS` may name the phase. If it does, still run the checks in step 2
on it; stop and say why if it fails them.

## 1. Sync

```bash
git status --porcelain                 # must be empty; stop otherwise
git fetch upstream --tags && git fetch origin
git switch master && git merge --ff-only upstream/master
```

Local master is often behind: new phase files arrive through PRs merged on
gwpreston16. Never read the ROADMAP before this step.

## 2. Pick the phase

```bash
grep -n '^| \[' ROADMAP.md
ls docs/phases/
gh pr list -R gwpreston16/Logbook --state open
git branch -a --list '*phase-*'
```

Key off the phase **number** in the first column, not its link (some rows
link `phase-N.M.md` without the `docs/phases/` prefix).

1. **Resume first.** A row marked 🚧, an open PR from a `phase-*` branch, or
   a `phase-N.M` branch with commits not on `upstream/master` means a phase
   is under way. Carry it on (switch to its branch, read its phase file's
   ticks and `git log upstream/master..` to see where it stands). Never
   start a second branch for a phase. If its PR is open and only waiting for
   review or CI, say so and stop: there's nothing to build.
2. **Otherwise** take the first 📋 row in table order.
3. **Prerequisites:** the phase file's `**Prerequisites:**` line must be met
   (the named phases ✅ and merged into `upstream/master`; a release named
   there tagged, `git tag -l vX.Y.Z`). If not, report what is missing and
   stop.
4. **The phase file must exist.** If `docs/phases/phase-N.M.md` is missing,
   no code is written (CLAUDE.md §12). Tell the owner, offer to draft the
   file from the ROADMAP row, the spec §13 entry and the neighbouring phase
   files (in their style: goal, scope, spec additions, decisions, tasks,
   acceptance criteria, open questions), and wait for them to approve it.

Tell the user which phase you picked and why in one or two lines before
going on.

## 3. Open questions (a hard stop)

Follow CLAUDE.md §12 exactly. Read `docs/phases/open-questions.md`, then the
*Open questions* of this phase file and of every earlier phase file.

- Already answered by the spec, code or tests: record that in the log (and
  the phase file) with where.
- Still open and would change behaviour, data, UI or configuration: **ask
  the owner** with `AskUserQuestion`, giving the options and a
  recommendation. Batch them (up to four per call). Don't build anything
  the answer touches until they reply. Never guess an answer.
- Questions you find while reading the phase or the code get the next
  number in the log and the same treatment ("found while starting it").
- Once decided: `spec.md` first, then the phase file (*Decided*, date,
  decision) and the log row, and the log's intro paragraph, in the style
  of the entries already there.

Commit this as the first commit on the branch (step 4).

## 4. Branch and spec first

```bash
git switch -c phase-N.M          # from master at upstream/master
```

- The phase file's `N.M.0 Spec first` task: `spec.md` sections and §13,
  `ROADMAP.md` row 🚧 and the phase file status `🚧 in progress`.
- Commit: `Phase N.M: the owner's answers (#a–#b) and the spec first` (or
  `Phase N.M: spec first` with no questions).

## 5. Build

Work through the phase file's tasks in order, following CLAUDE.md §5–§10
and the conventions in the existing code.

- One commit per task or coherent step, message
  `Phase N.M: <what changed, in the user's words> (N.M.k)`, ending with the
  session's Co-Authored-By line. Tick the task in the phase file as it lands.
- Tests with every step (CLAUDE.md §11.2: ≥ 80% of changed `src/` lines
  covered). New user-facing strings go in **every** catalogue in
  `translations/`. Rebuild assets if a source asset changed, and commit the
  built ones.
- Migrations: Phinx, portable, and `migrate`, `rollback`, `migrate` clean
  on every engine.
- UI changes: check them in the browser (the `run` skill or
  `bin/dev-setup.sh`) at 375, 768 and 1280 px, light and dark, with JS off
  for core flows, and at a subpath. Record a design review in the phase
  file as 33.x did, and fix HIGH and MEDIUM items.
- Sample data: if the phase file has a *Sample data* task, extend the seeds.
- Anything the phase file doesn't decide goes to step 3, not into the code.
- Avoid variable-length lookbehinds in regexes: CI's PCRE2 is older than the
  local one and rejects them.

## 6. Done before the PR

All of CLAUDE.md §11, checked, not assumed:

```bash
composer lint && composer analyse && composer test
composer test:coverage && composer coverage:check
```

- The suite on **SQLite, PostgreSQL, MySQL and MariaDB** with
  `bin/test-all-dbs.sh` (migrate → full rollback → migrate → PHPUnit on
  each; needs Docker). Note any engine you couldn't run, and why.
- A subpath test for new pages or links.
- If `.claude/skills/review/SKILL.md` exists, run that review on the branch
  and fix what it finds before opening the PR.

Then the phase's own bookkeeping, in the style of the last phases
(`git show --stat` on their final commits):

- **Phase file:** every task ticked except a `Tag vX.Y.Z once merged.`
  item; status `✅ complete` with `no release of its own (ships with …)` or
  `releases **vX.Y.Z**`, as its title says. Open questions decided or
  carried into the log.
- **ROADMAP.md:** the row ✅.
- **A phase that releases** (its title ends `+ vX.Y release`): the
  `CHANGELOG.md` section for every phase the release covers (under an empty
  `## [Unreleased]`, no compare links yet; `/release` adds them), `VERSION`,
  the README status line (the version only), the new features in
  `docs/features.md`, docs guides (each listed in `docs/README.md`), and
  the screenshots re-made if a page they show changed. Copy the last release's
  house style (`git show v<last> --stat`, its CHANGELOG section).
- **A phase that doesn't release:** no `VERSION` or README bump. Follow how
  33.1–33.3 recorded their changes before 33.4 released them.

Commit: `Phase N.M: phase complete; roadmap` (or similar).

## 7. Open the PR

```bash
git push -u origin phase-N.M
gh pr create -R gwpreston16/Logbook --base master --head gwpreston:phase-N.M \
  --title "Phase N.M: <title from the ROADMAP row>" --body-file <scratchpad>/pr-N.M.md
```

The body follows PR #63: one opening line with the phase file and the
decisions' numbers in the log; `## What changes` as user-facing bullets;
`## Checks` with test counts per engine, lint, PHPStan, coverage and the
floor, the design review and the subpath test; for a releasing phase
`After merge: tag vX.Y.Z with /release.` It ends with the session's PR
attribution line.

Tell the owner it must be merged as a merge commit or fast-forward (not a
squash) so `/release` can tag the phase's commits.

## 8. Turn on autofix

Autofix is Claude Code's built-in **`/autofix-pr`** command: a cloud
session watches the PR and pushes fixes for failing CI and review comments.
It is an interactive command, so this skill can't run it; the user types
it. Set things up so it finds the PR first:

1. Stay on the `phase-N.M` branch: autofix reads the PR from the current
   branch and refuses to run on `master`.
2. Point `gh` at upstream, since the PR lives there and not on the fork:
   ```bash
   gh repo set-default --view          # if it isn't gwpreston16/Logbook:
   gh repo set-default gwpreston16/Logbook
   gh pr view --json number,url,state  # must print this phase's open PR
   ```
3. Make sure nothing is left unpushed (`git status -sb` shows no `ahead`).
4. Ask the user to run, in this session:
   ```
   /autofix-pr
   ```
   Any text after it is passed to the cloud session as extra instructions
   (e.g. `/autofix-pr follow CLAUDE.md; never squash; keep every engine
   green`).

If it fails, the message says why. The usual causes: the session isn't
signed in to claude.ai or isn't interactive, the PR carries the PR Steward
label (remove it on GitHub and retry), or an earlier autofix session is
still running on the PR (`/autofix-pr stop` ends this session's polling).

## 9. Report

The phase built and why it was next, the decisions taken (with log
numbers), the PR URL, the checks and their results per engine, anything
skipped or carried over, and whether autofix is on or still waiting for the
user's `/autofix-pr`. For a releasing phase, remind them that `/release`
tags it once merged. Say plainly if any step was skipped or failed.
