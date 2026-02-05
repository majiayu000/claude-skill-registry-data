---
name: debug
description: Debug code, analyze errors, interpret stack traces, find root causes, and suggest fixes. Use when troubleshooting bugs, analyzing crashes, or investigating unexpected behavior.
allowed-tools: Read, Grep, Bash, Glob
---

# Debug Skill

Comprehensive debugging assistance for finding and fixing bugs.

## 1. Stack Trace Analysis

**Python Stack Traces:**
```python
# Read and analyze Python tracebacks
# Look for:
# - File paths and line numbers
# - Exception types
# - Variable values
# - Call stack order

# Common patterns:
# - AttributeError: Check object types
# - KeyError: Check dictionary keys
# - IndexError: Check list bounds
# - TypeError: Check function arguments
# - ImportError: Check module installation
```

**JavaScript Stack Traces:**
```javascript
// Analyze JavaScript errors
// Look for:
// - Error type (TypeError, ReferenceError, etc.)
// - File and line numbers
// - Function call stack
// - Async operation context

// Common patterns:
// - "Cannot read property 'x' of undefined"
// - "x is not a function"
// - "Maximum call stack size exceeded"
```

## 2. Log Analysis

**Parse Application Logs:**
```bash
# Find errors in logs
grep -i "error\|exception\|fatal\|critical" logs/*.log

# Find warnings
grep -i "warn\|warning" logs/*.log

# Analyze by timestamp
grep "2026-01-22" logs/*.log | grep -i "error"

# Count error types
grep -i "error" logs/*.log | cut -d: -f2 | sort | uniq -c | sort -rn

# Find patterns before crashes
grep -B10 "fatal\|crash" logs/*.log
```

**Structured Log Analysis:**
```bash
# JSON logs
cat logs/app.log | jq 'select(.level == "error")'
cat logs/app.log | jq 'select(.statusCode >= 500)'

# Parse specific fields
cat logs/app.log | jq '.timestamp, .message, .error'

# Group by error type
cat logs/app.log | jq -r '.error.type' | sort | uniq -c | sort -rn
```

## 3. Common Bug Patterns

**Null/Undefined Issues:**
```bash
# Find potential null reference errors
grep -r "\..*\." . --include="*.js" --include="*.py"

# Check for null checks
grep -r "if.*is None\|if.*== None" . --include="*.py"
grep -r "if.*=== null\|if.*!== null" . --include="*.js"
```

**Race Conditions:**
```bash
# Find potential race conditions
grep -r "threading\|Thread\|async\|await" . --include="*.py" --include="*.js"

# Check for proper locking
grep -r "lock\|mutex\|semaphore" . --include="*.py" --include="*.js"

# Find shared state
grep -r "global\|shared\|static" . --include="*.py" --include="*.js"
```

**Memory Leaks:**
```bash
# Find potential memory leaks (Python)
grep -r "global\|cache" . --include="*.py"

# JavaScript event listeners without cleanup
grep -r "addEventListener" . --include="*.js" | grep -v "removeEventListener"

# Unclosed file handles
grep -r "open(" . --include="*.py" | grep -v "with\|close()"
```

**Off-by-One Errors:**
```bash
# Check loop boundaries
grep -r "range(.*len\|for.*in.*length" . --include="*.py" --include="*.js"

# Array access patterns
grep -r "\[.*-\s*1\]\|\[.*+\s*1\]" . --include="*.py" --include="*.js"
```

## 4. Debugging Techniques

**Add Debug Logging:**
```python
# Python debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

def problematic_function(arg):
    logging.debug(f"Input: {arg}, Type: {type(arg)}")
    # ... rest of function
    logging.debug(f"Output: {result}")
    return result
```

```javascript
// JavaScript debug logging
function problematicFunction(arg) {
    console.log('Input:', arg, 'Type:', typeof arg);
    console.trace('Call stack');
    // ... rest of function
    console.log('Output:', result);
    return result;
}
```

**Binary Search Debugging:**
```bash
# Comment out half the code to isolate the issue
# Use git bisect to find the commit that introduced the bug
git bisect start
git bisect bad  # Current commit is bad
git bisect good <commit-hash>  # Known good commit
# Test each commit until bug is found
git bisect reset
```

**Rubber Duck Debugging:**
```markdown
# Explain the code step by step:
1. What is the expected input?
2. What transformations happen?
3. What is the expected output?
4. Where does actual differ from expected?
```

## 5. Interactive Debugging

**Python Debugger (pdb):**
```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or Python 3.7+
breakpoint()

# pdb commands:
# n - next line
# s - step into
# c - continue
# p variable - print variable
# pp variable - pretty print
# l - list code
# w - where (stack trace)
# q - quit
```

**Node.js Debugger:**
```bash
# Start with debugger
node inspect app.js

# Or use Chrome DevTools
node --inspect app.js
node --inspect-brk app.js  # Break on first line

# Debugger commands:
# cont, c - Continue
# next, n - Next line
# step, s - Step in
# out, o - Step out
# watch('expr') - Watch expression
```

**Browser DevTools:**
```javascript
// Add breakpoint
debugger;

// Console debugging
console.log('Value:', value);
console.table(arrayOfObjects);
console.time('label');
// ... code ...
console.timeEnd('label');

// Conditional breakpoints in DevTools:
// Right-click line number > Add conditional breakpoint
// e.g., user.id === 123
```

## 6. Performance Debugging

**Find Performance Bottlenecks:**
```python
# Python profiling
import cProfile
import pstats

cProfile.run('slow_function()', 'output.prof')
stats = pstats.Stats('output.prof')
stats.sort_stats('cumulative')
stats.print_stats(20)

# Line profiler
# pip install line_profiler
@profile
def slow_function():
    # Code here
    pass

# Run: kernprof -l -v script.py
```

```javascript
// Node.js profiling
node --prof app.js
node --prof-process isolate-*.log

// Or use Chrome DevTools Performance tab
```

**Memory Profiling:**
```python
# Python memory profiler
from memory_profiler import profile

@profile
def memory_heavy_function():
    # Code here
    pass

# Run: python -m memory_profiler script.py
```

```bash
# Node.js memory profiling
node --inspect --expose-gc app.js
# Use Chrome DevTools Memory tab to take heap snapshots
```

## 7. Database Debugging

**SQL Query Debugging:**
```sql
-- Add EXPLAIN to understand query execution
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- Check for missing indexes
EXPLAIN ANALYZE SELECT ...;

-- Find slow queries
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```

**ORM Debugging:**
```python
# Django debug toolbar
# settings.py
DEBUG = True
INSTALLED_APPS += ['debug_toolbar']

# SQLAlchemy echo
engine = create_engine('sqlite:///db.db', echo=True)

# Sequelize logging
const sequelize = new Sequelize({
    logging: console.log
});
```

## 8. Network Debugging

**HTTP Request Debugging:**
```bash
# cURL with verbose output
curl -v https://api.example.com/endpoint

# Check DNS resolution
nslookup api.example.com
dig api.example.com

# Test connectivity
ping api.example.com
telnet api.example.com 443

# Trace route
traceroute api.example.com
```

**API Debugging:**
```bash
# Request/Response logging
curl -v -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"test"}'

# Check SSL/TLS
openssl s_client -connect api.example.com:443

# Monitor network traffic
tcpdump -i any port 443
```

## 9. Error Investigation Workflow

**Step 1: Reproduce the Error**
- Consistent reproduction steps
- Minimal test case
- Document environment (OS, versions, etc.)

**Step 2: Gather Information**
```bash
# System information
uname -a
python --version
node --version

# Environment variables
env | grep -i app

# Dependencies
pip list
npm list --depth=0

# Recent changes
git log --oneline -10
git diff HEAD~1
```

**Step 3: Isolate the Issue**
- Binary search through code
- Remove dependencies one by one
- Test with minimal configuration
- Check if issue exists in different environments

**Step 4: Analyze**
- Read stack traces carefully
- Check logs around the error time
- Review recent code changes
- Search for similar issues online

**Step 5: Form Hypothesis**
- What could cause this error?
- What are the assumptions?
- What can be tested?

**Step 6: Test Hypothesis**
- Add logging/debugging statements
- Create unit test that reproduces issue
- Test edge cases

**Step 7: Fix and Verify**
- Implement fix
- Verify fix resolves issue
- Add regression test
- Check for similar issues elsewhere

## 10. Common Debugging Commands

**Process Debugging:**
```bash
# Find running processes
ps aux | grep python
ps aux | grep node

# Check process details
top -p <pid>
htop -p <pid>

# Monitor system resources
vmstat 1
iostat -x 1

# Check open files
lsof -p <pid>

# Trace system calls
strace -p <pid>
strace -c python script.py  # Count syscalls
```

**Container Debugging:**
```bash
# Docker logs
docker logs <container-id>
docker logs -f <container-id>  # Follow

# Execute in container
docker exec -it <container-id> bash

# Inspect container
docker inspect <container-id>

# Container stats
docker stats <container-id>
```

## 11. Debugging Checklist

When debugging, verify:

- [ ] Can you reproduce the error consistently?
- [ ] Do you have the complete error message and stack trace?
- [ ] What are the exact steps to reproduce?
- [ ] When did it last work correctly?
- [ ] What changed since then?
- [ ] Does it work in a different environment?
- [ ] Are all dependencies up to date?
- [ ] Are there any relevant error logs?
- [ ] Have you checked for typos?
- [ ] Are variable types what you expect?
- [ ] Are boundary conditions handled?
- [ ] Is the data valid?

## When to Use This Skill

Use `/debug` when:
- Application crashes or throws errors
- Unexpected behavior occurs
- Performance issues need investigation
- Stack traces need interpretation
- Logs need analysis
- Root cause needs identification
- Debugging strategy needed
- Troubleshooting production issues

The skill will help analyze errors, suggest debugging approaches, and guide you to the root cause.
