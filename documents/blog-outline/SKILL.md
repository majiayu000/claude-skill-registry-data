---
name: blog-outline
description: Use when a post's thesis has been approved and no section order exists yet. Trigger on "outline this", "what order should this go in", "how should this be structured", or before invoking blog-write on a post whose working doc has an approved Thesis but no Outline.
---

# Order the argument

Turns the settled thesis and the decisions recorded during research into a section order.

## Prerequisite

The working doc `docs/research/<slug>.md` must contain a `## Thesis` section with
`- [x] Thesis` ticked in the stage block. **An unapproved thesis means no outline** — the
order of an argument is derived from its claim, so outlining first means ordering evidence
around a claim that may still move.

## Most of the outline already exists

Ordering constraints accumulate during research and get recorded as decisions. Harvest them
before inventing structure — on this site's SDD post, the `## Decisions` block already
specified that the 2004 precedent opens and then steps aside, that the quality argument
leads over the coverage argument, that the rival framing lands only after the core evidence,
and that a polysemous term gets defined early. That is four of roughly seven sections,
already settled and already justified.

Read `## Decisions` first. Invent only what it does not cover.

## Write to the working doc

Append an `## Outline` section. One row per section:

```markdown
## Outline

**Register.** Essay (~7k chars) or grey paper (~50k, full APA reference list). Decide here —
it changes section count more than any other choice.

| #   | Section | Claim it makes | Evidence      | Debt  |
| --- | ------- | -------------- | ------------- | ----- |
| 1   | ...     | one sentence   | which finding | any ⚠ |
```

Every section needs a **claim**, not a topic. "Background on SDD" is a topic and will
produce filler. "The term was borrowed twice, so it was never specified" is a claim and
produces a paragraph that has to earn its place.

## Checks before handing off

- **Does the order build the thesis sentence?** Read the claims column top to bottom. It
  should compose into the thesis. If it does not, the order is wrong or a section is filler.
- **Does the strongest objection get answered?** It was named at the thesis gate. Find the
  section that handles it. If there is not one, add it.
- **Is any section carrying a ⚠ that must close before publishing?** Mark it. That is the
  pre-publication checklist, derived rather than remembered.
- **Does anything survive that the thesis demoted?** Cut it. Demoted findings reappearing in
  an outline is how a piece turns back into a list of interesting things.

## Do not

- **Do not outline around the evidence you liked most.** Order follows the argument, not
  the research effort. A finding that took an hour to verify and supports nothing gets cut.
- **Do not defer the register decision.** "Decide the length while drafting" produces an
  essay that grows into a grey paper without the structure of one.

## Next step

→ `blog-write` to draft against this outline.
