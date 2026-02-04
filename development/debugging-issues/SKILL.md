---
name: Debugging Issues
description: Systematically debug issues with reproduction steps, error analysis, hypothesis testing, and root cause fixes. Use when investigating bugs, analyzing production incidents, or troubleshooting unexpected behavior.
---

# Debugging Issues

## Purpose
Provides systematic approaches to debugging, troubleshooting techniques, and error analysis strategies.

## When to Use
- Investigating bugs or unexpected behavior
- Analyzing error messages and stack traces
- Troubleshooting system issues
- Performance debugging
- Root cause analysis
- Production incident response

## Systematic Debugging Process

### 1. Reproduce the Issue
**Goal**: Create a consistent way to trigger the bug

**Steps:**
- [ ] Document exact steps to reproduce
- [ ] Identify required preconditions
- [ ] Note the environment (OS, browser, versions)
- [ ] Create minimal reproduction case
- [ ] Verify it reproduces consistently

**Example:**
```yaml
reproduction_steps:
  - action: "Login as admin user"
  - action: "Navigate to /dashboard"
  - action: "Click 'Export Data' button"
  - expected: "CSV file downloads"
  - actual: "Error 500 appears"
  - frequency: "Occurs every time"
```

### 2. Isolate the Problem
**Goal**: Narrow down where the issue occurs

**Techniques:**
```yaml
isolation_methods:
  Divide and Conquer:
    description: "Split system in half, test which half has issue"
    example: "Comment out half the code, see if error persists"

  Binary Search:
    description: "Use git bisect or similar to find breaking commit"
    command: "git bisect start && git bisect bad && git bisect good v1.0"

  Component Isolation:
    description: "Test each component individually"
    example: "Test database, API, frontend separately"

  Environment Comparison:
    description: "Compare working vs broken environments"
    checklist:
      - Different OS?
      - Different versions?
      - Different configurations?
      - Different data?
```

### 3. Analyze Logs and Errors
**Goal**: Gather evidence about what's going wrong

**Log Analysis:**
```yaml
log_analysis:
  error_messages:
    - Read the full error message
    - Note the error type/code
    - Identify the failing component

  stack_traces:
    - Start from the bottom (root cause)
    - Identify the first non-library code
    - Check function arguments at that point

  correlation:
    - Check logs before the error
    - Look for patterns
    - Correlate with user actions
    - Check timestamps
```

**Common Error Patterns:**
```python
# NullPointerException / AttributeError
# Usually: Accessing property of None/null object
# Fix: Add null checks or ensure object is initialized

# IndexError / ArrayIndexOutOfBoundsException
# Usually: Accessing array index that doesn't exist
# Fix: Check array length before accessing

# KeyError / Property not found
# Usually: Accessing dict/object key that doesn't exist
# Fix: Use .get() with default or check if key exists

# TypeError / Type mismatch
# Usually: Wrong type passed to function
# Fix: Validate types, add type hints

# ConnectionError / Timeout
# Usually: Network issues or service down
# Fix: Add retry logic, check service health
```

### 4. Form Hypothesis
**Goal**: Develop theory about what's causing the issue

**Hypothesis Framework:**
```yaml
hypothesis_template:
  observation: "What did you observe?"
  theory: "What do you think is causing it?"
  prediction: "If theory is correct, what else would be true?"
  test: "How can you test this?"

example:
  observation: "API returns 500 error on POST /users"
  theory: "Input validation is rejecting valid email format"
  prediction: "If true, different email format should work"
  test: "Try with various email formats"
```

### 5. Test the Hypothesis
**Goal**: Verify or disprove your theory

**Testing Approaches:**
```yaml
testing_methods:
  Add Logging:
    description: "Add detailed logs around suspected area"
    example: |
      logger.debug(f"Input data: {data}")
      logger.debug(f"Validation result: {is_valid}")

  Add Breakpoints:
    description: "Pause execution to inspect state"
    tools:
      - "pdb for Python"
      - "debugger for JavaScript"
      - "gdb for C/C++"

  Change One Thing:
    description: "Modify one variable at a time"
    example: "Change input value, run again, observe result"

  Write Failing Test:
    description: "Create test that reproduces the bug"
    benefit: "Ensures fix works and prevents regression"
```

### 6. Implement Fix
**Goal**: Resolve the root cause

**Fix Strategies:**
```yaml
fix_approaches:
  Quick Fix:
    when: "Production is down"
    approach: "Minimal change to restore service"
    followup: "Proper fix later"

  Root Cause Fix:
    when: "Have time to do it right"
    approach: "Fix underlying cause"
    benefit: "Prevents similar bugs"

  Workaround:
    when: "Fix is complex, need temporary solution"
    approach: "Add special handling"
    document: "Explain why workaround exists"
```

### 7. Verify the Fix
**Goal**: Ensure the issue is resolved

**Verification Checklist:**
- [ ] Original bug is fixed
- [ ] No new bugs introduced
- [ ] All tests pass
- [ ] Edge cases handled
- [ ] Code reviewed
- [ ] Deployed to test environment
- [ ] Tested in production-like environment

## Debugging Techniques

### Print Debugging
```python
# Simple but effective
def calculate_total(items):
    print(f"DEBUG: items = {items}")
    total = sum(item.price for item in items)
    print(f"DEBUG: total = {total}")
    return total
```

### Interactive Debugging
```python
# Python pdb
import pdb; pdb.set_trace()

# Common commands:
# n (next) - Execute next line
# s (step) - Step into function
# c (continue) - Continue execution
# p variable - Print variable
# l (list) - Show code context
# q (quit) - Exit debugger
```

### Rubber Duck Debugging
```yaml
rubber_duck_method:
  step_1: "Get a rubber duck (or patient colleague)"
  step_2: "Explain your code line by line"
  step_3: "Explain what you expect to happen"
  step_4: "Explain what actually happens"
  step_5: "Often you'll realize the issue while explaining"
```

### Binary Search Debugging
```bash
# Find which commit introduced a bug
git bisect start
git bisect bad  # Current commit is bad
git bisect good v1.0  # v1.0 was working

# Git will checkout commits for you to test
# After each test, mark as good or bad:
git bisect good  # if works
git bisect bad   # if broken

# Git will find the problematic commit
```

### Adding Instrumentation
```python
# Add metrics to understand behavior
import time
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper

@timing_decorator
def slow_function():
    # Your code here
    pass
```

## Common Debugging Scenarios

### Performance Issues
```yaml
performance_debugging:
  profile_the_code:
    python: "python -m cProfile script.py"
    node: "node --prof script.js"

  identify_bottlenecks:
    - Look for functions called many times
    - Check for slow database queries
    - Identify memory allocations

  optimize:
    - Cache repeated calculations
    - Use more efficient algorithms
    - Add database indexes
    - Implement pagination
```

### Memory Leaks
```yaml
memory_leak_debugging:
  detect:
    - Monitor memory usage over time
    - Look for steadily increasing memory
    - Check for unclosed resources

  common_causes:
    - Unclosed file handles
    - Unclosed database connections
    - Event listeners not removed
    - Circular references
    - Large objects not garbage collected

  fix:
    - Use context managers (with statement)
    - Explicitly close connections
    - Remove event listeners
    - Break circular references
```

### Race Conditions
```yaml
race_condition_debugging:
  symptoms:
    - Intermittent failures
    - Harder to reproduce
    - Timing-dependent

  detection:
    - Add logging with timestamps
    - Use thread/process IDs in logs
    - Add artificial delays to expose timing issues

  solutions:
    - Add proper locking (mutex, semaphore)
    - Use atomic operations
    - Redesign to avoid shared state
    - Use message queues
```

### Database Issues
```yaml
database_debugging:
  slow_queries:
    identify: "EXPLAIN ANALYZE query"
    solutions:
      - Add indexes
      - Optimize joins
      - Reduce data fetched
      - Use connection pooling

  deadlocks:
    detect: "Check database logs for deadlock errors"
    prevent:
      - Acquire locks in consistent order
      - Keep transactions short
      - Use appropriate isolation levels

  connection_issues:
    symptoms: "Connection refused, timeout errors"
    check:
      - Database is running
      - Connection string correct
      - Firewall/network allows connection
      - Connection pool not exhausted
```

## Error Analysis Patterns

### Stack Trace Reading
```python
# Example stack trace
Traceback (most recent call last):
  File "app.py", line 45, in main
    process_user(user_data)
  File "services.py", line 23, in process_user
    validate_email(user_data['email'])
  File "validators.py", line 12, in validate_email
    if '@' not in email:
TypeError: argument of type 'NoneType' is not iterable

# Analysis:
# 1. Error: TypeError at line 12 in validators.py
# 2. Cause: 'email' variable is None
# 3. Origin: Likely user_data['email'] is None from services.py line 23
# 4. Fix: Add None check before validation
```

### Error Messages Interpretation
```yaml
error_interpretation:
  "Connection refused":
    likely_causes:
      - Service not running
      - Wrong port
      - Firewall blocking

  "Permission denied":
    likely_causes:
      - Insufficient file permissions
      - User lacks required role
      - Protected resource

  "Resource not found":
    likely_causes:
      - Typo in path/URL
      - Resource deleted
      - Wrong environment

  "Timeout":
    likely_causes:
      - Service too slow
      - Network issues
      - Infinite loop
      - Deadlock
```

## Debugging Checklist

### Before Starting
- [ ] Can you reproduce the issue?
- [ ] Do you have access to logs?
- [ ] Do you have a test environment?
- [ ] Is there a recent change that might have caused it?

### During Debugging
- [ ] Have you isolated the problem area?
- [ ] Have you checked the logs?
- [ ] Have you formed a hypothesis?
- [ ] Have you tested your hypothesis?
- [ ] Are you changing one thing at a time?

### Before Closing
- [ ] Is the original issue fixed?
- [ ] Have you written a test for this bug?
- [ ] Have you checked for similar bugs?
- [ ] Have you documented the root cause?
- [ ] Have you shared knowledge with the team?

## Production Debugging

### Safe Debugging in Production
```yaml
production_debugging:
  do:
    - Add detailed logging
    - Monitor metrics
    - Use feature flags to isolate issues
    - Take snapshots/backups before changes
    - Have rollback plan ready

  dont:
    - Don't use debugger breakpoints (freezes service)
    - Don't make changes without review
    - Don't restart services unnecessarily
    - Don't expose sensitive data in logs
```

### Incident Response
```yaml
incident_response:
  immediate:
    - Assess severity
    - Notify stakeholders
    - Start incident log
    - Begin mitigation

  mitigation:
    - Restore service (rollback if needed)
    - Implement workaround
    - Monitor closely

  resolution:
    - Identify root cause
    - Implement proper fix
    - Test thoroughly
    - Deploy fix

  followup:
    - Write postmortem
    - Update runbooks
    - Add monitoring/alerts
    - Share learnings
```

## Tools and Resources

### Debugging Tools
```yaml
tools_by_language:
  python:
    - "pdb - Interactive debugger"
    - "ipdb - Enhanced pdb"
    - "memory_profiler - Memory profiling"
    - "cProfile - Performance profiling"

  javascript:
    - "Chrome DevTools"
    - "Node.js debugger"
    - "VS Code debugger"

  general:
    - "Git bisect - Find breaking commit"
    - "curl - Test APIs"
    - "tcpdump - Network debugging"
    - "strace/dtrace - System call tracing"
```

---
*Use this skill when debugging issues or conducting root cause analysis*
