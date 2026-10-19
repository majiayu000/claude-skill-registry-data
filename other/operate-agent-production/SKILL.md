---
name: operate-agent-production
description: Instrument, operate, and optimize a production agent. Use when adding OpenTelemetry tracing, dashboards, alerts, SLOs, privacy controls, token and spend budgets, model routing, context reduction, caching, retry controls, or incident diagnostics.
---

# Operate a Production Agent

Make agent behavior observable and cost-bounded without exposing sensitive content.

## Workflow

1. Define service-level objectives for success, hard-gate safety, latency, availability, and cost per successful task.
2. Establish one trace hierarchy from entry point through durable workflow and durable step (when used), agent run, model request, and tool call.
3. Attach stable correlation fields: agent, prompt, model, dataset or release, workflow, capability, tenant or environment, and outcome versions.
4. Record tokens, latency, retries, tool calls, cache behavior, failures, and estimated cost at the narrowest useful scope.
5. Apply redaction, hashing, allowlisting, sampling, access control, and retention before exporting telemetry. Treat prompts and tool payloads as sensitive by default.
6. Create dashboards for quality, safety, reliability, latency, and spend. Alert on user-impacting symptoms and budget burn, not raw event volume alone.
7. Set per-run and aggregate limits for tokens, model calls, tool calls, retries, wall time, and spend. Define graceful behavior when a limit is reached.
8. Optimize in evidence-driven order: remove unnecessary calls, shrink context and tool outputs, route simpler work to smaller models, cache stable results, then tune retries and concurrency.
9. Re-run quality, safety, latency, and cost evals after every optimization.
10. Document rollback signals and ownership.

Read [the operations standard](references/standard.md) before defining telemetry or budgets. Use [the examples](references/examples.md) for trace fields, alerts, and cost controls.

## Guardrails

- Do not place secrets, raw credentials, or unrestricted prompt content in spans.
- Do not optimize token cost while ignoring retries, tool infrastructure, or failed-run cost.
- Do not use sampling that can hide all high-risk failures.
- Do not route to a cheaper model without eval evidence for that route.
- Do not set a budget without specifying the user-visible exhaustion behavior.

## Completion Check

An operator must be able to diagnose one failed task end to end, quantify cost per successful task, detect an SLO breach, identify the responsible version, and execute a documented rollback.
