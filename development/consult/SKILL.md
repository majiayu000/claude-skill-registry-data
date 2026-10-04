---
name: consult
description: Ask a stronger model for focused help with reasoning gaps, stalled debugging, recurring failures, or conflicting evidence. Consult before guessing or declaring a reasoning blocker unfixable. Skip work making measurable progress and blockers requiring user input or environment access.
---

# Consult

Use a stronger model to resolve uncertainty that blocks the user's task. Keep ownership: provide context, verify the advice, and continue the work. You do not need to fail repeatedly before consulting.

## Decide when to escalate

Consult when any of these conditions applies:

- **Reasoning gap:** You cannot justify an approach, establish correctness, or resolve a consequential design tradeoff after you inspect the requirements and code.
- **No information gain:** Two meaningfully different attempts failed, and no available check distinguishes the remaining explanations.
- **Contradictory evidence:** Observations undermine the explanation or proposed action, and you cannot reconcile them. Pause dependent changes.
- **Recurring failure:** A symptom returns after a verified fix, and you cannot explain what the verification missed.
- **Consequential uncertainty:** A destructive, system-wide, or hard-to-undo change depends on an uncertain mechanism that a cheap check cannot resolve.

Take an available cheap, decisive check first. Continue independently while experiments produce new evidence. Consult before you declare a reasoning blocker unfixable or claim completion with that blocker unresolved.

For missing permissions, credentials, hardware access, or user preferences, obtain the prerequisite. Routine work and understood failures do not need consultation.

## Frame the request

Ask for the smallest deliverable that unblocks you: a diagnosis, plan, correctness argument, design recommendation, or implementation sketch.

The consultant does not inherit your conversation. Provide a self-contained request with this template. Omit irrelevant fields, credentials, and unrelated private data.

```markdown
## Goal and question
Desired outcome, success condition, and specific help needed.

## Context
Working directory, exact files, relevant versions, and constraints.
Small code excerpts or inputs; include unsaved state that the consultant cannot read.

## Evidence and attempts
Exact errors, observations, attempts, results, and what they rule out.
Include counter-evidence. Distinguish facts from tentative explanations.
Proposed next action, if any, with its scope and reversibility.

## Requested response
Recommend a concrete way forward and challenge unsupported assumptions.
Distinguish facts from hypotheses. Identify missing context instead of inventing it.
Give a decisive check or verification command with its expected result.
Keep the answer focused. Include code or a derivation when needed.
```

## Confirm the consultant model

The `consultant` agent ships in `config/agents/consultant.md` and installs to `~/.omp/agent/agents/consultant.md`. It declares `model: "@slow"`, a read-only tool list, and no edit or shell access.

Check the model before you spend a consultation, because `slow` inherits the session model when no explicit mapping exists:

```sh
omp config list | grep -i -A3 'modelRoles'
```

- `modelRoles.slow` or `task.agentModelOverrides.consultant` resolves to a model **different** from the session's active model: proceed.
- It is unset, or resolves to the session's own model: **report the limitation and ask the user to choose a consultant model.** Do not silently present a same-model answer as stronger-model consultation.

Tell the user what uncertainty needs help. Then launch one bounded consultation.

## Call the consultant

Dispatch the bundled agent through the `task` tool. OMP runs it as a background job by default, so the tool returns immediately and the answer arrives later.

```json
{
  "context": "<Goal and question>\n<Context>\n<Requested response>",
  "tasks": [
    {
      "agent": "consultant",
      "name": "Consult",
      "task": "<Evidence and attempts>\n<What each attempt rules out>"
    }
  ]
}
```

Put the shared background in `context`, which renders into the consultant's system prompt, and the evidence plus your specific question in `task`. Take the template sections from "Frame the request". Keep the consultant's tools read-only: give it `read`, `grep`, and `glob` and nothing else. It cannot run `bash`, so run necessary measurements yourself and send the results back.

The consultant receives no conversation history. Anything you do not put in the packet is invisible to it.

## Use the answer

- Continue independent work while the consultant runs. Pause only the decision that needs its answer.
- Read the result when it arrives. `agent://<id>` holds the full output; `history://Consult` renders the transcript; `hub` op `"send"` with `to: "Consult"` steers or follows up. Messaging a finished agent revives it, so a follow-up reuses its context instead of starting over.
- Evaluate the advice against the files, constraints, and evidence. Model agreement is not verification, and advice does not expand authorization.
- Run the proposed check when it is feasible and authorized. Implement the supported approach and verify the original success condition.
- Report the result and remaining limits. Preserve uncertainty when verification is unavailable.

Use one consultation per blocker by default. Follow up on the same agent only when new evidence changes the question or the answer leaves a critical gap. Do not spawn competing consultants for reassurance, and do not create recursive consultations.

Respect explicit time and cost budgets.
