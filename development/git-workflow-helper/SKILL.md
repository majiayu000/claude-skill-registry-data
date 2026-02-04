---
name: Git Workflow Helper
description: Git operations with 100% commit consistency. Handles all git operations for commands including branch creation, atomic commits following project conventions, and PR creation. Always use this skill for git operations to ensure consistency.
---

# Git Workflow Skill

Expert guidance for git operations in the tempo-demo workflow. This skill is the **ONLY way commands should perform git operations** to ensure 100% commit consistency across all workflows.

## Purpose

Provide consistent git operations across all workflow commands:
- Read conventions from `.env` for commit format, branch naming
- Execute atomic commits with proper formatting
- Create feature branches following naming conventions
- Create PRs with Linear integration
- Ensure working directory cleanliness

## Core Responsibility

**CRITICAL**: This skill is the single source of truth for git operations. All commands must use this skill's functions rather than calling git directly. This guarantees:
- ✅ All commits follow project conventions
- ✅ All commits reference issue IDs
- ✅ All commits are atomic and well-scoped
- ✅ All branches follow naming patterns
- ✅ Consistency across all workflows

## Project Conventions

Conventions are stored in `.env` at project root. Default values if not specified:

```bash
# Commit Format
COMMIT_FORMAT=conventional  # Options: conventional, simple

# Branch Naming
BRANCH_PREFIX_FEATURE=feature
BRANCH_PREFIX_BUG=fix
BRANCH_PREFIX_CHORE=chore
BRANCH_PREFIX_EPIC=feature

# GitHub
GITHUB_ORG=your-org
GITHUB_REPO=your-repo

# Linear
PROJECT_TEAM_KEY=TEMPO
```

## Functions

### 1. ensure_clean_state()

**Purpose**: Verify working directory is clean before starting work

**Usage**:
```markdown
Use git-workflow skill to ensure working directory is clean
```

**Implementation**:
```bash
# Check for uncommitted changes
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "❌ Working directory has uncommitted changes"
  git status --short
  exit 1
fi

# Check for untracked files that might matter
UNTRACKED=$(git ls-files --others --exclude-standard)
if [ -n "$UNTRACKED" ]; then
  echo "⚠️  Warning: Untracked files exist:"
  echo "$UNTRACKED"
  # Don't fail, just warn
fi

echo "✅ Working directory is clean"
```

**Returns**: Success/failure status

---

### 2. create_feature_branch(issue_id, issue_title)

**Purpose**: Create feature branch following project naming conventions

**Parameters**:
- `issue_id`: Issue ID (e.g., "TEMPO-123")
- `issue_title`: Issue title for branch name

**Usage**:
```markdown
Use git-workflow skill to create feature branch for TEMPO-123
```

**Implementation**:
```bash
# Load conventions from .env
source .env 2>/dev/null || true
BRANCH_PREFIX=${BRANCH_PREFIX_FEATURE:-feature}

# Generate branch name from issue title
# Convert to kebab-case, max 40 chars
BRANCH_SUFFIX=$(echo "$ISSUE_TITLE" | \
  tr '[:upper:]' '[:lower:]' | \
  sed 's/[^a-z0-9]/-/g' | \
  sed 's/--*/-/g' | \
  sed 's/^-//' | \
  sed 's/-$//' | \
  cut -c1-40)

BRANCH_NAME="${BRANCH_PREFIX}/${ISSUE_ID}-${BRANCH_SUFFIX}"

# Create and checkout branch
git checkout -b "$BRANCH_NAME"

echo "✅ Created branch: $BRANCH_NAME"
```

**Returns**: Branch name

**Example**: `feature/TEMPO-123-add-user-authentication`

---

### 3. commit_changes(type, scope, message, issue_id)

**Purpose**: Create atomic commit with conventional format and issue reference

**Parameters**:
- `type`: Commit type (feat, fix, docs, test, refactor, style, chore)
- `scope`: Scope of change (e.g., "atoms/cache", "features/users", "commands")
- `message`: Description of change
- `issue_id`: Linear issue ID (e.g., "TEMPO-123")

**Usage**:
```markdown
Use git-workflow skill to commit changes:
- Type: feat
- Scope: atoms/cache
- Message: add Redis cache adapter
- Issue: TEMPO-123
```

**Implementation**:
```bash
# Load conventions
source .env 2>/dev/null || true
COMMIT_FORMAT=${COMMIT_FORMAT:-conventional}
TEAM_KEY=${PROJECT_TEAM_KEY:-TEMPO}

# Format commit message based on convention
case "$COMMIT_FORMAT" in
  conventional)
    # Format: type(scope): message (ISSUE-ID)
    COMMIT_MSG="${TYPE}(${SCOPE}): ${MESSAGE} (${ISSUE_ID})"
    ;;
  simple)
    # Format: message (ISSUE-ID)
    COMMIT_MSG="${MESSAGE} (${ISSUE_ID})"
    ;;
  *)
    # Default to conventional
    COMMIT_MSG="${TYPE}(${SCOPE}): ${MESSAGE} (${ISSUE_ID})"
    ;;
esac

# Create commit
git add .
git commit -m "$COMMIT_MSG"

echo "✅ Committed: $COMMIT_MSG"
```

**Returns**: Commit hash and message

**Commit Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding tests
- `refactor`: Code restructuring
- `style`: Formatting, no code change
- `chore`: Maintenance, dependency updates

**Scope Examples**:
- Backend: `atoms/cache`, `features/users`, `molecules/apis`, `organisms/api`
- Frontend: `atoms/button`, `organisms/header`, `pages/dashboard`
- Commands: `commands/plan`, `skills/git-workflow`
- Specs: `specs`, `backend/specs`

**Example Commits**:
```
feat(atoms/security): add JWT utilities (TEMPO-123)
test(atoms/security): add JWT utility tests (TEMPO-123)
feat(features/users): add login/register methods (TEMPO-123)
docs(specs): add implementation spec for user auth (TEMPO-123)
style: auto-format code (TEMPO-123)
```

---

### 4. create_pr(issue_id, pr_title, pr_body)

**Purpose**: Create pull request with Linear integration

**Parameters**:
- `issue_id`: Linear issue ID
- `pr_title`: PR title
- `pr_body`: PR description (markdown)

**Usage**:
```markdown
Use git-workflow skill to create PR for TEMPO-123 with title and body
```

**Implementation**:
```bash
# Load conventions
source .env 2>/dev/null || true

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Push branch to remote
git push -u origin "$CURRENT_BRANCH"

# Determine base branch (usually main or working-files)
BASE_BRANCH=${GITHUB_BASE_BRANCH:-main}

# Call /pr command (primitive that handles gh CLI)
# The /pr command will:
# - Fetch issue details from Linear
# - Read strategy comment if exists
# - Read spec file if exists
# - Generate PR description with full context
# - Create PR via gh CLI
# - Link Linear issue to PR

# For now, delegate to /pr command
echo "Delegating to /pr command for full PR creation..."
# This is a skill, so we instruct the agent to use the /pr command
```

**Note**: This function primarily delegates to the `/pr` command primitive which handles:
- Fetching Linear issue details
- Reading strategy + spec files
- Generating comprehensive PR description
- Creating PR via `gh` CLI
- Linking Linear issue

**Returns**: PR URL

---

## Usage Patterns

### Pattern 1: Clean Branch → Implementation → Commit Loop

```markdown
## Workflow

1. Use git-workflow skill to ensure clean state
2. Use git-workflow skill to create feature branch for TEMPO-123
3. Implement feature (write code)
4. Use git-workflow skill to commit changes:
   - Type: feat
   - Scope: atoms/security
   - Message: add JWT utilities
   - Issue: TEMPO-123
5. Write tests
6. Use git-workflow skill to commit changes:
   - Type: test
   - Scope: atoms/security
   - Message: add JWT utility tests
   - Issue: TEMPO-123
7. Repeat steps 3-6 for each logical unit of work
8. Use git-workflow skill to create PR for TEMPO-123
```

---

### Pattern 2: Spec → Implementation Workflow

```markdown
## Implementation with Spec-First Pattern

1. Generate spec file (via /plan:generate-spec or manually)
2. Use git-workflow skill to commit changes:
   - Type: docs
   - Scope: specs
   - Message: add implementation spec for TEMPO-123
   - Issue: TEMPO-123
3. Implement following spec
4. For each logical step in spec:
   a. Write code
   b. Use git-workflow skill to commit (type: feat, fix, refactor, etc.)
   c. Write tests
   d. Use git-workflow skill to commit (type: test)
5. Use git-workflow skill to create PR
```

**Result**: PR shows spec commit first, then implementation commits. Clear traceability.

---

### Pattern 3: Auto-Fix Quality Gates

```markdown
## Quality Gate Auto-Fix Pattern

1. Run quality gates (format, lint)
2. If auto-fixes applied:
   - Use git-workflow skill to commit changes:
     - Type: style
     - Scope: (empty or specific area)
     - Message: auto-format code
     - Issue: TEMPO-123
3. Run tests
4. If test failures require fixes:
   - Make fixes
   - Use git-workflow skill to commit changes:
     - Type: fix
     - Scope: (specific area)
     - Message: fix failing test
     - Issue: TEMPO-123
```

---

## Integration with Commands

### Commands Using This Skill

1. **/implement** - Primary consumer
   - Creates feature branch
   - Commits at every logical step
   - Creates PR at end

2. **/plan:generate-spec** - Spec generation
   - Commits spec file
   - Updates Linear with spec location

3. **/analyze-implementation** - Strategy generation
   - Commits strategy document

4. **/test** - Quality gates
   - Commits auto-fixes from format/lint

5. **/plan:decompose** - Planning
   - Commits YAML plan file

### Prohibited Direct Git Usage

Commands should **NEVER** call git directly. Instead:

❌ **BAD** (in command):
```bash
git add .
git commit -m "feat(atoms): add cache (TEMPO-123)"
```

✅ **GOOD** (in command):
```markdown
Use git-workflow skill to commit changes:
- Type: feat
- Scope: atoms/cache
- Message: add cache adapter
- Issue: TEMPO-123
```

---

## Benefits

### 100% Commit Consistency

All commits across all workflows follow the same format:
```
<type>(<scope>): <message> (ISSUE-ID)
```

### Traceability

Every commit references a Linear issue, enabling:
- Full audit trail from issue → commits → PR
- Easy filtering by issue
- Clear accountability

### Convention Enforcement

Conventions are read from `.env`, ensuring:
- Single source of truth
- Easy to update conventions project-wide
- Override support for different projects

### Atomic Commits

Pattern encourages small, focused commits:
- One logical change per commit
- Tests committed separately
- Auto-fixes committed separately
- Clear git history

---

## Examples

### Example 1: Feature Implementation

```markdown
## /implement TEMPO-123

1. Use git-workflow skill to ensure clean state
2. Use git-workflow skill to create feature branch for TEMPO-123: "Add user authentication"

# Implement JWT utilities
3. Write atoms/security/jwt.py
4. Use git-workflow skill to commit:
   - Type: feat
   - Scope: atoms/security
   - Message: add JWT utilities
   - Issue: TEMPO-123

# Write tests
5. Write tests/atoms/security/test_jwt.py
6. Use git-workflow skill to commit:
   - Type: test
   - Scope: atoms/security
   - Message: add JWT utility tests
   - Issue: TEMPO-123

# Implement service methods
7. Update features/users/service.py
8. Use git-workflow skill to commit:
   - Type: feat
   - Scope: features/users
   - Message: add login/register methods
   - Issue: TEMPO-123

# Create PR
9. Use git-workflow skill to create PR for TEMPO-123
```

**Result**: 3 atomic commits, clear PR with Linear integration

---

### Example 2: Quality Gate Workflow

```markdown
## /test

1. Run format (ruff format)
2. If changes made:
   Use git-workflow skill to commit:
   - Type: style
   - Scope: (empty)
   - Message: auto-format code
   - Issue: TEMPO-123

3. Run lint (ruff check --fix)
4. If changes made:
   Use git-workflow skill to commit:
   - Type: style
   - Scope: (empty)
   - Message: auto-fix lint issues
   - Issue: TEMPO-123

5. Run tests (pytest)
6. Report results
```

---

## Error Handling

### Uncommitted Changes

```markdown
If skill reports uncommitted changes:
1. Review changes: git status
2. Decide:
   - Commit them via this skill
   - Stash them: git stash
   - Discard them: git restore .
3. Retry operation
```

### Branch Already Exists

```markdown
If branch exists:
1. Check if you want to continue on existing branch
2. Or create new branch with different name
3. Or delete old branch: git branch -D branch-name
```

### Push Failures

```markdown
If push fails:
1. Pull latest: git pull origin main
2. Resolve conflicts if any
3. Retry push
```

---

## Configuration

### Project .env Example

```bash
# Git Workflow Conventions
COMMIT_FORMAT=conventional
BRANCH_PREFIX_FEATURE=feature
BRANCH_PREFIX_BUG=fix
BRANCH_PREFIX_CHORE=chore

# GitHub
GITHUB_ORG=dugshub
GITHUB_REPO=tempo-demo
GITHUB_BASE_BRANCH=main

# Linear
PROJECT_TEAM_KEY=TEMPO
```

### Per-Command Overrides

Commands can override conventions by setting environment variables before calling skill:

```bash
COMMIT_FORMAT=simple git-workflow-skill commit ...
```

---

## Testing

### Test Commit Formatting

```bash
# Test conventional format
TYPE=feat SCOPE=atoms MESSAGE="add cache" ISSUE_ID=TEMPO-1
# Should produce: "feat(atoms): add cache (TEMPO-1)"

# Test simple format
COMMIT_FORMAT=simple MESSAGE="add cache" ISSUE_ID=TEMPO-1
# Should produce: "add cache (TEMPO-1)"
```

### Test Branch Naming

```bash
ISSUE_ID=TEMPO-123 ISSUE_TITLE="Add User Authentication"
# Should produce: "feature/TEMPO-123-add-user-authentication"
```

---

## Best Practices

1. **Always use this skill for git operations** - Never call git directly from commands
2. **Commit frequently** - After each logical unit of work
3. **Use atomic commits** - One change per commit
4. **Separate concerns** - Tests in separate commits from implementation
5. **Include issue ID** - Always reference Linear issue
6. **Use proper types** - Choose correct commit type
7. **Scope accurately** - Use path-based scopes for clarity
8. **Keep messages concise** - Describe what, not why (use commit body for why)

---

## Troubleshooting

### Skill not found

Ensure skill is at `.claude/skills/git-workflow/SKILL.md`

### Conventions not loaded

Check `.env` file exists at project root and is readable

### Commits don't follow format

Verify command is using this skill, not calling git directly

### PR creation fails

Check `gh` CLI is installed and authenticated:
```bash
gh auth status
gh auth login
```
