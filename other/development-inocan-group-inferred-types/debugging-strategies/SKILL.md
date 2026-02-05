---
name: debugging-strategies
description: Systematic debugging including root-cause tracing (trace backward through call stack), reproduction strategies, pdb/debugpy usage, logging analysis, binary search debugging, and error pattern recognition. Use when debugging errors, tracing bugs through call stacks, investigating production issues, or reproducing intermittent bugs.
allowed-tools:
  - Read
  - Bash
  - Grep
---

# Debugging Strategies

**Purpose:** Systematic approaches for debugging code, tracing root causes, and fixing bugs efficiently.

**When to use:** When debugging errors, investigating production issues, tracing bugs through call stacks, reproducing intermittent failures, or analyzing performance problems.

**For detailed examples and advanced techniques:** See reference.md

---

## Core Principles

1. **Root-cause tracing** - Bugs manifest deep in call stack, fix at source not symptom
2. **Reproduce first** - Can't fix what you can't reproduce consistently
3. **Binary search debugging** - Divide and conquer to isolate failures
4. **One bug at a time** - Fix, validate, then move to next issue
5. **Evidence over assumptions** - Verify with logs, debugger, or tests
6. **Minimal reproduction** - Strip away complexity until bug is isolated

---

## Root-Cause Tracing (obra Pattern)

**Problem:** Errors often manifest far from their actual cause. Stack trace shows where code crashes, not where the bug originates.

### The Backward Trace Technique

**Instead of fixing symptoms, trace backward to find the trigger:**

| Step | Action | Question to Ask |
|------|--------|-----------------|
| 1. **Error location** | Read stack trace | Where did code crash? |
| 2. **Immediate context** | Check surrounding code | What assumptions failed here? |
| 3. **Trace backward** | Follow call chain up | What caller provided bad input? |
| 4. **Find trigger** | Identify origin | Where did bad data enter system? |
| 5. **Fix at source** | Fix the trigger | Validate/sanitize at entry point |

### Example: Tracing AttributeError

```python
# SYMPTOM: Error manifests here
def process_user_data(user):
    return user.profile.email.lower()  # AttributeError: 'NoneType'

# TRACE BACKWARD: Who passed None?
def handle_request(request):
    user = get_user_from_token(request.headers['Authorization'])
    return process_user_data(user)  # Passed None here

# ROOT CAUSE: Exception handling returns None
def get_user_from_token(token):
    try:
        return db.find_user_by_token(token)
    except:
        return None  # BUG: Silent failure

# FIX AT SOURCE: Let exception propagate
def get_user_from_token(token):
    user = db.find_user_by_token(token)
    if not user:
        raise AuthenticationError(f"Invalid token")
    return user
```

**Anti-pattern:** Defensive coding at symptom
```python
# BAD - fixes symptom only
def process_user_data(user):
    if user and user.profile and user.profile.email:
        return user.profile.email.lower()
    return ""  # Silent failure continues
```

---

## Systematic Debugging Workflow

### 1. Understand the Error

Gather facts: error message, stack trace, operation, input triggering it.

```bash
python script.py 2>&1 | tee error.log  # Capture error
python -X dev script.py                # Enable debug mode
```

### 2. Reproduce Reliably

Can't fix what you can't reproduce. Create minimal test case.

```python
def test_reproduce_bug():
    """Minimal case that triggers bug."""
    with pytest.raises(AuthenticationError):
        authenticate("expired_token")  # Should raise, but doesn't
```

### 3. Isolate with Binary Search

Add checkpoints to narrow down failure location. Test half the code, then quarters, etc.

### 4. Form Hypothesis

Predict root cause based on evidence from logs, stack trace, and code inspection.

### 5. Test Hypothesis

Verify with temporary logging or debugger before making changes.

### 6. Fix at Root Cause

Fix where problem originates, not where it manifests.

### 7. Validate Fix

```bash
pytest tests/test_auth.py::test_expired_token -v  # Specific test
pytest tests/ -v                                   # Full suite
```

---

## Binary Search Debugging

**Divide problem space in half repeatedly until bug isolated.**

### Binary Search Over Code

Comment out half the code, test, repeat until isolated.

### Binary Search Over Data

```python
# Test with half the data at a time
process(records[:500])  # Success
process(records[500:])  # Fails! Bug in second half
# Continue narrowing to specific record
```

### Binary Search Over Time (git bisect)

```bash
git bisect start
git bisect bad          # Current broken
git bisect good v1.2.0  # v1.2.0 worked
# Test, mark good/bad until isolated
git bisect reset
```

---

## Python Debugger (pdb)

### Basic Usage

```python
# Set breakpoint
def buggy_function(data):
    breakpoint()  # Python 3.7+
    result = process(data)
    return result

# Older Python
import pdb; pdb.set_trace()
```

### Essential pdb Commands

| Command | Shortcut | Purpose |
|---------|----------|---------|
| `list` | `l` | Show code around current line |
| `next` | `n` | Execute next line (step over) |
| `step` | `s` | Step into function call |
| `continue` | `c` | Continue until next breakpoint |
| `print(var)` | `p var` | Print variable value |
| `where` | `w` | Show stack trace |
| `up` / `down` | `u` / `d` | Navigate call stack |
| `break file.py:42` | `b file.py:42` | Set breakpoint at line |
| `quit` | `q` | Exit debugger |

### Example pdb Session

```python
# Code
def authenticate(token):
    breakpoint()
    user = db.find_user_by_token(token)
    if not user:
        raise AuthenticationError("Invalid token")
    return user

# Session
$ python app.py
> /app/auth.py(3)authenticate()
-> user = db.find_user_by_token(token)
(Pdb) p token
'expired_xyz'
(Pdb) n
> /app/auth.py(4)authenticate()
-> if not user:
(Pdb) p user
None
(Pdb) # Found it! user is None
```

**For debugpy (VS Code) and advanced pdb techniques:** See reference.md

---

## Logging for Debugging

### Strategic Log Placement

| Location | What to Log | Why |
|----------|-------------|-----|
| **Function entry** | Parameters, operation name | Trace execution flow |
| **Before external calls** | Request details, target | Debug integration issues |
| **After external calls** | Response status, data | Verify external behavior |
| **Decision points** | Condition values, branch taken | Understand control flow |
| **Error paths** | Error details, context | Diagnose failures |

### Effective Debug Logging

```python
import logging
LOG = logging.getLogger(__name__)

def authenticate(token):
    LOG.debug(f"authenticate called with token={token[:8]}...")

    try:
        user = db.find_user_by_token(token)
        LOG.debug(f"DB returned user={user}")

        if not user:
            LOG.warning(f"Token {token[:8]}... not found")
            raise AuthenticationError("Invalid token")

        LOG.info(f"User {user.id} authenticated")
        return user

    except DBConnectionError as e:
        LOG.error(f"DB connection failed: {e}")
        raise
```

**Logging levels:**
- `DEBUG` - Detailed trace (params, values)
- `INFO` - Operation milestones
- `WARNING` - Recoverable issues
- `ERROR` - Failures requiring attention

### Temporary Debug Logging

```python
# Prefix with DEBUG: for easy removal
def complex_function(data):
    LOG.debug(f"DEBUG: data = {data}")  # Remove after debugging
    result = step_one(data)
    LOG.debug(f"DEBUG: step_one = {result}")  # Temporary
    return result

# Remove later: grep -r "DEBUG:" . | grep LOG.debug
```

---

## Reproduction Strategies

### Creating Minimal Reproducible Examples

Strip away complexity until only bug remains.

```python
# Minimal reproduction test
def test_reproduce_bug():
    """Minimal case that triggers bug."""
    authenticate("test_123")  # Crashes here
```

### Reproduction Techniques

| Bug Type | Strategy |
|----------|----------|
| **Intermittent** | Loop 1000x, add delays |
| **Race condition** | Threading test, stress test |
| **Memory leak** | Process large dataset, monitor memory |
| **Environment-specific** | Capture env (Python, deps, OS) |
| **Timing-dependent** | Mock time.time() |

**For detailed reproduction scenarios:** See reference.md

---

## Common Error Patterns and Root Causes

### AttributeError on None

**Error:** `AttributeError: 'NoneType' object has no attribute 'x'`

**Root causes:**
1. Function returns None instead of raising exception
2. Optional chaining missing
3. Initialization failure silently returns None

**Debug:** Trace backward to where None introduced

### KeyError / IndexError

**Error:** `KeyError: 'missing_key'` or `IndexError: list index out of range`

**Root causes:**
1. Assuming key/index exists without validation
2. Off-by-one error
3. Empty list/dict passed unexpectedly

**Debug:**
```python
LOG.debug(f"Dict keys: {data.keys()}")
LOG.debug(f"List length: {len(items)}, accessing index {i}")
value = data.get('key', default)  # Use .get()
```

### ImportError / ModuleNotFoundError

**Error:** `ModuleNotFoundError: No module named 'foo'`

**Root causes:**
1. Virtual environment not activated
2. Package not installed
3. Circular imports
4. Wrong PYTHONPATH

**Debug:**
```bash
which python
python -c "import sys; print(sys.path)"
pip list | grep package
```

### Infinite Loop / Hang

**Error:** Process hangs, never completes

**Root causes:**
1. Loop condition never becomes false
2. Waiting for resource that never responds
3. Deadlock

**Debug:**
```python
max_iterations = 1000
for i in range(max_iterations):
    if i % 100 == 0:
        LOG.debug(f"Iteration {i}")
    if condition:
        break
else:
    raise TimeoutError(f"Loop exceeded {max_iterations}")
```

---

## Debugger vs Logging: When to Use What

| Situation | Use Debugger | Use Logging |
|-----------|--------------|-------------|
| **Development** | ✅ Interactive exploration | ✅ Permanent tracing |
| **Production** | ❌ Rarely (careful!) | ✅ Primary tool |
| **CI/CD** | ❌ Can't interact | ✅ Only option |
| **Intermittent bugs** | ❌ Hard to catch | ✅ Capture over time |
| **Complex state** | ✅ Inspect variables | ❌ Too verbose |
| **Call stack** | ✅ Navigate up/down | ❌ Manual tracing |
| **Quick fixes** | ✅ Immediate feedback | ❌ Slower iteration |

**Best practice:** Use both strategically
- **Debugger:** Understand complex state, explore unknowns
- **Logging:** Track behavior over time, production debugging

---

## Quick Reference Commands

### Python pdb

```python
breakpoint()                      # Set breakpoint (Python 3.7+)
import pdb; pdb.set_trace()      # Set breakpoint (older)
```

**During debugging:**
```
l          # List code
n          # Next line (step over)
s          # Step into function
c          # Continue
p var      # Print variable
w          # Stack trace
u/d        # Up/down stack
b file:N   # Breakpoint at line N
q          # Quit
```

### Logging Setup

```python
import logging
LOG = logging.getLogger(__name__)

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
```

### Git Bisect

```bash
git bisect start
git bisect bad                # Current broken
git bisect good v1.0.0       # v1.0.0 worked
# Test, then mark good/bad
git bisect reset             # Exit bisect
```

### Environment Debugging

```bash
python --version              # Check Python version
which python                  # Check Python path
pip list                      # List packages
env | grep -i python         # Check env vars
python -X dev script.py      # Run with warnings
```

---

## Remember

**The Golden Rules:**

1. **Trace backward to root cause** - Don't fix where error manifests, fix where bug originates
2. **Reproduce before fixing** - If you can't reproduce it consistently, you can't fix it reliably
3. **Binary search to isolate** - Divide and conquer to find exact failure point
4. **One bug at a time** - Fix, validate, move to next
5. **Evidence over assumptions** - Use debugger/logs to verify, don't guess

**Most common mistake:** Fixing symptoms instead of root cause. Always trace backward through the call stack.

**Debugging is 30-50% of development time** - invest in systematic approaches to debug efficiently.

---

**For detailed examples, advanced techniques, and production debugging patterns:** See reference.md
