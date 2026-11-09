---
name: "logo-design"
description: "Generate logo variants for a brand, producing multiple production-grade marks across different architectures (wordmark, lockup, symbol-only, letterform-as-symbol, monogram) with rationale, application specs, and decision-ready presentation. Distinct from `brand-identity`, which produces the complete system (logo plus color, type, voice, applications). Goes deep on the logo specifically: typographic register, symbol approach, application-context discipline (16px favicon, embroidery, signage, motion), and production specs (SVG-ready, single-color, reverse). Triggers on logo design, design a logo, wordmark, monogram, lockup, mark variants, logo iterations, redesign or refine the logo, logo refresh, letterform-as-symbol, and exploring mark variants for an established brand. Does NOT fire for full brand identity (use `brand-identity`), positioning or strategy (use `brand-discovery`), project-wide creative direction (use `creative-direction`), or one-off illustration."
---

# Logo Design

A logo is a system of marks, not a single drawing. This skill produces multiple production-grade variants exploring different architectural approaches, each with rationale, application specs, and a clear position on what it signals and rejects.

The output is decision material, not a finished logo. The brand owner selects from the variants and the skill produces production refinement on the chosen direction.

---

## When to use

- The brand has a name and tonal direction; the deliverable is logo work specifically
- Generating 6 to 12 variants for client review and selection
- Refining a wordmark to production: kerning, optical adjustments, weight selection
- Exploring symbol options to pair with an existing wordmark
- Designing a monogram from a longer name for use in constrained contexts
- Adapting an existing logo across application contexts (small-size, signage, motion, embroidery)
- The brand owner has reviewed a first round and wants iteration on a specific direction

## When NOT to use

- Use `brand-identity` instead when the deliverable is the complete identity system (logo plus color plus type plus voice plus applications). This skill is the logo-specific layer; brand-identity is the system layer.
- Use `brand-discovery` for brand positioning, audience, and voice work. A logo without strategy is a drawing.
- Use `creative-direction` for project-wide aesthetic direction. Creative direction calibrates many decisions; logo design produces specific marks.
- One-off illustration, icon, or pictogram work
- Designing brand patterns, textures, or supporting graphics
- Pure typographic exploration unrelated to a brand name

---

## Required inputs

- **Brand name.** Exact spelling. Capitalization and punctuation preferences if any. Whether the name has a category descriptor that travels with it (e.g., "Atlas Coffee" vs just "Atlas").
- **Industry or category.** Legal firm, consumer goods, B2B SaaS, hospitality, etc. Category implies defaults that can be honored or broken.
- **Audience.** Who sees the logo, where, in what state of mind. The audience-side perception drives selection more than the founder-side aesthetic.
- **Tonal direction.** Where on the formal-to-casual axis. Where on the restrained-to-expressive axis. Where on the heritage-to-modern axis.
- **Application contexts.** Common set: web header, mobile app icon (28px), favicon (16 to 32px), business card, letterhead, email signature, social profile picture, signage (large format), embroidery patch (1.5 inch), single-color print, video motion lockup, merch (apparel, hats, totes).
- **Reference logos liked**, with a sentence each on what specifically resonates. The reference clarifies which architecture and register fit better than abstract description does.
- **Reference logos disliked**, with a sentence on what to avoid. Negative space sharpens positive selection.
- **Hard constraints.** Must include element X. Must avoid color Y due to industry conventions. Must reproduce in single color. Must work as a 16px favicon. Must survive embroidery.
- **Optional**: existing brand assets if the project is a refresh, not greenfield. Existing wordmark if the work is symbol-only. Existing color palette if it must remain locked.

---

## Workflow

1. **Gather inputs.** Required inputs above. If the user has reference logos, walk through what specifically resonates in each. The references calibrate which architecture and register actually fit.

2. **Establish primary architecture.** Wordmark-only? Lockup? Letterform-as-symbol? Monogram? This is the foundational decision; everything else flows from it. For most new brands with a distinctive descriptive name, the right architecture is lockup with literal or letterform-derived symbol, plus a monogram fallback for square contexts.

3. **Generate typographic explorations.** Produce 3 to 4 wordmark-only variants exploring different typographic registers. Each variant should be a complete, kerned, optically-adjusted wordmark. These serve as both standalone candidates and as the foundation for subsequent symbol pairing.

4. **Generate symbol explorations** (if architecture includes a symbol). For each typographic exploration, generate 1 to 2 symbol pairings using different symbol approaches (literal, abstract gesture, letterform-derived, monogram). The symbol must visually agree with the wordmark's type weight, optical density, and tonal register. A heavy slab wordmark needs a chunky symbol; a hairline geometric wordmark needs a thin symbol.

5. **Test each variant against application contexts.** For each candidate, walk through 16px favicon, 1.5 inch embroidery, single-color reproduction, square stacked alternate. Eliminate variants that fail more than two contexts. Document which contexts each variant excels in versus needs a fallback for.

6. **Pick top candidates for client review.** Typically 6 to 12 final variants. Each variant must be visually distinct from the others. Variants that are too similar dilute the review and frustrate the client (they cannot tell why they should pick one over the other).

7. **Document each variant.** Per-variant: descriptive name (e.g., "01, Light geometric wordmark, Avenir Next"), architecture, typography, symbol approach if applicable, color tokens, application notes, signals (what it communicates), rejects (what it explicitly is NOT).

8. **Provide production specs** for the top 3 candidates. SVG-ready construction notes, color hex codes (primary plus single-color black plus single-color white plus reverse), sizing guidelines (minimum sizes per medium), motion entry and exit recommendation, embroidery and foil-stamp adaptations.

9. **Provide application mockups.** Render each top candidate in 3 to 5 representative contexts: web header, business card, favicon at 16 and 32px, embroidery patch, signage. Mockups can be image-generated or schematic. The point is to show the client how the mark lives across contexts, not to deliver finished marketing material.

10. **Hand off.** Output is decision material. The brand owner selects a direction. The skill (or a follow-up iteration) then produces production refinement on the chosen path: cleaner construction, refined kerning, color system finalization, application library.

---

## Output format

Default output is a markdown spec with multiple variants, typically saved as `logo-variants.md` at the project root or in a `design/` subdirectory. The spec is paired with rendered images for each variant, saved alongside (typically in `design/logo-variants/`).

Per-variant structure:

1. **Variant name.** Descriptive identifier with index (e.g., "01, Light geometric wordmark, Avenir Next" or "07, Mountain peak A lockup, IBM Plex Sans").
2. **Architecture.** Wordmark / Lockup / Symbol / Letterform-as-symbol / Monogram.
3. **Typography.** Specific typeface name and weight. Custom letterform notes if any. Tracking and kerning treatments.
4. **Symbol description** (if applicable). Approach (literal / abstract gesture / geometric reduction / letterform-derived / monogram) and visual description. Construction grid notes if relevant.
5. **Color tokens.** Hex codes for primary palette, single-color black version, single-color white version, reverse-on-dark treatment.
6. **Application notes.** Which contexts the variant excels in (e.g., "strong at large signage and letterhead") and which contexts need a fallback mark (e.g., "favicon falls back to letterform-as-symbol at 16px"). Embroidery adaptation notes if relevant.
7. **Signals.** What this variant communicates about the brand. The features it foregrounds.
8. **Rejects.** What this variant explicitly is NOT. The negative space the variant creates.
9. **Mockups.** Rendered in 3 to 5 application contexts. At minimum: web header, business card, favicon. Bonus: embroidery patch, large-format signage, social profile.

The spec is decision material. The next step after delivery is selection plus production refinement on the chosen direction.

---

## Reference files

- [`references/architectures-explained.md`](references/architectures-explained.md). The 5 mark architectures with examples, when each fits, when each fails, and how to combine them in a primary plus fallback hierarchy.
- [`references/typographic-registers.md`](references/typographic-registers.md). The typographic registers with named typefaces, category-fit notes, and example brands per register.
- [`references/symbol-approaches.md`](references/symbol-approaches.md). The 5 symbol approaches with pattern examples, calibrating the agent's vocabulary for symbol generation.
- [`references/application-contexts.md`](references/application-contexts.md). The contexts every logo must pass, with constraint specs (favicon size, embroidery color count, single-color rules, motion entry recommendations).
- [`references/category-conventions.md`](references/category-conventions.md). A survey of common conventions across major brand categories, with defaults that work, conventions worth honoring, conventions worth breaking for positioning, and category-specific application contexts.
- [`references/example-variant-spec.md`](references/example-variant-spec.md). A complete example showing all nine per-variant fields filled in for a representative project.
- [`references/client-package.md`](references/client-package.md). The package format clients expect at delivery: file format matrix, variant matrix, folder structure, naming convention, documentation layer (usage guide plus brand colors plus license), delivery mechanisms, and the failure patterns that send the client back asking for a missing variant.


## Conditional methods

Before applying a method below, read its linked section. For a narrow task select only relevant methods; for a full audit/design use the framework and relevant failure patterns. Existing references remain available for deeper details.

- The framework: 5 considerations for logo design: [method](references/domain-guide.md#the-framework-5-considerations-for-logo-design).
- Failure patterns: [method](references/domain-guide.md#failure-patterns).
