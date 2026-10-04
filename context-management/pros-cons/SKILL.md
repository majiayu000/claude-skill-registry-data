---
name: pros-cons
version: 1.0.0
description: Structure a decision into steelmanned, impact-weighted pros and cons - irreversible consequences flagged, the decisive unknown named, and a clear recommendation you can reject.
triggers:
  - pros and cons
  - help me decide
  - weigh this decision
  - should I
  - tradeoffs of
capabilities: []
inputs:
  - name: decision
    required: true
    description: The decision or options being weighed.
  - name: context
    required: false
    description: Constraints that matter (budget, deadline, risk tolerance, who is affected).
---

# Pros / Cons

## When to use
Use this when someone faces a real "should I...?" choice with genuine tradeoffs and wants a decision they can defend: both sides argued properly, consequences sized, and a recommendation they are free to override.

**Not for:** decisions with an obvious right answer (a pros/cons theater wastes everyone's time), choices that are purely a matter of taste, or situations that are actually blocked on a fact nobody has gathered yet - there the move is "find X out first," which this method surfaces but does not replace. Not a substitute for domain expertise on high-stakes safety, legal, or medical calls.

## Method
1. **Restate the decision in one sentence,** including the do-nothing option if it is viable - often it is the real baseline.
2. **Steelman both sides.** *Decision point:* write the strongest argument FOR and the strongest AGAINST as their best advocate would - if one side reads weaker, you have not steelmanned it, you have strawmanned it.
3. **Size each point high / med / low impact.** Ten trivial pros do not outweigh one high-impact con; never let the count decide.
4. **Flag irreversibility.** *Decision point:* any consequence that cannot be undone - data loss, burned relationship, signed contract, public statement - gets a "one-way door" marker and extra weight.
5. **Name the decisive unknown,** if one fact would settle it. Sometimes the honest recommendation is to go learn that fact cheaply first.
6. **Recommend one option** in two lines, and state its single biggest risk. "It depends" is banned unless you say exactly what it depends on.

## Example
**Input:** "should we rewrite the billing service in Go or keep patching the Node one"

**Output (abridged):**
**Decision:** Rewrite billing in Go now, or keep patching Node (do-nothing is viable).

**For rewrite:** (high) chronic memory leaks caused 3 billing incidents this quarter; (med) team already runs 4 Go services.
**Against:** (high, one-way door) 2-3 months where bugs land in TWO codebases during migration; (med) the leak might be fixable in days if profiled - nobody has tried.

**Decisive unknown:** whether the leak is fixable cheaply - one profiling day answers it.
**Recommendation:** Spend 2 days profiling before deciding. Biggest risk: the leak looks fixable, gets patched, and the architecture debt resurfaces in 6 months.

## Pitfalls
- **Strawmanning the loser.** Writing a weak version of the side you already reject so the "analysis" just confirms your prior.
- **Counting instead of weighing.** Declaring the side with more bullets the winner regardless of impact.
- **Missing the one-way door.** Treating an irreversible cost as just another medium con.
- **Cowardly ending.** Closing with "it depends" and no recommendation, leaving the person exactly where they started.

## Output format
```
**Decision:** <one sentence, include the do-nothing option if viable>

**For** <option>
- (high|med|low)[, one-way door] <steelmanned point>

**Against** <option>
- (high|med|low)[, one-way door] <steelmanned point>

**Decisive unknown:** <the one fact that would settle it, or "none">
**Recommendation:** <option> - <why, two lines>. Biggest risk: <one line>.
```
