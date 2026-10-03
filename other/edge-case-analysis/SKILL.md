---
name: edge-case-analysis
description: >
  Use when designing solutions to identify and test boundary conditions, unusual inputs,
  and uncommon scenarios that could cause failures. This skill provides a systematic
  approach to finding edge cases before they become bugs in production.
---

# Edge Case Analysis

## Overview
This skill defines how to systematically identify and test edge cases - unusual conditions, extreme values, or unexpected combinations that can cause failures. Finding edge cases early prevents production bugs and improves robustness.

## When to Use
- When designing functions, APIs, or user inputs
- Before delivering any solution that handles variable input
- When reviewing code or specifications for completeness
- When creating test plans
- **Don't use when:** Solution only handles fixed, known, single value

## Core Procedures

### Step 1: Identify Dimensions
For each input, parameter, or condition, identify its dimensions:
- **Range:** Minimum to maximum values
- **Type:** String, number, list, object, null, undefined
- **Length:** Empty, single, typical, maximum
- **Encoding:** Unicode, special characters, binary, emojis
- **State:** New, existing, deleted, locked, expired
- **Access:** Owner, admin, guest, anonymous, unauthorized

### Step 2: Apply Analysis Techniques
For each dimension:

**BOUNDARY VALUES:** Test exact boundaries and just outside
- Min-1, Min, Min+1, Typical, Max-1, Max, Max+1
- Zero, one, many, too many

**COMBINATIONS:** Test pairs of conditions
- Valid input + invalid state
- Normal operation at boundary conditions
- Multiple edge cases occurring simultaneously

**NEGATIVE TESTING:** Test what should NOT work
- Invalid types for each parameter
- Missing required fields
- Unauthorized access attempts
- Malformed input (truncated, corrupted)

**TEMPORAL:** Test time-based edge cases
- Midnight, end of month, leap day, DST changes
- Timezone conversions, expired data
- Race conditions, concurrent operations
- Rapid succession of same operation

### Step 3: Document and Prioritize
```
EDGE CASE
=========
Description: [what condition could cause a problem]
Category: [boundary/combination/negative/temporal/state]
Likelihood: [RARE/UNLIKELY/POSSIBLE/LIKELY]
Impact: [LOW/MEDIUM/HIGH/CRITICAL]
Test: [how to validate this edge case]
Status: [OPEN / TESTED PASS / TESTED FAIL / FIXED]
```

### Step 4: Validate Fixes
For each edge case that fails:
- Understand WHY it fails (root cause)
- Fix the root cause, not just the symptom
- Re-test the edge case
- Add to regression test suite

## Quality Checklist
- [ ] All input dimensions analyzed
- [ ] Boundary values identified for each dimension
- [ ] Negative testing scenarios defined
- [ ] Temporal edge cases considered (if applicable)
- [ ] High-impact edge cases added to test suite
- [ ] Root cause identified for any failing edge cases

## Error Handling
- **Error:** Too many edge cases to test all
  **Response:** Prioritize by Impact × Likelihood, test HIGH and CRITICAL first
- **Error:** Edge case requires conditions hard to reproduce
  **Response:** Simulate or mock the condition, document in automated test

## Cross-Team Integration
**Related Skills:** testing-strategy, test-driven-development, testing-verification, output-validation-checklist
**Used By:** Testers, developers, QA agents, validators, especially Performance, Load, Security testing agents