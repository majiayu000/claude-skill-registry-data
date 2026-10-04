---
name: threat-model-check
description: Verify attack prerequisites are realistic. Block unrealistic threat models pre-submission. Matches "threat model", "attack prerequisites", "prereq check"
user-invocable: true
argument-hint: <finding-description-or-file>
allowed-tools: [Read, Bash]
---

# Threat Model Consistency Check

## CRITICAL RULES (NEVER VIOLATE)
1. **BLOCK → finding MUST NOT be sent to exploiter**
2. **3+ prerequisites = unrealistic attack scenario** → automatic BLOCK
3. **D-Bus/local access → BLOCK unless root escalation chain exists**

Verifies that a finding's attack prerequisites are consistent with the program's threat model.
Threat model breaches account for 19% of all failures (MCP, Immutable, OPPO).

## Input
- `$ARGUMENTS`: finding description text or report file path

## Procedure

### Step 1: Extract Attack Prerequisites
Read finding and classify what the attacker must control:

| Prerequisite Category | Description | Realism |
|-----------------------|-------------|---------|
| Network access | Reachable from internet | HIGH (common) |
| User credentials | Valid account/token required | MEDIUM (phishing etc.) |
| Code execution | Execute code on target system | LOW (already compromised) |
| Infrastructure access | Server/cloud access | VERY LOW |
| Physical access | Physical device access | VERY LOW |
| Insider | Internal org privileges | VERY LOW |
| Victim device access | Access to victim's device | LOW |
| MitM position | Network intermediary position | LOW-MEDIUM |

### Step 2: Prerequisite Count Verdict
```
prerequisite_count = number of categories attacker must control

if prerequisite_count == 0-1:
    → PASS (realistic attack scenario)
elif prerequisite_count == 2:
    → WARN ("2 prerequisites — attack feasibility may be low")
elif prerequisite_count >= 3:
    → BLOCK ("3+ prerequisites — unrealistic attack scenario")
```

### Step 3: Program Threat Model Cross-check
```
Read targets/<target>/program_rules_summary.md  # program threat model
```

Special rules:
- **D-Bus/local access** → no root escalation chain → **BLOCK**
- **Admin/governance access** → "admin trust assumed" program → **BLOCK**
- **Physical access required** → no remote exploit → **WARN** (low severity)
- **User interaction required** → 1-click = OK, complex scenario = **WARN**

### Step 4: Output
```
[THREAT-MODEL] Finding: <summary>
[THREAT-MODEL] Prerequisites:
  - [category1]: <description> (realism: HIGH/MEDIUM/LOW)
  - [category2]: <description> (realism: HIGH/MEDIUM/LOW)
[THREAT-MODEL] Prerequisite count: N
[THREAT-MODEL] Program threat model match: YES/NO
[THREAT-MODEL] Result: PASS / WARN(<reason>) / BLOCK(<reason>)
```

## Few-Shot Examples

### PASS (1 prerequisite) — Remote API IDOR
```
Finding: GET /api/invoices/{id} returns any user's invoice without auth check
Prerequisites: [Network access] (realism: HIGH)
Prerequisite count: 1
→ PASS — realistic, single prerequisite, internet-reachable API
```

### WARN (2 prerequisites) — Authenticated SSRF
```
Finding: Authenticated user can trigger SSRF via webhook URL parameter
Prerequisites: [Network access] + [User credentials]
Prerequisite count: 2
→ WARN — feasible but requires valid account. Disclose prerequisite honestly
```

### BLOCK (3+ prerequisites) — Local D-Bus + SUID + config
```
Finding: D-Bus method bypasses polkit, then SUID binary reads config with secret
Prerequisites: [Local access] + [D-Bus session] + [Specific SUID binary present]
Prerequisite count: 3
Program OOS: "local access bugs OOS unless root escalation"
→ BLOCK — 3 prerequisites + no root chain + matches program OOS rule
```

## Lessons Learned
- **MCP (Immutable)**: "attacker can modify MCP server code" premise → program judged "intended behavior"
- **OPPO**: "static analysis alone claims RCE" → no execution environment access to prove → Informative
- **AXIS D-Bus**: local access + D-Bus call → no root escalation chain → OOS
- **Keeper EPM**: "unauthenticated" claim → only tested with enrolled user → peer credential checking existed

> **REMINDER**: BLOCK = never send to exploiter. More prerequisites = lower severity (adjust CVSS PR/UI).
