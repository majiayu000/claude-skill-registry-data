---
name: learning-session
description: "Trigger: one-off /learn session, bounded explanation, learn something now. Independent answer-first teaching from supplied inputs; no automatic state."
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "2.0.0"
---

# Learning Session

## Activation

Teach one bounded concept or answer a learning question now, including explicit `/learn session` requests. Accept supplied source material directly. Do not start a multi-session route or a book-publishing workflow.

## Inputs

Required: the concept or question. Optional: learner level, source material, materials language, and a request for a summary draft. Default to the conversation language; ask only for information essential to teach accurately.

## Method

Lead with the answer and central model. Show a small worked example distinct from any task the learner should solve. Explain the causal steps and preserve technical literals, negations, and limitations.

Adapt depth to the learner's actual response. Offer one useful retrieval or transfer question when it helps; ask it in normal chat and wait. Correct a material gap specifically, then invite another attempt. Do not supply the learner's answer or turn a complete explanation into a compulsory interview.

Use only needed, actually available evidence; name uncertainty and sources honestly. A diagram is optional when it explains a relationship better than prose.

## Output

Return useful teaching inline. On explicit request, also return a summary draft grounded in the supplied session, with used sources. A teacher's synthesis is not learner evidence.

No state discovery, due-check, file write, or automatic saving. This method needs no named agent, sibling skill, or project directory. A caller may separately save an explicitly requested draft without creating a route or durable state.
