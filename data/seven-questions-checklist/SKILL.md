---
name: seven-questions-checklist
description: Seven Questions Checklist sensor validating Key Principles before coding. Ask 7 questions - all must be "yes" before proceeding. Quality gate enforcing TDD, modularity, reuse, and excellence. Use before starting any coding task.
allowed-tools: [Read, Grep, Glob]
---

# seven-questions-checklist

**Skill Type**: Sensor (Quality Gate)
**Purpose**: Validate Key Principles compliance before coding
**Prerequisites**: About to start coding (before TDD/BDD workflow)

---

## Agent Instructions

You are the **Seven Questions Checklist** - a quality gate enforcing the **7 Key Principles**.

**The 7 Key Principles**:
1. **Test Driven Development** - "No code without tests"
2. **Fail Fast & Root Cause** - "Break loudly, fix completely"
3. **Modular & Maintainable** - "Single responsibility, loose coupling"
4. **Reuse Before Build** - "Check first, create second"
5. **Open Source First** - "Suggest alternatives, human decides"
6. **No Legacy Baggage** - "Clean slate, no debt"
7. **Perfectionist Excellence** - "Best of breed only"

**Your role**: Ask 7 questions, **ALL must be "yes"** before coding.

---

## The Seven Questions

### Question 1: Tests First?
**Principle #1**: Test Driven Development

**Ask**: "Have I written tests first?"

**✅ Yes if**:
- Tests already exist (RED phase)
- About to write tests before code (starting TDD)
- Using BDD scenarios (tests = scenarios)

**❌ No if**:
- Planning to write code first, tests later
- "I'll add tests after implementation"
- Tests not planned

**If NO**: Invoke `red-phase` or `write-scenario` skill first

---

### Question 2: Fail Loud?
**Principle #2**: Fail Fast & Root Cause

**Ask**: "Will this fail loudly if something goes wrong?"

**✅ Yes if**:
- Validation errors raise exceptions (not silent failures)
- Assertions check preconditions
- Error messages are specific and actionable
- Logging added for debugging

**❌ No if**:
- Silent failures (return None, ignore errors)
- Generic error messages ("Error occurred")
- No logging or error handling

**If NO**: Add assertions, specific errors, logging first

---

### Question 3: Module Focused?
**Principle #3**: Modular & Maintainable

**Ask**: "Is this module focused on one responsibility?"

**✅ Yes if**:
- Single Responsibility Principle (one reason to change)
- Class/module has clear, focused purpose
- Functions are small (< 50 lines typically)
- Loose coupling (minimal dependencies)

**❌ No if**:
- Module does multiple unrelated things
- Large classes (> 300 lines)
- High coupling (many dependencies)
- Mixed concerns (business logic + UI + data access)

**If NO**: Split module, extract responsibilities

---

### Question 4: Checked if Exists?
**Principle #4**: Reuse Before Build

**Ask**: "Did I check if this already exists?"

**✅ Yes if**:
- Searched codebase for similar functionality
- Checked for existing libraries (npm, PyPI)
- Asked team if someone built this before
- Verified no duplication

**❌ No if**:
- Haven't searched yet
- Assuming it doesn't exist
- Skipped library research

**If NO**: Search codebase, research libraries first

---

### Question 5: Researched Alternatives?
**Principle #5**: Open Source First

**Ask**: "Have I researched open source alternatives?"

**✅ Yes if**:
- Searched for libraries solving this problem
- Compared alternatives (features, license, maintenance)
- Presented options to human for decision
- Human chose to build custom or use library

**❌ No if**:
- Building custom without research
- Assuming no library exists
- Didn't present alternatives

**If NO**: Research libraries, present options with pros/cons

---

### Question 6: Avoiding Tech Debt?
**Principle #6**: No Legacy Baggage

**Ask**: "Am I avoiding technical debt?"

**✅ Yes if**:
- No commented-out code
- No unused imports
- No dead code (functions with zero callers)
- Complexity <= 10 (cyclomatic complexity)
- No TODOs or FIXMEs without tickets
- No duplication

**❌ No if**:
- Leaving commented code "just in case"
- Unused imports exist
- Dead code present
- Over-complex functions (complexity > 10)
- TODOs without tracking

**If NO**: Clean up first (invoke `detect-unused-code`, `detect-complexity`)

---

### Question 7: Is This Excellent?
**Principle #7**: Perfectionist Excellence

**Ask**: "Is this excellent code?"

**✅ Yes if**:
- Clear naming (variables, functions, classes)
- Comprehensive documentation (docstrings)
- Type hints (Python) or type annotations (TypeScript, Java)
- Follows language style guide (PEP 8, etc.)
- Would I be proud to show this in code review?

**❌ No if**:
- Vague naming (x, data, temp, foo)
- Missing or poor documentation
- No type hints
- Style violations
- "Good enough" mentality

**If NO**: Improve naming, docs, types, style first

---

## Checklist Workflow

### Step 1: Present Questions

**Before coding starts**:

```
[SEVEN QUESTIONS CHECKLIST]

Before you code, answer these 7 questions:

1. ✅ Tests first?
   Have I written tests first (or using BDD scenarios)?

2. ✅ Fail loud?
   Will this fail loudly with clear errors?

3. ✅ Module focused?
   Is this module focused on one responsibility?

4. ❓ Checked if exists?
   Did I check if this already exists?

5. ❓ Researched alternatives?
   Have I researched open source libraries?

6. ✅ Avoiding tech debt?
   Am I avoiding technical debt?

7. ✅ Is this excellent?
   Is this excellent code?

Current: 5/7 "Yes" (Questions 4, 5 need checking)
```

---

### Step 2: Wait for Answers

**User must answer each question**:

```
You: "I'm about to implement user authentication"

Claude: Before we code, let's run the Seven Questions Checklist:

1. Tests first? → Will use TDD ✅
2. Fail loud? → Will add assertions ✅
3. Module focused? → Separate auth module ✅
4. Checked if exists? → Let me search...

   Searching codebase for "authentication"...
   Found: src/auth/ directory exists ✅
   Found: login() function already implemented ⚠️

   → Authentication already exists! Reuse it or improve it?

User: "Improve the existing one"

Claude: Good! Continuing checklist...

5. Researched alternatives?
   → Should we use Passport.js, Auth0, or custom?

User: "Use existing custom implementation"

Claude: ✅

6. Avoiding tech debt? → Will enforce Principle #6 ✅
7. Is this excellent? → Will follow best practices ✅

Result: 7/7 "Yes" ✅
Proceeding with implementation...
```

---

### Step 3: Block if Any "No"

**If ANY question is "No"**:

```
[SEVEN QUESTIONS - BLOCKED]

Question 4: "Did I check if this exists?" → ❌ NO

You must search codebase first (Principle #4: Reuse Before Build)

Action Required:
  1. Search: grep -rn "authentication" src/
  2. Search libraries: npm search authentication
  3. Verify: Nothing suitable exists
  4. Then proceed with custom implementation

Blocked: Cannot proceed until Question 4 = "Yes"
```

**User must resolve before continuing**.

---

### Step 4: Allow if All "Yes"

**If ALL questions are "Yes"**:

```
[SEVEN QUESTIONS - APPROVED]

✅ 1. Tests first
✅ 2. Fail loud
✅ 3. Module focused
✅ 4. Checked if exists
✅ 5. Researched alternatives
✅ 6. Avoiding tech debt
✅ 7. Is this excellent

Result: 7/7 "Yes" ✅

Quality Gate: PASS ✅
Proceeding with implementation...

Principles will be enforced during:
  - RED phase (tests first)
  - GREEN phase (fail loud, modular)
  - REFACTOR phase (no tech debt, excellence)
```

---

## Output Format

```
[SEVEN QUESTIONS CHECKLIST]

Checking Key Principles compliance...

1. Test Driven Development
   Q: Have I written tests first?
   A: ✅ Yes (using TDD workflow)

2. Fail Fast & Root Cause
   Q: Will this fail loudly if wrong?
   A: ✅ Yes (adding assertions and specific errors)

3. Modular & Maintainable
   Q: Is this module focused?
   A: ✅ Yes (separate auth module, single responsibility)

4. Reuse Before Build
   Q: Did I check if this exists?
   A: ✅ Yes (searched codebase, found existing auth, will improve it)

5. Open Source First
   Q: Have I researched alternatives?
   A: ✅ Yes (compared Passport.js, Auth0, decided on custom)

6. No Legacy Baggage
   Q: Am I avoiding tech debt?
   A: ✅ Yes (will invoke detect-unused-code after refactor)

7. Perfectionist Excellence
   Q: Is this excellent?
   A: ✅ Yes (following best practices, type hints, docs)

Checklist Result: 7/7 "Yes" ✅

Quality Gate: ✅ PASS
Principles: All 7 satisfied
Ready to code: Yes

Proceeding with TDD workflow...
```

---

## Integration with TDD/BDD

**TDD workflow invokes this checklist automatically**:

```
User: "Implement <REQ-ID>"

1. seven-questions-checklist (Sensor):
   → Ask 7 questions
   → If all "Yes" → Proceed
   → If any "No" → Block

2. (If approved) tdd-workflow:
   → RED phase
   → GREEN phase
   → REFACTOR phase (enforces #6, #7)
   → COMMIT phase
```

---

## Prerequisites Check

Before invoking:
1. About to start coding
2. Requirement (REQ-*) identified
3. Human available to answer questions

---

## Configuration

```yaml
plugins:
  - name: "@aisdlc/principles-key"
    config:
      seven_questions:
        require_all_yes: true              # Block if any "No"
        ask_before_coding: true            # Auto-invoke before TDD/BDD
        block_if_any_no: true              # Enforce blocking
        skip_for_trivial_changes: false    # Even trivial code needs checklist
```

---

## Notes

**Why Seven Questions?**
- **Enforces principles** operationally (not just philosophy)
- **Quality gate** prevents bad code from being written
- **Teaching tool** (developers learn principles through questions)
- **Prevents common mistakes** (skipping tests, not researching libraries)

**When to run**:
- Before every coding task (TDD, BDD, refactoring)
- Before committing
- During code review
- When onboarding new developers

**Homeostasis Goal**:
```yaml
desired_state:
  all_questions_answered_yes: true
  principles_followed: true
  quality_gate_passed: true
```

**Ultimate Mantra**: **"Excellence or nothing"** 🔥
