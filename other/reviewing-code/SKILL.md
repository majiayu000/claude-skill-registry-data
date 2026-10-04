---
name: reviewing-code
description: Conducts systematic code review with quality checks, architectural verification, and actionable feedback. Use when reviewing pull requests, code changes, or ensuring code quality standards.
---

# Code Review Framework

## Core Principles

- **Plan alignment first** - Implementation must match stated requirements
- **Technical rigor** - Verify claims, don't assume
- **Actionable feedback** - Specific issues with clear fixes
- **Prioritized findings** - Critical vs Important vs Minor
- **Constructive approach** - Acknowledge strengths, guide improvements

## Review Phases

### Phase 1: Plan Alignment Analysis

**Purpose**: Verify implementation matches original requirements.

**Process**:
1. Read the planning document, specification, or requirements
2. Review the implementation (git diff, changed files, new code)
3. Compare actual vs planned functionality
4. Identify deviations (both good and bad)

**Evaluate**:
- All planned functionality implemented?
- Any missing features or partial implementations?
- Deviations from planned approach?
- Are deviations justified improvements or problematic departures?

**Output**: List of alignment issues with severity

---

### Phase 2: Code Quality Assessment

**Purpose**: Ensure code meets quality standards.

**Review Areas**:

#### Error Handling
- Proper try/catch blocks or error returns
- Meaningful error messages
- Graceful degradation
- Edge case handling

#### Type Safety
- Proper type annotations (TypeScript/typed languages)
- No `any` types without justification
- Correct use of generics
- Validated inputs/outputs

#### Code Organization
- Logical file structure
- Clear separation of concerns
- Appropriate module boundaries
- Consistent naming conventions

#### Maintainability
- Code is readable and self-documenting
- Complex logic has explanatory comments
- No unnecessary complexity
- DRY principle followed

**Output**: Quality issues categorized by area

---

### Phase 3: Architecture and Design Review

**Purpose**: Validate architectural soundness.

**Evaluate**:

#### SOLID Principles
- **S**ingle Responsibility: Each module/function has one job
- **O**pen/Closed: Extensible without modification
- **L**iskov Substitution: Subtypes are substitutable
- **I**nterface Segregation: No fat interfaces
- **D**ependency Inversion: Depend on abstractions

#### Design Patterns
- Appropriate patterns used correctly
- No anti-patterns present
- Patterns not overused or misapplied

#### Integration
- Integrates cleanly with existing systems
- API contracts respected
- Dependencies properly managed
- No tight coupling to implementation details

#### Scalability & Extensibility
- Can handle growth in data/users
- Easy to add new features
- Configuration externalized where appropriate
- No hard-coded limits that will break

**Output**: Architectural concerns with recommendations

---

### Phase 4: Testing Review

**Purpose**: Ensure adequate test coverage, quality, and TDD compliance.

#### TDD Compliance (FIRST CHECK)

**Verify tests were written BEFORE implementation:**

**Questions to ask:**

1. **Does each function/method have corresponding tests?**
   ```
   For each public function in implementation files:
   - [ ] Test file exists
   - [ ] Test covers function behavior
   - [ ] Test name clearly describes what's tested
   ```

   **If NO**: Flag as Important issue
   ```
   IMPORTANT: Missing tests for [function_name] in [file].
   All functions require tests. Add tests before merging.
   ```

2. **Request TDD Compliance Certification**

   Ask implementer to provide certification from practicing-tdd skill:

   "Please provide TDD Compliance Certification for each function
    (format from practicing-tdd skill)."

   **Verify:**
   - [ ] Certification provided for all new functions
   - [ ] All "Watched fail" are YES (or justified NO)
   - [ ] All "Watched pass" are YES
   - [ ] Failure reasons are specific (not vague)

   **If certification missing or incomplete**: Flag as Important issue
   ```
   IMPORTANT: TDD Compliance Certification required.
   Must provide certification with one entry per function (see practicing-tdd skill).
   Certification proves RED-GREEN-REFACTOR cycle was followed.
   ```

   **If author cannot provide certification**: Flag as Important issue
   ```
   IMPORTANT: Unable to verify TDD followed for [function_name].
   Tests may have been written after implementation.
   Recommend: Verify tests actually fail when implementation removed.
   ```

3. **Do tests fail when implementation removed?**

   **If suspicious that tests written after** (e.g., all tests pass immediately, no git history showing test-first):

   ```bash
   # Verify tests actually test implementation
   # Comment out implementation
   git stash  # Temporarily remove implementation
   npm test   # Tests should FAIL
   git stash pop  # Restore implementation
   ```

   **If tests still pass with no implementation**: Flag as Critical issue
   ```
   CRITICAL: Tests for [function_name] pass without implementation.
   Tests are not actually testing the code.
   See avoiding-testing-anti-patterns skill (Anti-Pattern 1: Testing Mock Behavior).
   Rewrite tests to verify real behavior.
   ```

4. **Does git history suggest test-first?**

   **Optional check** (not definitive, but helpful indicator):

   ```bash
   git log --oneline --all -- tests/[file].test.ts src/[file].ts
   ```

   **Look for:**
   - Test commits before implementation commits
   - Separate commits for RED → GREEN → REFACTOR
   - Commit messages mentioning TDD phases

   **If commits show implementation before tests**: Flag as Important issue
   ```
   IMPORTANT: Git history suggests tests written after implementation.
   Commits show [file].ts before [file].test.ts.
   Verify TDD was followed. If not, recommend rewriting with TDD.
   ```

5. **Are there any files with implementation but no tests?**

   ```bash
   # Find source files
   find src/ -name "*.ts" -o -name "*.js"

   # For each source file, check if test exists
   # tests/[name].test.ts or tests/[name].spec.ts
   ```

   **If source file has no corresponding test file**: Flag as Important issue
   ```
   IMPORTANT: No tests found for src/[file].ts
   All implementation files require tests.
   Add comprehensive tests before merging.
   ```

**TDD Compliance Summary:**

After checking above:

```markdown
### TDD Compliance: [PASS / NEEDS IMPROVEMENT / FAIL]

- Functions with tests: X / Y (Z% coverage)
- Author attestation to RED-GREEN-REFACTOR: [Yes / No / Partial]
- Tests verified to fail without implementation: [Yes / No / Not checked]
- Files without tests: [List or "None"]

[If NEEDS IMPROVEMENT or FAIL]:
Recommendations:
- Add tests for [list functions]
- Verify tests for [list functions] actually fail when implementation removed
- Consider rewriting [list functions] with TDD for higher confidence
```

#### Test Coverage
- All new code paths tested
- Edge cases covered
- Error paths tested
- Integration points verified

#### Test Quality
- Tests actually verify behavior (not just mock everything)
- Tests are isolated and independent
- Tests have clear arrange/act/assert structure
- Test names describe what they verify

#### Test Patterns and RED-GREEN-REFACTOR
- Appropriate use of mocks/stubs/fakes
- No test-only methods in production code
- Tests fail when they should (RED-GREEN-REFACTOR)

**See Also**: `avoiding-testing-anti-patterns` skill for what NOT to do, `practicing-tdd` skill for TDD process

**Output**: Testing gaps, quality issues, and TDD compliance status

---

### Phase 5: Security & Performance

**Purpose**: Identify vulnerabilities and performance issues.

**Security Review**:
- No SQL injection vulnerabilities
- No XSS vulnerabilities
- No command injection
- Proper authentication/authorization
- Sensitive data properly handled
- No secrets in code

**Performance Review**:
- No obvious N+1 queries
- Appropriate use of caching
- No unbounded loops or recursion
- Database queries optimized
- Async operations used appropriately

**Output**: Security and performance concerns

---

### Phase 6: Documentation Review

**Purpose**: Verify code is properly documented.

**Check**:
- Public APIs documented
- Complex algorithms explained
- Non-obvious decisions justified in comments
- README updated if needed
- Breaking changes documented

**Output**: Documentation gaps

---

## Issue Categorization

Categorize all findings by **Priority**:

### Critical (Must Fix Before Merge)
- Security vulnerabilities
- Data corruption risks
- Breaking existing functionality
- Missing core requirements
- Test failures

### Important (Should Fix Before Merge)
- Missing error handling
- Poor architecture that will cause problems
- Significant performance issues
- Missing important tests
- Plan deviations without justification

### Minor (Nice to Have)
- Style inconsistencies
- Minor optimizations
- Better naming suggestions
- Additional test coverage
- Documentation improvements

---

## Review Output Format

Structure your review as follows:

```markdown
# Code Review: [What Was Implemented]

## Summary

**Overall Assessment**: [Ready to merge / Needs fixes / Major revision needed]

**Strengths**:
- [What was done well]
- [Good decisions made]
- [Quality aspects worth noting]

**Issues Found**: [X] Critical, [Y] Important, [Z] Minor

---

## Critical Issues

### 1. [Issue Title]
**Location**: `file/path.ts:123-145`
**Issue**: [Specific problem with evidence]
**Impact**: [Why this is critical]
**Fix**: [Specific steps to resolve]

---

## Important Issues

### 1. [Issue Title]
**Location**: `file/path.ts:67`
**Issue**: [Specific problem]
**Why Important**: [Consequences if not fixed]
**Recommendation**: [How to fix]

---

## Minor Issues

### 1. [Issue Title]
**Location**: `file/path.ts:89`
**Suggestion**: [Improvement idea]
**Benefit**: [Why this would help]

---

## Plan Alignment

**Planned**: [What the plan said to do]
**Implemented**: [What was actually done]
**Deviations**:
- [Deviation 1]: [Justified/Problematic and why]
- [Deviation 2]: [Assessment]

---

## Testing Review

### TDD Compliance: [PASS / NEEDS IMPROVEMENT / FAIL]

**Findings:**
- Functions with tests: X / Y (Z% coverage)
- Author attestation to TDD: [Yes / No / Partial]
- Tests verified to fail without implementation: [Yes / No / Not checked]
- Files without tests: [List or "None"]

**Issues identified:**
[List TDD compliance issues here]

### Test Coverage

**Coverage**: [Percentage or qualitative assessment]
**Gaps**:
- [Untested scenario 1]
- [Untested scenario 2]

**Test Quality**: [Assessment]

---

## Recommendations

**Immediate Actions** (before merge):
1. [Action 1]
2. [Action 2]

**Future Improvements** (can defer):
1. [Improvement 1]
2. [Improvement 2]

---

## Approval Status

- [ ] Critical issues resolved
- [ ] Important issues addressed or acknowledged
- [ ] Tests passing
- [ ] Documentation updated

**Status**: [Approved / Approved with minor items / Needs revision]
```

---

## Integration with Workflows

### Requesting Review

See `requesting-reviewing-code` skill for how to invoke this review process.

**When to review**:
- After completing each task (subagent-driven development)
- After major features
- Before merging to main
- When stuck (fresh perspective)

### Receiving Review

See `receiving-reviewing-code` skill for how to handle review feedback.

**Key principles**:
- Verify before implementing
- Ask for clarification if unclear
- Push back with technical reasoning if reviewer is wrong
- No performative agreement

### Integration with Other Skills



## Workflow Checklist

Copy this checklist to track your progress:

See `assets/workflow-checklist.md` for the complete checklist.

## References


For detailed information, see:

- `references/detailed-guide.md` - Complete workflow details, examples, and troubleshooting
