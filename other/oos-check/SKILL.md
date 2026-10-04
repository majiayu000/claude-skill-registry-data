---
name: oos-check
description: Pre-check if a Bug Bounty finding is Out-of-Scope. Auto-triggered at Phase 0 (full scan) and Phase 1 (per-finding). Matches "OOS", "out of scope", "exclusion check"
user-invocable: true
argument-hint: <target-dir> [finding-type]
allowed-tools: [Read, Grep, Glob, Bash, WebFetch]
---

# OOS (Out-of-Scope) Pre-Check

## CRITICAL RULES (NEVER VIOLATE)
1. **BLOCK → immediately remove finding from vulnerability_candidates.md**
2. **WARN → do NOT proceed without bypass reframing strategy**
3. **Phase 0 = full program OOS scan, Phase 1 = per-finding scan — never skip**

OOS misses account for 22% of all failures — CapyFi (oracle staleness), AXIS (D-Bus) were both explicitly listed in program brief.

## Input
- `$ARGUMENTS`: `<target-dir>` (e.g., `targets/keeper`) + optional `[finding-type]` (e.g., `oracle-staleness`)
- If no finding-type: full program OOS scan

## Procedure

### Step 1: Load Program Rules
```
Read targets/<target>/program_rules_summary.md
```
- Extract OOS items from "Exclusion List" section
- Extract known issues from "Known Issues" section

### Step 2: Common Exclusion Pattern Matching
Load OOS pattern DB (`scripts/oos_patterns.json`) and cross-match with finding-type:

!`cat /home/rootk1m/01_CYAI_Lab/01_Projects/Terminator/.claude/skills/oos-check/scripts/oos_patterns.json 2>/dev/null || echo "pattern DB not found"`

### Step 3: Platform OOS Verification
- Immunefi: `immunefi.com/common-vulnerabilities-to-exclude/` default exclusion list
- H1/Bugcrowd: program policy page "Out of Scope" items

### Step 4: Verdict

| Result | Condition | Action |
|--------|-----------|--------|
| **PASS** | No OOS pattern matched | Phase 1 proceed OK |
| **WARN** | Partial match (bypass possible) | Alert analyst + bypass reframing required |
| **BLOCK** | Clear OOS match | Auto-exclude finding. Analysis forbidden |

### Step 5: Output
```
[OOS-CHECK] Target: <target>
[OOS-CHECK] Finding type: <type or "full scan">
[OOS-CHECK] Program exclusions matched: <count>
[OOS-CHECK] Common pattern matched: <count>
[OOS-CHECK] Result: PASS / WARN(<reason>) / BLOCK(<reason>)
```

## Few-Shot Examples

### PASS — IDOR in user API
```
Finding: GET /api/users/{id} returns other users' PII without authorization check
Program OOS: "Rate limiting, clickjacking, self-XSS"
Pattern match: None
→ PASS (IDOR not in any exclusion list)
```

### BLOCK — Oracle staleness on Immunefi
```
Finding: Chainlink oracle has no staleness check, stale price could cause bad liquidation
Program OOS: Immunefi common exclusion "Incorrect data supplied by third party oracles"
Pattern match: "oracle-staleness" → Immunefi default exclusion
→ BLOCK (oracle staleness is auto-OOS on Immunefi unless manipulation via flash loan)
```

### WARN — D-Bus authorization bypass
```
Finding: D-Bus method call bypasses polkit authorization check
Program OOS: "Local access bugs OOS unless vertical privilege escalation to root"
Pattern match: "dbus-local" → partial (root escalation chain could bypass)
→ WARN (need root escalation chain to reframe as in-scope)
```

## Lessons Learned (this skill exists to catch these)
- **CapyFi**: oracle staleness → Immunefi common exclusion. OOS rejection
- **AXIS**: D-Bus auth bypass → "local access OOS unless root escalation" in brief
- **Kiln DeFi**: offset=0 vault → code path inactive = latent bug = OOS
- **stake.link**: sandwich attack → "third party oracle data" OOS by default
- **DEXX/HackenProof**: rate limiting + account pre-takeover = OOS (platform-specific)

> **REMINDER**: BLOCK = remove from candidates immediately. WARN = no progress without bypass reframing.
