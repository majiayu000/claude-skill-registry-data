---
name: firmware-service-state-discovery
description: Use when a service candidate has inputs or sinks but state/auth requirements are unclear, including UI, login, service dependency, and host reachability preconditions.
---

# Firmware Service State Discovery

## Overview

Model service state, auth boundaries, preconditions, and reachability constraints. This skill is part of the discovery-first firmware research suite for authorized binary/service exploitability assessment. It preserves blocker-first workflow, compact local evidence, and provenance-first claims.

## Routing

```yaml
role: domain
purpose: Model service state, auth boundaries, preconditions, and reachability constraints.
when_to_use:
  - Use when a service candidate has inputs or sinks but state/auth requirements are unclear.
when_not_to_use:
  - Do not use when required inputs are missing; return to the orchestrator and write a blocker instead.
required_inputs:
  - service_inventory.json
  - attack_surface_graph.json
  - input_vectors.json
produces:
  - service_state_map.json
  - reachability_blockers.json
  - ui_access_requirements.json
completion_gate:
  - service_state_map.json is written with schema_version, provenance, warnings, errors, evidence labels, service dependency state, auth state, UI reachability state, and blockers for missing inputs.
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
- attack_surface_graph.json
- input_vectors.json

## Workflow

1. Map required files, daemons, hardware, credentials, sessions, and startup state.
2. Classify auth boundaries and preconditions.
3. For UI-bearing services, map the browser entrypoint, static asset path, API base URL, WebSocket endpoints, reverse proxy assumptions, login endpoint, token/session storage, and key feature routes.
4. For every key feature route, map frontend route -> reverse proxy -> backend service -> port/socket -> config file -> data directory -> hardware/simulator dependency. Include likely root-cause collection points such as stderr/stdout logs, service logs, process table, `ss -ltnp`, and read-only direct backend curls.
5. Separate reachable, degraded, blocked, and unknown services; distinguish guest-loopback reachability from host/browser reachability.
6. Mark hardware-backed dependencies explicitly: CAN/vcan, serial buses, GPIO/sysfs, modem, storage partitions, TPM/TEE, certificates, databases, MQTT brokers, controller agents, and simulators. Missing hardware that causes empty service state or HTTP 500 is an emulation blocker unless a scoped shim is intentionally used.
7. Handoff runnable services to emulation or runtime observation with a required UI/service success gate when the user wants real UI or feature use.

Always use `firmware-artifact-contract` before trusting shared artifacts. Every JSON output must include `schema_version`, `generated_at`, `generated_by`, `source_inputs`, `warnings`, and `errors`. Use `missing_tool` warnings or blockers when required tooling is unavailable. Static evidence, sandbox_generated evidence, Qiling-only output, and public writeups are not runtime truth; keep behavior_claim_allowed=false unless observed_runtime_qemu, observed_runtime_live_hook, observed_runtime_live_debugger, or verified evidence proves the target workload was observed.

## Session Continuation

Treat same-session follow-up prompts about the current firmware artifact as continuation signals. Resume from the latest artifact index, hypothesis ledger, next_skill_decision.json, or blockers.json instead of waiting for the user to invoke the skill again explicitly.

## Loop Guard

Do not repeat the same failing action, validation, probe, or handoff when inputs and artifacts have not changed. If the same blocker appears twice, write or update blockers.json with the repeated blocker, stop and ask the user for the missing input or decision. Prefer a lower-cost evidence-gathering step only when it changes the artifact state.

## Outputs

- `service_state_map.json`
- `reachability_blockers.json`
- `ui_access_requirements.json`

## Verification Gate

Do not mark this skill complete until outputs satisfy the routing completion gate and the artifact contract. Evidence levels must progress from E0 to E8 without skipping runtime or duplicate-check gates. `verification-before-completion` is required before claiming a result is valid.

## Safety

Operate only on firmware and runtimes the user is authorized to test. Keep destructive probes disabled by default; record runtime modifications; prefer local evidence and redacted summaries; use exact dates and versions in vulnerability reports; do not install tools without explicit user approval. Do not commit firmware, secrets, proprietary dumps, raw traces, or private vendor material. Do not mass target devices, do not scan public IPs, do not build a weaponized exploit generator, and do not invent CVE IDs.

## Common Mistakes

- Skipping firmware-artifact-contract validation.
- Making a vulnerability claim from static-only evidence.
- Forgetting missing_tool or blocker records when tooling is unavailable.
- Treating HTTP 403, HTTP 404, CORS OPTIONS, or static route discovery as proof that login and feature use are ready.
- Losing track of frontend-to-backend routing, WebSocket, or reverse-proxy assumptions needed for a real UI session.
- Failing to connect a UI 500/404 to the missing backend port, config file, data directory, or hardware/simulator dependency that actually caused it.
