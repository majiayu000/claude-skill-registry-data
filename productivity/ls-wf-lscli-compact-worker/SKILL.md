---
name: ls-wf-lscli-compact-worker
description: Qualify and assign a bounded local compact worker task through existing LSCli profiles and native tool calling, without adding a runner.
metadata:
  version: "1.1"
---

Use this workflow to decide whether an existing local compact model/profile can safely complete one small, independent task through LSCli. The controller owns scope, grants, acceptance, and the checkpoint. Do not create another runner, silently change profile configuration, or treat model availability as task qualification.

Write a worker packet before dispatch: one observable outcome; exact read, disclosure, write, and recipe boundaries; allowed tools/files; checks; deadline/resource limits; checkpoint and acceptance criteria. Split coupled work before dispatch. If it cannot be split into an independently verifiable slice, keep it with the controller. Run at most two delegated assistants concurrently. For bounded research, implementation, and tests, follow the active client role configuration and choose the least costly available role capable of the task at an appropriate effort. Use an independent reviewer with capability matched to the risk for material-risk or policy-sensitive results. Preserve the user's active controller selection; do not change global routing.

Qualification has two separate gates: an OpenAI-compatible endpoint handshake proves only transport/schema compatibility; a successful observed native tool round trip through the actual LSCli runner is required before assigning tool-enabled work. Capture exact model ID, quantization, chat template, parser/tool-call format and revision. A local Gemma-family Q4 model is an example candidate, never a blanket-qualified model. Measure task completion, invalid tool calls, context use, latency, and resource use on representative bounded tasks before tuning. Preserve working profiles unless comparative evidence supports a change.

Follow the migration and smoke metadata in `workflow.yaml`. Canonical runner and permission contracts are in [LSCLI.md](../../docs/LSCLI.md) and [LSCLI_RUNTIME.md](../../docs/LSCLI_RUNTIME.md); compose [LocalSetup Agent-* lane routing](../../skills/ls-agent-capability-routing/SKILL.md) and [task matching](../../skills/ls-task-skill-matcher/SKILL.md) rather than duplicating them. The LocalSetup lane matrix recommends a task lane; it does not select a client model, effort, or worker configuration. Follow the active client's role configuration for those choices. The controller reviews the result against the packet and records the existing LSCli checkpoint; tool output or a worker report alone is not acceptance.
