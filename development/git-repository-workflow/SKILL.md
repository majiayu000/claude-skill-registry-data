---
name: git-repository-workflow
description: Provides Git repository workflow guidelines including branch management, testing practices (TDD), Docker environment handling, and PR workflow. Use this skill when implementing features, fixing bugs, or making any code changes in a Git repository.
---

# Git Repository Workflow

## Instructions

### CRITICAL: Never Push to Default Branches

**PROHIBITED**: `git push origin main/develop/master`

ALL changes must go through Pull Requests. No exceptions.

### Workflow Decision

```
Start Implementation
    ↓
Existing PR? → YES → gh pr checkout <PR#> → git pull → Implement → Push
    ↓ NO
User says "current branch"? → YES → Implement directly
    ↓ NO
git checkout main && git pull → git checkout -b feature/name → Implement
```

### Branch Naming

- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation

### Testing Requirements

#### Check Test Necessity First

Before writing tests, verify if tests are required:

1. Check CLAUDE.md for test configuration (e.g., "no tests required", "skip tests")
2. If no existing tests in project and unclear, ask user: "This project has no tests. Should I add tests?"
3. If tests not required, proceed to next step without testing

#### Test-Driven Approach (When Tests Required)

Follow Red-Green-Refactor cycle:

1. **Test Skeleton First**: Define test structure before implementation
2. **Descriptive Names**: `should return 404 when user not found` (not `test1`)
3. **Test Coverage**: Happy path → Edge cases → Error cases

#### Docker Environment

When running tests, lint, or other commands in Docker projects:

```
Check if container is running → docker ps | grep <container>
    ↓
Running? → YES → docker exec <container> <command>
    ↓ NO
Start container first or run locally
```

### Web Application Testing

For E2E tests or browser automation, see [web-app-testing.md](web-app-testing.md).

### DO / DON'T

**DO**: Pull latest before starting, use descriptive branch names, verify test requirements, check Docker container status

**DON'T**: Push to main directly, create new branch for existing PR, add tests to test-free projects without confirmation, run commands outside container when app runs in Docker

## Examples

### New Feature Branch

```bash
git checkout main && git pull origin main
git checkout -b feature/descriptive-name
```

### Existing PR

```bash
gh pr checkout <PR-number>
git pull origin <branch-name>
# Make changes
git push origin <branch-name>
```

### Test Skeleton

```typescript
describe('UserAuthentication', () => {
  describe('login', () => {
    it('should successfully login with valid credentials', () => {});
    it('should reject invalid credentials', () => {});
    it('should lock account after multiple failed attempts', () => {});
  });
});
```

### Docker Command Execution

```bash
# Check container status
docker ps | grep myapp

# Execute in running container
docker exec myapp-web npm test
docker exec myapp-web npm run lint
```
