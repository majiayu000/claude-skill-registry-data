---
name: feynman-teachback
description: "Trigger: feynman, teach back, teach-back, explicamelo, metodo feynman, learn teach. Diagnose learner explanations and return gaps without automatic mutations."
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "3.0.0"
---

# Feynman Teach-Back

## Activation

Use a learner explanation to diagnose causal understanding of a supplied concept, especially where understanding is uncertain. Do not turn this into a lecture or require it after equivalent evidence already exists.

## Inputs

Required: concept and reference answer or source material. Optional: learner explanation, prior observations, and language. No topic state is necessary.

## Method

Invite the learner to explain to a curious novice. Listen without completing sentences or correcting every phrase mid-explanation. Ask one short question at a time in normal chat, then wait: why a step works, what a term means, or what changes in a new case.

Classify material gaps as missing piece, hand-waved step, wrong claim, or jargon crutch. Ground each finding in the actual explanation and reference. Give specific corrective feedback after the attempt, then let the learner try again.

Use an example, counterexample, or analogy only when it reveals understanding. Never require an analogy regardless of topic. Reuse an existing correct explanation or novel application rather than demand a duplicate ritual.

Agree a focused return path for remaining gaps: a supplied source passage, targeted explanation, or new learner attempt. A teach-back never changes stored progression by itself; it produces a diagnostic proposal only.

## Output

Return the observed explanation, questions, classified gaps, suggested return paths, and verdict inline. Use `assets/teachback-template.md` when a structured record is requested. Quote learner evidence faithfully; never claim unobserved delayed retention or invent practical mastery. No sibling calls, state discovery, or writes.
