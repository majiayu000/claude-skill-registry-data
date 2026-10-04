---
name: "prototype"
description: "Build a throwaway prototype to settle a design question or an empirical fork by observing it, instead of asking a question a quick sketch could answer. Use for prototype, mock it up, sketch this, try this layout, or when checking whether a state model or logic feels right."
disable-model-invocation: true
---

# Prototype

A prototype is **throwaway code that answers a question**. You own the
decision, not the code. The real build follows afterwards.

This is the one place where the **laziness-protocol** principle
(`principles/laziness-protocol.md`) inverts. Speed over polish, code quality
does not matter, no planning. The rigor is in picking the right design cheaply.
Be bold: propose variations nobody asked for, throw an approach away and try
another.

## When to reach for it

Two triggers, and the second is the one that gets missed.

- **A design question.** Which layout, which interaction, which density, does this state model hold up.
- **An empirical fork you were about to ask the human about.** If the answer is a fact you could observe by running something (behavior, timing, layout, output, performance), it is not the human's to answer. Sketch it and let the result decide. The ask is the slow path; a throwaway probe usually answers faster and hands them a result to react to instead of a decision to make.

Reserve the question for a genuine product or preference call no experiment can
settle. **No decision means no prototype.** Route to the real build instead.

## Pick a branch

The question decides the shape, and getting this wrong wastes the whole
prototype.

- **"Does this logic or state model feel right?"** → [LOGIC.md](LOGIC.md). One shareable HTML file, free-play buttons plus tabbed guided walkthroughs, pushing the state machine through cases that are hard to reason about on paper, drivable by a non-developer.
- **"What should this look like?"** → [UI.md](UI.md). Several radically different variations on one route, switchable via a URL search param and a floating bottom bar.
- **"Which behavior, timing, or approach?"** → no separate file needed. The smallest script that exercises the question, logging the timing or printing the output. The observation is the test, not an assertion.

If genuinely ambiguous and the user is not reachable, default by what surrounds
it (a backend module → logic, a page or component → UI) and state the
assumption at the top.

## Rules for all branches

1. **Throwaway from day one, and marked as such.** Put it near what it prototypes for so the context is obvious, but name it so a casual reader sees it is not production. For throwaway UI routes, follow the project's existing routing convention; do not invent a new top-level structure. For a purely behavioral probe, an isolated scratch dir outside production source is fine.
2. **Trivial to run.** One command from the project's task runner, or a single HTML file the user double-clicks. No thinking required to start it.
3. **No persistence by default.** State lives in memory. Persistence is the thing being checked, not something to depend on. If the question genuinely involves a database, use a scratch one named "PROTOTYPE, wipe me".
4. **Skip the polish.** No tests, no error handling beyond what makes it runnable, no abstractions.
5. **Surface the state.** After every action, or on every variant switch, render the full relevant state so the change is visible.
6. **Compare behind one switcher.** When there are alternatives, put them behind buttons or a keypress, each labelled so the user can name it. This is the **exhaust-the-design-space** principle (`principles/exhaust-the-design-space.md`) made cheap.
7. **Gather references first when the design space is open.** Prior art, a short moodboard of themes, palettes, and layouts, and let the user pick a direction before you build. Skip when the direction is already set.

## Verify on the matching surface

For a visual decision, screenshot each variant and drive the interaction. The
`claude-in-chrome` skill covers browser surfaces; the built-in `/run` skill
covers CLIs and servers. The eye is the test.

For a behavioral or timing decision, observe the thing you are deciding: log the
timing, print the output, watch the render.

## Capture it when done

Fold the validated decision into the real code. Then capture the prototype
itself as a primary source: commit it to a throwaway branch, off main, and
leave a pointer to that branch on the implementation issue. Record the verdict
and the question it settled. Main keeps only the validated decision.

**Reply:** the variants explored, the evidence (screenshots for a visual call,
observed output or timing for a behavioral one), the tradeoffs, your
recommendation, and the scratch path. Say plainly that the prototype is
throwaway.
