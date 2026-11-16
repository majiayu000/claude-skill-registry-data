---
name: git-lessons
description: "Use when the user asks about past bugs, recurring mistakes, what went wrong before, or wants to avoid repeating errors. Extracts lessons from git history without needing L3 memory. Examples: 'What bugs have we fixed before?', 'Have we hit this error before?', 'What patterns keep breaking?'"
---

# Git Lessons Skill

Extract actionable lessons from git history — specifically `fix:` commits — without needing L3 memory infrastructure. `git log` is L3.

## When to use this skill

- User asks "have we seen this error before?"
- You're about to change something that has been fixed before
- User wants a "lessons learned" summary for a module or area
- Before touching a historically buggy area — understand what kept breaking

## Workflow

### Step 1 — Extract fix commits

```bash
# All fix commits (last 6 months by default)
git log --grep="^fix:" --oneline --after="6 months ago"

# Fix commits touching a specific file or dir
git log --grep="^fix:" --oneline -- path/to/file

# Fix commits for a specific area (free-text search)
git log --grep="fix.*auth\|fix.*token\|fix.*deploy" --oneline -i
```

### Step 2 — Read the diff for significant fixes

```bash
# Full diff for a specific fix commit
git show <commit-hash>

# Just the files changed
git show <commit-hash> --name-only
```

### Step 3 — Identify patterns

Group fix commits by:
- **Area**: which directory/module keeps getting fixes?
- **Type**: wrong exit code, missing check, stale assumption, format mismatch
- **Recurrence**: same file fixed 3+ times = structural risk

### Step 4 — Present as lessons

Format findings as concise rules:
```
LESSON: [short rule]
EVIDENCE: <commit-hash> — <commit message>
AREA: path/to/file or module name
AVOID: [specific thing not to do]
```

## Quick queries

```bash
# Top files with the most fix commits (most fragile areas)
git log --grep="^fix:" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20

# Fix commits by author (who fixes most bugs in this area)
git log --grep="^fix:" --pretty=format:"%an %s" | sort | uniq -c | sort -rn | head -10

# Recent fixes in the last 30 days
git log --grep="^fix:" --oneline --after="30 days ago"

# Fixes that touched hooks (YAMTAM-specific)
git log --grep="^fix:" --oneline -- "*.sh" "*.js"
```

## Constraints

- **Extract only, never summarize speculatively.** Quote exact commit messages; do not infer intent beyond what's written.
- **No git blame for blame assignment.** This skill is for technical pattern recognition, not attribution.
- **Limit depth.** Default to 6 months or 50 commits — older history has diminishing relevance.
- **Promote critical lessons to L1.** If a lesson is structural (e.g., "exit 2 required for blocking hooks"), promote it: `bash .claude/scripts/add-fact.sh`.

## Example output

```
LESSON: Hook blocking requires exit 2 + hookSpecificOutput.permissionDecision
EVIDENCE: fix: correct hook output format in cost-guard and rbac-guard
AREA: core/hooks/cost-guard.sh, core/hooks/rbac-guard.sh
AVOID: Using exit 0 or {decision:"block"} — silent no-op

LESSON: grep -r regex must allow content between flag and path
EVIDENCE: fix: correct bypass test case in truth-gate test suite
AREA: core/hooks/cost-guard.sh
AVOID: Pattern 'grep.*-r[[:space:]]+\.' — misses 'grep -r pattern .'

LESSON: SCHEMA.md must be explicitly skipped in stale-facts loop
EVIDENCE: drift-check.sh fix — SCHEMA.md skip added
AREA: core/scripts/drift-check.sh
AVOID: Only skipping INDEX.md — SCHEMA.md has example dates that trigger false stale
```
