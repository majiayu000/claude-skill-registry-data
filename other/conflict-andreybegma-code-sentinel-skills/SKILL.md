---
name: cs-conflict
description: Resolve merge conflicts for a PR or current branch — auto-resolves obvious conflicts, interactive resolution for ambiguous ones
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Edit, AskUserQuestion
---

# PR Merge Conflict Resolver

You are a senior engineer resolving merge conflicts. Given a PR number or current branch, you detect conflicts, auto-resolve obvious ones (imports, formatting, non-overlapping additions), and interactively resolve ambiguous ones.

## Inputs

`$ARGUMENTS` — PR number (optional). If empty, uses current branch.

## Step 1: Gather Context

### 1.1: Determine branches

**If PR number given:**

```bash
gh pr view $ARGUMENTS --json headRefName,baseRefName,title,number
```

If command fails (non-zero exit code, or PR not found), output:

```
Error: Could not fetch PR #$ARGUMENTS. Verify the PR number and that `gh` is authenticated.
```

**Stop here.**

Parse JSON → `HEAD_BRANCH` = headRefName, `BASE_BRANCH` = baseRefName, `PR_TITLE` = title, `PR_NUMBER` = number.

Checkout the PR branch:

```bash
git checkout <HEAD_BRANCH>
```

If checkout fails (branch not found locally or remotely), try:

```bash
gh pr checkout $ARGUMENTS
```

If still fails, output error and **stop**.

```bash
git pull origin <HEAD_BRANCH>
```

**If no PR number:**

```bash
git branch --show-current
```

Set `HEAD_BRANCH` to current branch. If HEAD is detached, output:

```
Error: Detached HEAD state. Please checkout a branch first.
```

**Stop here.**

Detect base branch by looking up the open PR for this branch first:

```bash
gh pr list --head <HEAD_BRANCH> --state open --json number,baseRefName,title --limit 1
```

If the result is a non-empty JSON array:

- Parse → `BASE_BRANCH` = baseRefName, `PR_NUMBER` = number, `PR_TITLE` = title

If the result is empty (no open PR found), fall back to remote default branch:

```bash
git remote show origin | grep "HEAD branch"
```

If that also fails (no remote, no network), fall back:

```bash
git branch -l main master develop
```

Use the first branch that exists. If none exist, output:

```
Error: Could not detect base branch. Specify a PR number instead: /cs-conflict <PR#>
```

**Stop here.**

Set `BASE_BRANCH` to the result. If PR was not found via `gh pr list`, set `PR_NUMBER` to empty, `PR_TITLE` to empty.

### 1.2: Check working tree & save restore point

```bash
git status --porcelain
```

If output is non-empty (uncommitted changes exist):

```bash
git stash push -m "cs-conflict: auto-stash before merge"
```

Save `STASHED = true`. If stash fails, output:

```
Cannot proceed: uncommitted changes detected and stash failed.
Please commit or stash your changes manually, then re-run /cs-conflict.
```

**Stop here.**

If working tree is clean, set `STASHED = false`.

Then save restore point:

```bash
git rev-parse HEAD
```

Save the output as `RESTORE_SHA`. This is the fallback for abort.

### 1.3: Fetch and attempt merge

```bash
git fetch origin <BASE_BRANCH>
```

```bash
git merge origin/<BASE_BRANCH> --no-commit --no-ff
```

**If merge succeeds (exit code 0):** no conflicts exist.

```bash
git merge --abort
```

If `STASHED = true`:

```bash
git stash pop
```

Output:

```
## Conflict Resolution: <HEAD_BRANCH> <- <BASE_BRANCH>

No merge conflicts detected. The branch can be merged cleanly.
```

**Stop here.** Do not proceed to Step 2.

**If merge fails (exit code 1):** conflicts exist. Continue to Step 2.

## Step 2: Identify Conflicted Files

```bash
git diff --name-only --diff-filter=U
```

Save as `CONFLICT_FILES`. Output the numbered list:

```
Found N conflicted files:

1. src/services/user.service.ts
2. src/utils/helpers.ts
3. package-lock.json
```

## Step 3: Analyze & Categorize Conflicts

Read each file in `CONFLICT_FILES` using the Read tool. For each file, find all conflict regions (delimited by `<<<<<<<`, `=======`, `>>>>>>>`).

Categorize each conflict region into one of these types:

### AUTO-resolvable categories

| Category | Detection | Strategy |
|---|---|---|
| **Import ordering** | Both sides add/reorder import statements, no semantic overlap | Merge + deduplicate + sort alphabetically |
| **Formatting-only** | Diff is whitespace, semicolons, trailing commas, quote style only | Accept HEAD (ours) |
| **Non-overlapping additions** | Both sides add new code at the same location but the additions are independent (different functions, different properties, different lines) | Keep both — ours first, then theirs |
| **Deleted vs unchanged** | One side deletes code, other side keeps it unchanged (no modifications) | Accept deletion |
| **Lock files** | File is `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb`, `Gemfile.lock`, `poetry.lock`, `composer.lock` | Accept theirs to clear conflict state, then flag for regeneration |

### MANUAL-resolution categories

| Category | Detection |
|---|---|
| **Overlapping logic** | Both sides modify the same lines of functional code |
| **Structural conflict** | Changes to function signatures, class structure, type definitions that affect both sides |
| **Same insertion point** | Both sides add different functional code at the exact same location |

Build a summary for each file:

```
File: src/services/user.service.ts
  Region 1 (lines 5-12): AUTO — Import ordering (merge + deduplicate)
  Region 2 (lines 45-60): MANUAL — Overlapping logic (both sides modify validateUser)

File: package-lock.json
  AUTO — Lock file (flag for regeneration)
```

## Step 4: Present Analysis & Confirm

Output the full categorized summary as plain text:

```
## Conflict Analysis

**Auto-resolvable:** N conflicts across M files
**Manual resolution needed:** X conflicts across Y files
**Lock files:** K files (will be flagged for regeneration)

### Auto-Resolvable
1. src/utils/helpers.ts:5-12 — Import ordering (merge + deduplicate)
2. src/utils/helpers.ts:30-35 — Non-overlapping additions (keep both)
3. src/components/Button.tsx:1-8 — Formatting-only (accept ours)

### Manual Resolution Needed
4. src/services/user.service.ts:45-60 — Overlapping logic
5. src/services/user.service.ts:80-95 — Structural conflict

### Lock Files
6. package-lock.json — Regenerate after resolution
```

Then use `AskUserQuestion`:

- **question**: "How should conflicts be resolved?"
- **options** (exactly 3):

| Option | Description |
|---|---|
| **Proceed (Recommended)** | Auto-resolve obvious conflicts, then handle manual ones interactively |
| **Review each** | Review every conflict interactively, including auto-resolvable ones |
| **Abort** | Cancel merge and restore branch to original state |

If **Abort** → jump to **Abort Procedure**.

If **Review each** → treat all conflicts as MANUAL in Steps 5 and 6.

## Step 5: Auto-Resolve

Process files one at a time (skip if user chose "Review each"). For each file with AUTO conflicts:

1. Resolve ALL conflict regions in the file — apply the resolution strategy using the Edit tool for each region, removing conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) and applying the merged content
2. **Only after ALL regions in the file are resolved**, stage it:

```bash
git add <FILE_PATH>
```

**Important:** If a file has mixed regions (some AUTO + some MANUAL), do NOT stage it in Step 5. Leave it for Step 6 — resolve the remaining MANUAL regions first, then stage.

For lock files: do NOT edit textually. Clear the conflict state so they don't block the commit:

```bash
git checkout --theirs <LOCK_FILE>
```

```bash
git add <LOCK_FILE>
```

Note them for the regeneration reminder in Step 7 (regeneration will overwrite this placeholder).

After all auto-resolutions, output:

```
### Auto-Resolved
| # | File | Strategy |
|---|---|---|
| 1 | src/utils/helpers.ts:5-12 | Import ordering — merged + deduplicated |
| 2 | src/utils/helpers.ts:30-35 | Non-overlapping additions — kept both |
| 3 | src/components/Button.tsx:1-8 | Formatting-only — accepted ours |
```

If no MANUAL conflicts remain, skip to Step 7.

## Step 6: Manual Resolution

For each MANUAL conflict (or all conflicts if "Review each" was chosen):

### 6.1: Show conflict context

Display the conflict with both sides clearly labeled:

```
### File: src/services/user.service.ts (lines 45-60)
**Type:** Overlapping logic

**Ours (HEAD — <HEAD_BRANCH>):**
[code from ours side]

**Theirs (origin/<BASE_BRANCH>):**
[code from theirs side]

**Context:** [1-line explanation — e.g., "Both sides modify the validateUser function: ours adds email validation, theirs adds phone validation"]
```

### 6.2: Ask for resolution

Use `AskUserQuestion`:

- **question**: "How to resolve this conflict? (<FILE>:<LINES>)"
- **options** (exactly 4):

| Option | Description |
|---|---|
| **Ours** | Keep HEAD version (current branch) |
| **Theirs** | Keep base branch version |
| **Merge both** | Combine both changes into one |
| **Skip** | Leave unresolved for now |

**If Ours:** Edit the file to keep only the ours side, remove conflict markers.

**If Theirs:** Edit the file to keep only the theirs side, remove conflict markers.

**If Merge both:** Propose a merged version that combines both changes. Show the proposed code, then use `AskUserQuestion`:

- **question**: "Accept this merged code?"
- **options** (exactly 2):

| Option | Description |
|---|---|
| **Accept (Recommended)** | Use the proposed merged code |
| **Edit** | Describe what to change |

If **Edit**, apply the user's requested changes, show the updated code, and re-confirm with the same Accept/Edit question. Then Edit the file with the final version.

**If Skip:** Leave the conflict markers in place. Note as skipped.

### 6.3: Stage resolved files

After processing all regions for a file, check if ALL conflict regions in that file are resolved (none were Skipped). If yes:

```bash
git add <FILE_PATH>
```

If any region in the file was Skipped, do NOT stage the file — it still contains conflict markers.

After all manual resolutions, output:

```
### Manually Resolved
| # | File | Resolution |
|---|---|---|
| 4 | src/services/user.service.ts:45-60 | Merge both — combined email + phone validation |
| 5 | src/services/user.service.ts:80-95 | Theirs — accepted base branch type definition |
```

## Step 7: Finalize

### 7.1: Check remaining conflicts

```bash
git diff --name-only --diff-filter=U
```

If any files remain unresolved (were Skipped), git will NOT allow a merge commit. Handle this:

**If ALL conflicts were skipped** (nothing staged):

```
No conflicts were resolved. Aborting merge.
```

Run the Abort Procedure. **Stop here.**

**If some conflicts were skipped** (partial resolution):

```
**Warning:** N files still have unresolved conflicts:
- <file list>

Git requires ALL conflicts to be resolved for a merge commit.
```

Use `AskUserQuestion`:

- **question**: "How to handle unresolved files?"
- **options** (exactly 3):

| Option | Description |
|---|---|
| **Accept ours (Recommended)** | Keep HEAD version for all unresolved files, complete the merge |
| **Accept theirs** | Keep base branch version for all unresolved files, complete the merge |
| **Abort** | Cancel merge and restore branch to original state |

If **Abort** → run Abort Procedure.

If **Accept ours** or **Accept theirs**: for each unresolved file:

```bash
git checkout --ours <FILE_PATH>
```

or:

```bash
git checkout --theirs <FILE_PATH>
```

```bash
git add <FILE_PATH>
```

### 7.2: Lint check

Read `package.json` and extract all lint-related scripts (keys containing `lint` or `biome`, case-insensitive).

**If no lint scripts found:** skip this step entirely.

**If lint scripts found:**

Detect the package manager from lock file presence:
- `bun.lockb` → `bun run`
- `pnpm-lock.yaml` → `pnpm run`
- `yarn.lock` → `yarn`
- `package-lock.json` or fallback → `npm run`

Run each detected lint script in order:

```bash
<PM> run lint
<PM> run biome:lint
```

(Skip scripts that are clearly fix-only, e.g. `lint:fix`, `biome:fix` — run those only during auto-fix.)

**If all lint scripts pass:** continue to 7.3.

**If any lint script fails:** show the full error output, then use `AskUserQuestion`:

- **question**: "Lint errors found after conflict resolution. How to proceed?"
- **options** (exactly 3):

| Option | Description |
|---|---|
| **Auto-fix (Recommended)** | Run fix scripts (`lint:fix`, `biome:fix`, or `--fix` variant) and re-stage |
| **Commit anyway** | Ignore lint errors and commit as-is |
| **Abort** | Cancel merge and restore branch |

If **Auto-fix:**

Run available fix scripts detected from `package.json` (prefer explicit fix scripts over adding `--fix` flag):

```bash
<PM> run lint:fix       # if exists
<PM> run biome:fix      # if exists
<PM> run biome:check --fix  # fallback if biome:fix not present
```

Re-stage resolved files after auto-fix:

```bash
git add <RESOLVED_FILES>
```

If lint still fails after auto-fix, show remaining errors and continue to commit (some errors may not be auto-fixable).

If **Abort** → run Abort Procedure.

### 7.3: Show staged changes summary

```bash
git diff --cached --stat
```

Output the result.

### 7.4: Suggest commit message

Do NOT run `git commit`. Output the suggested commit command for the user to run manually:

```
### Ready to commit

All conflicts resolved and staged. Run this to commit:

```bash
git commit -m "Resolve merge conflicts: <HEAD_BRANCH> <- origin/<BASE_BRANCH>"
```
```

**Important:** Do NOT add `Co-Authored-By`, `Signed-off-by`, or any AI/Claude attribution to commits.

### 7.5: Restore stash

If `STASHED = true`:

```bash
git stash pop
```

If stash pop fails (conflicts with merged result), output:

```
Warning: Could not restore stashed changes automatically. Run `git stash pop` manually and resolve.
```

### 7.6: Lock file reminder

If any lock files were in the conflict list, output a reminder to regenerate each one with the appropriate install command for its package manager, then commit separately.

## Step 8: Output

```
## Conflict Resolution: <HEAD_BRANCH> <- <BASE_BRANCH>
**PR:** #<PR_NUMBER> — <PR_TITLE>

### Auto-Resolved (N)
| # | File | Strategy |
|---|---|---|
| ... | ... | ... |

### Manually Resolved (M)
| # | File | Resolution |
|---|---|---|
| ... | ... | ... |

### Skipped (K)
| # | File | Reason |
|---|---|---|
| ... | ... | ... |

### Lock Files (regenerate with install command)
- [lock file list]

### Next step
```bash
git commit -m "Resolve merge conflicts: <HEAD_BRANCH> <- origin/<BASE_BRANCH>"
```
```

If no PR number was given, omit the `**PR:**` line.

## Abort Procedure

When abort is triggered (user chooses Abort, or an error occurs):

1. Try clean abort:

```bash
git merge --abort
```

2. If `git merge --abort` fails, fall back to hard reset:

```bash
git reset --hard <RESTORE_SHA>
```

3. Verify restoration:

```bash
git rev-parse HEAD
```

Confirm the SHA matches `RESTORE_SHA`.

4. If `STASHED = true`, restore the stash:

```bash
git stash pop
```

Output:

```
Merge aborted. Branch restored to original state (<RESTORE_SHA>).
```

If stash was restored, add: `Stashed changes have been restored.`

## Important

- **Interactive only** — conflict resolution is inherently risky, no auto-only variant exists
- **Never force-push** — if push fails, report the error and stop
- **No AI attribution** — no `Co-Authored-By` or `Signed-off-by` in commits
