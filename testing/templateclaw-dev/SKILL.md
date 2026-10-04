---
name: templateclaw-dev
description: "Apply dev methodology templates — TDD workflow, CI/CD pipeline, code review checklist, git workflow, and API design guide. Generates actionable guides and configuration files."
allowed-tools: Read, Write, Edit, Bash, Glob
argument-hint: "[guide: tdd|cicd|review|git|api]"
---

# TemplateClaw — Dev Methodology Guides

Generate actionable development methodology guides and configurations.

## When Invoked

1. If argument provided (e.g., `/templateclaw-dev tdd`), generate that guide
2. If no argument, ask: "Which guide? (tdd / cicd / review / git / api)"

## Available Guides

### TDD Workflow Guide (`/templateclaw-dev tdd`)

Generate for the detected project language:

**Output files:**
- `docs/tdd-guide.md` — Step-by-step TDD workflow
- Test config file (jest.config.js / pytest.ini / etc.)
- Example test file demonstrating Red→Green→Refactor

**Content:**
```markdown
# TDD Workflow

## The Cycle
1. RED: Write a failing test
2. GREEN: Write minimum code to pass
3. REFACTOR: Clean up, maintain tests passing

## Rules
- Never write production code without a failing test
- One assert per test (when possible)
- Test behavior, not implementation

## Test Structure (AAA)
- Arrange: Set up test data
- Act: Execute the behavior
- Assert: Verify the outcome

## Coverage Targets
- Unit: 80%+
- Integration: 60%+
- E2E: Critical paths only
```

### CI/CD Pipeline Setup (`/templateclaw-dev cicd`)

Detect repository and generate:

**GitHub Actions** (`.github/workflows/ci.yml`):
```yaml
- Lint → Test → Build → Deploy
- Matrix testing (Node 18/20/22 or Python 3.10/3.11/3.12)
- Caching (node_modules / pip / cargo)
- Security scanning (npm audit / safety / cargo audit)
- Deployment (conditional on branch)
```

**Output:** Working CI/CD config + `docs/cicd-guide.md` explaining each stage.

### Code Review Checklist (`/templateclaw-dev review`)

**Output: `docs/code-review-checklist.md`**

```markdown
## Pre-Review (Author)
- [ ] Tests pass locally
- [ ] No lint warnings
- [ ] Self-reviewed diff
- [ ] PR description explains WHY

## Logic & Correctness
- [ ] Edge cases handled
- [ ] Error paths covered
- [ ] No off-by-one errors
- [ ] Concurrency-safe (if applicable)

## Security
- [ ] No hardcoded secrets
- [ ] Input validation at boundaries
- [ ] SQL injection prevented (parameterized queries)
- [ ] XSS prevention (output encoding)

## Performance
- [ ] No N+1 queries
- [ ] Appropriate indexing
- [ ] No unnecessary re-renders (frontend)

## Maintainability
- [ ] Functions under 50 lines
- [ ] Clear naming (no abbreviations)
- [ ] DRY without over-abstraction
```

### Git Workflow Guide (`/templateclaw-dev git`)

**Output: `docs/git-workflow.md`**

Covers:
- Branch naming: `feature/`, `fix/`, `hotfix/`, `chore/`
- Commit message convention (Conventional Commits)
- PR template
- Merge strategy (squash vs rebase)
- Release tagging (semver)
- Protected branch rules

### API Design Guide (`/templateclaw-dev api`)

**Output: `docs/api-design.md` + example OpenAPI spec**

Covers:
- RESTful conventions (HTTP methods, status codes, URL structure)
- Request/response format (JSON:API or custom)
- Authentication (Bearer token, API key)
- Pagination (cursor-based vs offset)
- Error format (RFC 7807 Problem Details)
- Rate limiting headers
- Versioning strategy (URL vs header)
- OpenAPI 3.1 spec template

## Auto-Detection

Detect project type to customize outputs:
- Language-specific test frameworks
- CI provider (GitHub Actions / GitLab CI / etc.)
- Package manager (npm/yarn/pnpm/pip/cargo)
