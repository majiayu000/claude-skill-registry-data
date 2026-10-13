---
name: ui-system
description: Define the design system foundations for a UI project — color tokens (semantic and literal), spacing scale, typography scale, elevation, border-radius, and layout rules — so every downstream component spec and code generation references the same vocabulary instead of guessing values. Use this skill at the start of any new frontend project, when the user references "design tokens", "design system", "theme", or "style guide", or when component specs are blocked because the token names they reference don't yet exist. Also use it whenever Claude has been generating components with inconsistent colors or padding values across a project — that's a sign the system layer is missing.
status: stable
---

# UI System

Defines the foundational vocabulary — tokens — that every downstream component and code skill draws from. Without this, every new component is a fresh guess at colors and spacing, which is the root cause of drift across a project.

## When to use this skill

Use this skill when:
- A new frontend project is starting and no design system exists.
- Component specs reference tokens (e.g. `border-default`, `space-4`) that don't yet have values.
- Generated UI shows inconsistent colors or paddings across the project — indicates no shared system.
- The user asks to define a "theme", "style guide", "design tokens", or "design system".

Do **not** use this skill when:
- A design system already exists. Reference it; don't recreate it. If the user has a Figma library or a tokens file, ingest it instead.
- The project is single-component and one-off — system overhead isn't worth it. A short token list at the top of the component spec is enough.

## Core principle

**Tokens are a vocabulary, not a mood board.** Every token has two layers — the literal (what value it resolves to) and the semantic (what it means). Components should never reference literals directly; they reference semantics. This makes theme changes (light/dark, brand updates) trivial and prevents the model from picking arbitrary hex values mid-component.

## Pre-flight check

Before drafting, confirm:

1. **Brand or vibe direction.** Has `ui-brief` or `ui-blueprint` established a visual direction? If not, ask: "What's the overall feel — playful and rounded, serious and dense, neutral and quiet, expressive and brand-led?" Refuse vague answers like "modern" — translate to concrete properties.
2. **Existing brand assets.** Does the user have a logo, primary color, font, or existing brand book? If yes, ingest those as constraints — do not propose conflicting choices.
3. **Theme requirements.** Light only, dark only, or both? Affects how semantic tokens are structured.
4. **Density preference.** Dense (B2B data tools) or sparse (consumer apps)? Affects spacing scale base unit and typography scale.

If any is missing, ask. Do not pick defaults silently.

## The two-layer token rule

Always produce tokens in two layers:

**Literal layer** — raw values, named after what they are.
- `blue-500: #4F46E5`
- `gray-900: #111827`
- `space-1: 4px`

**Semantic layer** — meanings, named after what they do. They reference literals.
- `color.action.primary: blue-500`
- `color.text.body: gray-900`
- `space.gutter.tight: space-1`

Components reference **only** semantic tokens. The literal layer is the only place a hex value or pixel value appears.

This rule is non-negotiable because it's the only way to make theme switches and brand updates not require a full rewrite.

## Workflow

### Step 1 — Establish the spacing base unit

This is the most important early decision. Pick a base unit from {2px, 4px, 8px}. Most modern systems use 4px. Dense data UIs sometimes use 2px. Larger consumer apps sometimes use 8px.

Then build a scale: 0.5x, 1x, 1.5x, 2x, 3x, 4x, 6x, 8x, 12x, 16x, 24x of the base. Not every step is required, but the scale must be mathematically consistent.

### Step 2 — Establish the type scale

Pick:
- **Font family / families** — sans (default), serif, mono (for code).
- **Base size** — typically 14, 15, or 16px.
- **Scale ratio** — 1.125 (subtle), 1.2 (moderate), 1.25 (clear), 1.333 (strong). Pick one and stick to it.
- **Weights used** — typically 400 (regular), 500 (medium), 600 (semibold), 700 (bold). Don't use more than 3–4.
- **Line heights** — typically 1.25 for headings, 1.5 for body.

### Step 3 — Establish color literals

Build a palette:
- **Neutral / gray scale** — 50, 100, 200, 300, 400, 500, 600, 700, 800, 900 (10 steps, perceptually evenly spaced).
- **Brand color** — same 50–900 scale.
- **Status colors** — success, warning, danger, info — each with at least 100, 500, 700.

Use OKLCH or HSL if the user knows what those are; otherwise hex is fine. Never invent specific hex values without either user input or a stated reasoning ("blue-500 is #3B82F6, mid-saturation blue chosen to match user's reference product X").

### Step 4 — Map semantic colors

Define semantic roles:
- `color.text.body`, `color.text.muted`, `color.text.inverse`, `color.text.disabled`
- `color.surface.1` (page bg), `color.surface.2` (card bg), `color.surface.3` (overlay)
- `color.border.default`, `color.border.strong`, `color.border.muted`
- `color.action.primary`, `color.action.primary-hover`, `color.action.primary-active`
- `color.action.danger`, `color.action.danger-hover`
- `color.feedback.success`, `color.feedback.error`, `color.feedback.warning`, `color.feedback.info`
- `color.focus-ring`

If light + dark theme: map semantics for both modes.

### Step 5 — Border radius scale

Pick 3–5 named radii:
- `radius.none: 0`
- `radius.sm: 4px`
- `radius.md: 8px`
- `radius.lg: 12px`
- `radius.full: 9999px` (for pills, avatars)

Don't add more than 5.

### Step 6 — Elevation / shadow scale

3 levels typical: `elevation.1`, `elevation.2`, `elevation.3`. Each with a defined box-shadow value. If the visual direction is "flat", explicitly set elevations to `none` and document the choice.

### Step 7 — Layout rules

- **Container max-widths** — typically 640px (narrow / reading), 1024px (medium), 1280px (wide), 1440px (full).
- **Grid** — column count and gutter at each breakpoint.
- **Breakpoints** — typically 640, 768, 1024, 1280px. Pick a set and stick to it.

### Step 8 — Confirm with the user

Show the user the system. Ask: "Anything that feels wrong? Any token name you'd change?" Iterate before declaring done.

## Output template

```markdown
---
spec_type: system
spec_id: <project-slug>-system
based_on: brief-<slug> (or none if standalone)
created: <YYYY-MM-DD>
status: draft
themes: [light]  # or [light, dark]
---

# Design system: <project name>

## 1. Visual direction (recap)
- **Mood:** <2–3 concrete adjectives from blueprint>
- **Density:** <dense | medium | sparse>
- **Reference products:** <named>

## 2. Spacing

**Base unit:** 4px

| Token | Value | Usage |
|---|---|---|
| `space.0` | 0 | none |
| `space.1` | 4px | tightest gaps, inline icons |
| `space.2` | 8px | tight gaps |
| `space.3` | 12px | small gaps |
| `space.4` | 16px | default gap |
| `space.6` | 24px | section spacing |
| `space.8` | 32px | large section spacing |
| `space.12` | 48px | major divisions |
| `space.16` | 64px | between major page regions |

## 3. Typography

**Family:** Inter, system-ui, sans-serif (body) · ui-monospace (code)

**Scale ratio:** 1.25

| Token | Size | Line height | Weight | Usage |
|---|---|---|---|---|
| `type.display` | 36px | 1.2 | 700 | hero / page title |
| `type.h1` | 28px | 1.25 | 700 | page title |
| `type.h2` | 22px | 1.3 | 600 | section title |
| `type.h3` | 18px | 1.35 | 600 | subsection |
| `type.body` | 15px | 1.5 | 400 | default text |
| `type.body-strong` | 15px | 1.5 | 600 | emphasized body |
| `type.small` | 13px | 1.45 | 400 | captions, helper text |
| `type.code` | 14px | 1.5 | 400 (mono) | inline code, snippets |

## 4. Color — literals

(In light theme. Dark theme literals listed in section 5 if applicable.)

| Family | 50 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 |
|---|---|---|---|---|---|---|---|---|---|---|
| gray | #F9FAFB | #F3F4F6 | #E5E7EB | #D1D5DB | #9CA3AF | #6B7280 | #4B5563 | #374151 | #1F2937 | #111827 |
| blue (brand) | ... | ... | ... | ... | ... | #4F46E5 | ... | ... | ... | ... |
| green | ... | ... | ... | ... | ... | #10B981 | ... | ... | ... | ... |
| red | ... | ... | ... | ... | ... | #EF4444 | ... | ... | ... | ... |
| amber | ... | ... | ... | ... | ... | #F59E0B | ... | ... | ... | ... |

## 5. Color — semantics

| Token | Light theme | Dark theme | Usage |
|---|---|---|---|
| `color.text.body` | gray-900 | gray-50 | default text |
| `color.text.muted` | gray-600 | gray-400 | secondary text, captions |
| `color.text.disabled` | gray-400 | gray-600 | disabled states |
| `color.text.inverse` | white | gray-900 | text on inverse surfaces |
| `color.surface.1` | white | gray-900 | page background |
| `color.surface.2` | gray-50 | gray-800 | card / panel background |
| `color.surface.3` | white | gray-700 | overlay / popover background |
| `color.border.default` | gray-200 | gray-700 | default borders |
| `color.border.strong` | gray-400 | gray-500 | hover or emphasized borders |
| `color.border.muted` | gray-100 | gray-800 | dividers |
| `color.action.primary` | blue-500 | blue-400 | primary buttons, links |
| `color.action.primary-hover` | blue-600 | blue-300 | hover state |
| `color.action.primary-active` | blue-700 | blue-200 | pressed state |
| `color.action.danger` | red-500 | red-400 | destructive actions |
| `color.feedback.success` | green-500 | green-400 | success messages, valid states |
| `color.feedback.error` | red-500 | red-400 | error messages, invalid states |
| `color.feedback.warning` | amber-500 | amber-400 | warnings |
| `color.feedback.info` | blue-500 | blue-400 | informational |
| `color.focus-ring` | blue-500 (50% alpha) | blue-400 (50% alpha) | keyboard focus indicator |

## 6. Border radius

| Token | Value | Usage |
|---|---|---|
| `radius.none` | 0 | sharp corners (data tables, dense UI) |
| `radius.sm` | 4px | inputs, small buttons |
| `radius.md` | 8px | cards, larger buttons |
| `radius.lg` | 12px | modals, large surfaces |
| `radius.full` | 9999px | pills, avatars |

## 7. Elevation / shadow

| Token | Value | Usage |
|---|---|---|
| `elevation.0` | none | flat surfaces |
| `elevation.1` | `0 1px 2px rgba(0,0,0,0.05)` | cards at rest |
| `elevation.2` | `0 4px 8px rgba(0,0,0,0.08)` | hover, popovers |
| `elevation.3` | `0 12px 24px rgba(0,0,0,0.12)` | modals, dropdowns |

## 8. Motion

| Token | Value | Usage |
|---|---|---|
| `motion.fast` | 100ms ease-out | hover transitions |
| `motion.medium` | 200ms ease-out | toggles, expansions |
| `motion.slow` | 300ms ease-in-out | page transitions, modals |

(If user requests reduced motion, all of these collapse to 0.)

## 9. Breakpoints

| Token | Value | Usage |
|---|---|---|
| `bp.sm` | 640px | small tablets |
| `bp.md` | 768px | tablets |
| `bp.lg` | 1024px | small laptops |
| `bp.xl` | 1280px | desktops |
| `bp.2xl` | 1536px | wide desktops |

## 10. Layout

- **Default container max-width:** 1280px
- **Reading container max-width:** 720px (for prose)
- **Grid columns at lg+:** 12 columns, 24px gutter
- **Grid columns at md:** 8 columns, 16px gutter
- **Grid columns at sm and below:** 4 columns, 16px gutter

## 11. Open questions
- <Numbered>

## 12. Assumptions made
- ⚠️ <flagged>
```

## Rules that prevent hallucinated decisions

1. **No literal values in components.** Components reference semantic tokens only. The semantic→literal map lives here.
2. **No invented brand colors.** If the user has a brand color, use it. If they don't, propose 2–3 candidates and ask them to pick — do not silently choose.
3. **Mathematically consistent spacing.** Spacing scale must follow a clear rule (multiples of base unit). No ad-hoc values like 13px or 22px.
4. **Type scale must use a ratio, not arbitrary numbers.** Pick a ratio (1.125, 1.2, 1.25, 1.333) and stick to it.
5. **Don't sneak in tokens that aren't used.** Every token in the system should have at least one referenced use case in a downstream component spec. If a token is purely speculative, mark it `// proposed, not yet used` and consider deleting.
6. **Light + dark must be specified together if both are needed.** Don't define light first and "we'll do dark later" — that always produces a broken dark theme. Either commit to dark now or defer it as an explicit non-goal.

## Acceptance criteria for this skill's output

A design system spec produced by this skill is acceptable only if every one of these is true:

- [ ] Spacing scale has a stated base unit and is mathematically consistent.
- [ ] Type scale uses a stated ratio (not arbitrary sizes).
- [ ] Color literals include neutrals, brand, and status colors.
- [ ] Color semantics are defined as a separate layer that references literals.
- [ ] If both light and dark themes are required, both are specified in the same table.
- [ ] Border-radius scale has at most 5 named values.
- [ ] Elevation scale is defined (or explicitly set to `none` if flat).
- [ ] Breakpoints are listed with values and a stated use case for each.
- [ ] Every token name uses dot-notation (`group.role.modifier`) consistently.
- [ ] No literal hex / px / ms value appears outside the literals section.
- [ ] Open questions section has at least one entry, or assumptions section has at least one entry — if both are empty, the system was not interrogated hard enough.

If any check fails, revise before delivering.
