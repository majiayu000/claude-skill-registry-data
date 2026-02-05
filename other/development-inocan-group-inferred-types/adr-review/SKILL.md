---
name: adr-review
description: Use when reviewing code for Architecture Decision Record (ADR) compliance during refactoring or code review - checks code against all project ADRs and reports violations with specific fixes
---

# ADR Review

## Overview

**Review code for compliance with Architecture Decision Records (ADRs).**

ADRs document architectural decisions (test structure, naming conventions, error handling patterns). This skill guides systematic review of code against those decisions.

**Core principle:** ADRs are team agreements. Code must comply. Period.

## The Iron Law

```
AGENTS CANNOT CHANGE OR IGNORE ADRs
```

Your job: Report compliance status.
NOT your job: Decide if ADR is wrong, doesn't apply, or should be ignored.

**Authority boundary:**
- You report: "Code violates ADR-001 at line X"
- Supervisor decides: Whether to fix code or update ADR
- You never decide: "This ADR doesn't make sense here, so I'll ignore it"

## When to Use

**Use during:**
- REFACTOR phase of TDD (after tests pass)
- Code review before merge
- After implementing feature
- When establishing new ADR compliance

**Don't use:**
- Before tests pass (behavior correctness first)
- For subjective style preferences (only documented ADRs)
- When no ADRs exist (create them first)

## The Review Process

### Step 1: Find All ADRs

```bash
# Locate ADR directory (common locations)
docs/adr/
doc/architecture/decisions/
.adr/
```

Read ALL ADR files - you need complete picture of standards.

### Step 2: Identify Code to Review

What changed?
- New files added
- Functions modified
- Tests written

Review scope = what's new or changed.

### Step 3: Check Each ADR

For each ADR, ask:
1. **Does this ADR apply to the code under review?**
   - If clearly no, skip to next ADR
   - If uncertain, REPORT IT (don't decide yourself)
   - If yes, proceed to check

2. **What does the ADR require?**
   - Read the "Decision" section carefully
   - Note specific rules, patterns, conventions

3. **Does the code comply?**
   - Check each requirement against code
   - Note line numbers for violations
   - Note what's done correctly too

### Step 4: Report Findings

**Format:**

```markdown
## ADR Review: [File/Feature Name]

### ADR: [ADR-001-name]

**Status:** COMPLIANT / PARTIAL / VIOLATION

**Applies to:** [which parts of code]

**Compliant:**
- ✓ [What was done correctly]

**Violations:**
- ❌ Line X: [What's wrong]
  - Current: [actual code/pattern]
  - Required by ADR: [what ADR requires]
  - Fix: [specific change needed]

**Questions for supervisor:**
- [If ADR seems problematic, note here - don't decide yourself]
```

## Common Rationalizations (All Wrong)

| Excuse | Reality |
|--------|---------|
| "ADR doesn't make sense for this case" | Report it. Supervisor decides if ADR needs updating. |
| "Spirit vs letter - I'll follow spirit" | Follow the letter. That's what's written. |
| "Small violation, won't matter" | Small violations create inconsistency. Report all. |
| "ADR is outdated/wrong" | Not your decision. Report violation, note concern. |
| "This is a special case" | Report it as exception needing supervisor review. |
| "Team won't care about this" | Team wrote the ADR. They care. Report it. |
| "Too much work to fix" | Not a review concern. Report violation. |
| "Previous code violates it too" | Report that too. Don't compound violations. |
| "I found a better pattern" | Report to supervisor. Don't ignore ADR. |

**Seeing yourself in this table? STOP. Report the violation without deciding it's acceptable.**

## Review Checklist

For each ADR:
- [ ] Read ADR completely
- [ ] Determine if it applies (if uncertain, report)
- [ ] Check each requirement in ADR "Decision" section
- [ ] Note line numbers for issues
- [ ] Provide specific fix showing compliance
- [ ] Acknowledge what's done correctly
- [ ] Report concerns without making decisions

## Being Strict vs Fair

**Be strict on:**
- Explicit requirements in ADR "Decision"
- Patterns shown in ADR examples
- Rules stated as "must" or "required"
- Anything written in the ADR

**Be fair on:**
- Provide clear fix guidance
- Acknowledge compliant aspects
- Note when ADR might need clarification

**Never accept:**
- "Spirit vs letter" arguments (follow letter)
- "Good enough" for explicit violations
- "No one will notice" reasoning
- "Special case" without supervisor approval

## Handling Ambiguity

**If ADR is unclear:**

```markdown
**Question for supervisor:**
ADR-001 requires X, but unclear how this applies to Y case.

Options:
1. Interpret as: [option A]
2. Interpret as: [option B]

Recommend supervisor clarify ADR-001 for this scenario.

For now, flagging as potential violation.
```

**Don't:**
- Pick interpretation yourself
- Decide "close enough"
- Apply "common sense" override

**Do:**
- Present options clearly
- Ask supervisor to decide
- Flag as needs-clarification

## Common ADR Types

### Structural ADRs
Test structure, file organization, module boundaries

**Review for:**
- Correct nesting/hierarchy
- Naming follows convention
- Files in right locations

### Pattern ADRs
Error handling, async patterns, state management

**Review for:**
- Pattern used correctly
- No anti-patterns
- Consistent with examples

### Style ADRs
Naming conventions, documentation, formatting

**Review for:**
- Names follow convention
- Required docs present
- Format matches standard

## Violation Severity

Report all violations, but categorize by severity:

**BLOCKING:** Cannot merge until fixed
- Explicit ADR requirement violated
- Creates inconsistency with established pattern
- Example: Wrong test structure per ADR-001

**WARNING:** Should fix before merge
- Minor deviation from pattern
- Ambiguous ADR interpretation
- Example: Test name less specific than ADR suggests

**NOTE:** Consider for future
- Enhancement beyond ADR requirements
- Potential ADR improvement discovered
- Example: Pattern could be clearer

**Never:**
- Downgrade blocking to warning because "it's close enough"
- Promote warning to blocking because you personally prefer it
- Skip noting issues because "too minor"

## Integration with TDD

**In REFACTOR phase:**

```
1. Tests pass (GREEN)
2. Dispatch reviewer with adr-review skill
3. Reviewer reports violations
4. Supervisor decides: fix code or update ADR
5. Fix violations
6. Re-run tests (ensure still GREEN)
7. Commit
```

**Why after GREEN, not before:**
- Behavior correctness proven first
- ADR compliance is structural, not functional
- Separates concerns: "does it work?" vs "is it right?"

## Example Review

```markdown
## ADR Review: getChangedFiles() implementation

### ADR-001: Test Structure

**Status:** PARTIAL COMPLIANCE

**Applies to:** api/test/jj.test.ts lines 67-75

**Compliant:**
- ✓ Uses describe blocks for circumstances (line 68)
- ✓ Uses test blocks for assertions (line 69)
- ✓ Present tense in describe blocks

**Violations:**

**BLOCKING:**
- ❌ Line 69: Test name too generic
  - Current: `test("throws error", async () => {`
  - Required by ADR: "State what the function does" explicitly
  - Fix: `test("throws error with message 'No repository set'", async () => {`

**WARNING:**
- ⚠️ Line 68: Uses beforeEach hook
  - Current: `beforeEach(() => { cleanup(); });`
  - ADR philosophy: "self-contained tests" over hidden setup
  - Suggestion: Move cleanup() into each test explicitly
  - Note: ADR doesn't explicitly forbid beforeEach, but philosophy suggests avoiding

**Questions for supervisor:**
- Should ADR-001 explicitly address beforeEach usage?
- Current wording is ambiguous for this scenario
```

## Red Flags - You're Rationalizing

**STOP if you catch yourself thinking:**
- "This ADR is outdated"
- "ADR doesn't cover this case"
- "Close enough to compliant"
- "Spirit not letter"
- "Small violation doesn't matter"
- "Too much work to be strict"
- "I found a better way"
- "This is a special case"
- "Previous code also violates it"
- "Team won't care"

**All of these mean:** You're deciding instead of reporting. Stop. Report the violation and let supervisor decide.

## When ADR Seems Wrong

**If you discover ADR is problematic:**

```markdown
**Note for supervisor discussion:**

ADR-001 requires X, but this creates Y problem in this scenario.

Evidence:
- [Specific issue with following ADR]
- [Why it seems problematic]

Recommendation: Team should discuss updating ADR-001 to handle Z scenario.

**For now: Code violates ADR-001.** Flagging as BLOCKING until supervisor decides:
1. Fix code to comply, or
2. Update ADR-001 to allow this pattern
```

**Critical: You still flag it as violation.** You don't approve the violation because ADR seems wrong.

## The Bottom Line

**Your job: Report compliance status accurately.**

Not your job:
- Decide if ADR is right
- Determine if ADR applies
- Choose when to ignore ADR
- Interpret ambiguous ADRs
- Make exceptions for "special cases"

**When in doubt: Flag it and ask supervisor.**

Better to over-report than to make unauthorized exceptions.

ADRs are team agreements. Changing them is a team decision. You enforce, you don't decide.
