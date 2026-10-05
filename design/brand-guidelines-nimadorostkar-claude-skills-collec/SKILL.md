---
name: brand-guidelines
description: Use when applying or documenting a brand identity. Covers extracting a system from existing assets, documenting colour, type, and voice, and applying a brand consistently across new work.
metadata:
  category: design
  version: 1.0.0
  tags: [brand, identity, guidelines, consistency, style]
---

# Brand Guidelines

## Purpose

Apply a brand consistently, and document it well enough that someone else can too. A brand that exists only in one designer's judgment is not a brand; it is a taste.

## When to Use

- Applying an existing brand to new material.
- Documenting a brand that has never been written down.
- Auditing material for brand consistency.
- Extracting a system from a set of existing assets.

## Capabilities

- Extracting colour, type, spacing, and voice from existing assets.
- Documenting a usable brand system.
- Applying a brand across media.
- Auditing for drift.

## Inputs

- Existing brand assets, or a brand guideline document.
- The material to be produced or audited.
- The medium and its constraints.

## Outputs

- A documented system: colour, type, spacing, imagery, voice.
- Material that is on-brand and can be verified as such.
- A list of the places the brand has drifted.

## Workflow

1. **Extract before inventing** — If a brand exists in assets but not in a document, derive it: sample the colours, identify the typefaces, measure the spacing, read the copy for voice. What is consistent across the assets is the brand; what varies is drift.
2. **Document the decisions, not just the values** — "Primary blue #2563EB, used for actions and links only. Never for large fills." The constraint is the useful part.
3. **Cover the cases people get wrong** — Minimum logo size, clear space, what to do on a dark background, what happens when the brand colour fails contrast.
4. **Document the voice** — It is half the brand and it is nearly always omitted. Give examples of on-brand and off-brand copy.
5. **Apply, then audit** — Check the output against the system rather than against instinct.

## Best Practices

- A brand guideline without a "do not" section is not usable. The prohibitions are what prevent drift.
- Colour is where drift starts. Two similar blues in circulation becomes five within a year.
- The brand's primary colour frequently fails accessibility contrast for text. Document what to use instead, before someone ships an unreadable button.
- Voice examples do more than adjectives. "Confident, not arrogant" means nothing; a before-and-after pair of sentences means something.
- Logo misuse — stretching, recolouring, placing on a busy photograph — is universal and is prevented only by showing the wrong version explicitly.
- A brand that cannot survive being applied by a non-designer is not documented well enough.

## Examples

**A brand system documented so that it can be applied:**

```markdown
## Colour

| Token                | Hex      | Use                                      | Never                        |
|----------------------|----------|------------------------------------------|------------------------------|
| brand/primary        | #2563EB  | Primary actions, links, active states     | Large fills; body text       |
| brand/primary-dark   | #1D4ED8  | Hover and pressed states only             | Anything else                |
| brand/ink            | #111827  | Body text, headings                       | —                            |
| brand/paper          | #FFFFFF  | Backgrounds                               | —                            |
| brand/accent         | #F59E0B  | Warnings, highlights. Sparingly.          | More than one per screen     |

**Contrast:** `brand/primary` on white is 4.6:1 — it passes for body text but only
just. For text below 16px, use `brand/primary-dark` (7.1:1). Never place
`brand/accent` text on white: it is 2.1:1 and unreadable.

## Type

Display : Söhne, 600 weight. Headings only. Tracking -0.02em above 32px.
Text    : Söhne, 400/500. Body, UI, everything else.
Never   : a third typeface. Hierarchy comes from size and weight.

## Voice

We are direct and specific. We do not hedge, and we do not perform enthusiasm.

| Off-brand                                          | On-brand                                    |
|----------------------------------------------------|---------------------------------------------|
| "Oops! Something went wrong."                     | "We couldn't save your changes. Try again." |
| "We're thrilled to announce an exciting new..."     | "Exports now include line items."           |
| "Please kindly note that you may wish to consider"  | "You can also..."                           |

## Logo

- Minimum width: 24px (digital), 20mm (print).
- Clear space: the height of the mark, on all four sides.
- On photography: use the white version, on an area of the image with
  low detail. Never on a busy background.
- Never: stretch, rotate, recolour, add effects, or place inside a shape
  that is not part of the mark.
```

## Notes

- The contrast note above is the kind of detail that separates a usable guideline from a decorative one. A brand colour that fails contrast for small text will be used for small text unless the document says what to use instead.
- Voice tables with a wrong/right pair are the most effective format for the writing half of a brand. Adjectives are not actionable.
- Audit quarterly. Brand drift is gradual, and it is only visible when the current material is placed next to the guideline.
