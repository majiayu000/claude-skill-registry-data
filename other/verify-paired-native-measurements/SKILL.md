---
name: verify-paired-native-measurements
description: "Audit the process, sample and archive evidence behind paired native benchmarks, especially wrappers around an unchanged official client. Use before admitting benchmark results or when reviewing the controller that produced them. Ordinary unit tests do not need this."
---

# Zwillingswaag (verify-paired-native-measurements)

Bind the conclusion to the declared experiment, exact native artifacts and actual retained evidence. Local comparisons do not establish an official score or promotion. This skill adds no execution, provider, spending or submission authority. Use the existing mission and its canonical Mission Command policy when applicable.

## Admission boundaries

- Preserve the official client's ordering, sample counts, timing endpoints and statistic definitions when that is the experiment's contract. Disclose wrapper overhead included inside those endpoints; do not silently subtract it or claim equivalence to the bare client.
- Enforce elapsed limits with a monotonic clock and separately enforce absolute work/grant deadlines. Carry remaining limits across process boundaries. A wall-clock rollback must not authorize a new subprocess after the elapsed cap. Include preparation, verification and finalization in whichever caps the declared design assigns them.
- Across machines, monotonic timestamps have unrelated origins. Keep the controller's original budget start and bind a separate worker clock/boot observation. Transfer a conservatively reduced remaining duration; never compare the raw clocks or restart the allowance at worker launch. A declared end-to-end cap also covers the final local readback. See [cross-host budgets](references/cross-host-budgets.md) when designing that boundary.
- Validate every retained complete run, including warmups. Exclusion from statistics does not waive positive time/RSS, correctness, byte identity or other declared evidence requirements.
- Reconstruct the exact conditional phase progression. A passing prefix with missing successor phases is incomplete. A completed early stop requires the declared failed gate and corresponding terminal decision. Recompute the gate from rows rather than trusting its stored label.
- Retain the direct parent's actual child wait status and raw streams. Worker success or process disappearance cannot replace an unavailable supervisor exit. Bind PID/start identity when process IDs may be reused.
- Distinguish pre-archive snapshots from final terminal sidecars. Validate the implementation's actual status transition instead of either accepting a stale success label or requiring fields saved at different phases to be identical.
- Snapshot the exact expected receipt bytes before use. Verify the compressed archive, every declared member, and the fresh restore. Recheck the same compressed identity after semantic validation and at successful publication. Emit the identity actually validated. A newly computed unchecked hash is not provenance.

Use focused counterexamples at actual admission boundaries. [Observed failure cases](references/failure-cases.md) give four useful examples; adapt them to the declared experiment rather than importing its historical counts or thresholds.

Preserve failed evidence. Missing exits, truncated archives, timeouts and incomplete phases close admission; they do not by themselves refute the candidate algorithm.
