---
license: Apache-2.0
name: allen-cacm1983
description: Temporal interval algebra for reasoning about time relationships in planning and knowledge representation
category: Research & Academic
tags:
  - temporal-reasoning
  - interval-algebra
  - knowledge-representation
  - ai
  - planning
---

# SKILL.md: Temporal Interval Reasoning (Allen 1983)

## When to Use This Skill

Load this skill when you encounter:

| Trigger Situation | Why Allen Applies |
|---|---|
| "Does task A finish before task B starts?" | Requires interval relation classification (before, meets, overlaps…) |
| "I don't know exactly when X happened, only that it was during Y" | Disjunctive uncertainty over the 13 relations |
| "If we add this constraint, does the schedule still work?" | Constraint propagation + inconsistency detection |
| "Event A happens daily; event B happens yearly — how do they interact?" | Reference interval hierarchy for scope management |

**Do not use** if you only need to compare two absolute timestamps with no uncertainty — plain arithmetic suffices.

---

## Decision Points

### New Temporal Assertion Added
```
IF assertion conflicts with existing constraints:
    → Detect empty arc label during propagation
    → HALT immediately, report inconsistent interval pair
    → Do NOT continue with inconsistent state

IF assertion is consistent:
    → Run constraint propagation from affected arcs
    → Update labels by intersecting transitivity consequences
    → Continue until no more refinements possible
```

### Handling Temporal Uncertainty
```
IF evidence only supports multiple relations:
    → Maintain full disjunctive label {before, meets, overlaps}
    → Never collapse to single relation without evidence
    → Log when/why constraint set narrows

IF forced to act under uncertainty:
    → Use disjunctive label as-is for planning
    → Tag any assumptions as defeasible
    → Avoid premature commitment
```

### Scoping Temporal Reasoning
```
IF dealing with events at vastly different timescales:
    → Identify reference interval hierarchy (year→month→day)
    → Reason within each cluster separately
    → Create explicit bridge constraints at boundaries
    → Avoid flattening everything into one global graph

IF local reasoning feels sufficient:
    → Verify query scope matches reference interval level
    → Propagate only within relevant cluster
    → Escalate cross-cluster only when dependency detected
```

### State Persistence
```
IF state continues with no explicit end bound:
    → Apply persistence default AND mark as defeasible
    → Any future end-bound assertion overrides default
    → Never treat persistence assumption as hard constraint

IF explicit temporal bound provided:
    → Override any existing persistence defaults
    → Propagate new constraint normally
```

---

## Failure Modes

| Anti-Pattern | Symptom | Diagnosis | Fix |
|---|---|---|---|
| **Point-ification** | Reducing events to timestamps, losing overlap/containment info | Using `time=14:30` instead of `[14:30, 14:45]` intervals | Model every event as interval with start/end, even if duration unknown |
| **Premature Commitment** | Picking single relation when evidence supports multiple | Asserting "before" when you only know "not during" | Maintain full disjunctive label until evidence forces narrowing |
| **Global Propagation Bomb** | O(N²) cost per update, performance degrades with KB size | Running constraint propagation across entire graph for local query | Use reference interval hierarchy to limit propagation scope |
| **Empty Label Denial** | Continuing reasoning after inconsistency detected | Getting nonsense results because conflicting constraints ignored | Treat empty arc label as SUCCESS (inconsistency caught early), halt immediately |
| **Persistence Rigidity** | Cannot override "continues until changed" assumptions | New temporal bounds rejected because they conflict with persistence | Tag all persistence defaults as defeasible, allow override by explicit assertions |

**Detection Rules:**
- If you see timestamps without duration → Point-ification
- If you see single relation chosen arbitrarily → Premature Commitment  
- If propagation cost grows with total KB size → Global Propagation Bomb
- If reasoning continues after empty label → Empty Label Denial
- If new temporal facts get rejected → Persistence Rigidity

---

## Worked Examples

### Example 1: Meeting Schedule Conflict Detection

**Scenario:** Adding "Team Review" to calendar that already has "Client Call" and "Engineering Standup"

**Initial State:**
```
Client Call (I₁): [10:00, 11:00]
Engineering Standup (I₂): [11:30, 12:00]
Known: I₁ {before} I₂
```

**New Assertion:** Team Review (I₃): [10:45, 11:15]

**Expert Reasoning Trace:**
1. **Classify new relations:**
   - I₃ vs I₁: starts at 10:45, I₁ ends at 11:00 → {overlaps}
   - I₃ vs I₂: ends at 11:15, I₂ starts at 11:30 → {before}

2. **Constraint propagation:**
   - From I₁ {before} I₂ and I₃ {overlaps} I₁
   - Transitivity: overlaps ∘ before = {before, overlaps, meets, starts, during}
   - New constraint: I₃ {before, overlaps, meets, starts, during} I₂
   - Intersect with I₃ {before} I₂: label becomes {before}

3. **Consistency check:** All labels non-empty → Schedule is feasible but has overlap

**Novice Would Miss:** 
- Might not check I₃ overlap with I₁ creates resource conflict
- Might not verify transitivity maintains consistency
- Might not distinguish "feasible ordering" from "no resource conflicts"

**Expert Catches:**
- Overlap detection flagged immediately via relation classification
- Propagation verifies global consistency maintained
- Clear distinction between temporal feasibility and resource availability

### Example 2: Process Phase Dependencies

**Scenario:** Deployment pipeline with uncertain task completion times

**Initial State:**
```
Build Phase (B): duration unknown, must finish before Deploy
Test Phase (T): overlaps with end of Build, duration uncertain  
Deploy Phase (D): starts after both B and T complete
```

**Constraint Network:**
```
T {overlaps, finishes} B  (Test can finish with or before Build)
B {before, meets} D       (Build must complete before Deploy)
T {before, meets} D       (Test must complete before Deploy)
```

**New Information:** "Test found critical bug, extending by 2 hours"

**Expert Reasoning:**
1. **Update affects scope:** Test extension pushes T endpoint later
2. **Propagation:** If T {finishes} B originally, now T {overlaps} B (extends past Build end)
3. **Check consistency:** T {overlaps} B still allows B {before, meets} D and T {before, meets} D
4. **Result:** Deployment delayed but pipeline logic intact

**Novice Would Miss:**
- Might assume Test completion doesn't affect Build-Deploy dependency
- Might not propagate Test extension through to Deploy timing
- Might treat "Test extends" as isolated fact rather than constraint network update

**Expert Catches:**
- Recognizes Test-Build relation must be re-evaluated
- Propagates timing implications through full constraint network
- Maintains uncertainty appropriately (Deploy could start immediately after Build OR after extended Test)

---

## Quality Gates

Temporal reasoning task is complete when:

- [ ] All intervals represented with explicit start/end bounds (no point events)
- [ ] Every interval pair has non-empty arc label from the 13-relation vocabulary
- [ ] Constraint propagation run to completion (no pending transitivity updates)
- [ ] All disjunctive labels honestly reflect current evidence (no arbitrary commitments)
- [ ] Reference interval hierarchy established for multi-scale reasoning
- [ ] Persistence defaults tagged as defeasible where applicable
- [ ] Inconsistency detection verified (empty labels caught and reported)
- [ ] Cross-reference scope bridges explicitly defined
- [ ] All temporal assertions traced to evidence source
- [ ] Query scope matches reasoning granularity level

---

## NOT-FOR Boundaries

**Do NOT use Allen's interval algebra for:**

- **Simple timestamp comparison** → Use arithmetic: `if (t1 < t2)`
- **Metric duration calculation** → Use calendar arithmetic: `end_date - start_date`
- **Real-time scheduling optimization** → Use constraint satisfaction with numeric domains
- **Probabilistic temporal inference** → Use temporal probabilistic networks
- **Continuous time dynamics** → Use differential equations
- **High-frequency event streams** → Use stream processing frameworks

**Delegate instead:**
- For metric constraints: Use **constraint-satisfaction-with-numeric-domains**
- For probabilistic temporal reasoning: Use **bayesian-temporal-networks** 
- For real-time systems: Use **rate-monotonic-scheduling**
- For continuous dynamics: Use **temporal-logic-model-checking**
- For event stream processing: Use **complex-event-processing**

**Allen excels at:** Qualitative temporal reasoning under uncertainty with incremental knowledge updates and hierarchical scope management.