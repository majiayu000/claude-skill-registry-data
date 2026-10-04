---
name: code-review
description: >-
  Code review is time-consuming and inconsistent. Reviewers miss security
  issues, overlook edge cases, or focus on style over substance. Meanwhile, AI
  agents catch these mechanical issues instantly but can't judge business logic
  correctness, UX decisions, or architectural fit.
---
# AI-Assisted Code Review

> AI excels at catching what you miss. Humans excel at judging what matters.

## The Problem

Code review is time-consuming and inconsistent. Reviewers miss security issues, overlook edge cases, or focus on style over substance. Meanwhile, AI agents catch these mechanical issues instantly but can't judge business logic correctness, UX decisions, or architectural fit.

The mistake: treating AI review as a replacement for human review. The result: merged code with correct syntax but wrong behavior, or wasted time arguing with AI about subjective decisions.

The insight: AI and human reviewers have complementary strengths. Use both, for different purposes.

## The Pattern

### AI Review Strengths

AI is excellent at reviewing:

| Category | What AI Catches | Example |
|----------|----------------|---------|
| **Security** | SQL injection, XSS, exposed secrets, unsafe deserialization | `db.query("SELECT * FROM users WHERE id = " + userId)` |
| **Consistency** | Naming violations, pattern deviations, style drift | Function named `getUserData` when pattern is `getUser` |
| **Edge Cases** | Missing null checks, unhandled errors, boundary conditions | Array access without length check |
| **Resource Leaks** | Unclosed files, connections, event listeners | `fs.readFile()` without `.close()` |
| **Type Safety** | Missing validations, unsafe casts, implicit any | `JSON.parse()` without try/catch |
| **Accessibility** | Missing alt text, keyboard navigation, ARIA labels | `<button>` without accessible label |

### Human Review Strengths

Humans are excellent at reviewing:

| Category | What Humans Judge | Example |
|----------|------------------|---------|
| **Business Logic** | Does this implement the requirement correctly? | Discount calculation logic |
| **UX Decisions** | Is this the right user experience? | Error message clarity |
| **Architecture** | Does this fit the system design? | Adding state to a stateless service |
| **Tradeoffs** | Is this the right optimization? | Caching vs freshness tradeoff |
| **Context** | Does this break something elsewhere? | Changing API contract |
| **Intent** | Is this solving the right problem? | Feature vs actual user need |

### Two-Pass Review Workflow

**Pass 1: AI Review (5 minutes)**

1. Run AI review on diff first (faster, focused)
2. Get structured output: severity, confidence, category
3. Auto-fix trivial issues (formatting, imports, simple refactors)
4. Flag issues for human review

**Pass 2: Human Review (15-30 minutes)**

1. Review AI findings with medium/high confidence
2. Ignore low-confidence nitpicks
3. Focus on business logic, UX, architecture
4. Check test coverage and quality
5. Verify AI didn't hallucinate issues

### Diff-First Review Pattern

Review the diff before reviewing full files. Faster and more focused.

**Step 1: Get the diff**
```bash
gh pr diff 123 > changes.diff
```

**Step 2: AI review on diff**
```
Review this diff for security issues, edge cases, and resource leaks:

```diff
- const user = await db.users.findById(userId);
+ const user = await db.users.findById(userId).lean();
  return user;
```

Focus on: data exposure, performance impact, breaking changes
```

**Step 3: Context review if needed**
```
The change to .lean() looks safe, but show me the full @services/user.ts file to verify no code depends on Mongoose document methods.
```

### Structured Review Output

Request reviews in a consistent format for easier triage.

**Template:**
```
Review @api/users/route.ts for security and edge cases.

Format each finding as:
**[SEVERITY]** Category: Issue
- Line: X
- Problem: Description
- Fix: Specific suggestion
- Confidence: High/Medium/Low
```

**Example output:**
```
**[HIGH]** Security: SQL Injection
- Line: 42
- Problem: User input directly in SQL query
- Fix: Use parameterized query: db.query('SELECT * FROM users WHERE email = ?', [email])
- Confidence: High

**[MEDIUM]** Edge Case: Missing null check
- Line: 56
- Problem: user.profile accessed without checking if user exists
- Fix: Add if (!user) return null before accessing user.profile
- Confidence: High

**[LOW]** Style: Inconsistent naming
- Line: 23
- Problem: Function named getUserData but pattern is getUser
- Fix: Rename to getUser for consistency
- Confidence: Medium
```

### Review Checklist Template

Use this checklist for both AI and human review:

**Security (AI-first)**
- [ ] No hardcoded secrets, API keys, passwords
- [ ] Input validation on all user data
- [ ] SQL/NoSQL injection prevention (parameterized queries)
- [ ] XSS prevention (escaped output, Content-Security-Policy)
- [ ] Authentication/authorization checks on sensitive operations
- [ ] No sensitive data in logs or error messages

**Correctness (Human-first)**
- [ ] Implements the requirement as specified
- [ ] Handles all specified use cases
- [ ] Edge cases identified and handled
- [ ] Error messages are clear and actionable
- [ ] No breaking changes to public APIs

**Code Quality (AI-assisted)**
- [ ] Functions < 50 lines, cyclomatic complexity < 10
- [ ] No duplicate code (DRY violations)
- [ ] Consistent naming and patterns
- [ ] TypeScript types (no implicit any, proper generics)
- [ ] No console.log or debug code

**Testing (Human-first)**
- [ ] Tests cover happy path + edge cases
- [ ] Realistic test data (not foo/bar/baz)
- [ ] Tests behavior, not implementation
- [ ] No brittle mocks (mocking internals)
- [ ] New code increases coverage (target >80%)

**Performance (Human judgment)**
- [ ] No N+1 queries
- [ ] Appropriate caching strategy
- [ ] Large data sets handled efficiently
- [ ] No blocking operations in async code

**Accessibility (AI-assisted)**
- [ ] Semantic HTML elements
- [ ] Alt text on images
- [ ] Keyboard navigation works
- [ ] ARIA labels where needed
- [ ] Color contrast meets WCAG AA

### Confidence-Based Filtering

AI reviews often produce false positives. Filter by confidence.

**High Confidence (review immediately):**
- Security vulnerabilities (SQL injection, XSS, exposed secrets)
- Resource leaks (unclosed connections, memory leaks)
- Type errors (unsafe casts, missing validations)
- Unhandled errors (missing try/catch, no error boundary)

**Medium Confidence (review selectively):**
- Edge cases (null checks, boundary conditions)
- Performance issues (N+1 queries, missing indexes)
- Consistency violations (naming, patterns)
- Missing tests

**Low Confidence (ignore or batch review):**
- Style preferences (spacing, line breaks)
- Subjective naming suggestions
- "Could be refactored" without specific issue
- Nitpicks with no user impact

### Progressive Review Depth

Adjust review depth based on change risk.

| Change Type | Review Depth | Focus |
|------------|--------------|-------|
| **Docs/comments** | AI scan only | Spelling, accuracy, broken links |
| **Tests** | Light human review | Realistic data, behavior testing, coverage |
| **Refactoring** | Medium review | No behavior change, test coverage |
| **New features** | Full review | Security, correctness, architecture |
| **Security/auth** | Deep review + audit | Threat modeling, penetration testing |

## Anti-Patterns

### 1. Trusting AI Reviews Blindly

**Bad:**
```
AI says this is a security issue, so I'll fix it without understanding why.
```

**Why:** AI hallucinates vulnerabilities. Example: flagging `innerHTML` in a React component that's already using DOMPurify.

**Fix:**
```
AI flagged innerHTML as XSS risk. Verify:
1. Is user input actually in the HTML?
2. Is it sanitized (DOMPurify, escapeHtml)?
3. Is there a safer alternative (textContent, React children)?

If sanitized properly, add a comment explaining why it's safe and ignore the AI warning.
```

### 2. No Human Review

**Bad:**
```
AI review passed, merging.
```

**Why:** AI can't judge business logic, UX, or architectural fit.

**Fix:**
```
AI review checks security and edge cases. Human review checks:
- Does this solve the right problem?
- Is the UX clear?
- Does this fit our architecture?
- Are the tests sufficient?
```

### 3. Reviewing Too Much at Once

**Bad:**
```
Review this 2000-line PR that touches 47 files.
```

**Why:** Both AI and humans lose coherence. AI misses context. Humans skim and miss issues.

**Fix:**
```
Break into smaller PRs:
1. Refactor existing code (200 lines)
2. Add new models (150 lines)
3. Add API endpoints (300 lines)
4. Add UI components (250 lines)
5. Integration (100 lines)

Each PR is independently reviewable in 15-30 minutes.
```

### 4. Arguing With AI About Subjective Decisions

**Bad:**
```
AI: "This function should be named getUserProfile"
Human: "No, getUser is fine"
AI: "getUserProfile is more descriptive"
Human: "getUser matches our pattern"
[5 more rounds of arguing]
```

**Why:** AI doesn't have organizational context. You're wasting time.

**Fix:**
```
AI suggestions on subjective style: ignore unless they fix a real inconsistency.
Focus AI on objective issues: security, correctness, edge cases.
```

### 5. Reviewing Trivial Code

**Bad:**
```
Review this getter:
```typescript
get userId() {
  return this._userId;
}
```
```

**Why:** No value. AI will nitpick spacing. Human time wasted.

**Fix:**
```
Skip trivial code in review. Focus on:
- Business logic
- Security-sensitive code
- Public APIs
- Complex algorithms
- Error handling

Trivial getters/setters: auto-approve.
```

### 6. Ignoring Test Quality

**Bad:**
```
Tests pass, looks good!
```

**Why:** Tests might be brittle, unrealistic, or testing implementation instead of behavior.

**Fix:**
```
Review test quality:
- Do they test behavior (what) not implementation (how)?
- Is test data realistic (real names, not foo/bar)?
- Do they cover edge cases, not just happy path?
- Are they maintainable (no brittle mocks)?

Bad test is worse than no test. It gives false confidence.
```

### 7. Missing Context Review

**Bad:**
```
This function looks fine in isolation.
```

**Why:** Change might break callers, violate contracts, or duplicate existing functionality.

**Fix:**
```
Review in context:
1. Where is this function called?
2. Does it match the existing pattern?
3. Is there already a function that does this?
4. Does this break any contracts (API, types, behavior)?

Use git blame and code search to find callers.
```

## Practical Workflow

### Daily PR Review Routine

**Morning (30 minutes):**
1. Run AI review on all open PRs in background
2. Review AI findings: triage by severity/confidence
3. Auto-fix trivial issues (formatting, imports)
4. Flag high-severity issues for human review

**Afternoon (1 hour):**
1. Human review of flagged PRs
2. Check business logic, UX, architecture
3. Verify test coverage and quality
4. Request changes or approve
5. Merge approved PRs

### Review Request Template

```
## Changes
Brief description of what changed and why.

## Review Focus
What reviewers should pay attention to:
- [ ] New auth flow (security critical)
- [ ] Database schema changes (breaking?)
- [ ] API contract changes (versioned?)

## AI Review
Ran AI review, addressed:
- Fixed SQL injection in user query (line 42)
- Added null check on user.profile (line 56)
- Renamed getUserData → getUser (line 23)

## Testing
- Added 12 tests (happy path + edge cases)
- Coverage: 87% → 91%
- All tests pass

## Deployment Notes
- Requires database migration (migrations/007_add_teams.sql)
- No breaking changes to API
- Feature flag: ENABLE_TEAMS (default false)
```

### Review Response Template

```
## Security ✅
- No hardcoded secrets
- Input validation on all endpoints
- Parameterized queries

## Correctness ⚠️
- Business logic looks correct for team creation
- **Question:** Line 78 - should team owners be able to delete their own team? Requirements unclear.

## Code Quality ✅
- Functions < 50 lines
- Consistent naming
- No duplication

## Testing ⚠️
- Happy path covered
- **Missing:** Edge case test for deleting team with active members

## Architecture ✅
- Fits existing pattern
- No breaking changes
- Proper separation of concerns

## Changes Requested
1. Clarify team deletion permissions in line 78
2. Add test for deleting team with members

Otherwise looks good!
```

## Measuring Review Effectiveness

Track these metrics:

- **False positives:** AI findings that weren't real issues (target: <20%)
- **Escaped bugs:** Issues found in production that review missed (target: <5%)
- **Review time:** Time from PR open to approval (target: <24 hours)
- **Rework rate:** PRs requiring multiple rounds of changes (target: <30%)

If false positives are high: tune AI review sensitivity, ignore low-confidence findings.

If escaped bugs are high: add more human review depth, expand test coverage.

If review time is high: reduce PR size, automate more checks, batch low-priority reviews.

AI review is a tool, not a replacement. Use it to catch what humans miss. Use humans to judge what AI can't.
