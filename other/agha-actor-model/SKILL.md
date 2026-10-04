---
license: Apache-2.0
name: agha-actor-model
description: Foundational concurrent computation model where actors communicate exclusively through asynchronous message passing
category: Research & Academic
tags:
  - actor-model
  - concurrency
  - distributed-systems
  - message-passing
---

# SKILL.md — Agha Actor Model: Concurrent Agent System Design

## Decision Points

### Choosing Actor Creation Strategy Based on Task Type

```
IF task has sequential dependencies:
├─ Use customer pattern: create child with reply address
├─ Pass customer address to child as parameter
└─ Child sends result directly to customer (not parent)

IF task requires long computation:
├─ Create insensitive actor for computation
├─ Forward incoming messages to buffer actor
└─ Resume from buffer when computation completes

IF task needs dynamic resource allocation:
├─ Create resource manager actors on demand
├─ Pass capabilities (addresses) as message data
└─ No central registry - addresses flow through system

IF task has failure isolation requirements:
├─ Spawn supervised child actors for risky operations
├─ Supervisor detects failure via missing replies
└─ Replace failed actors without affecting others

IF composing existing agent systems:
├─ Verify interface preserves causal structure
├─ Test behavior under composition (not just isolation)
└─ Use message protocols as boundaries (not shared state)
```

### Message Sending vs State Replacement Decision Tree

```
IF coordination needed with other agents:
├─ SEND messages (don't modify local state first)
├─ Include reply address if response expected
└─ Never assume message ordering

IF local computation needed:
├─ SPECIFY replacement behavior
├─ Encapsulate new state (don't expose internals)
└─ Ensure one-message-at-a-time processing

IF dynamic scaling needed:
├─ CREATE new actors with specific behaviors
├─ Pass necessary addresses to new actors
└─ No shared initialization state
```

## Failure Modes

### 1. Central Orchestrator Anti-Pattern
**Detection**: If you see one actor routing all messages or holding all system state
**Symptoms**: Single point of failure, bottleneck under load, infinite regression problem
**Fix**: Decompose into community of actors, each knowing only local context, use capability routing

### 2. Synchronous Blocking Fallacy
**Detection**: If actors wait/block for responses instead of specifying replacement behavior
**Symptoms**: Deadlock under load, hidden timing assumptions, reduced concurrency
**Fix**: Model as request-reply message pairs, use customer pattern for dependencies, apply insensitive actor pattern

### 3. Shared State Contamination
**Detection**: If multiple actors read/write same data structure (even with locks)
**Symptoms**: Race conditions, sequential bottlenecks, hidden global state
**Fix**: Encapsulate state in single actor, use message passing for coordination, mutual exclusion is free

### 4. Output-Only Verification
**Detection**: If testing only compares final outputs without checking interaction patterns
**Symptoms**: Brock-Ackerman anomaly - identical outputs but different composition behavior
**Fix**: Verify causal structure preservation, test behavior under composition, use observation equivalence

### 5. Static Topology Assumption
**Detection**: If communication graph is fixed at startup with no runtime reconfiguration
**Symptoms**: Cannot handle open systems, no dynamic resource management, brittle under change
**Fix**: Treat addresses as first-class data, implement capability routing, support runtime topology changes

## Worked Examples

### Example 1: Task Decomposition with Customer Pattern

**Scenario**: Agent needs to process a complex request requiring sequential subtasks A → B → C, but must remain responsive to other messages.

**Novice Approach**: 
```
receive request →
  block while calling subtask A
  block while calling subtask B  
  block while calling subtask C
  send final result
```

**Expert Application of Actor Model**:
```
receive request →
  create customer_BC actor with addresses for B, C, final recipient
  send subtask A request to A_processor with customer_BC as reply address
  specify replacement behavior: ready for next request

customer_BC receives A result →
  send result to B_processor with customer_C as reply address
  
customer_C receives B result →
  send result to C_processor with final_recipient as reply address
```

**Key Decisions Made**:
- Used customer pattern to avoid blocking
- Each step creates next customer in chain
- Original agent remains responsive throughout
- Failure in any subtask only affects that chain

### Example 2: Failure Recovery with Supervision

**Scenario**: System needs to handle agent failures without cascading to whole system.

**Novice Approach**: Try-catch around agent calls, restart everything on failure.

**Expert Application**:
```
supervisor creates worker_actor →
  sends task to worker with reply timeout
  specifies replacement: "waiting_for_reply"

IF reply received within timeout →
  forward result to client
  specify replacement: "ready"

IF timeout expires →
  create new worker_actor (old one failed)
  resend task to new worker
  specify replacement: "waiting_for_reply"
```

**Trade-offs Navigated**:
- Supervision is separate concern from business logic
- Failed actors are isolated and replaced, not repaired
- Timeout detection vs guaranteed delivery balance
- No shared state between supervisor and workers

## Quality Gates

- [ ] No actor blocks its message processing loop (insensitive actor pattern applied where needed)
- [ ] All coordination uses message passing (no shared mutable state between actors)
- [ ] Message delivery is guaranteed but ordering is not assumed
- [ ] Addresses are treated as first-class data for capability routing
- [ ] Each actor specifies replacement behavior for every message type
- [ ] Actor creation happens dynamically based on computation needs
- [ ] Failure isolation prevents cascading failures across actor boundaries
- [ ] System topology can reconfigure at runtime without central registry
- [ ] Composition behavior verified, not just isolated component behavior
- [ ] Synchronous operations modeled as request-reply message pairs

## NOT-FOR Boundaries

**This skill should NOT be used for**:
- Simple sequential computations → use functional programming instead
- Systems where shared memory is physically required → use lock-based concurrency patterns
- Real-time systems with hard timing constraints → use synchronous message passing with formal timing analysis
- Mathematical computations without coordination → use pure functional approaches

**Delegate to other skills when**:
- Implementing specific actor frameworks → use platform-specific implementation guides
- Performance tuning actor systems → use [performance-optimization] skill
- Formal verification of actor properties → use [formal-methods] skill
- Database design for actor persistence → use [data-architecture] skill

**Common misconceptions about scope**:
- Actors are not just "objects with async methods" - they require the full 3-tuple response
- Actor model is not just for distributed systems - applies to any concurrent computation
- Not primarily a performance optimization - it's a correctness and compositionality framework