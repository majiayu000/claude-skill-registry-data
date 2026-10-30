---
name: scouting-flight
description: Momo's scouting flight for throwaway prototypes and spikes. Use for prototype, "spike", "mock it up", "try this layout", "sketch it to decide", or "try it and see". Use to settle a design fork by observing it instead of debating it, to compare layouts, interactions, or densities side by side, to test whether an approach fits a timing or latency budget, or to answer a "which approach" question with an experiment instead of asking the human. Also for small bounded tasks with one clear check. The prototype is thrown away; the decision is the output.
---

# Momo's scouting flight

Momo flies ahead, grabs what he finds, and comes back fast. He does not build a nest. A prototype is the same. Take a quick flight to see the terrain, then throw the code away and bring back the answer.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

**You own the design decision, not the code.** The prototype is a throwaway instrument. The real build follows the new-behavior chain in `avatar-mode`.

This is the one flight where the Air principle of the smallest change and the usual verification bar invert. Speed beats polish. Code quality does not matter. There is no plan. The rigor is in picking the right design cheaply. Propose variations nobody asked for. Throw an approach away and try another.

## When to fly

Before you ask the human a "which approach", "how should I", or "what should this do" question, classify it. If the answer is a fact you could observe by running something (behavior, timing, layout, output, performance, even whether an eval separates two variants), it is not the human's to answer. Fly and let the result decide.

- A read-only investigation whose deliverable is a cited answer stays in `seismic-sense`. Answer from the evidence instead of building a sketch.
- Save the question for a genuine product or preference call that no experiment can settle.

## Steps

1. **Name the decision.** One sentence on what the prototype settles. For a visual fork that is which layout, which interaction, or which density. For an empirical fork it is which behavior, which timing, or which approach. Whether an API shape reads well at the call site counts too. No decision means no prototype. Route to `avatar-mode` instead.
2. **Gather references when the design space is open.** Search for prior art. Summarize a moodboard of themes, palettes, and layouts, and let the user pick directions before you build. Skip this when the direction is already set.
3. **Build throwaway in scratch.** Work in an isolated scratch directory, separate from production source. For a visual decision, use vanilla HTML, CSS, and JS or the lightest stack that renders the idea, with CDN dependencies and a dev server with hot reload. For a behavioral or timing decision, write the smallest script that exercises the question. No production framework, no tests, no abstractions.
4. **Build the alternatives side by side.** When comparing options, put them behind one switcher (buttons, a keypress, a flag, or a command argument) and label each variant. This is [Exhaust the Design Space](../four-elements/references/exhaust-the-design-space.md) made cheap.
5. **Observe on the matching surface.** For a visual decision, screenshot each variant and drive the interaction through the project's verify skill, or Claude Code's `run` skill when the repo has none (`vital-signs` creates a verify skill). For a behavioral or timing decision, observe the thing you are deciding. Log the timing with the same harness for every variant, print the output, or watch the render. The observation is the test here, not an assertion.
6. **Bring it back.** Present the alternatives, the tradeoffs, and a recommendation. The output is the decision plus the throwaway artifact, not shippable code.
7. **Hand off the real build.** The chosen direction goes to the new-behavior chain in `avatar-mode`, with `war-room` for the shape and `master-plan` when it has several steps. Never promote prototype code to production as is.

## Quick tasks

Momo also takes small, bounded tasks a dispatcher hands him. That means one file, one clear change, and one check. Do it, run the check, and report the result in a few lines. If the task turns out bigger or ambiguous, stop and report back rather than expanding scope.

## Reply

Name the variants you explored and the evidence for each. That is a screenshot for a visual decision, and the observed output or timing for a behavioral one. Then give the tradeoffs, your recommendation, and the scratch path. Say plainly that the prototype is throwaway.
