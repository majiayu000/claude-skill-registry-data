---
name: debug
description: Systematic debugging using hypothesis-driven investigation with test, narrow, and resolve loops
layer: hub
category: workflow
triggers:
  - "/debug"
  - "debug this"
  - "why is this broken"
  - "find the bug"
  - "this is not working"
  - "something is wrong with"
inputs:
  - symptom: Description of the observed incorrect behavior
  - expected: What the correct behavior should be (optional but helpful)
  - context: Error messages, stack traces, reproduction steps, recent changes (optional)
outputs:
  - rootCause: Identified root cause with evidence
  - hypothesis log: Record of hypotheses tested and their outcomes
  - fix recommendation: Suggested fix (handed off to fix skill for application)
linksTo:
  - fix
  - scout
  - test
  - code-review
linkedFrom:
  - cook
  - team
  - ship
preferredNextSkills:
  - fix
  - test
fallbackSkills:
  - scout
  - research
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - May run test commands to reproduce issues
  - May read many files during investigation
  - Produces hypothesis log in working memory
---

# Debug Skill

## Purpose

Systematically find the root cause of bugs using a disciplined hypothesis-test-narrow loop. This skill treats debugging as a scientific investigation, not a guessing game.

The core principle: **never change code to debug**. Observe, hypothesize, test, narrow. Only hand off to `fix` once the root cause is identified with evidence.

## Workflow

### Phase 1: Symptom Analysis

1. **Capture the symptom precisely**
   - What is the observed behavior? (exact error, incorrect output, crash, hang, etc.)
   - What is the expected behavior?
   - Is it reproducible? (always, sometimes, only under certain conditions)
   - When did it start? (after a specific change, deployment, data change)

2. **Gather initial evidence**
   - Error messages and stack traces (read them carefully -- every line matters)
   - Relevant log output
   - Browser console errors (if frontend)
   - Network requests/responses (if applicable)
   - Recent git changes in the affected area

3. **Classify the bug type** (this guides the investigation strategy)
   - **Crash/Error**: Code throws an exception or returns an error
   - **Wrong Output**: Code runs but produces incorrect results
   - **Performance**: Code is too slow or uses too many resources
   - **Race Condition**: Behavior depends on timing/ordering
   - **State Corruption**: Data gets into an invalid state over time
   - **Integration**: Works in isolation, fails when combined
   - **Environment**: Works in one environment, fails in another

### Phase 2: Hypothesis Generation

4. **Generate 2-5 hypotheses** ranked by likelihood. For each hypothesis:
   - **Statement**: "The bug is caused by [X] because [reasoning]"
   - **Evidence for**: What supports this hypothesis?
   - **Evidence against**: What contradicts this hypothesis?
   - **Test**: How can we confirm or eliminate this hypothesis?
   - **Effort**: How hard is it to test? (prefer easy tests first)

5. **Prioritize hypotheses** using these heuristics:
   - **Recent changes first**: If something just changed, start there
   - **Simple before complex**: Check obvious causes before subtle ones
   - **Cheap tests first**: If two hypotheses are equally likely, test the one that is faster to verify
   - **Follow the error**: Stack traces point at causes; start where they point

### Phase 3: Hypothesis Testing (Loop)

6. **Test the highest-priority hypothesis**
   - Read the relevant code carefully
   - Trace the execution path mentally or with search tools
   - Check variable values, function inputs/outputs, state transitions
   - Run existing tests if they cover the area
   - Use Grep to find related code that might interact

7. **Record the result**
   - **Confirmed**: Evidence strongly supports this as the root cause
   - **Eliminated**: Evidence contradicts this hypothesis
   - **Refined**: Partially correct -- adjust the hypothesis and continue
   - **Inconclusive**: Cannot determine -- need more information

8. **Narrow the search space**
   - Each test should eliminate possibilities, making the remaining search space smaller
   - If a hypothesis is eliminated, what does that tell us? Update remaining hypotheses.
   - If a hypothesis is refined, generate a more specific sub-hypothesis.

9. **Repeat from step 6** until root cause is identified or all hypotheses are exhausted.

### Phase 4: Root Cause Confirmation

10. **State the root cause clearly**
    - What is the exact bug? (the specific line(s), condition, or interaction)
    - Why does it happen? (the causal chain from trigger to symptom)
    - Under what conditions? (always, or only when [condition])

11. **Verify with evidence**
    - Can you trace from root cause to symptom step by step?
    - Does the root cause explain ALL observed symptoms?
    - Does the root cause explain why it worked before (if it did)?

12. **If all hypotheses exhausted without finding root cause**:
    - Generate new hypotheses based on what was learned
    - Escalate scope: look at infrastructure, dependencies, environment
    - Consider invoking `scout` for broader codebase exploration
    - Consider invoking `research` for known issues with the technology

### Phase 5: Handoff

13. **Produce the debug report** using the template below.
14. **Recommend fix approach** -- hand off to `fix` skill for implementation.
15. **Recommend test** -- suggest what test should be written to prevent regression.

## Debug Report Template

```markdown
# Debug Report

## Symptom
**Observed**: [exact behavior]
**Expected**: [correct behavior]
**Reproducibility**: Always | Sometimes | Rare
**First noticed**: [when/context]

## Root Cause
**Location**: [file:line]
**Cause**: [precise description]
**Mechanism**: [how the cause produces the symptom]

## Evidence Chain
1. [observation 1] → indicates [conclusion 1]
2. [observation 2] → confirms [conclusion 2]
3. Therefore: [root cause]

## Hypothesis Log
| # | Hypothesis | Test | Result |
|---|-----------|------|--------|
| H1 | [statement] | [what was checked] | Eliminated: [reason] |
| H2 | [statement] | [what was checked] | Confirmed |

## Recommended Fix
[Description of what should change and why]
**Affected files**: [list]
**Risk**: Low | Medium | High

## Regression Prevention
[What test should be written to catch this if it recurs]
```

## Usage

### With error message
```
/debug TypeError: Cannot read property 'map' of undefined in UserList component
```

### With symptom description
```
/debug The checkout flow completes but the order is not saved to the database
```

### With context
```
/debug Login stopped working after merging PR #42. Users get a 401 even with valid credentials.
```

### Continuing investigation
```
/debug We eliminated the auth middleware hypothesis. What else could cause 401s on the /api/user endpoint?
```

## Examples

### Example: Frontend crash

**Symptom**: "TypeError: Cannot read property 'map' of undefined"
**Hypotheses**:
1. API returns null instead of array (H1 -- test by checking API response)
2. Component renders before data loads (H2 -- test by checking loading state)
3. Data shape changed after API update (H3 -- test by comparing schema)

**Investigation**: Read the component, find it expects `data.items.map(...)`. Check the API endpoint -- it returns `{ items: [...] }` on success but `{ error: "..." }` on failure with no `items` key.
**Root cause**: Missing error handling -- component assumes API always returns items.

### Example: Silent data loss

**Symptom**: "Orders created via API are missing the discount field"
**Hypotheses**:
1. Discount field not included in API request body (H1)
2. Discount field not mapped in ORM model (H2)
3. Database migration did not add the column (H3)

**Investigation**: Check API route -- discount is in the request. Check ORM model -- discount field exists. Check database -- column exists. Check the create function -- found it: the `createOrder` function destructures the input but does not include `discount` in the destructured fields.
**Root cause**: Destructuring omission in `createOrder()` at `src/lib/orders.ts:42`.

## Guidelines

- **Never guess-and-fix** -- Changing code to see if it helps is not debugging; it is gambling. Understand the cause before changing anything.
- **Read error messages fully** -- The answer is often in the error message or stack trace. Read every line.
- **One variable at a time** -- When testing hypotheses, change only one thing. Otherwise you cannot attribute the result.
- **Document as you go** -- Record each hypothesis and result. This prevents circular investigation.
- **Time-box escalation** -- If 3 hypotheses are eliminated with no progress, step back and reconsider the problem framing.
- **Distinguish symptoms from causes** -- "The variable is null" is a symptom. "The function does not handle the empty response case" is a cause.
- **Check the obvious first** -- Typos, missing imports, wrong environment variables, stale cache. Check these before diving deep.
- **Trust the evidence, not your intuition** -- If the evidence says the "impossible" thing is happening, believe the evidence.
