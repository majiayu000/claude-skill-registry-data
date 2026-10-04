---
name: slop-check
description: Measure AI slop score (0-10) in reports. Used by triager-sim/reporter. Matches "slop", "AI detection", "ai detection", "template language"
user-invocable: true
argument-hint: <report-file-path>
allowed-tools: [Read, Bash, Grep]
---

# AI Slop Detection

## CRITICAL RULES (NEVER VIOLATE)
1. **KILL (6+) → delete finding or full rewrite** — simple pattern removal is insufficient
2. **STRENGTHEN (3-5) → remove ALL flagged patterns then re-check**

Measures AI slop score on 0-10 scale.
AI-generated reports are a problem in 40%+ of submissions — triagers actively detect them.

## Input
- `$ARGUMENTS`: report file path

## Score Thresholds (unified standard)

| Score | Verdict | Action |
|-------|---------|--------|
| **0-2** | PASS | Ready for submission |
| **3-5** | STRENGTHEN | Rewrite required — remove slop patterns, re-check |
| **6-10** | KILL | Submission forbidden — full rewrite or delete finding |

## Few-Shot Examples

### PASS (score 1) — Specific, observational, evidence-rich
```
The `pg_list_all_subscriptions()` function returns the `conninfo` field
containing plaintext credentials for cross-owner subscriptions.

Tested on Aiven PostgreSQL 14.9 (plan hobbyist):
  SELECT subname, subconninfo FROM pg_subscription;
  → subconninfo = 'host=xxx password=s3cret_value'

Impact: Any database user with pg_read_all_stats can read connection
passwords of subscriptions owned by other users.
```

### KILL (score 7) — Template language, no specifics, vague impact
```
It is important to note that this comprehensive vulnerability leverages
a robust attack vector. Furthermore, the holistic impact potentially
facilitates unauthorized access to sensitive data. Subsequently, this
could lead to significant security implications. It should be noted
that the vulnerability seamlessly enables privilege escalation.
```

## Procedure

### Step 1: Read Report
```
Read $ARGUMENTS
```

### Step 2: Slop Pattern Count

**Template language** (+0.5 each):
!`grep -ciE "It is important to note|comprehensive|robust|Furthermore|In conclusion|It should be noted|leveraging|utilizing|In summary|As mentioned|It is worth noting|It is crucial|seamlessly|facilitate|Subsequently|Consequently|Notably|Specifically|Importantly|holistic|paradigm|synergy|delve into|multifaceted" "$ARGUMENTS" 2>/dev/null || echo "0"`

**Uncertain language** (+0.5 each):
!`grep -ciE "should work|probably|most likely|presumably|seems to|appears to|it is believed|potentially|theoretically|could potentially|might potentially" "$ARGUMENTS" 2>/dev/null || echo "0"`

**Missing specific evidence** (+2):
- No specific block number / tx hash / timestamp
- No specific file:line references
- No actual response captures

### Step 3: Positive Signals (deductions)

**Target-specific details** (-1 each):
- Specific block number or tx hash included
- Actual API response or error message quoted
- Specific code line reference (file.ts:123)
- Custom analysis element (unique attack scenario name, diagram, etc.)

**Structure differentiation** (-0.5):
- Different section order from previous submissions
- Observational language ("identified in reviewed code")

### Step 4: Score Calculation
```
score = 0
score += template_language_count * 0.5
score += uncertain_language_count * 0.5
score += (2 if no_specific_evidence else 0)
score -= target_specific_details * 1.0
score -= (0.5 if structure_differentiated else 0)
score = clamp(score, 0, 10)
```

### Step 5: Cross-validation with validation_prompts.py (if available)
!`python3 -c "
import sys; sys.path.insert(0, '/home/rootk1m/01_CYAI_Lab/01_Projects/Terminator')
from tools.validation_prompts import check_ai_slop
with open('$ARGUMENTS') as f: text = f.read()
result = check_ai_slop(text)
print(f'validation_prompts score: {result}')
" 2>/dev/null || echo "validation_prompts.py unavailable — manual scoring only"`

### Step 6: Output
```
[SLOP-CHECK] File: <path>
[SLOP-CHECK] Template language instances: N
[SLOP-CHECK] Uncertain language instances: N
[SLOP-CHECK] Specific evidence present: YES/NO
[SLOP-CHECK] Target-specific details: N
[SLOP-CHECK] Score: X/10
[SLOP-CHECK] Result: PASS (<=2) / STRENGTHEN (3-5) / KILL (6+)
[SLOP-CHECK] Fix suggestions: <specific fix suggestions>
```

> **REMINDER**: KILL = delete or full rewrite. triager-sim uses this score for SUBMIT/STRENGTHEN/KILL verdict.
