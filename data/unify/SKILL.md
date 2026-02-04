---
name: unify
description: Validate spec-implementation-test alignment and convergence for spec groups. Checks spec completeness, atomic spec coverage, implementation evidence, test evidence, and traceability. Use after implementation and tests are complete.
allowed-tools: Read, Glob, Grep, Bash, Task
user-invocable: true
---

# Unify Skill

## Purpose

Validate that implementation and tests conform to the spec group's atomic specs. Ensure convergence before approval and merge.

**Key Input**: Spec group at `.claude/specs/groups/<spec-group-id>/`

## Usage

```
/unify <spec-group-id>          # Validate full spec group convergence
/unify <spec-group-id> --quick  # Quick check (skip deep validation)
```

## Convergence Criteria

A spec group is **converged** when:
1. **Requirements complete** - All REQ-XXX requirements present with EARS format
2. **Spec complete** - spec.md has all required sections
3. **Atomic specs complete** - All atomic specs have implementation and test evidence
4. **Traceability intact** - REQ → atomic spec → implementation → test chain is complete
5. **Tests pass** - All tests passing, coverage adequate
6. **Contracts valid** - (For MasterSpec) Contracts consistent across workstreams

If any criterion fails → Task is **not converged** → Iteration needed.

## Validation Process

### Step 1: Load Spec Group

```bash
# Load manifest
cat .claude/specs/groups/<spec-group-id>/manifest.json

# Load requirements
cat .claude/specs/groups/<spec-group-id>/requirements.md

# Load spec
cat .claude/specs/groups/<spec-group-id>/spec.md

# List atomic specs
ls .claude/specs/groups/<spec-group-id>/atomic/
```

Verify in manifest.json:
- `review_state` is `APPROVED`
- `atomic_specs.enforcement_status` is `passing`
- `work_state` is `VERIFYING`

### Step 2: Requirements Completeness Check

Verify requirements.md:
- [ ] Problem statement present
- [ ] Goals and non-goals defined
- [ ] REQ-XXX requirements in EARS format
- [ ] Each requirement has rationale and priority
- [ ] Constraints and assumptions documented
- [ ] Edge cases identified
- [ ] Open questions resolved or deferred

**Output**: Requirements completeness report

```markdown
## Requirements Completeness: ✅ Pass

- Problem statement: Present
- Goals: 3 defined
- Requirements: 4 in EARS format (REQ-001 through REQ-004)
- All high priority questions resolved
- No blocking open questions
```

### Step 3: Spec Completeness Check

Verify spec.md:
- [ ] Context (references requirements.md)
- [ ] Goals/Non-goals (consistent with requirements.md)
- [ ] Requirements Summary (references, doesn't duplicate)
- [ ] Acceptance Criteria (mapped to requirements)
- [ ] Core Flows documented
- [ ] At least one sequence diagram
- [ ] Edge cases from requirements addressed
- [ ] Interfaces & Data Model (if applicable)
- [ ] Security considerations
- [ ] Task list with dependencies
- [ ] Test plan mapping ACs to test cases
- [ ] Open questions resolved

**Output**: Spec completeness report

```markdown
## Spec Completeness: ✅ Pass

- All required sections present
- 8 acceptance criteria (mapped to REQ-001 through REQ-004)
- 1 sequence diagram for logout flow
- Security considerations addressed
- All open questions resolved
```

### Step 4: Atomic Spec Validation

For each atomic spec in `atomic/`:

```bash
# Read atomic spec
cat .claude/specs/groups/<spec-group-id>/atomic/as-001-logout-button-ui.md
```

Verify each atomic spec:
- [ ] `status` is `implemented`
- [ ] Requirements refs present (REQ-XXX)
- [ ] Acceptance criteria defined
- [ ] Implementation Evidence section filled
- [ ] Test Evidence section filled
- [ ] Decision Log has completion entry

**Output**: Atomic spec coverage report

```markdown
## Atomic Spec Coverage: ✅ Pass

| Atomic Spec | Status | Impl Evidence | Test Evidence |
|-------------|--------|---------------|---------------|
| as-001 | implemented | ✅ 2 files | ✅ 2 tests |
| as-002 | implemented | ✅ 1 file | ✅ 2 tests |
| as-003 | implemented | ✅ 1 file | ✅ 2 tests |
| as-004 | implemented | ✅ 2 files | ✅ 2 tests |

**All 4 atomic specs have complete evidence**
```

### Step 5: Traceability Validation

Verify complete chain: REQ → Atomic Spec → Implementation → Test

```markdown
## Traceability Matrix

| Requirement | Atomic Specs | Implementation | Tests |
|-------------|--------------|----------------|-------|
| REQ-001 | as-001 | UserMenu.tsx:15 | user-menu.test.ts:12 |
| REQ-002 | as-002 | auth-service.ts:67 | auth-service.test.ts:24 |
| REQ-003 | as-003 | auth-router.ts:23 | auth-router.test.ts:18 |
| REQ-004 | as-004 | auth-service.ts:72 | auth-service.test.ts:35 |

**Coverage**: 100% of requirements traced to atomic specs, implementation, and tests
```

### Step 6: Implementation Alignment Check

Verify implementation matches atomic spec requirements.

```bash
# For each atomic spec, verify implementation evidence
# Read the files listed in Implementation Evidence
cat src/services/auth-service.ts
```

For each atomic spec AC:
- [ ] Implementation exists at stated location
- [ ] Behavior matches AC description
- [ ] Error handling matches edge cases
- [ ] No undocumented functionality

**Output**: Implementation alignment report

```markdown
## Implementation Alignment: ✅ Pass

**as-001**: Logout Button UI
- AC1 ✅ Button rendered in UserMenu (UserMenu.tsx:15)
- AC2 ✅ Button triggers logout (UserMenu.tsx:18)

**as-002**: Token Clearing
- AC1 ✅ Token cleared from localStorage (auth-service.ts:67)
- AC2 ✅ Server session invalidated (auth-service.ts:70)

**as-003**: Post-Logout Redirect
- AC1 ✅ Redirect to /login (auth-router.ts:23)
- AC2 ✅ Confirmation message shown (auth-router.ts:28)

**as-004**: Error Handling
- AC1 ✅ Error message displayed (auth-service.ts:72)
- AC2 ✅ User stays logged in on error (auth-service.ts:75)

**No undocumented features detected**
```

### Step 7: Test Coverage Check

Verify tests cover all atomic spec ACs and pass.

```bash
# Run tests
npm test

# Check coverage
npm test -- --coverage
```

For each atomic spec:
- [ ] Every AC has at least one test
- [ ] Test references atomic spec ID and AC
- [ ] Test passes
- [ ] Test validates behavior (not implementation)

**Output**: Test coverage report

```markdown
## Test Coverage: ✅ Pass

**Per Atomic Spec**:
| Atomic Spec | AC | Test | Status |
|-------------|-----|------|--------|
| as-001 | AC1 | user-menu.test.ts:12 | ✅ Pass |
| as-001 | AC2 | user-menu.test.ts:20 | ✅ Pass |
| as-002 | AC1 | auth-service.test.ts:24 | ✅ Pass |
| as-002 | AC2 | auth-service.test.ts:35 | ✅ Pass |
| as-003 | AC1 | auth-router.test.ts:18 | ✅ Pass |
| as-003 | AC2 | auth-router.test.ts:28 | ✅ Pass |
| as-004 | AC1 | auth-service.test.ts:45 | ✅ Pass |
| as-004 | AC2 | auth-service.test.ts:55 | ✅ Pass |

**Summary**: 8 tests total, 100% AC coverage, 94% line coverage
```

### Step 8: Contract Validation (MasterSpec Only)

For multi-workstream efforts, validate contracts.

```bash
# Check contract registry in manifest
grep -A 10 "contracts" .claude/specs/groups/<spec-group-id>/manifest.json
```

Verify:
- All contracts registered
- No duplicate contract IDs
- Implementations match contract interfaces
- No dependency cycles

### Step 9: Generate Convergence Report

Aggregate all checks:

```markdown
# Convergence Report: <spec-group-id>

**Date**: 2026-01-14 16:30
**Spec Group**: .claude/specs/groups/<spec-group-id>/

## Summary: ✅ CONVERGED

All validation checks passed. Ready for code review.

---

## Validation Results

### Requirements: ✅ Pass
- 4 requirements in EARS format
- All high priority questions resolved

### Spec: ✅ Pass
- All sections present
- 8 acceptance criteria
- 1 sequence diagram

### Atomic Specs: ✅ Pass
- 4 atomic specs, all implemented
- Implementation evidence complete
- Test evidence complete

### Traceability: ✅ Pass
- 100% coverage: REQ → atomic spec → impl → test

### Implementation: ✅ Pass
- All ACs implemented per atomic specs
- No undocumented features

### Tests: ✅ Pass
- 8 tests, all passing
- 100% AC coverage
- 94% line coverage

---

## Evidence

**Files Modified**:
- src/services/auth-service.ts
- src/components/UserMenu.tsx
- src/router/auth-router.ts

**Test Files**:
- src/services/__tests__/auth-service.test.ts (4 tests)
- src/components/__tests__/user-menu.test.ts (2 tests)
- src/router/__tests__/auth-router.test.ts (2 tests)

**Test Output**:
```
PASS  src/services/__tests__/auth-service.test.ts
PASS  src/components/__tests__/user-menu.test.ts
PASS  src/router/__tests__/auth-router.test.ts

Tests: 8 passed, 8 total
Coverage: 94% statements
```

---

## Next Steps

1. Run `/code-review <spec-group-id>` for code quality review
2. Run `/security <spec-group-id>` for security review
3. Browser tests (if UI changes)
4. Ready for commit
```

### Step 10: Update Manifest

Update manifest.json with convergence status:

```json
{
  "work_state": "READY_TO_MERGE",
  "convergence": {
    "spec_complete": true,
    "all_acs_implemented": true,
    "all_tests_written": true,
    "all_tests_passing": true,
    "test_coverage": "94%",
    "traceability_complete": true,
    "code_review_passed": false,
    "security_review_passed": false
  },
  "decision_log": [
    {
      "timestamp": "<ISO timestamp>",
      "actor": "agent",
      "action": "convergence_validated",
      "details": "All 4 atomic specs converged, 8 tests passing"
    }
  ]
}
```

### Step 11: Handle Non-Convergence

If validation fails, identify specific gaps:

```markdown
# Convergence Report: <spec-group-id>

## Summary: ❌ NOT CONVERGED

Issues found. Implementation iteration required.

---

## Issues

### Issue 1: Missing Implementation Evidence (Priority: High)
- **Atomic Spec**: as-003
- **Problem**: Implementation Evidence section empty
- **Action**: Fill evidence in as-003-post-logout-redirect.md

### Issue 2: Test Failing (Priority: High)
- **Atomic Spec**: as-002
- **Test**: auth-service.test.ts:35
- **Error**: Expected null, got "test-token"
- **Action**: Fix token clearing logic or fix test

### Issue 3: Broken Traceability (Priority: Medium)
- **Requirement**: REQ-003
- **Problem**: No atomic spec references REQ-003
- **Action**: Update as-003 to reference REQ-003

---

## Recommendations

**Iteration 1**:
1. Fill Implementation Evidence in as-003
2. Fix failing test for as-002
3. Update REQ-003 reference in as-003

After fixes, re-run `/unify <spec-group-id>` to validate.
```

## Convergence Gates

### Spec Group Gates
- [ ] Requirements complete (EARS format)
- [ ] Spec complete with all sections
- [ ] Atomic specs all `status: implemented`
- [ ] Implementation Evidence filled in all atomic specs
- [ ] Test Evidence filled in all atomic specs
- [ ] Traceability 100% (REQ → atomic spec → impl → test)
- [ ] All tests passing
- [ ] Coverage ≥ 80%
- [ ] No undocumented features

### MasterSpec Gates
All spec group gates plus:
- [ ] All workstream spec groups converged
- [ ] Contract registry validated
- [ ] No cross-workstream conflicts
- [ ] Dependency graph acyclic
- [ ] Integration tests passing

## Integration with Other Skills

After convergence, the review chain is:
1. `/code-review <spec-group-id>` - Code quality review (always)
2. `/security <spec-group-id>` - Security review (always)
3. `/browser-test <spec-group-id>` - UI validation (if UI changes)
4. `/docs <spec-group-id>` - Documentation generation (if public API)
5. Commit

**Next step after unify passes**: Dispatch `/code-review`

If not converged:
- Use `/implement` to fill missing evidence
- Use `/test` to fix failing tests
- Re-run `/unify` after fixes

## Examples

### Example 1: Converged Spec Group

**Input**: Spec group sg-logout-button (all atomic specs complete)

**Unifier Process**:
1. Requirements: ✅ 4 REQ-XXX in EARS format
2. Spec: ✅ All sections present
3. Atomic specs: ✅ 4/4 implemented with evidence
4. Traceability: ✅ 100% coverage
5. Implementation: ✅ All ACs implemented
6. Tests: ✅ 8 tests passing, 94% coverage

**Output**: CONVERGED ✅ - Ready for code review

### Example 2: Non-Converged Spec Group

**Input**: Spec group sg-dark-mode (missing test evidence)

**Unifier Process**:
1. Requirements: ✅ Pass
2. Spec: ✅ Pass
3. Atomic specs: ❌ as-002 missing Test Evidence
4. Tests: ❌ 1 test failing

**Output**:
```markdown
❌ NOT CONVERGED

**Issues**:
- as-002: Missing Test Evidence section
- as-002: Test auth-service.test.ts:35 failing

**Action**: Fill Test Evidence, fix failing test
**Iteration 1**: Run /test to fix
```

After test fixed → Re-run unifier → CONVERGED ✅

### Example 3: Traceability Gap

**Input**: Spec group with broken traceability

**Unifier Process**:
1. Requirements: ✅ 4 requirements
2. Atomic specs: 3 atomic specs
3. Traceability: ❌ REQ-004 has no atomic spec

**Output**:
```markdown
❌ NOT CONVERGED

**Issue**: REQ-004 "Error Handling" has no atomic spec

**Action**: Either:
- Add as-004-error-handling.md for REQ-004
- Update existing atomic spec to reference REQ-004

**Iteration 1**: Run /atomize to create missing atomic spec
```
