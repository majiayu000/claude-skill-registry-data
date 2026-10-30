---
name: antislop
description: >-
  Anti-slop filter for AI work: rejects technique without purpose and demands
  liveliness, for UI, copy and code comments. Use whenever generating or editing
  an interface, a landing page, product copy, headlines or prose, and when
  auditing existing output for the usual AI tells.
---

# antislop — the filter, not the direction

> Home branch in Memora: `root/skill/antislop`.
>
> Direction comes from `DESIGN.md` or the owner's brand brief; this skill only
> rejects slop and raises the liveliness bar. Without direction the result drifts
> to default taste — say so instead of inventing a style.

## Choosing a part

**Task references** — the practical files, opened by the task at hand:

| Task | Reference |
|---|---|
| Building or editing an interface: colour, layout, components, decoration, motion | `references/ui.md` |
| Writing or editing copy: headlines, CTAs, value propositions, tone, product prose | `references/copywriting.md` |
| Making a UI work for different eyes, hands and setups: contrast, keyboard, focus, states | `references/people-and-accessibility.md` |
| Layouts that must hold up on a phone: breakpoints, scale, grids, overflow, tap targets | `references/layout-mobile.md` |
| Code comments: remove generic AI-slop comments, keep the valuable ones, never touch the code | `references/code.md` |
| Editing prose in the writer's own voice, or detecting AI-slop patterns in text | `references/prose-editing.md` |

**Rule parts** — the law, opened when the task needs it:

| Part | What it covers |
|---|---|
| `parts/rules/` | R-01 to R-38 in three groups: hard gate (absolute), purpose-gate (technique allowed, reason required), quality locks (consistency) |
| `parts/patterns/` | The slop patterns to audit for — colour, layout, components, copy, decoration, functionality, identity, accessibility |
| `parts/liveliness/` | Three dials, the levers that turn them into visual decisions, how a design read sets them; plus the functional patterns list |
| `parts/delivery-gate/` | The mandatory gate before delivery: hard gate, purpose-gate justifications, consistency locks, evidence required |
| `parts/ai-copywriter/` | Writing site copy, posts, letters and product prose — the craft side of the same standard |

## Rules

- **The filter rejects technique without purpose, not technique itself.** Before
  any visual choice answer "what does this serve?"; if the only answer is "it looks
  AI" or "it looks safe", the choice goes or is reworked.
- **Done means three things**: every technique passes the purpose test, the result
  has its own identity, and it actually works (the craftsmanship standard below).
- **Ask once, at the start**: does antislop apply during the work or after it is
  done? Ask in the owner's language and wait — do not start UI work before the answer.
- **Forks worth `ask_questions`**: missing brand direction, a request that
  contradicts the owner's own brand, an accessibility requirement that changes the
  layout, or a claim that cannot be evidenced (C-5 forbids showing it at all).
- **Evidence over claims**: contrast, keyboard and state checks are run with the
  checkers (`scripts/contrast-check.py`, plus the parts named above); a claim
  without a run is not a pass.
- **Decisions that outlive the task** become Memora nodes under
  `root/skill/antislop`; the design direction itself belongs in the project's
  `DESIGN.md`.

## The craftsmanship standard

"Not slop" is the floor. A design passes when it meets five preference-agnostic
criteria — use them as questions, not recipes:

- **C-1 Intentionality** — every visual and copy decision has a reason you can
  articulate; "it's the AI default" is a red flag.
- **C-2 Functional completeness** — every interactive element works, or it does not
  exist. A button that cannot do anything is a defect, not decoration.
- **C-3 Content-driven composition** — every section exists because the product's
  content needs it, not because every landing page has one.
- **C-4 Resilience** — holds up in every state (empty, loading, error), every theme
  shipped, every breakpoint, and keyboard-only use.
- **C-5 Evidence over claims** — anything presented as fact (testimonials,
  statistics, security claims) is real and verifiable, or it is not shown.

## Related

`design` (the craft and the parts that build the interface), `media`
(images and assets), `decks` and `documents` (when the slop-prone artifact is a
deck or a document rather than a screen).
