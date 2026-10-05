---
name: diagnostic-fix
description: Structured diagnostic-then-fix workflow using GitNexus knowledge graph
  and Ariya-4 problem framing. Gathers symptoms, isolates root causes, formulates
  hypotheses, verifies via reproduction, and applies targeted fixes.
argument-hint: <error symptom or stack trace>
---

<!-- Generated from workflows/diagnostic-fix.md by tools/generate_integrations.py. Edit the source file, not this one. This is an execution WORKFLOW packaged as an Agent Skill so it is discoverable and directly invocable ("/diagnostic-fix") in every compatible tool. -->

# Workflow: Diagnostic-then-Fix

## When to Use
| Criteria | Match |
|----------|-------|
| Intention | bug_fix, error_investigation |
| Complexity | unknown root cause, needs tracing |
| Power Mode | Balanced or Deep |
| Clarity | symptom is known, cause is unknown |

## Required Skills
- codebase-understanding (GitNexus) — HEAVY use
- file-operations
- code-execution
- code-quality-testing
- communication-tone
- safety-profiles (default)

## Flow

### Phase 0: Thinking Stage (Pre-Action)
- [ ] What is the exact symptom? Error message, wrong output, crash?
- [ ] Have I gathered all available diagnostic context? (logs, stack traces, state)
- [ ] Do NOT jump to fixing — root cause must be identified first
- [ ] Re-evaluate intent: is this diagnostic or fix? *(Factory)*

### Phase 1: Gather Symptoms
- What is the exact error message / unexpected behavior?
- When does it happen? (always, intermittent, specific conditions)
- What changed recently that might have caused it?

### Phase 2: Trace Root Cause (Ariya-4 Problem Frame)

Before proposing any fix, complete all 4 fields of the Ariya-4 Problem Frame:
- **Problem**: What is actually broken (the root mechanism, not the symptom).
- **Cause**: Root causes (structural constraints, misaligned incentives, or reinforcing feedback loops).
- **Cessation**: Definition of Done (measurable, specific, bounded criteria for resolution).
- **Path**: Least-friction route from Problem to Cessation.

```
1. query({search_query: "<error text or symptom>"})
   → Identify suspect symbols and execution flows

2. context({name: "<suspect>"})
   → See all callers, callees, and processes

3. trace({from: "<entry_point>", to: "<suspect>"})
   → Find the shortest call chain if needed

4. READ gitnexus://repo/{name}/process/{name}
   → Step-by-step execution trace
```

### Phase 3: Confirm Hypothesis
- Read source files at identified locations
- Add targeted logging to confirm the flow
- Reproduce the issue if possible
- If hypothesis is wrong: return to Phase 2 with new information

### Phase 4: Fix
- Apply minimal targeted change addressing root cause
- DO NOT fix symptoms — fix the root
- DO NOT refactor unrelated code

### Phase 5: Verify
- Run tests for affected execution flows
- Verify the original symptom is resolved
- Run `detect_changes()` to check blast radius

### Phase 5b: Sanity Check
- [ ] Did I fix the ROOT CAUSE, not just the symptom?
- [ ] Have I verified the original symptom is actually resolved?
- [ ] Are there other places with the same pattern that need fixing?
- [ ] Did `detect_changes()` show only expected files changed?
- [ ] Is the fix minimal? No unrelated refactoring?

### Phase 6: Report
- Root cause (1 sentence)
- Fix applied (1-2 sentences)
- Verification result

## Token Budget
- **Typical**: 10K-40K tokens
- **Max recommended**: 80K tokens
- **Warning threshold**: >80K → consider session summarization

## GitNexus Integration — Required
This workflow depends on GitNexus for:
- `query` — find code related to error
- `context` — 360° view of suspect symbols
- `trace` — call chain between entry point and error site
- `detect_changes` — verify fix scope

If GitNexus index is stale, run `npx gitnexus analyze` first.

## Hallucination Watchpoints
- Fixing symptoms instead of root cause (most common)
- Making changes without tracing the full path
- Applying multiple fixes at once (which one worked?)
- Editing files in a loop without verifying results
- Assuming the error source based on surface similarity

## Example
```
User: "Payment endpoint returns 500 intermittently"

Phase 2:
1. query({search_query: "payment error handling"})
   → CheckoutFlow: processPayment → validateCard → chargeStripe
   → ErrorHandling: handlePaymentError

2. context({name: "validatePayment"})
   → Outgoing calls: verifyCard, fetchRates (external API!)

3. trace({from: "checkoutHandler", to: "fetchRates"})
   → checkoutHandler → processPayment → validatePayment → fetchRates

4. Read fetchRates → no timeout configured on HTTP call

Phase 4: Add 5s timeout to fetchRates HTTP call
Phase 5: detect_changes() → only fetchRates.ts changed ✓
```
