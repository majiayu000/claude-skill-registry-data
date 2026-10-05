---
name: inov8-orthopedics-design
description: This skill should be used when the user wants to design, prototype, or build anything branded for INOV8 Orthopedics or INOV8 Surgical (Houston, TX), such as a web page, slide, mock, email, form, dashboard, or production UI. Triggers on phrases like "INOV8 branding", "make this look like INOV8", "INOV8 design system", "INOV8 colors", "INOV8 Orthopedics page", "use our brand", or any request for INOV8-branded output. Points the agent at the brand book, the token files, and the component previews in this folder, and enforces the brand's hard rules.
---

# INOV8 Orthopedics design system

This folder is a mirror of the INOV8 Orthopedics design system. Read it before producing any INOV8-branded output, then design with its tokens and rules rather than from memory.

## Read these first, in order

1. `README.md` — the brand book: brand context, voice and casing rules, visual foundations, iconography, assets, open caveats. Every rule below is explained there.
2. `tokens.css` — every color, type, spacing, radius, shadow, and motion token as CSS custom properties, plus one class per type style (`.display`, `.h1` … `.h6`, `.body`, `.lead`, `.eyebrow`, `.caption`, `.label`). Link or inline this file in HTML output and use its variables instead of raw values.
3. `tokens.json` — the same tokens as data, each with a usage note. Read it when generating non-CSS output (slides, native UI, design tools).
4. `api/tokens.md` and `api/components/<Component>.md` — short cards per token family and per showcase component. Read a component's card before reusing its pattern.
5. `components/<Component>/preview.html` — live examples of badges, buttons, CTA block, forms, icons, info card, nav, physician card, procedure card, and the full home page (`Index`). Copy patterns out of them.

Also available: `components/bundle.css` (component classes such as `.gradient-rule`, `.eyebrow`, `.name-emphasis`), `components/assets/inov8-logo.png` (the wordmark, full color, transparent background), `components/Index/*.jsx` (the home page's React sources), and `ui_kits/website/index-standalone.html` (the home page as one self-contained file).

## Hard rules

- Write the brand name as **INOV8**: all caps, the digit 8, no space, no hyphen.
- Sentence case for headlines, buttons, navigation, and labels. Title Case only for proper nouns and product names. No exclamation marks, no emoji, no urgency marketing.
- "We" for the practice, "you / your" for the patient. Never "I".
- List specialties in this order: Hip, Knee, Shoulder, Elbow, Sports Medicine, Physical Therapy.
- The brand gradient (`--inov8-gradient`, teal to navy) is for the wordmark, hero accents, and the 4 px `.gradient-rule` divider only. Never as a CTA fill, never behind body text.
- Primary CTA and accent color is `--cyan-500` (#00A9D2). Dark surfaces use `--navy-900` (#20265A). Headings on light sit at `--navy-950`.
- Display headings use `--font-display` (Jost) at `--fw-light` (300). Never bold or black weights for display; semibold (600) is the ceiling anywhere.
- Body and UI text use `--font-body` (DM Sans).
- Corners: `--radius-md` (10 px) for cards and buttons, `--radius-pill` for chips and the primary CTA, `--radius-xs` for small inputs.
- Shadows are the four navy-tinted steps `--shadow-xs` to `--shadow-lg`. Never pure black. Focus rings use `--shadow-focus`; never remove them.
- Icons are Lucide, 1.5 px stroke, rounded caps, used sparingly. No decorative marketing iconography.
- Photography over illustration; flat backgrounds; no textures or patterns.
- On dark surfaces show the wordmark reversed to white with `filter: brightness(0) invert(1)`. Never recolor the gradient.

## How to work

- For throwaway visuals (mocks, slides, prototypes) produce a self-contained HTML file: inline `tokens.css` and the relevant parts of `components/bundle.css`, embed the logo as a data URI, and load fonts from Google Fonts (Jost, DM Sans).
- For production code, copy `tokens.css` and `components/bundle.css` into the project and reference variables and classes from them. Do not fork values.
- If the user invokes this skill with no other guidance, ask what they want to build, who will see it, and whether it is a mock or production work, then act as an expert designer for this brand.
- Keep the source's known contrast misses in mind and do not make them worse: white on `--brand` and on `--accent`, `--link` on white, and `--warning-500` on white all fall short of 4.5:1. Prefer `--cyan-600` / `--cyan-700` for text-sized cyan and `--navy-950` for body emphasis.

## Open substitutions

Flag these if they matter to the task; do not silently fix them.

- Fonts: Jost and DM Sans are Google Fonts substitutes for unspecified brand typefaces.
- Icons: Lucide substitutes for an in-house set that does not exist yet.
- Photography: image slots are placeholders; no licensed photography ships here.
- Accreditation marks (ISTA, AAHKS, ABOS, AAOS) are not redistributed.

## Where this comes from

The source of truth is the Claude design-system artifact named in `ARTIFACT.md`; this folder is re-synced from it. Edit the artifact, not these files, unless the change is repo-only (`ARTIFACT.md`, this `SKILL.md`).
