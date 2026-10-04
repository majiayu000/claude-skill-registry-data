---
name: firmware-crash-root-cause
description: Use when probing, runtime observation, or debugging produces a crash or suspicious controlled effect.
---

# Firmware Crash Root Cause

## Overview

Classify crashes and suspicious effects into root-cause evidence and bug class. This skill is part of the discovery-first firmware research suite for authorized binary/service exploitability assessment. It preserves blocker-first workflow, compact local evidence, and provenance-first claims.

## Routing

```yaml
role: domain
purpose: Classify crashes and suspicious effects into root-cause evidence and bug class.
when_to_use:
  - Use when probing, runtime observation, or debugging produces a crash or suspicious controlled effect.
when_not_to_use:
  - Do not use when required inputs are missing; return to the orchestrator and write a blocker instead.
required_inputs:
  - probe_results.json or runtime_observation.json
  - debug transcript index
  - candidate hypothesis
produces:
  - crash_analysis.json
  - root_cause_blockers.json
completion_gate:
  - crash_analysis.json is written with schema_version, provenance, warnings, errors, evidence labels, and blockers for missing inputs.
reentry_triggers:
  - Re-enter when new services, IPC paths, runtime observations, contradictions, or candidate evidence changes the artifact.
handoff_hints:
  - Return to firmware-discovery-orchestrator or firmware-exploitability-orchestrator with next evidence gaps.
misuse_signals:
  - The skill is being misused if it turns static, sandbox, Qiling, or public-source evidence into runtime truth.
```

## Required Superpowers

- Use `superpowers:systematic-debugging` when validation fails unexpectedly.
- Use `superpowers:verification-before-completion` before claiming an artifact is valid.

## Inputs

- probe_results.json or runtime_observation.json
- debug transcript index
- candidate hypothesis

## Workflow

1. Normalize crash signature and reproduction metadata.
2. Classify root_cause_status and bug class.
3. Assess input influence and affected component.
4. Handoff primitive questions to exploitability modeling.

Always use `firmware-artifact-contract` before trusting shared artifacts. Every JSON output must include `schema_version`, `generated_at`, `generated_by`, `source_inputs`, `warnings`, and `errors`. Use `missing_tool` warnings or blockers when required tooling is unavailable. Static evidence, sandbox_generated evidence, Qiling-only output, and public writeups are not runtime truth; keep behavior_claim_allowed=false unless observed_runtime_qemu, observed_runtime_live_hook, observed_runtime_live_debugger, or verified evidence proves the target workload was observed.

## Session Continuation

Treat same-session follow-up prompts about the current firmware artifact as continuation signals. Resume from the latest artifact index, hypothesis ledger, next_skill_decision.json, or blockers.json instead of waiting for the user to invoke the skill again explicitly.

## Loop Guard

Do not repeat the same failing action, validation, probe, or handoff when inputs and artifacts have not changed. If the same blocker appears twice, write or update blockers.json with the repeated blocker, stop and ask the user for the missing input or decision. Prefer a lower-cost evidence-gathering step only when it changes the artifact state.

## Outputs

- `crash_analysis.json`
- `root_cause_blockers.json`

## Verification Gate

Do not mark this skill complete until outputs satisfy the routing completion gate and the artifact contract. Evidence levels must progress from E0 to E8 without skipping runtime or duplicate-check gates. `verification-before-completion` is required before claiming a result is valid.

## Safety

Operate only on firmware and runtimes the user is authorized to test. Keep destructive probes disabled by default; record runtime modifications; prefer local evidence and redacted summaries; use exact dates and versions in vulnerability reports; do not install tools without explicit user approval. Do not commit firmware, secrets, proprietary dumps, raw traces, or private vendor material. Do not mass target devices, do not scan public IPs, do not build a weaponized exploit generator, and do not invent CVE IDs.

## Common Mistakes

- Skipping firmware-artifact-contract validation.
- Making a vulnerability claim from static-only evidence.
- Forgetting missing_tool or blocker records when tooling is unavailable.
