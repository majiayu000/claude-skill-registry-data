---
name: lead-merge
description: Method for the long-running lead who merges many patch or lane branches into one integration branch from a queue, with one gate for each batch and a merge log. Use for a merge queue.
---

# Lead merge

The **lead** is one long-running agent (`shark:lead-engineer`). It merges the patch branches of the
`shark:patch-fanout` skill (or the lane branches of a round) into `<integration branch>`. It owns the merged
result. A patch report is a claim; the diff and the tests are the facts. `<scratch>` is the session scratch
folder, outside the repository.

The `shark:lead-engineer` agent definition gives the jobs of a single round merge. This skill adds the rules for a
lead that runs for hours, from a queue, while patches still arrive. The audit engineer (`shark:merge-audit`)
reviews each merge in parallel, read-only.

```
operator ─► queue.md ─► lead: read-ahead ─► merge batch (3-4) ─► one combined check ─► merge-log.md ─► report
                                                                                          │
                                                     merge-audit (read-only) ◄────────────┘ ─► fix specs ─► operator ─► queue.md
```

## Project values

| Section of `AGENTS.md` (or `CLAUDE.md`) | Used for |
| --- | --- |
| `## Commands` › `setup`, `test-db:copy` | The integration worktree and its test database |
| `## Commands` › `gate:fast`, `gate:scoped <paths>` | The combined check of each batch |
| `## Commands` › `gate:full`, `bench` | The costly runs at validation, once each, with the owner's OK |
| `## Invariants`, `## Architecture rules` | What the read-ahead and each resolution keep |
| `## Test scope` | Which test folders a batch must run |
| `## Owner rules` | Pushes, long checks, approvals |

If a section is missing, ask the user once. Suggest adding it to `AGENTS.md`.

## The contract comes first

Before parallel lanes start, the operator writes a **round contract** (`shark:operator`, contract step). It
holds:

- each shared name, with its one owner file;
- every writer and reader of each new or changed event or field;
- the invariants and the owner decisions to keep;
- each rule to delete, with its callers and its new owner;
- the lane boundaries.

The lead checks each merge against the contract. A lane that decided a shared thing alone is a
finding: log it, and ask the operator.

## Files

| File | Content | Writer |
| --- | --- | --- |
| `<scratch>/port/queue.md` | State, rules, batches (template: `references/queue-template.md`) | operator |
| `<scratch>/port/merge-log.md` | One row and one entry for each merge (template: `references/merge-log-template.md`) | lead |
| `<scratch>/port/notes/<UNIT>.md` | The patch notes (`shark:patch-fanout`) | patch agents |
| `<scratch>/port/review-log.md` | The findings of the audit engineer (`shark:merge-audit`) | audit engineer |

The templates are in `references/` in this skill folder (`${CLAUDE_PLUGIN_ROOT}/skills/lead-merge/references/`).

## The queue file is the source of truth

The lead can lose its context in a long run (a full disk, a compaction, a restart). Thus:

1. The operator writes each batch into `queue.md` before the lead merges it.
2. The lead writes each merge, conflict resolution and check result into `merge-log.md` at once.
3. **At a restart**, read `queue.md` and the end of `merge-log.md`. Check the integration head with
   `git log -1`. Continue from the first unit that the log does not show as merged.
4. Never keep state only in the conversation.

## First job: the integration branch

1. Make the integration worktree from the refactor head: `git worktree add <path> -b <integration branch> <sha>`.
2. Run the project's `setup` in it. If the tests need a database, run the project's `test-db:copy`. Never build a
   test database from zero.
3. Merge the commits that only production has (the `shark:port-audit` Step 0 list) with `--no-ff`.
4. Run the project's `gate:scoped` on the touched folders. Report the head sha. The operator gives this sha to the
   first wave of patch agents.

## Each batch

Merge in batches of 3 to 4 units. Merge the units of one conflict group in the order of the queue.

1. **Read ahead.** Before the batch, read the diffs of the queued units (`git diff <integration head>...pu/<U>`):
   - a duplicate name: a constant or a rule that already has an owner. Import the owner; add the name to the
     one-definition list of the architecture test, if the project has one;
   - a layer break: an import across the project's `## Architecture rules` (for example an evaluation or
     test-support module imported by production code);
   - file damage from a shell write: stray lines, duplicated blocks, CR line ends, a missing end newline.

   Write each finding into the merge log as a merge item for that unit.
2. **Merge each unit** with `git merge --no-ff pu/<UNIT>`.
3. **Resolve each conflict from the notes of both sides.** Read `notes/<UNIT>.md` of the new unit and of each
   unit that wrote the other side. Keep every invariant of both. Typical resolutions:
   - two new fields of one record: keep both; fields with no default come before fields with a default;
   - two appended test blocks: keep both;
   - two wiring arguments of one builder: pass both.
4. **Log each resolution**: file, function, what each side kept, and the invariants that you checked.
5. **Do the merge items** of the queue (a fix that the operator or the audit asked for). Test first. Make each
   lead fix its own commit (`shark:commit-blocks`).
6. **One combined check for the batch** (see "Checks").
7. **A unit that breaks a test you cannot fix in 10 minutes:** undo its merge with `git revert -m 1 <merge sha>`.
   Put the unit back in the queue with the failure, and report it.
8. **Remove each merged worktree** (`git worktree remove <path>`). Use `--force` only when the queue names the
   extra files as known leftovers (AGENTS.md › Working rules §4). Keep the branch. Remove the test database of the worktree too.
9. **Report** after each batch (see "Report").

## Checks

Lanes check only their own files. The lead runs the folders once for each batch. The fast path comes before any
costly run; the costly runs come last, once each.

- For each batch, do one run: the project's `gate:fast` (lint, format, types, unit, smoke; 5 minutes at most).
  Then the project's `gate:scoped` with the test folders of the touched modules and the architecture tests (the
  project's `## Test scope`).
- Wrap each test run in a timeout (for example `timeout 600`). Run at most 2 test runs at the same time.
- Run long commands as background tasks and wait for the notice. Never write a wait loop.
- A check that can run longer than 10 minutes needs the owner's OK each time (the project's `## Owner rules`).
  Examples: the bench, the full integration suite, the full gate.
- Test-runner pitfall: a call with a test folder and a file inside that folder can collect only the file (pytest
  does this). Give folders and files in separate calls, or give only folders. Parallel test workers (for example
  pytest-xdist) can build new test databases from zero: turn them off, or give each worker a copy of the template.

**Snapshot tests.** A **snapshot test** compares the recorded output of fixed replays with a stored file. Do not
re-record the snapshot for each batch. Instead:

1. Run a read-only script that groups the differences by field and by kind ("new field" or "changed").
2. Map each group to the patch note that predicts it ("<count> × `<field>: new` = <UNIT>").
3. Write the map into the merge log. A difference that no note predicts is a finding: stop and check it.
4. Re-record once, at validation, with the full map.

**Pinned hashes.** A test can pin a hash of a generated text, for example a prompt hash, or a contract hash
between two services. It fails by design when a unit changes that text. Log it as "fails by design after <UNIT>".
Recompute the hash once, at validation. A contract hash between two services changes on both sides, byte-identical.

## Validation (the operator says "validate")

1. Run the full fast path once: all test folders, the architecture tests, lint, format, the whole-repo type
   checker. Use the project's `gate:fast`, then `gate:scoped` on all folders; `gate:full` needs the owner's OK.
2. Review every snapshot difference against the merge-log map. Re-record once. Commit the new snapshot with the
   map in the commit body.
3. Recompute each pinned hash once. Commit it.
4. Fast-forward the target branch to the integration head (`git merge --ff-only`), only when every check is green.
5. Push only when the user asks, or when an owner rule allows a push of that branch (fast-forward, never force,
   never `--no-verify`).
6. Report. The operator then runs the project's `bench` (if it has one), with the owner's OK when it is longer
   than 10 minutes.

## Hard rules

- Edit files only with the Edit or Write tool.
- Never `git stash`, `--no-verify`, a force push, a rebase of a patch branch, or `git branch -D` without a check
  that each commit of the branch is on the target (`git branch --merged`, or `git cherry <target> <branch>` with no
  `+` line for a branch that landed by cherry-pick).
- Never merge into the production branch or the default branch without the owner's OK. Never push without a
  request or an owner rule for that branch.
- Do not invent a business rule. A case that the spec, the decisions and the code do not decide goes to the
  operator as a question, with your recommendation.
- Never decide a shared name alone: the round contract owns it. Stop and ask the operator.
- Fix items from the audit engineer come through the operator. Treat each one as the next patch.
- Never read an env file (the project's `## Secrets`).

## Report (after each batch, short, outcome first, ASD-STE100)

- The integration head sha, and the units merged.
- For each conflict: file, function, the resolution, the invariants kept.
- The lead fixes (sha, test first).
- The check results: counts, failures, time.
- The snapshot map: total differences, new ones in this batch, any difference with no note.
- The worktrees and test databases removed and kept.
- The blocker table (test, cause `file:line`, evidence). Empty if none.
- The follow-up items for the operator (for example "F-<UNIT>: <behaviour>").
- The full path of `merge-log.md`.

## Lessons

- **A full disk can stop the lead in the middle of a run.** The queue and the merge log let the restart continue
  at the next unit with no rework.
- **Read-ahead finds the cheap defects first.** A copied name or an evaluation import in production code shows in
  the queued diff. A fix before the merge costs less than a fix after it.
- **A re-recorded snapshot hides the evidence.** With one record at the end, each difference has a note that
  explains it, also when there are more than 1000 differences.
- **A flaky test hides a real failure.** Prove a known flake on the base branch once, and log it in the blocker
  table with that evidence.
- **A running worker keeps old code in memory.** Restart the local workers and servers before a migration or a
  check that uses the new code.
