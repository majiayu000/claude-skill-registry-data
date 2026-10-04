---
name: firmware-service-emulation
description: Use when a selected service has inventory, state map, and a hypothesis requiring emulated execution, including full service readiness, host/browser UI access, login, or feature-use gates.
---

# Firmware Service Emulation

## Overview

Emulate selected services only when readiness gates and service state evidence support it. For UI-bearing firmware, successful emulation requires host/browser UI access and service readiness, not only a boot log or guest listener. This skill is part of the discovery-first firmware research suite for authorized binary/service exploitability assessment. It preserves blocker-first workflow, compact local evidence, and provenance-first claims.

## Routing

```yaml
role: interaction
purpose: Emulate selected services only when readiness gates and service state evidence support it.
when_to_use:
  - Use when a selected service has inventory, state map, and a hypothesis requiring emulated execution.
  - Use when the user asks to make firmware services usable through a browser UI, WBM, API, or authenticated workflow.
when_not_to_use:
  - Do not use when required inputs are missing; return to the orchestrator and write a blocker instead.
required_inputs:
  - service_inventory.json
  - service_state_map.json
  - hypothesis_ledger.json
produces:
  - runtime_readiness.json
  - reachable_services.json
  - ui_access_status.json
  - emulation_success.json
  - emulation_blocker.json
completion_gate:
  - runtime_readiness.json and reachable_services.json are written with schema_version, provenance, warnings, errors, evidence labels, and blockers for missing inputs.
  - If the target has UI or API services, ui_access_status.json records browser/host reachability, login state, and feature-use readiness, and emulation_success.json is true only when all required gates pass.
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

- service_inventory.json
- service_state_map.json
- hypothesis_ledger.json

## Workflow

1. Check required files, libraries, devices, ports, env, and init state.
2. Block readiness on unexplained HTTP 500/404, missing backend listeners, missing reverse-proxy targets, or missing required services.
3. Record qemu-user, qemu-system, chroot, container, proxy, or static-only mode; degraded userland lanes are allowed but must be labeled as degraded instead of full-device emulation.
4. For UI-bearing firmware, expose the real UI to the host or browser, verify static assets load, and verify HTTP/API routing from the same origin the browser uses.
5. Verify auth state without storing secrets: negative-control invalid credentials should reach the login endpoint, and valid user-provided credentials should be entered by the user or used only in ephemeral local commands.
6. After login, run an authenticated read-only route matrix for representative UI functions and API proxies. For each non-2xx key route, record the mapped backend service, expected port, observed process/listener state, direct backend result, and relevant log excerpt in `debug_transcript_index.json` or `emulation_blocker.json`.
7. Confirm service dependencies, not only the main web process: MQTT, config managers, update/certificate state, databases, WebSocket servers, controller agents, simulators, fieldbus/CAN devices, load-management/OCPP/modbus daemons, and persistent data/log directories.
8. Do not claim `ready_for_pentest=true` or `emulation_success=true` without observed processes, ports, host/browser UI access, login/auth handling, authenticated feature/API usability, and an explicit degraded/blocked/usable map for key services.

## Emulation Success Gate

Set `emulation_success=true` only when all required gates pass:

- `boot_or_userland_started`: the target runtime lane is named and observed.
- `service_ready`: required daemons/processes and backend ports are observed or intentionally scoped out.
- `host_reachable`: UI/API entrypoints are reachable from the host/browser path the user will use.
- `ui_accessible`: static assets and app routing load in the browser path.
- `login_flow_observed`: valid auth succeeds or the auth blocker is explicit; secrets are not stored.
- `feature_use_observed`: authenticated read-only feature route matrix passes for required functions.
- `dependency_scope_clear`: missing hardware/simulator dependencies are fixed, shimmed with scope, or recorded as active blockers.

If any required gate fails, write `emulation_success=false` and `emulation_blocker.json` with root-cause evidence and next actions.

Always use `firmware-artifact-contract` before trusting shared artifacts. Every JSON output must include `schema_version`, `generated_at`, `generated_by`, `source_inputs`, `warnings`, and `errors`. Use `missing_tool` warnings or blockers when required tooling is unavailable. Static evidence, sandbox_generated evidence, Qiling-only output, and public writeups are not runtime truth; keep behavior_claim_allowed=false unless observed_runtime_qemu, observed_runtime_live_hook, observed_runtime_live_debugger, or verified evidence proves the target workload was observed.

## Session Continuation

Treat same-session follow-up prompts about the current firmware artifact as continuation signals. Resume from the latest artifact index, hypothesis ledger, next_skill_decision.json, or blockers.json instead of waiting for the user to invoke the skill again explicitly.

## Loop Guard

Do not repeat the same failing action, validation, probe, or handoff when inputs and artifacts have not changed. If the same blocker appears twice, write or update blockers.json with the repeated blocker, stop and ask the user for the missing input or decision. Prefer a lower-cost evidence-gathering step only when it changes the artifact state.

## Outputs

- `runtime_readiness.json`
- `reachable_services.json`
- `ui_access_status.json`
- `emulation_success.json`
- `emulation_blocker.json`

## Verification Gate

Do not mark this skill complete until outputs satisfy the routing completion gate and the artifact contract. Evidence levels must progress from E0 to E8 without skipping runtime or duplicate-check gates. `verification-before-completion` is required before claiming a result is valid.

## Safety

Operate only on firmware and runtimes the user is authorized to test. Keep destructive probes disabled by default; record runtime modifications; prefer local evidence and redacted summaries; use exact dates and versions in vulnerability reports; do not install tools without explicit user approval. Do not commit firmware, secrets, proprietary dumps, raw traces, or private vendor material. Do not mass target devices, do not scan public IPs, do not build a weaponized exploit generator, and do not invent CVE IDs.

## Common Mistakes

- Skipping firmware-artifact-contract validation.
- Making a vulnerability claim from static-only evidence.
- Forgetting missing_tool or blocker records when tooling is unavailable.
- Calling emulation successful when only guest-loopback works but host/browser UI cannot be used.
- Hiding degraded dependencies such as missing hardware, system managers, WebSocket backends, or helper daemons.
- Calling emulation successful when login works but authenticated feature/API routes still produce unexplained 500/404.
- Treating a stub, seeded DB row, generated cert, or local proxy as full-device behavior without labeling the claim scope.
