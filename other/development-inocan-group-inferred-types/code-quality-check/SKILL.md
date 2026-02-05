---
name: code-quality-check
description: Automated code quality verification checklist
trigger: auto
---

# Code Quality Check

Run this checklist before committing code:

## 1. SOLID Principles
```
[S] Single Responsibility - Each class/function does ONE thing
[O] Open/Closed - Extend without modifying
[L] Liskov Substitution - Subtypes are substitutable
[I] Interface Segregation - Small, focused interfaces
[D] Dependency Inversion - Depend on abstractions
```

## 2. Clean Code Rules
```
✓ Names reveal intent
✓ Functions < 20 lines
✓ Max 3 parameters (use objects if more)
✓ No magic numbers/strings
✓ DRY - No duplication
✓ Comments explain WHY not WHAT
```

## 3. Error Handling
```
✓ All errors caught and handled
✓ No silent failures
✓ Meaningful error messages
✓ Proper logging
✓ Cleanup in finally blocks
```

## 4. Performance
```
✓ No N+1 queries
✓ Proper indexing
✓ Caching where appropriate
✓ Lazy loading for heavy ops
✓ No memory leaks
```

## 5. Security
```
✓ Input validated
✓ Output sanitized
✓ No SQL injection vectors
✓ No XSS vulnerabilities
✓ Secrets in env vars
✓ Dependencies updated
```

## 6. Testing
```
✓ Unit tests written
✓ Edge cases covered
✓ Mocks used for external deps
✓ Tests are fast (< 1s each)
✓ Coverage > 80%
```

## 7. Documentation
```
✓ Public APIs documented
✓ Complex logic explained
✓ README updated
✓ Examples provided
```

## Quick Scan (30 seconds)
```bash
# Run before commit:
1. grep -r "TODO\|FIXME\|XXX\|HACK" .
2. Check for console.log / print statements
3. Verify no commented-out code blocks
4. Check for hardcoded credentials
5. Run linter
6. Run tests
```

## Token-Efficient Usage
- Use as final validation, not during writing
- Catch issues before review (saves back-and-forth)
- Automate what you can (linters, formatters)
