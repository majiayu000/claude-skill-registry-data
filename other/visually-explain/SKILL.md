---
name: visually-explain
description: >
  Produce a single self-contained interactive HTML document that visually
  explains how a *specific* system, mechanism, or design in the codebase works --
  built for visual learners who find static markdown insufficient. Walks a
  concrete worked example through its states with toggles, steppers, diffs, and
  side-by-side comparisons. Invoked explicitly as /visually-explain; it is for
  explaining a particular thing you can point at in code or a spec, not for
  general-concept tutorials.
---

# Visually Explain

Turn a specific mechanism from the codebase into a single self-contained
interactive HTML document that you can open in a browser and play with. For a
visual learner, a toggle that flips between "what happens now" and "what should
happen", or a stepper that walks a real example through each state, lands an idea
that no paragraph can.

The artifact is the explanation. Prose annotates it; it doesn't carry it. If the
result reads like a Markdown doc that happens to be wrapped in `<div>`s, it
failed.

## When this runs

Invoked explicitly with `/visually-explain` — it is never auto-triggered by a
bare conceptual question. If someone just asks "how does X work?", answer in
prose; you may _offer_ to build an explainer, but only build on an explicit ask.
Producing the artifact writes a file and opens a browser tab, so opting in should
be deliberate.

**Scope: codebase/spec-grounded only.** This skill explains a _particular_ system
you can point at — the actual code, a design doc, a spec. It is **not** for
general-concept tutorials ("explain how operational transform works in the
abstract"). Without a concrete source to verify against, there's nothing to keep
the visual honest, and honesty is the whole point (below). If the request is a
general-concept explainer, say so and stop.

## Correctness is the whole job (non-negotiable)

This is the one rule that overrides everything else in this skill. An interactive
visual _looks_ authoritative -- polished layout, confident color-coding, smooth
transitions all signal "this is right". That makes a wrong explainer far more
dangerous than wrong prose: the reader trusts it and builds a broken mental model
on top. **A bad or buggy explanation is worse than none at all.**

So:

- **Never guess, never hallucinate, never smooth over a gap.** If you don't fully
  understand a mechanic, you cannot visualize it. Don't invent how something works
  to make a cleaner animation or a tidier diagram.
- **Don't visualize anything you can't verify.** Every state transition, index
  shift, color, and label must be something you've confirmed from the source --
  the code, the spec, the user -- not inferred because it seems plausible.
- **When you're unsure, stop and ask** (or leave it visibly out). It is correct
  and expected to tell the user "I don't understand X well enough to draw it
  truthfully -- can you clarify, or should I leave it out?" That is a success, not
  a failure.
- **Mark genuine uncertainty in the artifact itself.** If something is your
  best-effort interpretation rather than confirmed fact, label it as such in the
  document (e.g. a dimmed "assumption" tag) so the reader never mistakes a guess
  for ground truth. Better still: resolve it first.
- **Keep it simple, because simplicity is what makes it trustable.** Simplicity
  here is not an aesthetic preference — it's a correctness requirement. Every bit
  of cleverness (more states, more moving parts, more computed logic) is extra
  surface where the explanation can quietly go wrong. A simple visual you can
  fully stand behind beats an elaborate one you can't. When in doubt, show less,
  more correctly.

There is no partial credit for a beautiful diagram that's subtly false.

## First, actually understand the thing

You cannot visualize what you don't understand. Garbage in, garbage out.

Before writing any HTML: read the code, the design, the thread -- whatever the
concept lives in. Trace the concrete worked example through by hand and confirm
each state is what the real system would actually produce.

**The source is the authority, not the user.** You're usually invoked precisely
because the user _doesn't_ fully understand the thing yet — so don't quiz them to
reconstruct it. Read the code, build from it, and keep questions minimal. Default
to building. Only stop to ask when your hand-trace hits something genuinely
ambiguous that changes the visual _and_ you can't resolve it from the source _and_
getting it wrong would make the visual false. That one high-stakes point is worth
a quick confirm (or an "assumption" tag); everything else, just build it.

When you're confident you understand it, find the **one concrete worked example**
that exposes the heart of the idea -- the smallest input that still shows the
interesting behavior. The screenshot that inspired this skill threads `"Hello"`
through two concurrent edits to show exactly where client-side rebasing diverges.
That single example does more than three paragraphs of theory. Pick yours before
you design anything.

## Choose an interaction that fits the concept

The interaction is not decoration -- it's how the reader builds the mental model.
Match it to what the concept actually is:

- **Compare toggle / tabs** -- flip the _same_ state between two readings:
  "current behavior" vs "intended result", naive vs correct, before vs after a
  fix. Best when the whole point is a divergence.
- **Stepper / timeline** -- walk one concrete example through sequential states
  (Initial -> Client A -> Server -> ...), forward and back. Best for protocols,
  algorithms, request lifecycles, anything with ordered causality.
- **Side-by-side** -- two approaches running the same scenario in parallel
  (client-side rebasing vs server-side rebasing). Best for "why this design over
  that one".
- **Annotated state** -- render the domain object _concretely_ (text as boxed
  characters, a queue as cells, a tree as nodes) and color-code roles:
  accepted/green, deleted/red, stale/amber, new/blue. The reader should _see_ the
  state, not read a description of it.
- **Diff / highlight** -- show what changed between two states, with the delta
  emphasized and the unchanged parts dimmed.
- **Progressive reveal** -- expandable detail for layered ideas, so the overview
  stays uncluttered and depth is opt-in.
- **Live playground** -- let the reader change an input and watch the result
  recompute. The most powerful option when the concept is a transformation, and
  worth the extra effort when it is.

Combine them when it serves the idea (a stepper _with_ a compare toggle at each
step is exactly the screenshot's pattern). Don't combine them to show off.

## Bake in pre-computed states; don't trust live JS

There are two independent ways the visual can lie: you can misunderstand the
system (covered above), or your inline JS can be buggy — the stepper shifts an
index wrong, a computed state comes out subtly off — so the explanation is false
even though your mental model was right.

So by default, **bake in the states you traced by hand.** The states are data you
already verified; the JS just reveals them step by step. A dumb presenter over
hand-checked data has almost nothing to get wrong. This is the same simplicity =
trust principle: the less the artifact computes, the less it can fool you with.

A **live playground** that recomputes from arbitrary user input is the opposite —
a whole new program that must itself be correct, running on inputs you never
traced. Reserve it for when the concept genuinely _is_ a transformation worth
playing with, and when you do reach for it, **verify the computed output against
your hand-traced example before shipping** — e.g. run the logic in Node and
confirm it reproduces the known-correct sequence. Never trust live computation
blind.

## Aesthetics

This skill owns _what to show and how it behaves_, not how it looks. **If the
`frontend-design` skill is available, invoke it** (via the Skill tool) for
typography, color, motion, and composition before styling — don't just nod at it.

It may not be installed, though (this skill ships standalone), so here's a
self-sufficient fallback guardrail when it isn't:

- Distinctive but legible. No generic AI slop — no Inter/Arial, no
  purple-gradient-on-white. Pick type and color with intent.
- Restraint over flash. The simplicity that makes the artifact trustable also
  makes it look considered. Don't drown the explanation in effects.

Two domain-specific rules apply on top either way:

- Color must **encode meaning**, not just look nice. If green means "accepted" in
  one place, it means "accepted" everywhere. Keep a tiny, legible legend.
- Motion should clarify causality (a character sliding as an index shifts), never
  just animate for delight. A transition that shows _why_ an index moved is worth
  it; a fade-in for its own sake is noise.

## Self-contained, always

One `.html` file. All CSS and JS inline. No build step, no framework, no network
calls -- the user double-clicks it, or opens it on a plane, and it just works.
Vanilla JS and CSS are plenty for these; reach for nothing heavier.

The single tolerable exception is one web font from a CDN -- and only with a real
system fallback in the stack so it degrades gracefully offline. Everything else
(icons, logic, state, styles) ships in the file.

## You can't see the render — split the work honestly

You write the HTML, but it opens in the _user's_ browser, not yours. You can
verify the **data** (the states are correct) by reading your own code; you cannot
verify the **rendering** — that step 3 shows the right state, that the colors
landed, that nothing overflows. So own what you can and hand off what you can't:
you're responsible for truth-of-data, the user is your eyes on the visual. Never
claim it "looks good" — you haven't seen it. Ask them to open it and flag
anything off, then iterate. (If headless tooling like Playwright already exists in
the project, a quick self-screenshot is a fine bonus check — but don't add it as a
dependency.)

## Output

Write the file to the current working directory with a sensible name derived from
the topic (e.g. `livetext-rebasing.html`), then open it:

```sh
open livetext-rebasing.html
```

It's a throwaway artifact — an understanding aid, not a committed doc. Leave it in
cwd for the user to keep or `rm`; never commit it. On revisions, overwrite the
same file and re-open.

**What goes in the chat.** The artifact carries the explanation — don't re-explain
the concept in prose (that's a redundant second copy to keep in sync). The chat
carries only what the file can't speak for itself:

- The filename, and that it's opened.
- A short **guided walkthrough** — how to _drive_ the visual to the interesting
  moment: "press **Intended result**, then step to the second Server row — that's
  where B's index goes stale." Point them straight at the aha, and note any
  subtlety about operating it.
- Any **assumptions or unverified points** you flagged, and anything specific you
  want them to eyeball ("does step 3 match what you'd expect?").

## Smell test before you ship

- **Is every single thing in it true and verified?** Can you point to where each
  state, transition, and label comes from in the source? Any "I think it works
  like this" must be resolved or visibly marked as an assumption -- never shipped
  as fact. This gate comes first; a wrong artifact fails regardless of how good it
  looks.
- Are the displayed states baked-in hand-verified data, or computed live? If
  computed, have you run the logic and confirmed it reproduces the traced example?
- Could a reader get the core idea from the visual alone, with the prose hidden?
  If not, the visual isn't doing its job yet.
- Is there a real worked example, or just abstract boxes labeled "State A"?
- Does every color and animation mean something?
- Is it as simple as it can be? Could any state, control, or effect be removed
  without losing the point — and would removing it make the rest more trustable?
- Does it open offline by double-clicking, with nothing fetched?
- Is it one focused concept, not a sprawling tour? One artifact, one idea.
