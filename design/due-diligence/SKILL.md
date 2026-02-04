---
name: due-diligence
description: Comprehensive application audit. Analyzes best practices, security compliance, frontend design quality. Identifies top improvements and critical errors. Produces scores for design, code quality, and security.
---

# Due Diligence Skill

This skill performs a **comprehensive audit** of the finans application. You are a seasoned engineer conducting a thorough technical review.

**Output**: A detailed due-diligence report saved to `.docs/DUE-DILIGENCE-REPORT.md`

---

## Audit Scope

The audit covers six key areas:

1. **Best Practices Compliance** - Architecture, patterns, conventions
2. **Security Compliance** - OWASP, auth, data protection
3. **Frontend Design Quality** - Clean, simple, accessible
4. **Top 5 Valuable Improvements** - Highest ROI recommendations
5. **Top 5 Critical Errors** - Bugs, vulnerabilities, blockers
6. **Overall Scores** - Design, Code Quality, Security (0-100)

---

## Audit Workflow

### Phase 1: Codebase Exploration

Launch **5 parallel Explore agents with haiku model** using the Task tool.

See **Subagent Strategy** section below for exact Task parameters.

Each agent focuses on one area:
1. **Backend Architecture** - Routes, controllers, services, middleware, CosmosDB
2. **Frontend Architecture** - Features, components, state, routing, hooks
3. **Security Analysis** - Secrets, auth, validation, headers, OWASP
4. **Design Review** - CSS, typography, colors, responsive, accessibility
5. **Code Quality** - TypeScript, errors, duplication, formatting, imports

All 5 agents run in parallel and return structured findings.

### Phase 2: Findings Compilation

After exploration, compile findings into structured categories:

#### Best Practices Checklist

| Category | Items to Check |
|----------|----------------|
| **Architecture** | Monorepo structure, vertical slicing, separation of concerns |
| **TypeScript** | Strict mode, no implicit any, proper typing |
| **React** | Functional components, hooks patterns, state management |
| **Express** | Middleware chain, error handling, logging |
| **API Design** | REST conventions, response format, status codes |
| **Data Layer** | CosmosDB patterns, partition strategy, queries |
| **Styling** | CSS organization, design system adherence |
| **Testing** | E2E patterns only (no unit tests per CLAUDE.md) |
| **Documentation** | README, inline comments, API docs |
| **Dependencies** | Up-to-date, no vulnerabilities |

#### Security Checklist (OWASP Top 10)

| Risk | Items to Check |
|------|----------------|
| **A01: Broken Access Control** | Auth middleware on all routes, user isolation |
| **A02: Cryptographic Failures** | HTTPS only, no plaintext secrets |
| **A03: Injection** | Parameterized queries, input validation |
| **A04: Insecure Design** | Threat modeling, secure defaults |
| **A05: Security Misconfiguration** | Helmet, CORS, CSP headers |
| **A06: Vulnerable Components** | npm audit, outdated dependencies |
| **A07: Auth Failures** | EasyAuth validation, session handling |
| **A08: Data Integrity** | Input validation, business validation |
| **A09: Logging Failures** | Security events logged, no sensitive data |
| **A10: SSRF** | URL validation, internal network protection |

#### Frontend Design Criteria

| Criteria | What to Check |
|----------|---------------|
| **Clarity** | Information hierarchy, scannable layout |
| **Simplicity** | Minimal UI, no clutter, focused interactions |
| **Consistency** | Design system adherence, reusable patterns |
| **Accessibility** | Semantic HTML, ARIA, keyboard navigation |
| **Responsiveness** | Mobile-first, breakpoints, touch targets |
| **Performance** | Bundle size, lazy loading, render efficiency |
| **Localization** | Norwegian text, number/date formatting |

### Phase 3: Score Calculation

Score each area from 0-100 based on findings:

**Scoring Rubric**:

| Score Range | Meaning |
|-------------|---------|
| 90-100 | Excellent - Industry best practices, production-ready |
| 80-89 | Good - Minor improvements needed, solid foundation |
| 70-79 | Acceptable - Some issues to address before production |
| 60-69 | Needs Work - Significant gaps, requires attention |
| 50-59 | Poor - Major issues, not production-ready |
| 0-49 | Critical - Fundamental problems, requires rework |

**Scoring Factors**:

**Design Score** (weight each 0-20):
- Visual consistency with design system
- Information hierarchy and clarity
- Responsive design implementation
- Accessibility compliance
- User experience flow

**Code Quality Score** (weight each 0-20):
- TypeScript correctness and strictness
- Architecture and separation of concerns
- Error handling and edge cases
- Code organization and DRY principles
- Documentation and maintainability

**Security Score** (weight each 0-20):
- Authentication implementation
- Authorization and access control
- Input validation and sanitization
- Dependency security (npm audit)
- Security headers and configuration

### Phase 4: Report Generation

Generate the due-diligence report with this structure:

```markdown
# Due Diligence Report - Finans Application

**Generated**: [date]
**Auditor**: Claude Code Due Diligence Skill
**Codebase Version**: [latest commit or date]

---

## Executive Summary

[2-3 paragraph overview of findings]

**Overall Assessment**: [One-line verdict]

| Area | Score | Status |
|------|-------|--------|
| Design | XX/100 | [Emoji] [Status] |
| Code Quality | XX/100 | [Emoji] [Status] |
| Security | XX/100 | [Emoji] [Status] |
| **Overall** | **XX/100** | [Emoji] [Status] |

---

## Best Practices Compliance

### ✅ What's Done Well
- [List of good practices observed]

### ⚠️ Areas for Improvement
- [List of gaps identified]

### Detailed Findings

#### Architecture
[Findings]

#### TypeScript Usage
[Findings]

#### React Patterns
[Findings]

#### API Design
[Findings]

#### Data Layer
[Findings]

---

## Security Compliance

### ✅ Security Strengths
- [List of good security practices]

### 🚨 Security Concerns
- [List of vulnerabilities or gaps]

### OWASP Top 10 Assessment

| Risk | Status | Notes |
|------|--------|-------|
| A01: Broken Access Control | ✅/⚠️/❌ | [Notes] |
| A02: Cryptographic Failures | ✅/⚠️/❌ | [Notes] |
| ... | ... | ... |

---

## Frontend Design Quality

### ✅ Design Strengths
- [List of design positives]

### ⚠️ Design Issues
- [List of design problems]

### Design System Compliance
[How well it follows Nordic Minimal]

### Accessibility Status
[WCAG compliance level]

---

## Top 5 Valuable Improvements

Ranked by ROI (effort vs. impact):

### 1. [Improvement Title]
**Impact**: High/Medium/Low
**Effort**: High/Medium/Low
**Description**: [What and why]
**Recommendation**: [Specific action]

### 2. [Improvement Title]
...

### 3. [Improvement Title]
...

### 4. [Improvement Title]
...

### 5. [Improvement Title]
...

---

## Top 5 Critical Errors

Ranked by severity:

### 🔴 1. [Error Title]
**Severity**: Critical/High/Medium
**Category**: Bug/Security/Performance/UX
**Location**: [File(s)]
**Description**: [What's wrong]
**Impact**: [What happens if unfixed]
**Fix**: [How to resolve]

### 🔴 2. [Error Title]
...

### 🟠 3. [Error Title]
...

### 🟠 4. [Error Title]
...

### 🟡 5. [Error Title]
...

---

## Scores Breakdown

### Design Score: XX/100

| Factor | Score | Notes |
|--------|-------|-------|
| Visual Consistency | X/20 | [Notes] |
| Information Hierarchy | X/20 | [Notes] |
| Responsive Design | X/20 | [Notes] |
| Accessibility | X/20 | [Notes] |
| User Experience | X/20 | [Notes] |

### Code Quality Score: XX/100

| Factor | Score | Notes |
|--------|-------|-------|
| TypeScript Correctness | X/20 | [Notes] |
| Architecture | X/20 | [Notes] |
| Error Handling | X/20 | [Notes] |
| Code Organization | X/20 | [Notes] |
| Documentation | X/20 | [Notes] |

### Security Score: XX/100

| Factor | Score | Notes |
|--------|-------|-------|
| Authentication | X/20 | [Notes] |
| Authorization | X/20 | [Notes] |
| Input Validation | X/20 | [Notes] |
| Dependency Security | X/20 | [Notes] |
| Security Config | X/20 | [Notes] |

---

## Recommendations Summary

### Immediate Actions (Do Now)
- [Critical fixes]

### Short-Term (Next Sprint)
- [High-priority improvements]

### Long-Term (Roadmap)
- [Strategic improvements]

---

## Appendix

### Files Reviewed
[List of key files analyzed]

### Tools Used
- Static analysis: ESLint, TypeScript compiler
- Security: npm audit, manual review
- Design: Visual inspection, accessibility checks

### Methodology
[Brief description of audit approach]
```

---

## Subagent Strategy

Use **parallel Explore agents with haiku** for fast exploration (Phase 1):

Launch 5 Task calls in a **single message** with these parameters:

```typescript
// Agent 1: Backend Analysis
Task({
  subagent_type: "Explore",
  model: "haiku",
  description: "Backend architecture analysis",
  prompt: `Analyze backend architecture for due diligence audit.
    Read: backend/src/index.ts, routes/, controllers/, services/
    Check: middleware (auth, error handling, rate limiting)
    Verify: API patterns, validation, error responses, CosmosDB integration
    Return: structured findings for best practices and security`
})

// Agent 2: Frontend Analysis
Task({
  subagent_type: "Explore",
  model: "haiku",
  description: "Frontend architecture analysis",
  prompt: `Analyze frontend architecture for due diligence audit.
    Read: frontend/src/features/, shared/components/
    Check: state management (TanStack Query, Context), hooks usage
    Verify: component patterns, routing, navigation
    Return: structured findings for code quality and patterns`
})

// Agent 3: Security Scan
Task({
  subagent_type: "Explore",
  model: "haiku",
  description: "Security vulnerability scan",
  prompt: `Perform security analysis for due diligence audit.
    Scan for: hardcoded secrets, API keys, exposed credentials
    Check: auth implementation (EasyAuth header validation)
    Verify: input validation, sanitization, CORS, CSP, security headers
    Look for: SQL injection, XSS, OWASP Top 10 vulnerabilities
    Return: security findings with severity levels`
})

// Agent 4: Design Review
Task({
  subagent_type: "Explore",
  model: "haiku",
  description: "Frontend design review",
  prompt: `Review frontend design for due diligence audit.
    Check: CSS architecture (Nordic Minimal compliance in design system)
    Verify: typography (Cormorant, DM Sans, JetBrains Mono usage)
    Check: color palette usage, responsive design patterns
    Verify: accessibility basics (semantic HTML, labels, ARIA)
    Return: design compliance findings`
})

// Agent 5: Code Quality Review
Task({
  subagent_type: "Explore",
  model: "haiku",
  description: "Code quality analysis",
  prompt: `Analyze code quality for due diligence audit.
    Check: TypeScript strictness (any types, explicit typing)
    Verify: error handling patterns, code duplication
    Check: consistent formatting, import organization
    Look for: DRY violations, dead code, complexity issues
    Return: code quality findings with locations`
})
```

**Key points**:
- All 5 agents launched in **one message** (parallel execution)
- Use `subagent_type: "Explore"` for fast codebase analysis
- Use `model: "haiku"` for speed (exploration doesn't need opus/sonnet)
- Each agent returns structured findings for compilation

Then use the main agent to compile findings and generate the report.

---

## Critical Rules

1. **BE THOROUGH** - Check every file that matters
2. **BE HONEST** - Don't sugarcoat issues
3. **BE SPECIFIC** - File paths, line numbers, exact problems
4. **BE ACTIONABLE** - Every finding has a recommendation
5. **USE TOOLS** - Read/Glob/Grep for analysis, never bash cat/grep

---

## Example Invocation

When user says "run due diligence" or invokes this skill:

1. Read CLAUDE.md for project context
2. Launch 5 parallel Explore agents (haiku) in **one message**
3. Collect findings from all agents
4. Calculate scores based on findings
5. Generate report to `.docs/DUE-DILIGENCE-REPORT.md`
6. Present summary to user

---

## Output Location

**Report saved to**: `.docs/DUE-DILIGENCE-REPORT.md`

Always save the full report. Present a summary in the conversation.


NOTES FROM THE USER:
- NO .env FILES ARE CHECKED IN. ALL .env FILES ARE IGNORED BY GIT.