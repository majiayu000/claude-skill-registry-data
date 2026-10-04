---
name: crew-review
description: Run bounded creative review using Critique-Correct-Verify or Debate-Judge for consequential story, screenplay, directing, storyboard, or shot decisions, with explicit criteria, persistent verdicts, and escalation instead of endless loops.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Crew Review

## Workflow

1. Read core contract and `COLLABORATION_PROTOCOLS.md`.
2. Define one review scope and the criteria before creating any alternate or critique.
3. Choose `Critique-Correct-Verify` for fixable quality failures. Choose `Debate-Judge` for a real choice between materially different approaches.
4. If one model performs multiple roles, isolate the passes and do not claim independent model consensus.
5. Save durable review rounds under `00_project/reviews/<scope-id>/` when the decision affects downstream work.
6. Obey the protocol iteration cap. After repeated failure or an authority conflict, record `ESCALATE` and state the exact decision needed.
7. Apply accepted corrections through the owning specialist skill. A reviewer does not silently edit an approved upstream artifact.

## Done

The scope has a PASS or an explicit escalated decision, the criteria and unresolved items are recorded, and the review did not exceed its bounded iteration count.
