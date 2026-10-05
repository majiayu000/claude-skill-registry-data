---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, passing, or findings are confirmed - requires running verification and confirming output before making any success claims; evidence before assertions always
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command/check proves this claim?
2. RUN: Execute the FULL verification (fresh, complete)
3. READ: Full output, check results, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Build succeeds | Build command: exit 0 | Linter passing, looks good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Experiment worked | Data shows expected result | Protocol completed, assumed success |
| Finding confirmed | Statistical test: significant | Pattern observed, assumed real |
| Replication succeeded | Same result within tolerance | Similar result, close enough |
| Analysis complete | All steps executed, output verified | Script ran without errors |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/publish/report without verification
- Trusting automated reports without checking
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Script passed" | Script success ≠ correct results |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Software - Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Software - Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Research - Experiment:**
```
✅ [Check data] [See: effect size X, p < 0.05] "Hypothesis supported"
❌ "Experiment completed" / "Data collected"
```

**Research - Replication:**
```
✅ [Compare results] [See: within 5% of original] "Replication successful"
❌ "Protocol followed correctly"
```

**Requirements:**
```
✅ Re-read requirements → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Agent delegation:**
```
✅ Agent reports success → Check actual output → Verify changes → Report actual state
❌ Trust agent report
```

## Why This Matters

From past failures:
- Trust broken: "I don't believe you"
- Broken code shipped: would crash in production
- False findings reported: would fail replication
- Missing requirements shipped: incomplete work
- Time wasted on false completion → redirect → rework
- Violates: "Honesty is a core value."

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, publishing, reporting, sharing
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## The Bottom Line

**No shortcuts for verification.**

Run the check. Read the output. THEN claim the result.

This is non-negotiable.
