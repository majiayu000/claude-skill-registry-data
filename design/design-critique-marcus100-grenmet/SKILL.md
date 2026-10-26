---
name: design-critique
description: "Critiques a UI surface against the Refactoring UI ladder and returns a ranked, token-legal fix list. Needs no design reference."
disable-model-invocation: true
---

# Design Critique

`/ui-check` compares an implementation against a reference. This does the opposite job: it judges a surface **on its own terms** when there is no canvas to compare against — "this looks off and I don't know why."

Load [`refactoring-ui`](../refactoring-ui/SKILL.md) and the lane spec (`docs/design/<lane>.md`) before starting. Every finding must trace to a named principle in it; a critique you cannot attribute is taste, not review.

## Step 1 — Get the subject

You need one of:

- a screenshot (pasted or attached), **or**
- a component/page file path, **or**
- a published Claude Design canvas URL

and the intended viewport (375px mobile, 1280px desktop, or both).

Given only a file path, render it before critiquing:
`pnpm ui:screenshots --app <app> --path <route>` writes phone and desktop PNGs in
both themes (the dev server must be running on the host). Critique the PNGs, not
the source.

Ask for the app if the path does not make it obvious — the lane changes the verdict. `gms` is the public reference app and should read spacious; `gaa-admin` is deliberately dense and must not be critiqued into looking like a marketing page; `wxproducts` and `hr` are fixed-dimension document/print surfaces where A4 constraints outrank white-space advice.

Do not proceed on a described-from-memory surface. If there is no screenshot and no file, ask the user to run the app on the host (see `docs/ports.md`) and screenshot it.

**Done when:** you have the subject, the viewport, and the app lane.

## Step 2 — Read the surface before judging it

Write down, in one or two lines each:

- What is this screen for, and what is the single most important thing on it?
- What is the one primary action?
- What content is secondary, and what is tertiary?

This is the yardstick for everything that follows. A hierarchy finding is only meaningful against a stated intent.

**Done when:** the primary element, the primary action, and the demoted content are each named. If the surface does not have an obvious primary element, that is itself finding #1.

## Step 3 — Walk the ladder in order

Work rungs 1→8 from the `refactoring-ui` ladder, loading each chapter file as you reach it. **Do not skip ahead** — a spacing complaint on a page with broken hierarchy wastes the user's attention on the wrong fix.

At each rung, record findings as:

| Field | Content |
|---|---|
| Rung | hierarchy / spacing / type / colour / depth / images / finish / craft |
| Observation | what is actually on screen, concretely |
| Principle | the named rule it violates, e.g. "Emphasise by de-emphasising" |
| Fix | the specific change, expressed in existing tokens or utilities |

Stop descending when you have 3–4 findings on the top two rungs — fixing those changes everything below, and a critique with twenty items gets ignored. If the top rungs are clean, keep going to the finish rung.

**Done when:** every rung above your stopping point has been examined and either produced findings or been explicitly cleared.

## Step 4 — Make every fix token-legal

For each fix, resolve the value onto what already exists:

- type → a `text-*` step and its paired `leading-*` (`packages/ui/src/styles/globals.css`)
- colour → a semantic token (`text-muted-foreground`, `bg-warning-soft`), or a `--gm-*` GMS brand colour on GMS surfaces (`packages/gms/src/styles/foundation.css`)
- spacing → Tailwind's own scale
- elevation → `shadow-card`
- radius → `rounded-*`

Any fix that needs a value with no token is **a separate, flagged line item**: a token request for the user to approve, not something to write inline. Say so explicitly rather than substituting the nearest token and staying quiet about it.

**Done when:** every fix is either expressible in existing utilities or flagged as a token request.

## Step 5 — Report, ranked

Present findings **most-impactful first** — which after step 3 means roughly ladder order. For each: the observation, the principle, and the fix.

End with:

- the two or three changes that would do most of the work, if the user only makes a few
- any token requests, listed separately
- anything you could not judge from the material given (interaction states, empty states, dark mode, real data at volume)

**Do not edit any files in this step.** The critique is the deliverable.

## Step 6 — Apply, if asked

Only on the user's go-ahead, and only the findings they name. Then:

```bash
pnpm design-system:check
pnpm fix:changed && pnpm type-check
```

In a shared checkout, format explicit owned files as required by root AGENTS.md.

Before declaring done, grep for other consumers of anything you touched — a shared primitive in `@barrelsgd/ui` reaches every app, and `gaa-admin` alone fronts cap, hr, wxwatch, wxproducts and salesbus. Report what the search surfaced; do not silently widen the edit.

**Done when:** the approved findings are applied, the three commands pass, and the blast radius is reported.
