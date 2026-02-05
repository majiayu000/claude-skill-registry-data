---
name: debug-issues
description: Debug bugs and errors using intel-first approach with systematic root cause analysis. Use proactively when errors occur, tests fail, or unexpected behavior appears. MUST trace from symptom to root cause with CoD^Σ reasoning.
---

# Debugging Skill

## Overview

This skill performs systematic bug diagnosis using intelligence-first approach to trace from symptom to root cause with complete CoD^Σ reasoning chain.

**Core principle:** Capture symptom → Parse error → Intel trace → Root cause → Propose fix

**Announce at start:** "I'm using the debug-issues skill to diagnose this problem."

## Quick Reference

| Phase | Key Activities | Output |
|-------|---------------|--------|
| **1. Capture Symptom** | Reproduction steps, error message, environment | Symptom description |
| **2. Parse Error** | Extract error type, file:line, stack trace | Parsed error object |
| **3. Intel Trace** | project-intel.mjs queries from error to cause | Intel evidence chain |
| **4. Root Cause** | Identify specific file:line with CoD^Σ trace | Root cause |
| **5. Report** | Generate bug report with fix proposal | bug-report.md |

## Templates You Will Use

- **@.claude/templates/bug-report.md** - Complete bug report with fix (Phase 5)
- **@.claude/templates/mcp-query.md** - For verifying library behavior (Phase 4)

## Intelligence Tool Guide

- **@.claude/shared-imports/project-intel-mjs-guide.md** - For systematic intel queries

## The Process

Copy this checklist to track progress:

```
Debugging Progress:
- [ ] Phase 1: Symptom Captured (reproduction steps documented)
- [ ] Phase 2: Error Parsed (file:line extracted)
- [ ] Phase 3: Intel Trace Complete (queries executed)
- [ ] Phase 4: Root Cause Identified (specific file:line)
- [ ] Phase 5: Bug Report Generated (with fix proposal)
```

### Phase 1: Capture Symptom

Document the complete symptom:

1. **Error Message:**
   ```
   TypeError: Cannot read property 'discount' of undefined
   at calculateTotal (src/pricing/calculator.ts:67)
   at processCheckout (src/checkout/checkout.ts:123)
   ```

2. **Reproduction Steps:**
   ```
   1. Add items to cart
   2. Apply discount code "SAVE20"
   3. Click "Checkout"
   4. ERROR: 500 response
   ```

3. **Frequency & Environment:**
   ```
   - Frequency: 15% of checkout attempts
   - Environment: Production
   - User impact: High (blocks checkout)
   ```

**Enforcement:**
- [ ] Complete error message captured
- [ ] Reproduction steps documented
- [ ] Frequency and environment noted

### Phase 2: Parse Error

Extract structured information from error:

#### Parse Stack Trace

```
ERROR: TypeError: Cannot read property 'discount' of undefined
  at calculateTotal (src/pricing/calculator.ts:67)  ← ROOT ERROR
  at processCheckout (src/checkout/checkout.ts:123)
  at POST /api/checkout (src/api/routes.ts:45)

Parsed:
{
  error_type: "TypeError",
  message: "Cannot read property 'discount' of undefined",
  root_location: "src/pricing/calculator.ts:67",
  root_function: "calculateTotal",
  call_chain: [
    "src/api/routes.ts:45",
    "src/checkout/checkout.ts:123",
    "src/pricing/calculator.ts:67"
  ]
}
```

#### Identify Entry Point

```
Entry point: src/pricing/calculator.ts:67
Function: calculateTotal
Issue: Accessing .discount on undefined object
```

**Enforcement:**
- [ ] Error type identified
- [ ] Root file:line extracted
- [ ] Function name identified
- [ ] Call chain documented

### Phase 3: Intel Trace

Use project-intel.mjs to trace from error to cause.

#### Query 1: Locate Function

```bash
project-intel.mjs --search "calculateTotal" --type ts --json > /tmp/debug_search.json
```

**Result:**
```json
{
  "files": [
    "src/pricing/calculator.ts",
    "src/pricing/calculator.test.ts"
  ]
}
```

#### Query 2: Analyze Symbols

```bash
project-intel.mjs --symbols src/pricing/calculator.ts --json > /tmp/debug_symbols.json
```

**Result:**
```json
{
  "symbols": [
    {"name": "calculateTotal", "line": 62, "type": "function"},
    {"name": "applyDiscount", "line": 89, "type": "function"},
    {"name": "getDiscount", "line": 105, "type": "function"}
  ]
}
```

**Key Finding:** calculateTotal is at line 62, error at line 67 (5 lines into function)

#### Query 3: Trace Dependencies

```bash
# What does calculateTotal import?
project-intel.mjs --dependencies src/pricing/calculator.ts --direction upstream --json
```

**Result:**
```json
{
  "imports": [
    {"module": "./discountService", "symbols": ["getDiscount"]},
    {"module": "../models/Cart", "symbols": ["Cart"]},
    {"module": "../utils/currency", "symbols": ["formatPrice"]}
  ]
}
```

**Key Finding:** Imports getDiscount from discountService - likely source of undefined

#### Query 4: Check getDiscount Function

```bash
project-intel.mjs --symbols src/pricing/discountService.ts --json
```

**Result:**
```json
{
  "symbols": [
    {"name": "getDiscount", "line": 12, "type": "function", "returns": "Discount | undefined"}
  ]
}
```

**CRITICAL FINDING:** getDiscount returns `Discount | undefined` - can be undefined!

**Enforcement:**
- [ ] All relevant files identified
- [ ] Symbol locations found
- [ ] Dependencies traced
- [ ] Return types checked

### Phase 4: Identify Root Cause

Now read ONLY the relevant lines identified by intel:

#### Targeted Read 1: Error Location

```bash
sed -n '62,75p' src/pricing/calculator.ts
```

**Code:**
```typescript
// Line 62
export function calculateTotal(cart: Cart, discountCode?: string): number {
  const subtotal = cart.items.reduce((sum, item) => sum + item.price * item.quantity, 0)

  // Line 67 - ERROR LINE
  const discountAmount = discountCode
    ? getDiscount(discountCode).discount * subtotal  // ← BUG: no null check
    : 0

  const total = subtotal - discountAmount
  return formatPrice(total)
}
```

#### Targeted Read 2: getDiscount Function

```bash
sed -n '12,25p' src/pricing/discountService.ts
```

**Code:**
```typescript
// Line 12
export function getDiscount(code: string): Discount | undefined {
  const discount = discounts.find(d => d.code === code && d.active)
  return discount  // ← Returns undefined when code not found
}
```

#### Root Cause Analysis (CoD^Σ)

```markdown
**Claim:** Error occurs because calculateTotal doesn't handle undefined from getDiscount

**Complete CoD^Σ Trace:**
```
Step 1: → ParseError
  ↳ Source: Error log
  ↳ Data: TypeError at src/pricing/calculator.ts:67

Step 2: ⇄ IntelQuery("locate calculateTotal")
  ↳ Query: project-intel.mjs --search "calculateTotal"
  ↳ Data: Found in src/pricing/calculator.ts at line 62

Step 3: ⇄ IntelQuery("analyze symbols")
  ↳ Query: project-intel.mjs --symbols calculator.ts
  ↳ Data: calculateTotal at line 62, error at line 67 (5 lines in)

Step 4: → TargetedRead(lines 62-75)
  ↳ Source: sed -n '62,75p' calculator.ts
  ↳ Data: Line 67 calls getDiscount(code).discount without null check

Step 5: ⇄ IntelQuery("check getDiscount")
  ↳ Query: project-intel.mjs --symbols discountService.ts
  ↳ Data: getDiscount returns Discount | undefined

Step 6: → TargetedRead(getDiscount function)
  ↳ Source: sed -n '12,25p' discountService.ts
  ↳ Data: Returns undefined when code not found/inactive

Step 7: ⊕ MCPVerify("TypeScript best practices")
  ↳ Tool: Ref MCP
  ↳ Query: "TypeScript optional chaining undefined handling"
  ↳ Data: Use ?. operator for potentially undefined values

Step 8: ∘ Conclusion
  ↳ Logic: getDiscount returns undefined → accessing .discount throws TypeError
  ↳ Root Cause: src/pricing/calculator.ts:67 - missing null check
  ↳ Fix: Use optional chaining: getDiscount(code)?.discount ?? 0
```
```

**Token Comparison:**
- Reading full files: ~8600 tokens
- Intel + targeted reads: ~750 tokens
- **Savings: 91%**

**Enforcement:**
- [ ] Root cause identified with specific file:line
- [ ] Complete CoD^Σ trace documented
- [ ] MCP verification performed
- [ ] Fix approach validated

### Phase 5: Generate Bug Report

Use **@.claude/templates/bug-report.md** to create comprehensive report:

```markdown
---
bug_id: "checkout-discount-500"
severity: "critical"
status: "open"
assigned_to: "executor-agent"
---

# Bug Report: 500 Error on Checkout with Discount

## Symptom
[Full symptom from Phase 1]

## CoD^Σ Trace
[Complete trace from Phase 4]

## Root Cause
**Location:** src/pricing/calculator.ts:67

**Issue:** Missing null check before accessing .discount property

**Why It Fails:**
- getDiscount() returns Discount | undefined
- When discount code invalid/inactive, returns undefined
- Code attempts undefined.discount → TypeError

## Fix Specification
**Approach:** Add optional chaining

**Changes Required:**
```typescript
// Before (buggy)
const discountAmount = discountCode
  ? getDiscount(discountCode).discount * subtotal
  : 0

// After (fixed)
const discountAmount = discountCode
  ? (getDiscount(discountCode)?.discount ?? 0) * subtotal
  : 0
```

**Reason:**
- Optional chaining (?.) returns undefined if getDiscount returns undefined
- Nullish coalescing (?? 0) provides default value
- No TypeError, discount defaults to 0 for invalid codes

## Verification
**Test Plan:**
```typescript
it('handles invalid discount codes gracefully', () => {
  const cart = { items: [{ price: 100, quantity: 1 }] }
  const total = calculateTotal(cart, 'INVALID_CODE')
  expect(total).toBe(100) // No discount applied, no error
})
```

**Acceptance Criteria:**
- [ ] Invalid discount codes return subtotal (no discount)
- [ ] Valid discount codes still apply correctly
- [ ] No TypeError thrown
```

**File Naming:** `YYYYMMDD-HHMM-bug-<id>.md`

**Enforcement:**
- [ ] Bug report uses template
- [ ] CoD^Σ trace complete
- [ ] Root cause with file:line specified
- [ ] Fix proposal provided
- [ ] Verification plan included

## Common Error Patterns

### Pattern 1: React Infinite Re-render

**Symptom:**
```
Warning: Maximum update depth exceeded
Component: LoginForm
```

**Debugging Process:**
```
1. Search for component: project-intel.mjs --search "LoginForm" --type tsx
2. Analyze symbols: Find useEffect hooks
3. Targeted read: Check dependency arrays
4. Common cause: useEffect depends on value it mutates
5. MCP verify: Ref MCP "React useEffect dependencies"
6. Fix: Remove mutated value from dependencies or use functional setState
```

### Pattern 2: N+1 Query Problem

**Symptom:**
```
Slow page load (10+ seconds)
Dashboard with 100 users
```

**Debugging Process:**
```
1. Search for data fetch: project-intel.mjs --search "fetchUsers"
2. Analyze code: Look for loops around database queries
3. Common pattern:
   users.forEach(user => {
     const posts = await db.query("SELECT * FROM posts WHERE user_id = ?", user.id)
   })  // ← Query inside loop!
4. Fix: Single query with JOIN or WHERE IN clause
```

### Pattern 3: Memory Leak

**Symptom:**
```
Browser tab memory grows over time
Eventually crashes
```

**Debugging Process:**
```
1. Search for event listeners: project-intel.mjs --search "addEventListener"
2. Check useEffect cleanup: Look for return functions
3. Common issue: Missing cleanup
4. MCP verify: Ref MCP "React useEffect cleanup"
5. Fix: Add cleanup function:
   useEffect(() => {
     window.addEventListener('resize', handler)
     return () => window.removeEventListener('resize', handler)  // ← Cleanup
   }, [])
```

## Enforcement Rules

### Rule 1: Complete CoD^Σ Trace

**❌ Violation:**
```
The bug is in the discount calculation.
```

**✓ Correct:**
```
Root cause: src/pricing/calculator.ts:67

CoD^Σ Trace:
Step 1: ParseError → TypeError at line 67
Step 2: IntelQuery → getDiscount returns undefined
Step 3: MCPVerify → TypeScript docs confirm optional chaining needed
Step 4: Conclusion → Missing null check causes error
```

### Rule 2: Intel Before Reading

**❌ Violation:**
```bash
# Read entire codebase looking for bug
cat src/**/*.ts  # Thousands of lines
```

**✓ Correct:**
```bash
# Intel-first approach
project-intel.mjs --search "calculateTotal"  # Find exact file
project-intel.mjs --symbols calculator.ts    # Find exact line
sed -n '62,75p' calculator.ts                # Read only relevant lines
```

### Rule 3: Propose Fix with Verification

**❌ Violation:**
```
Fix: Change the code to handle undefined.
```

**✓ Correct:**
```
Fix: Use optional chaining at line 67:
  getDiscount(code)?.discount ?? 0

Verification:
- Test with invalid code (should return subtotal)
- Test with valid code (should apply discount)
- AC: No errors thrown for any input
```

## Common Pitfalls

| Pitfall | Impact | Solution |
|---------|--------|----------|
| Assumptions without verification | Wrong diagnosis | Use MCP to verify library behavior |
| Skipping intel queries | Token waste | Always query before reading |
| Incomplete reproduction steps | Can't verify fix | Document exact steps |
| No fix proposal | Bug remains open | Always propose specific fix |

## When to Use This Skill

**Use debug-issues when:**
- User reports an error or bug
- Tests are failing
- Unexpected behavior occurs
- Performance is degraded
- Memory issues detected

**Don't use when:**
- User wants general code analysis (use analyze-code skill)
- User wants to plan implementation (use create-plan skill)
- No specific error (use analyze-code for investigation)

## Related Skills & Commands

- **Analyze-code skill** - For general code analysis (not bug-specific)
- **Implement-and-verify skill** - For implementing the fix after debugging
- **/bug command** - User-invoked debugging (can invoke this skill)

## Success Metrics

**Accuracy:**
- Root cause identified: 95%+
- Fix proposal validated: 100%

**Efficiency:**
- Token usage: 80%+ savings vs direct reading
- Time to diagnosis: 5-15 minutes

**Completeness:**
- CoD^Σ trace: 100% complete
- MCP verification: 100% for library issues

## Version

**Version:** 1.0
**Last Updated:** 2025-10-19
**Owner:** Claude Code Intelligence Toolkit
