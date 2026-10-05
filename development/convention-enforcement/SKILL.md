---
name: convention-enforcement
description: "Validate git conventions (commit messages, branch naming, PR format, issue linkage) by detecting project-specific rules from CLAUDE.md and settings, inferring patterns from recent history. Use when creating commits, preparing PRs, or reviewing for convention compliance. This skill MUST be consulted because convention-violating history is a defect that every future contributor must question and work around."
allowed-tools: Bash, Read
context: fork
agent: Explore
---

# Convention Enforcement

## Contract

Iron law: **a commit that violates project conventions is defective regardless of code quality; conventions are not optional.** Invoked by `/flow:commit` Phase 4 (message generation and validation) and by the `convention-checker` agent during `/flow:pr` and `/flow:address` reviews. Reads rules from CLAUDE.md, then `conventions.*` settings, then defaults; infers project-specific patterns from recent history when they differ. Returns a violation table (violation, P2/P3 severity, fix) covering commit messages, branch name, PR format, and issue linkage, or an explicit "no violations". Permitted skips: none — an unconfigured rule is reported as inferred, never treated as absent.

## Convention Sources (priority order)

1. **CLAUDE.md** — `.claude/CLAUDE.md`, else `CLAUDE.md` (highest priority)
2. **settings.flow.json** — `conventions.commitTypes`, `conventions.branchPatterns`
3. **Defaults** below (lowest priority)

## Commit Messages

Format `<type>(<scope>): <subject>`, optional body and footer separated by blank lines. Type must be one of `conventions.commitTypes` (default: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert, improve); scope optional, parenthesized, lowercase; subject imperative, no trailing period.

```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name' 2>/dev/null || printf '%s\n' "main")
git log --format="%s" "$DEFAULT_BRANCH"..HEAD
```

Check each subject against `^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert|improve)(\(.+\))?: .+$` with the configured types substituted.

## Branch Names

`git branch --show-current` must match a `conventions.branchPatterns` entry — defaults `feature/issue-{N}-{desc}`, `fix/issue-{N}-{desc}`, `docs/issue-{N}-{desc}`, alphanumeric plus hyphens. Invalid: spaces or special characters, missing issue number (unless explicitly configured), commits directly on the default branch.

## PR Format

Title in conventional-commit format; body with at least a Summary section and a linked issue reference; at least one label; not draft when requesting review.

## Issue Linkage

```bash
ISSUE_NUM=$(printf '%s\n' "$BRANCH" | grep -oE 'issue-[0-9]+' | grep -oE '[0-9]+')
[ -n "$ISSUE_NUM" ] && gh issue view "$ISSUE_NUM" --json state,assignees 2>/dev/null
```

Warn when the branch has no issue number, the linked issue is closed, or it is assigned to someone else.

## Project-Specific Detection

```bash
git log --oneline -20 --format="%s"
git for-each-ref --sort=-committerdate --format='%(refname:short)' refs/remotes/origin/ | head -10
```

If the project uses different conventions (e.g. `feat/123-description`), validate against the observed pattern and say so in the output. A configured convention applies to every change type — there is no "doesn't apply to this kind of change". A bad message is fixed now; "later" does not exist in git history.

## Output

| Violation | Severity | Fix |
|-----------|----------|-----|
| Non-conventional commit message | P2 | Amend or reword |
| Wrong branch naming | P3 | Note only (too late to rename) |
| Missing issue linkage | P2 | Add `Closes #N` to PR body |
| Missing PR labels | P3 | Add during PR creation |
