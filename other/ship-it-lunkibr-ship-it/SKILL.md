---
name: ship-it
description: Use this skill whenever building, reviewing, or auditing any product surface — a mobile app screen, a web app (in-product) screen, a marketing website page, or a cross-screen interaction flow — especially right before calling it done or shipping it. Start here to identify which section (mobile app, web app, website, flow, and more as they're added) the surface belongs to, then drill down to name every pattern (login, checkout, billing, pricing, admin panel, empty state, and more) it should have and flag which are missing — weighed against what this specific product actually is, never applied as a blind checklist. Trigger even when the user just says a screen or page is finished or asks for a review, not only when they say "checklist."
---

# Ship It

Catalog of product/UX patterns — one section per surface type (mobile app, web app, website, flow, more to come), one file per pattern within a section. Never load a pattern file, or a section you're not working in, before you need it.

## Steps

1. **Build a one-line picture of the product** — what it does, who it's for, and which capabilities it actually has (sells something, runs subscriptions, accepts uploads, has teams/multi-user accounts). Pull this from the code, README, or prior conversation first; ask the person directly only for the specific unknowns that would change a judgment call (see Judgment calls). This picture is what step 3 is weighed against — skipping it is what turns a checklist into noise.
2. **Identify the section(s) in scope** — mobile app, web app, website, flow, or a section added later (see `sections/`). A task usually touches one section; ask only if genuinely ambiguous.
3. **Open that section's index** (table below) and, from its pattern names, tiers, and one-liners alone, list which patterns the current project already has, is currently building, or lacks outright. Start from each pattern's tier as the default assumption, then weigh it against the picture from step 1 before naming a gap — see Judgment calls. Don't open a pattern file for this step.
4. **For each pattern actually being built, reviewed, or fixed right now**, open its reference file (linked from the section index) and check the implementation against every item in it, applying the same per-item judgment (an item needing a capability this product doesn't have is not a gap).
5. **Report gaps grouped by pattern**, pointing at the actual file/line. Separate what's clearly expected from what's worth confirming with the person rather than presenting both with equal certainty.

## Judgment calls

A pattern or item only counts as a gap if the product's own context calls for it — never because the section index lists it. Every pattern carries a **Tier**, set in its section index, that fixes the starting assumption before any product-specific reasoning runs — without it, "use judgment" has no anchor and drifts toward whichever way is less work.

- **Fundamental** — expected on virtually every product in the section, independent of business model (Security, Privacy, 404, Contacting support-adjacent basics). Assume it applies. Exclude only for a stated, unusual reason, and treat that reason with real suspicion — this tier is where waving something away costs the most (legal exposure, not just a rough edge).
- **Common** — expected on most products of this kind, with ordinary, real exceptions (Billing, Checkout, Making a card payment: most monetized products need some payment flow, but plenty of legitimate products are free or sales-led). Assume it applies unless the product picture from step 1 clearly rules it out; state the one-line reason when it does.
- **Conditional** — applies only once a specific, narrower capability is confirmed present, not just plausible in general (Cart, Adding to cart, Entering promo code: need multi-item purchase specifically, a narrower thing than "this product takes payment"). Assume it does **not** apply until that capability is confirmed; don't ask the person to build the capability just to satisfy the pattern.

This is why payment outranks cart even though neither is Fundamental: most products that charge money do so through some Common-tier payment flow, but only a subset of those need a Conditional-tier multi-item cart on top of it.

Beyond the tier itself:

- **Stage counts as context too.** A pre-launch waitlist page isn't missing a Pricing page; a two-person startup isn't missing a Careers page — both are absent on purpose, not by oversight, regardless of either pattern's tier.
- **Once the person has confirmed an exclusion, don't raise it again this session.** Accept the answer and move on — repeating a question the person already answered reads as nagging, not thoroughness.
- **When it's genuinely unclear, say so and ask** — don't silently assume a pattern applies (noise) or silently assume it doesn't (a missed gap presented as if it were checked).

## Sections

| Section | Patterns | Index |
|---|---|---|
| Sidekick (mobile app) | 20 | [sections/sidekick.md](sections/sidekick.md) |
| Control Room (in-product web app) | 10 | [sections/control-room.md](sections/control-room.md) |
| Storefront (marketing website) | 23 | [sections/storefront.md](sections/storefront.md) |
| Choreography (cross-screen flows) | 13 | [sections/choreography.md](sections/choreography.md) |

More sections are added as new categories are ingested — each gets one row here and one file under `sections/`, following the same shape.

## Cross-cutting patterns

Billing, Login, Account, Settings, Search, and Cart each show up in more than one section's index (a mobile app and a website both need a Cart, for instance). Each still resolves to exactly one reference file — the pattern was reviewed once, from whichever section index you reached it, never re-checked per section. Flow patterns overlap the other sections' patterns more loosely (e.g. "Resetting password" is a sub-flow of Login, "Deleting account" of Account) — until those are reconciled, treat a Flow pattern and a same-topic screen pattern as two different checks, not duplicates.
