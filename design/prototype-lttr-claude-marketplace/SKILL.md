---
name: prototype
description: Build a throwaway HTML or in-app prototype that answers one design question. Use when the user wants to try a state model or UI idea before committing, or says "mock it up", "prototype", "what should this look like".
disable-model-invocation: true
---

# Prototype

A prototype is throwaway code that answers **one question**. Write the question down first, in one paragraph at the top of the prototype where the reader sees it. Then build the smallest thing that answers it.

## Two modes

Pick by asking: does the prototype need the real app around it to be judged?

- **Standalone (default).** Plain HTML/CSS/JS, no framework, no bundler, no server. One file per prototype, saved in the task folder per the `aiwork-protocol` skill: `prototype/index.html`, or `prototype/{name}.html` for several. Everything inline so it opens by double-click and can be sent to anyone. Use for logic and state models, and for UI ideas that can be judged in isolation.
- **Integrated.** Variants rendered inside the project's framework, on a real route with the real header, data and density, because a variant in a vacuum always looks fine. Work on a dedicated `prototype/{name}` branch that is never merged. Follow the project's conventions (Nuxt: `pages/`, `components/`, its CSS system) and name files so they are obviously prototypes: `components/prototype/`, `pages/prototype/{name}.vue`. Start it with the project's normal dev command.

## Rules

- **No polish.** No tests, no error handling beyond what makes it run, no abstractions, no generalising for later.
- **No persistence.** State lives in memory. Persistence is something a prototype checks, not something it depends on.
- **Surface the state.** After every action or variant switch, show the full relevant state and what just changed.
- **Read-only against the real app.** Integrated variants never call real mutations. Stub them.

## Logic prototype

For "does this state machine / data model / API shape hold up". One HTML file a non-developer can drive.

- Keep the logic in one `<script>` block as a pure module: a reducer `(state, action) => state`, an explicit state machine when "which actions are legal now" is part of the question, or a few pure functions over plain data. No DOM inside it. The page calls it, never the reverse.
- Page layout, top to bottom:
  1. Title and the question.
  2. Current state as labelled fields, not raw JSON, re-rendered after every click.
  3. Free-play: one button per action, always available, any order.
  4. Guided scenarios as tabs. Each has a short plain-language description (the situation and what to watch for) and its steps as real buttons that run in order. Starting a scenario resets to a known initial state.
- Scenarios cover what is hard to reason about on paper: the happy path, an awkward edge case, an attempt at something that should be illegal.
- Domain language everywhere. Buttons and labels read like the business, not like the code.
- Clean and restrained: readable typography, generous spacing, one accent colour, no animation.

## UI prototype

For "what should this look like". Several **structurally different** variants behind one switcher.

- Default to three variants, never more than five. They must disagree about layout, information hierarchy and primary affordance, not just colour or copy. If two come out alike, redo one with an explicit constraint such as "no card grid".
- Share small pieces between variants (a header), never the layout. Each variant is free to throw the layout away.
- Use the project's styling system (in jedlik-nejedlik that is Puleo CSS and the tokens shown on `/style`). Standalone HTML inlines the tokens it needs.
- Name variants `A`, `B`, `C` plus a short label, e.g. `B (sidebar layout)`.
- Integrated: variants on the existing route, selected by `?variant=`. Keep the page's data fetching, swap only the rendered subtree. A new throwaway route is the last resort, only when nothing existing can host the variants. An empty route hides problems a populated one exposes.
- Switcher: one shared component, a fixed bar at the bottom centre, visually distinct from the page so it is obviously not part of the design. Previous and next buttons that wrap, the current variant key and label, arrow keys as shortcuts (not while an input, textarea or contenteditable is focused). It updates the URL so a variant is shareable and reload-stable.
- Hand over the URL and the variant keys. The useful feedback is usually "the header from B with the sidebar from C". Add variants or scenarios on request; prototypes evolve.

## When it has answered

Record the verdict and why: in the task folder's spec or notes (per the `aiwork-protocol` skill), or a `Verdict` section at the top of the prototype file. The prototype itself stays where it is, in the `.aiwork/` folder or on its branch, as the primary source. It is never promoted to production code; the real implementation is written separately, using what the prototype taught.
