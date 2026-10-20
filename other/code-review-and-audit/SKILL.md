---
name: code-review-and-audit
description: 'Conduct systematic code reviews and audits including automated checks, security audits, compliance verification, and review checklists. Use when reviewing pull requests, performing security audits, verifying coding standards compliance, or setting up automated code review workflows.'
---

# Code Review & Audit

> **Purpose**: Systematic validation of implementations against production guardrails. 
> **Focus**: Self-review automation, manual review checklists, security audits, compliance verification.

---

## When to Use This Skill

- Reviewing pull requests for code quality
- Performing security audits on codebases
- Verifying coding standards compliance
- Setting up automated code review pipelines
- Conducting pre-merge quality gates

## Prerequisites

- Git and GitHub/Azure DevOps familiarity
- Code analysis tools (ESLint, Roslyn Analyzers, etc.)

## Code Review Checklist

### Architecture & Design (AGENTS.md Alignment)

- [ ] **Research -> Design -> Implement** workflow followed
- [ ] Architecture documented (ADRs for significant decisions)
- [ ] SOLID principles adhered to (especially SRP, DIP)
- [ ] Design patterns used appropriately (not over-engineered)
- [ ] No premature optimization (YAGNI principle)

### Code Quality

- [ ] **Single Responsibility** - Each class/method does one thing
- [ ] **DRY** - No code duplication (extracted to methods/classes)
- [ ] **KISS** - Simple solution, not over-complicated
- [ ] **Meaningful names** - Self-documenting code
- [ ] **Functions < 50 lines** - Long methods refactored
- [ ] **No magic numbers** - Constants with clear names
- [ ] **No dead code** - Unused code removed
- [ ] **No commented code** - Remove or document why kept

### Type Safety & Documentation

- [ ] **Type annotations** on all parameters and return values
- [ ] **Nullable reference types** handled correctly
- [ ] **XML documentation** on all public APIs
- [ ] **Inline comments** explain "why", not "what"
- [ ] **README updated** with new features/changes
- [ ] **API documentation** generated and accurate

### Error Handling

- [ ] **Specific exceptions** caught (not generic `Exception`)
- [ ] **No empty catch blocks** - Log or handle properly
- [ ] **Errors logged** with context (correlation IDs)
- [ ] **Retry logic** for transient failures (Polly)
- [ ] **Circuit breakers** for external dependencies
- [ ] **Timeouts configured** on all external calls
- [ ] **Graceful degradation** implemented where needed
- [ ] **No sensitive data** in error messages

### Security (OWASP Top 10)

- [ ] **Input validation** - All user inputs sanitized
- [ ] **SQL parameterized** - NEVER string concatenation
- [ ] **No hardcoded secrets** - Use Key Vault/env vars
- [ ] **Authentication implemented** - JWT/OAuth
- [ ] **Authorization checks** - Proper role/claim validation
- [ ] **HTTPS enforced** in production
- [ ] **CORS configured** correctly (not AllowAnyOrigin)
- [ ] **Rate limiting** enabled on public APIs
- [ ] **Security headers** added (CSP, X-Frame-Options, etc.)
- [ ] **Passwords hashed** with BCrypt/Argon2 (work factor 12)
- [ ] **Dependencies audited** - No known vulnerabilities

### Testing (80%+ Coverage)

- [ ] **Test pyramid** followed (70% unit, 20% integration, 10% e2e)
- [ ] **Unit tests** for all business logic
- [ ] **Integration tests** for API endpoints
- [ ] **E2E tests** for critical user journeys
- [ ] **Edge cases tested** (null, empty, boundary values)
- [ ] **Error paths tested** (exceptions, timeouts)
- [ ] **Mocks used properly** - Isolate unit tests
- [ ] **Tests are fast** (< 1s per unit test)
- [ ] **Tests are deterministic** - No flaky tests
- [ ] **Code coverage 80%** - Verified

### Performance

- [ ] **Async/await** used for I/O operations
- [ ] **No blocking calls** (Task.Result, .Wait())
- [ ] **Database queries optimized** (indexes, projections)
- [ ] **N+1 queries prevented** (Include() or projections)
- [ ] **Caching implemented** where appropriate
- [ ] **Connection pooling** enabled
- [ ] **Large collections paginated**
- [ ] **Response compression** enabled

### Database (EF Core)

- [ ] **Migrations created** and tested
- [ ] **Indexes defined** on foreign keys and query filters
- [ ] **Transactions used** for multi-step operations
- [ ] **AsNoTracking** for read-only queries
- [ ] **Soft deletes** implemented (not hard deletes)
- [ ] **Audit fields** present (CreatedAt, UpdatedAt, etc.)

### Configuration & Deployment

- [ ] **Config externalized** - No hardcoded values
- [ ] **Environment-specific settings** in appsettings.{env}.json
- [ ] **Feature flags** for toggleable features
- [ ] **Health checks** implemented (liveness + readiness)
- [ ] **Structured logging** with correlation IDs
- [ ] **Metrics/monitoring** configured
- [ ] **Graceful shutdown** handling
- [ ] **Dependencies version-pinned** in lock files

### Version Control

- [ ] **Atomic commits** - One logical change per commit
- [ ] **Conventional commits** format followed
- [ ] **No merge commits** in feature branch (use rebase)
- [ ] **PR description** clear and complete
- [ ] **Tests passing** in CI/CD pipeline
- [ ] **No merge conflicts** with main branch

---

## Best Practices

### [PASS] DO

- **Automate checks** - Pre-commit hooks, CI/CD
- **Review incrementally** - Small, focused PRs
- **Use checklists** - Ensure nothing missed
- **Run security scans** - Before every release
- **Document decisions** - ADRs for architecture
- **Test audit scripts** - Verify they catch issues
- **Update checklists** - As standards evolve

### [FAIL] DON'T

- **Skip automated checks** - Always run before PR
- **Large PRs** - > 400 lines hard to review
- **Review own code only** - Get peer review
- **Ignore warnings** - Fix or document exceptions
- **Manual-only audits** - Automate what you can
- **Deploy without audit** - Security scans mandatory

---

## Quick Reference

**Pre-Review Command**:
```bash
dotnet format --verify-no-changes && \
dotnet build && \
dotnet test --collect:"XPlat Code Coverage" && \
dotnet list package --vulnerable --include-transitive
```

**Security Scan**:
```bash
grep -rn "password.*=.*\"" . --include=*.cs
dotnet list package --vulnerable
```

**Coverage Check**:
```bash
dotnet test --collect:"XPlat Code Coverage"
reportgenerator -reports:"**/coverage.cobertura.xml" -targetdir:"coverage"
```

---

**See Also**: [AGENTS.md](../../../../AGENTS.md) - [Testing](../testing/SKILL.md) - [Security](../../architecture/security/SKILL.md) - [Remote Git Ops](../../operations/remote-git-operations/SKILL.md)

**Last Updated**: January 13, 2026

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [`run-checklist.ps1`](scripts/run-checklist.ps1) | Automated code review checklist (large files, TODOs, secrets, tests) | `./scripts/run-checklist.ps1 [-Path ./src]` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| False positives from linters | Configure rule exclusions in .eslintrc or .editorconfig |
| Review backlog growing | Set SLA for review turnaround, use auto-assignment for reviewers |
| Security scan too slow | Run SAST incrementally on changed files only in CI pipeline |

## References

- [Pre Review Automation](references/pre-review-automation.md)
- [Security Audit Compliance](references/security-audit-compliance.md)
- [Review Tools Workflow](references/review-tools-workflow.md)