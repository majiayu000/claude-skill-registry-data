---
name: spec
description: Create traceable specifications from architecture. Use after architecture is approved to define invariants, edge cases, and acceptance criteria.
---

# GATE 2: SPECIFICATION — SPEC_ENGINEER PROTOCOL

> **Agent**: SPEC_ENGINEER
> **Gate**: 2 of 6
> **Prerequisite**: Gate 1 (Architecture) COMPLETE
> **Output**: docs/specification/SPECIFICATION.md

---

## GATE 2 ENTRY CHECKLIST

Before proceeding, verify:

- [ ] .fortress/gates/GATE_1_ARCHITECTURE.md exists
- [ ] docs/architecture/ARCHITECTURE.md is approved
- [ ] HOSTILE_ARCHITECT has signed off
- [ ] All SPEC_IDs from Gate 1 are listed

**If any checkbox fails**: STOP. Complete Gate 1 first.

---

## SPEC_ENGINEER PROTOCOL

### Step 1: Extract Every Invariant

Read ARCHITECTURE.md line by line. For every:
- "must"
- "shall"
- "always"
- "never"
- "at least"
- "at most"

Create an invariant entry:

```markdown
## INVARIANT REGISTRY

| INV_ID | Statement | Source | Enforcement | Test Type |
|:-------|:----------|:-------|:------------|:----------|
| INV001 | risk_score in [0.0, 1.0] | S001 | property test | proptest |
| INV002 | signals never None | S001 | type system | mypy |
| INV003 | cache expires after TTL | S020 | timer test | unit |
| INV004 | API timeout ≤ 500ms | S030 | config | integration |
| INV005 | offline mode = no network | S025 | mock assert | unit |
| INV006 | package name ASCII only | S001 | validation | unit+fuzz |
| INV007 | registry response cached | S020 | cache hit test | unit |
```

### Step 2: Catalog All Edge Cases

For each data structure and operation, enumerate:

```markdown
## EDGE CASE CATALOG

### Package Name Input (EC001-EC010)

| EC_ID | Scenario | Input | Expected | Test |
|:------|:---------|:------|:---------|:-----|
| EC001 | Empty name | "" | ValidationError | unit |
| EC002 | Very long name | "a"*1000 | ValidationError | unit |
| EC003 | Unicode name | "flask-помощник" | ValidationError | unit |
| EC004 | Special chars | "flask@redis" | ValidationError | unit |
| EC005 | Valid name | "flask-redis-helper" | Passes | unit |
| EC006 | Underscore vs hyphen | "flask_redis" | Normalized | unit |
| EC007 | Case sensitivity | "Flask" → "flask" | Normalized | unit |
| EC008 | Numbers | "py3-redis" | Passes | unit |
| EC009 | Leading hyphen | "-flask" | ValidationError | unit |
| EC010 | Trailing hyphen | "flask-" | ValidationError | unit |

### Registry Responses (EC011-EC020)

| EC_ID | Scenario | Input | Expected | Test |
|:------|:---------|:------|:---------|:-----|
| EC011 | Package exists | "flask" | exists=true | unit |
| EC012 | Package not found | "nonexistent123" | exists=false | unit |
| EC013 | Registry timeout | network delay | TimeoutError | unit |
| EC014 | Registry 500 error | mock 500 | RetryError | unit |
| EC015 | Rate limited | 429 response | RateLimitError | unit |
| EC016 | Invalid JSON | malformed | ParseError | unit |
| EC017 | Missing fields | partial JSON | graceful default | unit |
| EC018 | Empty response | {} | handled | unit |
| EC019 | Huge response | 10MB JSON | truncated/error | unit |
| EC020 | Network offline | no connection | OfflineMode | unit |

### Risk Scoring (EC021-EC030)

| EC_ID | Scenario | Input | Expected | Test |
|:------|:---------|:------|:---------|:-----|
| EC021 | All signals safe | no risk signals | score=0.0 | unit |
| EC022 | All signals risky | all risk signals | score=1.0 | unit |
| EC023 | Mixed signals | some risky | 0<score<1 | unit |
| EC024 | New package | age<30 days | contributes risk | unit |
| EC025 | No downloads | downloads=0 | contributes risk | unit |
| EC026 | No repo link | repo=null | contributes risk | unit |
| EC027 | Hallucination pattern | "flask_*_helper" | contributes risk | unit |
| EC028 | Popular package | flask, requests | score≈0 | unit |
| EC029 | Exact known slop | from database | score=1.0 | unit |
| EC030 | Typosquat candidate | "reqeusts" | score high | unit |
```

### Step 3: Create Acceptance Matrix

Map every SPEC_ID to required tests:

```markdown
## ACCEPTANCE MATRIX

| SPEC_ID | Description | Unit | Property | Fuzz | Integration | Bench | Total |
|:--------|:------------|:-----|:---------|:-----|:------------|:------|:------|
| S001 | Package validation | 5 | 2 | 1 | 1 | 1 | 10 |
| S002 | Risk scoring | 10 | 3 | 1 | 0 | 1 | 15 |
| S003 | Signal detection | 8 | 2 | 0 | 0 | 0 | 10 |
| S010 | CLI interface | 5 | 0 | 0 | 3 | 0 | 8 |
| S020 | Caching | 6 | 1 | 0 | 2 | 1 | 10 |
| S030 | PyPI client | 4 | 0 | 0 | 3 | 1 | 8 |
| S040 | npm client | 4 | 0 | 0 | 3 | 1 | 8 |
| S050 | crates.io client | 4 | 0 | 0 | 3 | 1 | 8 |

### Test ID Assignment

| TEST_ID | SPEC_ID | Type | Description |
|:--------|:--------|:-----|:------------|
| T001.1 | S001 | unit | validate_package with valid input |
| T001.2 | S001 | unit | validate_package with empty input |
| T001.3 | S001 | property | risk_score always in bounds |
| T001.4 | S001 | fuzz | random package names |
| T001.5 | S001 | integration | real PyPI query |
| T001.6 | S001 | bench | latency measurement |
| ... | ... | ... | ... |
```

### Step 4: Define Failure Modes

```markdown
## FAILURE MODE ANALYSIS

### Critical Failures (Must Not Happen)

| FM_ID | Failure | Impact | Prevention | Detection |
|:------|:--------|:-------|:-----------|:----------|
| FM001 | False positive on popular pkg | User loses trust | Whitelist popular | Test against top-1000 |
| FM002 | Miss known malware | Security breach | Pattern database | Cross-reference CVEs |
| FM003 | Crash on input | Denial of service | Input validation | Fuzz testing |

### Recoverable Failures (Handle Gracefully)

| FM_ID | Failure | Impact | Recovery | Detection |
|:------|:--------|:-------|:---------|:----------|
| FM010 | Registry timeout | Slow check | Cache/retry | Timeout metric |
| FM011 | Rate limited | Slow check | Backoff | 429 counter |
| FM012 | Network offline | No online check | Cached/warn | Ping test |

### Degraded Operation

| Condition | Behavior | User Impact |
|:----------|:---------|:------------|
| No network | Use cache only | Stale data warning |
| Rate limited | Exponential backoff | Slower checks |
| Cache corrupt | Rebuild cache | One-time slowdown |
| API changed | Graceful fallback | Limited signals |
```

---

## SPECIFICATION DOCUMENT TEMPLATE

```markdown
# Phantom Guard — Specification

> **Version**: 0.1.0
> **Date**: YYYY-MM-DD
> **Status**: DRAFT | REVIEW | APPROVED
> **Approver**: [name] | PENDING

---

## 1. Invariant Registry

[Table from Step 1]

## 2. Edge Case Catalog

### 2.1 Input Validation
[Tables from Step 2]

### 2.2 Registry Interactions
[Tables from Step 2]

### 2.3 Risk Calculation
[Tables from Step 2]

### 2.4 CLI Behavior
[Tables for CLI edge cases]

## 3. Acceptance Matrix

[Tables from Step 3]

## 4. Test ID Registry

[Full list of TEST_IDs]

## 5. Failure Mode Analysis

### 5.1 Critical Failures
[Table from Step 4]

### 5.2 Recoverable Failures
[Table from Step 4]

### 5.3 Degraded Operation
[Table from Step 4]

## 6. Coverage Targets

| Metric | Target | Minimum |
|:-------|:-------|:--------|
| Line coverage | 90% | 85% |
| Branch coverage | 85% | 80% |
| Property test iterations | 10000 | 1000 |
| Fuzz duration | 1 hour | 10 min |

## 7. Trace Links

| SPEC_ID | INV_IDs | EC_IDs | TEST_IDs | Code Location |
|:--------|:--------|:-------|:---------|:--------------|
| S001 | INV001, INV002 | EC001-EC010 | T001.* | TBD |
| ... | ... | ... | ... | ... |

---

## Appendix: Open Questions
[Any unresolved specification details]
```

---

## GATE 2 EXIT CHECKLIST

Before Gate 2 is complete:

- [ ] docs/specification/SPECIFICATION.md exists
- [ ] Every invariant has INV_ID and test type
- [ ] Every edge case documented with EC_ID
- [ ] Acceptance matrix complete for all SPEC_IDs
- [ ] Every SPEC_ID has at least one TEST_ID
- [ ] Failure modes analyzed for critical paths
- [ ] Coverage targets defined
- [ ] SPEC_VALIDATOR review requested

**If any checkbox fails**: DO NOT PROCEED TO GATE 3.

---

## SPEC_VALIDATOR REVIEW

After completing specification:

```
/hostile-review specification
```

The reviewer checks:
- Are all invariants testable?
- Are edge cases exhaustive?
- Are failure modes realistic?
- Are coverage targets achievable?
- Are there missing specifications?

**Only after SPEC_VALIDATOR approval can Gate 2 be marked complete.**

---

## RECORDING GATE COMPLETION

```markdown
# .fortress/gates/GATE_2_SPECIFICATION.md

## Gate 2: Specification — COMPLETE

**Date**: YYYY-MM-DD
**Approver**: SPEC_VALIDATOR
**Output**: docs/specification/SPECIFICATION.md

### Summary
- X invariants defined
- Y edge cases cataloged
- Z test IDs assigned

### Coverage
- Total SPEC_IDs: X
- Total TEST_IDs: Y
- Tests per SPEC: average Z

### Next Gate
Gate 3: Test Design
```

---

## PROTOCOL VIOLATIONS

| Violation | Response |
|:----------|:---------|
| Invariant without test type | Add test type |
| SPEC_ID without TEST_ID | Assign TEST_ID |
| Edge case not tested | Add test case |
| Skipped SPEC_VALIDATOR review | Run review |
| Proceeding to Gate 3 without approval | BLOCKED |

---

*Gate 2 is about SPECIFYING what to test. Gate 3 is about DESIGNING those tests.*
