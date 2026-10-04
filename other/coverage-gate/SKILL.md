---
name: coverage-gate
description: Check endpoint_map.md coverage at Phase 1→2 transition. Blocks Phase 2 if below 80%. Matches "coverage check", "endpoint coverage", "Phase 2 gate"
user-invocable: true
argument-hint: <target-dir>
allowed-tools: [Read, Bash, Grep, Glob]
---

# Endpoint Coverage Gate

## CRITICAL RULES (NEVER VIOLATE)
1. **FAIL → Phase 2 is BLOCKED** — no Phase 2 spawn without coverage gate pass
2. **No premature "analysis complete" declarations** — must verify numbers against endpoint_map.md

Checks endpoint_map.md coverage at Phase 1→2 transition.
Lesson: NAMUHX had 40% coverage at Phase 2 entry; the real IDOR was in the untested 60%.

## Input
- `$ARGUMENTS`: target directory (e.g., `targets/keeper`)

## Procedure

### Step 1: Run bb_preflight.py coverage-check
!`python3 /home/rootk1m/01_CYAI_Lab/01_Projects/Terminator/tools/bb_preflight.py coverage-check "$ARGUMENTS" 2>&1`

### Step 2: Parse Result

| Result | Condition | Action |
|--------|-----------|--------|
| **PASS** | coverage >= 80% | Phase 2 proceed |
| **FAIL** | coverage < 80% | Phase 2 **BLOCKED**. Output UNTESTED endpoint list |
| **ERROR** | endpoint_map.md missing | Scout must generate it. Phase 2 blocked |

### Step 3: On FAIL — List UNTESTED Endpoints
!`grep -i "UNTESTED" "$ARGUMENTS/endpoint_map.md" 2>/dev/null || echo "endpoint_map.md not found"`

### Step 4: Small Target Exception
- Total endpoints < 10 → **100% coverage required** (not 80%)
- Reason: 1-2 untested endpoints on small targets = critical attack surface gap

### Step 5: Output
```
[COVERAGE-GATE] Target: <target>
[COVERAGE-GATE] Total endpoints: N
[COVERAGE-GATE] Tested: N (VULN=X, SAFE=Y, TESTED=Z)
[COVERAGE-GATE] Untested: N
[COVERAGE-GATE] Coverage: XX.X%
[COVERAGE-GATE] Threshold: 80% (or 100% for <10 endpoints)
[COVERAGE-GATE] Result: PASS / FAIL
[COVERAGE-GATE] Action: <"Phase 2 proceed" or "Additional analyst/exploiter round needed — UNTESTED list attached">
```

> **REMINDER**: FAIL = Phase 2 blocked. Spawn additional analyst/exploiter rounds targeting UNTESTED endpoints.
