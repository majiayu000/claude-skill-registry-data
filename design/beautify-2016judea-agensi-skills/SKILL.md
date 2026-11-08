---
name: beautify
description: Use when asked to make a UI, page, or component more visually compelling — "sexier," more polished, more UX-savvy, or when asked for creative visual redesign ideas. Prototype live, interactive Artifact concepts using the real design system and real content, before touching production code — never guess a single aesthetic and ship it straight to a file. Covers presenting distinct visual directions, refining a chosen direction's feel as live variants, and porting the validated design into production with full QA.
---

# Beautify

## The foremost idea

**Prototype live, in an Artifact, before you touch production code.** Not a
text description of an idea — a real, clickable, on-brand build of it. A
sentence like "cards that flip to reveal the data" is a guess about whether
it'll actually feel good; a working flip card the person can click is not a
guess. This applies twice in the same task: once when picking a *concept*,
and again when refining that concept's *feel* (motion, timing, "sleeker,"
"more responsive"). Both are subjective calls — don't resolve either one by
guessing and shipping. Build it, show it, let them react to something real.

Everything else in this skill is in service of that one idea.

## When to use

- "Make this more sexy / polished / premium / UX-savvy."
- "Give me some visual ideas for X."
- Any request to redesign a component's look-and-feel where the end state
  is genuinely open — not a spec, a vibe.
- Refining a chosen direction's micro-interactions ("make the reveal feel
  more alive," "sleeker," "lead to an ah-hah moment") — this is still
  beautify work, not implementation work, even after a concept is picked.

Not this skill: a request with an already-fixed visual spec (just build
it), or a pure copy change, or a bug fix with no aesthetic question in it.

## The method

1. **Ground in the real subject first.** Read the actual component/page
   before proposing anything — its current markup, its design tokens, its
   real copy. Ideas that aren't anchored to the real palette and real
   content read as generic ("AI slop") no matter how clever the layout is.
   Honor whatever design system already exists in the project (see the
   `artifact-design` skill) — find its real tokens (colors, type scale,
   spacing) before inventing new ones.

2. **Build the concepts as one live Artifact, not a written list.**
   Genuinely distinct directions (not five variations on one idea), each
   fully interactive, each using real product copy — not lorem ipsum, not
   placeholder numbers. Load `artifact-design` before writing it. Give an
   opinionated recommendation at the end, but let the person choose — a
   recommendation is not a decision made for them.

3. **When the chosen concept needs subjective refinement, don't guess —
   build named variants and let them compare live.** Words like "sleeker,"
   "more responsive," "ah-hah moment" describe a feeling, not a spec, and
   guessing wrong here costs a full round trip. Build 2-3 real, distinct
   takes (e.g. a fast one, a narrated one, a minimal one) in the *same*
   artifact and republish to the *same URL* — don't mint a new link for
   every iteration; keep one thread of truth. Subjective style/color/motion
   calls are worth asking about explicitly rather than guessing — a wrong
   guess costs a full round trip, a question costs a beat.

4. **Fix real feedback live, in the artifact, before porting anywhere.**
   When told something looks wrong ("the yellow is obtrusive"), diagnose
   the actual cause (a browser default, a missed CSS reset — not just "make
   it a different color") and fix it in the prototype first. Cheaper to
   iterate there than in production markup.

5. **Only port to production once the concept is validated live.** When you
   move the winning design into the real file:
   - Preserve every existing functional contract exactly — form field
     `name`/`value` strings, API payload shape, event names, accessibility
     semantics (real `<input>` elements for real form controls, not
     styled `<div>`s standing in for them).
   - Check call sites that define those contracts (wherever the project
     declares its option lists, prop types, or payload schemas) before
     assuming a label string is safe to keep or rename.
   - Re-read the file before editing if anything suggests it changed
     underneath you (concurrent edits, hooks) — don't blind-fire an `Edit`
     against stale context.

6. **QA the shipped version like any other change — a visual change is not
   exempt.** Check for mobile/responsive overflow with real screenshots at
   phone width (not just a desktop glance), and verify runtime behavior
   actually still works — drive the real handler with a mocked
   side-effecting network call, don't assume from the diff. Visual
   rewrites break real things (an HTML entity rendering literally because
   `textContent` was used where `innerHTML` was needed; a mobile layout
   that breaks under a horizontal scroll container) that only a real
   render + real click catches.

   **A sweep that clicks a captured node list reports clean without ever
   running.** If any handler re-renders its container, the elements you
   collected before the first click are detached: every later `.click()`
   fires on a corpse, and reading `dataset.*` off it returns the stale
   attribute — so the sweep cheerfully reports four distinct settings
   having exercised one. Re-query by selector *inside* the loop, and
   **assert the result actually changed** — count distinct outcomes across
   the run and treat that count as the evidence, not the absence of
   errors. Green that cannot distinguish "clean" from "never ran" is the
   most expensive kind. (Seen in practice: the same detached-node bug
   existed in both the page and the sweep meant to catch it, and the sweep
   passed.)

   While you are in there: drive the **failure** path too (stub `fetch` to
   a 503 before the component's first load), and read a generated download
   back rather than trusting the click — stub `URL.createObjectURL` and
   `HTMLAnchorElement.prototype.click`, then parse the Blob.

7. **Confirm on the live URL after deploy, not just "it pushed."** CDN/
   build lag is real; check the actual production page renders the new
   markup before calling it done — and poll rather than checking once,
   since a fresh asset can 404 for a minute after the push.

## Common mistakes

- Jumping straight to editing the real file with one guessed aesthetic —
  even a good guess costs a full round trip if it's wrong, and it usually
  costs more than building two extra live options would have.
- Describing concepts in prose ("imagine cards that flip...") instead of
  building them — motion and feel are not describable in a way that lets
  someone actually judge them.
- Offering near-identical options dressed as "distinct concepts" — each
  one should represent a genuinely different structural idea, not a color
  swap.
- Treating a visual/motion port to production as exempt from QA — it
  isn't; entity-encoding bugs, layout breaks, and broken form contracts
  hide inside "just a redesign" just as easily as in any other change.
- Minting a new Artifact URL on every round of feedback instead of
  republishing the same file path — fragments the thread and makes it
  harder to track what's current.

## Done when

The chosen concept was validated live (clicked through, not just read)
before any production file was touched; the shipped version passes a
real mobile-width check with zero overflow; the real functional path
(form submit, event fire, whatever the component drives) was verified with
the actual handler and a mocked network call, not assumed from the diff;
and the live production URL was checked post-deploy.

## See also

- `artifact-design` — load before building any prototype Artifact; covers
  design-system-honoring, typography, and avoiding generic "AI-slop" looks.
