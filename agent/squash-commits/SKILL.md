---
name: squash-commits
description: Squash unpushed commits into clean, higher-level feat/fix/chore commits that follow the project commit policy. Use when local history has too many small/WIP/fixup commits (common after superhuman or gsd runs), or the user says "squash commits", "squash my commits", "tidy history", "clean up commits", "combine commits before pushing".
argument-hint: '[--conservative] [base-ref]'
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Squash Commits

Combine the unpushed commits on the current branch into the smallest set of clean,
self-contained commits, each adhering to the commit policy (`feat`/`fix`/`chore`,
**no scopes**, subject only). Superhuman/gsd-style runs leave many superfluous
commits — initial work, follow-up fixes, tests, docs — that belong together as one
higher-level feature commit.

This skill rewrites history, so it **proposes a plan and only proceeds after the user
confirms**. It never touches the branch ref until the very last step, and only ever
operates on **unpushed** commits. It creates no backup tags or stashes; the original tip
is recoverable from the branch reflog after the verified ref move.

## Usage

```
/squash-commits                  # aggressive feature-level grouping of unpushed commits
/squash-commits --conservative   # only fold obvious WIP/fixup commits into their parent
/squash-commits origin/main      # use an explicit base instead of auto-detecting unpushed range
```

## Hard rules

- **Never rewrite pushed commits.** Only squash commits not present on any remote.
- **Never reorder commits.** Groups are contiguous runs in original order. Each new
  commit is the snapshot at its group's last commit, so a non-contiguous group would
  silently absorb every commit between its members.
- **The final tree must be byte-identical** to the original tip before the branch is
  moved. Squashing changes *history*, never *content*. Verify this and abort if it differs.
- **Require a clean working tree.** If there are uncommitted changes, stop without
  creating a stash. Let the user decide how to preserve their work before re-running.
- **No interactive rebase.** `git rebase -i` is unsupported in this harness. Use the
  rebuild method below.
- **Leave no persistent helper state.** Do not create backup tags, branches, or stashes.
- **Leave no temporary files.** Use subject-only commit messages, so no message files are
  needed. Git's normal reflog and unreachable-object retention are not helper state and
  can be left to normal expiry/GC.

## Workflow

### Step 1: Preconditions

```bash
git status --porcelain      # MUST be empty — else stop without changing Git state
git rev-parse --abbrev-ref HEAD   # current branch (save as BRANCH)
```

If the working tree is dirty, stop: "Working tree has uncommitted changes. Preserve or
commit them as you prefer, then re-run `/squash-commits`. This skill did not create a
stash or change the working tree."

### Step 2: Determine the unpushed range

Find the commits to squash and the base (the commit they sit on top of).

- **If a base ref is passed as an argument** (e.g. `origin/main`, a SHA): `BASE` = that ref.
  Range = `BASE..HEAD`.
- **Otherwise auto-detect unpushed commits:**
  ```bash
  git rev-list HEAD --not --remotes --oneline
  ```
  This lists commits reachable from HEAD that are on no remote-tracking branch (newest
  first). The oldest of these is the last line; `BASE` = its parent (`<oldest>^`).
  - If the list is **empty** → nothing to squash. Tell the user and stop.
  - If it includes the **root commit** (no parent), or there are **no remotes at all**,
    auto-detection is unreliable — ask the user for an explicit base ref (e.g.
    `origin/main`) and re-run, or confirm a base before continuing.

Save `ORIG_TIP = git rev-parse HEAD`.

**Check for merge commits** in the range:
```bash
git rev-list --merges BASE..HEAD
```
If non-empty, stop: this skill only handles linear history. Tell the user the range
contains merge commits and squashing them is out of scope.

If the range has **0 or 1 commit**, there is nothing to combine — say so and stop.

### Step 3: Read and analyze the commits

List the range oldest→newest and read what each commit does:
```bash
git log --reverse --format='%h %s' BASE..HEAD
git log --reverse --stat BASE..HEAD     # add -p for full diffs if grouping is unclear
```

For each commit note: its subject, the files it touches, and whether it's substantive
work, a fixup of an earlier commit, tests, or docs.

### Step 4: Propose a grouping plan

Partition the commits into **contiguous groups**, each becoming one new commit.

**Default (aggressive, feature-level):** collapse adjacent commits that serve one logical
feature into a single commit — initial implementation + its follow-up fixes + its tests +
its docs become one. The goal is the smallest set of commits that each stand on their own.

**`--conservative`:** only fold obvious checkpoint/WIP/fixup commits (e.g. "wip", "fix
typo", "address review", "oops") into the substantive commit they belong to. Leave
genuinely distinct logical commits as separate groups.

For each group, write a new message per the commit policy:
- Type is exactly one of `feat` / `fix` / `chore`. **No scopes, no parentheses** — write
  `feat: add login button`, not `feat(ui): ...`.
  - `feat` — a user-noticeable addition. `fix` — a user-noticeable bug fix.
    `chore` — everything else (refactor, tests, docs, internal).
  - If a group mixes a feature and an unrelated fix, that's a sign they shouldn't be one
    group — split them.
- Omit the body. Use a single subject line so this workflow needs no temporary message
  files.

Present the plan as a before→after table and stop for confirmation:

```markdown
## Squash plan (BASE = <short-sha or ref>, <N> commits → <M> commits)

### Group 1 → `feat: <new subject>`
- `abc123` wip feat1
- `def456` fix feat1 typo
- `ghi789` add tests for feat1

### Group 2 → `feat: <new subject>`
- `jkl012` start feat2
- `mno345` fix feat2

Proceed? This rewrites unpushed history. The original tip will remain recoverable from
the branch reflog; no backup tag or stash will be left behind.
```

**Wait for explicit user confirmation.** Do not proceed otherwise. If the user wants
edits to the grouping or messages, revise and re-present.

### Step 5: Preserve the recovery point without helper refs

Do not create anything. Keep the recorded `ORIG_TIP`: the original branch still points
there until Step 7, and the branch reflog records that tip when the ref moves. This gives
the user an undo point without a backup tag, branch, stash, or temporary file.

### Step 6: Rebuild the history (commit-tree)

Determine each group's **tip** = the newest (last) original commit in that group, in order.
The last group's tip must be `ORIG_TIP`.

Build one new commit per group directly from its tip's tree, oldest group first. Each
command prints the new commit's SHA, which is the parent of the next:

```bash
git commit-tree '<group1_tip>^{tree}' -p <BASE> -m '<group1-subject>'   # prints N1
git commit-tree '<group2_tip>^{tree}' -p <N1> -m '<group2-subject>'     # prints N2
# ...one command per group; the last SHA printed is NEWTIP
```

Each new commit is exactly the snapshot at its group's tip, so nothing is merged and
nothing can conflict. Do **not** use `git merge --squash` for this: a squash merge records
no parent, so every group after the first merges against `BASE` and conflicts wherever it
edits lines an earlier group touched.

`commit-tree` touches no working tree, index, HEAD or ref; the new commits stay
unreferenced until Step 7. If a command fails, fix it and re-run from that group — there
is nothing to clean up.

Run one command per group with literal SHAs, copying each printed SHA into the next
command. Do not drive the rebuild or the checks below with a shell loop, array, or
word-split variable: zsh does not split unquoted variables, so a list of pairs arrives as
one argument.

`commit-tree` runs no commit hooks. The content already passed them, but a `commit-msg`
hook enforcing a message format does not run, so each subject must follow the commit
policy on its own.

### Step 7: Verify, then move the branch

**Verify the content is identical** before touching the branch:
```bash
git rev-parse '<ORIG_TIP>^{tree}' '<NEWTIP>^{tree}'   # MUST print the same hash twice
git log --oneline <BASE>..<NEWTIP>                     # MUST show exactly the planned subjects
```
If the tree hashes differ, the last group's tip was not `ORIG_TIP` — do **not** move the
branch. Report what diverged; the branch is untouched and nothing needs cleaning up.

If both checks pass, point the branch at the rebuilt history:
```bash
git update-ref -m 'squash-commits: <N> → <M> commits' refs/heads/<BRANCH> <NEWTIP> <ORIG_TIP>
git status --short         # should be clean
```
`update-ref` with the old value moves the branch only if it still points at `ORIG_TIP`. If
it moved since Step 2 (a new commit, a pull), it fails with `cannot lock ref … expected
<ORIG_TIP>` and changes nothing — stop and re-plan from Step 2. The working tree and index
already match `NEWTIP`'s tree, so status stays clean.

### Step 8: Report

Show the result and how to undo:
```bash
git log --oneline <BASE>..HEAD
```

```markdown
## Done — squashed <N> commits into <M>

<new oneline log>

Original tip: `<ORIG_TIP>` (retained in `<BRANCH>`'s reflog).
- Undo: `git reset --hard <ORIG_TIP>` (run it yourself — the agent does not run
  `reset --hard`).
- Cleanup: complete — no backup tag, branch, stash, or temporary message files remain.
```

Git will normally retain the replaced commits through the branch reflog until reflog
expiry and garbage collection. That is standard Git recovery history, not a leaked ref;
do not expire reflogs or run GC as part of this skill.

## Examples

### Example 1: superhuman run left 6 WIP commits

> /squash-commits

Auto-detects 6 unpushed commits via `git rev-list HEAD --not --remotes`. Reading them
shows two features: an export button (impl + 2 fixups + a test) and an unrelated config
tweak. Proposes Group 1 → `feat: add CSV export button` (5 commits) and Group 2 →
`chore: bump lint config` (1 commit, kept as-is). After confirmation, builds two commits
with `git commit-tree` from the two group tips' trees, verifies the final tree matches the
original tip, and `update-ref`s `main` onto the result — 6 commits become 2 with the
original tip retained only in the reflog.

### Example 2: conservative, only fold fixups

> /squash-commits --conservative

Range has `feat: add auth`, `fix typo`, `address review`, `refactor session store`,
`feat: add logout`. Folds `fix typo` and `address review` into `feat: add auth`; leaves
the refactor and the logout feature as their own commits. 5 commits → 3.

### Example 3: explicit base

> /squash-commits origin/develop

Skips auto-detection and squashes everything in `origin/develop..HEAD`, useful when the
branch has no upstream set or you want to bound the range to a specific integration point.

## Troubleshooting

### "Nothing to squash"

**Cause:** `git rev-list HEAD --not --remotes` is empty — all commits are already pushed,
or HEAD is at a remote-tracking branch.
**Solution:** Confirm there are local-only commits. If the branch has no upstream and no
remote contains the work, pass an explicit base: `/squash-commits origin/main`.

### Auto-detection picks up too many commits (no remotes / new repo)

**Cause:** With no remote-tracking branches, `--not --remotes` excludes nothing, so the
range walks back to the root commit.
**Solution:** Pass an explicit base ref (e.g. `/squash-commits main` or a SHA) bounding
the commits you want to squash.

### Verify step shows different tree hashes

**Cause:** The last `commit-tree` did not use `ORIG_TIP`'s tree — a group tip was
misidentified, or the plan dropped the newest commit.
**Solution:** Do not move the branch; it was never touched, so there is nothing to undo.
Re-check each group's tip against `git log --reverse --format='%h %s' BASE..HEAD` and
rebuild from Step 6.

### `update-ref` fails with "cannot lock ref"

**Cause:** The branch no longer points at `ORIG_TIP` — a commit landed or the branch was
reset after the range was read.
**Solution:** Nothing changed. Re-run from Step 2 so the plan covers the current tip.

### Range contains merge commits

**Cause:** The unpushed history isn't linear.
**Solution:** This skill is out of scope for merges. Tell the user; suggest they handle
the merges manually or rebase to a linear history first.

### User wants to undo after the squash

**Cause:** The new grouping/messages aren't what they wanted.
**Solution:** Use the `ORIG_TIP` printed in the completion report:
`git reset --hard <ORIG_TIP>` (the user runs this — the agent does not run
`reset --hard`). If the report is unavailable, inspect `git reflog <BRANCH>` and identify the tip
immediately before the squash. Then adjust the plan and re-run.

### Legacy `squash-backup-*` tags exist

**Cause:** Older versions of this skill intentionally left a backup tag after every run.
They did not create stashes.
**Solution:** Inspect them with `git tag --list 'squash-backup-*'`. Delete only tags whose
target you no longer need with `git tag -d <exact-tag-name>`. Current runs do not create
these tags.
