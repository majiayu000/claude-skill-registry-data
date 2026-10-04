---
name: qa-testing
description: Comprehensive QA and testing methodology from Google (Chrome/Android scale, 2B+ users). Use when writing unit tests (Jest, Vitest), integration tests, E2E tests (Playwright, Cypress), performance tests (k6), security tests (OWASP), setting up test coverage, creating test plans, or coordinating UAT sign-off. Triggers on testing, test cases, test coverage, QA, E2E tests, unit tests, integration tests, or quality assurance.
---

# QA Testing - Comprehensive Testing Skills

**Purpose**: Complete testing methodology from Google's testing infrastructure team

**Agent**: Google QA Engineer
**Use When**: Phase 4 (Testing) - need comprehensive quality assurance

---

## Overview

This skill module provides comprehensive testing procedures used at Google to ensure quality at massive scale (2B+ users for Chrome, Android OS).

**Core Philosophy**:
- Test early, test often
- Automate everything
- Fast feedback (tests in <5 minutes)
- Zero flaky tests

---

## Available Reference Guides

### 1. Test Planning
**File**: `references/test-planning.md`

**Covers**:
- Creating comprehensive test plans
- Test strategy (unit, integration, E2E, performance, security)
- Test environment setup
- Test data preparation
- Success criteria definition

**When to Use**: Beginning of Phase 4 (Testing)

---

### 2. Test Automation
**File**: `references/test-automation.md`

**Covers**:
- Unit test writing (Jest, pytest)
- Integration test implementation (Supertest, REST Assured)
- E2E test automation (Playwright, Cypress)
- Visual regression testing (Percy, Chromatic)
- Test framework setup

**When to Use**: Week 2-3 of Testing phase

**Example Topics**:
- Frontend E2E with Playwright
- API integration tests
- Database integration tests
- Real-time WebSocket testing
- Mobile app testing (Appium, Espresso)

---

### 3. Performance Testing
**File**: `references/performance-testing.md`

**Covers**:
- Load testing with k6
- Stress testing
- Performance benchmarking
- Core Web Vitals optimization
- API performance testing

**When to Use**: Before deployment to production

**Example Scenarios**:
- Load test: 100 concurrent users
- Stress test: Find breaking point
- Benchmark: API < 500ms p95

---

### 4. Security Testing
**File**: `references/security-testing.md`

**Covers**:
- OWASP Top 10 testing
- SQL injection prevention
- XSS prevention
- CSRF protection
- Dependency vulnerability scanning (Snyk, npm audit)
- Penetration testing basics

**When to Use**: Before UAT and production deployment

**Tools Covered**:
- OWASP ZAP
- Snyk
- npm audit
- Security headers validation

---

### 5. UAT Coordination
**File**: `references/uat-coordination.md`

**Covers**:
- Creating UAT test scenarios
- Coordinating client testing
- Bug tracking and reporting
- UAT sign-off process
- Feedback incorporation

**When to Use**: Week 5 of Testing phase

**Templates Included**:
- UAT test plan
- Test scenario template
- Bug report template
- UAT sign-off checklist

---

## Quick Start

### For QA Engineer (you):

```bash
# Week 1: Test Planning
Read: references/test-planning.md
Create: Test plan for project
Setup: Test frameworks

# Week 2-3: Test Implementation
Read: references/test-automation.md
Write: Unit, integration, E2E tests

# Week 4: Performance & Security
Read: references/performance-testing.md
Read: references/security-testing.md
Execute: Load tests, security scans

# Week 5: UAT
Read: references/uat-coordination.md
Coordinate: Client testing
Verify: All acceptance criteria met
```

### For Other Agents:

**PM**: Review test plans, track testing progress
**Developers**: Write unit tests (refer to test-automation.md)
**BA**: Coordinate UAT (refer to uat-coordination.md)
**DevOps**: Integrate tests in CI/CD pipeline

---

## Test Pyramid (Google Standard)

```
       /\
      /  \     E2E Tests (10%)
     /____\    - Critical user journeys
    /      \   - Slow but high confidence
   /________\
  /          \ Integration Tests (30%)
 /____________\ - API tests, DB tests
/              \ - Medium speed
\______________/
\              / Unit Tests (60%)
 \____________/  - Fast, isolated
  \          /   - High coverage
   \________/
```

**Why this ratio?**
- Unit tests: Fast feedback (seconds), catch bugs early
- Integration: Verify components work together
- E2E: Verify critical paths work end-to-end

---

## Quality Gates Checklist

Before deployment approval:

```markdown
## Code Quality ✅
- [ ] Unit test coverage ≥ 80%
- [ ] All unit tests passing
- [ ] No code smells (SonarQube)

## Integration Testing ✅
- [ ] All API endpoints tested
- [ ] Database tests passing
- [ ] Third-party integration tests passing

## E2E Testing ✅
- [ ] Top 10 user flows tested
- [ ] No flaky tests
- [ ] Cross-browser testing done

## Performance ✅
- [ ] API p95 latency < 500ms
- [ ] Page load time < 2s
- [ ] Core Web Vitals: Good
- [ ] Load test passed (target concurrency)

## Security ✅
- [ ] OWASP Top 10 tested
- [ ] No critical vulnerabilities
- [ ] Dependency scan passed
- [ ] Security headers configured

## UAT ✅
- [ ] Client testing completed
- [ ] All critical scenarios passed
- [ ] Feedback incorporated
- [ ] UAT sign-off received

**QA Sign-Off**: _______________
**Date**: _______________
```

---

## Testing Tools (Google Tech Stack)

### Frontend Testing

**Browser automation — priority order (must respect)**

1. **Claude Chrome MCP** (`mcp__Claude_in_Chrome__*`) — PREFERRED when available. Drives the user's real Chromium via the Claude extension. Reuses live session (auth, cookies, extensions), fastest loop for interactive smoke tests and visual verification. Check availability via ToolSearch `{ query: "Claude_in_Chrome", max_results: 20 }` before declaring it unavailable.
2. **Playwright MCP** (`mcp__plugin_playwright_playwright__browser_*`) — FALLBACK when Chrome MCP unavailable, or when a headless/reproducible run is explicitly required.
3. **`npx playwright test`** — CI GATE. The committed E2E suite in `tests/e2e/` MUST be run via the CLI before sprint close, regardless of which MCP was used during dev. MCP screenshots alone do not close a sprint.

**Unit / component**
- **Jest**: Unit testing for JavaScript / TypeScript
- **Vitest**: Jest-compatible, faster — prefer for Vite-based projects
- **Testing Library** (React / Vue / Svelte): component-level interaction tests

**Other browser runners (only if project already uses them)**
- **Cypress**: keep if pre-existing; do not introduce alongside Playwright.

### API Testing
- **Supertest**: Node.js API testing
- **Postman**: Manual API testing
- **Pact**: Contract testing (microservices)

### Performance
- **k6**: Modern load testing
- **Lighthouse**: Web performance auditing
- **JMeter**: Traditional load testing

### Security
- **OWASP ZAP**: Automated security scanning
- **Snyk**: Dependency vulnerabilities
- **npm audit**: Node.js security

### Mobile
- **Appium**: Cross-platform mobile
- **Espresso**: Android native
- **XCUITest**: iOS native

---

## Google Testing Standards

**Coverage**: 80%+ for production code
**Speed**: Full test suite < 5 minutes
**Flakiness**: 0% - all tests must be reliable
**Documentation**: Every test has clear description

**Test Naming Convention**:
```typescript
describe('TodoService', () => {
  describe('createTodo', () => {
    it('should create todo with valid data', () => {
      // Test implementation
    });

    it('should throw error when title is empty', () => {
      // Test implementation
    });
  });
});
```

---

## Communication Templates

### Daily QA Status Update (to PM)
```
**Testing Progress**: Day 3 of Week 2
- Unit tests: 87% coverage (✅ target: 80%)
- Integration tests: 12/15 passing (⚠️ 3 fixing)
- E2E tests: Setup complete, writing scenarios

**Blockers**:
- Need staging environment for integration tests (ETA: tomorrow)

**Next 24h**:
- Complete integration test fixes
- Begin E2E test writing
```

### Weekly Quality Report
```markdown
## Week 2 Quality Report

**Test Execution**:
- Total tests: 450
- Passing: 445 (98.9%)
- Failing: 5 (under investigation)

**Coverage**: 87% (target: 80%) ✅

**Bugs Found**: 8
- P0: 0
- P1: 2 (both fixed)
- P2: 6 (4 fixed, 2 in progress)

**On Track**: Yes, UAT scheduled for Week 5
```

---

## Remember

🛡️ **Quality is not negotiable**
- Don't skip tests to meet deadlines
- Every bug caught in testing = user saved from bad experience
- Google ships to billions - quality matters

⚡ **Fast feedback wins**
- Developers need test results in minutes, not hours
- Optimize slow tests
- Run tests in parallel

🔄 **Zero tolerance for flaky tests**
- Flaky test = useless test
- Fix immediately or delete

---

**For detailed procedures, read the reference guides in `references/` folder**

**Created**: 2026-02-04
**Maintained By**: Google QA Engineer
**Review Cycle**: After each major project
