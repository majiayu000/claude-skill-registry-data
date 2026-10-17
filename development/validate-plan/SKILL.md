---
name: validate-plan
description: Validate implementation plans against DRY, YAGNI, TDD principles and best practices. Use when reviewing plans from pocket-planning or another planning workflow to identify gaps, anti-patterns, and improvement opportunities before execution.
category: planning
---

# Validate Plan

## Overview

Comprehensive validation workflow for development implementation plans. This skill systematically analyzes plans against DRY (Don't Repeat Yourself), YAGNI (You Aren't Gonna Need It), and TDD (Test-Driven Development) principles while performing codebase-aware gap analysis to prevent implementation disasters.

**Use when:**
- Reviewing implementation plans created by the Pocket planning workflow or another source
- Validating development plans before execution
- Checking plans for DRY/YAGNI/TDD compliance
- Preventing over-engineering and scope creep
- Ensuring test-first approach in development workflow

**Triggers:** `/validate-plan` or "Validate this implementation plan"

---

## Validation Workflow

### Step 1: Plan Discovery

Accept either a plan file path or plan text supplied directly in the request. When invoked as a non-interactive reviewer (including the hotfix reviewer dispatch), use the supplied inline plan and do not ask questions or request a file path. If neither a path nor plan text is available in an interactive session, ask the user which plan to review.

For a file path:
1. Load plan file
2. Extract metadata: feature name, tech stack, hypothesis
3. Identify all tasks and their structure

For inline plan text, perform the same analysis from the supplied content without looking for or editing a plan file.

### Step 2: Codebase Analysis

**Scan existing codebase for:**
- Existing implementations of similar functionality
- Reusable components, utilities, patterns
- Project structure and conventions
- Test patterns and frameworks
- Previous implementations that could be referenced

**Key questions:**
- What functionality already exists that could be reused?
- What patterns are established in the codebase?
- Where should new files be placed?
- What testing approach is already used?

### Step 3: DRY Validation

**Checklist for Don't Repeat Yourself:**

| Check | Description | Finding Level |
|-------|-------------|---------------|
| **Functionality Check** | Does the plan propose implementing functionality that already exists? | CRITICAL |
| **Code Reuse** | Are there existing utilities/components that could be reused? | CRITICAL |
| **Abstraction** | Does the plan duplicate similar patterns without abstraction? | WARNING |
| **Library Choice** | Is the plan using the same libraries already in the project? | INFO |

**Common DRY violations to detect:**
- Creating new validation logic when validation utilities exist
- Reimplementing API clients when shared clients exist
- Duplicating UI components instead of extending existing ones
- Writing new auth logic when auth system exists

### Step 4: YAGNI Validation

**Checklist for You Aren't Gonna Need It:**

| Check | Description | Finding Level |
|-------|-------------|---------------|
| **Over-abstraction** | Does the plan create abstractions without concrete use cases? | WARNING |
| **Future-proofing** | Are there features planned for hypothetical future needs? | WARNING |
| **Complexity** | Is the solution more complex than the problem requires? | CRITICAL |
| **Scope Creep** | Are there tasks outside the core requirement? | WARNING |

**Common YAGNI violations to detect:**
- Creating plugin architectures when no plugins are planned
- Adding configuration options that won't be changed
- Building admin interfaces before user features are proven
- Optimizing for scale before product-market fit

### Step 5: TDD Validation

**Checklist for Test-Driven Development:**

| Check | Description | Finding Level |
|-------|-------------|---------------|
| **Test-First** | Are tests written BEFORE implementation? | CRITICAL |
| **Red-Green** | Does each task follow red-green-refactor cycle? | CRITICAL |
| **Test Commands** | Are exact test commands specified with expected output? | WARNING |
| **Coverage** | Is there a clear testing strategy for each component? | WARNING |
| **Commits** | Are commits tied to test milestones? | INFO |

**TDD Anti-patterns to detect:**
- "Write tests" as a separate task at the end
- Implementation without corresponding test steps
- Vague test instructions without expected outcomes
- Missing edge case testing

### Step 6: Gap Analysis

**Technical Specification Gaps:**
- Missing exact file paths
- Unclear acceptance criteria
- Vague implementation details
- Missing error handling specifications
- No rollback/contingency plans

**Architecture Gaps:**
- Wrong file locations (violating project structure)
- Missing integration patterns
- No database schema changes specified
- Missing API contract details

**Disaster Prevention:**
- Breaking changes not identified
- Missing security considerations
- No performance requirements
- Missing dependency analysis

### Step 7: Generate Validation Report

Assign an overall grade using this rubric:

| Grade | Criteria |
|-------|----------|
| **A** | No critical issues or warnings; any findings are informational only. |
| **B** | No critical issues and one or two warnings. |
| **C** | No critical issues and three or more warnings. |
| **D** | Exactly one critical issue. |
| **F** | Two or more critical issues, or a critical security/safety issue that makes execution unsafe. |

A critical finding always makes the verdict **BLOCKED**, regardless of the grade. With no critical findings, the verdict is **APPROVED**; warnings may still need an explicit exception or plan change before execution.

**Report Structure:**

```markdown
# Plan Validation Report: [Feature Name]

## Executive Summary
- **Critical Issues:** [N] blockers must be fixed
- **Warnings:** [N] improvements recommended
- **Info:** [N] suggestions for enhancement
- **Overall Grade:** [A-F]
- **VERDICT:** [APPROVED or BLOCKED]

## DRY Analysis
[Findings with specific recommendations]

## YAGNI Analysis
[Findings with specific recommendations]

## TDD Analysis
[Findings with specific recommendations]

## Gap Analysis
[Missing requirements and potential disasters]

## Codebase Context
[Reusable components, patterns found]

## Findings
### CRITICAL
- [Blockers, or "None"]

### WARNING
- [Recommended fixes, or "None"]

### INFO
- [Optional suggestions, or "None"]

## Verdict
Emit exactly one verdict line: `VERDICT: APPROVED` when there are no critical findings, or `VERDICT: BLOCKED` when one or more critical findings remain.
```

### Step 8: Optional Plan Changes (Interactive Mode Only)

Validation is read-only by default. Never rewrite a plan automatically, make edits merely to make them "look natural," or continue directly to execution after changing a plan.

This step is available only when the user is interacting directly. For an inline plan or subagent review, skip this step and return the report without asking questions or modifying files.

**Present findings to user:**

```
🎯 **PLAN VALIDATION COMPLETE**

Found [N] critical issues, [N] warnings, [N] info suggestions.

## 🚨 CRITICAL (Must Fix)
1. [Issue with specific location in plan]
2. [Issue with recommendation]

## ⚡ WARNINGS (Should Fix)
1. [Warning with explanation]

## ✨ INFO (Nice to Have)
1. [Suggestion]

**IMPROVEMENT OPTIONS:**
- **all** - Select all proposed changes for review
- **critical** - Select critical fixes for review
- **select** - Select specific findings for review
- **none** - Keep plan unchanged
- **details** - Show more details
```

After the user selects changes, show the proposed unified diff and wait for the user's explicit approval before writing to the plan file. Preserve the surrounding format and structure. Do not save changes to an inline plan unless the user provides a destination and explicitly approves the diff.

If an approved Pocket plan is changed, set its existing approval/status marker to unapproved using the plan's established format. If it has no such marker, add a clear note that validation edits require another `pocket-planning` Spec Reviewer review before the plan can be treated as approved. Do not proceed to structuring or development; return the changed plan to `pocket-planning` for review, including its recovery checkpoint limits.

If the user declines or has not approved the diff, leave the source plan unchanged.

---

## Validation Principles

### DRY - Don't Repeat Yourself

**Principle:** Every piece of knowledge must have a single, unambiguous representation.

**Validation Approach:**
- Search codebase for similar functionality
- Identify reuse opportunities
- Flag duplicate logic patterns
- Check for existing abstractions

**Questions to Ask:**
1. Is this functionality already implemented elsewhere?
2. Can this use existing utilities/components?
3. Should this be a shared abstraction?
4. Is this the right place for this logic?

### YAGNI - You Aren't Gonna Need It

**Principle:** Don't implement functionality until it's actually needed.

**Validation Approach:**
- Check for speculative features
- Identify over-engineering
- Flag premature optimization
- Detect scope creep

**Questions to Ask:**
1. Is this feature required for the current scope?
2. Is this abstraction solving a real problem?
3. Will this configuration ever be changed?
4. Is this optimization necessary now?

### TDD - Test-Driven Development

**Principle:** Write tests before implementation; red-green-refactor cycle.

**Validation Approach:**
- Verify test-first approach
- Check for red-green-refactor steps
- Validate test coverage
- Ensure commit granularity

**Questions to Ask:**
1. Is the test written before the implementation?
2. Does the plan specify expected test failures?
3. Are test commands exact with expected output?
4. Are commits at test milestones?

---

## Example Usage

### Input: Plan to Validate

```markdown
# User Authentication Implementation Plan

**Goal:** Add user login functionality

### Task 1: Create Login Component

**Files:**
- Create: `src/components/LoginForm.tsx`

**Step 1: Write test**
```typescript
// Test login form renders
describe('LoginForm', () => {
  it('renders email and password inputs', () => {
    render(<LoginForm />);
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
  });
});
```

**Step 2: Run test to verify failure**
```bash
npm test LoginForm.test.tsx
```
Expected: FAIL - component not found

**Step 3: Implement minimal component**
```tsx
export function LoginForm() {
  return (
    <form>
      <input name="email" />
      <input name="password" type="password" />
    </form>
  );
}
```

**Step 4: Run test to verify pass**
```bash
npm test -- LoginForm.test.tsx
```
Expected: PASS

**Step 5: Commit**
```bash
git add src/components/LoginForm.tsx test/LoginForm.test.tsx
git commit -m "feat: add LoginForm component with tests"
```
```

### Output: Validation Report

```markdown
# Plan Validation Report: User Authentication

## Executive Summary
- **Critical Issues:** 0
- **Warnings:** 1
- **Info:** 1
- **Overall Grade:** B
- **VERDICT:** APPROVED

## DRY Analysis
- No duplicate functionality detected
- Consider using existing `Input` component from `src/components/ui/`

## YAGNI Analysis
- Clean implementation, no over-engineering detected

## TDD Analysis
- Follows red-green-refactor cycle
- The test command is specific and the expected result is PASS
- Minor: Add edge case test for invalid email format

## Codebase Context
- Existing `src/components/ui/Input.tsx` can be reused
- Auth utilities exist in `src/lib/auth.ts`
- Form validation pattern in `src/hooks/useForm.ts`

## Recommendations
1. **INFO:** Reuse `Input` component for consistency
2. **WARNING:** Add an error handling test case

The grade is B because this example contains one warning and no critical issues.
```

---

## Common Anti-Patterns to Detect

### Plan Structure Issues

1. **Missing acceptance criteria**
   - ❌ "Implement the feature"
   - ✅ "Feature accepts X input and returns Y output"

2. **Vague test instructions**
   - ❌ "Write tests"
   - ✅ "Write test: when input is invalid, show error message"

3. **Missing file paths**
   - ❌ "Create component"
   - ✅ "Create: `src/components/UserProfile.tsx`"

4. **Implementation without tests**
   - ❌ Write code → Test later
   - ✅ Write failing test → Make it pass → Refactor

### DRY Violations

1. **Reinventing utilities**
   - ❌ Create new `formatDate()` when `date-fns` is available
   - ✅ Use existing library

2. **Duplicate API logic**
   - ❌ New fetch wrapper per component
   - ✅ Use shared API client

### YAGNI Violations

1. **Premature abstraction**
   - ❌ "Create plugin system for future extensions"
   - ✅ Implement direct solution first

2. **Over-configuration**
   - ❌ "Add 10 config options"
   - ✅ Hardcode defaults, expose when needed

### TDD Violations

1. **Testing after implementation**
   - ❌ Task 1: Implement → Task 5: Add tests
   - ✅ Each task: Test → Implement → Commit

2. **Missing red phase**
   - ❌ "Write test and run it"
   - ✅ "Run test, verify it FAILS with expected error"

---

## Integration with Workflows

### With pocket-planning

After `pocket-planning` creates a plan:
1. User runs `/validate-plan`
2. Load the generated plan
3. Perform comprehensive validation
4. Report findings without changing the plan
5. If the user approves proposed edits, show the diff and wait for approval before saving
6. Return any changed Pocket plan to `pocket-planning` for a new Spec Reviewer review

### With pocket-structuring and pocket-development

After approval is confirmed by `pocket-planning`, the Pocket pipeline continues through `pocket-structuring` and `pocket-development`. A validation report alone does not approve a plan. Validated plans have:
- Clear, testable steps
- Exact file paths
- Verified DRY/YAGNI/TDD compliance
- Lower risk of implementation issues

---

## Resources

### references/
- `references/dry-principles.md` - Detailed DRY guidelines
- `references/yagni-checklist.md` - YAGNI detection patterns
- `references/tdd-patterns.md` - TDD workflow patterns
- `references/gap-analysis-guide.md` - Comprehensive gap analysis framework
