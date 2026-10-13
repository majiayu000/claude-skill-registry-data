---
name: teach
description: Teach a concept, walk through a session, or conduct an explicitly requested ongoing course.
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
---

# Teach

Teach the requested concept at the learner's chosen depth. A single explanation
or session walkthrough does not imply a course or persistent learning workspace.

## Choose the learning shape

- One concept: explain with a relevant example and invite a focused question.
- Session walkthrough: cover the problem, decision, implementation and consequences;
  use retrieval questions to expose gaps, without requiring total mastery to stop.
- Ongoing course explicitly requested: use the optional workspace below.

Infer level from the conversation, then adjust from the learner's responses.
Separate what happened from why it was chosen. Use a small exercise or prediction
question when useful; give feedback after the learner responds. Quiz options
should be plausible and avoid answer giveaways, not match exact character counts.
Respect requested pace and stopping points. Check unfamiliar or changing facts
against appropriate sources; cite material external claims.

## Optional durable course

When course artifacts are authorized, use the supplied location and create files
lazily. `MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `LEARNING-RECORD-FORMAT.md` and
`GLOSSARY-FORMAT.md` define the corresponding documents. Keep lessons focused on
an observable learning objective and link useful prior material.

HTML lessons are optional; use html-artifact for a standalone interactive lesson
when that format helps. Reuse existing assets, but do not invent a component
library for a single lesson. Record learning progress only within course scope;
persistent preferences or memory require an explicit request. Never assume the
repository root is a teaching workspace.
