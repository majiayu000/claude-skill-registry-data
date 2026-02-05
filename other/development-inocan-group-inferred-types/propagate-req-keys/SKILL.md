---
name: propagate-req-keys
description: Homeostatic actuator that tags code, tests, and commits with REQ-* keys for traceability. Adds "# Implements:" tags to code and "# Validates:" tags to tests. Use when code or tests are missing requirement tags.
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# propagate-req-keys

**Skill Type**: Actuator (Homeostasis)
**Purpose**: Tag code and tests with REQ-* keys for traceability
**Prerequisites**: REQ-* key exists and is validated

---

## Agent Instructions

You are an **Actuator** in the homeostasis system. Your job is to **correct deviations** from the desired state.

**Desired State**: `all_artifacts_tagged = true` (all code/tests have REQ-* tags)

Your goal is to **add REQ-* tags** to code and tests for bidirectional traceability.

---

## Workflow

### Step 1: Understand What to Tag

**Input**: REQ-* key and files to tag

**Determine tagging target**:
- **Implementation files** (src/): Add `# Implements: REQ-*`
- **Test files** (tests/): Add `# Validates: REQ-*`
- **Feature files** (features/): Add `# Validates: REQ-*`
- **Commit messages**: Include REQ-* in subject or footer

---

### Step 2: Tag Implementation Files

**Add tag at top of file or above function/class**:

**Python**:
```python
# Before
def login(email: str, password: str) -> LoginResult:
    """User login functionality"""
    return authenticate(email, password)

# After
# Implements: <REQ-ID>
def login(email: str, password: str) -> LoginResult:
    """User login functionality"""
    return authenticate(email, password)
```

**TypeScript**:
```typescript
// Before
export function login(email: string, password: string): LoginResult {
  return authenticate(email, password);
}

// After
// Implements: <REQ-ID>
export function login(email: string, password: string): LoginResult {
  return authenticate(email, password);
}
```

**Java**:
```java
// Before
public class LoginService {
    public LoginResult login(String email, String password) {
        return authenticate(email, password);
    }
}

// After
// Implements: <REQ-ID>
public class LoginService {
    public LoginResult login(String email, String password) {
        return authenticate(email, password);
    }
}
```

**Tag Placement Rules**:
- **Function/method**: Tag immediately above function definition
- **Class**: Tag immediately above class definition
- **File**: Tag at top of file (if entire file implements one REQ-*)
- **Multiple REQ-***: Use comma-separated list

**Multiple requirements example**:
```python
# Implements: <REQ-ID>, REQ-NFR-SEC-001
def secure_login(email: str, password: str, mfa_token: str) -> LoginResult:
    """Secure login with MFA"""
    pass
```

---

### Step 3: Tag Test Files

**Add tag at top of test file or above test function**:

**Python (pytest)**:
```python
# Before
def test_user_login_with_valid_credentials():
    result = login("user@example.com", "SecurePass123!")
    assert result.success == True

# After
# Validates: <REQ-ID>
def test_user_login_with_valid_credentials():
    result = login("user@example.com", "SecurePass123!")
    assert result.success == True
```

**TypeScript (Jest)**:
```typescript
// Before
test('user login with valid credentials', () => {
  const result = login('user@example.com', 'SecurePass123!');
  expect(result.success).toBe(true);
});

// After
// Validates: <REQ-ID>
test('user login with valid credentials', () => {
  const result = login('user@example.com', 'SecurePass123!');
  expect(result.success).toBe(true);
});
```

**Gherkin (BDD)**:
```gherkin
# Before
Feature: User Login
  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    Then I should see "Welcome"

# After
# Validates: <REQ-ID>
Feature: User Login
  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    Then I should see "Welcome"
```

---

### Step 4: Tag Business Rules

**Tag BR-*, C-*, F-* implementations**:

```python
# Implements: <REQ-ID>, BR-001
def validate_email(email: str) -> bool:
    """Email validation (BR-001)"""
    pattern = r'^[a-zA-Z0-9._%+-]+@...'
    return re.match(pattern, email) is not None

# Implements: BR-002
def validate_password_length(password: str) -> bool:
    """Password minimum length (BR-002)"""
    return len(password) >= 12

# Implements: F-001
def calculate_stripe_fee(amount: float) -> float:
    """Stripe fee calculation (F-001)"""
    return (amount * 0.029) + 0.30
```

---

### Step 5: Tag Commit Messages

**Add REQ-* to commit messages**:

**Format 1: In subject line**:
```
feat: Add user login (<REQ-ID>)
```

**Format 2: In footer**:
```
feat: Add user login

Implement authentication with email and password.

Implements: <REQ-ID>
Validates: BR-001, BR-002, BR-003
```

**Format 3: Both**:
```
feat: Add user login (<REQ-ID>)

Implement authentication with email and password.

Business Rules:
- BR-001: Email validation
- BR-002: Password minimum length
- BR-003: Account lockout

Implements: <REQ-ID>
Validates: BR-001, BR-002, BR-003
```

---

### Step 6: Verify Tags Added

**After tagging, verify**:

```bash
# Verify implementation tags
grep -rn "# Implements: <REQ-ID>" src/

# Verify test tags
grep -rn "# Validates: <REQ-ID>" tests/

# Count tags added
echo "Implementation tags: $(grep -rc "# Implements:" src/ | grep -v ":0" | wc -l)"
echo "Test tags: $(grep -rc "# Validates:" tests/ | grep -v ":0" | wc -l)"
```

---

## Output Format

When you complete tagging:

```
[PROPAGATE REQ-KEYS - <REQ-ID>]

Files Tagged:

Implementation Files (3):
  ✓ src/auth/login.py:23
    Added: # Implements: <REQ-ID>
  ✓ src/auth/validators.py:67
    Added: # Implements: <REQ-ID>, BR-001
  ✓ src/auth/lockout.py:34
    Added: # Implements: <REQ-ID>, BR-003

Test Files (2):
  ✓ tests/auth/test_login.py:15
    Added: # Validates: <REQ-ID>
  ✓ features/authentication.feature:8
    Added: # Validates: <REQ-ID>

Total Tags Added: 5
  - Implementation tags: 3
  - Test tags: 2

Traceability Status:
  Forward: <REQ-ID> → 3 code files, 2 test files ✅
  Backward: Code/tests → <REQ-ID> ✅

Verification:
  ✓ All tags added
  ✓ Tags follow format
  ✓ Traceability established

✅ Propagation Complete!
```

---

## Homeostasis Behavior

**Triggering this actuator**:
1. **Sensor detects**: Requirements without tags (via check-requirement-coverage)
2. **Signal**: "Need tags for <REQ-ID>"
3. **User confirms** or auto-invoke if configured
4. **Actuator runs**: Add tags
5. **Re-check**: Sensor should show homeostasis achieved

**Homeostasis loop**:
```
Sensor (check-requirement-coverage):
  → Deviation: <REQ-ID> has no tags
  → Signal: "Missing tags"
  ↓
Actuator (propagate-req-keys):
  → Add tags to code and tests
  → Report: "Tags added"
  ↓
Sensor (check-requirement-coverage):
  → Check: <REQ-ID> now has tags
  → Status: Homeostasis achieved ✓
```

---

## Prerequisites Check

Before invoking this skill, ensure:
1. REQ-* key exists and is validated
2. Files to tag exist (code or tests)

If prerequisites not met:
- Invalid REQ-* → Use `requirement-traceability` skill to validate
- No files → Ask user which files implement the requirement

---

## Tag Format Options

### Option 1: Single Line Above

```python
# Implements: <REQ-ID>
def login(email, password):
    pass
```

### Option 2: Inline with Docstring

```python
def login(email, password):
    """
    User login functionality.

    Implements: <REQ-ID>
    Business Rules: BR-001, BR-002, BR-003
    """
    pass
```

### Option 3: Multi-Line Block

```python
# ═══════════════════════════════════════
# Implements: <REQ-ID>
# Business Rules: BR-001, BR-002, BR-003
# ═══════════════════════════════════════
def login(email, password):
    pass
```

**Recommended**: Option 1 (single line, consistent, greppable)

---

## Bulk Tagging

**When tagging multiple files**:

```python
# Tag all files in a module
files_to_tag = [
    ("src/auth/login.py", "<REQ-ID>"),
    ("src/auth/validators.py", "<REQ-ID>, BR-001"),
    ("src/auth/lockout.py", "<REQ-ID>, BR-003"),
]

for file_path, req_keys in files_to_tag:
    add_tag_to_file(file_path, f"# Implements: {req_keys}")
```

---

## Next Steps

After tagging:
1. Verify tags with `grep -rn "# Implements:" src/`
2. Run coverage check again (should show improved coverage)
3. Commit changes: `git commit -m "docs: Add REQ-* tags for traceability"`

---

## Configuration

```yaml
plugins:
  - name: "@aisdlc/aisdlc-core"
    config:
      propagation:
        auto_propagate_on_commit: true        # Auto-tag before commit
        tag_format: "# Implements: {REQ-KEY}"
        test_tag_format: "# Validates: {REQ-KEY}"
        include_business_rules: true          # Also tag BR-*, C-*, F-*
        placement: "above"                    # above | inline | block
```

---

## Notes

**Why propagate REQ-* keys?**
- **Bidirectional traceability**: Forward (REQ → code) and backward (code → REQ)
- **Impact analysis**: Find all code for a requirement
- **Debugging**: Trace production issues to requirements
- **Compliance**: Prove requirements are implemented

**Tag visibility**:
- Tags are **source code comments** (visible in code reviews)
- Tags are **greppable** (searchable with grep/ripgrep)
- Tags are **version controlled** (tracked in git)
- Tags are **persistent** (don't disappear on refactoring)

**Homeostasis Goal**:
```yaml
desired_state:
  all_code_tagged: true
  all_tests_tagged: true
  tags_follow_format: true
  traceability_bidirectional: true
```

**"Excellence or nothing"** 🔥
