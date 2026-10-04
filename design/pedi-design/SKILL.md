---
name: pedi-design
description: Design, implement, or review light- and dark-mode Pedi-branded websites, mobile apps, product interfaces, internal tools, and marketing surfaces. Use when work must follow Pedi's visual identity, UI tokens, component conventions, theming, responsive behavior, or accessibility standards; do not use for products unrelated to Pedi.
---

# Pedi Design

Create experiences that feel modern, dependable, accessible, friendly, and recognizably Pedi. Preserve the user's requested platform, framework, scope, and existing product behavior.

## Required reference

Read [references/design-system.md](references/design-system.md) before making visual or interaction decisions. It is the canonical source for Pedi colors, typography, spacing, shape, components, imagery, responsive behavior, accessibility, and motion.

Exact token values come from the Figma variables in `figma-variables/`, compiled into:

- [references/tokens.md](references/tokens.md): every color, spacing, radius, width, and typography token, with light and dark values and aliases for colors. Look up exact values here rather than guessing.
- [references/tokens.css](references/tokens.css): the same tokens as CSS custom properties with light, dark, and `system` theme blocks. Copy or import it into web projects that do not already have Pedi tokens, and map existing token systems to its names.

If the Figma export or `typography.json` changes, run `python3 scripts/build_tokens.py` to regenerate both files. Read only the Pedi collections listed in `figma-variables/README.md`; the other kit exports in that folder are not Pedi tokens.

When an existing Pedi implementation conflicts with the reference, do not silently replace an established product convention. Identify the conflict and use the supplied reference as the default unless the user or repository provides a newer authoritative rule.

## Workflow

1. Inspect the existing surface, theme mechanism, design tokens, shared components, assets, and framework conventions before editing. Reuse established Pedi primitives when they conform to the reference.
2. Identify the primary user task and information hierarchy. Keep one clearly dominant action per screen or section, using Pedi Red deliberately rather than as decoration.
3. Apply the design system through the semantic and component tokens in `tokens.md` rather than raw hex values or primitive ramps. Support both light and dark appearances when the product has or requests them, while preserving an established theme mechanism.
4. Adapt the experience for its context: consumer surfaces should feel spacious; admin and data-heavy surfaces may be denser without sacrificing readability.
5. Verify responsive states, keyboard focus, labels, contrast, touch targets, non-color status cues, loading and error states, and reduced-motion behavior where motion is present.
6. Review the result against the checklist below and validate it using the project's normal checks. When visual tooling is available, inspect both light and dark themes at representative mobile and desktop widths.

## Design decisions

- Consistency takes priority over novelty. Extend established patterns before inventing new ones.
- Pedi Red (`--color-brand-500`) is the brand color, and filled primary actions use `--color-button-primary-bg` (`--color-brand-600`). Pedi Navy supplies contrast and secondary emphasis. Semantic colors communicate state, not decoration.
- Dark mode is a designed theme, not an inversion filter. Preserve Pedi's hierarchy and warmth by mapping semantic surface, text, border, action, and status tokens to deliberate dark values.
- Use Inter for all interface text, from display headings to metadata; build hierarchy with size and weight. Outfit is reserved for the Pedi logo, so use the logo asset and never set UI text in Outfit. Use readable fallbacks when Inter is unavailable and do not claim the typography is complete until the font is loaded. Keep typography configurable: consume the `--font-family-*`, `--font-weight-*`, and `--text-*` tokens (from `typography.json`) through the project's theme, and never hard-code font names or sizes in components.
- Prefer whitespace, alignment, borders, and restrained elevation over heavy shadows, gradients, or decorative containers.
- Use rounded forms consistently without turning ordinary buttons, inputs, and cards into pills.
- Pair destructive wording with an icon or confirmation when warranted because the primary brand color is also red.
- Do not invent brand assets, photography rules, or product-specific interaction patterns that the reference does not define. Ask for or preserve authoritative assets when exact brand reproduction depends on them.

## Completion checklist

- The primary task and action hierarchy are immediately clear.
- Colors, type roles, spacing, radii, surfaces, and icon treatment follow the reference.
- Fonts, sizes, line heights, and weights come from typography tokens or theme configuration, so the typeface or scale can be changed in one place.
- Light, dark, and system theme settings render without illegible text, missing assets, incorrect browser chrome, or a flash of the wrong theme.
- Pedi Red is not overused and competing primary actions have been removed.
- Forms have visible labels, clear focus and validation states, and helpful errors.
- Status is communicated by text or icons in addition to color.
- Mobile is an adapted layout, not merely a shrunken desktop layout.
- Text remains readable, controls have adequate targets, and keyboard navigation is visible in every supported theme.
- Animation is subtle, fast, purposeful, and respects reduced-motion preferences when implemented.
- The result fits the surrounding Pedi product while remaining recognizably part of the same ecosystem.
