---
name: logic-prototype
description: Build a single-file HTML demo that answers whether a state model, business logic, or data shape feels right — a pure liftable module driven by free-play buttons and tabbed guided walkthroughs a non-developer can click through. Use when the user wants to sanity-check a state machine or reducer, probe an edge case ("what happens if X then Y"), feel out a data model or API shape before building it, or hand a domain expert something to poke at. For what a UI could look like use prototype; for editable Paper artboards use paper-prototype.
---

# Logic prototype

A logic prototype is **throwaway code that answers one question about a state
model** — the kind of model that looks reasonable on paper but only feels wrong
once someone pushes it through real cases. The artefact is a single,
self-contained HTML file anyone can double-click: a designer, a PM, a domain
expert. It speaks their language, not the code's.

If the question is "what could this look like", wrong skill — use `prototype`.

## Process

### 1. State the question

Write down what state model and what question this prototype answers — one
paragraph, visible at the top of the demo, not a code comment. A logic
prototype that answers the wrong question is pure waste; making the question
explicit lets it be checked later, whether the user is watching now or
returning to it AFK.

### 2. Isolate the logic in a pure, liftable module

The logic under test lives in one `<script>` block as a small pure module that
could be lifted out and dropped into the real codebase later. The page around
it is throwaway; this module is not. Pick the shape that fits the question:

- **Pure reducer** — `(state, action) => state`, for discrete events over a single value.
- **State machine** — explicit states and transitions, when "which actions are even legal right now" is part of the question.
- **Set of pure functions** over a plain data type, when there is no implicit current state.
- **Class with a clear method surface**, when the logic genuinely owns ongoing internal state.

Keep it pure: no DOM, no `document`, no button handlers reaching inside. The
page calls into it; nothing flows the other way. That boundary is what makes
the validated module lift straight into the real code once the question is
answered.

### 3. Build the shareable HTML file

One file, plain HTML/CSS/JS — no framework, no bundler, no server, everything
inline, so it opens by double-click and survives being sent around. Write it
for a non-developer: every label in **domain language**, buttons and state
reading like the business, not the reducer. Top to bottom:

1. **Title and the question** from step 1.
2. **Current state** — the full relevant state as a readable panel (labelled
   fields, not raw JSON), re-rendered after every click, with a callout of
   what just changed.
3. **Free-play buttons** — one real button per action, always available, so
   anyone can poke at the model in any order.
4. **Guided walkthroughs** — scenarios, one per tab: a short plain-language
   description of the situation and what to watch for, then the ordered
   buttons to press. Each step is a live button; starting a walkthrough
   resets to a known initial state so the scenario replays deterministically.

Choose scenarios that demonstrate the awkward cases: the happy path, a tricky
edge, an attempt at something that should be illegal.

Keep it restrained: clean typography, generous spacing, one accent colour, no
animation. Real `<button>` elements, keyboard operable — nothing competes with
the state and the buttons.

### 4. Save, open, hand over

Save to a durable notes or artefacts location outside the repo — wherever the
project keeps design records (create it lazily) — print the path, and open it.
The interesting moments are "wait, that shouldn't be possible" and "I assumed X
would differ" — those are bugs in the *idea*, which is the point. Add actions
or scenarios on request; prototypes evolve.

### 5. Capture the answer

When the question is answered, add a one-line verdict (what was settled and
why) to a notes file beside the HTML, and leave a pointer wherever the
implementation is tracked. The validated module lifts into the real code
through the `build` skill; the HTML shell stays behind in the artefacts
location as the record of how the question was answered.

## Anti-patterns

- **No tests.** A prototype that needs tests is no longer a prototype.
- **No real database.** In-memory state, unless persistence *is* the question.
- **No generalising.** No "what if we later want X" — one question per prototype.
- **No blurring module and page.** A module that touches the DOM is no longer liftable.
- **No framework, bundler, or server.** One double-clickable file; a dev server defeats "shareable".
- **Never ship the shell.** Only the module lifts into the codebase; the page stays in the artefacts location.

## Credits

Derived from Matt Pocock's MIT-licensed `prototype` skill (`LOGIC.md` branch,
[github.com/mattpocock/skills](https://github.com/mattpocock/skills)); upstream
licence in [LICENSE-upstream](./LICENSE-upstream).
