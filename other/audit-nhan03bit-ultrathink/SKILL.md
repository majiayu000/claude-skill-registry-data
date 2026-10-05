---
name: audit
description: Full codebase audit orchestrator covering security, code quality, performance, and accessibility analysis with prioritized findings.
layer: orchestrator
category: orchestration
triggers:
  - "/audit"
  - "audit this codebase"
  - "full code audit"
  - "security audit"
  - "quality audit"
  - "review the whole project"
inputs:
  - Codebase path or repository
  - Optional audit scope (security, quality, performance, accessibility, or all)
  - Optional focus areas or concerns
  - Optional severity threshold for reporting
outputs:
  - Categorized findings (security, quality, performance, accessibility)
  - Severity-ranked issue list (critical, high, medium, low, info)
  - Remediation recommendations per finding
  - Executive summary with overall health score
  - Actionable fix list ordered by priority
linksTo:
  - scout
  - code-review
  - test
  - optimize
  - research
  - debug
  - fix
  - refactor
  - sequential-thinking
  - mermaid
  - docs-writer
  - plan
linkedFrom:
  - team
  - ship
preferredNextSkills:
  - fix
  - refactor
  - cook
  - ship
fallbackSkills:
  - code-review
  - scout
riskLevel: low
memoryReadPolicy: full
memoryWritePolicy: always
sideEffects:
  - Reads all source files (read-only analysis phase)
  - May run test suite to assess coverage
  - May run linting tools
  - Produces audit report artifacts
  - Does NOT modify code unless explicitly asked to fix findings
---

# Audit

## Purpose

Audit is the comprehensive codebase analysis orchestrator. It systematically examines a codebase across four dimensions -- security, code quality, performance, and accessibility -- and produces a prioritized report of findings with remediation recommendations. Think of it as a thorough health checkup for your code.

Audit is read-only by default. It analyzes and reports but does not change code unless the user explicitly asks it to fix findings. This makes it safe to run at any time without risk of unintended changes.

## Workflow

### Phase 1: Scope & Inventory
1. **Parse audit parameters** -- Determine what to audit (full or specific dimensions) and any focus areas.
2. **Invoke `scout`** -- Build a comprehensive inventory of the codebase:
   - File count and types
   - Directory structure
   - Dependency list and versions
   - Configuration files
   - Test coverage status
   - CI/CD configuration
3. **Establish baselines** -- Record current metrics:
   - Test count and pass rate
   - Lint error count
   - Bundle size (if applicable)
   - Dependency count and age

### Phase 2: Security Audit
4. **Dependency vulnerability scan** -- Check all dependencies for known vulnerabilities:
   - Outdated packages with security patches available
   - Packages with known CVEs
   - Abandoned or unmaintained dependencies
5. **Secret detection** -- Scan for accidentally committed secrets:
   - API keys, tokens, passwords in source code
   - Hardcoded credentials in configuration
   - Secrets in git history (if accessible)
   - Proper .gitignore coverage for sensitive files
6. **Input validation analysis** -- Check all user input handling:
   - SQL injection vectors (raw queries, string concatenation)
   - XSS vectors (unescaped output, unsafe innerHTML usage)
   - Command injection (exec, spawn with user input)
   - Path traversal (file operations with user input)
7. **Authentication & authorization review** -- Examine auth implementation:
   - Session management (secure cookies, expiration, rotation)
   - Token handling (JWT validation, refresh flow, storage)
   - Route protection (middleware coverage, missing auth checks)
   - CORS configuration
   - Rate limiting
8. **Data handling review** -- Check sensitive data practices:
   - PII exposure in logs
   - Encryption at rest and in transit
   - Data sanitization before storage
   - Proper error messages (no stack traces to users)

### Phase 3: Code Quality Audit
9. **Architecture analysis** -- Evaluate structural health:
   - Separation of concerns adherence
   - Single responsibility violations
   - Circular dependencies
   - Module coupling analysis (via `mermaid` dependency graph)
   - Dead code detection
10. **Code patterns analysis** -- Check for antipatterns:
    - God objects or functions (> 200 lines)
    - Deep nesting (> 4 levels)
    - Callback hell or promise chains
    - Magic numbers and strings
    - Copy-paste code (DRY violations)
    - Inconsistent naming conventions
    - TODO/FIXME/HACK comment inventory
11. **Error handling analysis** -- Examine error management:
    - Uncaught promise rejections
    - Empty catch blocks
    - Generic error messages
    - Missing error boundaries (React)
    - Insufficient logging
12. **Test quality analysis** -- Evaluate the test suite:
    - Coverage percentage and gaps
    - Test quality (assertions per test, edge cases)
    - Flaky test indicators
    - Missing test categories (unit, integration, e2e)
    - Test organization and naming

### Phase 4: Performance Audit
13. **Bundle analysis** (frontend) -- Evaluate client-side performance:
    - Bundle size and composition
    - Tree-shaking effectiveness
    - Code splitting coverage
    - Dynamic import usage
    - Image optimization
    - Font loading strategy
14. **Runtime performance** -- Check for performance antipatterns:
    - N+1 query patterns
    - Missing database indexes (if schema is accessible)
    - Unnecessary re-renders (React)
    - Memory leak patterns (event listeners, intervals)
    - Expensive computations without memoization
    - Missing pagination on large data sets
15. **API performance** -- Review API design:
    - Response payload sizes
    - Missing caching headers
    - Over-fetching or under-fetching patterns
    - Connection pooling configuration
    - Timeout handling

### Phase 5: Accessibility Audit
16. **Semantic HTML analysis** -- Check markup quality:
    - Proper heading hierarchy
    - Landmark usage (nav, main, aside, etc.)
    - List markup for list content
    - Table markup for tabular data
17. **Interactive element analysis** -- Check usability:
    - Keyboard navigation support
    - Focus management
    - Touch target sizes
    - Form label associations
    - Error message accessibility
18. **ARIA analysis** -- Check assistive technology support:
    - ARIA role usage and correctness
    - Live region announcements
    - Modal/dialog focus trapping
    - Loading state announcements
19. **Visual analysis** -- Check visual accessibility:
    - Color contrast ratios (WCAG AA: 4.5:1 text, 3:1 UI)
    - Font size minimums (>= 14px body)
    - Motion preferences respected (prefers-reduced-motion)
    - Focus indicator visibility

### Phase 6: Report
20. **Compile findings** -- Aggregate all findings with severity ratings:
    - **Critical**: Security vulnerabilities, data exposure, auth bypass
    - **High**: Performance blockers, major accessibility failures, architectural debt
    - **Medium**: Code quality issues, minor security concerns, missing tests
    - **Low**: Style inconsistencies, minor optimization opportunities
    - **Info**: Suggestions, best practice recommendations
21. **Generate executive summary** -- Produce a high-level health assessment:
    - Overall health score (A-F or numeric)
    - Per-dimension scores
    - Top 5 priority fixes
    - Trend comparison (if previous audit data exists)
22. **Invoke `docs-writer`** -- Format the audit report.
23. **Present findings** -- Deliver the report with actionable next steps.
24. **Suggest remediation plan** -- Invoke `plan` to create a fix plan if the user wants to address findings.

## Severity Matrix

| Dimension | Critical | High | Medium | Low |
|-----------|----------|------|--------|-----|
| Security | Data breach risk, auth bypass | Injection vectors, weak crypto | Missing headers, verbose errors | Outdated non-vulnerable deps |
| Quality | Circular deps, no tests | God objects, no error handling | DRY violations, magic numbers | Naming inconsistencies |
| Performance | Memory leaks, N+1 in loops | Missing indexes, huge bundles | Missing memoization | Minor optimization opportunities |
| Accessibility | No keyboard access, missing alt | No focus management, low contrast | Missing ARIA labels | Suboptimal heading order |

## Usage

Use Audit when you want a comprehensive understanding of a codebase's health. It's especially valuable before major releases, after inheriting a codebase, or on a regular cadence (monthly/quarterly).

**Best for:**
- Pre-release quality gates
- Codebase health assessments
- New team member onboarding (to understand tech debt)
- Compliance and security reviews
- Post-incident reviews
- Regular health checkups

**Not ideal for:**
- Building features (use `cook`)
- Fixing specific bugs (use `debug` + `fix`)
- Reviewing a single PR (use `code-review`)

## Examples

### Example 1: Full audit
```
User: /audit Run a full audit on this codebase

Audit workflow:
1. scout -> Inventory: 342 files, 18 deps, 67% test coverage
2. Security -> 2 critical (exposed API key in config, SQL injection in search),
              4 medium (missing rate limiting, verbose error messages)
3. Quality -> 1 high (circular dependency in models/), 8 medium (DRY violations),
             12 low (naming inconsistencies)
4. Performance -> 1 high (N+1 in user list endpoint), 3 medium (no code splitting)
5. Accessibility -> 2 high (no keyboard nav on modal, missing form labels),
                   5 medium (low contrast on secondary text)
Report: Overall score C+, 2 critical security fixes needed immediately
```

### Example 2: Security-focused audit
```
User: /audit Security audit only, we're preparing for SOC 2

Audit workflow:
1. scout -> Full codebase inventory
2. Security deep dive -> All 5 security sub-phases with extra scrutiny
3. Report -> Security-specific findings with compliance mapping
4. Suggest -> Plan for remediating all findings before SOC 2 audit
```

### Example 3: Performance audit
```
User: /audit Our app is slow, audit the performance

Audit workflow:
1. scout -> Inventory with focus on bundle size, API routes, DB queries
2. Performance deep dive -> Bundle analysis, runtime patterns, API review
3. Report -> Ranked performance findings with estimated impact
4. Suggest -> Top 5 optimizations with expected improvement
```

## Guardrails

- **Read-only by default.** Audit reports findings but does not change code unless explicitly asked.
- **Always complete the full scope.** If the user asks for a "full audit," run all four dimensions.
- **Severity must be justified.** Every finding needs a clear explanation of why it's rated at that severity.
- **Findings must be actionable.** Every finding needs a remediation recommendation.
- **No false positives.** Verify findings before reporting. A false alarm erodes trust.
- **Respect scope constraints.** If the user says "security only," don't report code quality issues (but mention if you notice critical non-security issues).
- **Maintain confidentiality.** If the audit finds secrets, report their presence without displaying the actual values.
