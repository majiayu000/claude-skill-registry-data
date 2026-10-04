---
name: firmware-discovery-orchestrator
description: Use when starting, resuming, continuing, or recovering analysis of an authorized firmware artifact and deciding which skill should run next, including UI/service emulation success gates.
---

# Firmware Discovery Orchestrator

## Overview

Choose the next evidence-gated discovery action from current firmware artifacts. This skill is part of the discovery-first firmware research suite for authorized binary/service exploitability assessment. It preserves blocker-first workflow, compact local evidence, and provenance-first claims.

## Routing

```yaml
role: orchestrator
purpose: Choose the next evidence-gated discovery action from current firmware artifacts.
when_to_use:
  - Use when starting, resuming, continuing, or recovering analysis of an authorized firmware artifact and deciding which skill should run next.
when_not_to_use:
  - Do not perform deep reverse engineering, probing, debugging, or duplicate research inside the orchestrator.
required_inputs:
  - artifact index
  - firmware_manifest.json
  - hypothesis_ledger.json
  - current evidence levels
produces:
  - discovery_plan.json
  - target_selection.json
  - hypothesis_ledger.json
  - next_skill_decision.json
  - blockers.json
completion_gate:
  - A next skill is selected with required_inputs_satisfied=true, or a blocker explains why no skill is valid.
reentry_triggers:
  - Re-enter after every artifact change, contradiction, blocker resolution, or new runtime observation.
handoff_hints:
  - Route to intake, inventory, attack-surface graph, input-path discovery, sink/source analysis, or exploitability orchestration.
misuse_signals:
  - The skill is being misused if it makes vulnerability claims or runs analysis itself.
```

## Required Superpowers

- Use `superpowers:systematic-debugging` when validation fails unexpectedly.
- Use `superpowers:verification-before-completion` before claiming an artifact is valid.

## Inputs

- artifact index
- firmware_manifest.json
- hypothesis_ledger.json
- current evidence levels

## Workflow

1. Read artifact index and hypothesis ledger.
2. Identify evidence level E0 through E8 for each candidate.
3. List skills with satisfied required inputs and exclude anti-triggered skills.
4. If the current goal includes firmware emulation, WBM/UI, login, or feature use, require a path to `runtime_readiness.json`, `reachable_services.json`, `ui_access_status.json`, `ui_runtime_observation.json`, `debug_transcript_index.json`, and `emulation_success.json`; route to service-state-discovery, service-emulation, runtime-observation, or firmware-debugging until those artifacts exist or a blocker explains why not.
5. Preserve an `emulation_success_gate` in next_skill_decision.json that names required UI entrypoints, auth/login expectations, representative authenticated routes, backend dependency ports, acceptable degraded lanes, and non-acceptable blockers.
6. Treat unexplained authenticated HTTP 500/404, missing backend listeners, missing WebSocket/API proxies, and hardware/simulator blockers as active emulation blockers. Do not route onward as if emulation succeeded until each is fixed, scoped as degraded, or recorded in emulation_blocker.json.
7. Select the skill with highest expected evidence gain or write a blocker.

Always use `firmware-artifact-contract` before trusting shared artifacts. Every JSON output must include `schema_version`, `generated_at`, `generated_by`, `source_inputs`, `warnings`, and `errors`. Use `missing_tool` warnings or blockers when required tooling is unavailable. Static evidence, sandbox_generated evidence, Qiling-only output, and public writeups are not runtime truth; keep behavior_claim_allowed=false unless observed_runtime_qemu, observed_runtime_live_hook, observed_runtime_live_debugger, or verified evidence proves the target workload was observed.

## Session Continuation

Treat same-session follow-up prompts about the current firmware artifact as continuation signals. Resume from the latest artifact index, hypothesis ledger, next_skill_decision.json, or blockers.json instead of waiting for the user to invoke the skill again explicitly.

## Loop Guard

Do not repeat the same failing action, validation, probe, or handoff when inputs and artifacts have not changed. If the same blocker appears twice, write or update blockers.json with the repeated blocker, stop and ask the user for the missing input or decision. Prefer a lower-cost evidence-gathering step only when it changes the artifact state.

## Outputs

- `skill_decision_001`
- `expected_evidence_gain`
- `reentry_condition`

For emulation goals, next_skill_decision.json must include `emulation_success_gate` with required services, required UI entrypoints, login/auth handling, authenticated read-only route matrix expectations, acceptable degraded lanes, and blockers that prevent browser-level feature use. If any key UI/API route remains 500/404, next_skill_decision.json must route to debugging/runtime observation rather than declare success.

## Verification Gate

Do not mark this skill complete until outputs satisfy the routing completion gate and the artifact contract. Evidence levels must progress from E0 to E8 without skipping runtime or duplicate-check gates. `verification-before-completion` is required before claiming a result is valid.

## Safety

Operate only on firmware and runtimes the user is authorized to test. Keep destructive probes disabled by default; record runtime modifications; prefer local evidence and redacted summaries; use exact dates and versions in vulnerability reports; do not install tools without explicit user approval. Do not commit firmware, secrets, proprietary dumps, raw traces, or private vendor material. Do not mass target devices, do not scan public IPs, do not build a weaponized exploit generator, and do not invent CVE IDs.

## Common Mistakes

- Calling a skill because its topic sounds related.
- Skipping blockers when inputs are missing.
- Forgetting re-entry after artifact changes.
- Routing away from emulation before host/browser UI access and required services are either usable or explicitly blocked.
- Treating full-system QEMU, qemu-user, chroot, container, or proxy modes as equivalent without labeling their claim scope.
- Losing the one-shot emulation goal after a partial UI success; login alone does not satisfy service/function usability.
