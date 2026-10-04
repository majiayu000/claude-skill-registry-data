---
name: ai-agent-case-study
description: "Structure and write design case studies for AI agents, copilots, autonomous workflows, multi-agent systems, and other probabilistic products. Use when a case study must explain autonomy levels, permissions, approval thresholds, steering, observability, user-visible rationale, uncertainty, trust calibration, streaming, latency, orchestration, failures, retries, rollback, state recovery, evals, or human-in-the-loop design."
---

# AI Agent Case Study

Treat the agent as a probabilistic collaborator operating inside a control system. Do not present it as a linear CRUD flow or a magical chat box.

## Start with evidence

Request or inspect the architecture, tool and permission model, interaction states, approval rules, traces, action history, evals, incidents, metrics, research, screenshots, and decision records. If an artifact is missing, mark the gap.

Never request or publish hidden chain-of-thought. Use user-visible rationale, action summaries, provenance, tool calls, diffs, logs, confidence signals, and outcomes.

## Apply SUPERVISE

Read `references/supervise-framework.md`, then cover:

1. **System role and scope**
2. **Uncertainty model**
3. **Permissions and autonomy**
4. **Execution observability**
5. **Recovery and reversibility**
6. **Verification evidence**
7. **Intervention mechanics**
8. **Success telemetry**
9. **Evolution and learning**

Use `assets/ai-agent-case-study-template.md` for a new draft.

## Required distinctions

- Separate model behavior, orchestration behavior, interface behavior, and product outcome.
- Separate designed safeguards from safeguards proven in execution.
- Separate a confidence display from actual calibration evidence.
- Separate system completion from user success.
- Separate latency perception from raw model latency.
- Show both the autonomous path and the human intervention path.

## Narrative order

Lead with the supervisory problem and pivotal control decision. Then explain the system boundary, human-agent interaction model, observability, failure recovery, trade-offs, validation, outcomes, and limitations.

Avoid generic process theater. Include interviews or personas only when they changed a control, trust, or system decision.

## Done

The reader can reconstruct:

- what the agent may perceive, decide, and change;
- when it acts silently versus requests approval;
- how the user pauses, steers, corrects, rejects, or reverses work;
- what the interface reveals during long-running or failed execution;
- which signals calibrate trust without implying certainty;
- what evidence proves the claimed outcome.
