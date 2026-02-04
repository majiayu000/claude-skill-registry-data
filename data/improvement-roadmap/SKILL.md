---
name: improvement-roadmap
description: Structures actionable improvement recommendations to transform code from current state to 10/10 quality. Use when creating improvement plans, prioritizing technical debt, building remediation roadmaps, or after code quality assessments.
---

# Improvement Roadmap

Transform code quality assessments into actionable, prioritized improvement plans that guide codebases from their current score to a 10/10.

## Quick Start

**Create improvement roadmap:**
```
Based on this code quality assessment, create an improvement roadmap to reach 10/10
```

**Prioritize technical debt:**
```
Help me prioritize these issues by impact and effort
```

**Define milestones:**
```
Break this list of improvements into phases with clear milestones
```

## Roadmap Structure

Every improvement roadmap follows this six-phase structure:

```
1. CURRENT STATE SUMMARY
   Score breakdown by dimension (security, maintainability, etc.)
   Key metrics snapshot
   Critical blockers identified

2. TARGET STATE
   What 10/10 looks like for THIS specific codebase
   Concrete quality gates to achieve
   Expected metrics after improvements

3. CRITICAL FIXES (Phase 1)
   Security vulnerabilities
   Functionality blockers
   Data integrity issues
   Must fix before any other work

4. QUICK WINS (Phase 2)
   High impact, low effort
   Visible improvements to build momentum
   Often linting, formatting, simple refactors

5. MAJOR IMPROVEMENTS (Phase 3)
   High impact, high effort
   Architecture changes
   Large-scale refactoring
   New testing infrastructure

6. POLISH ITEMS (Phase 4)
   Getting from 9 to 10
   Documentation completeness
   Edge case handling
   Performance optimization
```

---

## Action Item Format

Every action item uses this structure:

```
[PRIORITY] [CATEGORY] [ESTIMATED SCORE IMPACT]
Issue: Specific problem description
Location: File(s) and line(s)
Fix: Concrete steps to resolve
Verification: How to confirm fixed
```

### Priority Levels

| Priority | Meaning |
|----------|---------|
| **P0** | Critical blocker - fix before anything else |
| **P1** | High priority - fix in current work cycle |
| **P2** | Medium priority - address after P0/P1 complete |
| **P3** | Low priority - address when core issues resolved |

### Categories

| Category | Scope |
|----------|-------|
| **SECURITY** | Vulnerabilities, auth, data protection |
| **RELIABILITY** | Error handling, edge cases, data integrity |
| **PERFORMANCE** | Speed, memory, scalability |
| **MAINTAINABILITY** | Code quality, complexity, coupling |
| **ORGANIZATION** | File structure, naming, architecture |
| **TESTING** | Coverage, quality, types of tests |
| **DOCUMENTATION** | Code comments, README, API docs |
| **ACCESSIBILITY** | WCAG compliance, keyboard nav, screen readers |

---

## Example Roadmap

### Current State Summary

```
Overall Score: 5.8/10

Dimension Breakdown:
- Security:        4/10 (SQL injection, no input validation)
- Reliability:     6/10 (missing error handling in API layer)
- Maintainability: 5/10 (high cyclomatic complexity, duplicated code)
- Organization:    5/10 (47 files in src/ root, no structure)
- Testing:         6/10 (40% coverage, no integration tests)
- Documentation:   8/10 (good README, inline comments sparse)

Critical Issues: 3
Major Issues: 12
Minor Issues: 28
```

### Target State (10/10)

```
- All inputs validated with Zod schemas
- Parameterized queries, no SQL injection vectors
- Error boundaries and graceful degradation
- <10 cyclomatic complexity per function
- Feature-based directory structure
- 80%+ test coverage with integration tests
- API documentation complete
```

### Phase 1: Critical Fixes

```
[P0] [SECURITY] [+1.0 points]
Issue: SQL injection in user search endpoint
Location: src/api/users.ts:45-52
Fix:
  1. Replace string concatenation with parameterized query
  2. Add input sanitization for search term
  3. Implement Zod schema for query params
Verification: SQL injection scanner shows no vulnerabilities

[P0] [SECURITY] [+0.5 points]
Issue: Hardcoded API keys in source code
Location: src/config.ts:12, src/services/payment.ts:8
Fix:
  1. Move to environment variables
  2. Add .env.example with placeholder values
  3. Update deployment docs
Verification: grep -r "sk_live_" returns no results
```

### Phase 2: Quick Wins

```
[P1] [ORGANIZATION] [+0.5 points]
Issue: 47 files in src/ root with no directory structure
Location: src/*.ts (all 47 files)
Fix:
  1. Create features/, shared/, types/ directories
  2. Move files by domain (auth -> features/auth/)
  3. Update all import paths
  4. Add barrel exports (index.ts)
Verification: No files in src/ root except index.ts, all imports work

[P1] [MAINTAINABILITY] [+0.3 points]
Issue: Inconsistent code formatting
Location: Entire codebase
Fix:
  1. Add Prettier config
  2. Run npx prettier --write .
  3. Add to pre-commit hook
Verification: npx prettier --check . passes

[P1] [MAINTAINABILITY] [+0.2 points]
Issue: No TypeScript strict mode
Location: tsconfig.json
Fix:
  1. Enable "strict": true
  2. Fix resulting type errors
  3. Enable noUncheckedIndexedAccess
Verification: tsc --noEmit passes with strict mode
```

### Phase 3: Major Improvements

```
[P2] [TESTING] [+0.8 points]
Issue: No integration tests for API endpoints
Location: tests/ (missing api tests)
Fix:
  1. Set up test database with Docker
  2. Create test fixtures and factories
  3. Write integration tests for each endpoint
  4. Add to CI pipeline
Verification: npm run test:integration passes, 80%+ coverage

[P2] [MAINTAINABILITY] [+0.5 points]
Issue: High cyclomatic complexity in order processing
Location: src/services/orders.ts (processOrder: complexity 25)
Fix:
  1. Extract validation to separate function
  2. Use strategy pattern for payment processing
  3. Extract inventory checks to dedicated service
  4. Add unit tests for each extracted function
Verification: escomplex shows <10 complexity per function
```

### Phase 4: Polish Items

```
[P3] [DOCUMENTATION] [+0.2 points]
Issue: API endpoints lack JSDoc documentation
Location: src/api/**/*.ts
Fix:
  1. Add JSDoc for all public functions
  2. Include @param and @returns
  3. Add usage examples for complex endpoints
Verification: TypeDoc generates complete API docs

[P3] [PERFORMANCE] [+0.3 points]
Issue: N+1 queries in user dashboard
Location: src/api/dashboard.ts:23
Fix:
  1. Add eager loading for user relations
  2. Implement DataLoader for batch queries
  3. Add query complexity analyzer
Verification: Query count reduced from 47 to 3 for dashboard load
```

---

## Prioritization Framework

Use the impact-effort matrix to order improvements.

See [references/prioritization-matrix.md](references/prioritization-matrix.md) for the complete framework including:
- Impact vs effort scoring
- Dependency mapping
- Quick win identification
- Risk-based ordering

---

## Milestone Templates

Structure phases into clear milestones with defined scope.

See [references/milestone-templates.md](references/milestone-templates.md) for:
- Critical milestone template (security/blockers)
- Quick wins milestone template (high impact, low effort)
- Major improvements milestone template (architecture changes)
- Polish milestone template (final refinements)
- Definition of done criteria

---

## Writing Action Items

Create specific, measurable, actionable items.

See [references/action-items.md](references/action-items.md) for:
- SMART criteria for action items
- Location specification patterns
- Verification method examples
- Common anti-patterns to avoid

---

## Score Impact Estimation

Estimate how each improvement affects the overall score.

See [references/score-tracking.md](references/score-tracking.md) for:
- Score dimension weights
- Impact calculation formulas
- Compound improvement effects
- Progress tracking templates

---

## Roadmap Presentation

### For Developers

```markdown
## Improvement Roadmap

### Phase 1: Critical Fixes
- [ ] Fix SQL injection vulnerability (+1.0)
- [ ] Remove hardcoded credentials (+0.5)
- [ ] Add input validation (+0.5)

### Phase 2: Quick Wins
- [ ] Organize directory structure (+0.5)
- [ ] Enable strict TypeScript (+0.2)
- [ ] Add Prettier config (+0.3)

**Expected Score After Phase 2: 5.8 -> 8.8**
```

### For Stakeholders

```markdown
## Technical Debt Remediation Plan

Current State: 5.8/10 (High technical debt)
Target State: 10/10 (Production-ready)

### Phases
1. **Security**: Fix critical vulnerabilities
2. **Quick Wins**: Build momentum with visible improvements
3. **Architecture**: Major refactoring
4. **Quality**: Testing and documentation

### Risk Mitigation
- All changes covered by tests
- Incremental deployment
- Rollback plan for each phase
```

---

## Roadmap Checklist

```markdown
## Roadmap Quality
- [ ] Current state clearly documented with metrics
- [ ] Target state is specific and measurable
- [ ] All items have priority, category, and impact
- [ ] Locations are specific (file:line)
- [ ] Fixes are concrete steps, not vague goals
- [ ] Verification methods are testable
- [ ] Dependencies between items are identified
- [ ] Quick wins are front-loaded for momentum

## Prioritization
- [ ] Critical/security issues in Phase 1
- [ ] High impact, low effort items in Phase 2
- [ ] Dependencies resolved before dependents
- [ ] Each phase has clear done criteria

## Tracking
- [ ] Score impact estimated per item
- [ ] Cumulative score projections included
- [ ] Milestone checkpoints defined
- [ ] Progress can be measured objectively
```

---

## Reference Files

- [references/prioritization-matrix.md](references/prioritization-matrix.md) - Impact vs effort framework
- [references/milestone-templates.md](references/milestone-templates.md) - Phase and milestone templates
- [references/action-items.md](references/action-items.md) - Writing specific, measurable action items
- [references/score-tracking.md](references/score-tracking.md) - Estimating and tracking score improvements
