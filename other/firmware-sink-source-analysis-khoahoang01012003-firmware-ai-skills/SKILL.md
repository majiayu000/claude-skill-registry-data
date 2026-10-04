---
name: firmware-sink-source-analysis
description: Use when input paths exist and parser/sink relationships need prioritization.
---

# Firmware Sink Source Analysis

## Overview

Map sources to dangerous sinks and produce hypotheses instead of vulnerability claims. This skill is part of the discovery-first firmware research suite for authorized binary/service exploitability assessment. It preserves blocker-first workflow, compact local evidence, and provenance-first claims.

## Routing

```yaml
role: domain
purpose: Map sources to dangerous sinks and produce hypotheses instead of vulnerability claims.
when_to_use:
  - Use when input paths exist and parser/sink relationships need prioritization.
when_not_to_use:
  - Do not use when required inputs are missing; return to the orchestrator and write a blocker instead.
required_inputs:
  - input_vectors.json
  - input_path_chains.json
  - binary context
produces:
  - sink_source_map.json
  - hypothesis updates
completion_gate:
  - sink_source_map.json is written with schema_version, provenance, warnings, errors, evidence labels, and blockers for missing inputs.
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

- input_vectors.json
- input_path_chains.json
- binary context

## Workflow

1. Identify sinks such as memory copy, command execution, path traversal, parser arithmetic, auth checks, and unsafe deserialization.
2. Connect each sink to attacker-controlled sources only when evidence supports it.
3. Write hypotheses with confidence, contradictions, and next missing evidence.
4. Avoid vulnerability claims before reachability/runtime evidence.

Always use `firmware-artifact-contract` before trusting shared artifacts. Every JSON output must include `schema_version`, `generated_at`, `generated_by`, `source_inputs`, `warnings`, and `errors`. Use `missing_tool` warnings or blockers when required tooling is unavailable. Static evidence, sandbox_generated evidence, Qiling-only output, and public writeups are not runtime truth; keep behavior_claim_allowed=false unless observed_runtime_qemu, observed_runtime_live_hook, observed_runtime_live_debugger, or verified evidence proves the target workload was observed.

## Session Continuation

Treat same-session follow-up prompts about the current firmware artifact as continuation signals. Resume from the latest artifact index, hypothesis ledger, next_skill_decision.json, or blockers.json instead of waiting for the user to invoke the skill again explicitly.

## Loop Guard

Do not repeat the same failing action, validation, probe, or handoff when inputs and artifacts have not changed. If the same blocker appears twice, write or update blockers.json with the repeated blocker, stop and ask the user for the missing input or decision. Prefer a lower-cost evidence-gathering step only when it changes the artifact state.

## Outputs

- `sink_source_map.json`
- `hypothesis updates`

## Verification Gate

Do not mark this skill complete until outputs satisfy the routing completion gate and the artifact contract. Evidence levels must progress from E0 to E8 without skipping runtime or duplicate-check gates. `verification-before-completion` is required before claiming a result is valid.

## Safety

Operate only on firmware and runtimes the user is authorized to test. Keep destructive probes disabled by default; record runtime modifications; prefer local evidence and redacted summaries; use exact dates and versions in vulnerability reports; do not install tools without explicit user approval. Do not commit firmware, secrets, proprietary dumps, raw traces, or private vendor material. Do not mass target devices, do not scan public IPs, do not build a weaponized exploit generator, and do not invent CVE IDs.

## Common Mistakes

- Skipping firmware-artifact-contract validation.
- Making a vulnerability claim from static-only evidence.
- Forgetting missing_tool or blocker records when tooling is unavailable.
