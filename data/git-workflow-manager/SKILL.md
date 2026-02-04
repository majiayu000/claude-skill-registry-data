---
name: git-workflow-manager
version: 5.1.0
description: |
  Manages git operations: worktree creation, branch management, commits,
  PRs, semantic versioning, daily rebase workflow, and PR feedback handling.

  Use when: Creating branches/worktrees, committing, pushing, versioning, handling PR feedback

  Triggers: create worktree, commit, push, rebase, version, PR, PR feedback
---

# Git Workflow Manager

## Purpose

Handles all git operations following git-flow + GitHub-flow hybrid model.

## Branch Structure

```
main                           ← Production (tagged vX.Y.Z)
  ↑
release/vX.Y.Z                ← Release candidate
  ↑
develop                        ← Integration branch
  ↑
contrib/<gh-user>             ← Personal contribution branch
  ↑
feature/<timestamp>_<slug>    ← Isolated feature (worktree)
hotfix/vX.Y.Z-hotfix.N       ← Production hotfix (worktree)
```

### Protected Branch Policy

**CRITICAL:** This skill manages git operations and MUST enforce branch protection rules.

**Protected branches (NEVER delete, NEVER commit directly):**
- `main` - Production branch (tagged releases only)
- `develop` - Integration branch (PR merges only)

**All scripts in this skill comply with:**
1. No direct commits to `main` (except tag operations)
2. No direct commits to `develop` (except backmerge_release.py - documented exception)
3. All merges via pull requests (user merges in GitHub/Azure DevOps UI)

**Exception documented:**
- `backmerge_release.py` commits to `develop` during Phase 5.5 back-merge
- This is safe: merges from release branch only, no code changes, maintains history

**Script validation:**
- All scripts in `scripts/` directory are validated for compliance
- Test: `tests/test_branch_protection.py` verifies no unintended main/develop commits
- See WORKFLOW.md "Branch Protection Policy" for complete rules

## Scripts

### create_worktree.py

Creates feature/release/hotfix worktree with TODO file.

```bash
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  <feature|release|hotfix> <slug> <base_branch>
```

**Arguments:**
- `workflow_type`: feature, release, or hotfix
- `slug`: Short descriptive name (e.g., 'json-validator')
- `base_branch`: Branch to create from (e.g., 'contrib/username')

**Output:**
- Creates worktree directory
- Creates new branch
- Generates TODO file in main repo

### daily_rebase.py

Performs daily rebase of contrib branch onto develop.

```bash
python .claude/skills/git-workflow-manager/scripts/daily_rebase.py \
  <contrib_branch>
```

**Steps:**
1. Checkout contrib branch
2. Fetch origin
3. Rebase onto origin/develop
4. Force push with lease

### semantic_version.py

Calculates semantic version based on component changes.

```bash
python .claude/skills/git-workflow-manager/scripts/semantic_version.py \
  <base_branch> <current_version>
```

**Version bump logic:**
- **MAJOR**: Breaking changes (API changes, removed features)
- **MINOR**: New features (new files, new functions)
- **PATCH**: Bug fixes, refactoring, docs

### create_release.py

Creates release branch from develop with TODO file generation.

```bash
python .claude/skills/git-workflow-manager/scripts/create_release.py \
  <version> <base_branch>
```

**Arguments:**
- `version`: Semantic version (e.g., v1.1.0, v2.0.0)
- `base_branch`: Branch to release from (typically 'develop')

**Steps:**
1. Validates version format and inputs
2. Checks semantic version recommendation
3. Creates release branch (release/vX.Y.Z)
4. Generates TODO_release_*.md file
5. Pushes branch to origin

**Output:**
```
✓ Created release branch: release/v1.1.0
✓ Base: develop (commit abc123)
✓ TODO file: TODO_release_20251023T143000Z_v1-1-0.md
✓ Ready for final QA and documentation updates
```

### tag_release.py

Creates annotated tag on main branch after release merge.

```bash
python .claude/skills/git-workflow-manager/scripts/tag_release.py \
  <version> <branch>
```

**Arguments:**
- `version`: Semantic version to tag (e.g., v1.1.0)
- `branch`: Branch to tag (typically 'main')

**Steps:**
1. Validates version format and inputs
2. Checks out and pulls latest from branch
3. Creates annotated tag with release message
4. Pushes tag to origin
5. Optionally creates GitHub release via gh CLI

**Output:**
```
✓ Checked out main branch
✓ Pulled latest changes (commit def456)
✓ Created annotated tag: v1.1.0
  Message: "Release v1.1.0: Production release with vocabulary modules"
✓ Pushed tag to origin
✓ GitHub release created: https://github.com/user/german/releases/tag/v1.1.0
```

### backmerge_release.py

Merges release branch back to develop after main merge.

```bash
python .claude/skills/git-workflow-manager/scripts/backmerge_release.py \
  <version> <target_branch>
```

**Arguments:**
- `version`: Release version (e.g., v1.1.0)
- `target_branch`: Branch to merge into (typically 'develop')

**Steps:**
1. Validates version and verifies tag exists
2. Checks out and pulls target branch
3. Attempts merge with --no-ff strategy
4. On success: pushes to remote
5. On conflicts: creates PR for manual resolution

**Output (no conflicts):**
```
✓ Checked out develop
✓ Pulled latest changes
✓ Merged release/v1.1.0 into develop (no conflicts)
✓ Pushed to origin/develop
✓ Back-merge complete
```

**Output (with conflicts):**
```
⚠ Merge conflicts detected
✓ Created PR: https://github.com/user/german/pull/46
  Title: "chore(release): back-merge v1.1.0 to develop"

Please resolve conflicts in GitHub UI and merge.
```

### cleanup_release.py

Deletes release branch after successful release and back-merge.

```bash
python .claude/skills/git-workflow-manager/scripts/cleanup_release.py \
  <version>
```

**Arguments:**
- `version`: Release version (e.g., v1.1.0)

**Safety Checks (all must pass):**
1. Tag exists
2. Tag is on main branch
3. Release commits are in develop
4. Branch is fully merged

**Steps:**
1. Runs comprehensive safety checks
2. Deletes local release branch (git branch -d)
3. Deletes remote release branch
4. Archives TODO file

**Output:**
```
✓ Verified tag v1.1.0 exists
✓ Verified tag on main branch
✓ Verified back-merge to develop complete
✓ Deleted local branch: release/v1.1.0
✓ Deleted remote branch: origin/release/v1.1.0
✓ Archived: TODO_release_20251023T143000Z_v1-1-0.md
✓ Release workflow complete for v1.1.0
```

### generate_work_items_from_pr.py

Generates work-items from unresolved PR conversations for tracking follow-up work.

```bash
python .claude/skills/git-workflow-manager/scripts/generate_work_items_from_pr.py \
  <pr_number>
```

**Arguments:**
- `pr_number`: Pull request number to analyze

**Purpose:**
- Extracts unresolved PR review conversations
- Creates separate work-items (GitHub issues or Azure DevOps tasks) for each conversation
- Enables PR approval while tracking feedback as separate feature work

**When to use:**
- After PR review, when conversations require follow-up work
- Before approving PR in web portal
- When feedback is substantive enough to warrant separate features

**What it does:**
1. Detects VCS provider (GitHub or Azure DevOps)
2. Fetches PR conversations/threads
3. Filters for unresolved conversations:
   - **GitHub**: `reviewThreads.isResolved == false`
   - **Azure DevOps**: `threads.status == active|pending`
4. For each unresolved conversation, creates work-item:
   - **GitHub**: `gh issue create` with label "pr-feedback"
   - **Azure DevOps**: `az boards work-item create --type Task`
5. Work-item slug pattern: `pr-{pr_number}-issue-{sequence}`
   - Example: `pr-94-issue-1`, `pr-94-issue-2`
6. Links work-item to original PR in title/body
7. Outputs work-item URLs for tracking

**GitHub Integration:**
- Uses GitHub GraphQL API for `isResolved` status
- Query: `repository.pullRequest.reviewThreads`
- Filters: `isResolved: false, isOutdated: false`
- Creates issues with:
  - Title: "PR #94 feedback: {first line of conversation}"
  - Body: Full conversation thread with file/line context
  - Labels: `pr-feedback`, `pr-94`
  - Metadata: Author, file path, line number, PR link

**Azure DevOps Integration:**
- Uses Azure CLI for thread enumeration
- Query: `az repos pr show --id {pr} --query threads`
- Filters: `status == "active" || status == "pending"`
- Creates work-items with:
  - Title: "PR #{pr} feedback: {thread subject}"
  - Description: Full thread content with file context
  - Type: Task
  - Tags: `pr-feedback`, `pr-{pr_number}`
  - Relations: Links to PR URL

**Workflow Pattern:**
```bash
# 1. Create PR from feature to contrib
gh pr create --base contrib/stharrold --head feature/20251108T112041Z_auth

# 2. Reviewers add comments in web portal

# 3. Generate work-items for unresolved conversations
python .claude/skills/git-workflow-manager/scripts/generate_work_items_from_pr.py 94

# Output:
# ✓ Found 3 unresolved conversations
# ✓ Created work-item: pr-94-issue-1 (https://github.com/user/repo/issues/123)
# ✓ Created work-item: pr-94-issue-2 (https://github.com/user/repo/issues/124)
# ✓ Created work-item: pr-94-issue-3 (https://github.com/user/repo/issues/125)

# 4. Approve PR in web portal (conversations remain as work-items)

# 5. For each work-item, create new feature worktree:
python .claude/skills/git-workflow-manager/scripts/create_worktree.py \
  feature pr-94-issue-1 contrib/stharrold

# 6. Implement fix, create PR, merge
# 7. Repeat for remaining work-items
```

**Key Features:**
- Compatible with all issue trackers (GitHub Issues, Azure DevOps Work Items)
- Preserves conversation context (file, line, author, timestamps)
- Enables PR approval without blocking on follow-up work
- Creates traceable lineage: PR → work-items → feature branches → new PRs
- Supports both GitHub and Azure DevOps workflows

**Decision Tree:**
```
PR reviewed with comments
├─ Simple fixes (typos, formatting)
│  └─ Fix directly on feature branch, push update
└─ Substantive changes (new features, refactoring)
   └─ Generate work-items, approve PR, fix in separate features
```

## Release Workflow

The release workflow implements Phase 5 from WORKFLOW.md, providing a complete automation of git-flow release process.

### When to Use Release Workflow

**Use release workflow when:**
- Ready to create production release from develop
- All features for version are integrated and tested
- Quality gates pass on develop branch
- Following semantic versioning for the release

**Use hotfix workflow when:**
- Critical production bug needs immediate fix
- Cannot wait for regular release cycle
- Fix targets specific production version

### Typical Release Sequence

```bash
# Step 1: Create release branch from develop
python .claude/skills/git-workflow-manager/scripts/create_release.py \
  v1.1.0 develop

# Step 2: Perform QA on release branch
# - Run quality gates
# - Update documentation
# - Update version in pyproject.toml

# Step 3: Create PR: release/v1.1.0 → main
gh pr create --base main --title "Release v1.1.0"

# Step 4: User merges PR in GitHub UI
# (Manual step - review and merge)

# Step 5: Tag release on main
python .claude/skills/git-workflow-manager/scripts/tag_release.py \
  v1.1.0 main

# Step 6: Back-merge to develop
python .claude/skills/git-workflow-manager/scripts/backmerge_release.py \
  v1.1.0 develop

# Step 7: Cleanup release branch
python .claude/skills/git-workflow-manager/scripts/cleanup_release.py \
  v1.1.0

# Step 8: Update contrib branch
python .claude/skills/git-workflow-manager/scripts/daily_rebase.py \
  contrib/<gh-user>
```

### Integration with Phase 5

The release scripts implement the 8-step process documented in WORKFLOW.md Phase 5:

| Step | Script | Description |
|------|--------|-------------|
| 5.1 | create_release.py | Create release branch |
| 5.2 | Manual | QA and documentation updates |
| 5.3 | gh pr create | Create PR to main |
| 5.4 | Manual | User merges in GitHub UI |
| 5.5 | tag_release.py | Tag release on main |
| 5.6 | backmerge_release.py | Back-merge to develop |
| 5.7 | cleanup_release.py | Delete release branch |
| 5.8 | daily_rebase.py | Update contrib branch |

### Error Recovery

If a release workflow step fails:

1. **create_release.py fails**: Branch and TODO file are cleaned up automatically
2. **tag_release.py fails**: Local tag is cleaned up on push failure
3. **backmerge_release.py conflicts**: PR is created for manual resolution
4. **cleanup_release.py safety checks fail**: Branch is NOT deleted, manual cleanup required

All scripts include comprehensive error messages with recovery instructions.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** feat, fix, docs, style, refactor, test, chore

**Example:**
```
feat(validator): add JSON schema validation endpoint

Implements REST API endpoint for validating JSON against schemas.
Uses jsonschema library for validation logic.

Implements: impl_003
Spec: specs/json-validator/spec.md
Tests: tests/test_validator.py
Coverage: 85%

Refs: TODO_feature_20251022T143022Z_json-validator.md
```

## PR Creation

```bash
# Feature → contrib/<gh-user>
gh pr create \
  --base "contrib/<gh-user>" \
  --head "<feature-branch>" \
  --title "feat: <description>" \
  --body "See TODO_feature_*.md for details"

# After user merges in GitHub UI:
# Contrib → develop
gh pr create \
  --base "develop" \
  --head "contrib/<gh-user>" \
  --title "feat: <description>" \
  --body "Completed feature: <name>"
```

## Integration with Other Skills

Other skills call these scripts:

```python
import subprocess

# Create worktree
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/create_worktree.py',
    'feature', 'my-feature', 'contrib/user'
], capture_output=True, text=True)

# Calculate version
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/semantic_version.py',
    'develop', 'v1.0.0'
], capture_output=True, text=True)

new_version = result.stdout.strip()
```
