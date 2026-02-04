---
name: hypothesis-debugging
description: Structured code debugging through hypothesis formation and falsification planning. Use when diagnosing bugs, unexpected behaviour, or system failures where the root cause is unclear. Produces a hypothesis document for execution by another agent rather than performing the investigation directly. Triggers on requests to debug issues, diagnose problems, investigate failures, or create debugging plans.
---

# Hypothesis-Driven Debugging

Generate a structured debugging document that identifies candidate root causes and provides falsification plans for each. The output document instructs a separate execution agent; do not perform the investigation yourself.

## Philosophical Foundation

Apply Popperian falsificationism: hypotheses cannot be proven true, only disproven. Design tests that could definitively rule out each hypothesis rather than confirm it. A good falsification test produces a clear negative result if the hypothesis is wrong.

## Process

### 1. Gather Context

Before forming hypotheses, collect:

- **Symptom description**: What behaviour is observed vs expected?
- **Reproduction conditions**: When does it occur? Intermittent or consistent?
- **Recent changes**: Deployments, configuration changes, dependency updates
- **Error artefacts**: Stack traces, logs, error messages, screenshots
- **Environmental factors**: OS, runtime versions, network conditions

If information is missing, note gaps in the output document.

### 2. Form Hypotheses

Generate 1–5 hypotheses ranked by plausibility. Each hypothesis must be:

- **Specific**: Name the component, function, or interaction suspected
- **Falsifiable**: A concrete test could disprove it
- **Independent**: Falsifying one should not automatically falsify others

Common hypothesis categories:

| Category | Examples |
|----------|----------|
| State | Race condition, stale cache, corrupted data |
| Input | Malformed payload, encoding issue, boundary case |
| Environment | Missing dependency, version mismatch, resource exhaustion |
| Logic | Off-by-one, incorrect predicate, missing null check |
| Integration | API contract violation, timeout, auth failure |

Avoid vague hypotheses ("something wrong with the database"). Pin down the specific failure mode.

### 3. Design Falsification Plans

For each hypothesis, specify:

1. **Prediction**: If this hypothesis is correct, what observable outcome follows?
2. **Falsification test**: What action would produce a contradicting observation?
3. **Expected negative result**: What outcome would disprove the hypothesis?
4. **Tooling required**: Commands, scripts, or instrumentation needed
5. **Confidence impact**: How decisively would a negative result rule this out?

Prefer tests that are:
- Quick to execute
- Minimally invasive
- Deterministic rather than probabilistic

### 4. Output Document

Generate a Markdown document following the template in `assets/debugging-plan.md`. Save to the working directory as `debugging-plan-{timestamp}.md`.

## Quality Criteria

A well-formed debugging plan exhibits:

- **Mutual exclusivity**: At least one hypothesis should survive if others fail
- **Collective exhaustiveness**: Hypotheses cover the likely failure space
- **Ordered efficiency**: Cheapest decisive tests appear first
- **Clear success criteria**: The executing agent knows when to stop

## Anti-Patterns

- Confirmation bias: Designing tests that can only succeed, not fail
- Hypothesis creep: Adding new hypotheses during execution rather than revision
- Coupling: Tests that cannot isolate individual hypotheses
- Vagueness: "Check the logs" without specifying what pattern would falsify

## References

- `references/examples.md`: Worked examples of hypothesis-falsification pairs across common debugging scenarios (API timeouts, flaky tests, memory leaks)
