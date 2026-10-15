---
name: landing-page-art-director
description: Plan a landing page section by section - one hero idea, a proof sequence and one call to action - and choose a component for each slot with a reason, using the Vitrine library at tryvitrine.dev. Use when starting a product, launch or campaign page, or when a landing page feels like a stack of unrelated blocks.
---

# /landing-page-art-director

A landing page is an argument with one conclusion: the action you want. Every section is a step in that argument. Pick components for the step, never the other way round.

## 1. Write the argument before any design

Answer in one sentence each:

1. **Who** lands here, and from where (an ad, search, a friend's link)?
2. **What** do they need to believe to act?
3. **The action:** one primary verb ("Start free", "Book a call").
4. **The proof:** what makes it believable (a demo, numbers, customers, a guarantee)?

The sections are those answers in order: *promise → show it → prove it → remove doubt → ask*.

## 2. Map steps to slots

| Step | Slot | Choose one, e.g. from tryvitrine.dev/components |
|---|---|---|
| Orient | Navbar | `masthead-nav` (editorial), or a plain bar for a product |
| Promise | Hero | `waitlist-hero`, `letterform-hero`, or `local-sky-hero` — plus at most one background (`silk-field`, `dusk-mesh`, `gravity-grid`) |
| Show it | Product moment | `feature-trio`, `step-path`, an AI piece like `agent-run` or `prompt-composer` |
| Prove it | Evidence | `odometer-stats`, `then-now-stats`, `voices-carousel`, a chart such as `pulse-line-chart` |
| Remove doubt | Pricing / FAQ | `subtractive-pricing` or `usage-ruler`; `focus-faq` or `search-faq` |
| Ask | CTA + footer | `focus-pull-cta`, `inline-cta` or `tideline-cta`; `sign-off-footer` |

Check every slug exists in the library before you use it.

## 3. Restraint rules

- **One** signature moment per page: the hero *or* a showpiece section, not both competing.
- **One** moving background at most, behind the hero or the final CTA, never behind body text.
- **One** primary button style repeated. Secondary actions are quieter (a text link or hairline).
- **One** cursor treatment, if any, scoped to a section that benefits from it.
- Pick two typefaces and one accent colour; every component is re-tinted to match.

## 4. Rhythm

- Alternate dense and calm sections. Give the hero and the final CTA the most space.
- Each section's heading is a sentence that advances the argument. Read the headings alone: they should make the case.

## 5. Check

- First screen at 375px: the promise and the primary action are visible without scrolling.
- Run `/accessibility-pass`, `/responsive-audit` and `/performance-pass`, then `/conversion-ux-review` on the finished page.

## Output

The one-line argument, the section table with chosen components and a reason for each, and what was deliberately left out.
