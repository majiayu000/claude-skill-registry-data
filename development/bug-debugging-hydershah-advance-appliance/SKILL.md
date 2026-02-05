---
name: bug-debugging
description: Systematic bug debugging methodology, root cause analysis, and fix verification. Use when investigating and fixing bugs. (project)
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Bug Debugging Methodology

## Systematic Debugging Process

### 1. Reproduce the Bug
- Get exact steps to reproduce
- Note the environment (browser, OS, Node version)
- Identify if it's consistent or intermittent
- Document expected vs actual behavior

### 2. Gather Information
```bash
# Check logs
tail -f logs/app.log | grep -i error

# Check recent changes
git log --oneline -20
git diff HEAD~5

# Check environment
node --version
npm list --depth=0
```

### 3. Isolate the Problem

#### Binary Search Method
- If bug appeared recently, use `git bisect`
- Narrow down to specific commit
```bash
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>
```

#### Component Isolation
- Disable features one by one
- Add logging at key points
- Test with minimal reproduction case

### 4. Root Cause Analysis

#### Ask "5 Whys"
1. Why did the error occur?
2. Why was that state possible?
3. Why wasn't it validated?
4. Why wasn't it caught in tests?
5. Why wasn't it caught in review?

#### Common Bug Categories
| Category | Symptoms | Common Causes |
|----------|----------|---------------|
| Race Condition | Intermittent failures | Async timing, shared state |
| Memory Leak | Gradual slowdown | Unclosed connections, event listeners |
| Null Reference | Crash on access | Missing validation, async timing |
| Off-by-One | Wrong counts/indexes | Loop boundaries, array access |
| State Bug | Inconsistent UI/data | Stale state, mutation |

### 5. Debugging Tools

#### JavaScript/TypeScript
```javascript
// Strategic console logging
console.log('[DEBUG] Function entry:', { args, state });
console.trace('Call stack');
console.time('operation'); // ... console.timeEnd('operation');

// Debugger statement
debugger; // Pauses in DevTools

// Node.js debugging
// node --inspect-brk app.js
```

#### Database Debugging
```sql
-- Check recent queries
EXPLAIN ANALYZE SELECT ...;

-- Check locks
SELECT * FROM pg_locks;

-- Check connections
SELECT * FROM pg_stat_activity;
```

### 6. Fix Verification

#### Before Committing
- [ ] Bug is reproducible without fix
- [ ] Bug is not reproducible with fix
- [ ] No regression in related functionality
- [ ] Edge cases are handled
- [ ] Error messages are helpful

#### Test Coverage
```javascript
describe('Bug fix: #123', () => {
  it('should handle the edge case that caused the bug', () => {
    // Arrange: Set up the exact conditions
    // Act: Trigger the bug scenario
    // Assert: Verify correct behavior
  });
});
```

### 7. Documentation

#### Commit Message Format
```
fix: Brief description of the fix

Root cause: [Explain why the bug occurred]
Solution: [Explain what the fix does]

Fixes #123
```

## Common Debugging Patterns

### Async/Promise Issues
```javascript
// Add timeout to detect hanging promises
const withTimeout = (promise, ms) =>
  Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Timeout')), ms)
    )
  ]);
```

### State Debugging
```javascript
// Track state changes
const debugState = (label, state) => {
  console.log(`[${label}]`, JSON.stringify(state, null, 2));
  return state;
};
```

### Network Issues
```bash
# Check if service is reachable
curl -v http://localhost:3000/health

# Check DNS
nslookup api.example.com

# Check ports
netstat -tlnp | grep 3000
```

## Prevention Checklist

- [ ] Add regression test for the bug
- [ ] Consider if similar bugs exist elsewhere
- [ ] Update documentation if needed
- [ ] Add input validation if applicable
- [ ] Improve error messages
