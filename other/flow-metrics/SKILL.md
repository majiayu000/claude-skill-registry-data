---
name: flow-metrics
description: Measure iterative delivery flow using throughput, lead/cycle time, work age, work in progress, blocked time, and predictability without turning metrics into individual performance scores.
---
# Flow Metrics

Use when a team wants evidence about how work moves through its system and where delivery friction accumulates.

## Procedure
1. Define the work-item boundaries and state transitions used for measurement so lead/cycle time and age are interpretable.
2. Track throughput over consistent windows and segment materially different work types when one aggregate hides behavior.
3. Measure cycle or lead-time distributions, including percentiles or ranges rather than averages alone.
4. Track work-in-progress and age of active items to expose accumulating queues and stale work.
5. Measure blocked/wait time separately where dependencies or approvals materially affect delivery.
6. Examine variability and predictability over time before treating a single fast or slow iteration as a trend.
7. Correlate flow changes with process, scope, incident, staffing, tooling, or dependency changes before asserting cause.
8. Use the metrics to test team-level process hypotheses and capacity decisions, then review whether interventions changed the expected signal.

## Decision rules
- Flow metrics describe the work system, not individual developer productivity.
- Averages can hide long-tail work.
- Higher throughput is not automatically better if quality or outcome declines.
- Avoid gaming by keeping definitions stable and pairing speed with quality evidence.

## Quality gate
The metrics are useful when definitions are explicit, distributions and aging reveal real flow behavior, blocked time and WIP are visible, quality is considered, and the team can use the evidence to test process changes without turning metrics into surveillance.