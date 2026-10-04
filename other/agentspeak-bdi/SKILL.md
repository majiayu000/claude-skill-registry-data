---
license: Apache-2.0
name: agentspeak-bdi
description: Logic-based agent programming language implementing BDI architecture for practical autonomous agent development
category: Research & Academic
tags:
  - bdi
  - agents
  - agentspeak
  - logic-programming
  - agent-language
---

# SKILL.md — AgentSpeak(L) & BDI Agent Architecture

When autonomous entities must perceive, deliberate, and act while managing competing goals and responding to events without abandoning ongoing work.

---

## Decision Points

### Primary Architecture Selection
```
IF system needs only event-reaction with no persistent goals
  → Use reactive/rule system (BDI is overkill)
ELIF system needs planning in static environment with no interrupts  
  → Use classical planner
ELIF system needs both reactivity AND goal persistence in dynamic environment
  → Use BDI architecture
```

### Selection Function Invocation Table
| Situation | Use Function | Decision Criteria |
|-----------|-------------|-------------------|
| New event arrives | **SE** (Event Selection) | Priority, urgency, resource constraints |
| Event needs plan | **SO** (Option Selection) | Context guards, plan success history, risk tolerance |
| Multiple active intentions | **SI** (Intention Selection) | Deadlines, resource allocation, fairness policy |
| Plan failure occurs | **SO** then **SI** | Find failure-handling plan, then reschedule intentions |

### Plan Failure Recovery Decision Tree
```
Plan P fails executing action A:
IF failure-handling plan exists for this failure type
  → Post failure event, let SO select recovery plan
  → Continue with modified intention stack
ELIF alternative plans exist for same triggering event
  → Backtrack to event, let SO try next applicable plan  
  → Remove failed plan from consideration
ELIF no alternatives available
  → Propagate failure up intention stack
  → IF parent plan exists → trigger failure event at parent level
  → ELSE drop intention entirely
```

### Belief Update Impact Assessment
```
New belief B arrives:
IF B contradicts existing beliefs
  → Run belief revision protocol
  → Check all active intentions for context guard violations
  → IF context no longer holds → suspend intention (don't drop)
ELIF B enables new applicable plans
  → Check event queue for dormant events that now have applicable plans
  → Reprioritize using SE
ELIF B satisfies pending goal conditions  
  → Mark achievement, clean up related intentions
  → Post achievement event for plan cleanup
```

---

## Failure Modes

### 1. Plan Thrashing
**Symptoms:** Agent rapidly cycles between plans without making progress; same event triggers different plans repeatedly.
**Detection Rule:** If the same event is processed >3 times in N execution cycles with different plan selections each time, you have plan thrashing.
**Root Cause:** SO (option selection) function is non-deterministic or context guards are too weak/overlapping.
**Fix:** Make SO explicitly ordered by priority; strengthen context guards to be mutually exclusive; add plan success/failure history to selection criteria.

### 2. Stale Belief Paralysis  
**Symptoms:** Agent selects plans based on outdated world model; plans fail immediately due to false assumptions about environment.
**Detection Rule:** If plan failure rate >50% and failures are due to context guard violations at execution time (not planning time), you have stale beliefs.
**Root Cause:** Belief update frequency is too low relative to environment change rate; belief revision is not propagating to intention context checks.
**Fix:** Increase perception frequency; add belief staleness timestamps; suspend intentions when their context guards become invalid.

### 3. Infinite Intention Loops
**Symptoms:** Agent creates intentions that post events that create more intentions for the same goal; intention stack grows without bound.
**Detection Rule:** If intention stack depth increases monotonically over time without corresponding goal achievements, you have intention loops.
**Root Cause:** Plans create subgoals that eventually lead back to the original goal without termination conditions.
**Fix:** Add achievement detection in context guards; implement intention subsumption (merge duplicate intentions); add maximum recursion depth limits.

### 4. Policy-in-Plans Anti-Pattern
**Symptoms:** Same events trigger different behaviors based on conditionals inside plan bodies; agent policy is scattered and hard to change.
**Detection Rule:** If plan bodies contain priority/urgency conditionals (`if high_priority then X else Y`), policy is in the wrong place.
**Root Cause:** Agent rationality is encoded in plan logic instead of selection functions.
**Fix:** Move all priority/policy logic to SE/SO/SI functions; make plans policy-neutral and context-sensitive only.

### 5. Single-Intention Bottleneck
**Symptoms:** Agent cannot handle interrupts; urgent events wait while agent completes long-running tasks; no concurrency.
**Detection Rule:** If agent has at most one active intention at any time, you have single-intention bottleneck.
**Root Cause:** SI (intention scheduling) function is not implementing true concurrency; treating intentions as exclusive rather than concurrent.
**Fix:** Allow multiple active intentions; implement preemptive scheduling in SI; design plans as interruptible sequences.

---

## Worked Examples

### Example 1: Multi-Agent Task Allocation with Plan Conflicts

**Scenario:** Two agents (A1, A2) coordinate to achieve `deliver(package, destination)`. Both have plans but different capabilities.

**Initial State:**
- A1 beliefs: `location(A1, warehouse)`, `can_carry(A1, small_items)`, `location(package, warehouse)`
- A2 beliefs: `location(A2, depot)`, `can_carry(A2, any)`, `has_vehicle(A2)`
- Shared belief: `size(package, large)`, `destination(customer_site)`

**Event:** `+!deliver(package, customer_site)` posted to both agents

**Decision Process:**
1. **A1 Plan Selection (SO):**
   - Plan P1: `+!deliver(X,Y) : can_carry(A1,small_items) & size(X,small) <- pickup(X); transport(X,Y)`
   - Context guard fails: `size(package,large)` contradicts `size(X,small)`
   - No applicable plans → posts `plan_failure(deliver, no_capability)`

2. **A2 Plan Selection (SO):**
   - Plan P2: `+!deliver(X,Y) : can_carry(A2,any) & has_vehicle(A2) <- pickup(X); drive(X,Y); dropoff(X)`
   - Context guard succeeds → P2 selected
   - Creates intention I1: `[pickup(package), drive(package,customer_site), dropoff(package)]`

3. **A1 Belief Update:**
   - Receives message: `attempting(A2, deliver, package)`
   - Updates beliefs: `+delegated(deliver, package, A2)`
   - Drops failed intention

**Novice Error:** Would have both agents attempt delivery, creating resource conflicts.
**Expert Insight:** Coordination happens through belief sharing and plan context guards, not hardcoded agent knowledge.

### Example 2: Interrupt Handling with Intention Reconsideration

**Scenario:** Agent executing long-running data processing task receives urgent security alert.

**Initial State:**
- Active intention I1: `[process_batch(data1), process_batch(data2), generate_report()]`
- Current execution: middle of `process_batch(data1)` (will take 10 more minutes)

**Event:** `+security_alert(intrusion_detected, server_3)`

**Decision Process:**
1. **Event Selection (SE):**
   - SE priorities: security_events > routine_processing
   - `security_alert` selected over continuing I1

2. **Plan Selection (SO):**
   - Plan P3: `+security_alert(Type,Location) : has_admin_access <- isolate_system(Location); notify_team(Type)`
   - Context guard satisfied → P3 selected
   - Creates intention I2: `[isolate_system(server_3), notify_team(intrusion_detected)]`

3. **Intention Scheduling (SI):**
   - Current intentions: I1 (suspended at `process_batch(data1)`), I2 (new, urgent)
   - SI policy: security intentions preempt processing intentions
   - Selects I2 for execution

4. **Execution:**
   - Executes `isolate_system(server_3)` immediately
   - Executes `notify_team(intrusion_detected)`
   - I2 completes, drops from intention set

5. **Resumption:**
   - Only I1 remains: `[process_batch(data1), process_batch(data2), generate_report()]`
   - Resumes `process_batch(data1)` from suspension point

**Novice Error:** Would either ignore the security alert or abandon the processing task entirely.
**Expert Insight:** Intention suspension preserves progress while enabling responsive behavior. SI scheduling policy is explicit and configurable.

---

## Quality Gates

- [ ] Agent architecture has explicit SE, SO, SI selection functions with documented policies
- [ ] Each plan has well-defined triggering event and context guard that can be evaluated against current beliefs
- [ ] Plan library includes failure-handling plans for each major plan type (not just success paths)
- [ ] Belief update mechanism can handle contradictory information and propagate changes to active intentions
- [ ] Multiple intentions can be active concurrently with clear scheduling/preemption rules
- [ ] Event queue processing is prioritized (not FIFO) with explicit priority assignment
- [ ] Plan failure triggers events rather than system crashes or silent failures  
- [ ] Context guards are mutually exclusive OR plan selection is explicitly ordered to avoid non-determinism
- [ ] Agent can explain its actions by exposing intention stack and triggering events
- [ ] System performance degrades gracefully under high event load (no infinite loops or stack overflow)

---

## NOT-FOR Boundaries

**NOT FOR:** Simple rule-based systems where all behavior is reactive (no persistent goals)
→ **USE INSTEAD:** Basic rule engine or event-action system

**NOT FOR:** Static planning problems where environment doesn't change during execution  
→ **USE INSTEAD:** Classical planners (A*, STRIPS, HTN)

**NOT FOR:** Real-time systems requiring guaranteed response times or hard deadlines
→ **USE INSTEAD:** Real-time scheduling systems with timing analysis

**NOT FOR:** Systems where all coordination can be handled by a central controller
→ **USE INSTEAD:** Workflow orchestration or centralized task queuing

**NOT FOR:** Pure data transformation pipelines with no autonomous decision-making
→ **USE INSTEAD:** ETL tools, stream processing frameworks

**NOT FOR:** Applications requiring machine learning or statistical inference as primary capability
→ **USE INSTEAD:** ML frameworks with BDI as coordination layer if needed