---
name: firmware-start
description: Use when a user has a firmware file or extracted directory and wants to start, continue, resume, or recover authorized local firmware discovery without knowing the full skill sequence.
---

# Firmware Start

## Overview

Act as the beginner entrypoint that turns a one-line firmware path prompt into the discovery-first workflow. This skill is part of the discovery-first firmware research suite for authorized binary/service exploitability assessment. It preserves blocker-first workflow, compact local evidence, and provenance-first claims.

## Routing

```yaml
role: orchestrator
purpose: Act as the beginner entrypoint that turns a one-line firmware path prompt into the discovery-first workflow.
when_to_use:
  - Use when a user has a firmware file or extracted directory and wants to start, continue, resume, or recover authorized local firmware discovery without knowing the full skill sequence.
when_not_to_use:
  - Do not perform extraction, reverse engineering, probing, debugging, duplicate research, or exploitability analysis inside the entrypoint.
required_inputs:
  - firmware path or extracted directory
  - optional authorization note
  - optional device/model/version hint
  - optional emulation goal such as full services, browser UI, login, or feature use
  - optional output workspace
produces:
  - starter_request.json
  - next_skill_decision.json
  - blockers.json
completion_gate:
  - starter_request.json captures the input artifact, authorization scope, safety boundary, requested goal, and handoff to firmware-discovery-orchestrator.
reentry_triggers:
  - Re-enter for a new firmware artifact, extracted directory, beginner goal, same-session follow-up, or blocker recovery for the current firmware artifact.
handoff_hints:
  - Route immediately to firmware-discovery-orchestrator after starter request normalization.
misuse_signals:
  - The skill is being misused if it performs deep analysis instead of handing off to firmware-discovery-orchestrator.
```

## Required Superpowers

- Use `superpowers:systematic-debugging` when validation fails unexpectedly.
- Use `superpowers:verification-before-completion` before claiming an artifact is valid.

## Inputs

- firmware path or extracted directory
- optional authorization note
- optional device/model/version hint
- optional emulation goal such as full services, browser UI, login, or feature use
- optional output workspace

## Workflow

1. Accept a one-line beginner prompt such as `Dùng firmware-start với D:\path\firmware.bin`.
2. Normalize the firmware path or extracted directory into starter_request.json.
3. If the user asks to emulate, access WBM/UI, log in, or use functions, record `requested_goal.emulation_success_gate=true` and require host/browser UI access plus service readiness before any "emulation successful" claim.
4. For one-shot emulation goals, preserve a concrete success contract in starter_request.json:
   - real UI entrypoint is reachable from the host/browser, not only guest loopback;
   - login/auth is observed or explicitly blocked without storing credentials, tokens, or cookies;
   - authenticated read-only route matrix covers representative UI features and API proxies;
   - unexplained HTTP 500/404 on key feature routes blocks success until root-caused or marked degraded with evidence;
   - backend dependency ports/processes/logs are mapped for each failed UI/API route;
   - hardware/simulator requirements such as CAN, serial devices, NVRAM, TPM, modem, storage partitions, or service-specific daemons are either emulated, shimmed with explicit scope, or written as blockers.
5. Apply default safety boundaries: local artifact analysis, no public targeting, no mass scanning, no destructive probing, no upload of raw firmware or evidence, no stored credentials, and no invented CVE IDs.
6. If authorization is ambiguous, write blockers.json or ask for confirmation before runtime interaction, probing, login, or exploitability claims.
7. Write next_skill_decision.json that selects firmware-discovery-orchestrator as the handoff skill.

Always use `firmware-artifact-contract` before trusting shared artifacts. Every JSON output must include `schema_version`, `generated_at`, `generated_by`, `source_inputs`, `warnings`, and `errors`. Use `missing_tool` warnings or blockers when required tooling is unavailable. Static evidence, sandbox_generated evidence, Qiling-only output, and public writeups are not runtime truth; keep behavior_claim_allowed=false unless observed_runtime_qemu, observed_runtime_live_hook, observed_runtime_live_debugger, or verified evidence proves the target workload was observed.

## Session Continuation

Treat same-session follow-up prompts about the current firmware artifact as continuation signals. Resume from the latest artifact index, hypothesis ledger, next_skill_decision.json, or blockers.json instead of waiting for the user to invoke the skill again explicitly.

## Loop Guard

Do not repeat the same failing action, validation, probe, or handoff when inputs and artifacts have not changed. If the same blocker appears twice, write or update blockers.json with the repeated blocker, stop and ask the user for the missing input or decision. Prefer a lower-cost evidence-gathering step only when it changes the artifact state.

## Outputs

- `starter_request.json`
- `next_skill_decision.json`
- `blockers.json`
- `handoff_skill: firmware-discovery-orchestrator`

When `requested_goal.emulation_success_gate=true`, starter_request.json should preserve that goal so downstream skills must produce `runtime_readiness.json`, `reachable_services.json`, `ui_access_status.json`, `ui_runtime_observation.json`, `debug_transcript_index.json`, and `emulation_success.json` or an explicit blocker. A one-shot run is not confirmed successful until these artifacts show service readiness, browser/UI reachability, login/auth handling, and feature/API usability.

## Verification Gate

Do not mark this skill complete until outputs satisfy the routing completion gate and the artifact contract. Evidence levels must progress from E0 to E8 without skipping runtime or duplicate-check gates. `verification-before-completion` is required before claiming a result is valid.

## Safety

Operate only on firmware and runtimes the user is authorized to test. Keep destructive probes disabled by default; record runtime modifications; prefer local evidence and redacted summaries; use exact dates and versions in vulnerability reports; do not install tools without explicit user approval. Do not commit firmware, secrets, proprietary dumps, raw traces, or private vendor material. Do not mass target devices, do not scan public IPs, do not build a weaponized exploit generator, and do not invent CVE IDs.

## Common Mistakes

- Asking beginners to know the full skill sequence.
- Doing extraction or probing inside the entrypoint.
- Continuing when authorization is ambiguous.
- Skipping the discovery orchestrator handoff.
- Treating a boot log, shell, or guest-loopback listener as successful emulation when the user asked for browser UI or feature use.
- Treating "login page works" or "login succeeds" as enough when authenticated feature routes still return unexplained 500/404.
