---
name: commit
description: Commit ONLY the changes this session made, never another agent's work in the same checkout. With a message argument, makes one commit; with no argument, splits the session's work into the fewest self-contained commits and generates a short feat/fix/chore message for each. Use when the user says "commit", "commit this", "commit my changes", "commit just my/this session's changes", or invokes commit — especially when multiple agents share one working tree.
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Commit (session-scoped)

Commit the changes **this session** made — and nothing else. Multiple agents may
share one checkout; a plain `git add -A` / `git add .` would sweep in another
session's work. This skill stages by explicit path, and at hunk granularity when
a file was touched by more than one session.

## Usage

```
/commit                       # split this session's work into logical commits, auto-message each
/commit "fix: correct pager"  # one commit, using this message verbatim
```

An argument is always the message for a **single** commit — never split when one
is given. With no argument, group into the fewest self-contained commits (Step 3).

## Instructions

### Step 1: Reconstruct what THIS session changed
Build the set of paths you edited this session from **your own actions** — the
`Write`, `Edit`, `NotebookEdit`, and file-creating `Bash` calls you ran. This is
the source of truth for ownership, not the working tree.

- List every file you created, modified, renamed, or deleted this session.
- If the conversation was summarized and you're unsure, reconstruct from the
  summary + visible history. If you still can't tell which changes are yours,
  do NOT guess wide — jump to Troubleshooting → "Unsure which changes are mine".

### Step 2: See the working-tree state
Run these (read-only) to compare your list against reality:
```
git status --porcelain
git diff --stat            # unstaged
git diff --cached --stat   # anything already staged
```
Anything changed in the tree that is NOT in your Step-1 list belongs to another
session (or the user) — leave it alone.

If files are already staged that you did NOT edit, unstage them first so your
commit stays clean: `git restore --staged <their-file>`.

### Step 3: Group your changes into commits
**Argument given** → one group containing everything from Step 1. Skip to Step 4.

**Blank** → partition your files into the **fewest** groups such that each group
is one self-contained unit of work. Read your own diff (`git diff <your paths>`)
if the split isn't obvious from the file list.

Keep in the **same** commit:
- a feature and its tests, docs, config, types, and follow-up fixes
- a refactor and the call-site updates it forced
- a generated file and the source that generated it
- anything that leaves the repo broken, or the change half-explained, if the
  other part landed without it

Split into **separate** commits only when two changes are genuinely independent:
either could have been made without the other, and neither explains the other —
e.g. a new feature in module A alongside an unrelated typo fix in module B.

Rules of thumb:
- **Never split by change type.** `feat` + its docs + its tests + its connected
  chores is ONE commit, not four. Type is the wrong axis to cut on.
- **Bias to fewer.** One commit is the common, correct answer. Two or three is
  normal for a session that did unrelated things. If you land on more than
  three, you're over-splitting — merge the marginal groups back.
- **Group at file granularity.** If one file's changes belong to two groups,
  don't hunk-split for grouping — merge those groups into one. (Hunk-level
  staging in Step 4 is only for excluding *another session's* work.)
- **Order by dependency.** If one group's code needs another's, commit that one
  first, so every commit leaves the tree in a working state.

Then run Steps 4–6 once per group, in order. Do not ask for confirmation of the
grouping — just commit and report the result (Step 6).

### Step 4: Stage only your changes
Stage only the paths in the group you're currently committing. For each such
path, decide file-level vs hunk-level:

- **File only you touched** (its entire current diff is your work) → stage whole:
  ```
  git add <path>              # modified or new
  git rm <path>              # you deleted it
  ```
  New files you created and untracked → `git add <path>`.

- **File you AND another session touched** (its diff contains hunks you didn't
  write) → stage surgically with the helper so foreign hunks stay unstaged:
  ```
  python3 scripts/stage-hunks.py <path> --list      # numbered hunks
  python3 scripts/stage-hunks.py <path> 1 3 4       # stage only yours
  ```
  Identify "yours" by matching each hunk to an edit you actually made. When in
  doubt about a hunk, exclude it — under-committing is recoverable, committing
  someone else's half-finished work is not.

Verify before committing: `git diff --cached` should show this group's changes
and only those — nothing from another session, nothing from a later group.

### Step 5: Message
- **Argument given** → use it verbatim as the subject.
- **Blank** → generate a short subject for this group following the user's
  commit policy:
  - Type is one of `feat` (user-noticeable addition), `fix` (something broken now
    works), or `chore` (everything else). No scopes/parentheses.
  - Format: `type: short description`, lowercase, imperative, no trailing period.
  - Body: omit it, or one short sentence of *what* — never why/how, no essays.
  - If a group's subject needs an "and" to cover it, the grouping was too coarse;
    if two groups would get near-identical subjects, it was too fine.

### Step 6: Commit and report (silently)
Commit the staged changes, then move to the next group (back to Step 4) — don't
ask for confirmation first (unless Troubleshooting sent you to confirm
ownership):
```
git commit -m "feat: add commit skill"
```
Once every group is committed, report one line per commit — files + message:
```
Committed 3 files as "feat: add commit skill".
Committed 1 file as "chore: bump lefthook to 1.14".
(Left src/api.ts from another session untouched.)
```

If a pre-commit hook fails, fix the reported problem and retry — never
`--no-verify`. If a hook reformats your staged files, re-stage them (Step 4) and
commit again.

### What NOT to do
- Never `git add -A`, `git add .`, `git add -u`, or `git commit -a`.
- Never stage or commit a file you didn't edit this session.
- Never `git push` (harness-blocked; not this skill's job).
- Never split one logical change across commits by type (code / tests / docs /
  chore), or leave a commit that only makes sense together with the next one.
- Never make more than one commit when a message argument was given.

## Examples

### Example 1: message given, clean ownership
User: `commit "fix: correct off-by-one in pager"`
Actions:
1. This session edited `src/pager.ts` only.
2. `git status` shows `src/pager.ts` modified plus `src/api.ts` modified — api.ts
   isn't mine, leave it.
3. `git add src/pager.ts`; `git diff --cached` confirms only my change.
4. `git commit -m "fix: correct off-by-one in pager"`.
Result: `Committed 1 file as "fix: correct off-by-one in pager" (left src/api.ts from another session untouched).`

### Example 2: blank message, shared file, one logical change
User: `commit`
Actions:
1. This session added a helper in `utils.ts` and created `helper.ts` +
   `helper.test.ts`, and documented it in `README.md`. Another session also
   changed `utils.ts` (added a different function).
2. Grouping: helper + its test + its README entry are one unit → 1 commit.
3. `git add helper.ts helper.test.ts README.md`. For `utils.ts`:
   `stage-hunks.py utils.ts --list` shows 2 hunks; hunk 1 is mine, hunk 2 is
   theirs → `stage-hunks.py utils.ts 1`.
4. `git diff --cached` shows my files + only my utils.ts hunk.
5. No argument → generate `feat: add slugify helper`.
6. `git commit -m "feat: add slugify helper"`.
Result: `Committed 4 files as "feat: add slugify helper" (staged only my hunk of utils.ts).`

### Example 3: blank message, two unrelated changes
User: `commit`
Actions:
1. This session did two things: added CSV export (`export.ts`, `export.test.ts`,
   `docs/export.md`, a new dep in `package.json`), and separately fixed a stale
   path in the unrelated `scripts/deploy.sh`.
2. Grouping: export work is one unit — code, test, docs and the dep it needs all
   land together, NOT as four commits. The deploy fix is independent of it → 2
   groups total.
3. Group 1: `git add export.ts export.test.ts docs/export.md package.json`;
   `git commit -m "feat: add CSV export"`.
4. Group 2: `git add scripts/deploy.sh`;
   `git commit -m "fix: correct build path in deploy script"`.
Result:
```
Committed 4 files as "feat: add CSV export".
Committed 1 file as "fix: correct build path in deploy script".
```

## Troubleshooting

### Unsure which changes are mine
**Cause:** Context was summarized, or the tree has changes you can't attribute.
**Solution:** Do not commit wide. List the specific files/hunks you believe are
yours, state which you're unsure about, and ask the user to confirm before
committing. Safety overrides the silent-commit default here.

### Can't tell whether two changes belong in one commit
**Cause:** The changes are related but not obviously one unit.
**Solution:** Default to one commit. A slightly-too-broad commit is a normal
commit; a too-narrow one leaves history with entries that don't stand alone. If
they're genuinely unrelated, the subject line test settles it — if you can't
write one short subject covering both without "and", split.

### `stage-hunks.py` reports "git apply --cached failed"
**Cause:** The working tree shifted between listing and staging, or the hunk
context moved.
**Solution:** Re-run `stage-hunks.py <file> --list` to get fresh hunk numbers,
then retry. If a hunk still won't apply cleanly, stage that file whole only if
its entire diff is yours; otherwise report the conflict to the user.

### Nothing to commit after staging
**Cause:** Your edits were already committed, or another session committed them.
**Solution:** `git log --oneline -5` and `git status` to confirm. If your work is
already in history, say so — don't create an empty commit.

### Pre-commit hook keeps failing
**Cause:** Lint/format/type errors in the staged (or repo-wide) code.
**Solution:** Read all reported errors and fix them (per the repo's Test & Lint
policy — never skip with `--no-verify`), re-stage, and commit again.
