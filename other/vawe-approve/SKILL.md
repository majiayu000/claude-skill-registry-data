---
name: vawe-approve
description: "Give your OK on a film: first the plan, then the full draft. Only the person types this; the agent cannot run it."
disable-model-invocation: true
argument-hint: "[film name] [--param k=v] [--aspect W:H]"
allowed-tools: Bash(node ${CLAUDE_PROJECT_DIR}/harness/live/approve.mjs *)
---

The person typed /vawe-approve. The line below ran before you read this, and it recorded the step that was waiting for the person's OK. Report its output in one sentence. Do not run `approve` yourself, and do not start the next stage in this turn.

!`node ${CLAUDE_PROJECT_DIR}/harness/live/approve.mjs $ARGUMENTS`

If the output says "approve refused", say what it names and stop.
