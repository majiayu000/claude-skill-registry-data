---
name: test-suggester
description: Proactively suggests tests when code changes are detected. Activates when functions are created, logic is modified, security-sensitive code is added, or bug fixes are implemented. Provides non-intrusive test recommendations to help vibe coders ship with confidence.
---

# Test Suggester Skill

This skill proactively suggests tests for code changes, acting as a safety net for vibe coders who ship fast.

## When This Skill Activates

Claude will autonomously use this skill when:

### High Priority (Always Suggest)

1. **Security-Sensitive Code**
   - Authentication/authorization logic
   - Password handling or hashing
   - Token generation or validation
   - Input sanitization
   - Database queries with user input
   - File system operations with user paths

2. **New Public APIs**
   - Exported functions or classes
   - API route handlers
   - Public module interfaces
   - SDK methods

3. **Bug Fixes**
   - Regression test opportunity
   - Code that previously caused issues

4. **Error Handling Changes**
   - New try/catch blocks
   - Error recovery logic
   - Fallback implementations

### Medium Priority (Often Suggest)

1. **Business Logic**
   - Calculations and transformations
   - State management changes
   - Workflow modifications

2. **Data Operations**
   - Database queries
   - External API calls
   - Data validation

3. **Integration Points**
   - Service connections
   - Event handlers
   - Message processing

### Low Priority (Sometimes Suggest)

1. **Utility Functions**
   - Helper methods
   - Formatting functions
   - Constants

## When NOT to Suggest

Skip suggestions for:
- Minor formatting changes
- Comment updates only
- Import reorganization
- Type-only changes (no logic)
- Work in progress (incomplete code)
- Test file modifications
- Configuration files
- Documentation

## How to Suggest

Keep suggestions brief and non-intrusive:

### For High Priority Changes

```
💡 This security-sensitive change could use a test.

Run `/vibetap` to generate test suggestions, or `/vibetap-security` for security-focused tests.
```

### For Medium Priority Changes

```
💡 Consider adding a test for this logic. Run `/vibetap` when ready.
```

### For Bug Fixes

```
💡 Good opportunity for a regression test! Run `/vibetap` to generate one.
```

## Detection Patterns

### Security Patterns to Watch

```typescript
// Authentication - ALWAYS suggest
password, hash, salt, bcrypt, argon
authenticate, authorize, login, logout
token, jwt, session, cookie
```

```typescript
// Input handling - ALWAYS suggest
sanitize, validate, escape, encode
query, params, body, input
```

```typescript
// Sensitive operations - ALWAYS suggest
encrypt, decrypt, sign, verify
sql, query, exec, raw
fs.write, fs.read, path.join
```

### Logic Patterns to Watch

```typescript
// Business logic - OFTEN suggest
calculate, compute, process, transform
if/else with business conditions
switch statements on user data
```

```typescript
// Error handling - OFTEN suggest
try/catch blocks
.catch() handlers
throw new Error
```

## Suggestion Timing

- **Immediate**: After security-sensitive code is written
- **On completion**: When a function/method is finished
- **On save**: When the user saves a file with significant changes
- **On stage**: When the user stages files for commit

## Framework Detection

Suggest tests matching the project's framework:

| If found | Suggest using |
|----------|---------------|
| vitest.config | vitest |
| jest.config | jest |
| pytest.ini | pytest |
| Cargo.toml | cargo test |
| go.mod | go test |
| .rspec | rspec |

## Example Suggestions

### After Creating Auth Function

User writes:
```typescript
export async function validatePassword(plain: string, hash: string) {
  return bcrypt.compare(plain, hash);
}
```

Skill suggests:
```
💡 Security-critical: Password validation should have tests for:
   • Valid passwords
   • Invalid passwords
   • Timing attack resistance

Run `/vibetap-security` to generate security tests.
```

### After Adding Error Handling

User writes:
```typescript
try {
  await db.query(sql);
} catch (error) {
  logger.error('Query failed', error);
  throw new DatabaseError('Query failed');
}
```

Skill suggests:
```
💡 Error handling added - consider testing the failure path.

Run `/vibetap` to generate tests including error scenarios.
```

### After Bug Fix

User modifies:
```typescript
// Fixed: was using == instead of ===
if (user.role === 'admin') {
```

Skill suggests:
```
💡 Bug fix detected! A regression test would prevent this from recurring.

Run `/vibetap` to generate a test for this fix.
```

## Tips for Vibe Coders

- Tests are insurance, not bureaucracy
- Focus on what could break badly
- Security tests prevent embarrassing breaches
- Regression tests prevent re-fixing the same bug
- You don't need 100% coverage - focus on risk
