---
name: pr-review-common-patterns
description: Common patterns in PR reviews including false positives, security vulnerabilities, N+1 queries, breaking changes, and edge cases. Use when analyzing code, verifying findings, or understanding typical issues.
allowed-tools:
  - Read
---

# PR Review Common Patterns

**Purpose**: Catalog recurring patterns found during PR reviews to improve accuracy and speed.

**Use when**: Analyzing code changes, verifying agent findings, understanding typical issues

---

## Pattern Index

| Category | Count | Common Examples |
|----------|-------|-----------------|
| False Positives | 4 | Validation in caller, error handling missed, type hints ignored |
| Security Vulnerabilities | 7 | SQL injection, auth bypass, secrets, PII exposure |
| Performance Issues | 5 | N+1 queries, O(n²) regressions, removed caching |
| Breaking Changes | 4 | Added required param, return type change, removed function |
| Edge Cases | 4 | None/empty/0, unicode, concurrency, boundary conditions |

---

## DO NOT FLAG (Never Report These)

### Personal Preferences
- Variable naming style ("data" vs "result", "i" vs "index")
- Comment style ("TODO" vs "FIXME" vs "NOTE")
- Import ordering (unless breaks project linting)
- Blank line count between functions
- Single vs double quotes (unless project has standard)
- Trailing commas in lists/dicts
- f-strings vs .format() vs % formatting

### Style Nitpicks (Not Real Issues)
- Line length violations <5 chars over limit
- Missing docstrings on private/helper functions
- Variable names that are "not descriptive enough" (subjective)
- "Magic numbers" that are obvious (port 443, HTTP 200, 100%)
- Comments that "could be better" (subjective)
- Whitespace alignment preferences
- Parentheses around return values

### Theoretical Issues (No Proof)
- "This could be problematic" (without reproduction scenario)
- "Might cause issues if..." (without demonstrating the "if")
- "Could be refactored" (without measurable benefit)
- "Not following best practices" (vague, no standard)
- "Consider using X instead" (unless X solves concrete problem)
- "This looks wrong" (without evidence)

### Not Project Standards
- Missing type hints (unless project requires them)
- Line length >80 chars (if project allows 88/100/120)
- Naming conventions different from your preference
- Import style (absolute vs relative) unless project standard exists
- Docstring format (Google vs NumPy vs Sphinx) unless standard exists

### Already Handled Elsewhere
- Validation in caller/entry point (agent only checked function)
- Error handling in try/except wrapping call
- Type hints guarantee safety (non-None, correct type)
- Authentication at decorator/middleware level
- Logging in caller or error handler

**THE RULE: If you can't write a failing test case, DON'T FLAG IT.**

---

## False Positive Patterns

### Pattern 1: Validation in Caller (Not Function)

**What agent reports**: "Missing validation on parameter"

**Reality**: Validation exists in calling code

**Example**:
```python
# Agent flags this:
def process(amount):
    return amount * 0.1  # No validation!

# But misses this:
def api_handler(request):
    if request.amount < 0:
        raise ValueError  # Validation at entry point
    return process(request.amount)
```

**Why it happens**: Agent only reads flagged function, not callers

**How to verify**: Use Grep to find all callers, check for validation at entry points

**Decision**: FALSE_POSITIVE if validation exists at API/entry layer

---

### Pattern 2: Error Handling in Caller

**What agent reports**: "Potential division by zero"

**Reality**: try/except wraps the call

**Example**:
```python
# Agent flags this:
def average(total, count):
    return total / count  # count could be 0!

# But misses this:
try:
    avg = average(total, count)
except ZeroDivisionError:
    avg = 0  # Error handled appropriately
```

**Why it happens**: Agent doesn't trace execution to catch blocks

**How to verify**: Search for try/except blocks around function calls

**Decision**: FALSE_POSITIVE if error handling exists and is appropriate

---

### Pattern 3: Type Hints Guarantee Safety

**What agent reports**: "None dereference possible"

**Reality**: Type hints enforce non-None at call sites

**Example**:
```python
# Agent flags this:
def process(user):
    return user.email.lower()  # user could be None!

# But type hint guarantees non-None:
def process(user: User) -> str:  # Type checker enforces this
    return user.email.lower()
```

**Why it happens**: Agent ignores type hint semantics

**How to verify**: Check type hints, look for Optional[] vs bare type

**Decision**: FALSE_POSITIVE if type hints guarantee safety (and project uses type checking)

---

### Pattern 4: Intentional Public Endpoints

**What agent reports**: "Missing auth check"

**Reality**: Endpoint is intentionally public

**Example**:
```python
# Agent flags this:
@app.route('/api/health')
def health_check():
    return {"status": "ok"}  # No @requires_auth!

# But this is intentional - health checks should be public
```

**Why it happens**: Agent doesn't understand business logic intent

**How to verify**: Check endpoint purpose - health, metrics, public APIs

**Decision**: FALSE_POSITIVE if public access is intentional

---

## Security Vulnerability Patterns

### Pattern 1: SQL Injection

**Evidence**:
```python
# CRITICAL vulnerability
query = f"SELECT * FROM users WHERE id={user_id}"
cursor.execute(query)  # user_id from request.args
```

**Exploitation**:
```
?user_id=1 OR 1=1        → Returns all users
?user_id=1; DROP TABLE   → Deletes table
```

**Fix**:
```python
# Use parameterized query
cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
```

**Severity**: CRITICAL (if user input) / HIGH (if internal)

---

### Pattern 2: Auth Bypass

**Evidence**:
```python
# CRITICAL vulnerability
@app.route('/admin/delete', methods=['POST'])
def delete_user():
    user_id = request.json.get('user_id')
    db.delete({'user_id': user_id})  # No auth check!
```

**Exploitation**: Any unauthenticated user can call `/admin/delete`

**Fix**:
```python
@app.route('/admin/delete', methods=['POST'])
@requires_auth
@requires_role('admin')
def delete_user():
    ...
```

**Severity**: CRITICAL

---

### Pattern 3: Hardcoded Secrets

**Evidence**:
```python
# CRITICAL vulnerability
API_KEY = "sk_live_abc123xyz789"
PASSWORD = "admin123"
DB_URL = "mongodb://admin:password@localhost"
```

**Impact**: Secrets exposed in repository, extractable from version history

**Fix**:
```python
# Use environment variables
API_KEY = os.environ['API_KEY']
PASSWORD = os.environ['DB_PASSWORD']
DB_URL = os.environ['DATABASE_URL']
```

**Severity**: CRITICAL

---

### Pattern 4: PII in Logs

**Evidence**:
```python
# HIGH severity issue
LOG.info(f"User {email} logged in")
LOG.debug(f"Processing SSN: {ssn}")
LOG.error(f"Failed payment for card {card_number}")
```

**Impact**: PII exposed in log files - GDPR/CCPA violation, targeted phishing risk

**Fix**:
```python
# Use IDs instead of PII
LOG.info("User logged in", extra={"user_id": user_id})
LOG.debug("Processing SSN", extra={"user_id": user_id})
LOG.error("Failed payment", extra={"user_id": user_id})
```

**Severity**: HIGH (legal compliance risk)

---

### Pattern 5: XSS Vulnerabilities

**Evidence**:
```python
# HIGH severity issue
@app.route('/profile')
def profile():
    username = request.args.get('name')
    return f"<h1>Welcome {username}</h1>"  # No escaping!
```

**Exploitation**:
```
?name=<script>alert(document.cookie)</script>
```

**Fix**:
```python
from markupsafe import escape

@app.route('/profile')
def profile():
    username = escape(request.args.get('name'))
    return f"<h1>Welcome {username}</h1>"
```

**Severity**: HIGH (if user content) / MEDIUM (if admin content)

---

### Pattern 6: CSRF Missing

**Evidence**:
```python
# HIGH severity issue
@app.route('/api/transfer', methods=['POST'])
@requires_auth
def transfer_funds():
    amount = request.json.get('amount')
    # No CSRF token check!
```

**Exploitation**: Attacker tricks logged-in user to visit malicious site that POSTs to /api/transfer

**Fix**:
```python
@app.route('/api/transfer', methods=['POST'])
@requires_auth
@csrf.protect  # Add CSRF protection
def transfer_funds():
    ...
```

**Severity**: HIGH (state-changing operations)

---

### Pattern 7: Improper try/except (Hiding Auth Failures)

**Evidence**:
```python
# CRITICAL vulnerability
try:
    verify_token(token)
    user = get_user_from_token(token)
except Exception:
    pass  # Silent failure - continues execution!

# Code continues as if auth succeeded
```

**Why dangerous**: Auth failure silently ignored - unauthenticated users get access

**Fix**:
```python
# Let exception propagate
verify_token(token)  # Will raise if invalid
user = get_user_from_token(token)

# OR return 401
if not verify_token(token):
    return abort(401)
```

**Severity**: CRITICAL

---

## Performance Issue Patterns

### Pattern 1: N+1 Query Problem

**Evidence**:
```python
# HIGH severity performance issue
users = db.users.find()
for user in users:
    orders = db.orders.find_one({'user_id': user.id})  # N queries!
    process(user, orders)
```

**Impact**: 1000 users = 1000 DB queries (should be 1-2 queries)

**Before/After**:
```python
# BEFORE: O(n) queries
for user in users:
    orders = db.find_one({'user_id': user.id})

# AFTER: O(1) queries
user_ids = [u.id for u in users]
orders_map = {o['user_id']: o for o in db.find({'user_id': {'$in': user_ids}})}
for user in users:
    orders = orders_map.get(user.id)
```

**Severity**: HIGH (1000x more queries)

---

### Pattern 2: Algorithm Complexity Regression (O(n) → O(n²))

**Evidence**:
```python
# CRITICAL performance regression
# BEFORE: O(n) - dict lookup
matches_dict = {m.id: m for m in list2}
for item in list1:
    match = matches_dict.get(item.id)

# AFTER: O(n²) - nested loops
for item in list1:
    for match in list2:
        if item.id == match.id:  # 1M comparisons for 1000 items!
            process(match)
```

**Impact**: 1000 items: 1000 ops → 1,000,000 ops (1000x slower)

**Severity**: CRITICAL (quadratic blowup)

---

### Pattern 3: Removed Caching

**Evidence**:
```python
# HIGH severity regression
# BEFORE: Cached expensive calculation
@lru_cache
def expensive_calculation(params):
    return heavy_compute(params)

# AFTER: No cache
def expensive_calculation(params):  # Called 1000x per request!
    return heavy_compute(params)
```

**Impact**: 1 calculation + 999 cache hits → 1000 calculations (1000x more work)

**Severity**: HIGH

---

### Pattern 4: Removed Batch Operations

**Evidence**:
```python
# HIGH severity regression
# BEFORE: Single batch insert
db.insert_many(items)  # 1 round-trip

# AFTER: Individual inserts
for item in items:
    db.insert_one(item)  # 100 round-trips!
```

**Impact**: 100 items = 100x more network overhead

**Severity**: HIGH

---

### Pattern 5: MongoDB Aggregation - Late $match

**Evidence**:
```python
# MEDIUM severity issue
# BEFORE: Filter early
pipeline = [
    {'$match': {'status': 'active'}},  # Filter to 1000 docs
    {'$project': {...}},  # Process 1000 docs
]

# AFTER: Filter late
pipeline = [
    {'$project': {...}},  # Process 1M docs!
    {'$match': {'status': 'active'}},  # Filter to 1000 docs
]
```

**Impact**: Processing 1M docs instead of 1000

**Severity**: MEDIUM (optimization opportunity)

---

## Breaking Change Patterns

### Pattern 1: Added Required Parameter

**Evidence**:
```python
# BEFORE
def calculate_total(amount):
    return amount * 1.1

# AFTER
def calculate_total(amount, tax_rate):  # tax_rate is required!
    return amount * (1 + tax_rate)
```

**Impact**:
```python
# All callers break:
total = calculate_total(100)  # TypeError: missing required argument
```

**Callers affected**: Use Grep to find all `calculate_total(` calls

**Fix**:
```python
# Make parameter optional:
def calculate_total(amount, tax_rate=0.1):
    return amount * (1 + tax_rate)
```

**Severity**: CRITICAL (breaks all callers)

---

### Pattern 2: Changed Return Type

**Evidence**:
```python
# BEFORE
def get_balance(user_id) -> float:
    return 123.45

# AFTER
def get_balance(user_id) -> Decimal:
    return Decimal('123.45')
```

**Impact**:
```python
# Callers doing float math may break:
balance = get_balance(user_id)
if balance > 0.0:  # Comparing Decimal to float
    total = balance + 10.0  # Decimal + float = precision loss
```

**Severity**: HIGH (type incompatibility)

---

### Pattern 3: Removed Function

**Evidence**:
```python
# BEFORE
def legacy_import(data):
    ...

# AFTER
# Function removed entirely
```

**Impact**: All callers raise `AttributeError: 'module' has no attribute 'legacy_import'`

**Callers affected**: Use Grep to find all `legacy_import(` calls

**Severity**: CRITICAL (immediate breakage)

---

### Pattern 4: Changed Behavior (Return Value)

**Evidence**:
```python
# BEFORE: Returns None on not found
def get_user(user_id):
    return db.find_one({'id': user_id})  # None if not found

# AFTER: Raises exception on not found
def get_user(user_id):
    user = db.find_one({'id': user_id})
    if not user:
        raise UserNotFoundError  # Different behavior!
    return user
```

**Impact**:
```python
# Callers expecting None will crash:
user = get_user(user_id)
if user is None:  # Never reached - exception raised instead
    handle_not_found()
```

**Severity**: HIGH (behavioral breaking change)

---

## Edge Case Patterns

### Pattern 1: None/Empty/Zero Handling

**Common issues**:
```python
# None dereference
def process(user):
    return user.email.lower()  # Crashes if user is None

# Empty collection
items = get_items()
first = items[0]  # IndexError if items is []

# Division by zero
avg = total / count  # ZeroDivisionError if count is 0

# Empty string
name = user.name.strip()
if name:  # Check emptiness after strip
    process(name)
```

**Verification checklist**:
- [ ] None checks before dereference
- [ ] Empty list checks before indexing
- [ ] Zero checks before division
- [ ] Empty string checks after strip/processing

---

### Pattern 2: Unicode and Large Inputs

**Common issues**:
```python
# Unicode handling
name = user.name.lower()  # Works for ASCII, but what about "ΔΗΜΟΣ"?

# Large inputs (DoS)
description = request.json.get('description')  # No size limit!
# Attacker sends 100MB string

# String encoding
email.encode('ascii')  # UnicodeEncodeError for "user@exämple.com"
```

**Verification checklist**:
- [ ] Input size limits enforced
- [ ] Unicode handling tested
- [ ] Encoding/decoding uses utf-8
- [ ] Large payloads rejected

---

### Pattern 3: Concurrent Access

**Common issues**:
```python
# Race condition
value = redis.get(key)
new_value = process(value)
redis.set(key, new_value)  # Not atomic - race condition!

# Cache invalidation race
def update_user(user_id, data):
    db.update({'id': user_id}, data)
    cache.delete(f"user:{user_id}")  # Another request might cache stale data
```

**Verification checklist**:
- [ ] Check-then-act patterns (race conditions)
- [ ] Cache invalidation order
- [ ] Distributed locks if needed
- [ ] Atomic operations used

---

### Pattern 4: Boundary Conditions

**Common issues**:
```python
# Off-by-one
for i in range(len(items)):
    if i < len(items):  # Redundant check - range already handles this
        process(items[i])

# Integer overflow (rare in Python)
large_num = 2**63 - 1
result = large_num + 1  # Python handles this, but C/Java don't

# Float precision
if price == 0.1 + 0.2:  # False! Float precision issues
    # Use: if abs(price - 0.3) < 0.001

# Negative numbers
def calculate_age(birth_year):
    age = current_year - birth_year  # Could be negative if birth_year > current_year
```

**Verification checklist**:
- [ ] Loop boundaries correct
- [ ] Float comparisons use epsilon
- [ ] Negative number handling
- [ ] Min/max value checks

---

## Quick Reference Checklist

### Verifying Agent Findings

**For each finding**:
1. Read ENTIRE function (not just flagged line)
2. Find ALL callers (use Grep across codebase)
3. Check error handling (try/except, if checks)
4. Verify business logic intent (public endpoint? intentional?)
5. If uncertain, flag as "needs_verification" (not false positive)

### Security Review Priorities

**Always check**:
- [ ] Hardcoded secrets
- [ ] PII in logs
- [ ] try/except hiding errors

**High scrutiny (external APIs)**:
- [ ] SQL/NoSQL injection
- [ ] Auth bypass
- [ ] Input validation
- [ ] XSS/CSRF

**Medium scrutiny (internal APIs)**:
- [ ] Injection vulnerabilities
- [ ] Secrets in logs

### Performance Review Priorities

**Always check**:
- [ ] Queries inside loops (N+1)
- [ ] Nested loops (O(n²))
- [ ] Removed caching

**Check if high-volume**:
- [ ] Individual vs batch operations
- [ ] Algorithm complexity changes
- [ ] Memory allocation patterns

### Breaking Change Review

**Always check**:
- [ ] Function signature changes
- [ ] Return type changes
- [ ] Behavior changes
- [ ] Removed functions

**For each change**:
1. Find ALL callers (Grep entire codebase)
2. Check if callers handle new signature/type/behavior
3. Include test code in analysis

---

## Using Patterns in Reviews

### Pattern Matching Workflow

1. **Initial scan**: Does code match known pattern?
2. **Classify**: False positive? Security? Performance? Breaking change?
3. **Verify**: Check evidence matches pattern exactly
4. **Adjust severity**: Context-aware (external vs internal)
5. **Provide fix**: Reference pattern solution

### When Patterns Don't Match

**If uncertain**:
- Flag as "needs_verification"
- Explain what's unclear
- Provide verification steps
- Don't force-fit pattern

### Severity Calibration

| Pattern Type | Base Severity | Adjust for Context |
|--------------|---------------|-------------------|
| SQL Injection | CRITICAL | → MEDIUM if internal only |
| Auth Bypass | CRITICAL | → N/A if intentionally public |
| N+1 Queries | HIGH | → MEDIUM if low traffic |
| Breaking Change | CRITICAL | → HIGH if internal API |
| PII in Logs | HIGH | → MEDIUM if admin logs only |

---

## Pattern Evolution

**When to add new patterns**:
- Same false positive appears 3+ times
- New vulnerability class discovered
- Recurring performance anti-pattern

**When to update patterns**:
- Fix proven more effective
- Severity calibration needed
- New exploitation technique

**Pattern validation**:
- Document example PR where pattern appeared
- Track false positive rate
- Update with lessons learned

---

## Summary

**Total patterns cataloged**: 24

**Coverage**:
- False Positives: 4 patterns
- Security: 7 patterns
- Performance: 5 patterns
- Breaking Changes: 4 patterns
- Edge Cases: 4 patterns

**Most common issues**:
1. Agent missed validation in caller (false positive)
2. SQL injection (security)
3. N+1 queries (performance)
4. Added required parameter (breaking change)
5. None/empty/zero handling (edge case)

**Remember**: Patterns are guidelines, not rules. Always verify with evidence and adjust for context.
