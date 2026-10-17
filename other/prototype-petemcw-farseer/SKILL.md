---
name: prototype
description: Build a throwaway but polished prototype that answers a design question. Either several genuinely different UI variants on the real page, flipped live with a floating picker, or a single-file demo that drives a state model through its awkward cases. Use when the user wants to explore what a page or component should look like, compare layouts or directions, or sanity-check whether some logic or a state model feels right.
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

"Throwaway" describes the code's structure, not how it looks. A prototype skips tests, abstractions, and project architecture, but everything the user sees and touches is built to a ship-quality craft bar. People react to whatever is in front of them: show them janky motion or lorem ipsum and the feedback is about the jank, not the idea.

## Pick a branch

Identify the question from the user's prompt or the surrounding code, or ask if the user is around:

- **"What should this look like?"** → [ui.md](./references/ui.md). Several genuinely different variants on the real page, switched live with [picker.md](./references/picker.md).
- **"Does this logic / state model feel right?"** → [logic.md](./references/logic.md). One self-contained HTML file with free-play buttons and guided walkthroughs that a non-developer can drive.

The two produce very different artifacts, so a wrong guess wastes the prototype. If the question is ambiguous and the user isn't reachable, follow the surrounding code (a page or component → UI; a backend module, reducer, or workflow → logic) and state the assumption at the top of the prototype.

## Two kinds of quality

| Polish this (the surface)                                                                                | Skip this (the scaffolding)                                    |
| -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Layout, hierarchy, spacing, typography, using the project's tokens                                       | Tests                                                          |
| Motion: easing, duration, origin, reduced motion ([craft.md](./references/craft.md))                     | Error handling beyond what keeps it runnable                   |
| Every interaction works: hover, press, focus, open, close, empty and loading states the question touches | Abstractions, shared layers, generalizing for later            |
| Realistic content: product-shaped copy, plausible names and numbers                                      | Persistence and real mutations (use in-memory state and stubs) |
| Accessibility basics: focus-visible, contrast, keyboard reachability                                     | Matching the project's file layout and architecture            |

## Rules for both branches

1. **Throwaway from day one, and marked as such.** Put the prototype next to the code it's for so the context is obvious, but name it so a casual reader can tell it's a prototype (`*.prototype.tsx`, a `prototype` path segment). Open every prototype file with a one-line comment stating the question it answers. Follow the project's existing routing and folder conventions; don't invent new top-level structure.
2. **Trivial to run.** A UI prototype is reachable with the project's usual dev command plus a URL. A logic demo is a single file you double-click. Nobody should have to think to start it.
3. **No persistence by default.** State lives in memory. If the question is explicitly about persistence, use a scratch DB or a local file with an obvious "PROTOTYPE, wipe me" name.
4. **Surface the state.** After every action (logic) or variant switch (UI), the relevant state is visible, so the user can see what changed.
5. **Verify before handing over.** Run it yourself. Click every variant, scenario, and interaction; the console is clean. If browser tooling is available, screenshot each variant or scenario. Don't hand over something you haven't driven.
6. **The choice belongs to the user.** Present what you built honestly, with the tradeoffs, and stop. Don't pre-pick a favorite. If asked which you'd choose, give a reason rooted in the product (its personality, how often the thing is used), not taste alone.
7. **Capture it when done.** See below.

## Capture and fold in

When the prototype has answered its question:

1. **Record the verdict.** Write down the question, the answer, and why, in two or three sentences. If there's an implementation issue, put it there with a pointer to the prototype branch (ask before posting to an external tracker). Otherwise it goes in the prototype branch's commit message and is referenced from the implementation commit.
2. **Keep the prototype as a primary source on a throwaway branch.** Commit the whole thing (every variant, the picker, the demo file) to `prototype/<slug>`, branched from the current HEAD. Stage only prototype files. If the working tree has unrelated uncommitted changes that touch the same files, stop and ask first. Don't push unless the user asks.
3. **Rewrite the winner properly on the working branch.** The prototype is polished, but its structure wasn't written to project standards, so don't move it in wholesale. Rebuild it the way the project builds things, carrying over the lessons:
   - **Carry over:** layout and hierarchy, copy, tokens chosen, motion values (easing, durations, origins), the interaction model, and every edge case or awkward state the prototype surfaced.
   - **Redo:** component boundaries, data flow, real mutations and error handling, tests, file placement, naming.
   - For logic prototypes, the pure module was written to be liftable. Move it into the real module and add tests around the cases the walkthroughs covered.
4. **Main keeps only the decision.** Losing variants, the variant switch, and the demo shell live on the prototype branch, never on main. (The shared `PrototypePicker` component may stay in the codebase for future prototypes, since it never renders in production.)
