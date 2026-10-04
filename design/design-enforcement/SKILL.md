---
name: "design-check"
description: "Anti-generic design enforcement -- catches AI-generated visual antipatterns and verifies brand compliance."
---

# Design Enforcement Check

<!-- WHY THIS SKILL EXISTS:
AI coding agents produce visually functional but aesthetically identical UIs. Left
unchecked, every AI-built app converges on the same gray cards with rounded corners.
This skill is a mechanical antidote: it catalogs the specific antipatterns, defines
what "on-brand" means for YOUR project, and provides a 27-item checklist that must
pass before any visual change ships. Invoke it every time you create or modify a
component, page, or layout. -->

You have been asked to verify design compliance. Read every section. Apply the checklist
to the component or page you are building. Do not skip items.

---

## Section 1: AI-Generated AntiPatterns

These are the five most common ways AI-produced UIs look generic. Learn to recognize
them so you can actively avoid them.

### 1.1 Tailwind Default Syndrome

The agent reaches for the same utility classes on every component:

- `rounded-lg` on everything (buttons, cards, inputs, avatars -- all the same radius)
- `bg-gray-50`, `bg-gray-100`, `bg-zinc-800` as the only surface colors
- `p-4 gap-4` as universal spacing (everything 16px apart, no rhythm)
- `shadow-sm` or `shadow-md` on every elevated surface
- `text-gray-500` for all secondary text regardless of context

**The tell:** screenshot any two pages and they look like the same page with different content.

### 1.2 Typography Flatness

- Inter or system-ui as the only typeface
- Two sizes only: "normal" and "slightly bigger"
- No weight variation within a page (everything is font-medium or font-semibold)
- Headings are just bigger body text -- same font, same weight, same tracking
- No italic, no letter-spacing variation, no typographic personality

**The tell:** cover the content and you cannot tell if you are on a landing page, a settings panel, or a dashboard.

### 1.3 Layout Monotony

- Everything in a CSS grid of equal-width cards
- Content centered on every page
- Uniform gap between all elements (no visual grouping through spacing)
- No asymmetric layouts, no sidebar variation, no content that breathes
- Padding is identical on mobile and desktop (just reflowed)

**The tell:** remove all text and images -- the wireframes of every page are interchangeable.

### 1.4 Missing Personality

- Button labels: "Submit", "Cancel", "Save", "Delete" -- no voice, no context
- Empty states: "No items found" with a generic illustration
- Loading states: a centered spinner, nothing else
- No micro-interactions (hover states are just color shifts)
- Transitions are either absent or uniform 150ms ease-in-out on everything
- No delight moments anywhere in the flow

**The tell:** replace the logo and the app could belong to any company in any industry.

### 1.5 Dark Mode Failures

- Dark mode is light mode with colors inverted
- All surfaces are the same dark shade (no elevation through luminance)
- Pure white (#FFFFFF) text on pure dark (#000000) backgrounds (harsh, not readable)
- Accent colors unchanged from light mode (saturation too high for dark surfaces)
- Borders invisible or too prominent -- no middle ground

**The tell:** squint at the screen and you see a flat rectangle with no visual hierarchy.

---

## Section 2: Design Constraints (Non-Negotiable)

<!-- [CUSTOMIZE] Replace everything in this section with your project's actual design
system. The structure (colors, typography, spacing, radii, elevation) should stay;
the values must be yours. -->

### Colors

Use design tokens exclusively. No raw Tailwind color utilities.

```
/* [CUSTOMIZE] -- replace with your token values */
--color-bg-primary: #0F1117;
--color-bg-elevated: #1A1D27;
--color-bg-surface: #242833;
--color-text-primary: #E8E6F0;
--color-text-secondary: #9B97A8;
--color-accent: #5B7FFF;
--color-accent-hover: #7B9AFF;
--color-success: #34D399;
--color-warning: #FBBF24;
--color-error: #F87171;
```

**Banned:** `bg-gray-*`, `bg-zinc-*`, `bg-slate-*`, `text-gray-*`, `text-zinc-*`,
`text-slate-*`, `border-gray-*`. Zero instances permitted.

### Typography

**[CUSTOMIZE]** -- specify your actual font stack.

| Role    | Font                | Fallback   | Usage                        |
|---------|---------------------|------------|------------------------------|
| Display | [Your display font] | serif      | Page titles, hero text       |
| Body    | [Your body font]    | serif      | Paragraphs, descriptions     |
| UI      | [Your UI font]      | sans-serif | Buttons, labels, inputs, nav |

Every page must use at least 2 of these 3 roles. A page using only the UI font fails.

### Spacing

Every screen must use at least 3 different spacing values. Uniform spacing (all `p-4 gap-4`)
is a failure. Use the design token scale:

```
--space-1: 4px;    --space-2: 8px;    --space-3: 12px;
--space-4: 16px;   --space-5: 20px;   --space-6: 24px;
--space-8: 32px;   --space-10: 40px;  --space-12: 48px;
--space-16: 64px;
```

### Corner Radii

Vary by component type. Do NOT use `rounded-lg` on everything.

| Component      | Radius               |
|----------------|----------------------|
| Buttons        | `rounded-md` (6px)   |
| Cards / Panels | `rounded-xl` (12px)  |
| Inputs         | `rounded-sm` (4px)   |
| Avatars        | `rounded-full`       |
| Modals         | `rounded-2xl` (16px) |

**[CUSTOMIZE]** -- adjust radii to match your brand.

### Elevation (Dark Backgrounds)

On dark themes, elevation is communicated through luminance, not shadows.

- Level 0 (page background): darkest value
- Level 1 (cards, panels): slightly lighter
- Level 2 (dropdowns, modals): lighter still
- Borders: subtle (1px, low-opacity) to reinforce edges
- `shadow-*` utilities: use sparingly and only with low-opacity, colored shadows (not black)

---

## Section 3: Anti-Generic Checklist

Run every item against the component or page you are building. Mark each PASS or FAIL.

### Typography (7 items)

1. [ ] Display/heading font is NOT the same as body/UI font.
2. [ ] At least 3 distinct font sizes are used on this screen.
3. [ ] At least 2 distinct font weights are used on this screen.
4. [ ] Letter-spacing varies (tighter on headings, normal on body).
5. [ ] Line-height differs between headings and body text.
6. [ ] No text uses Tailwind's default `text-gray-*` colors.
7. [ ] Heading hierarchy is clear (H1 > H2 > H3 visually distinct without relying on size alone).

### Color (5 items)

8. [ ] Zero instances of `bg-gray-*`, `bg-zinc-*`, `bg-slate-*` in this component.
9. [ ] Accent color is used intentionally (1-2 focal points per screen, not everywhere).
10. [ ] Text contrast meets WCAG AA (4.5:1 for body, 3:1 for large text).
11. [ ] Surface colors create visible elevation hierarchy (3+ distinct levels).
12. [ ] Interactive elements have distinct hover/focus/active states using the token palette.

### Layout (5 items)

13. [ ] Spacing is non-uniform (at least 3 different gap/padding values on this screen).
14. [ ] Content has visual grouping (related items closer together, sections separated).
15. [ ] The layout is NOT a centered column of uniform-width cards.
16. [ ] Mobile and desktop layouts differ meaningfully (not just reflowed).
17. [ ] Negative space is intentional (some areas have generous whitespace, some are compact).

### Interaction (4 items)

18. [ ] Buttons have labels specific to their action (not generic "Submit" / "Cancel").
19. [ ] At least one micro-interaction exists (hover effect, transition, subtle animation).
20. [ ] Loading states are contextual (skeleton matching content shape, not a centered spinner).
21. [ ] Empty states have personality (helpful message, suggested action -- not just "No data").

### Voice (3 items)

22. [ ] No user-facing text says "AI", "model", "generate", or "prompt" (unless that IS the product).
23. [ ] Error messages are specific and actionable ("Task title is required" not "Validation error").
24. [ ] Placeholder text is realistic (not "Lorem ipsum" or "Enter text here").

### Screenshot Verification (3 items)

25. [ ] Side-by-side with a competitor: this page is visually distinguishable.
26. [ ] Cover the logo: could this page belong to any app, or is the brand evident?
27. [ ] View at both mobile (375px) and desktop (1280px): nothing clips, overflows, or collapses.

---

## Section 4: Verification Steps

After completing the checklist:

1. Count PASS vs FAIL items.
2. If any item in Typography, Color, or Layout fails, the component is NOT ready to ship. Fix before proceeding.
3. If any item in Interaction or Voice fails, fix if possible; document in your agent memory if deferred.
4. Screenshot Verification items require visual confirmation -- use Playwright or a browser screenshot tool at 375px and
   1280px viewports.
5. Record the checklist results in your agent memory.

**Minimum passing score:** 22/27 (all Typography, Color, and Layout items must pass;
up to 5 items in Interaction/Voice/Screenshot may be deferred with justification).

---

## [CUSTOMIZE]

Replace Section 2 entirely with your project's design system. Section 1 (antipatterns)
and Section 3 (checklist) are universal -- keep them as-is and add project-specific items
if needed. Section 4 can be adjusted to match your verification tooling.
