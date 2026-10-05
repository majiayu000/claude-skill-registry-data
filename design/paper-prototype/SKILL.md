---
name: paper-prototype
description: Create Paper-first UI prototype directions, especially after grill-with-docs has settled product and domain decisions. Use to explore layout, hierarchy, density, flow, or visual framing as editable Paper artboards before committing to code, to compare structurally distinct directions, or to turn settled product decisions into an interface. For throwaway HTML explorations rather than editable Paper frames, use the prototype skill instead. For business-logic or state-machine prototyping use logic-prototype, unless the user explicitly asks for Paper output.
---

# Paper Prototype

Paper is paper.design's design canvas. This skill drives it through the Paper MCP server (paper.design's official MCP), which must be connected.

Paper prototypes are **throwaway UI explorations that answer one design question**.

The main job is to turn settled product/domain decisions into editable Paper directions so the user can make the design call before implementation. Default to 3 directions; use 2 for a small question; never more than 5.

## Default Workflow

Use [UI.md](UI.md) for the full workflow.

Start in Paper when the open question is about:

- layout or information hierarchy
- flow shape
- visual framing
- density
- affordances
- how product decisions should appear in the interface

Do not jump to code for a UI-direction question. The canvas is the shared decision surface.

## Post-Grilling Gate

When this follows `grill-with-docs`, create a one-page Prototype Brief before touching Paper. The brief is a disposable alignment artefact, not a PRD, spec, ADR, or replacement for `CONTEXT.md`.

The Prototype Brief must capture:

- **Goal:** what the prototype is trying to learn or decide.
- **Non-goals:** what the prototype must not reopen, decide, or explore.
- **Settled decisions:** product/domain decisions already resolved by `CONTEXT.md`, ADRs, or the grilling session.
- **Constraints:** canonical terminology, user roles, key states, platform limits, data assumptions, interaction boundaries, and must-preserve rules.
- **Core states:** the minimum states the prototype must represent.
- **Open design questions:** only the UI questions still worth exploring.
- **Good enough:** the exit condition that lets prototyping stop.
- **Sources:** the `CONTEXT.md`, ADRs, notes, or prior artefacts consulted.

Use the brief to constrain the Paper work:

1. Read the relevant `CONTEXT.md` and ADRs.
2. Extract canonical terms, user roles, key states, constraints, non-negotiable product decisions, and open design questions.
3. State the Prototype Brief and ask whether anything is wrong or missing.
4. Use those terms and constraints in the prototype.
5. Prototype only the remaining interface question. Do not re-litigate the product model or silently redefine domain boundaries.

Keep this lightweight. This is alignment, not a second grilling session.

If the brief exposes unresolved product/domain decisions, stop and return to `grill-with-docs`. Do not use Paper to settle domain model questions by accident.

## Fidelity Calibration

Before creating artboards, calibrate the output fidelity if the user has not specified it and the choice would materially change the prototype.

Do not ask every time. If the request implies a level, state the assumption and proceed.

Use these levels:

- **Sketch:** rough boxes, labels, layout ideas, and fast comparison.
- **Structural:** clear hierarchy, real content shape, and visible state coverage, with plain visual treatment.
- **Product-realistic:** plausible app UI with credible components, spacing, density, and interaction affordances.
- **Polished:** presentation-quality visual direction with refined colour, typography, component treatment, and brand feel.
- **Implementation-adjacent:** close enough to guide code, with component, state, responsive, and interaction implications made explicit.

Higher fidelity is not always better. Match fidelity to the question. Use low fidelity for structure and flow decisions; use high fidelity only when visual language, perceived quality, component treatment, or implementation guidance is the question.

If fidelity is ambiguous, recommend one level based on the design question and ask a tight question before creating artboards.

## Prototype Contract

Before creating artboards, state:

- **Question:** what are we trying to learn?
- **Already decided:** the constraints that must carry through.
- **Still open:** what the variants are allowed to disagree about.
- **Fidelity:** sketch, structural, product-realistic, polished, or implementation-adjacent.
- **Exit condition:** what answer lets us stop?

If the remaining uncertainty is business logic, state modelling, persistence, live data, routing, responsiveness, animation feel, keyboard behaviour, component API ergonomics, or implementation feasibility, say so directly. Recommend the appropriate prototype shape instead of forcing Paper to answer a question it cannot answer.

## User Control

The agent proposes directions. The user owns the design decision.

Do not collapse variants into a final direction unless the user chooses one or gives clear instruction. If the user edits the Paper canvas, treat those edits as design feedback and consolidate around them.

## When done

The answer is the only thing worth keeping from a prototype. Summarise:

- the question
- the chosen direction or remaining uncertainty
- what was kept and rejected
- what should happen next

Label the winning Paper frame and add a concise decision note on the canvas. If the work affects durable product/domain decisions, update `CONTEXT.md` or an ADR separately.

The chosen direction hands off to your implementation step (the `build` skill, if you use it) — the labelled frame and its decision note are what it reads.
