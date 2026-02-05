---
name: plan-incremental-commits
description: Review a mixed working tree and produce (and optionally execute) a small, logically grouped sequence of incremental git commits.
---

# Plan Incremental Commits

## When to use

Use this skill when:
- The working tree contains multiple unrelated edits (docs, scripts, content, config).
- You want a readable `git log` where each commit captures one intent.
- You want commits that are easy to revert, cherry-pick, and review.

**Keywords:** git, commits, commit plan, staging, review, history hygiene

## Inputs

Required:
- None (assumes you are already in the target git repo)

Optional:
- `commit_message_style` (string): e.g., `imperative`, `conventional-commits`
- `grouping_preference` (string): e.g., `by-intent` (default), `by-folder`, `by-feature`
- `execute` (boolean): if true, the agent creates commits after approval (default: false)

## Outputs

This skill produces:
1. A commit plan: ordered commits with intent + file list
2. For each commit: a suggested message + explicit `git add …` command
3. If `execute=true` and the user approves: the commits created, ending with a clean working tree

## Procedure

### 1. Snapshot repo state

Collect:
- `git status -uall`
- `git diff --stat`
- `git diff`
- `git log -n 20 --oneline --decorate`

If there are many changes, drill in with targeted diffs:
- `git diff -- path/to/file`

### 2. Cluster changes by intent

Partition files into small clusters where each cluster answers a single “why”:
- Spec/schema change (defines new rules)
- Mechanical migration (applies new rules; no semantic change)
- New capability/tooling (scripts, skills)
- Templates/config (supports workflow; low-risk)
- Content additions (new notes, new distilled items)
- Metadata normalization (front matter, formatting)
- Scratchpad/backlog updates (AR-style notes)

Avoid mixing unrelated intents even if they are small.

### 3. Order commits dependency-first

Prefer this ordering so history reads naturally:
1. Rules/spec first (docs that define conventions)
2. Mechanical migrations second (apply conventions)
3. New tooling/capabilities (scripts/skills)
4. Templates/config that support usage
5. Metadata-only normalization (if truly mechanical)
6. Content expansions and then new content batches

If a later commit depends on an earlier change, place it after the dependency.

### 4. Run quick consistency checks

Before committing, check for “paper cuts” introduced by migrations or edits:
- Internal links inadvertently removed
- Typos in paths/filenames
- Broken references caused by schema changes
- Accidental deletions of useful sections

If a small fix is required:
- Keep it minimal and scoped.
- Apply it in the commit where it belongs (so history reflects reality).

### 5. Propose the commit plan

For each commit, provide:
- Commit intent (1 line)
- Files included
- Suggested commit message
- Explicit staging command, e.g. `git add path/a path/b`

At this point, stop and ask the user for confirmation before creating commits.

### 6. Execute commits (only if requested and approved)

If `execute=true` and the user approves:
- Stage and commit each group in order.
- After each commit: `git status -uall` should show remaining planned changes.
- At the end: `git status -uall` should be clean.

## Examples

### Example: Mixed docs + scripts + content

Typical plan shape:
1. Update schema/docs (defines conventions)
2. Migrate existing files to new schema (mechanical)
3. Add new script/tooling
4. Add templates/config
5. Normalize metadata across notes
6. Add new content batches (split by type if large)

## Edge cases

- **Untracked files:** confirm they are intended to be committed (not generated artifacts).
- **Large refactors:** propose splitting into mechanical-only vs semantic commits.
- **One file contains two intents:** use partial staging (`git add -p`) or split the edit (only if the user wants that level of hygiene).

## References

- Commit message guidance: https://cbea.ms/git-commit/
- Pro Git (staging/commits): https://git-scm.com/book/en/v2
