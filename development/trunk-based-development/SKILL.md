---
name: trunk-based-development
description: Follow trunk-based development practices with short-lived branches, frequent integration to main, feature flags, and continuous integration. Use when managing git workflow and releases.
---

# Trunk-Based Development Skill

You are assisting with code that follows trunk-based development practices for rapid, continuous delivery.

## Core Concept

**One Main Branch**: All developers work on a single "trunk" branch (main/master) with short-lived feature branches that merge back quickly (within 1-2 days).

### Why Trunk-Based Development?

- **Reduced merge conflicts**: Frequent integration prevents large divergences
- **Faster feedback**: Issues discovered quickly through CI
- **Simplified workflow**: No complex branching strategies
- **Enables CI/CD**: Trunk is always in a deployable state
- **Better collaboration**: Everyone sees changes quickly

## Core Principles

### 1. Commit Directly to Main (Small Changes)
For small, low-risk changes:
```bash
# Make change
git add .
git commit -m "Add validation for grade range"
git pull --rebase
git push origin main
```

**When to commit directly:**
- Bug fixes that pass all tests
- Documentation updates
- Small refactorings
- Configuration changes

### 2. Short-Lived Feature Branches (Larger Changes)
For larger changes, use branches but merge within 1-2 days:

```bash
# Create short-lived branch
git checkout -b add-quota-rule
# Work for < 2 days
git add .
git commit -m "Add quota capacity validation"
git push origin add-quota-rule
# Create PR, get quick review, merge
```

**Rules for feature branches:**
- **Lifetime**: Maximum 1-2 days before merging
- **Size**: Keep changes small and focused
- **Integration**: Pull from main frequently
- **Review**: Quick reviews (< 2 hours)

### 3. Continuous Integration to Main
Merge to main multiple times per day:

```bash
# Update from main frequently
git checkout main
git pull
git checkout add-quota-rule
git rebase main
# Fix any conflicts
git push origin add-quota-rule --force-with-lease
```

**Target frequency:**
- Small teams: Merge every 4-6 hours
- Medium teams: Merge daily
- Large features: Break into smaller mergeable pieces

## Branch Strategy

### Main Branch Requirements
- **Always builds**: No broken commits
- **Always passes tests**: All CI checks green
- **Always deployable**: Can release at any time
- **Protected**: Requires PR and CI checks

### Feature Branch Guidelines

**Good branch names:**
```
add-minimum-grade-rule
fix-quota-overflow
refactor-competence-calculation
```

**Bad branch names:**
```
dev, development, feature  # Too generic
johns-work                 # Not descriptive
v2-rewrite                 # Too large/long-lived
```

**Branch lifecycle:**
```
1. Create from main
2. Work < 2 days
3. Keep up-to-date with main (rebase daily)
4. Create PR when ready
5. Quick review + CI
6. Merge to main
7. Delete branch immediately
```

## Feature Flags for Incomplete Work

When a feature takes longer than 2 days, use feature flags:

```python
# Feature flag pattern
from config import feature_flags

class AdmissionEvaluationService:
    def evaluate(self, application):
        if feature_flags.is_enabled('new_quota_algorithm'):
            return self._evaluate_with_new_algorithm(application)
        else:
            return self._evaluate_with_old_algorithm(application)
```

**Feature flag types:**

### Release Flags
Control when features go live:
```python
# config/feature_flags.py
FEATURE_FLAGS = {
    'new_quota_system': {
        'enabled': False,  # Not ready for production
        'description': 'New quota allocation algorithm'
    }
}
```

### Experiment Flags
A/B testing or gradual rollouts:
```python
def is_enabled_for_user(feature: str, user_id: str) -> bool:
    """Enable for percentage of users."""
    if feature == 'new_ui':
        # Enable for 10% of users
        return hash(user_id) % 100 < 10
    return False
```

### Permission Flags
Control access by role:
```python
def can_access_feature(feature: str, user_role: str) -> bool:
    if feature == 'admin_quota_override':
        return user_role in ['admin', 'superuser']
    return True
```

## Handling Long-Running Features

### Strategy 1: Branch by Abstraction
Introduce abstraction, implement new version behind it:

```python
# Step 1: Create abstraction (merge to main)
class QuotaAllocator(Protocol):
    def allocate(self, students: List[Student]) -> AllocationResult:
        ...

# Step 2: Make existing code use abstraction (merge to main)
class OldQuotaAllocator(QuotaAllocator):
    def allocate(self, students):
        # Existing logic
        pass

# Step 3: Add new implementation (merge to main, behind flag)
class NewQuotaAllocator(QuotaAllocator):
    def allocate(self, students):
        # New logic
        pass

# Step 4: Switch implementations via config (merge to main)
def get_allocator() -> QuotaAllocator:
    if feature_flags.is_enabled('new_quota'):
        return NewQuotaAllocator()
    return OldQuotaAllocator()

# Step 5: Eventually remove old implementation
```

### Strategy 2: Dark Launching
Deploy new code but don't expose it:

```python
def evaluate_admission(application):
    # Production code path
    result = old_evaluation(application)

    # Dark launch: run new code but don't use result
    if feature_flags.is_enabled('test_new_evaluator'):
        new_result = new_evaluation(application)
        log_comparison(result, new_result)  # Compare results

    return result
```

### Strategy 3: Incremental Implementation
Break large features into small, independently valuable pieces:

```
Large Feature: "New Quota System"

Break down:
✓ Day 1: Add Quota entity (merge)
✓ Day 2: Add capacity validation (merge)
✓ Day 3: Add allocation algorithm (merge behind flag)
✓ Day 4: Add UI for quota management (merge behind flag)
✓ Day 5: Enable flag, deprecate old system
```

## Commit Practices

### Commit Frequency
Commit small, logical units:
```bash
# Good: Small, focused commits
git commit -m "Add Grade value object"
git commit -m "Add grade validation rules"
git commit -m "Add tests for grade validation"

# Bad: Infrequent large commits
git commit -m "Implement entire grade system"
```

### Commit Messages
Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `test`: Add/update tests
- `docs`: Documentation
- `chore`: Maintenance

**Examples:**
```
feat(quota): Add capacity validation for quota entity

Implement validation to ensure quota capacity is never negative
and filled count never exceeds capacity.

Refs: #123

---

fix(grades): Handle missing grade in competence calculation

Previously crashed when student was missing a grade.
Now returns 0 points for missing grades with a warning.

Fixes: #456

---

refactor(admission): Extract rule evaluation to domain service

Move evaluation logic from use case to domain service to follow
Clean Architecture and DDD principles.
```

### Atomic Commits
Each commit should:
- **Build successfully**: Code compiles/runs
- **Pass tests**: All tests green
- **Be self-contained**: One logical change
- **Be revertible**: Can be reverted safely

## Pull Request Practices

### Small PRs
Keep PRs small for faster reviews:

**Good PR sizes:**
- 1-200 lines: Ideal
- 200-400 lines: Acceptable
- 400+ lines: Too large, split it

**How to keep PRs small:**
- Extract refactorings to separate PRs
- Use stacked PRs for related changes
- Split by layer (domain → application → infrastructure)

### Quick Reviews
Target review time: **< 2 hours**

**Reviewer checklist:**
- [ ] Does it build and pass tests?
- [ ] Are requirements met?
- [ ] Does it follow SOLID/Clean Architecture?
- [ ] Are tests adequate?
- [ ] Is it safe to merge?

**Auto-approve criteria:**
- Documentation only
- Test fixes
- Obvious bug fixes
- Approved by CI + 1 reviewer

### PR Description Template
```markdown
## What
Brief description of the change

## Why
Business reason or issue reference

## How
Technical approach

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing done

## Checklist
- [ ] Follows coding standards
- [ ] Documentation updated
- [ ] No breaking changes (or flagged)
- [ ] Ready to merge

## Screenshots (if UI changes)
[Add screenshots]
```

## Continuous Integration Setup

### Required CI Checks
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      - name: Lint
        run: |
          ruff check .
          mypy src/
      - name: Test
        run: |
          pytest --cov=src --cov-report=xml
      - name: Coverage check
        run: |
          coverage report --fail-under=80
```

### Pre-Merge Requirements
- [ ] All tests pass
- [ ] Code coverage ≥ 80%
- [ ] Linting passes
- [ ] Type checking passes
- [ ] At least 1 approval
- [ ] No merge conflicts

## Release Management

### Continuous Deployment
Main branch deploys automatically to staging:

```yaml
# .github/workflows/deploy-staging.yml
name: Deploy to Staging
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to staging
        run: ./scripts/deploy-staging.sh
```

### Release Tagging
Create release tags from main:

```bash
# When ready to release
git checkout main
git pull
git tag -a v1.2.0 -m "Release v1.2.0: Add quota management"
git push origin v1.2.0
```

### Semantic Versioning
Follow semver (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

```
v1.0.0 → Initial release
v1.1.0 → Add new quota rules (feature)
v1.1.1 → Fix quota calculation bug (patch)
v2.0.0 → Change quota API (breaking change)
```

## Common Pitfalls to Avoid

### ❌ Don't: Long-Lived Feature Branches
```
feature-branch (30 days old)
    └── 500 commits behind main
        └── Massive merge conflicts
```

### ✅ Do: Short-Lived Branches + Feature Flags
```
add-quota-entity (1 day) → merged
add-quota-validation (1 day) → merged
add-quota-ui (1 day, behind flag) → merged
```

### ❌ Don't: Wait to Integrate
```
Day 1: Start feature
Day 5: First merge from main
Day 10: Try to merge to main → Conflicts!
```

### ✅ Do: Integrate Frequently
```
Day 1: Merge from main, work, merge to main
Day 2: Merge from main, work, merge to main
```

### ❌ Don't: Large PRs
```
PR: "Implement entire admission system"
Files changed: 50
Lines changed: 2000+
Review time: 3 days
```

### ✅ Do: Small, Focused PRs
```
PR: "Add Grade value object"
Files changed: 3
Lines changed: 120
Review time: 15 minutes
```

## Workflow Checklist

### Starting Work
- [ ] Pull latest from main
- [ ] Create branch (if needed) for work > 4 hours
- [ ] Work in small increments
- [ ] Commit frequently

### During Work
- [ ] Pull/rebase from main at least daily
- [ ] Run tests locally before pushing
- [ ] Keep changes focused and small
- [ ] Use feature flags for incomplete work

### Before Merging
- [ ] All tests pass locally
- [ ] Code is reviewed
- [ ] CI checks pass
- [ ] Documentation updated
- [ ] No breaking changes (or behind flag)

### After Merging
- [ ] Delete feature branch
- [ ] Verify deployment to staging
- [ ] Monitor for issues
- [ ] Update related tickets/tasks

## Integration with Other Skills

### With TDD
- Write tests first (TDD)
- Commit passing tests frequently
- Green CI before merging

### With Clean Architecture
- Merge by layer to keep PRs small:
  1. PR 1: Domain entities
  2. PR 2: Use cases
  3. PR 3: Infrastructure
  4. PR 4: API/UI

### With DDD
- Use feature flags to deploy domain changes incrementally
- Merge bounded context changes separately

### With Requirements Writing
- Link commits/PRs to Gherkin scenarios
- Merge when acceptance criteria met

## Tools and Configuration

### Git Configuration
```bash
# Set up helpful aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.sync '!git fetch origin && git rebase origin/main'

# Set up pull to rebase by default
git config --global pull.rebase true
```

### Branch Protection Rules
In GitHub/GitLab, protect main:
- ✓ Require pull request before merging
- ✓ Require status checks to pass
- ✓ Require branches to be up to date
- ✓ Require conversation resolution
- ✗ Allow force pushes (never force push to main)
- ✓ Require signed commits (optional)

### Pre-Commit Hooks
```bash
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    hooks:
      - id: mypy
```

## Practical Examples for Admission System

### Example 1: Adding a New Rule (Small)
```bash
# 1. Create short-lived branch
git checkout -b add-age-requirement-rule

# 2. Implement (TDD)
# - Write tests
# - Implement rule
# - Tests pass

# 3. Commit
git add .
git commit -m "feat(admission): Add age requirement rule

Add rule to validate student age meets minimum requirement
for specific programs.

Refs: #234"

# 4. Push and create PR
git push origin add-age-requirement-rule

# 5. Quick review → merge → delete branch
```

### Example 2: New Quota System (Large)
```bash
# Day 1: Domain model
git checkout -b quota-domain-model
# Implement Quota entity, value objects
git commit -m "feat(quota): Add Quota entity and value objects"
# PR → merge → delete branch

# Day 2: Validation
git checkout -b quota-validation
# Add capacity validation
git commit -m "feat(quota): Add capacity validation"
# PR → merge → delete branch

# Day 3: Allocation algorithm (incomplete)
git checkout -b quota-allocation
# Add new algorithm behind feature flag
git commit -m "feat(quota): Add new allocation algorithm (feature-flagged)"
# PR → merge → delete branch

# Day 4: UI (hidden)
git checkout -b quota-ui
# Add UI behind same feature flag
git commit -m "feat(quota): Add quota management UI (feature-flagged)"
# PR → merge → delete branch

# Day 5: Enable feature
git checkout -b enable-quota-feature
# Change feature flag to enabled
git commit -m "feat(quota): Enable new quota system"
# PR → merge → delete branch
```

## Response Format

When practicing trunk-based development:
1. Assess if change is small enough to commit directly to main
2. If branch needed, ensure it's short-lived (< 2 days)
3. Break large features into small, mergeable pieces
4. Use feature flags for incomplete work
5. Commit frequently with good messages
6. Create small, focused PRs
7. Integrate with main frequently
8. Delete branches immediately after merge
