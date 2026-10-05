---
name: product-tracking-audit
description: "Audit what telemetry a codebase actually emits, including event calls, identity handling, properties, and dead instrumentation. Use for analytics inventory, tracking audit, event census, what is currently tracked, or before changing product telemetry. Turkish triggers: ürün takibini denetle, event ve property sorunları, veri boşlukları ve kalite."
---

# Product Tracking: Audit Current Reality

Describe the current implementation before recommending changes. The audit is a factual census, not a scorecard.

## Workflow

1. Confirm the repository, branches, and directories in scope. Do not inspect production dashboards, credentials, or external accounts unless explicitly authorized.
2. Detect telemetry libraries and wrappers from dependencies and source calls without assuming a vendor.
3. For every event definition or call, record exact name, properties, location, trigger context, client/server boundary, and identity/group behavior.
4. Verify whether named event helpers have real call sites. Mark live, unused, or uncertain; do not guess from a definition alone.
5. Capture initialization, consent gates, opt-out/reset behavior, error handling, queue/flush behavior, and environment configuration by observation only.
6. Separate facts from hygiene observations. Recommendations belong in `product-tracking-plan`.

## Output

Return a concise summary plus a machine-readable inventory if requested:

```text
SDK or wrapper observed
Event inventory: name | location | trigger | properties | live status
Identity and organization context
Client/server routing
Observed naming and schema patterns
Unknowns, exclusions, and evidence locations
```

## Guardrails

- Preserve exact event/property names and casing.
- Never print keys, tokens, raw identifiers, or customer payloads.
- Do not install SDKs, alter source, or claim coverage is complete when generated code or unscanned modules remain.
- Hand off to `product-tracking-plan` only after the factual baseline is clear.
