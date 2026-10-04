---
name: firmware-runtime-observation
description: Use when a service is runnable or a specific workload/hypothesis needs observed runtime evidence, including browser UI, login, API, WebSocket, or feature-use observations.
---

# Firmware Runtime Observation

## Overview

Run hypothesis-driven runtime tracing, hooking, logging, or packet capture. This skill is part of the discovery-first firmware research suite for authorized binary/service exploitability assessment. It preserves blocker-first workflow, compact local evidence, and provenance-first claims.

## Routing

```yaml
role: interaction
purpose: Run hypothesis-driven runtime tracing, hooking, logging, or packet capture.
when_to_use:
  - Use when a service is runnable or a specific workload/hypothesis needs observed runtime evidence.
  - Use when UI access, login, authenticated navigation, API calls, or feature use must be observed from the host/browser path.
when_not_to_use:
  - Do not use when required inputs are missing; return to the orchestrator and write a blocker instead.
required_inputs:
  - runtime_readiness.json
  - hypothesis
  - workload
  - expected observation
produces:
  - runtime_observation.json
  - ui_runtime_observation.json
  - observed_path_chains.json
  - observed_sink_hits.json
  - debug_transcript_index.json
completion_gate:
  - runtime_observation.json is written with schema_version, provenance, warnings, errors, evidence labels, and blockers for missing inputs.
  - For UI-bearing workloads, ui_runtime_observation.json records browser-visible UI load, login outcome, feature-route behavior, failed dependencies, and whether the observation came from full-system, userland, container, proxy, or live device mode.
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

- runtime_readiness.json
- hypothesis
- workload
- expected observation

## Workflow

1. Capture host-level and guest-level observations with strace, tcpdump, Frida, bpftrace, logs, or debugger-safe traces.
2. Treat Qiling only as a separate instrumentation lane unless runtime evidence verifies it.
3. For UI workloads, observe the same path a user will use: browser/static assets, API base path, WebSocket path, session/token storage, and at least one read-only feature route after login when credentials are available.
4. When the goal is usable firmware emulation, collect an authenticated read-only route matrix after login. Include status, short redacted samples, route purpose, and whether each route is required, optional, degraded, or blocked.
5. For every required route returning 500/404/502 or empty critical state, gather root-cause evidence at component boundaries: browser/proxy URL, backend port, service process, direct backend curl, config/data path, hardware/simulator dependency, and logs. Route to firmware-debugging when the cause is not already explained.
6. Redact local evidence summaries and never write real credentials, tokens, cookies, private keys, or private certificates into artifacts.
7. Re-enter when probing reaches a new parser, endpoint, sink, login boundary, blocked dependency, or degraded UI function.

Always use `firmware-artifact-contract` before trusting shared artifacts. Every JSON output must include `schema_version`, `generated_at`, `generated_by`, `source_inputs`, `warnings`, and `errors`. Use `missing_tool` warnings or blockers when required tooling is unavailable. Static evidence, sandbox_generated evidence, Qiling-only output, and public writeups are not runtime truth; keep behavior_claim_allowed=false unless observed_runtime_qemu, observed_runtime_live_hook, observed_runtime_live_debugger, or verified evidence proves the target workload was observed.

## Session Continuation

Treat same-session follow-up prompts about the current firmware artifact as continuation signals. Resume from the latest artifact index, hypothesis ledger, next_skill_decision.json, or blockers.json instead of waiting for the user to invoke the skill again explicitly.

## Loop Guard

Do not repeat the same failing action, validation, probe, or handoff when inputs and artifacts have not changed. If the same blocker appears twice, write or update blockers.json with the repeated blocker, stop and ask the user for the missing input or decision. Prefer a lower-cost evidence-gathering step only when it changes the artifact state.

## Outputs

- `runtime_observation.json`
- `ui_runtime_observation.json`
- `observed_path_chains.json`
- `observed_sink_hits.json`
- `debug_transcript_index.json`

## Verification Gate

Do not mark this skill complete until outputs satisfy the routing completion gate and the artifact contract. Evidence levels must progress from E0 to E8 without skipping runtime or duplicate-check gates. `verification-before-completion` is required before claiming a result is valid.

## Safety

Operate only on firmware and runtimes the user is authorized to test. Keep destructive probes disabled by default; record runtime modifications; prefer local evidence and redacted summaries; use exact dates and versions in vulnerability reports; do not install tools without explicit user approval. Do not commit firmware, secrets, proprietary dumps, raw traces, or private vendor material. Do not mass target devices, do not scan public IPs, do not build a weaponized exploit generator, and do not invent CVE IDs.

## Common Mistakes

- Skipping firmware-artifact-contract validation.
- Making a vulnerability claim from static-only evidence.
- Forgetting missing_tool or blocker records when tooling is unavailable.
- Claiming UI functionality from backend curl alone when browser routing, static assets, WebSockets, or auth storage were not observed.
- Recording secrets or bearer tokens in runtime artifacts.
- Reporting only aggregate "UI works" status without the authenticated route matrix and failed-dependency map.
- Treating empty state from missing hardware, simulator, or database dependencies as normal feature usability without evidence.
