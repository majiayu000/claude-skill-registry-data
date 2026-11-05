---
name: variant
description: "Use when building multiple variants of a component and iterating to pick the best one."
domain: content
author: jakubkrehel
license: MIT
subdomain: design
tags:
- components
- variants
- iteration
- prototyping
version: 1.0.0
category: content
triggers:
- "variant"
argument-hint: "<component>"
---

# Variants

## Overview

Builds multiple variants of a component and helps iterate and pick one. Takes one described piece of UI and builds three versions that differ on purpose, behind a picker in the real page.
## When to Use

Build three versions of a component that differ on purpose, behind a picker, so you can flip between them and choose.


This skill takes one described piece of UI and builds three versions that differ on purpose. They go behind a picker in the real page, so you can flip between them and choose.

It produces candidates and never ranks them. Reviewing existing UI is `interface-review` and `better-interface`, stress testing one component is `break` and working through a component's states is `state-machine`.
A throwaway picker is this skill's job. When the user wants persistent, browser-live iteration with design context (PRODUCT.md / DESIGN.md, token system, HMR hot-swap), use `impeccable`'s `live` / `generate` instead — its variants live in the project, not a scratch page.

## Different answers, not different tints

Each variant is a different answer to the same brief, on an axis this collection owns:

| Axis | Owner | What varies |
| --- | --- | --- |
| Structure | `better-layout` | Grouping, order, column count, what collapses |
| Density | `better-layout` | Spacing scale, how much fits |
| Emphasis | `better-colors` | Where filled color goes, what recedes |
| Type | `better-typography` | Scale steps, weight contrast, measure |
| Voice | `better-writing` | Labels, tone, how much copy |

Pick **one primary axis** and give each variant a different position on it. The axis names the picker's group heading. Secondary choices follow from it rather than varying on their own. A dense variant may need a smaller type step, and that is coherence, not a second axis.

## The floor every variant clears

Before a variant enters the picker it clears `better-interface`'s escalation triggers, which are:

- Every control has an accessible name and a visible focus indicator.
- Keyboard reaches everything a pointer does.
- Motion and auto-playing content respect `prefers-reduced-motion`.
- Nothing clips, overlaps or becomes unreachable at 320px width or 200% zoom.
- Body and control text pass their required contrast ratio.
- No state or meaning rides on color alone, and no state change on motion alone.
- A destructive action has a confirmation, an undo or a distinct treatment.
- Truncated content has a way to reach the full value.
- Nothing hides past a scroll edge or behind a disclosure with no visible cue.
- Every error names a way to recover.
- No semantic color is used against its meaning, such as the danger hue on a non-destructive action.

That floor is identical across variants. It is not an axis and never trades against one. Where a direction can only work by breaking it, say so and drop the direction.

## Workflow

1. Read the skill principles and references for the current task scope.
2. Apply the rules to the actual interface, code, or design under review.
3. Document findings or changes with evidence (file:line, measured values).
4. Verify against the project's existing conventions and constraints.
5. Report or implement the fix, never silently changing stack or taste.

## 1. Scope one piece

One piece of UI per run. "The dashboard" is not a piece; the metric card is. Where the request spans several, list the candidates and ask which one to explore.

Restate the brief in one sentence: what the thing is, where it renders, what it has to do.

## 2. Learn the ground

Variants have to look like they could ship tomorrow, so read what they stand on:

- The styling system, the component library and any motion library.
- The tokens: color, spacing, radius, type scale, easing.
- The product's density and voice. A dense professional tool bounds how far the boldest variant may go.
- Where the piece renders: against what background, beside which neighbours, at which widths.

With no project to read, use neutral grays, one accent and the system font stack, and say that is what you did.

## 3. Name the axis before writing code

Default to three variants. Go to five only when asked.

Write the set down first, a name and an axis position each. Names say what the direction is, so `Quiet`, `Editorial`, `Dense`, never `Option A`.

This step is done when no two variants share a position and you can state each one's axis in a phrase.

## 4. Build it into the real page

Host the variants on the page that will actually contain the piece, with the real chrome, the real neighbours and realistic data.

Select with a URL search param such as `?__variant=quiet`, so every variant is a link you can send someone. A grouped list beside the piece sets it. Where there is no room beside the piece, it moves above it as a select with the same groups. [picker.md](picker.md) holds the spec.

Render one variant at a time, full size. Thumbnails distort spacing and scale, and spacing is usually the thing you are choosing between.

Variant files may import production components. Only the hosting page imports a variant, and nothing else imports from the harness.

Where no page can host it, build one self-contained HTML file and keep the same picker.

Give every variant real content: product-shaped copy, plausible names and the number of items the page will really carry. Lorem ipsum and three rows make every structure look good.

## 5. Present the tradeoffs and stop

Load the page once in a browser already at hand and flip through every variant. Each one renders, each interaction responds and the console is clean. With no browser at hand, say so and hand the URL over for the user to check.

Then hand the decision over:

| Variant | Axis position | Right when | Costs |
| --- | --- | --- | --- |
| Quiet | Lowest visual weight | The page is used daily | Least memorable |
| Editorial | Largest type, most space | The moment deserves weight | Eats vertical space |

Say where the picker is running, which key flips it and which width you judged at. The answer can change between 375px and 1440px.

Never mark a favourite in the table. Asked directly, answer from how often the piece is seen and from the product's personality, not from which one you enjoyed building.

## 6. Promote one, delete the rest

On a choice, build that variant properly where it belongs, following the project's own conventions. Then delete the other variants, the picker and the hosting page's import of the variants. Search for the variant names and the `__variant` param, and check the diff leaves nothing of the harness behind.

Asked for another round instead, keep the harness and run **Name the axis before writing code** again, taking new positions around the direction you leaned toward.

## Before you finish

| Mistake | Fix |
| --- | --- |
| Variants differ only in accent color or copy | Move one to a different position on the primary axis, or cut it |
| Every axis varies at once | Vary one; let the rest follow from it |
| Judged on a blank route | Host them on the page that will contain the piece |
| Lorem ipsum, three rows, "Jane Doe" | Real copy and the item count the page will really carry |
| The boldest variant skips keyboard or focus | Clear the floor or drop the direction |
| A favourite marked in the table | State each variant's cost and let the user choose |
| Picker restyled with the project's tokens | Keep it visibly outside the design system |
| One long row of tabs, one per variant | A grouped list beside the piece that scrolls on its own; a select above it where the list does not fit |
| Harness left behind after promotion | Delete it and search for the names and the param |

## When NOT to Use

- Pure backend logic with no UI/design considerations
- Tasks outside the scope of interface design and evaluation
- When a more specific skill already covers the exact need

## Verification

- [ ] Applied the skill's principles to the actual interface/code
- [ ] Verified changes against project conventions and constraints
- [ ] Checked for accessibility and usability issues where relevant
- [ ] Documented findings or changes clearly

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Good enough for now" | Polish matters - small details compound into quality |
| "I'll fix it later" | Fix it now while context is fresh |
| "This is subjective" | Follow the principles and measurable criteria in this skill |
