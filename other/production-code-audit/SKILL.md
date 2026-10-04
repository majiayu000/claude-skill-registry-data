---
name: production-code-audit
description: "Autonomously deep-scan entire codebase line-by-line, understand architecture and patterns, then systematically transform it to production-grade, corporate-level professional quality with optimizations"
risk: unknown
source: community
date_added: "2026-02-27"
---

## Use this skill when

- User says "make this production-ready"
- User says "audit my codebase"
- User says "make this professional/corporate-level"
- User says "optimize everything"
- User wants enterprise-grade quality
- Preparing for production deployment
- Code needs to meet corporate standards

## Do not use this skill when

- The user wants a targeted fix for a known issue — use a domain-specific skill instead
- The task is a single-file change with a clear scope
- The user needs only a security review — use security-audit skill

## Instructions

When invoked, proceed autonomously through all four phases without asking the user for input.

**Phase 1: Codebase Discovery**
1. Read all files in the project recursively
2. Identify tech stack from package.json, requirements.txt, or equivalent
3. Understand architecture: structure, patterns, dependencies, data flow
4. Identify purpose of the application
5. Find entry points, routes, and controllers
6. Map how data moves through the system

**Phase 2: Comprehensive Issue Detection**
Scan line-by-line for all categories of issues. Do not skip any file.

**Phase 3: Automatic Fixes**
Fix all identified issues. Do not just report — actually make the changes.

**Phase 4: Verification and Report**
Run all tests. Measure improvements. Generate comprehensive before/after report.

## Capabilities

### Architecture Analysis
- Circular dependency detection
- Tight coupling identification
- God class detection (over 500 lines or over 20 methods)
- Missing separation of concerns
- Poor module boundary design
- Design pattern violations

### Security Vulnerability Detection
- SQL injection: string concatenation in database queries
- XSS vulnerabilities: unescaped output in responses
- Hardcoded secrets: API keys, passwords, tokens in source code
- Missing authentication on protected routes
- Missing authorization checks (broken access control)
- Weak password hashing: MD5, SHA1, unsalted hashes
- Missing input validation on API endpoints
- CSRF vulnerabilities in state-changing operations
- Insecure dependency versions
- Mass assignment vulnerabilities

### Performance Analysis
- N+1 query patterns
- Missing database indexes on foreign keys and filter columns
- Synchronous operations that should be async
- Missing caching for expensive repeated operations
- Inefficient algorithms (O(n²) or worse where O(n log n) is achievable)
- Large bundle sizes in frontend code
- Unoptimized images
- Memory leaks (unclosed event listeners, retained references)

### Code Quality Assessment
- High cyclomatic complexity (over 10 per function)
- Code duplication and copy-paste patterns
- Magic numbers without named constants
- Poor naming: single-letter variables, misleading names, inconsistent conventions
- Missing error handling for async operations, external calls, file I/O
- Inconsistent formatting and style
- Dead code and unused variables
- Unresolved TODO/FIXME comments in critical paths

### Testing Gaps
- Missing tests for critical business logic paths
- Test coverage below 80%
- No edge case testing for boundary conditions
- Flaky tests with race conditions or timing dependencies
- Missing integration tests for database operations and external APIs

### Production Readiness Gaps
- Missing or incomplete environment variable configuration
- No structured logging or monitoring integration
- No error tracking (Sentry, Bugsnag, or equivalent)
- Missing health check endpoints
- Incomplete API documentation
- No CI/CD pipeline configuration

### Automatic Fix Capabilities
- Refactor god classes into focused, single-responsibility services
- Fix circular dependencies by extracting shared logic or using event-based decoupling
- Replace string-concatenated SQL with parameterized queries
- Remove hardcoded secrets and replace with environment variable references
- Add authentication and authorization middleware to unprotected routes
- Upgrade weak password hashing to bcrypt with appropriate cost factor
- Add Zod/Joi validation schemas to all API endpoints
- Fix N+1 queries with proper joins or batch loading
- Add Redis caching for expensive repeated database queries
- Add composite database indexes on frequently filtered columns
- Add Winston/Pino structured logging
- Add Sentry error tracking integration
- Add /health and /ready endpoints
- Add Prometheus metrics endpoint
- Configure rate limiting for public endpoints
- Generate OpenAPI/Swagger documentation
- Write tests for untested critical paths
- Create CI/CD pipeline configuration

## Behavioral Traits
- Scans autonomously without asking for input
- Prioritizes critical security issues before performance before code quality
- Reports metrics in before/after format with percentages where measurable
- Actually makes the changes, not just reports findings
- Runs tests after each batch of changes to catch regressions
- Measures performance improvements with concrete numbers
- Creates GitHub issues or task lists for issues that cannot be auto-fixed

## Knowledge Base

### Issue Priority Order
1. Critical security: SQL injection, hardcoded secrets, missing auth, weak hashing
2. High: N+1 queries, missing indexes, god classes, circular dependencies, missing error handling
3. Medium: code duplication, high complexity, missing tests, missing logging
4. Low: naming conventions, formatting, dead code, documentation gaps

### Production Readiness Checklist

**Security**
- No SQL injection vulnerabilities (parameterized queries everywhere)
- No hardcoded secrets (all in environment variables)
- Authentication on all protected routes
- Authorization checks for all sensitive operations
- Input validation on all API endpoints
- Password hashing with bcrypt (cost factor 10+)
- HTTPS enforced
- Dependencies with no known vulnerabilities

**Performance**
- No N+1 query problems
- Database indexes on all foreign keys
- Caching implemented for expensive operations
- API response time under 200ms for typical operations
- Bundle size under 200KB gzipped for frontend code

**Testing**
- Test coverage above 80%
- Critical paths tested end-to-end
- Edge cases and error conditions covered
- No flaky tests
- Tests run automatically in CI/CD

**Production Readiness**
- Environment variables documented and validated on startup
- Error tracking configured (Sentry or equivalent)
- Structured logging implemented
- Health check endpoints responding
- Monitoring and alerting active
- API documentation complete

### Common Pitfalls During Audit
- Too many issues found: focus on critical/high priority only, create tracking issues for the rest
- False positives: verify in context before fixing; some patterns are intentional
- No follow-up: every finding should become a tracked issue or a code change
- Breaking changes: run tests after each set of changes to catch regressions

## Constraints
- Never delete code without confirming it is truly dead code (check all references first)
- Never change public API signatures without checking all callers
- Never modify tests to make them pass — fix the underlying code
- Always run tests after making changes to verify no regressions
- Always measure baseline metrics before optimizing so improvement can be quantified
- Document every security fix with before/after explanation
