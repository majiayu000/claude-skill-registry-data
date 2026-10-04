---
name: firmware-artifact-contract
description: Use when creating, validating, or consuming shared firmware discovery artifacts, observation labels, evidence levels, skill routing decisions, or blocker reports.
---

# Firmware Artifact Contract

## Overview

Define shared evidence, schema, sensitivity, evidence ladder, and validation rules for firmware discovery artifacts. This skill is part of the discovery-first firmware research suite for authorized binary/service exploitability assessment. It preserves blocker-first workflow, compact local evidence, and provenance-first claims.

## Routing

```yaml
role: protocol
purpose: Define shared evidence, schema, sensitivity, evidence ladder, and validation rules for firmware discovery artifacts.
when_to_use:
  - Use when creating, validating, or consuming shared firmware discovery artifacts, observation labels, evidence levels, skill routing decisions, or blocker reports.
when_not_to_use:
  - Do not use as a reverse-engineering or probing skill; it defines contracts and validation gates only.
required_inputs:
  - Any JSON artifact, JSONL observation stream, finding record, discovery artifact, or candidate report
produces:
  - validated artifact status
  - contract warnings
  - schema-aligned blocker notes
completion_gate:
  - Artifact has schema_version, provenance, sensitivity, warnings, errors, and artifact-specific required fields.
reentry_triggers:
  - Re-enter whenever a new artifact type, evidence level, or claim boundary is introduced.
handoff_hints:
  - Return to the calling orchestrator or domain skill after validation.
misuse_signals:
  - The skill is being misused if validation output is treated as firmware behavior proof.
```

## Required Superpowers

- Use `superpowers:systematic-debugging` when validation fails unexpectedly.
- Use `superpowers:verification-before-completion` before claiming an artifact is valid.

## Inputs

- Any JSON artifact, JSONL observation stream, finding record, discovery artifact, or candidate report

## Workflow

1. Check schema_version, generated_at, generated_by, source_inputs, warnings, and errors before trusting any JSON artifact.
2. Label every observation with artifact_sensitivity and behavior_claim_allowed.
3. Apply the E0 through E8 evidence ladder before allowing vulnerability or exploitability language.
4. For emulation artifacts, separate `boot_observed`, `service_ready`, `host_reachable`, `ui_accessible`, `login_flow_observed`, `feature_use_observed`, `route_matrix_observed`, `dependency_map_observed`, and `degraded_dependencies`; do not collapse them into one readiness flag.
5. For UI/API firmware, require `ui_runtime_observation.json` to include an authenticated read-only route matrix when credentials are available. Each required non-2xx route must have a matching blocker or debug transcript entry with backend service, expected port, observed listener/process state, direct backend result, and log/config evidence.
6. Write blockers instead of guessing when identity, extraction, reachability, tooling, UI routing, auth state, dependency state, hardware/simulator state, or provenance is unclear.

Always use `firmware-artifact-contract` before trusting shared artifacts. Every JSON output must include `schema_version`, `generated_at`, `generated_by`, `source_inputs`, `warnings`, and `errors`. Use `missing_tool` warnings or blockers when required tooling is unavailable. Static evidence, sandbox_generated evidence, Qiling-only output, and public writeups are not runtime truth; keep behavior_claim_allowed=false unless observed_runtime_qemu, observed_runtime_live_hook, observed_runtime_live_debugger, or verified evidence proves the target workload was observed.

## Session Continuation

Treat same-session follow-up prompts about the current firmware artifact as continuation signals. Resume from the latest artifact index, hypothesis ledger, next_skill_decision.json, or blockers.json instead of waiting for the user to invoke the skill again explicitly.

## Loop Guard

Do not repeat the same failing action, validation, probe, or handoff when inputs and artifacts have not changed. If the same blocker appears twice, write or update blockers.json with the repeated blocker, stop and ask the user for the missing input or decision. Prefer a lower-cost evidence-gathering step only when it changes the artifact state.

## Outputs

- `next_skill_decision.json`
- `hypothesis_ledger.json`
- `runtime_readiness.json`
- `reachable_services.json`
- `ui_access_status.json`
- `emulation_success.json`
- `exploitability_assessment.json`
- `duplicate_check.json`
- `candidate_report.json`

`emulation_success.json` may set `emulation_success=true` only when required services are observed, host/browser UI is reachable, login/auth flow is accounted for without storing secrets, authenticated required feature/API routes are usable, and dependencies are either working or explicitly marked non-required/degraded with evidence. Required feature routes with unexplained 500/404/502 force `emulation_success=false`. Userland, chroot, container, or proxy-based success must include `claim_scope` and must not be labeled full-device emulation.

## Verification Gate

Do not mark this skill complete until outputs satisfy the routing completion gate and the artifact contract. Evidence levels must progress from E0 to E8 without skipping runtime or duplicate-check gates. `verification-before-completion` is required before claiming a result is valid.

## Safety

Operate only on firmware and runtimes the user is authorized to test. Keep destructive probes disabled by default; record runtime modifications; prefer local evidence and redacted summaries; use exact dates and versions in vulnerability reports; do not install tools without explicit user approval. Do not commit firmware, secrets, proprietary dumps, raw traces, or private vendor material. Do not mass target devices, do not scan public IPs, do not build a weaponized exploit generator, and do not invent CVE IDs.

## Common Mistakes

- Treating static strings as runtime behavior.
- Writing artifacts without provenance.
- Letting an E1 static candidate become an E8 report.
- Copying secrets from local evidence into reports.
- Calling firmware emulation successful without browser/UI evidence when the target exposes a UI.
- Omitting degraded dependency and claim-scope labels for qemu-user, chroot, container, or proxy lanes.
- Omitting the authenticated route matrix or leaving failed required routes without root-cause/blocker evidence.
- Marking hardware-backed services successful when their simulator/fieldbus/device dependencies are absent or empty.
