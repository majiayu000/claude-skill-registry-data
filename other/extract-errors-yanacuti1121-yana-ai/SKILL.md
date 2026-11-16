---
name: extract-errors
description: Use when extracting, auditing, or standardizing error codes and messages across a codebase. Triggers on "error codes", "error messages", "unknown error", "extract errors", "error registry".
version: 1.4.20
compatibility: "Claude 4.5+, Sonnet 4.6, Haiku 4.5"
---

# Extract & Audit Error Codes

Cross-language skill for finding, cataloguing, and standardizing error codes and messages in any codebase.

## When to use

- "unknown error code" warning appears at runtime
- New error messages need codes assigned
- Error messages are inconsistent or duplicated across modules
- Building or auditing an error registry

## Instructions

### 1. Discover all error definitions

```bash
# JavaScript / TypeScript
grep -rn "throw new Error\|createError\|ErrorCode\.\|ERROR_" src/ --include="*.ts" --include="*.js"

# Python
grep -rn "raise \|class.*Error\|class.*Exception" . --include="*.py"

# Go
grep -rn "errors.New\|fmt.Errorf\|var Err" . --include="*.go"

# Rust
grep -rn "Err(\|thiserror\|anyhow" . --include="*.rs"
```

### 2. Check for unregistered errors

Compare discovered errors against the error registry file (e.g. `errors.json`, `error_codes.py`, `errors.go`).
Flag any error string not present in the registry.

### 3. Assign codes to new errors

- Use sequential numeric codes within the module's range (e.g. AUTH_001–AUTH_099)
- Format: `<MODULE>_<NNN>` (e.g. `GATE_001`, `HOOK_042`)
- Add to the registry with: code, message template, severity (info/warn/error/fatal), owner module

### 4. Report

Output a table:

| Code | Message | Module | Status |
|------|---------|--------|--------|
| GATE_001 | Identity verification failed | identity-gate | registered |
| HOOK_042 | Circuit breaker open | token-budget-guard | NEW — needs code |

### 5. Verify

Re-run discovery grep after updating the registry to confirm 0 unregistered errors remain.
