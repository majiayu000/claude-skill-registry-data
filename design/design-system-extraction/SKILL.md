---
name: design-system-extraction
description: Extracts the complete design system of an existing site (color tokens, type scale, spacing, breakpoints, radius, components, states, motion) by running scripts in the Chrome console, validates every contrast pair against WCAG, and turns it into an implementation guide ready for a coding-agent session. Use whenever the user mentions copying, cloning, replicating, taking inspiration from or matching a site visual language, asks what fonts or colors a page uses, talks about reverse-engineering a UI or a design system, or simply pastes a URL as a design reference. Works the same for prompts in Portuguese, como extrair o design system, copiar o estilo desse site, que fontes e cores esse site usa, quero um site parecido com X, engenharia reversa de UI. Do not wait for the words extract or extracao, they almost never appear.
---

# Design system extraction

Reconstructs the tokens, type scale, layout system and component patterns of a site you
did not build, using its real CSS instead of squinting at a screenshot and guessing.

The deliverable is an implementation document, not a list of colors.

## What this method does not do

It does not copy the site. What gets extracted are measurements and composition patterns.
So images, proprietary icons, copy and product names stay out. If the result could be
mistaken for the original by someone on their team, it went too far.

Tell the user this once, up front, without lecturing. Most already know, and whoever does
not needs to hear it before investing time.

## Before you start

**You need browser access.** Either through a connected Chrome extension, or by asking
the user to run the scripts in DevTools and paste the output back. If neither is
available, say so: with screenshots alone you can estimate typography and spacing by eye,
but the values will be approximate and you must say that clearly.

If the environment has restricted network access, test before promising. A `curl` that
comes back 403 from the proxy means you depend entirely on the browser.

**Pick the pages.** Two or three, and different from each other:

1. The **home**, which usually has the widest variety of components
2. An **inner content page**, which shows the system in ordinary use
3. If one exists, a page with a **form**, which reveals input and error states

Extracting from the home alone is the most common mistake. It is a showcase and often has
one-off components that do not represent the system.

---

## Phase 1: setup

Paste `scripts/setup.js` into the page console, whole, once per page. It registers a
global namespace `x` holding every extractor.

Every function takes a pagination argument. If the output comes back truncated, call it
again with the next number: `x.tokens(0)`, `x.tokens(1)`, `x.tokens(2)`.

If you are running through browser automation, output is usually truncated around a
thousand characters. Do not try to work around it with `console.log`, use the pagination.
If you are walking the user through DevTools, wrap the call in `copy(...)` to send the
result to the clipboard instead of fighting the console.

---

## Phase 2: extraction

Run in this order. The order matters: the first step determines how you read all the rest.

| Call | What it returns |
|---|---|
| `x.stack()` | Framework, libraries, and how many stylesheets are blocked |
| `x.tokens()` | Declared custom properties. What the system *says* it is |
| `x.type()` | Type scale, responsive overrides, loaded families |
| `x.layout()` | Container, grids, gaps, section padding, breakpoints |
| `x.shape()` | Radius, shadow, gradient, border, uppercase |
| `x.colors()` | Computed color audit. What the system *is* |
| `x.comp()` | Class definitions for button, card, chip, input |
| `x.states()` | Hover, focus, active, disabled |
| `x.motion()` | Transitions, animations, and whether reduced-motion is respected |
| `x.map()` | Section map with height and scroll position |
| `x.heads()` | Heading hierarchy, reveals the content architecture |

After `x.stack()`, **read `references/by-stack.md`** and follow only the section matching
the result. Webflow, Tailwind, CSS-in-JS, WordPress and hand-rolled sites need different
strategies, and following the wrong one wastes a lot of time.

If `x.stack()` reports blocked sheets, your token extraction is incomplete. Record that
and tell the user instead of delivering false confidence.

---

## Phase 3: visual capture

`x.map()` returns the coordinates of every section. Scroll to each one and capture:

```js
x.go(4050)     // instant scroll, never smooth
```

Wait two seconds after each scroll before shooting. Intersection Observer entrance
animations need that time, and without it you capture the section at `opacity: 0`.

Capture the top, two or three mid points, and the footer. If you can, also capture a
hover state and the mobile version.

---

## Phase 4: interpretation

**Read `references/interpretation.md` in full before writing the document.** It covers the
three lines of reasoning that separate a useful extraction from a list of values.

A summary of the three, so you know what you are looking for:

**Absence is signal.** An empty result for shadow or gradient is not a script failure, it
is the most valuable finding it delivers. Record every absence explicitly and turn it into
an anti-pattern in the final document.

**The diff between declared and measured.** Compare `x.tokens()` against `x.colors()`.
They almost never match, and the gap is token drift. Always build from the declared side,
which is the intent, never from the measured side, which includes their mistakes.

**Contrast.** Run `scripts/contrast.py`:

```bash
python contrast.py "#fdaccd" "#ffffff"     # one pair
python contrast.py --ramp "#fdaccd"        # 10-step ramp with suggested usage
python contrast.py --audit tokens.json     # ink x bg matrix with a failure report
```

Production systems violate contrast far more often than people assume. When you find a
violation in the original, tell the user and do not reproduce it. The fix is almost never
abandoning the color, it is adding a step. Details in `references/interpretation.md`.

---

## Phase 5: the document

Follow `assets/output-template.md`. Thirteen sections, ordered for consumption by a coding
agent, not for linear human reading.

Two sections carry the result and are exactly the ones that get skipped:

**Anti-patterns**, derived from the absences. Phrased negatively and verifiably: "if X
shows up in the result, it is wrong". This keeps the agent from reintroducing defaults the
source system rejected on purpose, which is the most common failure mode.

**Acceptance checklist**, with objectively answerable items. "Layout looks good" does not
work. "No horizontal scroll at 375, 768, 992 and 1440px" does. Without it the agent
declares success on its own.

---

## Behavior notes

**Ask for the brand colors early.** If the user will use their own palette instead of the
extracted site's, isolate the color block at the top of the document and flag it for
replacement. Swapping later becomes a one-block edit.

**Do not copy the naming.** Step structure yes, names no. The original's names carry
another team's history.

**Say what is extracted and what is proposed.** On a site with no system, much of the
result is your own reconstruction. That distinction matters when someone questions a
decision later.

**One question that saves time.** Up front, clarify whether the user wants the *system* or
the *look*. This method solves the system. The look also requires understanding the
composition decisions, and for that screenshots and human reading are worth more than any
script.

---

## Files

| File | When to read |
|---|---|
| `scripts/setup.js` | Always. Paste into the console before anything else |
| `scripts/contrast.py` | In phase 4, to validate the color tokens |
| `references/by-stack.md` | Right after `x.stack()`. Read only the detected stack's section |
| `references/interpretation.md` | Before writing the document. Read it in full |
| `assets/output-template.md` | When assembling the final document |
