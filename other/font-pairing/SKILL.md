---
name: font-pairing
description: "Two typefaces with clear roles and one shared mood."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, typography]
    category: web
    related_skills: [web-design, typographic-scale]
    web_designer_stages: [font]
---

# Font Pairing Skill

Combining typefaces gives a site personality without sacrificing readability: one face carries the headings, another carries the body, and both share a mood. This skill picks the pairing and records the rationale for it. It does not set the type scale — that is the typographic-scale skill — and it does not write the page copy.

This skill is load-on-demand only. The web-designer coordinator loads it for its stages and it never auto-loads. It never contacts the user directly — the coordinator is the only router.

## When to Use

- When a site needs personality without sacrificing readability.
- When choosing Google Fonts or system stacks for a new site.
- When the font stage needs a pairing decision recorded before the scale is built.
- When the current pairing is too similar or too clashing and needs replacing.
- When a new site section needs typefaces and must reuse the existing pairing rather than pick fresh ones.

It is NOT for setting heading sizes, fixing line length, or judging the finished page — the visual judger does that check.

## Prerequisites

- The run is active and the coordinator loaded this skill for the font stage.
- The direction stage is complete, so the pairing matches the chosen design direction.
- The brief is frozen, so the pairing serves the site's audience and tone rather than taste alone.
- The body copy's reading needs are known, so the body face is chosen for readability at length.

## How to Run

1. Pick the body font first: a highly readable sans, chosen for long text.
2. Propose one pairing with a named rationale — typically a characterful serif or display face for headings with the readable sans for body, or one superfamily in several weights.
3. Check contrast on one axis and shared mood on the other: the two faces must be distinct enough to tell apart, but close enough in mood to sit together.
4. Cap the pairing at 2 families and 3–4 weights; prefer variable fonts and WOFF2.
5. Reject pairings that are too similar (no visible role difference) or too clashing (no shared mood).
6. Test the pairing where it will be read: headings at display size and body at 16px, on the same page, so the roles are judged in context rather than in isolation.
7. Confirm the body face stays readable at length in the pairing — a heading face that looks good large can fail as body text.
8. Record the pairing and its rationale in the font stage record, so the typographic scale can be built on it.
9. Hold the pairing across all pages: a new page takes the same two faces, not a fresh choice.
10. Check the weights in context: 3–4 weights must cover headings, body and emphasis without a fifth creeping in.
11. Confirm the pairing survives the scale: headings distinct from body at every level the scale defines.
12. Prefer the variable-font form where it covers the capped weights in one file.

## Quick Reference

- At most 2 typefaces; rarely 3.
- Cap: 2 families, 3–4 weights.
- Prefer variable fonts and WOFF2.
- Body font first; headings distinct from body.
- Same pairing on every page.
- Contrast on one axis, shared mood on the other.
- Typical pairing: characterful serif or display face for headings, readable sans for body — or one superfamily in several weights.
- Judge the pairing with real headings and body copy together, not from specimens.
- A third face is rare and needs its own role; a third face for one detail is not a role.
- The capped weights cover headings, body and emphasis without a fifth.
- The body face reads well at 16px in long text.

## Procedure

### 1. What it is

Combining at most two (rarely three) typefaces — typically a characterful serif/display face for headings with a highly readable sans for body, or one superfamily in several weights — chosen for contrast on one axis and shared mood on the other.

### 2. How Hermes applies it

Hermes picks body font first, proposes one pairing with a named rationale, caps families/weights (2 families, 3-4 weights), prefers variable fonts/WOFF2, and rejects pairings that are too similar or too clashing.

### 3. What it returns to the stage

- Font stage: `families` — the chosen typefaces with their roles (heading, body) and the named rationale for the pairing; `scale` — the type scale built on those families, which the typographic-scale skill defines.

The pairing is the value the font stage records. The families record carries the two faces, their roles and the rationale; the scale record carries the sizes built on those faces. If either record key is missing, the stage does not complete.

### 4. Good looks like

Two fonts, clear roles, headings distinct from body, no visual noise; the same pairing holds across all pages.

## Pitfalls

- Pairings that are too similar: two near-identical faces give no role difference and add visual noise.
- Pairings that are too clashing: faces with no shared mood fight on the page.
- More than 2 families, or more than 3–4 weights, which bloats the page and muddies the roles.
- Picking the heading font first and forcing body copy into a face that reads badly at length.
- A different pairing per page, so the site loses its identity.
- Fixed weights per heading chosen by eye instead of the capped weight set, which drifts the pairing.
- A pairing judged from specimen sheets alone and never tested with real headings and body copy together.
- A body face chosen for looks that fails at 16px in long text.
- A third face added for a single page element, breaking the 2-family cap for one detail.
- Variable fonts ignored where they would have covered the weight range in one file.
- Weights that cover headings but leave body emphasis with no weight to use.
- A pairing whose mood fits the home page but not the rest of the site's pages.

## Verification

- Exactly 2 families (rarely 3) and no more than 3–4 weights across the site.
- Body font is readable at length; headings are visibly distinct from body.
- The pairing and its rationale are recorded in the font stage record.
- The same pairing appears on every page.
- The pairing was tested with real headings and body copy together, not from specimens alone.
- Headings and body share a mood while differing clearly in role.
- The capped weights cover headings, body and emphasis without a fifth.
- The body face reads well at 16px in long text.

The skill does the work and the visual judger checks it. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: font. Returns: `families`, `scale` (font stage). Judger boundary: the visual judger checks the pairing's roles and consistency across pages.
