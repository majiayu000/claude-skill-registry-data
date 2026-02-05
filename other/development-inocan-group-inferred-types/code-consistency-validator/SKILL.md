---
name: code-consistency-validator
description: Validates type consistency across Rust, TypeScript, PostgreSQL boundaries. Use when reviewing code, debugging type mismatches, or validating API contracts. Triggers on: check consistency, validate types, find mismatches, cross-language.
---

# Code Consistency Validator

## Critical Type Mappings

| Rust | TypeScript | PostgreSQL |
|------|------------|------------|
| i64/u64 | bigint (not number!) | BIGINT |
| U256 | string | DECIMAL(36,18) |
| f64 | number | DOUBLE PRECISION |

## 🔴 CRITICAL Patterns
```typescript
Number(response.profit_wei)  // ❌ Precision loss!
parseInt(hexBalance)         // ❌ Missing radix!
JSON.stringify({ amount: BigInt(x) })  // ❌ Fails!
```

## Quick Grep
```bash
grep -rn "Number(" --include="*.ts" | grep -E "(wei|balance|amount)"
grep -rn "parseInt(" --include="*.ts" | grep -v ", 10)" | grep -v ", 16)"
```

## Report Format

🔴 CRITICAL (funds at risk)
🟠 WARNING (potential bugs)
🟡 INFO (style)
✅ VALIDATED
