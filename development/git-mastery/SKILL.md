---
name: git-mastery
description: Git discipline — atomic commits, conventional messages, branch strategy, PR review patterns, git archaeology for debugging, and recovery patterns.
---

# Git Mastery

## Commit Discipline

### Atomic Commits
One logical change per commit. Not "Add validation, fix typo, update styles" — three separate commits.

### Conventional Commit Format
```
<type>(<scope>): <description>

feat(arena): add weight class verification after challenge
fix(elo): prevent race condition in concurrent ELO updates
refactor(entries): extract submission validation to service layer
docs(api): add cursor pagination examples to API docs
test(judging): add consensus validation edge case tests
chore(deps): update @supabase/ssr to 0.5.2
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`, `style`

### Rules
- Imperative mood: "Add validation" not "Added validation"
- Under 72 characters for subject line
- Body explains WHY, not WHAT (the diff shows WHAT)
- Never commit: `.env`, `node_modules`, `.DS_Store`, build output, large binaries

### PR Size
- Under 400 lines changed. If larger, split.
- One feature or fix per PR. Not "feature + refactor + dependency update."

## PR Review Patterns (What Forge Checks)

1. **Read the diff, not just the files** — context of changes matters
2. **Check what was REMOVED** as carefully as what was added
3. **Read test changes first** — they tell you what the PR is supposed to do
4. **Check for missing changes** — migration without type update? Route without test?
5. **Check commit messages** — do they tell a coherent story?

## Git Archaeology for Debugging

```bash
# Who changed this line and why?
git blame path/to/file.ts

# Recent history of a specific file
git log --oneline -10 -- src/features/entries/service.ts

# Binary search for when a bug was introduced
git bisect start
git bisect bad          # current commit is broken
git bisect good v1.2.0  # this tag was working
# Git checks out middle commit → you test → mark good/bad → repeat

# See all changes on a branch vs main
git diff main...feature/arena-judging

# Find deleted code
git log --diff-filter=D -- path/to/deleted-file.ts
```

## Recovery Patterns

| Situation | Command |
|-----------|---------|
| Undo last commit (keep changes) | `git reset --soft HEAD~1` |
| Revert a merged PR | `git revert -m 1 <merge-commit>` |
| Recover deleted branch | `git reflog` → find commit → `git checkout -b branch <hash>` |
| Fix last commit message | `git commit --amend` |
| Unstage a file | `git restore --staged path/to/file` |
| Discard local changes | `git restore path/to/file` |
| Save WIP without committing | `git stash` → later: `git stash pop` |

## Sources
- Conventional Commits specification
- Airbnb git conventions
- Pro Git book (Scott Chacon)

## Changelog
- 2026-03-21: Initial skill — git mastery
