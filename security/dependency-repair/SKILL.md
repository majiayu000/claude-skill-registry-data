---
name: dependency-repair
description: >-
  Repairs a product's main gone red by itself — a dependency audit reading advisories published after
  the last green run — on a branch off main, and merges it once the suite is green. It runs the
  audit the product's NFDR names and answers every advisory by the rules development-security uses: an
  allowed fix (a bump to the fixed release, a renamed identifier, a major bump only with the suite
  green), an exception for an advisory the product does not reach (in the product's exception record,
  with a row in the instance upkeep register), and a question for the owner where the only fix is
  forbidden. It writes a committed report whose first line says merged, unmerged or stopped, or
  closes with nothing-to-repair when main is not red from its audit. Halts outside a senior-engineer
  session or the senior-engineer subagent.
when_to_use: >-
  Use when a product's main is red with no commit behind it and the cause is its dependency audit —
  "main went red by itself", "repair main", "the audit turned main red", "fix the advisories on main",
  "dependency-repair". Do not use on a change's branch (development-security reviews that), for a red
  a commit made (that is the change's own), for holes in the code, or to decide what to do with what
  the repair leaves (the PM's).
license: MIT
metadata:
  author: Eyal Golan
  version: "1.0.0"
  created: "2026-10-24"
  category: execution
  tags: dependencies, advisories, repair, main, senior-engineer
  risk: safe
---

# Dependency Repair

## Purpose

A product's `main` can turn red with nobody committing to it: its dependency audit reads advisories
published after the last green run. This skill repairs that red on a branch off `main`, under the
owner's rules, and merges the branch once the suite is green.

**The rules are not here.** Which audit runs, the rules a repair is held to, the one answer each
advisory takes, the exception record, its window and the upkeep row, and how a forbidden move waits
for the end are `<CORE>/prompts/senior_engineer_repair_dependencies.md` — the same file
`development-security` reads for its dependency half. Read it in full before Step 3 and apply it. This
file owns only the run: the posture gate, the branch, the suite call, the report, the merge and the
commits.

**Announce at start:** "I'm using the dependency-repair skill to repair `main`'s dependency audit on a
branch off `main`."

## Posture

**Senior Engineer only.** Run in a `senior-engineer:` session or as the `senior-engineer` subagent.
Invoked from anywhere else, halt at once, say the posture is wrong, and name the way in. The seat's
contract is `<CORE>/roles/loaders/senior_engineer_global.md`. The gate is here because the run commits
and merges into `main` with nobody answering
(`<CORE>/doctrine/setup/authoring_layers.md` § *A skill that acts unattended gates to its seat*).

## Input

**The project** — `system/projects/<project>/`. Everything else is resolved from it.

**A relaunch** names the last report, `system/projects/<project>/docs/dependency-repair/<key>_report.md`,
and carries **the owner's answers**, each naming the question it answers in that report's § *Why the
run stopped*: the move allowed, or declined. Read the report first.

- **After `stopped`** the allowed repairs are already on `main`: open a fresh branch (Step 1) and
  answer only the questions.
- **After `unmerged`** the allowed repairs are only on that report's branch: continue on it — skip
  Step 1's branch, resolve its worktrees with the `development_path.py` call, and go to Step 3 with the
  questions answered — so the repairs reach `main` with the rest.

## The work, in order

### 1. Open the repair's branch

The key is `<YYYY-MM-DD>_dependency-repair`, today's date; where a branch of that name already exists in
the instance or the product's repository, add `-2`, `-3` and so on until none does. Open it with the
command the chain uses for a change:

```sh
python3 "<CORE>/tools/create_change_worktree.py" \
  --instance "$(git rev-parse --show-toplevel)" --project <project> --key <key>
```

It cuts branch `<key>` from `main`'s `HEAD` and makes the instance worktree, and a second worktree in
the product's own repository when it has one, then runs the card's `Setup command:` there. A non-zero
exit is a stop: report its `error`, `message`, `changed` and `repos` as printed. Then resolve the path
contract from the instance worktree:

```sh
python3 "<CORE>/tools/development_path.py" resolve --format json \
  --worktree "<instance worktree>" --project <project> --key <key>
```

Its `code_worktree` holds the product's code and its `pipeline_worktree` the instance's files; for a
product inside the instance they are one. Read the product's `docs/nfdr.md` from the `code_worktree`. A
product with no NFDR names no audit.

**Never run the product's code in its main checkout** — every command below runs in the worktrees
(`<CORE>/roles/CROSS_ROLE.md` § *Every seat — a run leaves the product's main checkout as it found it*).

### 2. Check that `main` is red, and that the red is its audit's

The branch is `main` as it stands. **The red is the audit's** — the red this skill exists for is the
audit reporting advisories, whether or not the product's suite runs the audit. Run the audit the shared
file's § *The audit command is the product's, not yours* names, in the `code_worktree`, and keep its
output. **No audit named, an audit that cannot run, or no advisory it has not already answered** — an
exception within its window is answered — → there is no red of the audit's.

Then there is nothing this skill repairs: nothing has been committed, so remove the worktrees
and delete branch `<key>` (Step 6's clean-up), write no report, and say in the closing message
`nothing-to-repair` and which case it was. Otherwise go on.

### 3. Answer every advisory

Apply `<CORE>/prompts/senior_engineer_repair_dependencies.md` to every advisory, in its order — except
an advisory the owner's answer on a relaunch settles: **allowed** → take that move, the owner's answer
lifting the rule that forbade it for that move only, and note the answer in the report; **declined** →
report it for the PM. Make
the fixes and the exceptions in the `code_worktree`, and each exception's upkeep row in
`system/upkeep.md` in the `pipeline_worktree`. A forbidden move is noted as a question and the run
carries on. Commit the changes in the `code_worktree` (§ *Commit*, the `dependencies` row).

### 4. Run the suite, and go back for a major bump it turns red

Run the suite (§ *The suite*). **Green, for this skill,** is the suite passing, or failing only where
the product's own audit check reports an advisory this run left as a question for the owner or for the
PM, or one excepted in a record the audit does not read — those are the report's, not a reason to hold
back the repairs. Where it is red past that and a major bump is the cause — a failure other than the
audit's that came with the bump — undo that bump, commit the
undo (the `dependencies` row again), and answer that advisory again from the shared file's next answer
down — as an advisory with no allowed fix — then run the suite again. Re-run the audit once the suite
settles, and keep that output.

### 5. Decide the outcome, write the report and commit it

The outcome is decided now, before anything merges, the first that applies:

- **`unmerged`** — the suite is red, as Step 4 judges it;
- **`stopped`** — the suite is green and the report lists a question for the owner; the allowed repairs
  still merge in Step 6, since they already help `main`;
- **`merged`** — the suite is green and nothing is asked.

Write `system/projects/<project>/docs/dependency-repair/<key>_report.md` in the `pipeline_worktree`
(§ *The report*) with that verdict, and commit it with the upkeep rows (§ *Commit*, the `report` row).
On `unmerged` stop here: the branch and its worktrees stay for the owner, and the report on it says
what is still red.

### 6. Merge, then clean up

On `merged` or `stopped`, merge branch `<key>` into `main` in each repository that committed on it,
through the builder — **the product's repository first, the instance last**, so the report lands only
once the code it describes has. `<repository>` is that repository's **main working tree**, standing on
`main` (the first entry `git -C <any worktree> worktree list` prints), because the merge runs there:

```sh
python3 "<CORE>/tools/commit_builder.py" --repo "<repository>" merge \
  --branch <key> --target-branch main \
  --description "dependency-repair — <what was fixed and excepted, in a phrase>" \
  --branch-commits <each line of: git -C <repository> log main..<key> --oneline> \
  --actor senior-engineer \
  --merge-context "dependency-repair <key> (suite green)" \
  --surface "<surface>" --co-authored-by "<runtime identity>"
```

A merge the builder refuses stops the run there: leave every branch and worktree as it is, and say in
the closing message which repository merged and which did not.

**Clean-up.** In each repository, once `git -C <repository> merge-base --is-ancestor <key> main`
holds there — or, from Step 2, when nothing was committed — remove the worktree
(`git -C <repository> worktree remove <worktree>`) and delete the branch, naming the SHA it was checked
at (`git -C <repository> branch -d <key>`, after confirming `git rev-parse <key>` is that SHA).

## The suite

Run it through the gate tool, never by hand: read `<CORE>/prompts/gate_suite.md`, build its evidence
file, and issue

```sh
python3 "<CORE>/tools/gate_suite.py" run \
  --worktree "<instance worktree>" --project "<project>" --key "<key>" \
  --gate code-integrity --inputs "<inputs file>" \
  > "<output file>" 2> "<error file>"
```

as `development-security` does — the tool has no gate of this skill's own, and a gate other than `seal`
changes nothing about how the suite runs. Copy each `Environment:` line it printed into the report as a
bullet.

## The report

Its reader is the owner, or the PM when nobody is watching. Use exactly this shape:

```markdown
# Dependency repair — <project>, <key>

Repair: <unmerged | stopped | merged>

## Why the run stopped
<one question per forbidden move — the advisory, the move it needs, the record that forbids it, and
what would be done if allowed. Otherwise: none.>

## Left for the PM
<every advisory left unfixed and unexcepted, each exception under the default window ("default window
used — raise it into the NFDR"), each exception the audit does not read ("wire the audit to honor the
exception record"), a red suite on an unmerged branch. Otherwise: none.>

## Dependency audit
<the command, cited to the NFDR line that names it, where it ran, and what it reported before and
after the repairs; or why it did not run, or that the NFDR names none.>

## Advisories
| Advisory | Dependency | Answer | What was done | Commit |
|---|---|---|---|---|
<one row per advisory: fixed · excepted · question for the owner · reported for the PM; an existing
exception that holds is a row too. "none" when the audit reported none.>

## Exceptions and upkeep rows
<each exception written, renewed or removed: the record and entry, its reason, its window and lapse
date, whether the audit reads the record, and the upkeep row. "record created", "default window used"
and "register created" where they apply. Otherwise: none.>

## Suite
<the verdict the gate tool gave on the repaired branch, and its `Environment:` bullets. A major bump
undone on a red run is named here.>

## Not checked
<everything the run could not cover and why. Otherwise: none.>
```

**The verdict line is bare**, the first line after the title, lower-case: `unmerged`, `stopped` or
`merged`, decided in Step 5. `nothing-to-repair` writes no report; it is said in the closing message.

## Commit

Through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply its
variables: **`--actor senior-engineer`**, `--skill dependency-repair`, and the directional resolved as
that file says. Never hand-write `git commit` or a trailer.

| Commit | Lands in | Carries |
|---|---|---|
| `dependency-repair: <key> — dependencies` | `code_worktree` | the lockfile and pin bumps, the renamed identifiers, and the exception record's entries (or the record created). Only when Step 3 changed anything; again for each major bump Step 4 undoes |
| `dependency-repair: <key> — report` | `pipeline_worktree` | the report and the `system/upkeep.md` rows (or the register created). Every run that reaches Step 5 |

All commit on branch `<key>`, never on `main`; Step 6's merge carries them there.

## Critical rules

- **The rules are the shared file's**, applied as `development-security` applies them; nothing about
  answering an advisory is decided here.
- **Only a red that is the audit's.** No audit, or no advisory left to answer, is
  `nothing-to-repair`, and leaves no branch behind.
- **Merge only on a green suite**, product repository first, through the builder, as
  `senior-engineer`.
- **Never take a forbidden move** the owner has not allowed — gather every one, do all allowed work,
  then stop once.
- **Never run the product's code in its main checkout.**
- **Write and commit the report before the merge**, with the verdict Step 5 decided, on every run that
  reaches Step 5.
