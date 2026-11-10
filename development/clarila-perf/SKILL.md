---
name: clarila-perf
description: "Diagnose a specified performance problem or measure a candidate improvement with comparable evidence. Not an automatic optimization pass on unrelated code."
---

# Measure the actual bottleneck

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Define the metric, affected scenario, expected improvement and comparable source/environment/fixture.
2. Measure the baseline with appropriate profiling and repeated samples. Separate cold/warm, device, network and workload effects.
3. Locate the responsible bottleneck from traces. If repair is authorized, make the smallest supported change.
4. Measure the candidate using the same method and controls. Report sample size, variability and regressions rather than an unsupported percentage.
5. Retain traces, commands, source and environment, then return the measured result and limits.

For a comparison, keep the unit of work, input size, cache state, build mode and device class equal. Record the raw samples and chosen statistic, including its units. A faster warm run against a cold baseline is a different experiment. Report the mismatch and obtain comparable samples before calculating an improvement. Use the repository's profiler to connect the measured cost to the proposed change.

For Go benchmarks, the official [benchstat method](https://pkg.go.dev/golang.org/x/perf/cmd/benchstat) describes repeated A/B samples and statistical comparison. For mobile metrics, verify which launch/navigation metric and source cohort the official [Expo metrics reference](https://docs.expo.dev/eas/observe/reference/metrics/) actually measures.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read the private handoff described in the shared contract. When independently delegated, save an assessor-owned report and return it to the workflow owner for incorporation; do not compete to write the shared handoff. Otherwise update only the handoff you actually own using native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record. Use the current host’s native tools during the invoked workflow.

## Deliverable

Return baseline/candidate measurements, method, bottleneck, regression checks and uncertainty.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.
