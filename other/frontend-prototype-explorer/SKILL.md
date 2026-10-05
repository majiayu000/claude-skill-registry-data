---
name: frontend-prototype-explorer
description: "Build disposable experiments for unresolved UI or state decisions. Use when code and documentation cannot settle the question; exclude approved implementation and small edits."
id: "agents.skills.frontend-prototype-explorer.skill"
title: "Frontend Prototype Explorer"
doc_type: "skill"
layer: "skill"
status: "active"
publishable: true
local_only: false
skill: "frontend-prototype-explorer"
tags: []
parent:
  - "[[AGENTS|Canonical Agent Policy]]"
related:
  - "[[common/domain-glossary-rules]]"
  - "[[templates/decision-log]]"
depends_on: []
---

# Frontend Prototype Explorer

Maturity: experimental. Validate a consequential UI or state decision through
a disposable experiment before production implementation.

## Purpose

Answer one unresolved question with the cheapest runnable artifact. Preserve
the decision and evidence, not an accidental production implementation.

## When To Use

- Compare interactive UI alternatives when descriptions cannot settle usability.
- Exercise a state model through cancellation, delayed responses, or recovery.
- Investigate a consequential choice that source and documentation cannot settle.

## When Not To Use

- Implementing an already approved layout or feature.
- A small style edit, routine bugfix, or question answered by existing source.
- Planning-only requests that do not authorize building an experiment.
- Backend, production data, benchmarking, or new infrastructure outside scope.

## Required Context

1. Apply the active runtime entrypoint (`AGENTS.md` for project targets or
   the native runtime prelude for plugin targets) and the confirmed question
   and constraints.
2. Inspect only the existing stack, commands, and affected ownership needed.
3. Read `common/domain-glossary-rules.md` when domain terms matter.
4. Read `common/verification-loop-rules.md` for executable observations and
   `common/rendered-visual-verification-policy.md` if UI interaction is needed.

## Tool Contract

Use available project-file and command capabilities. A callable browser is
required for claims about rendered interaction, not for a headless state probe.
Use existing dependencies. Tool or package installation, external mutations,
and production access retain their existing authorization boundaries.

## Workflow

1. State one question, what observation would change the decision, and the
   bounded experiment scope. Resolve facts from code before asking questions.
2. Choose an isolated scratch directory or disposable worktree outside production
   source and build inputs. Never overwrite an existing experiment. State the
   allowed files, stop condition, and attempt/time budget before implementation.
3. Build the minimum probe with synthetic in-memory data and one launch command.
   For usability, compare meaningfully different interactions on the same data;
   for logic, expose transitions and resulting state. Avoid production services,
   durable user storage, test infrastructure, and speculative abstractions.
4. Run the relevant cases and record observations. If a tool is unavailable,
   record blocked evidence. For subjective usability, present the alternatives
   and collect user judgment; agent preference alone is not user validation.
5. Stop when the question is answered, the budget is exhausted, or evidence is
   blocked. Report inconclusive results without defaulting to a preferred option.
6. Record Question, Observations, Decision, Limitations, and Evidence reference
   in the existing local decision log when durable work warrants it. Include
   rejected alternatives only when actually considered.
7. Hand the decision to the design/architecture or execution planner. Production
   implementation is a separate approved slice with its own acceptance checks.
   Do not silently promote prototype code, merge its branch, publish it, or
   delete artifacts owned by the user. Keep an evidence pointer for resumption.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Report the answered question, launch command or artifact, observations,
decision or pending user judgment, limitations, and next implementation step.
State experimental maturity. Do not report production readiness from a probe.

## Validation Gates

- One question and explicit budget bound the experiment.
- Production source, dependencies, and real data remain outside the experiment.
- Claims are tied to executed observations or clearly marked user judgments.
- Blocked or inconclusive evidence is not success.
- A decision survives the session, with the scope of what was actually tested.

## Trigger Evals

Should trigger:

- "Compare two interactive filter placements using disposable data before we choose."
- "Prototype cancel and retry transitions to decide whether this state model works."
- "Try a throwaway preview interaction; stop after answering the navigation question."

Should not trigger:

- "Implement the approved preview layout."
- "Change the prototype button color in this one file."
- "Explain this existing state reducer without making changes."

## Reference Map

- `common/domain-glossary-rules.md`
- `common/verification-loop-rules.md`
- `common/rendered-visual-verification-policy.md`
- `templates/decision-log.md`
