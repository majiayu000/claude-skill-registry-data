---
name: disambiguate-requirements
description: Break vague requirements into precise business rules (BR-*), constraints (C-*), and formulas (F-*) for code generation. Orchestrates extraction of BR-*, C-*, F-* from REQ-*. Use after requirement-extraction to enable autogeneration.
allowed-tools: [Read, Write, Edit]
---

# disambiguate-requirements

**Skill Type**: Orchestrator (Requirements Refinement)
**Purpose**: Transform vague requirements into precise BR-*, C-*, F-* specifications
**Prerequisites**: REQ-* requirement exists but lacks detailed BR-*, C-*, F-*

---

## Agent Instructions

You are **disambiguating requirements** to enable **code autogeneration**.

Your goal is to transform **vague requirements** into **precise specifications**:
- **BR-* (Business Rules)**: Specific rules, validations, logic
- **C-* (Constraints)**: Technical constraints from ecosystem E(t)
- **F-* (Formulas)**: Mathematical formulas and calculations

**This enables code autogeneration** - precise specs → auto-generated code.

---

## Workflow

### Step 1: Read Vague Requirement

**Example**:
```markdown
## <REQ-ID>: User Login

**Description**: Users can log in with email and password

**Acceptance Criteria**:
1. User enters credentials
2. System validates credentials
3. User gains access or sees error
```

**Problem**: Too vague for code generation!
- What email format?
- What password rules?
- What happens after N failures?
- What timeouts apply?

---

### Step 2: Extract Business Rules (BR-*)

**Invoke**: `extract-business-rules` skill

**Questions to ask**:
1. What validation rules apply? (format, length, range)
2. What business logic is needed? (calculations, decisions)
3. What edge cases exist? (null, empty, boundary values)
4. What error handling? (what goes wrong, what messages)

**Generated BR-* for <REQ-ID>**:
```yaml
Business Rules:
- BR-001: Email validation
  - Format: regex ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
  - Error: "Invalid email format"

- BR-002: Password requirements
  - Minimum length: 12 characters
  - Must contain: 1 uppercase, 1 lowercase, 1 number, 1 special char
  - Error: "Password must be at least 12 characters with mixed case, number, and special char"

- BR-003: Failed attempt handling
  - Max attempts: 3 per 15 minutes
  - Lockout duration: 15 minutes
  - Error: "Account locked. Try again in {remaining} minutes"

- BR-004: Email case sensitivity
  - Emails are case-insensitive
  - Store as lowercase
  - Compare as lowercase

- BR-005: Password case sensitivity
  - Passwords are case-sensitive
  - No transformation on storage or comparison
```

---

### Step 3: Extract Constraints (C-*)

**Invoke**: `extract-constraints` skill

**Questions to ask**:
1. What technical constraints exist? (timeouts, limits, dependencies)
2. What compliance requirements? (PCI-DSS, GDPR, HIPAA)
3. What ecosystem constraints? (APIs, libraries, platforms)
4. What performance constraints? (SLAs, latency)

**Generated C-* for <REQ-ID>**:
```yaml
Constraints:
- C-001: Database query timeout
  - Max query time: 100ms
  - Fallback: Return "Service temporarily unavailable"

- C-002: Session management
  - Session timeout: 30 minutes of inactivity
  - Token: JWT format
  - Storage: Redis cache

- C-003: Password hashing
  - Algorithm: bcrypt
  - Cost factor: 12
  - Library: bcrypt.js or bcrypt (Python)

- C-004: HTTPS required
  - All login requests must be HTTPS
  - Reject HTTP requests
  - Redirect HTTP → HTTPS

- C-005: Rate limiting
  - Max login attempts: 10 per minute per IP
  - Behavior: Return 429 (Too Many Requests)
```

---

### Step 4: Extract Formulas (F-*)

**Invoke**: `extract-formulas` skill

**Questions to ask**:
1. What calculations are needed? (fees, scores, times)
2. What mathematical formulas? (interest, conversions, algorithms)
3. What derived values? (totals, averages, percentages)

**Generated F-* for <REQ-ID>**:
```yaml
Formulas:
- F-001: Lockout expiry time
  - Formula: lockout_expiry = last_attempt_time + (15 * 60) seconds
  - Inputs: last_attempt_time (datetime)
  - Output: lockout_expiry (datetime)

- F-002: Remaining lockout time
  - Formula: remaining = max(0, (lockout_expiry - current_time) / 60) minutes
  - Inputs: lockout_expiry (datetime), current_time (datetime)
  - Output: remaining (int, minutes)

- F-003: Password strength score
  - Formula: score = length_score + complexity_score + uniqueness_score
  - Range: 0-100
  - Thresholds: <50 weak, 50-75 medium, >75 strong
```

---

### Step 5: Update Requirement Document

**Add BR-*, C-*, F-* to requirement**:

```markdown
## <REQ-ID>: User Login with Email and Password

[Previous content...]

---

### Business Rules (BR-*)

**BR-001: Email validation**
- Format: regex `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- Case insensitive (store and compare as lowercase)
- Error message: "Invalid email format"
- Autogenerate: Yes (code generation from regex)

**BR-002: Password requirements**
- Minimum length: 12 characters
- Must contain: 1 uppercase, 1 lowercase, 1 number, 1 special char
- Case sensitive
- Error message: "Password must be at least 12 characters with mixed case, number, and special char"
- Autogenerate: Yes (validation function)

**BR-003: Failed attempt handling**
- Max attempts: 3 per 15 minutes
- Lockout duration: 15 minutes
- Reset on successful login
- Error message: "Account locked. Try again in {remaining} minutes"
- Autogenerate: Yes (lockout tracker class)

**BR-004: Email case sensitivity**
- Normalization: Convert to lowercase before storage/comparison
- Autogenerate: Yes (email normalizer function)

**BR-005: Password case sensitivity**
- Storage: Hash as-is (no transformation)
- Comparison: Case-sensitive hash comparison
- Autogenerate: No (standard hashing library)

---

### Constraints (C-*)

**C-001: Database query timeout**
- Max time: 100ms
- Fallback: "Service temporarily unavailable"
- Monitoring: Alert if >80ms (warning threshold)

**C-002: Session management**
- Session timeout: 30 minutes inactivity
- Token format: JWT (HS256)
- Storage: Redis cache with TTL

**C-003: Password hashing**
- Algorithm: bcrypt
- Cost factor: 12 (secure but performant)
- Library: bcrypt (acknowledge E(t) - existing library)

**C-004: HTTPS required**
- Protocol: All requests must be HTTPS
- Reject: HTTP requests not allowed
- Redirect: Optional HTTP → HTTPS redirect

**C-005: Rate limiting**
- Max requests: 10 login attempts per minute per IP
- Response: HTTP 429 (Too Many Requests)
- Reset: 1 minute window

---

### Formulas (F-*)

**F-001: Lockout expiry time**
```
lockout_expiry = last_attempt_time + (15 * 60) seconds
```
- Inputs: last_attempt_time (datetime)
- Output: lockout_expiry (datetime)
- Autogenerate: Yes (datetime calculation)

**F-002: Remaining lockout time**
```
remaining = max(0, (lockout_expiry - current_time) / 60) minutes
```
- Inputs: lockout_expiry (datetime), current_time (datetime)
- Output: remaining (int, rounded to nearest minute)
- Autogenerate: Yes (timedelta calculation)

**F-003: Password strength score**
```
score = length_score + complexity_score + uniqueness_score
  where:
    length_score = min(50, length * 2)
    complexity_score = (has_upper * 10) + (has_lower * 10) + (has_number * 10) + (has_special * 20)
    uniqueness_score = 0 (check against common passwords)
```
- Range: 0-100
- Thresholds: <50 weak, 50-75 medium, >75 strong
- Autogenerate: Yes (password scorer function)

---

### Discovery Log

**Added during disambiguation**:
- BR-004: Email case sensitivity (discovered while discussing validation)
- BR-005: Password case sensitivity (discovered while discussing hashing)
- C-005: Rate limiting (discovered as security concern)
- F-003: Password strength scoring (discovered as UX enhancement)

**Source**: Product team discussion during disambiguation
**Date**: 2025-11-20
```

---

## Output Format

When disambiguation complete:

```
[DISAMBIGUATION - <REQ-ID>]

Original Requirement:
  "Users can log in with email and password"

Disambiguated Into:

Business Rules (5):
  ✓ BR-001: Email validation (regex, case handling)
  ✓ BR-002: Password requirements (length, complexity)
  ✓ BR-003: Failed attempt handling (lockout logic)
  ✓ BR-004: Email case sensitivity (normalization)
  ✓ BR-005: Password case sensitivity (hashing)

Constraints (5):
  ✓ C-001: Database query timeout (100ms)
  ✓ C-002: Session management (JWT, Redis, 30min)
  ✓ C-003: Password hashing (bcrypt, cost 12)
  ✓ C-004: HTTPS required (protocol enforcement)
  ✓ C-005: Rate limiting (10/min per IP)

Formulas (3):
  ✓ F-001: Lockout expiry time calculation
  ✓ F-002: Remaining lockout time calculation
  ✓ F-003: Password strength scoring

Total: 13 specifications (5 BR + 5 C + 3 F)

Autogeneration Ready:
  ✓ BR-001 → validate_email() + tests
  ✓ BR-002 → validate_password() + tests
  ✓ BR-003 → LockoutTracker class + tests
  ✓ F-001 → calculate_lockout_expiry() + tests
  ✓ F-002 → calculate_remaining_time() + tests
  ✓ F-003 → calculate_password_strength() + tests

Updated: docs/requirements/authentication.md

✅ Disambiguation Complete!
   Requirement now precise enough for code generation
```

---

## Skills Used

This orchestrator invokes:
1. `extract-business-rules` - Extract BR-* specifications
2. `extract-constraints` - Extract C-* specifications
3. `extract-formulas` - Extract F-* specifications

---

## Prerequisites Check

Before invoking:
1. REQ-* requirement exists (from requirement-extraction)
2. Requirement has description and acceptance criteria

If prerequisites not met:
- No REQ-* → Invoke `requirement-extraction` first

---

## Notes

**Why disambiguation?**
- **Enables code generation**: BR-*, C-*, F-* are precise enough to auto-generate code
- **Reduces ambiguity**: No developer guessing about requirements
- **Improves testability**: Each BR-* becomes a test case
- **Documents decisions**: Constraints acknowledge ecosystem E(t)

**Disambiguation vs Traditional Requirements**:
```
Traditional: "Email must be valid"
  → Vague, developers guess regex pattern

Disambiguated: "BR-001: Email validation"
  → Regex: ^[a-zA-Z0-9._%+-]+@...
  → Error: "Invalid email format"
  → Autogenerate validate_email() function
  → Clear, testable, auto-generatable
```

**Homeostasis Goal**:
```yaml
desired_state:
  all_requirements_disambiguated: true
  autogeneration_ready: true
  vague_requirements: 0
```

**"Excellence or nothing"** 🔥
