---
name: refine-requirements
description: Refine requirements from discoveries during TDD/BDD implementation. Captures edge cases, race conditions, and business rules discovered by developers. Enables requirements refinement loop. Use when developers discover missing requirements during coding.
allowed-tools: [Read, Write, Edit, Grep]
---

# refine-requirements

**Skill Type**: Actuator (Requirements Refinement Loop)
**Purpose**: Update requirements from TDD/BDD discoveries
**Prerequisites**: Requirement exists, discovery made during implementation

---

## Agent Instructions

You are implementing the **requirements refinement loop** - a key innovation in AI SDLC v3.0.

**The Loop**:
```
Requirements (REQ-*, BR-*, C-*, F-*)
  ↓ (used for)
TDD/BDD Implementation
  ↓ (discovers)
Missing Requirements (edge cases, race conditions)
  ↓ (feeds back to)
Updated Requirements (new BR-*, C-*, F-*)
  ↓ (used for)
Next Implementation
```

**Your role**: Capture discoveries and update requirements.

---

## Discovery Types

### Type 1: Edge Cases

**Discovered During**: GREEN phase (implementation)

**Example**:
```
Original: REQ-F-USER-001: User registration

TDD Implementation:
  Developer: "What if two users register with the same email simultaneously?"

Discovery: Race condition not covered in original requirement

New BR-*:
  BR-015: Concurrent registration prevention
    - Use database unique constraint on email
    - Catch IntegrityError on duplicate
    - Return "Email already registered"
    - Discovered: 2025-11-20 during TDD GREEN phase
    - Discovered by: Developer question
```

---

### Type 2: Missing Business Rules

**Discovered During**: RED phase (test writing)

**Example**:
```
Original: <REQ-ID>: Payment processing

TDD Implementation (RED phase):
  Developer writing test: "Should I test duplicate payments?"
  Developer: "What if user clicks 'Pay' button twice?"

Discovery: Idempotency not covered in original requirement

New BR-*:
  BR-020: Duplicate payment prevention
    - Generate idempotency key per payment
    - Same key = same charge (no duplicate)
    - Key format: SHA256(user_id + timestamp + amount)
    - Discovered: 2025-11-20 during TDD RED phase
    - Discovered by: Developer test case question

New F-*:
  F-005: Idempotency key generation
    - Formula: SHA256(user_id + timestamp + amount)
    - Inputs: user_id (str), timestamp (int), amount (float)
    - Output: hex string (64 chars)
    - Discovered: 2025-11-20 during TDD RED phase
```

---

### Type 3: Missing Constraints

**Discovered During**: REFACTOR phase

**Example**:
```
Original: REQ-F-EXPORT-001: User data export

TDD Implementation (REFACTOR phase):
  Developer: "Export takes 5 minutes for large accounts"

Discovery: Timeout constraint needed

New C-*:
  C-015: Export generation timeout
    - Max time: 5 minutes
    - Behavior: Generate in background, email link when ready
    - Discovered: 2025-11-20 during TDD REFACTOR phase
    - Discovered by: Performance observation
```

---

## Workflow

### Step 1: Capture Discovery

**Record**:
- What was discovered?
- During which phase? (RED, GREEN, REFACTOR)
- Who discovered it? (developer, tester, stakeholder)
- Why is it important?

**Template**:
```yaml
Discovery:
  date: 2025-11-20
  phase: TDD GREEN phase
  discovered_by: Developer
  question: "What if two users register with same email simultaneously?"
  impact: Race condition could create duplicate accounts
  severity: High (data integrity issue)
```

---

### Step 2: Determine Addition Type

**Options**:
1. **New BR-*** - Business rule not previously identified
2. **New C-*** - Constraint from ecosystem not acknowledged
3. **New F-*** - Formula/calculation not specified
4. **Updated BR-/C-/F-*** - Existing specification needs refinement

---

### Step 3: Update Requirement Document

**Add new BR-/C-/F-* with discovery metadata**:

```markdown
## REQ-F-USER-001: User Registration

[Existing content...]

### Business Rules

**BR-001: Email validation**
[Existing spec...]

**BR-002: Password requirements**
[Existing spec...]

**BR-015: Concurrent registration prevention** ⭐ NEW
- **Use database unique constraint on email column**
- **Catch unique constraint violation (IntegrityError)**
- **Return error: "Email already registered"**
- **Discovered**: 2025-11-20 during TDD GREEN phase
- **Discovery Source**: Developer question about race condition
- **Impact**: Prevents duplicate accounts in concurrent scenarios
- **Tests Added**: test_concurrent_registration_prevented()
- **Code Updated**: src/auth/registration.py (added try/except)
```

**Metadata to include**:
- ✅ Discovery date
- ✅ Discovery phase (RED/GREEN/REFACTOR/BDD)
- ✅ Discovery source (developer, tester, user feedback)
- ✅ Impact/rationale
- ✅ Tests added
- ✅ Code updated

---

### Step 4: Update Traceability

**Record refinement in traceability**:

```yaml
# docs/traceability/requirement-refinements.yml

REQ-F-USER-001:
  refinements:
    - date: 2025-11-20
      added: BR-015
      reason: "Race condition discovered during TDD"
      phase: GREEN
      discovered_by: "Developer"
      commit: "abc123"
```

---

### Step 5: Update Code and Tests

**If code already written**, update it:

```python
# Before (original implementation)
def register(email: str, password: str) -> RegisterResult:
    if User.exists(email):
        return RegisterResult(success=False, error="Email already registered")
    user = User.create(email=email, password=hash_password(password))
    return RegisterResult(success=True, user=user)

# After (refined with BR-015)
def register(email: str, password: str) -> RegisterResult:
    try:
        # BR-015: Database unique constraint handles race condition
        user = User.create(email=email, password=hash_password(password))
        return RegisterResult(success=True, user=user)
    except IntegrityError as e:
        # BR-015: Concurrent registration caught by database
        if "unique constraint" in str(e).lower():
            return RegisterResult(success=False, error="Email already registered")
        raise
```

**Add test**:
```python
# Validates: BR-015
def test_concurrent_registration_prevented():
    """Test race condition handled by database constraint"""
    # Simulate concurrent registrations
    with ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(register, "user@example.com", "Pass123!")
        future2 = executor.submit(register, "user@example.com", "Pass123!")
        results = [future1.result(), future2.result()]

    # One should succeed, one should fail
    successes = [r for r in results if r.success]
    failures = [r for r in results if not r.success]
    assert len(successes) == 1
    assert len(failures) == 1
    assert failures[0].error == "Email already registered"
```

---

### Step 6: Commit Refinement

```bash
git add docs/requirements/ src/ tests/
git commit -m "REFINE: Add BR-015 to REQ-F-USER-001 (race condition)

Refine user registration requirement with concurrent handling.

Discovery:
- Phase: TDD GREEN phase
- Question: What if two users register simultaneously?
- Impact: Race condition could create duplicate accounts

Added:
- BR-015: Concurrent registration prevention
  - Use database unique constraint
  - Catch IntegrityError
  - Return clear error message

Updated Code:
- src/auth/registration.py: Added try/except for IntegrityError

Added Tests:
- test_concurrent_registration_prevented() with thread pool

Refines: REQ-F-USER-001
Discovered: 2025-11-20 during TDD GREEN phase
"
```

---

## Output Format

```
[REFINE REQUIREMENTS - REQ-F-USER-001]

Original Requirement:
  REQ-F-USER-001: User registration with email

Discovery During TDD GREEN Phase:
  Question: "What if two users register with same email simultaneously?"
  Impact: Race condition → duplicate accounts
  Severity: High (data integrity)

Refinement Added:

  BR-015: Concurrent registration prevention ⭐ NEW
    - Use database unique constraint on email
    - Catch IntegrityError on duplicate
    - Return "Email already registered"
    - Discovered: 2025-11-20 during TDD GREEN phase
    - Source: Developer question

Code Updated:
  ✓ src/auth/registration.py (added try/except for IntegrityError)

Tests Added:
  ✓ test_concurrent_registration_prevented() (thread pool simulation)

Traceability Updated:
  ✓ docs/traceability/requirement-refinements.yml

Requirements Doc Updated:
  ✓ docs/requirements/user-management.md
    Added: BR-015 with discovery metadata

Commit: REFINE: Add BR-015 to REQ-F-USER-001

✅ Requirement Refined!
   REQ-F-USER-001 now covers race condition
   Next developer won't have same question
```

---

## Prerequisites Check

Before invoking:
1. REQ-* requirement exists
2. Discovery made (developer question, test case, implementation issue)

---

## Notes

**Why requirements refinement?**
- **Living requirements**: Requirements evolve based on implementation reality
- **Knowledge capture**: Developer discoveries become permanent documentation
- **Prevent re-discovery**: Next developer sees the edge case already covered
- **Better specifications**: Requirements improve over time

**Refinement vs Original Extraction**:
```
Original: Broad understanding, may miss edge cases
Refined: Precise understanding from implementation experience
```

**Homeostasis Goal**:
```yaml
desired_state:
  all_discoveries_captured: true
  requirements_continuously_refined: true
  edge_cases_documented: true
```

**"Excellence or nothing"** 🔥
