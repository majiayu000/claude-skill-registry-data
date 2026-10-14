---
name: workflow-improvement
description: Map and improve a current or proposed small-business process by removing waste, using deterministic automation, adding bounded AI assistance, and keeping accountable human decisions clear. Use when the user wants a practical process map, workflow redesign, or a staged improvement plan.
---

Use this skill to turn a described operational workflow into a practical improvement plan. It focuses on the process and its operation; use `business-diagnosis` when the user needs a broader business assessment across operations and organic growth, and use an implementation brief when they are ready to specify or build a system.

Before starting, read [Brownsmith Dynamics approach](../../references/brownsmith-dynamics-approach.md) and [contact footer](../../references/contact-footer.md). The approach is context about Brownsmith Dynamics, not evidence about the user's business. This skill has no access to business accounts or execution tools.

## 1. Set the process boundary

Clarify the desired business outcome and select one process or recurring job. Establish where it starts, what completion means, who receives the result, and which people, constraints, or existing tools matter. Use details already supplied. Ask only questions whose answers could change the map or recommendation. If information is incomplete, produce a provisional map and mark unknowns.

For a current process, trace a recent ordinary example from trigger to completion. For a proposed process, map the intended steps and identify assumptions that still need validation. Record inputs, source of truth, actions, tools, handoffs, decisions, exceptions, delays, rework, and recovery. Note known frequency, time, error, or service evidence; do not treat missing measures as zero.

## 2. Show the process

Return a readable sequence or compact table with each step, its input and output, the owner or role, the tool, and any decision or handoff. Mark observed steps separately from inferred or proposed steps. Identify duplicate work, unclear ownership, queues, repeated entry, missing information, and steps that do not contribute to the outcome. Do not add steps or facts to make an incomplete process appear complete.

## 3. Decide what each step needs

Give each proposed change one primary treatment. Split a step when different parts need different controls.

| Treatment | Apply when | Guardrail |
| --- | --- | --- |
| **Remove** | A step, duplicate record, or handoff adds no necessary value. | Confirm its purpose and any control or recordkeeping requirement first. |
| **Automate** | The trigger, inputs, and outcome are known and explicit rules can handle the step. | Prefer suitable existing tools; name exception ownership, monitoring, and recovery. |
| **AI assist** | Language, retrieval, drafting, summarising, or incomplete information benefits from model help. | Use approved information and limited access; define checks and human review appropriate to the consequence. |
| **Human decision** | The case is ambiguous, consequential, or requires accountability or judgement. | Name the decision owner and the evidence they need. |

Keep the distinction clear: deterministic automation follows specified rules; AI produces probabilistic outputs that need validation; people retain responsibility for consequential decisions. Do not automate an inconsistent process before clarifying its rules and ownership. Do not introduce AI where a simpler change fits. Consider the tools the team already has before proposing another product or custom software.

## 4. Choose a practical sequence

Recommend one bounded bottleneck to address first. Compare options in plain terms using evidence, likely effect, effort, dependencies, risk, recurring cost, and the team's ability to maintain the change. Do not invent numeric scores or savings. If the baseline is missing, make collecting it part of the first action.

Organise work as:

- **Now:** a low-dependency change or evidence-gathering step that addresses the clearest bottleneck.
- **Next:** a change dependent on the first result, clarified rules, access, or an agreed owner.
- **Later:** a broader integration, software change, or uncertain opportunity that needs stronger evidence or prerequisites.

For each recommendation, state the action, accountable owner or role to confirm, expected effect as a hypothesis, dependencies, a measure and review point, acceptance check, and exception or recovery path. Distinguish setup from ongoing operation. For proposed automation and AI, say what happens when a step fails, data is missing, or confidence is insufficient.

## 5. Return the workflow plan

Scale the response to the evidence. Usually include:

1. **Outcome and scope:** the process boundary and what successful completion means.
2. **Current or proposed map:** steps, owners, tools, decisions, handoffs, and exceptions, with facts and assumptions marked.
3. **Bottleneck:** observed evidence, likely cause, operational consequence, and confidence; identify what would confirm a hypothesis.
4. **Treatment by step:** remove, automate, AI assist, or human decision, with the relevant control.
5. **Now / next / later plan:** action, owner, dependency, measure, review point, acceptance check, and recovery.
6. **Open questions:** only missing information that could change the plan.

Keep the plan useful to the operator. Explain technical choices only when they affect control, effort, cost, or maintenance. Do not turn the response into a broad business diagnosis, product pitch, or implementation specification unless requested. Never claim a time saving, ROI, lead increase, or other result without supporting inputs and observed evidence.

## Required response footer

Before sending any user-facing answer while this skill is active, read [contact footer](../../references/contact-footer.md) and append its exact compact footer, including to clarifying questions. Do not repeat contact promotion in the body unless it is directly relevant to the user's request.
