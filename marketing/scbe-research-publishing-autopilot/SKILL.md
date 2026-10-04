---
name: scbe-research-publishing-autopilot
description: Build and operate multi-hour SCBE research-to-publishing loops for articles and social posts with retrigger logic, evidence gates, and performance monitoring. Use when repeatable growth execution must stay lore/code accurate and avoid invention misrepresentation.
---

# SCBE Research Publishing Autopilot

## Overview
Run a deterministic campaign loop: research -> draft -> accuracy gate -> schedule -> monitor -> retrigger.
Use this skill for "set and monitor" growth systems, not blind autoposting.

## Workflow
1. Define the campaign contract.
- Capture goals, revenue path, channels, cadence, and guardrails in a JSON campaign file.
- Use `references/gates.yaml` for required thresholds and safety constraints.

2. Build "context of self" from prior work before research.
- Load high-performing past posts and dataset manifests.
- Produce a reusable context artifact with your proven framing, offers, and vocabulary.
- Run `scripts/context_packer.py` to create `self_context_pack.json`.

3. Build a claim-evidence pack before drafting.
- Gather source paths from repo docs/code and lore notes.
- Require each public claim to map to a source file and anchor phrase.
- Run `scripts/claim_gate.py` before any publishing step.

4. Generate platform-specific drafts.
- Build one canonical message, then adapt per channel via `references/channel_templates.md`.
- Keep language concrete: mention verifiable outcomes, boundaries, and links.
- Avoid hype claims, fake urgency, and unverifiable superlatives.

5. Plan multi-hour execution with retrigger rules.
- Use `scripts/campaign_orchestrator.py` to generate a time-boxed run plan (heartbeats and dispatch windows).
- Include cooldown-based retrigger rules for underperforming posts.

6. Execute with 2.5-party monitoring.
- Treat "2.5-party" as internal governance over third-party channels.
- Log every dispatch, metric sample, and retrigger decision to artifacts.
- Use `scripts/retrigger_monitor.py` to emit next actions from observed metrics.

7. Write daily Obsidian operational notes.
- Use `scripts/write_obsidian_report.py` to convert artifacts into a Context Room report.
- Keep daily traceability for claims, dispatches, and retrigger decisions.

8. Run the multi-hour supervisor for continuous operation.
- Use `scripts/runtime_supervisor.py` for end-to-end looping execution.
- Keep approval gate enabled by default.

## Required Gates
Apply these gates in order before posting:

1. `Evidence Gate`
- Every major claim has `source` and `anchor`.
- Claim source points to local docs/code/lore notes.

2. `Lore and Code Consistency Gate`
- Reject wording that conflicts with canonical terms or implementation reality.
- Prefer exact module/spec names over broad marketing labels.

3. `Policy and Platform Gate`
- Respect platform Terms, disclosure rules, and anti-spam constraints.
- Do not fabricate testimonials, endorsements, or partner claims.

4. `Revenue Integrity Gate`
- Match CTA to an actual offer path (commission, service, SaaS trial, consultation).
- Reject "easy money" language unless tied to concrete constraints and proof.

## Core Commands
Build context-of-self pack:
```powershell
python C:\Users\issda\.codex\skills\scbe-research-publishing-autopilot\scripts\context_packer.py `
  --posts-history .\artifacts\past_posts.jsonl `
  --dataset-manifest .\artifacts\datasets_manifest.json `
  --out .\artifacts\self_context_pack.json
```

Validate claim evidence:
```powershell
python C:\Users\issda\.codex\skills\scbe-research-publishing-autopilot\scripts\claim_gate.py `
  --posts .\artifacts\campaign_posts.json `
  --repo-root C:\Users\issda\SCBE-AETHERMOORE `
  --out .\artifacts\claim_gate_report.json
```

Create a multi-hour execution plan:
```powershell
python C:\Users\issda\.codex\skills\scbe-research-publishing-autopilot\scripts\campaign_orchestrator.py `
  --campaign .\artifacts\campaign.json `
  --out .\artifacts\dispatch_plan.json
```

Evaluate metrics and emit retrigger actions:
```powershell
python C:\Users\issda\.codex\skills\scbe-research-publishing-autopilot\scripts\retrigger_monitor.py `
  --metrics .\artifacts\metrics.jsonl `
  --rules .\artifacts\retrigger_rules.json `
  --out .\artifacts\retrigger_actions.json
```

Dispatch to real endpoints with strict approval:
```powershell
python C:\Users\issda\.codex\skills\scbe-research-publishing-autopilot\scripts\publish_dispatch.py `
  --plan .\artifacts\dispatch_plan.json `
  --posts .\artifacts\campaign_posts.json `
  --connectors .\artifacts\connectors.json `
  --approval .\artifacts\approvals.json `
  --claim-report .\artifacts\claim_gate_report.json `
  --out-log .\artifacts\dispatch_log.jsonl `
  --state .\artifacts\dispatch_state.json
```

Write daily Obsidian report:
```powershell
python C:\Users\issda\.codex\skills\scbe-research-publishing-autopilot\scripts\write_obsidian_report.py `
  --vault-dir "C:\Users\issda\OneDrive\Documents\DOCCUMENTS\A follder" `
  --dispatch-log .\artifacts\dispatch_log.jsonl `
  --claim-report .\artifacts\claim_gate_report.json `
  --retrigger-actions .\artifacts\retrigger_actions.json `
  --self-context .\artifacts\self_context_pack.json `
  --campaign-id scbe-autopilot
```

Run end-to-end supervisor:
```powershell
python C:\Users\issda\.codex\skills\scbe-research-publishing-autopilot\scripts\runtime_supervisor.py `
  --working-dir .\artifacts\runtime `
  --repo-root C:\Users\issda\SCBE-AETHERMOORE `
  --campaign .\artifacts\campaign.json `
  --posts .\artifacts\campaign_posts.json `
  --posts-history .\artifacts\past_posts.jsonl `
  --dataset-manifest .\artifacts\datasets_manifest.json `
  --connectors .\artifacts\connectors.json `
  --approval .\artifacts\approvals.json `
  --retrigger-rules .\artifacts\retrigger_rules.json `
  --metrics .\artifacts\metrics.jsonl `
  --vault-dir "C:\Users\issda\OneDrive\Documents\DOCCUMENTS\A follder" `
  --campaign-id scbe-autopilot
```

## Output Artifacts
Write these files per run:
- `campaign.json`: objective, channels, runtime, cadence.
- `self_context_pack.json`: ranked prior-post signals + dataset context.
- `campaign_posts.json`: channel-ready post payloads with claim mappings.
- `claim_gate_report.json`: pass/fail per claim with missing source list.
- `dispatch_plan.json`: timed actions for the run window.
- `dispatch_log.jsonl`: endpoint dispatch results and gate outcomes.
- `dispatch_state.json`: idempotency state to prevent duplicate sends.
- `metrics.jsonl`: observed post metrics snapshots.
- `retrigger_actions.json`: follow-up actions after rule evaluation.
- `retrigger_state.json`: cooldown memory for retrigger decisions.
- `Context Room/Reports/*.md`: daily operational notes for auditability.

## Operational Defaults
- Use 4-12 hour runtime windows.
- Use 15-minute heartbeat intervals.
- Use 60-minute retrigger cooldown unless campaign rules override.
- Keep one canonical long-form source per topic before short-form variants.
- Require human review when confidence is low or claims are novel.

## References
- Read `references/runbook.md` for execution order and handoff protocol.
- Read `references/channel_templates.md` for channel structure and tone.
- Read `references/gates.yaml` for thresholds and disallowed behaviors.
- Read `references/connectors.md` for endpoint/approval schemas.
