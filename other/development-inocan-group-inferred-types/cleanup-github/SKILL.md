---
name: cleanup-github
description: Progressive audit and cleanup of GitHub accounts - stale forks, orphaned secrets, failing workflows, security configs. Audit-first with user approval before destructive actions. Triggers on 'clean up GitHub', 'audit my repos', 'GitHub hygiene', 'stale forks', 'orphaned secrets'. Requires gh CLI. (user)
---

# Cleanup GitHub

Progressive audit and cleanup of GitHub accounts with user approval before any destructive actions.

## Overview

This skill audits a GitHub account for:
- Failing workflows and misconfigured security scanning
- Stale forks with no custom changes
- Orphaned secrets not used by any workflow
- Dependabot and security configuration

**Workflow:** Audit all categories → Present findings → Get approval → Execute cleanup

**Prerequisite:** `gh auth status` must pass.

## When to Use

- "clean up my GitHub" / "audit my repos"
- "check for stale forks" / "orphaned secrets"
- "GitHub hygiene" / "repo cleanup"
- Investigating failing GitHub Actions
- Periodic account maintenance

## When NOT to Use

- Creating new repos or workflows
- Managing issues or PRs
- CI/CD pipeline setup
- Repository content changes

## Execution Modes

### Full Audit (default)
Run all phases, present consolidated findings.

### Quick Check
Focus on failing workflows and obvious issues only.

```
quick check my GitHub
```

### Targeted Audit
Focus on specific category:

```
check for stale forks
check for orphaned secrets
check failing workflows
```

## Phase Workflow

### Phase 0: Prerequisites

**Verify gh CLI and detect username:**

```bash
gh auth status
USERNAME=$(gh api user --jq '.login')
echo "Auditing GitHub account: $USERNAME"
```

**Count repos for expectations:**

```bash
gh repo list $USERNAME --limit 1000 --json name --jq 'length'
```

### Phase 1: Failing Workflows Audit

**List all repos with workflows:**

```bash
# Using bash to iterate (gh CLI doesn't have built-in cross-repo workflow listing)
/bin/bash -c 'for repo in $(gh repo list USERNAME --limit 100 --json name --jq ".[].name"); do
  workflows=$(gh workflow list --repo "USERNAME/$repo" 2>/dev/null)
  if [ -n "$workflows" ]; then
    echo "=== $repo ==="
    echo "$workflows"
  fi
done'
```

**Check CodeQL default setup (NOT a workflow file!):**

```bash
gh api repos/USERNAME/REPO/code-scanning/default-setup --jq '.state'
```

**Key insight:** CodeQL "default setup" is configured via GitHub Security settings, not workflow files. The API endpoint is `code-scanning/default-setup`, not `workflows`.

**Check recent workflow runs for failures:**

```bash
gh run list --repo USERNAME/REPO --limit 5 --json status,conclusion,name \
  --jq '.[] | select(.conclusion == "failure") | "\(.name): \(.conclusion)"'
```

### Phase 2: Stale Forks Audit

**List all forks:**

```bash
gh repo list USERNAME --fork --json name,parent --jq '.[] | "\(.name) (fork of \(.parent.nameWithOwner // "unknown"))"'
```

**Compare fork to upstream:**

```bash
gh api repos/USERNAME/REPO/compare/UPSTREAM_OWNER:main...USERNAME:main \
  --jq '{ahead: .ahead_by, behind: .behind_by}'
```

**Flag candidates for deletion:**
- `ahead_by: 0` = No custom changes
- `behind_by: N` = Stale (upstream has moved on)

**Present finding:**
```
REPO: 0 commits ahead, 445 behind upstream
→ Recommendation: DELETE (no custom changes, very stale)
```

### Phase 3: Orphaned Secrets Audit

**List secrets per repo:**

```bash
gh api repos/USERNAME/REPO/actions/secrets --jq '.secrets[].name'
```

**Cross-reference with workflow files:**

```bash
# Get workflow file content and search for secret references
gh api repos/USERNAME/REPO/contents/.github/workflows --jq '.[].name' | while read file; do
  gh api "repos/USERNAME/REPO/contents/.github/workflows/$file" --jq '.content' | base64 -d | grep -o 'secrets\.[A-Z_]*'
done | sort -u
```

**Flag orphaned secrets:**
- Secret exists but not referenced in any workflow
- Present for user review (secrets are sensitive - never auto-delete)

### Phase 4: Security Config Audit

**Check Dependabot:**

```bash
# Check for dependabot.yml
gh api repos/USERNAME/REPO/contents/.github/dependabot.yml 2>/dev/null && echo "Dependabot configured"

# Check vulnerability alerts status
gh api repos/USERNAME/REPO/vulnerability-alerts 2>/dev/null && echo "Alerts enabled"
```

**Check code scanning status:**

```bash
gh api repos/USERNAME/REPO/code-scanning/default-setup --jq '{state: .state, languages: .languages}'
```

### Phase 5: "What Did We Miss?" Checklist (MANDATORY)

**This phase is NOT optional.** Run through the comprehensive checklist before presenting final findings.

See [references/audit-checklist.md](references/audit-checklist.md) for the full checklist.

**Quick sweep:**

```bash
# Check for local clones that might have stale remotes
find ~/Repos -maxdepth 2 -name ".git" -type d 2>/dev/null | while read gitdir; do
  repo=$(dirname "$gitdir")
  remote=$(git -C "$repo" remote get-url origin 2>/dev/null)
  # Check if remote points to any repo we're considering deleting
  echo "$repo: $remote"
done
```

**Items to verify:**
- [ ] Local clones with stale remotes (to repos being deleted)
- [ ] GitHub Apps installations
- [ ] Deploy keys per repo
- [ ] Webhooks
- [ ] Collaborators on personal repos

### Phase 6: Cleanup Execution

**Present consolidated findings:**

```markdown
## Audit Summary

### Stale Forks (delete)
- repo1 (0 ahead, 200 behind)
- repo2 (0 ahead, 50 behind)

### Orphaned Secrets (delete)
- repo3: SECRET_NAME (not referenced)

### Failing Workflows (disable or fix)
- repo4: CodeQL misconfigured for wrong language

### Local Clone Check
- No local clones found for repos being deleted
```

**Use AskUserQuestion for approval:**

```
Which cleanup actions should I perform?
[ ] Delete stale forks (2)
[ ] Delete orphaned secrets (1)
[ ] Disable failing workflows (1)
```

**Execute approved actions:**

```bash
# Delete fork (requires delete_repo scope)
gh repo delete USERNAME/REPO --yes

# Delete secret
gh api repos/USERNAME/REPO/actions/secrets/SECRET_NAME -X DELETE

# Disable CodeQL
gh api repos/USERNAME/REPO/code-scanning/default-setup -X PATCH -f state=not-configured

# Disable workflow
gh workflow disable "Workflow Name" --repo USERNAME/REPO
```

**Verify after cleanup:**

```bash
# Confirm repo deleted
gh repo view USERNAME/REPO 2>&1 | grep -q "not found" && echo "Confirmed deleted"

# Confirm secret deleted
gh api repos/USERNAME/REPO/actions/secrets --jq '.secrets[].name' | grep -v SECRET_NAME
```

## Quick Reference

### Essential Commands

| Operation | Command |
|-----------|---------|
| List repos | `gh repo list USERNAME --json name,isFork,visibility` |
| List forks | `gh repo list USERNAME --fork --json name,parent` |
| Compare fork | `gh api repos/.../compare/upstream:main...owner:main` |
| List secrets | `gh api repos/.../actions/secrets --jq '.secrets[].name'` |
| Check CodeQL | `gh api repos/.../code-scanning/default-setup` |
| Delete repo | `gh repo delete USERNAME/REPO --yes` |
| Delete secret | `gh api repos/.../actions/secrets/NAME -X DELETE` |

### Scope Requirements

| Operation | Required Scope |
|-----------|---------------|
| Read repos | (default) |
| List secrets | (default) |
| Delete repos | `delete_repo` - run `gh auth refresh -h github.com -s delete_repo` |
| Modify security | `security_events` |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Assuming CodeQL is a workflow | Wrong API, can't find/disable it | Use `code-scanning/default-setup` API |
| Deleting repos without local check | Orphaned git remotes | Check ~/Repos first |
| Auto-deleting secrets | Secrets might be used externally | Always require user approval |
| Only checking the failing fork | Other forks might be stale too | Audit ALL forks |
| Checking `ahead_by` only | Fork might have upstream changes | Check both `ahead_by` AND `behind_by` |

## References

- [gh-cli-patterns.md](references/gh-cli-patterns.md) - Complete CLI reference with jq patterns
- [audit-checklist.md](references/audit-checklist.md) - Comprehensive "what did we miss?" checklist
- [cleanup-operations.md](references/cleanup-operations.md) - Safe patterns for destructive operations
