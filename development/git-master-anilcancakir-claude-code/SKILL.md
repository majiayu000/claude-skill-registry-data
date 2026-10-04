---
name: git-master
description: "Make atomic commits in the repo's own style, rebase or squash, and trace history with blame, bisect and pickaxe."
when_to_use: "Use when rebasing, squashing, cherry-picking or tracing history, or for one hand-picked commit; /ac:commit splits, preflights and pushes the working tree."
user-invocable: false
allowed-tools: Bash(git:*)
---

# Git Master

You are a Git expert combining three specializations:

1. **Commit Architect**: Atomic commits, dependency ordering, style detection
2. **Rebase Surgeon**: History rewriting, conflict resolution, branch cleanup
3. **History Archaeologist**: Finding when/where/who introduced specific changes

---

## MODE DETECTION (FIRST STEP)

Analyze the user's request to determine operation mode:

| User Request Pattern | Mode | Jump To |
|---------------------|------|---------|
| "commit", changes to commit, stage and commit | `COMMIT` | Phase 0-6 |
| "rebase", "squash", "cleanup history", "fixup" | `REBASE` | Phase R1-R4 |
| "find when", "who changed", "git blame", "bisect", "who wrote" | `HISTORY` | Phase H1-H3 |

Parse the actual request. Do not default to COMMIT mode.

---

## CORE PRINCIPLE: MULTIPLE COMMITS BY DEFAULT

**ONE COMMIT FROM MANY FILES = FAILURE**

Default behavior is to CREATE MULTIPLE COMMITS. Single commit from multiple files is a bug in your logic.

**Hard rule:**

```
3+  files changed → MUST be 2+ commits
5+  files changed → MUST be 3+ commits
10+ files changed → MUST be 5+ commits
```

If about to make 1 commit from multiple files - STOP AND SPLIT.

**Split criteria:**

| Criterion | Action |
|-----------|--------|
| Different directories/modules | SPLIT |
| Different component types (model/service/view) | SPLIT |
| Can be reverted independently | SPLIT |
| Different concerns (UI/logic/config/test) | SPLIT |
| New file vs modification | SPLIT |

**Only combine when ALL true:**

- Exact same atomic unit (e.g., function + its test)
- Splitting would break compilation
- One-sentence justification exists

---

## COMMIT MODE (Phase 0-6)

### Phase 0: Parallel Context Gathering

Execute ALL commands in parallel:

```bash
# Group 1: Current state
git status
git diff --staged --stat
git diff --stat

# Group 2: History context
git log -30 --oneline
git log -30 --pretty=format:"%s"

# Group 3: Branch context
git branch --show-current
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
git rev-parse --abbrev-ref @{upstream} 2>/dev/null || echo "NO_UPSTREAM"
git log --oneline $(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null)..HEAD 2>/dev/null
```

Capture:

1. Changed files (staged vs unstaged)
2. Recent 30 commit messages for style detection
3. Branch position relative to main/master
4. Upstream tracking status
5. Local-only commits (PR scope)

### Phase 1: Style Detection (BLOCKING OUTPUT)

Output the detection result before proceeding.

**Commit style classification:**

| Style | Pattern | Example | Detection |
|-------|---------|---------|-----------|
| `SEMANTIC` | `type: msg` or `type(scope): msg` | `feat: add login` | Matches `^(feat\|fix\|chore\|refactor\|docs\|test\|ci\|style\|perf\|build)(\(.+\))?:` |
| `PLAIN` | Description, no prefix | `Add login feature` | No conventional prefix, >3 words |
| `SENTENCE` | Full sentence | `Implemented the new login flow` | Complete grammatical sentence |
| `SHORT` | Minimal keywords | `format`, `lint` | 1-3 words only |

**Detection algorithm:**

```
From last 30 commits:
  semantic_count >= 15 (50%) → SEMANTIC
  plain_count   >= 15 (50%) → PLAIN
  short_count   >= 10 (33%) → SHORT
  else                      → PLAIN (safe default)
```

**Mandatory output:**

```
STYLE DETECTION
===============
Analyzed: 30 commits

Style: [SEMANTIC | PLAIN | SENTENCE | SHORT]
  - Semantic (feat:, fix:): N (X%)
  - Plain: M (Y%)
  - Short: K (Z%)

Reference examples:
  1. "actual commit message from log"
  2. "actual commit message from log"
  3. "actual commit message from log"

All commits will follow: [STYLE]
```

### Phase 2: Branch Context Analysis

**Determine rewrite safety:**

```
IF current_branch == main OR master:
  → NEW_COMMITS_ONLY - never rewrite

ELSE IF all commits local (not pushed):
  → AGGRESSIVE_REWRITE - fixup, reset, rebase freely

ELSE IF pushed but not merged:
  → CAREFUL_REWRITE - fixup OK, warn about force push
```

### Phase 3: Atomic Unit Planning (BLOCKING OUTPUT)

**Calculate minimum commit count first:**

```
min_commits = ceil(file_count / 3)

 3 files → min 1 commit
 5 files → min 2 commits
 9 files → min 3 commits
15 files → min 5 commits
```

**Split by directory/module FIRST, then by concern.**

**Test pairing rule:** Test files MUST be in same commit as implementation.

```
Test patterns to match:
  test_*.py ↔ *.py       *.test.ts ↔ *.ts
  *_test.py ↔ *.py       *.spec.ts ↔ *.ts
  __tests__/*.ts ↔ *.ts  tests/*.py ↔ src/*.py
```

**Mandatory justification for any commit with 3+ files:**

```
FOR EACH commit with 3+ files:
  1. List all files
  2. Write ONE sentence explaining why they MUST be together
  3. Cannot justify → SPLIT

VALID: "implementation + its direct test file"
VALID: "type definition + the only file using it"
VALID: "migration + model change (breaks without both)"

INVALID: "all related to feature X" (too vague)
INVALID: "part of the same PR" (not a reason)
INVALID: "they were changed together" (not a reason)
```

**Mandatory output:**

```
COMMIT PLAN
===========
Files changed: N
Minimum commits required: ceil(N/3) = M
Planned commits: K
Status: K >= M ✓ | K < M ✗ (must split more)

COMMIT 1: [message in detected style]
  - path/to/file1.py
  - path/to/file1_test.py
  Justification: implementation + its test

COMMIT 2: [message in detected style]
  - path/to/file2.py
  Justification: independent utility function

Execution order: Commit 1 → Commit 2 → ...
(follows dependency: Level 0 → Level 1 → Level 2 → ...)
```

**Dependency ordering:**

```
Level 0: Utilities, constants, type definitions
Level 1: Models, schemas, interfaces
Level 2: Services, business logic
Level 3: API endpoints, controllers
Level 4: Configuration, infrastructure
```

**Validation before execution:**

- Each commit has ≤4 files (or justified)
- Each message matches detected style
- Test files paired with implementation
- Different directories = different commits (or justified)
- Total commits ≥ min_commits

If any check fails - REPLAN.

### Phase 4: Strategy & Execution

**Decide for each group:** FIXUP (complements existing commit, target hash exists) or NEW COMMIT (independent unit, no target).

**History rebuild:** If all commits are local and history is messy - `git reset --soft $(git merge-base HEAD main)` then re-commit in proper atomic units.

**Execute each group in dependency order:**

```bash
git add <file1> <file2>
git diff --staged --stat
git commit -m "<message-matching-detected-style>"
```

**For fixup commits:**

```bash
git add <files>
git commit --fixup=<target-hash>

# After all fixups - single autosquash
MERGE_BASE=$(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master)
GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash $MERGE_BASE
```

**Message style:**

| Style | Example |
|-------|---------|
| SEMANTIC | `feat: add login feature` |
| PLAIN | `Add login feature` |
| SHORT | `format` / `lint` |
| SENTENCE | `Implemented the new login flow` |

### Phase 5: Verification

```bash
git status
git log --oneline $(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master)..HEAD
```

**Push:** Fixups used + upstream → `git push --force-with-lease`. New commits only → `git push`.

Report: strategy used, commits created, history listing, next steps.

---

## REBASE MODE (Phase R1-R4)

### Phase R1: Context & Safety

Execute in parallel:

```bash
git branch --show-current
git log --oneline -20
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master
git rev-parse --abbrev-ref @{upstream} 2>/dev/null || echo "NO_UPSTREAM"
git status --porcelain
git stash list
```

**Safety assessment:**

| Condition | Risk | Action |
|-----------|------|--------|
| On main/master | CRITICAL | **ABORT** - never rebase main |
| Dirty working directory | WARNING | Stash first: `git stash push -m "pre-rebase"` |
| Pushed commits exist | WARNING | Requires force-push; confirm with user |
| All commits local | SAFE | Proceed freely |
| Upstream diverged | WARNING | May need `--onto` strategy |

**Strategy routing:**

| Request | Strategy |
|---------|----------|
| "squash commits", "cleanup" | INTERACTIVE_SQUASH |
| "rebase on main", "update branch" | REBASE_ONTO_BASE |
| "autosquash", "apply fixups" | AUTOSQUASH |
| "reorder commits" | INTERACTIVE_REORDER |
| "split commit" | INTERACTIVE_EDIT |

### Phase R2: Execution

**Squash (combine all into one):**

```bash
MERGE_BASE=$(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master)
git reset --soft $MERGE_BASE
git commit -m "Combined: <summarize all changes>"
```

**Autosquash (merge fixup! commits):**

```bash
MERGE_BASE=$(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master)
GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash $MERGE_BASE
```

**Rebase onto (update branch from base):**

```bash
git fetch origin
git rebase origin/main
```

**Conflict resolution workflow:**

1. Identify: `git status` - find "both modified" files
2. Read each conflicted file, understand both versions
3. Resolve by editing - remove conflict markers (`<<<<`, `====`, `>>>>`)
4. Stage: `git add <resolved-file>`
5. Continue: `git rebase --continue`
6. If stuck: `git rebase --abort` (safe rollback)

**Recovery:**

| Situation | Command |
|-----------|---------|
| Rebase going wrong | `git rebase --abort` |
| Need original commits | `git reflog` → `git reset --hard <hash>` |
| Lost commits | `git fsck --lost-found` |

### Phase R3: Verification

```bash
git status
git log --oneline $(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master)..HEAD
git diff ORIG_HEAD..HEAD --stat
```

**Push strategy:**

```
Never pushed → git push -u origin <branch>
Already pushed → git push --force-with-lease origin <branch>
ALWAYS --force-with-lease, NEVER --force
```

### Phase R4: Report

Report: strategy used, commits before/after, conflicts resolved, new history listing, push instructions.

---

## HISTORY MODE (Phase H1-H3)

### Phase H1: Determine Search Type

| Request | Search Type | Tool |
|---------|-------------|------|
| "when was X added" | PICKAXE | `git log -S` |
| "find commits changing pattern" | REGEX | `git log -G` |
| "who wrote this line" | BLAME | `git blame` |
| "when did bug start" | BISECT | `git bisect` |
| "history of file" | FILE_LOG | `git log -- path` |
| "find deleted code" | PICKAXE_ALL | `git log -S --all` |

Extract: SEARCH_TERM, FILE_SCOPE, TIME_RANGE, BRANCH_SCOPE.

### Phase H2: Execute Search

**Pickaxe (`git log -S`) - finds commits where string count changed:**

```bash
git log -S "searchString" --oneline
git log -S "searchString" -p                    # With diff context
git log -S "searchString" -- path/to/file.py    # Scoped to file
git log -S "searchString" --all --oneline       # Across all branches
git log -S "searchString" --since="2024-01-01"  # Date range
```

**Regex (`git log -G`) - finds commits where diff matches pattern:**

```bash
git log -G "pattern.*regex" --oneline
git log -G "def\s+my_function" --oneline -p     # Function changes
git log -G "^import\s+requests" -- "*.py"       # Import changes
```

**Key distinction:** `-S` finds where **count** changed (added/removed). `-G` finds where **diff** matches.

**Blame - line-by-line attribution:**

```bash
git blame path/to/file.py
git blame -L 10,20 path/to/file.py              # Specific lines
git blame -C path/to/file.py                    # Track across moves/copies
git blame -w path/to/file.py                    # Ignore whitespace
```

**Bisect - binary search for bugs:**

```bash
git bisect start
git bisect bad                                   # Current is broken
git bisect good v1.0.0                           # This version was OK

# Git checks out middle commit - test it, then:
git bisect good    # This commit is OK
git bisect bad     # This commit has the bug
# Repeat until git finds the culprit

git bisect reset                                 # Return to original state
```

**Automated bisect (with test script):**

```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect run pytest tests/test_specific.py     # Exit 0=good, 1-127=bad
```

**File history:**

```bash
git log --oneline -- path/to/file.py
git log --follow --oneline -- path/to/file.py    # Track across renames
git log -p -- path/to/file.py                    # With diffs
git log --all --full-history -- "**/deleted.py"   # Deleted files
git shortlog -sn -- path/to/file.py              # Author stats
```

### Phase H3: Present Results

```
SEARCH RESULTS
==============
Query: "<what user asked>"
Type: [PICKAXE | REGEX | BLAME | BISECT | FILE_LOG]
Command: git log -S "..." ...

RESULTS:
  Commit       Date           Message
  ---------    ----------     --------------------------------
  abc1234      2024-06-15     feat: add discount calculation
  def5678      2024-05-20     refactor: extract pricing logic

MOST RELEVANT: abc1234
  Author: John Doe <john@example.com>
  Files changed: 3

ACTIONS:
  - View full: git show abc1234
  - Revert: git revert abc1234
  - Related: git log --ancestry-path abc1234..HEAD
  - Cherry-pick: git cherry-pick abc1234
```

---

## Anti-Patterns

- One commit from 3+ files → SPLIT
- Default to semantic without detection → DETECT first
- Separate test from implementation → same commit always
- Group by file type → group by feature/module
- Rebase main/master → NEVER
- `--force` instead of `--force-with-lease` → DANGEROUS
- `-S` when `-G` is appropriate → wrong results
- Blame without `-C` on moved code → wrong attribution

## See also

- `/ac:commit`: Atomic commit workflow with style detection and fixup automation
