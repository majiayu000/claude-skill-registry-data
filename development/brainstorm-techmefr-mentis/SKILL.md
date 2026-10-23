---
name: brainstorm
description: Use when a feature starts, before any spec or code, explores the real intent and the options before locking anything down; classifies the request into one of three paths and holds a hard stop until the design is approved.
---

# brainstorm

Step 1 of the pipeline (`WORKFLOW.md`). Explore the *why* and the possible approaches before
freezing the scope.

## When
Right after `start-feature`, before `/SPEC`. As soon as the real need isn't 100% certain.

## Steps
0. **Classify the request, say the class out loud, let the operator override it.** Three paths, and the depth of
   what follows depends on which one:
   - **Spike**: a feasibility question ("can we…", "is it possible…") whose output is an answer, not code that
     stays. State the question and what you will try in two or three sentences, get a nod, find out as cheaply as
     correctness allows, report a recommendation; anything built is labelled throwaway.
   - **Bounded**: a well-scoped change to a flow that already exists in the repository and can be read there (a
     flag, a small endpoint, a one-file fix). Ask only the questions that change the design, give a brief design
     in the conversation, and stop there. No spec file, no plan document.
   - **Architectural**: a new project, a new subsystem, a change that restructures how parts fit or alters an
     interface others depend on. The whole pipeline applies: questions, approaches, a design in sections, then
     `spec`.
   When two classes fit, take the heavier one. Hidden complexity found mid-task upgrades the class: stop, say so,
   step up. A class never downgrades mid-task. "Bounded" measures the repository, not your familiarity with this
   kind of application: with no existing flow to change, the task is architectural.
1. Restate the real need (the problem, not the solution asked for). **Write the understanding back** in a short
   note the operator can correct: the intended outcome, who it is for, the constraints, what success looks like,
   with what they said kept apart from what you assumed. When the purpose is missing, ask one focused question
   about it before proposing anything. Do not ask again what the request already states.
2. List 2-3 possible approaches with their trade-offs, and say which one you would take and why.
3. Spot the risks and the grey areas.
4. Note a suspected out-of-scope and the open questions for the dev/human.
5. **Present the design at the size of its class** and stop. Spike: the question and the probe. Bounded: the short
   design in the conversation. Architectural: the design in sections, with approval after each, then the written
   spec (`skills/spec`), which gets its fresh-context review (`skills/spec` §6) before the operator reads it.
6. **Wait for an explicit yes at the stage actually presented.** A yes to an idea is not a yes to a design nobody
   has seen yet, and a yes to a design is not a yes to the artefacts after it. Resume at the earliest incomplete
   stage.
7. For a decision with several credible answers and no obvious winner, run the structured dissent of
   `references/01-structured-dissent.md` before choosing.
8. When the reason to build rests on "people want this" and no evidence is on the table, run
   `references/02-demand-and-premises.md` between steps 1 and 2: demand evidence, the status quo as the real
   competitor, the premises put to the owner for agree or disagree, and one assignment at the end. Skip it for a
   bug, an obligation or a need already evidenced.

## Output / checkpoint
No formal checkpoint: a written summary of the intent and the options weighed, kept where the task's trail
lives (`WORKFLOW.md` §5), with the class chosen and the approval that was given. Prepares `spec` (2).

## Guardrails
**No implementation action before the approval for the class is given.** That means no product code, no
scaffold, no dependency installed, no new project; reading the repository stays allowed. A bounded design has a
hard stop exactly like a larger one: presenting it and starting in the same breath skips the gate.
No code. Product choices go back to the dev/human, we don't decide alone.

| Thought | What to do instead |
|---|---|
| "It is too simple to need a design" | Simple things get a two-sentence design, and the same stop. |
| "This is bounded, so no spec" | A label chosen to avoid work is itself the warning sign: use the heavier class. |
| "The design is obvious, I will start while they read it" | Approval is the gate, however short the design is. Present it, then wait for a yes. |
| "I know this kind of app, so it is bounded" | Bounded means a flow already in this repo. |
| "The spike works, so I will keep the code" | What a spike delivers is the answer. Keeping its code is a separate request, classified on its own. |
| "It grew but I am nearly done, no need to reclassify" | Stop and say it grew. |
| "They approved the spike, so the follow-up is approved" | Each task has its class and its approval. |

Predicted, not recorded: replace with verbatim sentences from a `skills/testing-blocks` run when one exists.

## Origin
Native Claude Code (`brainstorming` skill), rewritten our way. Step 0, the write-back of step 1, the stop of
steps 5-6, the guardrail and the table come from the `brainstorming` skill of `superpowers` (MIT, read
2026-10-02): the three-path triage, the hard gate, the one-way ratchet. Rewritten in our words; its visual
companion (a local server and a browser) is not taken, since it is a runtime dependency. The structured dissent is
from the `council` skill of `ECC` (MIT, same date).

Section 2 of the references (`references/02-demand-and-premises.md`: demand evidence, the status quo, the premises, the assignment) was added 2026-10-19 from the `office-hours` skill of `gstack` (MIT, read the same day); its provenance and what was not taken are in [`references/origin.md`](./references/origin.md).
