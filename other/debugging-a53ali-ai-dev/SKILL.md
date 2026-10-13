---
name: debugging
description: Systematic hypothesis-driven debugging — reproduce, isolate, fix, verify
triggers: [debug, bug, broken, not working, error, exception, investigate, diagnose]
audience: engineer
---

# Debugging

## Context
Debugging is the process of finding and fixing defects. Random trial-and-error wastes time and often introduces new bugs. This skill applies a systematic, scientific method: observe, hypothesize, test, conclude.

Use this skill when:
- Something is broken and the cause is unknown
- An error is thrown in production or tests
- Behavior is unexpected and you need to isolate why

## Instructions

### The Debugging Loop

1. **Reproduce the problem first.**
   - Can you trigger it consistently? If not, find the conditions that make it intermittent.
   - Write a failing test that demonstrates the bug before changing any code.
   - Define "broken" precisely: what is the actual vs. expected output?

2. **Form a hypothesis.**
   - State your best guess at the root cause in one sentence.
   - Example: *"I think the cache is returning stale data because the TTL key is computed incorrectly."*
   - Do not guess multiple causes at once. Pick the most likely one.

3. **Design the smallest possible test of your hypothesis.**
   - Add a log, set a breakpoint, write a targeted unit test, or isolate the function.
   - Do not make changes to fix it yet. Only gather evidence.

4. **Evaluate the evidence.**
   - Does the evidence support your hypothesis? If yes, proceed to fix.
   - If no, revise your hypothesis. Go back to step 2.

5. **Fix and verify.**
   - Make the targeted fix.
   - Run the failing test — it must now pass.
   - Run the full test suite — nothing else must break.
   - If the test suite has no coverage of this area, add it now.

6. **Understand the blast radius.**
   - Could this bug exist elsewhere? Search for similar patterns in the codebase.
   - Is there a systemic cause (wrong abstraction, missing validation layer) that should be addressed at a higher level?

### Common Bug Patterns to Check
- **Off-by-one:** Boundary conditions on loops and array indices
- **Null/nil dereference:** Unguarded access to optional or missing values
- **Race condition:** Shared mutable state accessed concurrently without synchronization
- **Stale cache:** Reading data that has been updated elsewhere
- **Wrong environment config:** Different behavior in local vs. staging vs. production due to env vars
- **Type coercion:** Implicit conversions causing incorrect comparisons
- **Missing error propagation:** Error is caught but not rethrown or logged

### Debugging in Production
- Use structured logs and distributed tracing to reconstruct the sequence of events.
- Never deploy a fix to production without being able to reproduce the issue in a lower environment first.
- Prefer a feature flag to roll back behavior over a hotfix if the scope is unclear.

## Principles
- Source: [Debugging — a mindset (Martin Fowler Blog)](https://martinfowler.com)
- Key idea: *"A debugger that runs randomly is not a debugger — it's a lottery ticket. Systematic hypothesis testing is the only reliable path."*

## Output Format
When applying this skill, the agent should:
- State the reproduced bug with actual vs. expected behavior
- State the hypothesis
- Show the evidence gathered (logs, test output, code trace)
- Show the fix applied
- Confirm the test is now green and the suite is unaffected
