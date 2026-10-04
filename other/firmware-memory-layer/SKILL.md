---
name: firmware-memory-layer
description: Use when validated local artifacts suggest a reusable exploitability, surface, parser, sink, crash, reachability, hook, debugging, or false-positive pattern.
---

# Firmware Memory Layer

## Overview

Suggest, draft, validate, and promote reusable firmware discovery patterns without modifying core skill behavior. This skill is part of the discovery-first firmware research suite for authorized binary/service exploitability assessment. It preserves blocker-first workflow, compact local evidence, and provenance-first claims.

## Routing

```yaml
role: update
purpose: Suggest, draft, validate, and promote reusable firmware discovery patterns without modifying core skill behavior.
when_to_use:
  - Use when validated local artifacts suggest a reusable exploitability, surface, parser, sink, crash, reachability, hook, debugging, or false-positive pattern.
when_not_to_use:
  - Do not use to promote unverified behavior claims or to silently change orchestrator rules, safety boundaries, artifact contracts, evidence ladder, or core SKILL.md files.
required_inputs:
  - validated artifact
  - pattern draft
  - source evidence
  - artifact sensitivity label
produces:
  - memory_suggestions.json
  - memory_draft.md
  - promotion_decision.json
completion_gate:
  - Draft has exact verified_on date, source artifacts or URLs, no secrets, and runtime evidence for behavior claims.
reentry_triggers:
  - Re-enter after a candidate is root-caused or after a validation decision requests more evidence.
handoff_hints:
  - Send drafts to firmware-pattern-validation before promotion.
misuse_signals:
  - The skill is being misused if it stores conversation memory instead of durable validated patterns.
```

## Required Superpowers

- Use `superpowers:systematic-debugging` when validation fails unexpectedly.
- Use `superpowers:verification-before-completion` before claiming an artifact is valid.

## Inputs

- validated artifact
- pattern draft
- source evidence
- artifact sensitivity label

## Workflow

1. Read current artifacts and suggest only relevant memory.
2. Capture new observations as draft-before-promote patterns.
3. Validate drafts before activation.
4. Require human review for core behavior or safety changes.

Always use `firmware-artifact-contract` before trusting shared artifacts. Every JSON output must include `schema_version`, `generated_at`, `generated_by`, `source_inputs`, `warnings`, and `errors`. Use `missing_tool` warnings or blockers when required tooling is unavailable. Static evidence, sandbox_generated evidence, Qiling-only output, and public writeups are not runtime truth; keep behavior_claim_allowed=false unless observed_runtime_qemu, observed_runtime_live_hook, observed_runtime_live_debugger, or verified evidence proves the target workload was observed.

## Session Continuation

Treat same-session follow-up prompts about the current firmware artifact as continuation signals. Resume from the latest artifact index, hypothesis ledger, next_skill_decision.json, or blockers.json instead of waiting for the user to invoke the skill again explicitly.

## Loop Guard

Do not repeat the same failing action, validation, probe, or handoff when inputs and artifacts have not changed. If the same blocker appears twice, write or update blockers.json with the repeated blocker, stop and ask the user for the missing input or decision. Prefer a lower-cost evidence-gathering step only when it changes the artifact state.

## Outputs

- `exploitability-pattern`
- `surface-fingerprint`
- `sink-pattern`
- `crash-signature`
- `false-positive-pattern`

## Verification Gate

Do not mark this skill complete until outputs satisfy the routing completion gate and the artifact contract. Evidence levels must progress from E0 to E8 without skipping runtime or duplicate-check gates. `verification-before-completion` is required before claiming a result is valid.

## Safety

Operate only on firmware and runtimes the user is authorized to test. Keep destructive probes disabled by default; record runtime modifications; prefer local evidence and redacted summaries; use exact dates and versions in vulnerability reports; do not install tools without explicit user approval. Do not commit firmware, secrets, proprietary dumps, raw traces, or private vendor material. Do not mass target devices, do not scan public IPs, do not build a weaponized exploit generator, and do not invent CVE IDs.

## Common Mistakes

- Promoting product-specific noise as reusable memory.
- Saving raw proprietary snippets.
- Using memory as a substitute for current artifact verification.
