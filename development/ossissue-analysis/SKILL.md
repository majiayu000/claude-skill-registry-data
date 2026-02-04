---
name: oss:issue-analysis
description: Phase 2 of OSS contribution - Deep analysis combining issue requirements with codebase exploration. Extracts requirements, explores code structure, identifies exact code locations to fix, traces execution paths, and maps code-level changes needed. Use when starting work on selected issue.
---

# Phase 2: Issue Analysis & Code Exploration

Deep analysis of issue requirements combined with codebase exploration to identify exact code changes needed.

## Purpose

Transform an issue into actionable code-level understanding by:
- **Understanding requirements:** What needs to be done and why
- **Exploring codebase:** Project structure, conventions, patterns
- **Locating code:** Find exact files/functions to modify
- **Identifying problems:** Pinpoint broken/missing code
- **Planning changes:** Map requirements to specific code modifications

## When to Use

**Triggers:**
- "이 이슈 분석해줘"
- "코드에서 어디를 고쳐야 하나?"
- "이슈와 코드 연결"
- "문제 있는 코드 찾기"

**Use when:**
- Starting work on a selected issue
- Need to understand both requirements AND code
- Want to identify exact modification points
- Ready to plan implementation

## Integrated Analysis Framework

### Step 0: Review CONTRIBUTING.md Requirements

**MANDATORY: Before analyzing the issue, review project contribution guidelines**
- Refer to CONTRIBUTING.md read in Phase 1
- Ensure your analysis aligns with project conventions
- Note any specific requirements for:
  - Code style and formatting
  - Testing requirements
  - Documentation standards
  - Commit message format
  - Branch naming conventions

**All analysis and subsequent work MUST comply with these guidelines**

### Step 1: Issue Type & Requirements Extraction

Identify issue type and extract core requirements.

**Issue Types:**

**Bug Fix:**
```markdown
### Bug Analysis Template

**Current Behavior:**
[What actually happens - be specific]

**Expected Behavior:**
[What should happen - reference docs/specs]

**Reproduction Steps:**
1. [Step 1]
2. [Step 2]
3. [Observe: ...]

**Environment:**
- Version: [version]
- Platform: [OS/browser/etc]

**Impact:**
- Severity: [Critical/High/Medium/Low]
- Affected users: [who/how many]
```

**Feature Request:**
```markdown
### Feature Analysis Template

**User Story:**
As a [user type], I want [capability] so that [benefit].

**Functional Requirements:**
1. [Requirement 1 - must have]
2. [Requirement 2 - must have]
3. [Requirement 3 - nice to have]

**Acceptance Criteria:**
- [ ] [Criterion 1 - specific and testable]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
```

**Refactoring:**
```markdown
### Refactoring Analysis Template

**Current Problems:**
1. [Problem 1: e.g., duplicated code across X files]
2. [Problem 2: e.g., poor separation of concerns]

**Desired Outcome:**
[What the code should look like after refactoring]

**Constraints:**
- [ ] No behavior changes
- [ ] All existing tests must pass
- [ ] No API changes (if library)
```

### Step 2: Project Structure & Convention Understanding

Explore codebase to understand organization and conventions.

**A. Directory Structure Mapping:**

```bash
# Get project overview
tree -L 2 -d

# Identify key directories
ls -la
```

```markdown
### Project Structure

**Main source:** [path to primary code]

**Key directories:**
- `src/` or `lib/` - Main source code
- `tests/` or `__tests__/` - Test files
- `docs/` - Documentation
- `.github/` - CI/CD, workflows

**Organization principle:**
- [x] By feature (e.g., /users, /products)
- [ ] By layer (e.g., /models, /views, /controllers)
- [ ] By type (e.g., /components, /utils, /services)

**Technologies:**
- Language: [language + version]
- Framework: [framework]
- Build tool: [npm/cargo/maven/etc]
- Testing: [jest/pytest/etc]
```

**B. Code Conventions Discovery:**

```bash
# Check for style configs
cat .prettierrc .eslintrc package.json

# Find naming patterns
find src -type f -name "*.js" | head -10
```

```markdown
### Code Conventions

**File Naming:**
- Components: [e.g., PascalCase.tsx]
- Utilities: [e.g., camelCase.ts]
- Tests: [e.g., file.test.js or file_test.go]

**Code Style:**
- Indentation: [2 spaces / 4 spaces / tabs]
- Quotes: [single / double]
- Import order: [external, internal, relative]

**Naming Patterns:**
- Classes: [PascalCase]
- Functions: [camelCase / snake_case]
- Constants: [UPPER_SNAKE_CASE]
```

**C. Testing Patterns:**

```bash
# Find test locations
find . -name "*test*" -type f | head -5

# Check test framework
cat package.json | grep -A5 "scripts"
```

```markdown
### Testing Strategy

**Test Location:**
- Unit tests: [e.g., __tests__/, alongside source]
- Integration tests: [location]

**Test Framework:** [Jest / pytest / go test / etc]

**Test Naming Pattern:**
- [describe/test, test_, Test*]

**Run Commands:**
```bash
npm test              # All tests
npm test -- file.test.js  # Specific test
npm test -- --coverage    # With coverage
```
```

### Step 3: Code Location Discovery

Find exact files and functions related to the issue.

**A. Entry Point Discovery:**

```bash
# For UI bugs/features - find component
rg "ComponentName" --type tsx
rg "class.*ComponentName"

# For API/backend - find endpoint
rg "app\.(get|post|put).*endpoint"
rg "@app.route|router"

# For CLI - find command
rg "subcommand|command.*name"

# For library - find exported function
rg "export (function|class|const).*functionName"
```

```markdown
### Entry Points

**Primary entry point:**
- File: `src/components/UserProfile.tsx:45`
- Function/Component: `UserProfile`
- Purpose: [what this code does]

**How to trigger:**
[Steps to reach this code - e.g., click button, call API]
```

**B. Find Similar/Related Code:**

```bash
# Find similar features for reference
rg "similar-feature" --type js

# Find similar patterns
find . -name "*Similar*.js"

# Find related tests
rg "describe.*YourFeature" tests/
```

```markdown
### Reference Examples

**Similar code to reference:**
1. `src/components/UserSettings.tsx:120`
   - Similar pattern for form handling
   - Shows validation approach

2. `src/utils/validation.ts:45`
   - Input validation logic
   - Error handling pattern
```

### Step 4: Code-Level Problem Identification

**THIS IS THE CRITICAL STEP - Find exact code that needs fixing**

**A. For Bug Fixes - Trace to Root Cause:**

```bash
# Search for error message or symptom
rg "error message text"

# Find function definitions
rg "function buggyFunction|def buggy_function"

# Find all callers
rg "buggyFunction\("
```

```markdown
### Bug Root Cause Analysis

**Symptom Location:**
- File: `src/auth/session.ts:78`
- Function: `validateSession`
- Problem: Crashes when `user` is null

**Code Analysis:**
```typescript
// CURRENT CODE (BROKEN)
function validateSession(sessionId: string) {
  const session = getSession(sessionId)
  return session.user.id  // ❌ CRASHES if user is null
}
```

**Root Cause:**
- Missing null check for `session.user`
- Happens during logout race condition

**Needs to be changed to:**
```typescript
// FIXED CODE
function validateSession(sessionId: string) {
  const session = getSession(sessionId)
  if (!session?.user) {  // ✅ Add null check
    return null
  }
  return session.user.id
}
```

**Additional locations to check:**
- [ ] `src/auth/logout.ts:34` - may have similar issue
- [ ] `src/auth/session.test.ts` - add test for null user
```

**B. For Features - Identify Where to Add Code:**

```bash
# Find where similar features are implemented
rg "similar feature" --type js

# Find integration points
rg "import.*Component|from.*module"
```

```markdown
### Feature Implementation Points

**Where to add code:**

**1. New function needed:**
- Location: `src/utils/export.ts` (new file)
- Function: `exportToCSV(data, options)`
- Based on: `src/utils/exportToJSON.ts` (similar pattern)

**2. UI Integration:**
- File: `src/components/DataTable.tsx:120`
- Add: Export button in toolbar
- Pattern: Follow existing "Download" button at line 115

**3. Hook into existing flow:**
- File: `src/components/DataTable.tsx:45`
- Add: Import new export function
- Call: On button click handler

**Code to add:**
```typescript
// In DataTable.tsx
import { exportToCSV } from '@/utils/export'

// Around line 120, add:
<Button onClick={() => exportToCSV(data, { headers: true })}>
  Export CSV
</Button>
```
```

**C. For Refactoring - Map Code Smells:**

```bash
# Find duplicated code
rg -A10 "duplicated pattern"

# Find long functions
# (Manual inspection)
```

```markdown
### Refactoring Map

**Code smells identified:**

**1. Duplicated validation logic:**
- `src/auth/login.ts:34-50` (17 lines)
- `src/auth/register.ts:28-44` (17 lines)
- `src/auth/resetPassword.ts:15-31` (17 lines)

**Solution:**
- Extract to: `src/auth/validators.ts`
- New function: `validateUserInput(input)`
- Replace 3 duplications with function call

**2. God function:**
- `src/api/userController.ts:100-350` (250 lines!)
- Does: validation + business logic + DB + response

**Solution:**
- Split into:
  - `validateUserData()` at line 100
  - `createUser()` at line 150
  - `sendWelcomeEmail()` at line 200
```

### Step 5: Execution Path Tracing

Trace code flow to understand full context.

```markdown
### Execution Flow

**For [bug/feature]: [description]**

```
1. Entry: src/components/Login.tsx:89 - handleSubmit()
   └─> Calls: validateCredentials(username, password)

2. Flow: src/auth/validation.ts:23 - validateCredentials()
   └─> Calls: checkPassword(password)
   └─> Returns: {valid: boolean, error?: string}

3. Bug: src/auth/validation.ts:45 - checkPassword()
   └─> ❌ PROBLEM: Doesn't handle null password
   └─> FIX: Add null check at line 46

4. Result: Returns to handleSubmit, shows error
```

**Key functions in flow:**
- `handleSubmit()` @ Login.tsx:89 - Form submission
- `validateCredentials()` @ validation.ts:23 - Main validator
- `checkPassword()` @ validation.ts:45 - ❌ NEEDS FIX HERE

**Data transformations:**
- Input: `{username: string, password: string}`
- Validation: checks format, length, special chars
- Output: `{valid: boolean, error?: string}`
```

### Step 6: Dependency & Impact Analysis

Understand what depends on your changes.

```bash
# Find all callers
rg "functionName\("

# Find all imports
rg "import.*ModuleName"

# Find test coverage
rg "describe.*functionName" tests/
```

```markdown
### Dependencies & Impact

**Upstream (what calls this code):**
- `src/components/Login.tsx:89` - Login form
- `src/components/Register.tsx:67` - Registration form
- `src/api/authController.ts:120` - API endpoint

**Impact of change:**
- 🟢 Low risk - adding validation only
- All callers already handle error case
- Existing tests cover error path

**Downstream (what this calls):**
- `src/utils/crypto.ts:hashPassword()` - crypto library
- `src/models/User.ts:findByUsername()` - DB query

**Side effects:**
- None - pure validation function
- No state mutations
- No external calls

**Test coverage:**
- Current: `tests/auth/validation.test.ts`
- Need to add: test case for null password
```

### Step 7: Modification Plan

Create concrete plan of what code to change.

```markdown
### Modification Plan

**Files to modify:**

**1. PRIMARY FIX: src/auth/validation.ts**
- **Line 45-50:** Function `checkPassword()`
- **Change type:** Add null/undefined check
- **Before:**
```typescript
function checkPassword(password: string): boolean {
  return password.length >= 8  // ❌ Crashes if null
}
```
- **After:**
```typescript
function checkPassword(password: string | null): boolean {
  if (!password) {  // ✅ Add null check
    return false
  }
  return password.length >= 8
}
```
- **Risk:** 🟢 Low - defensive programming

**2. ADD TEST: tests/auth/validation.test.ts**
- **Line:** After line 67 (add new test case)
- **Add:**
```typescript
it('should return false for null password', () => {
  expect(checkPassword(null)).toBe(false)
})
```

**3. UPDATE TYPES: src/types/auth.ts** (if needed)
- **Line 12:** Update PasswordInput type to allow null

**Files NOT to change:**
- ❌ `src/components/Login.tsx` - already handles errors correctly
- ❌ `src/api/authController.ts` - no changes needed
```

### Step 8: Edge Cases & Implicit Requirements

Identify edge cases from code analysis.

```markdown
### Edge Cases Discovered

**From code inspection:**
- [ ] Null password: `checkPassword(null)` - FOUND in code trace
- [ ] Empty string: `checkPassword("")` - check if handled
- [ ] Very long password: `checkPassword("x".repeat(10000))` - DOS risk?
- [ ] Unicode characters: `checkPassword("パスワード")` - supported?
- [ ] SQL injection: `checkPassword("' OR 1=1--")` - sanitized?

**Integration concerns:**
- Depends on: crypto library (trusted)
- Affects: Login, Register, Reset Password flows
- Breaking change: No - only adding validation

**Performance:**
- No loops or heavy computation
- O(1) complexity
- No performance concerns

**Security:**
- Input validation ✅
- No sensitive data logged
- Follow OWASP guidelines
```

### Step 9: Acceptance Criteria & Scope

Define concrete success criteria and scope.

```markdown
### Scope Definition

**In Scope:**
1. Add null check to `checkPassword()` function
2. Add unit test for null password case
3. Verify no crashes on null input

**Out of Scope:**
1. Password strength improvements (separate issue #456)
2. UI error message improvements (separate issue #457)
3. Refactoring validation.ts (not requested)

**Complexity:** 🟢 Simple (< 2 hours)
- Single function change
- One test case addition
- Low risk change

### Acceptance Criteria

**Functional:**
- [ ] `checkPassword(null)` returns `false` (no crash)
- [ ] `checkPassword(undefined)` returns `false` (no crash)
- [ ] `checkPassword("valid")` still works correctly
- [ ] Existing tests still pass

**Quality:**
- [ ] New test added and passing
- [ ] No linting errors
- [ ] Type definitions updated
- [ ] Code follows project conventions

**Verification:**
```bash
npm test                    # All tests pass
npm run lint               # No errors
npm run type-check         # No type errors
```

**Manual testing:**
1. Open login form
2. Submit with empty password
3. Verify: No crash, shows error message
```

## Analysis Patterns by Issue Type

### Bug Fix Pattern

1. **Understand symptom** - Read issue description
2. **Reproduce locally** - Follow reproduction steps
3. **Explore codebase** - Find project structure
4. **Locate bug** - Trace code to root cause
5. **Identify fix point** - Exact line to change
6. **Plan changes** - What code to modify
7. **Consider side effects** - Impact analysis

### Feature Pattern

1. **Understand need** - User story, use cases
2. **Explore codebase** - Structure and conventions
3. **Find similar features** - Reference implementations
4. **Identify integration points** - Where to add code
5. **Plan new code** - What to create
6. **Map dependencies** - What it will interact with
7. **Design interface** - API, props, parameters

### Refactoring Pattern

1. **Identify code smell** - What's wrong
2. **Explore codebase** - Understand context
3. **Map all instances** - Find all occurrences
4. **Plan extraction** - New structure
5. **Ensure test coverage** - Safety net
6. **Plan incremental steps** - Small safe changes
7. **Verify no behavior change** - Tests still pass

## Output Format

Provide comprehensive analysis with code-level details:

```markdown
# 🔍 Issue Analysis: [Issue Title]

**Issue:** #[number] | **Type:** [bug/feature/refactor]
**Status:** Ready to implement

---

## Summary
[2-3 sentences: what needs to be done, what code needs to change, why]

---

## Requirements

### Issue Requirements
[What user/maintainer wants]

### Code Requirements
[What code needs to change based on exploration]

---

## Project Understanding

### Structure
[Key directories and organization]

### Conventions
[Naming, style, patterns to follow]

### Testing
[Framework, location, how to run]

---

## Code Analysis

### Entry Points
- [File:line - function/component name]

### Problem Code Identified

**File: [path]**
**Line: [number]**
**Function: [name]**

**Current code (BROKEN):**
```language
[actual problematic code]
```

**Problem:**
- [what's wrong]
- [why it breaks]

**Fix needed:**
```language
[corrected code]
```

### Execution Flow
```
[trace from entry to problem]
```

---

## Modification Plan

### Files to Change

**1. [file path]**
- **Line:** [number]
- **Function:** [name]
- **Change:** [specific modification]
- **Before/After:** [code snippets]

**2. [test file]**
- **Add:** [new test cases]

### Impact Analysis
- **Upstream callers:** [list]
- **Risk:** 🟢/🟡/🔴
- **Breaking change:** Yes/No

---

## Testing Plan

**Existing tests to verify:**
- [test file:description]

**New tests to add:**
- [ ] Test case 1: [description]
- [ ] Test case 2: [description]

**Test commands:**
```bash
npm test
npm test -- specific.test.js
```

---

## Edge Cases
- [ ] [Edge case 1 - how to handle]
- [ ] [Edge case 2 - how to handle]

---

## Acceptance Criteria
- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] All tests pass
- [ ] Follows CONTRIBUTING.md guidelines

---

## Implementation Checklist
- [ ] Fix code at [file:line]
- [ ] Add test at [test-file]
- [ ] Run tests - all pass
- [ ] Run linter - no errors
- [ ] Manual verification

---

## Next Steps

✅ Analysis complete - Ready for **Phase 3: Solution Implementation**

**Start with:**
1. [Specific first task - e.g., "Fix checkPassword() at validation.ts:45"]
2. [Second task]
3. [Third task]
```

## Integration with Main Framework

When invoked from main framework:

1. **Receive context:** Issue URL, type from Phase 1
2. **Execute integrated analysis:**
   - Extract requirements
   - Explore codebase structure
   - Locate exact code to change
   - Identify problems in code
   - Plan modifications
3. **Return comprehensive analysis:** Ready to implement
4. **Update tracker:** Mark Phase 2 complete
5. **Transition:** Phase 3 (Implementation) with concrete code-level plan

## Common Pitfalls

**Avoid:**

❌ **Analyzing requirements without looking at code** - Will miss context
❌ **Exploring code without understanding requirements** - Will get lost
❌ **Assuming code structure** - Always verify by reading
❌ **Stopping at "what" without finding "where"** - Need exact locations
❌ **Ignoring existing patterns** - Must follow project conventions
❌ **Not tracing full execution path** - Will miss side effects
❌ **Forgetting to check tests** - Test changes are part of solution

## Verification Before Implementation

**Before moving to Phase 3, verify:**

- [ ] Requirements fully understood
- [ ] Codebase structure mapped
- [ ] Exact modification points identified
- [ ] Problem code located (for bugs)
- [ ] Integration points clear (for features)
- [ ] All duplications found (for refactoring)
- [ ] Execution path traced
- [ ] Dependencies identified
- [ ] Test strategy planned
- [ ] Edge cases listed
- [ ] Impact assessed and acceptable

If any unclear, dig deeper or ask maintainer.
