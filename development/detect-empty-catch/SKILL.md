---
name: detect-empty-catch
description: Detect empty catch blocks and exception swallowing anti-patterns. Finds catch blocks that silently ignore errors without logging or rethrowing. Works across all languages. Use when user asks about error handling issues.
allowed-tools: mcp__miller__fast_search, mcp__miller__get_symbols, Read
---

# Empty Catch / Exception Swallowing Detection

## Activation Announcement

**IMPORTANT**: When this skill activates, ALWAYS start your response with:

```
🚨 **Exception Handling Scan**
Scanning for empty catch blocks and swallowed exceptions...
```

This provides a visual indicator to the user that systematic detection is running.

## What's the Problem?

Empty catch blocks and swallowed exceptions hide errors, making debugging extremely difficult:

```csharp
try {
    ProcessPayment();
} catch (Exception) {
    // Silent failure - payment may have failed but app continues
}
```

## Detection Strategy

### Phase 1: Semantic Search for Exception Handling Issues

```
fast_search("catch empty exception ignore", method="semantic", limit=30)
fast_search("catch block no logging no rethrow", method="semantic", limit=30)
fast_search("try catch swallow error silent", method="semantic", limit=30)
fast_search("exception handler empty body", method="semantic", limit=30)
```

### Phase 2: Pattern Search for Language-Specific Idioms

```
# C# patterns
fast_search("catch Exception { }", method="text", limit=20)
fast_search("catch { }", method="text", limit=20)

# TypeScript/JavaScript patterns
fast_search("catch error { }", method="text", limit=20)
fast_search("catch (e) { }", method="text", limit=20)
fast_search(".catch(() =>", method="text", limit=20)

# Python patterns
fast_search("except: pass", method="text", limit=20)
fast_search("except Exception: pass", method="text", limit=20)
fast_search("except BaseException:", method="text", limit=20)

# Java patterns
fast_search("catch (Exception e) { }", method="text", limit=20)
fast_search("catch (Throwable", method="text", limit=20)

# Go patterns (error ignoring)
fast_search("_ = err", method="text", limit=20)
fast_search(", _ := ", method="text", limit=20)
```

### Phase 3: Inspect Suspicious Catches

For each finding:

```
get_symbols(file_path="<file>", target="<function>", mode="full")
```

Check if the catch block:
1. Has an empty body or only comments
2. Catches too broadly (Exception, Throwable, BaseException)
3. Missing logging statement
4. Missing rethrow or error propagation

## Output Format

**IMPORTANT**: Always present findings in this structured format:

```
## Exception Handling Scan Results

### Summary
- Files scanned: X
- Empty/swallowed catches found: Y
- Severity breakdown: Critical: A, Warning: B, Info: C

### Findings

#### 1. [CRITICAL] src/payment/processor.ts:87
**Issue**: Empty catch block in payment processing
**Code**:
```typescript
try {
    await chargeCard(amount);
} catch (e) {
    // TODO: handle this
}
```
**Risk**: Payment failures silently ignored - money issues!
**Fix**: Log error and notify, or rethrow with context

#### 2. [WARNING] src/utils/parser.cs:142
**Issue**: Catches base Exception class
**Code**:
```csharp
catch (Exception ex) {
    return null;
}
```
**Risk**: Hides all errors including critical ones
**Fix**: Catch specific exceptions, log others

#### 3. [INFO] src/cache/redis.py:56
**Issue**: Broad except with pass
**Code**:
```python
except Exception:
    pass  # Cache miss is OK
```
**Risk**: May hide connection errors, not just misses
**Fix**: Catch specific CacheMissError, log unexpected errors

### Recommendations
1. Never leave catch blocks empty
2. Always log exceptions with context
3. Catch specific exceptions, not base types
4. Consider: log + rethrow vs log + handle vs propagate
```

## Severity Classification

### CRITICAL (Must Fix)
- Empty catch in payment/financial code
- Empty catch in authentication/authorization
- Empty catch in data persistence operations
- Catching and ignoring all exceptions in critical paths

### WARNING (Should Fix)
- Empty catch with TODO comment (forgotten)
- Catching base Exception/Throwable class
- Catch that returns null/default without logging
- Generic error handler that swallows details

### INFO (Review)
- Empty catch with explanatory comment (intentional)
- Catch in test/mock code
- Catch in cleanup/finally paths
- Cache miss handlers (may be intentional)

## Language-Specific Patterns

| Language | Empty Catch Pattern | Too-Broad Catch |
|----------|--------------------|-----------------|
| C# | `catch { }` or `catch (Exception) { }` | `catch (Exception)` without filter |
| TypeScript | `catch (e) { }` or `.catch(() => {})` | `catch (e: any)` |
| Python | `except: pass` or `except Exception: pass` | `except BaseException` |
| Java | `catch (Exception e) { }` | `catch (Throwable)` |
| Go | `if err != nil { }` or `_ = err` | Ignoring specific error types |
| Rust | `let _ = result;` or `.ok()` | Discarding Result without handling |

## Context Matters

Some empty catches are intentional:

```python
# Acceptable: Cleanup that shouldn't fail the main operation
try:
    temp_file.delete()
except OSError:
    pass  # Best effort cleanup, don't fail if already deleted
```

When reviewing findings, consider:
- Is this a critical code path or cleanup?
- Is the comment explaining WHY it's empty?
- Would a failure here cause data corruption or security issues?

## Success Criteria

This skill succeeds when:
- Clear visual announcement at start
- All catch patterns searched across languages
- Findings categorized by severity
- Context considered (not all empty catches are bugs)
- Actionable recommendations provided
