---
name: firmware-candidate-adjudicator
description: Use when a same-session follow-up or candidate evidence bundle needs final duplicate check, report gating, or adjudication after exploitability assessment.
---

# Firmware Candidate Adjudicator

## Overview

Review a candidate before report readiness and duplicate/advisory status. This skill is part of the discovery-first firmware research suite for authorized binary/service exploitability assessment. It preserves blocker-first workflow, compact local evidence, and provenance-first claims.

## Routing

```yaml
role: orchestrator
purpose: Review a candidate before report readiness and duplicate/advisory status.
when_to_use:
  - Use when a same-session follow-up or candidate evidence bundle needs final duplicate check, report gating, or adjudication after exploitability assessment.
when_not_to_use:
  - Do not use as the main discovery engine or when no candidate/advisory question exists.
required_inputs:
  - exploitability_assessment.json
  - duplicate_check.json
  - candidate evidence bundle
produces:
  - candidate_report.json
  - adjudication_blockers.json
  - next_skill_decision.json
completion_gate:
  - Candidate report reaches E8 only after exploitability and duplicate/advisory checks are complete.
reentry_triggers:
  - Re-enter when duplicate research, root cause, or runtime evidence changes candidate status.
handoff_hints:
  - Route back to duplicate CVE research, exploitability modeling, crash root cause, or report writing.
misuse_signals:
  - The skill is being misused if it invents CVE assignment or promotes static-only claims.
```

## Required Superpowers

- Use `superpowers:systematic-debugging` when validation fails unexpectedly.
- Use `superpowers:verification-before-completion` before claiming an artifact is valid.

## Inputs

- exploitability_assessment.json
- duplicate_check.json
- candidate evidence bundle

## Workflow

1. Check evidence ladder status.
2. Confirm duplicate/advisory coverage and version applicability.
3. Reject unsupported CVE IDs and static-only vulnerability claims.
4. Write candidate report readiness or blockers for human review.

Always use `firmware-artifact-contract` before trusting shared artifacts. Every JSON output must include `schema_version`, `generated_at`, `generated_by`, `source_inputs`, `warnings`, and `errors`. Use `missing_tool` warnings or blockers when required tooling is unavailable. Static evidence, sandbox_generated evidence, Qiling-only output, and public writeups are not runtime truth; keep behavior_claim_allowed=false unless observed_runtime_qemu, observed_runtime_live_hook, observed_runtime_live_debugger, or verified evidence proves the target workload was observed.

## Session Continuation

Treat same-session follow-up prompts about the current firmware artifact as continuation signals. Resume from the latest artifact index, hypothesis ledger, next_skill_decision.json, or blockers.json instead of waiting for the user to invoke the skill again explicitly.

## Loop Guard

Do not repeat the same failing action, validation, probe, or handoff when inputs and artifacts have not changed. If the same blocker appears twice, write or update blockers.json with the repeated blocker, stop and ask the user for the missing input or decision. Prefer a lower-cost evidence-gathering step only when it changes the artifact state.

## Outputs

- `candidate_report.json`
- `duplicate_check`
- `CVE candidate`

## Verification Gate

Do not mark this skill complete until outputs satisfy the routing completion gate and the artifact contract. Evidence levels must progress from E0 to E8 without skipping runtime or duplicate-check gates. `verification-before-completion` is required before claiming a result is valid.

## Safety

Operate only on firmware and runtimes the user is authorized to test. Keep destructive probes disabled by default; record runtime modifications; prefer local evidence and redacted summaries; use exact dates and versions in vulnerability reports; do not install tools without explicit user approval. Do not commit firmware, secrets, proprietary dumps, raw traces, or private vendor material. Do not mass target devices, do not scan public IPs, do not build a weaponized exploit generator, and do not invent CVE IDs.

## Common Mistakes

- Inventing official CVE assignment.
- Skipping duplicate checks.
- Treating a public writeup as local runtime proof.
