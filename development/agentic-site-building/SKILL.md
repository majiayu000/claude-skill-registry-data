---
name: agentic-site-building
description: Design, implement, or harden an AI website-building agent that turns natural-language requests into scoped code changes with planning, structured edits, deterministic verification, bounded repair, safe previewing, version history, and token-aware model routing.
---

# Agentic Site Building

Build editing systems that can prove a requested change happened without rewriting unrelated work or claiming success on a no-op.

## Workflow

1. Map the editable artifact, source of truth, preview boundary, model providers, persistence, and rollback path.
2. Compile each request into an explicit contract: mode, target surface, allowed change radius, acceptance criteria, and risk.
3. Prefer a structured patch for an existing artifact. Require exact, unique anchors and a bounded change budget.
4. Apply patches locally, then validate syntax, structure, requested-surface change, and collateral-change limits.
5. If validation fails, give the verifier evidence to one bounded repair attempt. Escalate to a full rewrite only when scope requires it or patching is unsafe.
6. For redesigns, reject the current composition deliberately while preserving factual content and product constraints.
7. Render generated code in an isolated preview. Keep authentication, storage, parent DOM, and privileged network access outside the generated runtime.
8. Save only accepted outputs. Keep restorable revisions with prompt, mode, verifier result, and prompt/model version.
9. Expose honest progress and failure states. Never label an unchanged or unverified preview as updated.
10. Measure patch success, no-op rate, repair rate, latency, token cost, rollback rate, and user acceptance.

## Decision Rules

- Deterministic code owns safety and common runtime contracts; the model owns interpretation and creative composition.
- A small edit should not receive the full site unless the patch path fails safely.
- Verification must inspect the requested surface, not only whole-file similarity.
- Retries must use new evidence and stop after a fixed budget.
- Provider fallback handles availability; it must not silently weaken required structured-output or context capabilities.
- Keep generated code facts grounded in user data. Do not invent projects, metrics, employers, or media.

## Delivery Contract

Provide or implement:

1. **Execution contract** - modes, scope, acceptance criteria, and escalation rules.
2. **Orchestration path** - plan, patch or build, validate, repair, persist, preview, rollback.
3. **Verifier design** - deterministic checks and evidence returned to repair attempts.
4. **Safety boundary** - generated-code sandbox and authorization limits.
5. **Efficiency budget** - context selection, model routing, retries, and stopping conditions.
6. **Operational proof** - tests for no-op, collateral edit, failed patch, retry, rollback, and preview isolation.

## Reference

Read [references/orchestration-contract.md](references/orchestration-contract.md) when defining schemas, retry policy, or production metrics.
