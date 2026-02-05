---
name: root-cause-tracing
description: Systematic root cause analysis for debugging errors. Use when an error appears, something breaks unexpectedly, or you need to trace a problem back to its source. Prevents panic-driven debugging.
---

# Root Cause Tracing

## The Core Principle

**Trace backward through the call chain until you find the original trigger, then fix at the source.**

Do NOT fix symptoms. Find the root cause.

## The Protocol

### 1. STOP

When an error occurs:
- Do not make changes yet
- Do not guess at fixes
- Do not deploy anything

### 2. READ

Read the error carefully:
- What is the actual error message?
- Where does it occur (file, line, function)?
- What is the stack trace showing?

### 3. TRACE BACKWARD

Ask these questions in order:

```
1. What function threw the error?
2. What called that function?
3. What provided the bad input?
4. What changed since this last worked?
```

**The answer is usually in step 4.**

### 4. CHECK THE DIFF

```bash
# What changed recently?
git diff

# What changed in a specific file?
git diff path/to/file.py

# What changed since last known good state?
git log --oneline -10
git diff <commit>
```

### 5. ISOLATE

Once you identify the likely cause:
- Make ONE change to test your hypothesis
- Test locally before any deployment
- Verify the fix addresses the root cause, not just the symptom

## Decision Flow

```
Error Appears
     │
     ▼
Can you trace backward through the stack?
     │
     ├── YES → Trace to original trigger
     │              │
     │              ▼
     │         Fix at the source
     │
     └── NO (dead end) → Fix at symptom point
                              │
                              ▼
                         Add defense-in-depth
```

## Common Root Cause Patterns

### Configuration Changes

**Symptom**: "Connection refused" / "Authentication failed"
**Trace**: Check git diff for config file changes
**Example**: Removing `env_file=".env"` from pydantic settings breaks all credential loading

### Import Order / Dependencies

**Symptom**: "Module not found" / "Attribute error"
**Trace**: Check what imports changed, circular dependencies

### Environment Differences

**Symptom**: "Works locally, fails in production"
**Trace**: Compare env vars, check secrets, verify ports

### Data Shape Changes

**Symptom**: "KeyError" / "TypeError"
**Trace**: Check if API response format changed, verify source data

## Instrumentation (When Tracing Fails)

If you can't trace manually, add logging:

```python
import traceback

try:
    result = suspicious_function()
except Exception as e:
    print(f"Error: {e}")
    print(f"Traceback:\n{traceback.format_exc()}")
    raise
```

## The Anti-Patterns (Don't Do These)

### Panic Debugging
Making rapid changes without understanding the problem.
**Result**: Multiple new bugs, production spam, lost time.

### Symptom Fixing
Adding try/except around errors without understanding why they occur.
**Result**: Hidden bugs that resurface worse later.

### Conflation
Assuming two errors are related when they're not.
**Result**: "Fixing" one thing breaks another.

### Sunk Cost Fallacy
"I'm so close, one more fix will do it."
**Result**: 45 minutes of failed deployments.

## SignalRoom-Specific Traces

### Database Connection Errors

```
"password authentication failed"
     │
     ▼
Check SUPABASE_DB_USER format
     │
     ▼
Must be: postgres.{project_ref} (not just "postgres")
     │
     ▼
Check port: 6543 for pooler, 5432 for direct
```

### Temporal Activity Failures

```
"Activity failed: <error>"
     │
     ▼
Check activity logs (fly logs or make logs-worker)
     │
     ▼
Look at activity input in Temporal UI
     │
     ▼
Run the underlying function locally to reproduce
```

### Pipeline Load Failures

```
"Pipeline execution failed at step=sync"
     │
     ▼
Check _dlt_loads table for partial loads
     │
     ▼
Check source data format (API changed?)
     │
     ▼
Run pipeline locally with --dry-run
```

## Remember

> "What was working before, and what did I change?"

The answer is always in the git diff.
