---
name: pr-split
description: "Split a multi-feature pull request into smaller, focused PRs. Use when: (1) User says 'split pr' or 'break up pr', (2) A PR contains multiple independent features that should be reviewed separately, (3) User wants to decompose a large PR."
---

# PR Split Command

Split a multi-feature pull request into smaller, focused PRs.

**IMPORTANT: This command ALWAYS uses squash merge to discard try-and-error history and create clean, meaningful commits. Never use cherry-pick.**

## Process

### 1. Analyze Current PR

- Check current branch and commits
- Use `gh pr view` for PR details
- **CRITICAL: Extract EXACT base branch using `gh pr view --json baseRefName`**
- Extract original issue reference
- Run `git log origin/<BASE>..HEAD` (not main!)
- Identify distinct features/fixes

### 2. Determine if Split is Needed

- Check if PR contains multiple independent features
- If single feature, inform user split not needed
- If beneficial, explain what will be split

### 3. Plan the Split

- **Use the EXACT base branch from step 1**
- List distinct features/fixes to split
- Present plan for user approval

### 4. Execute Split

For each split feature:

a. **Create new branch from base**

```bash
git fetch origin
git checkout -b feature/split-name origin/<base-branch>
```

b. **Apply changes using squash merge**

```bash
git merge --squash original-branch
```

- Review staged changes
- Unstage files not related to this feature
- Create clean, logical commits

  **CRITICAL - NO COMMIT ALTERATION:**

- NEVER use `git commit --amend`
- NEVER use `git rebase`

c. **Push and create PR**

- Use `gh pr create --base <base-branch>`
- Include original issue reference FIRST
- Include old PR reference LAST

### 5. Handle Original PR

- Add `[outdated]` prefix to title
- Update description with references to new PRs
- Close with comment listing new PRs

## Important Notes

- **CRITICAL: ALWAYS use the original PR's base branch for ALL new PRs**
- **CRITICAL: Compare against the correct BASE branch**
- **CRITICAL: Never alter commits** (no amend, no rebase, no force push)
- **CRITICAL: Mark original PR as outdated**
- If the target project's CLAUDE.md defines PR title conventions (e.g. Japanese titles), follow them — otherwise use a clear default
- Always use squash merge to create clean commits
- Ask for confirmation before executing
