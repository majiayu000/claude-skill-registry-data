---
name: error-handling-completeness
description: Evaluates if error handling is sufficient for new code - checks try-catch coverage, logging, user messages, retry logic. Focuses on external calls and user-facing code.
---

# Error Handling Completeness Skill

**Purpose**: Prevent production crashes with systematic error handling.

**Trigger Words**: API call, external, integration, network, database, file, user input, async, promise, await

---

## Quick Decision: Needs Error Handling Check?

```python
def needs_error_check(code_context: dict) -> bool:
    """Decide if error handling review is needed."""

    # High-risk operations (always check)
    high_risk = [
        "fetch", "axios", "requests", "http",  # HTTP calls
        "db.", "query", "execute",  # Database
        "open(", "read", "write",  # File I/O
        "json.loads", "json.parse",  # JSON parsing
        "int(", "float(",  # Type conversions
        "subprocess", "exec",  # External processes
        "await", "async",  # Async operations
    ]

    code = code_context.get("code", "").lower()
    return any(risk in code for risk in high_risk)
```

---

## Error Handling Checklist (Fast)

### 1. **External API Calls** (Most Critical)
```python
# ❌ BAD - No error handling
def get_user_data(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()  # What if network fails? 404? Timeout?

# ✅ GOOD - Complete error handling
def get_user_data(user_id):
    try:
        response = requests.get(
            f"https://api.example.com/users/{user_id}",
            timeout=5  # Timeout!
        )
        response.raise_for_status()  # Check HTTP errors
        return response.json()

    except requests.Timeout:
        logger.error(f"Timeout fetching user {user_id}")
        raise ServiceUnavailableError("User service timeout")

    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise UserNotFoundError(f"User {user_id} not found")
        logger.error(f"HTTP error fetching user: {e}")
        raise

    except requests.RequestException as e:
        logger.error(f"Network error: {e}")
        raise ServiceUnavailableError("Cannot reach user service")
```

**Quick Checks**:
- ✅ Timeout set?
- ✅ HTTP errors handled?
- ✅ Network errors caught?
- ✅ Logged?
- ✅ User-friendly error returned?

---

### 2. **Database Operations**
```python
# ❌ BAD - Swallows errors
def delete_user(user_id):
    try:
        db.execute("DELETE FROM users WHERE id = ?", [user_id])
    except Exception:
        pass  # Silent failure!

# ✅ GOOD - Specific handling
def delete_user(user_id):
    try:
        result = db.execute("DELETE FROM users WHERE id = ?", [user_id])
        if result.rowcount == 0:
            raise UserNotFoundError(f"User {user_id} not found")

    except db.IntegrityError as e:
        logger.error(f"Cannot delete user {user_id}: {e}")
        raise DependencyError("User has related records")

    except db.OperationalError as e:
        logger.error(f"Database error: {e}")
        raise DatabaseUnavailableError()
```

**Quick Checks**:
- ✅ Specific exceptions (not bare `except`)?
- ✅ Logged?
- ✅ User-friendly error?

---

### 3. **File Operations**
```python
# ❌ BAD - File might not exist
def read_config():
    with open("config.json") as f:
        return json.load(f)

# ✅ GOOD - Handle missing file
def read_config():
    try:
        with open("config.json") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("config.json not found, using defaults")
        return DEFAULT_CONFIG
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config.json: {e}")
        raise ConfigurationError("Malformed config.json")
    except PermissionError:
        logger.error("Permission denied reading config.json")
        raise
```

**Quick Checks**:
- ✅ FileNotFoundError handled?
- ✅ JSON parse errors caught?
- ✅ Permission errors handled?

---

### 4. **Type Conversions**
```python
# ❌ BAD - Crash on invalid input
def process_age(age_str):
    age = int(age_str)  # What if "abc"?
    return age * 2

# ✅ GOOD - Validated
def process_age(age_str):
    try:
        age = int(age_str)
        if age < 0 or age > 150:
            raise ValueError("Age out of range")
        return age * 2
    except ValueError:
        raise ValidationError(f"Invalid age: {age_str}")
```

**Quick Checks**:
- ✅ ValueError caught?
- ✅ Range validation?
- ✅ Clear error message?

---

### 5. **Async/Await** (JavaScript/Python)
```javascript
// ❌ BAD - Unhandled promise rejection
async function fetchUser(id) {
    const user = await fetch(`/api/users/${id}`);
    return user.json();  // What if network fails?
}

// ✅ GOOD - Handled
async function fetchUser(id) {
    try {
        const response = await fetch(`/api/users/${id}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Failed to fetch user ${id}:`, error);
        throw new ServiceError("Cannot fetch user");
    }
}
```

**Quick Checks**:
- ✅ Try-catch around await?
- ✅ HTTP status checked?
- ✅ Logged?

---

## Error Handling Patterns

### Pattern 1: Retry with Exponential Backoff
```python
def call_api_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()

        except requests.Timeout:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # 1s, 2s, 4s
                logger.warning(f"Timeout, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise
```

**When to use**: Transient failures (network, rate limits)

---

### Pattern 2: Fallback Values
```python
def get_user_avatar(user_id):
    try:
        return fetch_from_cdn(user_id)
    except CDNError:
        logger.warning(f"CDN failed for user {user_id}, using default")
        return DEFAULT_AVATAR_URL
```

**When to use**: Non-critical operations, graceful degradation

---

### Pattern 3: Circuit Breaker
```python
class CircuitBreaker:
    def __init__(self, max_failures=5):
        self.failures = 0
        self.max_failures = max_failures
        self.is_open = False

    def call(self, func):
        if self.is_open:
            raise ServiceUnavailableError("Circuit breaker open")

        try:
            result = func()
            self.failures = 0  # Reset on success
            return result
        except Exception as e:
            self.failures += 1
            if self.failures >= self.max_failures:
                self.is_open = True
                logger.error("Circuit breaker opened")
            raise
```

**When to use**: Preventing cascading failures

---

## Output Format

```markdown
## Error Handling Report

**Status**: [✅ COMPLETE | ⚠️ GAPS FOUND]

---

### Missing Error Handling: 3

1. **[HIGH] No timeout on API call (api_client.py:45)**
   - **Issue**: `requests.get()` has no timeout
   - **Risk**: Indefinite hang if service slow
   - **Fix**:
     ```python
     response = requests.get(url, timeout=5)
     ```

2. **[HIGH] Unhandled JSON parse error (config.py:12)**
   - **Issue**: `json.load()` not wrapped in try-catch
   - **Risk**: Crash on malformed JSON
   - **Fix**:
     ```python
     try:
         config = json.load(f)
     except json.JSONDecodeError as e:
         logger.error(f"Invalid JSON: {e}")
         return DEFAULT_CONFIG
     ```

3. **[MEDIUM] Silent exception swallowing (db.py:89)**
   - **Issue**: `except Exception: pass`
   - **Risk**: Failures go unnoticed
   - **Fix**: Log error or use specific exception

---

**Good Practices Found**: 2
- ✅ Database errors logged properly (db.py:34)
- ✅ Retry logic on payment API (payments.py:67)

---

**Next Steps**:
1. Add timeout to API calls (5 min)
2. Wrap JSON parsing in try-catch (2 min)
3. Remove silent exception handlers (3 min)
```

---

## What This Skill Does NOT Do

❌ Catch every possible exception (too noisy)
❌ Force try-catch everywhere (only where needed)
❌ Replace integration tests
❌ Handle business logic errors (validation, etc.)

✅ **DOES**: Check critical error-prone operations (network, I/O, parsing)

---

## Configuration

```bash
# Strict mode: check all functions
export LAZYDEV_ERROR_HANDLING_STRICT=1

# Disable error handling checks
export LAZYDEV_DISABLE_ERROR_CHECKS=1
```

---

**Version**: 1.0.0
**Focus**: External calls, I/O, parsing, async
**Speed**: <2 seconds per file
