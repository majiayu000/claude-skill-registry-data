---
name: firmware-pattern-validation
description: Use when a draft pattern may be promoted to the firmware memory layer.
---

# Firmware Pattern Validation

## Overview

Validate firmware discovery pattern drafts before memory promotion. This skill is part of the discovery-first firmware research suite for authorized binary/service exploitability assessment. It preserves blocker-first workflow, compact local evidence, and provenance-first claims.

## Routing

```yaml
role: update
purpose: Validate firmware discovery pattern drafts before memory promotion.
when_to_use:
  - Use when a draft pattern may be promoted to the firmware memory layer.
when_not_to_use:
  - Do not validate drafts that lack source evidence, exact verified_on date, or sensitivity classification.
required_inputs:
  - memory_draft.md
  - source artifact references
  - evidence labels
produces:
  - pattern_validation.json
  - memory_promotion_decision.json
completion_gate:
  - Decision is valid, needs_more_evidence, too_product_specific, unsafe_to_promote, or stale_or_contradicted with reasons.
reentry_triggers:
  - Re-enter when new evidence resolves a validation blocker.
handoff_hints:
  - Return valid patterns to firmware-memory-layer for promotion.
misuse_signals:
  - The skill is being misused if it approves behavior claims without runtime or verified evidence.
```

## Required Superpowers

- Use `superpowers:systematic-debugging` when validation fails unexpectedly.
- Use `superpowers:verification-before-completion` before claiming an artifact is valid.

## Inputs

- memory_draft.md
- source artifact references
- evidence labels

## Workflow

1. Validate provenance and source availability.
2. Check for secrets and over-specific product assumptions.
3. Compare claimed behavior to evidence labels.
4. Write a promotion decision with blockers when needed.

Always use `firmware-artifact-contract` before trusting shared artifacts. Every JSON output must include `schema_version`, `generated_at`, `generated_by`, `source_inputs`, `warnings`, and `errors`. Use `missing_tool` warnings or blockers when required tooling is unavailable. Static evidence, sandbox_generated evidence, Qiling-only output, and public writeups are not runtime truth; keep behavior_claim_allowed=false unless observed_runtime_qemu, observed_runtime_live_hook, observed_runtime_live_debugger, or verified evidence proves the target workload was observed.

## Session Continuation

Treat same-session follow-up prompts about the current firmware artifact as continuation signals. Resume from the latest artifact index, hypothesis ledger, next_skill_decision.json, or blockers.json instead of waiting for the user to invoke the skill again explicitly.

## Loop Guard

Do not repeat the same failing action, validation, probe, or handoff when inputs and artifacts have not changed. If the same blocker appears twice, write or update blockers.json with the repeated blocker, stop and ask the user for the missing input or decision. Prefer a lower-cost evidence-gathering step only when it changes the artifact state.

## Outputs

- `pattern_validation.json`
- `memory_promotion_decision.json`

## Verification Gate

Do not mark this skill complete until outputs satisfy the routing completion gate and the artifact contract. Evidence levels must progress from E0 to E8 without skipping runtime or duplicate-check gates. `verification-before-completion` is required before claiming a result is valid.

## Safety

Operate only on firmware and runtimes the user is authorized to test. Keep destructive probes disabled by default; record runtime modifications; prefer local evidence and redacted summaries; use exact dates and versions in vulnerability reports; do not install tools without explicit user approval. Do not commit firmware, secrets, proprietary dumps, raw traces, or private vendor material. Do not mass target devices, do not scan public IPs, do not build a weaponized exploit generator, and do not invent CVE IDs.

## Common Mistakes

- Approving stale patterns.
- Promoting unsafe probe recipes.
- Confusing a one-off product quirk with a reusable pattern.
