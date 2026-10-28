---
name: commit-push-watch
description: Composite workflow that stages all changes, creates a conventional commit, pushes to origin, and monitors CI until green or failure. Use when you want to commit and push in one step with CI monitoring. Triggers on commit and push, push and watch, commit push watch, ship it, push and monitor CI.
group: git-pr
---

# Commit Push Watch

You are a **delivery pipeline agent** that executes the full local-to-CI
workflow in one pass: stage changes, commit with a conventional message, push to
origin, and monitor CI until a terminal state.

## When to Use

- "Commit, push, and watch CI"
- "Ship it"
- "Push these changes and make sure CI passes"
- After completing a fix or feature that needs immediate CI validation

**Not for:**

- Just committing without pushing (use conventional-commit)
- Just monitoring CI on an already-pushed branch (use ci-watcher)
- Creating PRs (use publish-branch after CI is green)

## Context

Aquarium component library:

- **Language**: TypeScript (React + Ant Design + Storybook)
- **CI/CD**: GitHub Actions
- **Commit Format**: Conventional Commits (`type(scope): description`)
- **Branch Naming**: `<type>/<description>-<TICKET>` (e.g., `feat/add-tooltip-MPD-59`)

## The Process

### Phase 1: Stage and Commit

1. Review current changes:

   ```bash
   git status
   git diff HEAD
   ```

2. Analyze the changes and determine commit type, scope, and message following
   conventional-commit conventions.

3. Stage and commit:

   ```bash
   git add <relevant_files>
   git commit -m "type(scope): description

   #agentic"
   ```

   Keep the message short and descriptive. No co-author tag needed for automated
   commits.

### Phase 2: Push to Origin

Push the current branch to origin:

```bash
git push
```

If no upstream is set:

```bash
git push -u origin $(git rev-parse --abbrev-ref HEAD)
```

### Phase 3: Monitor CI

After push succeeds, invoke the **ci-watcher** skill to monitor CI:

- Poll GitHub checks every 30 seconds
- Classify failures as RELATED or UNRELATED
- Auto-fix RELATED failures, retrigger UNRELATED flakes
- Report final status

Refer to the ci-watcher agent for the full monitoring protocol.

## Constraints

- **DO** analyze changes before committing (understand what changed and why)
- **DO** use conventional commit format
- **DO** transition seamlessly from push to CI monitoring
- **DO** always append `#agentic` as the last line of every commit message
- **DO NOT** use `git add .` or `git add -A` blindly -- review files first
- **DO NOT** push to main/master directly
- **DO NOT** continue CI monitoring beyond 50 minutes (100 polls at 30s)

## Output Format

**Commit:** The commit message used and files staged.

**Push:** Confirmation of successful push with branch and remote.

**CI Status:** Real-time monitoring table (from ci-watcher), followed by final
result: all green, failure requiring intervention, or timeout.
