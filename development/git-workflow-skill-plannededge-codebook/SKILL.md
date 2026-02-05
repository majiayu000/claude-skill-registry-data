---
document_name: "git-workflow.skill.md"
location: ".claude/skills/git-workflow.skill.md"
codebook_id: "CB-SKILL-GITFLOW-001"
version: "1.0.0"
date_created: "2026-01-03"
date_last_edited: "2026-01-03"
document_type: "skill"
purpose: "Procedural guide for Git operations including branching, commits, and pull requests"
category: "skills"
subcategory: "development"
skill_metadata:
  category: "development"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "Git installed"
    - "Repository access"
related_docs:
  - "standards/commit-messages.md"
  - "templates/github/pr.template.md"
  - "workflows/git-flow.md"
maintainers:
  - "head-cook"
status: "active"
tags:
  - "skill"
  - "git"
  - "version-control"
  - "workflow"
ai_parser_instructions: |
  This skill covers Git operations.
  Section markers: === SECTION ===
  Procedure markers: <!-- PROCEDURE:name:START/END -->
  Command examples are in code blocks.
---

# Git Workflow Skill

[!FIXED!]
## Purpose

This skill provides procedures for Git operations in the development workflow. It covers branching, commits, and pull requests.

**When to use:**
- Creating branches for new work
- Making commits
- Creating pull requests
- Merging changes
[!FIXED!]

---

=== PREREQUISITES ===
<!-- AI:PREREQUISITES:START -->

Before using this skill:

- [ ] Git is installed
- [ ] Repository is cloned locally
- [ ] Commit message standard exists (@ref(CB-STD-COMMITS-001))
- [ ] You have push access (or will create PR)

<!-- AI:PREREQUISITES:END -->

---

=== PROCEDURE: CREATE BRANCH ===
<!-- PROCEDURE:create-branch:START -->

### Branch Naming Convention

```
<type>/<description>

Types:
- feature/  : New features
- bugfix/   : Bug fixes
- hotfix/   : Urgent production fixes
- refactor/ : Code refactoring
- docs/     : Documentation only
- test/     : Test additions
- chore/    : Maintenance tasks
```

### Steps

1. **Ensure you're on main/develop**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create and checkout new branch**
   ```bash
   git checkout -b feature/add-user-authentication
   ```

3. **Log in buildlog**
   ```markdown
   | HH:MM | #micro-decision | Created branch feature/add-user-authentication | - |
   ```

### Branch Naming Examples

| Good | Bad |
|------|-----|
| `feature/add-oauth-login` | `new-login` |
| `bugfix/fix-null-pointer-123` | `fix` |
| `docs/update-api-docs` | `documentation` |

<!-- PROCEDURE:create-branch:END -->

---

=== PROCEDURE: MAKE COMMITS ===
<!-- PROCEDURE:commit:START -->

### Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Purpose |
|------|---------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation |
| style | Formatting (no code change) |
| refactor | Code restructuring |
| test | Adding tests |
| chore | Maintenance |
| perf | Performance improvement |

### Steps

1. **Stage changes**
   ```bash
   git add <files>
   # or for all changes:
   git add .
   ```

2. **Review staged changes**
   ```bash
   git status
   git diff --staged
   ```

3. **Commit with message**
   ```bash
   git commit -m "feat(auth): add OAuth2 login support"
   ```

4. **Log in buildlog**
   ```markdown
   | HH:MM | #commit | feat(auth): add OAuth2 login support | PR #XX |
   ```

### Commit Message Examples

| Good | Bad |
|------|-----|
| `feat(auth): add OAuth2 login support` | `added login` |
| `fix(api): handle null response from endpoint` | `fix bug` |
| `docs(readme): add installation instructions` | `update docs` |
| `refactor(utils): extract date formatting logic` | `refactoring` |

### Commit Frequency

- Commit logical chunks of work
- Each commit should be independently functional
- Don't bundle unrelated changes
- Can be squashed later if needed

<!-- PROCEDURE:commit:END -->

---

=== PROCEDURE: CREATE PULL REQUEST ===
<!-- PROCEDURE:create-pr:START -->

### Before Creating PR

1. **Ensure all commits are pushed**
   ```bash
   git push origin <branch-name>
   ```

2. **Run pre-merge checks**
   - [ ] All tests pass
   - [ ] Linter passes
   - [ ] Code reviewed by self
   - [ ] Documentation updated if needed

### PR Title Format

```
<type>(<scope>): <description>
```

Same format as commit messages.

### PR Description Template

```markdown
## Summary
Brief description of what this PR does.

## Changes
- List of significant changes
- Bullet points preferred

## Testing
- How was this tested?
- Test coverage info

## Related Issues
Closes #123
Related to #456

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Steps

1. **Push branch**
   ```bash
   git push -u origin feature/add-user-authentication
   ```

2. **Create PR via GitHub/GitLab/etc.**
   - Use PR title format
   - Fill in description template
   - Add reviewers
   - Add labels

3. **Log in buildlog**
   ```markdown
   | HH:MM | #micro-decision | Created PR #42 for feature/add-user-authentication | PR #42 |
   ```

<!-- PROCEDURE:create-pr:END -->

---

=== PROCEDURE: MERGE CHANGES ===
<!-- PROCEDURE:merge:START -->

### Merge Strategies

| Strategy | When to Use |
|----------|-------------|
| Squash and Merge | Feature branches, clean history |
| Rebase and Merge | Linear history preferred |
| Merge Commit | Preserve branch history |

### Steps

1. **Ensure PR is approved**
   - Required reviews complete
   - CI checks pass
   - No merge conflicts

2. **Merge using preferred strategy**
   - Via GitHub UI, or:
   ```bash
   git checkout main
   git merge --squash feature/add-user-authentication
   git commit -m "feat(auth): add OAuth2 login support (#42)"
   git push origin main
   ```

3. **Delete branch**
   ```bash
   git branch -d feature/add-user-authentication
   git push origin --delete feature/add-user-authentication
   ```

4. **Log in buildlog**
   ```markdown
   | HH:MM | #commit | Merged feat(auth): add OAuth2 login support | PR #42 |
   ```

<!-- PROCEDURE:merge:END -->

---

=== PROCEDURE: HANDLE CONFLICTS ===
<!-- PROCEDURE:conflicts:START -->

### Steps

1. **Update main and rebase**
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/your-branch
   git rebase main
   ```

2. **Resolve conflicts**
   - Open conflicting files
   - Resolve conflict markers
   - Test resolution
   ```bash
   git add <resolved-files>
   git rebase --continue
   ```

3. **Force push (if rebased)**
   ```bash
   git push --force-with-lease origin feature/your-branch
   ```

4. **Log in buildlog**
   ```markdown
   | HH:MM | #resolution | Resolved merge conflicts in <files> | PR #42 |
   ```

### Conflict Prevention

- Rebase frequently against main
- Communicate about files being modified
- Break large changes into smaller PRs

<!-- PROCEDURE:conflicts:END -->

---

=== PROCEDURE: REVERT CHANGES ===
<!-- PROCEDURE:revert:START -->

### Revert a Commit

```bash
# Revert last commit (creates new commit)
git revert HEAD

# Revert specific commit
git revert <commit-hash>

# Revert without auto-commit
git revert -n <commit-hash>
```

### Log in Buildlog

```markdown
| HH:MM | #resolution | Reverted commit <hash> due to <reason> | - |
```

<!-- PROCEDURE:revert:END -->

---

=== ANTI-PATTERNS ===
<!-- AI:ANTIPATTERNS:START -->

| Anti-Pattern | Why Bad | Alternative |
|--------------|---------|-------------|
| Force push to main | Destroys history | Never force push shared branches |
| Giant commits | Hard to review/revert | Break into logical chunks |
| Vague commit messages | No context | Use conventional format |
| Committing secrets | Security risk | Use .gitignore, env vars |
| Long-lived branches | Merge conflicts | Merge frequently |

<!-- AI:ANTIPATTERNS:END -->

---

=== RELATED DOCUMENTS ===
<!-- AI:RELATED:START -->

| Document | Codebook ID | Relationship |
|----------|-------------|--------------|
| commit-messages.md | CB-STD-COMMITS-001 | Message format |
| pr.template.md | CB-TPL-PR-001 | PR description |
| git-flow.md | CB-WF-GITFLOW-001 | Full workflow |

<!-- AI:RELATED:END -->
