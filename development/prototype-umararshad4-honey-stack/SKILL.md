---
name: prototype
description: "Build a throwaway prototype, or several, to settle a design question before committing."
disable-model-invocation: true
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "mattpocock/skills prototype (Codex copy, + LOGIC.md, UI.md); cursor/plugins pstack 0.15.25 principle-exhaust-the-design-space, arena"
---

# Prototype

A prototype is throwaway code that answers one question. The answer is the deliverable. The code is scaffolding for getting it, and it goes when the answer is in.

## 1. State the question

Write one sentence and what would settle it, at the top of the prototype: "Does the refund state machine stop a double refund? Settled if the walkthrough can't reach two `Refunded` events." A prototype that answers the wrong question is pure waste, so make it checkable.

Pick the branch:
- **Spike**: one question, one candidate answer to check (section 2).
- **Design it N ways**: the user asks for options, or the choice is a novel UI or architecture with no precedent in the repo, or it turns on feel rather than logic (section 3).

Pick the shape from the question:
- **Logic, state, data shape**: a pure module (reducer, state machine, or plain functions) with no DOM or I/O, driven by a thin harness. The harness is a script that prints the full state after every step, or one self-contained HTML file with a button per action and labels in domain language, so a non-developer can drive it by double-click.
- **Looks and layout**: variants rendered on the real page that will host it, behind a `?variant=` param, with real data and the real header around it. An empty route hides problems a populated one shows. A new throwaway route is the last resort.
- **Timing, performance, external behavior**: a script against the real thing that prints the measurement.

Done when: the question and its settling result are written down, and the branch and shape are chosen.

## 2. Spike

Put it somewhere obviously disposable:
- Standalone: `${TMPDIR:-/tmp}/proto-<slug>/`.
- Needs the repo's imports or routes: next to its future home, named so nobody mistakes it (`<name>.prototype.ts`, a route with `prototype` in the path), following the repo's existing conventions.

Build rules:
- One command or one double-click to run. Print that command.
- State in memory. Persistence only when persistence is the question, then a scratch store named `PROTOTYPE-wipe-me`.
- No tests, no error handling beyond what makes it run, no abstractions, no "what if later".
- Show the whole relevant state after every action or variant switch, so the change is visible.
- Keep the logic separate from the harness, so the validated part can lift out on its own.

Run it yourself and read the output. If it keeps growing, the question was too big: split it and spike the first half.

Done when: it ran, and the output answers the question or shows the question was wrong.

## 3. Design it N ways

Your first idea is unlikely to be the best. Build two or three sketches that disagree in structure, then pick.

1. **Frame.** Same question and constraints for every sketch, plus a rubric of three to five gradeable criteria, written before any sketch exists.
2. **Diverge.** Give each sketch a different constraint: smallest surface; most flexible; the common case trivial; borrowed from a named paradigm. UI variants differ in layout, hierarchy and primary affordance, not colour or copy. If two come out alike, redo one with "not a <shape of the other>".
   Run each in its own subagent with its own directory (`proto-<slug>/a`, `/b`, `/c`), each returning the sketch and three lines: what it optimises, what it gives up, what it rejected. Without subagents, build them one after another and finish each before starting the next.
3. **Compare.** Run every sketch and score it against the rubric, criterion by criterion. UI: put all variants on one route with a dev-only switcher (arrow keys, hidden in production builds) so the user can flip between them. Write where the sketches diverge most.
4. **Pick.** Recommend one base and graft at most one or two parts from the others, by hand, so the result keeps one mental model. Sketches that converge are strong agreement: take the shared shape. Sketches that diverge wildly mean the frame was vague: sharpen it and rerun. Logic picks rest on the rubric; taste picks are the user's, so show the variants with your recommendation.

Done when: one sketch (or a named hybrid) is picked, with the rubric scores behind it.

## 4. Capture and clean up

1. **Report the finding**: the question, the verdict, the evidence (output, measurement, the winning variant), what it means for the real code, and what the prototype did not test.
2. **Put the decision where decisions live**: the plan, the ticket, or an ADR through the `domain` skill when it qualifies.
3. **Remove the code.** Delete the prototype files, variants and switcher from the working tree. If the user wants the prototype kept as a primary source, it goes on a throwaway branch and the plan or ticket links that branch.
4. **Fold in properly.** The validated logic is rewritten as production code, test-first through the `tdd` skill. Prototype code was written without tests or error handling.

Done when: the finding is reported and `git status` shows no prototype files.

## Red flags

| Thought | Instead |
|---|---|
| "I'll add a few tests to the prototype" | A prototype that needs tests has become the product. Answer the question, then build it properly. |
| "These three variants are cards in different colours" | That's one design. Make them disagree on structure. |
| "The spike works, I'll just keep it" | Keep the decision. Rewrite the code under `tdd`. |
| "I'll ask the user which approach is faster" | That's observable. Spike it and bring the number. |
