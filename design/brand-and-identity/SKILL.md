---
name: brand-and-identity
description: Use when establishing brand foundations before any design work, when two products need to feel related, when defining voice and tone for microcopy, or when logo usage and visual identity rules need documenting.
---

# Brand and Identity

## Overview

Pin down brand essence, logo rules, color identity, typography identity, voice and tone, icon system, illustration style, and multi-product consistency *before* design tokens get chosen. Output is `.forge/brand-identity.md`. Upstream of `design-system` — brand colors map to UI semantic tokens; voice rules shape every microcopy decision; the icon system is inherited by `component-library`.

## When to Use

- A new company or product is being designed and no brand foundation exists
- A second product is being added to a shared brand and the relationship needs defining
- Microcopy is drifting (different voice in onboarding vs errors vs empty states)
- A logo is being used in slides, marketing, and product UI with no documented rules
- Icons in the product mix three styles (outlined, filled, custom) and the team can't agree

## When NOT to Use

- A single internal admin tool with no external surface — skip to `design-system`
- A backend-only service
- A trivial visual tweak inside one screen — that's `incremental-implementation`

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "We'll figure out the brand later" | Every screen you ship without brand rules is brand debt. Later means inconsistency baked into 50 screens. |
| "Just pick a color and go" | A color without a system becomes 15 slightly different blues across two products. |
| "Microcopy doesn't matter" | Users read microcopy more than marketing copy. Every button label is a brand moment. |
| "We don't need logo rules, it's just us" | The moment someone else makes a slide deck, they'll stretch the logo. Rules prevent this. |
| "One product, no need for multi-product rules" | Products multiply. Define what's shared on day one, not day 365. |

## Red Flags

- Logo used without clear space (text or graphics touching the mark)
- Brand colors used as UI colors directly with no semantic mapping
- Different voice in different parts of the product (formal in errors, casual in onboarding)
- Icon styles mixed in the same view (outline + filled + custom)
- No empty-state copy guideline — engineers write "No data found" by default
- Typography mixing brand and UI faces with no documented role split

## Core Process

### Step 1: Brand essence

One sentence that captures what the company feels like. Not what it does — what it feels like. "Calm in chaos." "Receipts, not opinions." "The clipboard that thinks." If the sentence could describe three other companies, it's too generic.

### Step 2: Logo usage

- **Clear space:** minimum padding around the mark, expressed in units of the mark's own height (e.g., `0.5x`).
- **Minimum size:** smallest legible size in print (`24px` digital, `0.5in` print).
- **Color variants:** full color, single-color (mono dark + mono light), reversed (for dark backgrounds).
- **Never do:** stretch, recolor (outside the variant set), rotate, add effects (shadow, gradient, outline), place on a busy photo without a scrim.

### Step 3: Color system — brand vs UI

Brand colors and UI colors are **different layers**.

- **Brand colors** drive marketing, identity, logo, OG cards, slide decks. A small palette (1 primary + 1 accent + 1–2 supporting).
- **UI colors** drive product surfaces and live in `design-system` as semantic tokens (`accent`, `surface`, `danger`, etc.).

Document the mapping explicitly:

```
brand.primary  → UI.accent
brand.accent   → UI.accent-emphasis (or product-specific)
brand.neutral  → UI.surface scale (light + dark variants derived here)
```

A brand color may never appear in product code as a raw hex — it always enters through a semantic token.

### Step 4: Typography identity

- **Brand typeface:** for marketing/headings/identity. Often display-oriented, often paid.
- **UI typeface:** for product. Often a system font or open-source for performance and legibility at small sizes. May be the same face as brand or different.
- **Weight roles:** which weights are used for what (e.g., `regular` body, `medium` UI emphasis, `semibold` headings, `bold` reserved for hero only).

If brand and UI faces differ, document the visual relationship — they must look intentional together, not accidental.

### Step 5: Voice and tone

How the product speaks. Examples, not just adjectives:

- **Button labels:** action verbs. "Save report" not "OK". "Send invitation" not "Submit".
- **Empty states:** helpful + brief + actionable. "No calls yet. Record your first one." not "No data found".
- **Error messages:** what happened + what to do. "Couldn't save. Check your connection and try again." not "Error 500".
- **Onboarding:** warm, encouraging, no jargon. "Let's set up your first team." not "Initialize workspace configuration."
- **Confirmation:** confident, not apologetic. "Report saved." not "Your report has been successfully saved."

Pick a voice axis pair (e.g., "friendly but not casual", "expert but not technical") and stress-test every category against it.

### Step 6: Iconography and illustration

- **Icon system:** one library (Lucide, Phosphor, Heroicons, or custom). Pick one style (outline OR filled, not both). Document size scale: `16 / 20 / 24 / 32`. Icons larger than 32px usually want illustration territory instead.
- **Icons vs text:** use icons with text labels for primary actions; icon-only is fine for universally-understood affordances (search, close, settings) — never for ambiguous ones.
- **Illustration style:** line art, flat, isometric, 3D, photographic, or none. Choose one. Empty states and onboarding use this style consistently.
- **When NOT to illustrate:** dense data screens, settings forms, error states for technical users — illustrations there feel patronizing.

### Step 7: Multi-product consistency

If two or more products share a brand:

- **Shared:** logo, brand color palette, voice, icon system, typography identity.
- **Distinct per product:** UI accent (a hue shift inside the brand palette), domain-specific icons, product name + favicon, OG art.

State the design promise: *"Someone using Product A and Product B should feel they're from the same company but know they're different products."*

### Step 8: Write `.forge/brand-identity.md`

Sections in this order: Essence, Logo, Color, Typography, Voice, Iconography & Illustration, Multi-product. Prepend a `forge:meta` header (`generated_by: brand-and-identity`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: []` — independent, no upstream, `generated_from: {}`, `content_hash: <sha256 first 8 of THIS file's body>`). See [forge-dependency-graph](../../references/forge-dependency-graph.md).

## Verification

- [ ] Brand essence is one sentence, specific enough to exclude three other companies
- [ ] Logo section lists clear space, minimum size, color variants, AND a "never do" list
- [ ] Brand colors map to UI semantic tokens — no brand hex appears in component code
- [ ] Typography identity names a brand face, a UI face, and weight roles per face
- [ ] Voice guidelines include concrete examples for buttons, errors, empty states, AND onboarding
- [ ] Icon system is one library with one style (outline OR filled, not both); size scale documented
- [ ] Illustration style decided (or explicitly "none")
- [ ] Multi-product section defines shared vs distinct elements (or notes "single product")
- [ ] `.forge/brand-identity.md` written with `forge:meta` header
