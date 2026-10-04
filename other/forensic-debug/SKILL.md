---
name: forensic-debug
description: >
  Activate for forensic debugging of software systems when symptoms indicate
  violated invariants, contradictory evidence, unreliable logs, production
  incidents, Heisenbugs, or causal timeline reconstruction.
when_to_use: >
  Use for persistent or contradictory failures, production incidents, regression
  root-cause analysis, violated invariants, Heisenbugs, or causal timeline
  reconstruction; avoid using for simple one-step bugs.
---

# Activation

Invoke this skill immediately upon any of the following:

- A production incident, post-mortem, or on-call alert where the observed symptom does not match expected system behavior.
- Any report of a violated invariant (null pointer, data corruption, race condition, split-brain, unexpected state transition).
- When logs, metrics, return codes, dashboards, or test results appear to conflict or tell an incomplete story.
- When the team is stuck in symptom-chasing or storytelling mode rather than causal reconstruction.

# Expert Salience

Load-bearing features (in strict priority order):

1. **The violated invariant** — the single most important signal. It is the anchor point for all reconstruction. [USER-GROUNDED]
2. **Authoritative source-of-truth state** — the last known-good state and the first observed bad state. [USER-GROUNDED]
3. **Provenance and authenticity of every artifact** — treat every log line, metric, trace, or core dump as a fallible claim until chain-of-custody is proven. [USER-GROUNDED]
4. **Happens-before causal ordering** — not wall-clock timestamps. [USER-GROUNDED]
5. **Absence of evidence** (missing logs, flatlined heartbeats, gaps in sequence numbers) — these are often the loudest signals. [USER-GROUNDED]
   Ignore or heavily discount: dashboard summaries, single-source logs, “it worked in staging,” and any narrative that lacks a mechanistic explanation of the exact state transition.

# Mental Models

- **Source-of-Truth State Transition Reconstruction**: Treat the system as a state machine. Recover the exact before → after transition graph using multiple independent sensors. Never trust a single source; cross-validate across application logs, kernel audits, network captures, hardware counters, distributed traces, and peer-service views. Visualize as a timeline with lanes per actor; mark inferential leaps explicitly. [USER-GROUNDED]
- **CSI-Style Evidence Provenance**: Every artifact is physical evidence with chain-of-custody. Verify origin, integrity, temporal authenticity, and corroboration. Use sequence numbers, epoch IDs, generation counters, and meta-logs (log rotation, OOM killer, systemd journals) to authenticate. [USER-GROUNDED]
- **Differential Diagnosis via Falsifiability**: Generate multiple competing hypotheses and actively seek disconfirming evidence for each. For every hypothesis, define the observation that would kill it. Prioritize falsification tests because they are faster and more decisive than confirmation. [USER-GROUNDED]
- **Happens-Before Reconstruction**: Reconstruct true causal order using logical clocks, vector clocks, message ordering, mutex acquisitions, and side-channel information. Swimlane diagrams with causal arrows; enumerate every possible writer (threads, interrupts, DMA, firmware, remote nodes). Timestamps are suggestions only. [USER-GROUNDED]

# Thinking Rules

- Debugging is controlled reconstruction of a state transition under uncertainty, not storytelling. [USER-GROUNDED]
- The system always tells the truth; our job is to learn to listen properly by authenticating every claim against an independent source-of-truth. [USER-GROUNDED]
- Every hypothesis must name the exact observation that would falsify it. [USER-GROUNDED]
- Start every investigation from the violated invariant and work outward. [USER-GROUNDED]
- Claim-verdict conflation is the cardinal sin: logs, metrics, return codes, and dashboards are claims, never verdicts. [USER-GROUNDED]

# Decision Heuristics

Condensed expert operating loop (apply in order):

1. State the violated invariant.
2. Identify the authoritative source of truth.
3. Capture before/after state.
4. Enumerate all possible writers or causal actors.
5. Authenticate evidence provenance.
6. Reconstruct happens-before order.
7. Maintain multiple falsifiable hypotheses.
8. Seek disconfirming evidence.
9. Explain affected and unaffected cases.
10. Commit root cause only when the causal chain survives adversarial testing.
11. Verify the fix against the invariant, not against symptom disappearance. [USER-GROUNDED]

If evidence is contradictory, default to causal ordering over timestamps and demand a third independent witness.

# Commitment Thresholds

Commit to a root-cause declaration **only** when **all** of the following are satisfied (mechanistic completeness + falsification resilience + independent corroboration + counterfactual success):

- There is a concrete, step-by-step mechanistic explanation that accounts for **every** observed symptom (including initial red herrings) and the exact code paths, timing, and state values.
- The hypothesis has survived multiple aggressive falsification attempts; alternative hypotheses have been eliminated.
- At least two independent sources of evidence directly support the mechanism.
- Ideally, a smoking-gun artifact (race-detector trace, hardware watchpoint, audit log) captures the causal moment.
- The proposed fix, when applied (or reverted), eliminates the failure under identical conditions.
- No anomalous residuals remain.

If any item above is missing, remain provisional and gather more data. [USER-GROUNDED]

# Anti-Patterns

- **Claim-verdict conflation**: Treating logs/metrics/dashboards/return codes as truth instead of fallible claims. [USER-GROUNDED]
- **Anchoring on the last change** (or any single temporal correlation) without proving mechanism.
- **Symptom-chasing**: Fixing the crash without fixing the root cause that produced the bad state.
- **Tool bias**: Trusting debugger output without understanding its limitations or observer effects.
- **Single-layer fallacy**: Assuming the bug lives in the application layer when it could be runtime, kernel, hypervisor, or hardware.
- **Absence blindness**: Ignoring missing logs, flatlined heartbeats, or gaps in sequence numbers.
- **Storytelling**: Asking “what story fits the evidence?” instead of “what evidence would force this explanation to be true or false?”
- **Mitigation trap**: Restoring service without first preserving forensic state (cores, traces, logs). [USER-GROUNDED]

Domain-specific:

- Distributed systems: Assume split-brain by default; treat timestamps as suggestions.
- Kernel/driver: Assume corruption can come from anywhere (DMA, interrupts); use page_owner/watchpoints.
- Production: Drill into per-request error budgets; never dismiss anomalies.

# Uncertainty Handling

- Apply the Law of Multiple Witnesses: require independent sources with different failure modes.
- Use Consilience of Inductions: prefer the explanation that accounts for the widest range of observations.
- Treasure anomalies; never explain them away as glitches.
- Default to causal ordering (happens-before, logical clocks) over wall-clock time.
- Be aware of the Observer Effect: debugging tools can hide races (Heisenbugs).
- Assume the system obeyed physics and its own rules; if a transition seems impossible, your evidence reconstruction is wrong. [USER-GROUNDED]
- When evidence conflicts, explicitly model uncertainty and defer commitment until a third witness resolves ordering.

# Examples of Judgment

**Phantom Network Timeout**  
Violated invariant: “A request should be sent to the provider within 100 ms of acceptance.”  
Logs claimed provider timeout, but trace showed the request never left the client for 2 seconds (thread-pool exhaustion). Expert down-weighted the log line, up-weighted absence of provider-side delay and thread-dump evidence, ran falsification load test, and committed only after revert eliminated the issue. [USER-GROUNDED]

**Kernel Memory Corruption**  
Violated invariant: “A buffer handed to the block layer must remain mapped until IO completes.”  
Page fault looked like filesystem bug. Expert set hardware watchpoint on page-table entry, discovered network driver DMA teardown race. Used page_owner to prove writer, disabled interrupt to falsify, and confirmed root cause. [USER-GROUNDED]

# Grounding Notes

All sections above are directly [USER-GROUNDED] from the expert operating loop, mental models, examples, commitment criteria, epistemic principles, and anti-patterns supplied in the query and clarifying response. Structural frontmatter and validation rules are [GROUNDED] in the attached Skill Wizard authoring document.
