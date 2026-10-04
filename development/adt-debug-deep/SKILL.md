---
name: debug-deep
description: Composite skill — full debugging workflow from "this is broken" to root cause and fix. Chains systematic-debugging (root-cause hypotheses) → tracer agent (evidence walk) → sentry (production correlation if applicable) → ci-watch (regression check) → incident-response (if production-impacting). Use when a bug needs deep investigation, not just a quick fix.
triggers:
  - debug-deep
  - complex-bug-reports
  - production-incidents
  - recurring-failures
  - composite skill
  - debug
---

# Debug Deep

The full investigation workflow. Replaces "OK try X, now try Y, hmm let me check Sentry"
with one chained skill that gathers evidence systematically.

## Auto-invocation triggers

- User reports a bug they've already tried to fix once
- Bug report mentions "intermittent", "sometimes", "in production but not local"
- Sentry / error monitoring shows the same issue 3+ times
- CI failure pattern matches a recurring class
- User says "this is broken, find why"

## Workflow

### Phase 1 — Hypothesis tree (always)
Invoke `systematic-debugging` to build a hypothesis tree with evidence-for/against
columns. No fixes yet — just structured root-cause analysis.

### Phase 2 — Evidence walk (always)
Invoke `tracer` agent (via Agent tool, subagent_type=tracer) to walk the call paths
and collect concrete evidence per hypothesis. Tracer ranks hypotheses by evidence
weight and recommends next probes.

### Phase 3 — Production correlation (if production-impacting)
Invoke `sentry` to query for matching error signatures in the last 30 days. Look for:
- Frequency trend (rising / steady / one-off)
- Affected users / orgs / environments
- Stack trace overlap with the local repro

If production data contradicts the hypothesis tree → loop back to Phase 1 with the
new evidence.

### Phase 4 — Regression check (always)
Invoke `ci-watch` to find when the failure first appeared in CI history. Bisect to
the introducing commit if linear history allows. Cross-reference with the hypothesis
tree's "introduced when" entries.

### Phase 5 — Fix (autonomous if hypothesis is high-confidence)
Once the tree converges on one hypothesis with strong evidence:
- For local-scope fixes: implement directly via Edit
- For cross-module fixes: invoke `refactor-pipeline`
- For production-impacting fixes: invoke `incident-response` to coordinate the fix
  with rollback plan, comms, and post-mortem

### Phase 6 — Capture (always)
- Invoke `adr-write` if the bug revealed a structural issue worth recording
- Add a regression test (don't skip — that's how the bug comes back)
- Invoke `knowledge-loop` to capture the debugging path for next time

## Reconciliation

```
DEBUG DEEP — <bug summary>
  Phase 1 Hypotheses:    N candidates ranked
  Phase 2 Evidence:      <strongest hypothesis, confidence>
  Phase 3 Production:    <Sentry frequency, affected scope>
  Phase 4 Regression:    introduced in commit <SHA> (<date>)
  Phase 5 Fix:           <commit / PR / incident ref>
  Phase 6 Captured:      <ADR path, regression test path>
```

## Outputs / Evidence

- Hypothesis tree (Phase 1)
- Evidence collected per hypothesis
- Sentry frequency data
- Bisect result
- Fix commit/PR
- Regression test
- ADR if structural

## Failure / Stop Conditions

- Hypothesis tree has zero high-confidence winners after Phase 2 → stop, do not
  guess; surface the tree to user with recommended next probes
- Sentry inaccessible → continue without Phase 3, mark report as PARTIAL
- Bisect not viable (force-pushed history) → skip Phase 4, rely on hypothesis tree
- Production fix without rollback plan → block; require incident-response
