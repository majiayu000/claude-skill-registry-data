---
name: create-pr
description: Create standardized pull/merge requests with summary, test plan, and linked context. Use when creating a PR, opening a merge request, or when user mentions "create PR", "open MR", "merge request", "pull request", "submit for review", or "push and create PR".
allowed-tools: Read, Glob, Grep, Bash
---

# Create PR Skill

You are creating a standardized pull request or merge request. PRs are the unit of reviewable work — they should tell the story of what changed and why.

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

## Process

### Step 1: Analyze Changes

1. **Check current state**
   ```bash
   git status
   git diff --stat
   git log --oneline $(git merge-base HEAD develop)..HEAD
   ```

2. **Identify the base branch** — Usually `develop` for team repos, `main` for CTO repo
3. **Count commits** — Summarize what each commit does
4. **List files changed** — Group by area (backend, frontend, config, tests, docs)
5. **Check for prior artifacts** — Look for plan, spec, review artifacts to reference in PR description

### Step 2: Determine PR Type

Based on the changes, classify:
- **Feature** — New functionality
- **Fix** — Bug fix
- **Refactor** — Code restructuring without behavior change
- **Chore** — Dependencies, config, CI/CD
- **Docs** — Documentation only

### Step 3: Write PR Description

Follow this structure:

```markdown
## Summary

{1-3 bullet points describing WHAT changed and WHY}

## Changes

### {Area 1 — e.g., Backend}
- {Specific change with file reference}
- {Specific change}

### {Area 2 — e.g., Frontend}
- {Specific change}

## Test Plan

- [ ] {Manual test step 1}
- [ ] {Manual test step 2}
- [ ] Unit tests pass: `{test command}`
- [ ] No regressions in: {related area}

## Related

- Task: {link to sprint task or handoff if applicable}
- Depends on: {other MR if applicable}
```

### Step 4: Create the PR/MR

**For GitLab repos (most team repos):**
```bash
# Ensure branch is pushed
git push -u origin $(git branch --show-current)
```

Then use the GitLab MCP tool (if configured):
- `mcp__gitlab__create_merge_request` with:
  - `project_id`: from your project configuration
  - `source_branch`: current branch
  - `target_branch`: `develop` (or `main`)
  - `title`: `{type}({scope}): {short description}` (under 70 chars)
  - `description`: the formatted description from Step 3

**For GitHub repos:**
```bash
gh pr create --title "{title}" --body "$(cat <<'EOF'
{description}
EOF
)"
```

### Step 5: Report

Output to user:
- **MR/PR URL**: {link}
- **Title**: {title}
- **Target**: {base branch}
- **Commits**: {count}
- **Files changed**: {count}
- **Review needed from**: {suggested reviewer based on changed files}

## Title Convention

Follow conventional commits format:
- `feat(auth): add OAuth2 PKCE flow`
- `fix(api): resolve N+1 query in orders endpoint`
- `refactor(models): extract payment logic to service`
- `chore(deps): upgrade Laravel to 12.1`
- `docs(api): add OpenAPI spec for v2 endpoints`

## Pre-PR Checklist

Before creating the PR, verify:
- [ ] All tests pass
- [ ] No unrelated changes included
- [ ] No debug code or console.log left behind
- [ ] No secrets or credentials in the diff
- [ ] Branch is up-to-date with target branch
- [ ] Commit messages are clean and descriptive

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
