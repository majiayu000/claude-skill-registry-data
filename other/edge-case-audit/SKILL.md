---
name: edge-case-audit
description: Analyze safety-critical boundaries, coupled failure modes, resilience risks, and trading edge cases.
when_to_use: >
  Use for edge cases, boundaries, failure modes, retries, timeouts, race conditions,
  graceful degradation, resilience reviews, and safety-critical trading behavior.
---

### Activation

Trigger this skill whenever the conversation references:

- “edge case”, “corner case”, “boundary condition”, “rare failure”, “what if X happens”
- retry logic, timeout handling, idempotency, exactly-once semantics, circuit breakers
- graceful error recovery, fallback paths, or “it recovered so we’re fine”
- post-mortem, incident review, chaos engineering, or production stress testing
- any mention of clock skew, leap seconds, network blips, DNS, GC pauses, lock contention, or correlated failures across “independent” components.

If none of the above appear, remain silent. Once activated, stay active for the remainder of the reasoning session.

### Expert Salience

Load-bearing features (in descending order of weight):

1. **Shared triggering conditions** over marginal individual rarity — joint probability is governed by common cause, not multiplication of independent probabilities.
2. **Temporal coupling & causal ordering** (happens-before relations, logical clocks) — any assumption of ordering that does not exist in the execution model.
3. **Invariant erosion & safety-margin drift** — normalisation of deviance after “graceful” recoveries.
4. **Feedback-loop instability** — retry amplification, queue phase transitions, control-loop oscillations.
5. **Hidden state divergence** — cache poisoning, stale locks, unreconciled replicas, delayed downstream effects.
6. **Correlated anomalies across subsystems** within a narrow time window — these are diagnostic of a common excitation point.

Ignore isolated input validation or single-component unit-test pass rates unless they are explicitly linked to one of the above signals.

### Mental Models

- **Common-Cause / Coupled-Failure Reasoning** [GROUNDED]: Rare conditions are rarely independent; they are coupled through shared stressors (network fate, clock events, contention, physical environment).  
- **Invariant Stress Testing** [GROUNDED]: Continuously probe whether system invariants hold under simultaneous stressors that real-world coupling can produce.  
- **Silent Degradation Detection** [GROUNDED]: Apparent recovery is provisional evidence only; measure post-recovery baseline drift in resources, state, and latency.  
- **Lamport’s Happens-Before & Logical Clocks** [USER-GROUNDED]: Track causal order explicitly; concurrent events expose assumed ordering that does not exist.  
- **Safety Margin Erosion (Reason’s DRIFT / normalisation of deviance)** [USER-GROUNDED]: Systems drift toward catastrophe; each “successful” recovery reduces remaining margin.  
- **Queueing-Theoretic Instability (Little’s Law, Kingman’s formula, phase transitions)** [USER-GROUNDED]: Retries and timeouts create positive feedback that turns rare edges into normal behaviour.  
- **Byzantine Fault Tolerance Reasoning** [USER-GROUNDED]: Assume components can behave arbitrarily (lie, replay, produce subtly wrong outputs) for brief correlated windows.  
- **Control Theory for Feedback Loops** [USER-GROUNDED]: Recovery mechanisms are controllers; look for integrator windup, oscillations, and instability.  
- **Snapshot Isolation & Serialisability Anomalies** [USER-GROUNDED]: Under contention, write skew, phantom reads, and causal reversals become probable.

### Thinking Rules

- Treat every passing test or graceful error as provisional evidence only; the expert always asks “what hidden state corruption or causal violation might this recovery have masked?” [GROUNDED]  
- When two edge cases appear independent, first search for the shared trigger that can make them co-occur deterministically. [GROUNDED]  
- Prioritise systemic invariants over local component correctness. [GROUNDED]  
- Normalisation of deviance after recovery is the most dangerous signal in the system. [USER-GROUNDED]  
- Clock, network, and contention events are universal coupling agents; design diversity and explicit causal checks are the only reliable mitigations. [USER-GROUNDED]

### Decision Heuristics

- If you observe any two or more anomalies (retries, GC pauses, 5xx spikes, lock contention) starting inside the same 100–500 ms window → immediately treat them as coupled and initiate invariant stress testing.  
- If post-recovery metrics (connections, heap, file descriptors, queue lengths) do not return to exact baseline within 30 s → escalate to committed audit.  
- When retry budget is burning at an accelerating rate despite half-open circuit breakers → force synthetic oscillation and observe the limit cycle.  
- When error logs contain “unordered”, “sequence mismatch”, “duplicate detected but no action”, or any causal language → trigger full Lamport-clock causal consistency audit.

### Commitment Thresholds

Commit to irreversible actions (architectural changes, deeper invariant probes, production stress testing, or quarantine) **if and only if** one or more of the following signals of dynamic instability or state drift are observed:  

- latent resource drift after recovery,  
- retry amplification with non-convergence,  
- divergent internal state across replicas,  
- correlated anomalies across unrelated subsystems within a narrow time window,  
- error messages containing causal or ordering language.  

Until these signals appear, remain provisional and continue diagnostic sequencing. If the commitment_threshold signals are absent, name the exact additional evidence required before escalation (e.g., “we still need a post-recovery state checksum divergence or retry amplification metric”).

### Anti-Patterns

- **Independence Fallacy** (primary) [GROUNDED]: Dismissing compound failures as “astronomically unlikely” without first testing whether a single shared stressor can trigger them together.  
- Treating “it recovered” or “tests passed” as conclusive proof of safety.  
- Performing only isolated boundary-value testing instead of coupled invariant stress testing.  
- Ignoring normalisation of deviance after graceful recovery.  
- Assuming ordering, monotonicity, or exactly-once semantics without explicit causal verification under real coupling conditions.  
- Continuing observation alone when contamination-model evidence suggests state corruption may be spreading.

### Uncertainty Handling

- Default stance: passing tests and graceful errors are provisional evidence only.  
- When recovery is reported, execute the fixed diagnostic sequence (snapshot → causal-order check → cache probe → stale lock scan → retry anomaly scan → downstream projection) before accepting “recovered”.  
- Maintain a contamination model: if any component’s state is suspect, treat every downstream component that has interacted with it since the incident as suspect until proven otherwise.  
- When domain context is unknown, first ask “what is the dominant coupling agent in this ecosystem?” (network, time/clock, physical environment, contention) and re-weight rarity conditional on that agent.  
- If evidence is ambiguous, force the smallest possible invariant stress test that can falsify the current mental model rather than accumulate more passive observation.

### Examples of Judgment

**Example 1 – DNS Timeout Cascade (Independence Fallacy)**  
Observation: Payment failures spike across “independent” services; monitoring flags the payment provider.  
Expert weighting: Correlate exact onset timestamps with DNS query failures → discover shared DNS cache TTL window synchronised the retries → recognise common-cause retry storm.  
Action taken: Synthetic DNS blip + partition test during load; added per-resolver circuit breakers and jittered retry backoff. Joint risk moved from “negligible” to “deterministic under brief network event”.

**Example 2 – Leap-Second HLC Rollback**  
Observation: Distributed DB experiences silent split-brain with data loss during a known leap-second window.  
Expert weighting: Leap second is a deterministic common-mode event affecting all nodes simultaneously; partition is now conditional on that window → HLC monotonicity must be hardened against clock slew.  
Action taken: Leap-second fire-drill injecting partition + NTP slew; added explicit HLC safety checks and fallback to wall-clock + logical clock hybrid with strict monotonicity enforcement.

### Grounding Notes

All sections are STRONGLY GROUNDED in the principal reliability engineer’s provided expertise description, real-world patterns, diagnostic sequences, and mental models (USER-GROUNDED). Additional TYPE-R grounding from NRC Common-Cause Failure guidance and Chaos Engineering / SRE cascading-failure literature. No claims are inferred. This skill encodes the exact expert salience function requested: coupled temporal phenomena, common-cause weighting, provisional-evidence stance, and explicit correction of the Independence Fallacy.
