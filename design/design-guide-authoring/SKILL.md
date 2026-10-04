---
name: design-guide-authoring
description:
  Create or update a design guide or design system specification, usually DESIGN.md, for web or mobile interfaces. Use
  when asked to document visual direction, design tokens, typography, component patterns, or interaction guidelines for
  developers and agents. Ground the guide in the project's existing design and stack. For auditing components against
  the system or documenting a single component, use design-system when available.
---

# Design Guide Generator

This skill produces a single markdown document — usually `DESIGN.md` at the project root or under `docs/` — that serves
as the source of truth for a project's visual and interaction design.

The audience for that document is dual:

- **Humans** designing, reviewing, or onboarding onto the product.
- **LLMs and developers** who need a reference when generating new components, pages, or screens.

A useful design guide is opinionated. It expresses a creative point of view (a "theme" or "north star"), explains _why_
the rules exist, and gives concrete primitives — colors, typography, spacing, component patterns — that someone (or some
model) can apply without ambiguity. Generic, hedging guides get ignored. Specific, confident guides shape the product.

## Inputs

The user may pass natural-language context. Read whatever they give and extract these fields:

| Field                           | Examples                                                            | Notes                                                                                                                                                                                                              |
| ------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `framework`                     | React, Next.js, Vue, Svelte, SwiftUI, Flutter, vanilla JS           | The component / app framework                                                                                                                                                                                      |
| `styling`                       | Tailwind, vanilla CSS, CSS Modules, styled-components, SCSS, StyleX | How styles are authored                                                                                                                                                                                            |
| `ui_library`                    | shadcn/ui, Base UI, Radix, MUI, Chakra, Mantine, HeadlessUI         | Headless or full component lib. Some newer shadcn-style projects use Base UI primitives; many existing shadcn/ui projects still use Radix. Detect the actual imports before naming the primitive layer in the doc. |
| `primary_color` / `brand_color` | `#006a61`, "deep teal", "indigo 600"                                | Hex preferred, names accepted                                                                                                                                                                                      |
| `theme_name`                    | "The Architectural Flow", "Quiet Confidence"                        | Memorable, opinionated, optional                                                                                                                                                                                   |
| `product_name`                  | "Formbricks", "Acme Mail"                                           | The product the guide is for                                                                                                                                                                                       |
| `tone` / `personality`          | "premium and editorial", "playful and bold"                         | Optional creative direction                                                                                                                                                                                        |
| `platform`                      | web, mobile, desktop, dashboard                                     | Affects which components to cover                                                                                                                                                                                  |

If the user supplies nothing, infer from the project (Step 1). **Do not invent values to fill empty slots.** A design
guide gets baked into a codebase — overconfident assumptions are worse than gentle generalities. When a slot is unknown,
either omit it from the metadata block or speak generically in that section.

## Step 1 — Gather context

If the user supplied arguments, parse them first. Then, **when filesystem / project access is available**, inspect the
current working directory to fill any gaps:

1. **Tech detection**
   - `package.json` dependencies → React/Vue/Svelte/Next/Remix/Astro, Tailwind, shadcn/ui, Base UI
     (`@base-ui-components/react`), Radix (`@radix-ui/*`), MUI, etc.
   - Tailwind: `tailwind.config.{js,ts}` indicates v3-style config; a `@import "tailwindcss";` line plus an `@theme`
     block in a global CSS file (and no config file) indicates v4. The version matters — see the Tailwind callout in
     authoring guidance.
   - `tsconfig.json`, `vite.config.*`, `next.config.*`, `nuxt.config.*`, `astro.config.*` → confirms framework.
   - `components.json` at root → shadcn/ui is installed. Check whether its components import from
     `@base-ui-components/react` (current) or `@radix-ui/react-*` (older); the doc should reference whichever the
     project actually uses.
   - `Gemfile`, `pubspec.yaml`, `Package.swift`, `*.xcodeproj`, `build.gradle` → non-JS stacks
     (Rails/Flutter/Swift/Android).
2. **Color & token detection**
   - CSS custom properties (`--primary`, `--brand`, `--accent`, `--background`) in `globals.css`, `app.css`, or similar.
   - Tailwind theme colors / `extend.colors` in the config.
   - `theme.ts`, `tokens.ts`, `design-tokens.json`.
3. **Existing components**
   - Use `rg --files` or shallow directory listings for `components/`, `src/components/`, `app/`, `pages/`, and `views/`
     to see what UI primitives already exist.
   - Open only representative files needed to identify conventions; do not bulk-read entire component trees.
   - This lets you write a Components section that reflects reality instead of a generic checklist.
4. **Existing design notes**
   - Look for `DESIGN.md`, `STYLEGUIDE.md`, `docs/design.md`, `BRAND.md`. If present, extend rather than overwrite — and
     ask the user before discarding anything substantive.
5. **No project signal (or no filesystem access)**
   - If the directory is empty, missing manifests, unrelated, or simply unreachable, tell the user what you found (or
     that you couldn't inspect anything) and offer to (a) write a generic, framework-agnostic guide, or (b) wait for
     more context. Don't fabricate a stack.

## Step 2 — Pick a creative direction

The opening of the guide is the most important part. A guide with a clear _creative north star_ gives the team something
to rally around and gives an LLM a vibe to optimize for. Without one, the guide reads like a compliance document.

- If the user gave a `theme_name` or tone, use it.
- If the user wants a single-shot deliverable ("just write it", "generate the doc", "in one pass"), pick the strongest
  direction from the available context, write the doc, and clearly state the assumption when you deliver. Don't make
  them pick first.
- Otherwise — when there's room for collaboration — propose 2–3 directions based on what you know about the product and
  let the user pick before you write the full document. Evocative theme names imply a metaphor; pick from clusters that
  fit the product type:
  - **Premium / serious** — _The Architectural Flow_ (precision, clinical, IDE-like) · _Quiet Confidence_ (minimalist,
    trust-forward) · _Atrium_ (open, airy, generous spacing) · _Periodical_ (editorial, typographic, longform)
  - **Utility / dense** — _Signal_ (high-contrast, data-dense) · _Toolbox_ (utility-first, robust, enterprise-internal)
    · _Workshop_ (warm, tactile, hand-built)
  - **Playful / expressive** — _Carnival_ (kinetic, color-forward, consumer) · _Saturday_ (relaxed, optimistic,
    lifestyle) · _Notebook_ (friendly, drafted, lightly imperfect)
- If you genuinely don't have enough signal — and the user hasn't given any direction — leave the theme line out and
  write the rest of the guide in a neutral, professional voice rather than inventing a fake personality.

The metaphor, once chosen, is what every subsequent rule should enforce. Surface rules, type rules, component rules —
they all serve the metaphor.

## Step 3 — Write the document

Use `assets/template.md` as the structural skeleton. Use `assets/example.md` as a reference for _energy and voice_ only
— see the "signature moves" bullet in authoring guidance below for what not to copy.

### Required sections, in order

1. **Title + metadata block** (see below)
2. **Overview & Creative North Star** — the theme, the metaphor, what the design is _not_
3. **Colors & Surface Philosophy** — palette, surface roles, rules about borders / backgrounds / contrast
4. **Typography** — typeface choices, hierarchy, what the type system _says_
5. **Iconography** — icon style, source, sizes, stroke, color rules. Locks in the icon system so new components don't
   drift.
6. **Elevation & Depth** — shadows, layering, how things "lift"
7. **Components** — concrete patterns for the components that matter for this product
8. **Accessibility & UX Quality Bar** — keyboard, focus, contrast, touch, motion. The non-negotiables an LLM will guess
   wrong without a reference.
9. **Implementation Notes for LLMs** — short, addressed directly to the model that will read this doc when generating
   new UI
10. **Do's and Don'ts** — short, scannable, opinionated summary
11. **Director's Closing Note** — one paragraph restating the philosophy

Required sections can be lightly trimmed for tiny projects, but never removed entirely without telling the user.

### Optional sections — include only when warranted

Not every product needs every section. Adding empty or speculative versions of these is worse than omitting them.

- **Dark Mode** — include only when the project actually ships dark mode, the user explicitly asks for it, or the
  codebase has dark-mode infrastructure (`prefers-color-scheme` rules, dual CSS variable sets, a theme toggle component,
  `class="dark"` patterns). For products that ship dark _only_ (developer tools, code editors, some media apps), write
  the Colors & Surface Philosophy section in dark first and skip a separate section. For products that support both, add
  a "Dark Mode" subsection inside Colors & Surface Philosophy describing the parallel palette and the inversion rules.
  Do not add a "future considerations" stub for dark mode.

- **Motion** — a dedicated Motion section is for products where motion is part of the brand: consumer apps with
  delightful micro-interactions, themes that explicitly call for kinetic energy ("Carnival", "Saturday"), or codebases
  that already pull in `framer-motion`, `gsap`, or Lottie. For utility apps, B2B tools, dashboards, admin UIs, and most
  serious products, do _not_ add a Motion section — the single "respect `prefers-reduced-motion`" line in the
  Accessibility section is sufficient. When you do include Motion (place it after Elevation & Depth), cover: easing
  curves, duration scale, what triggers animation, and the _purpose_ of motion (feedback, continuity, expression).

- **Brand Voice & Illustration** — include when the product has illustration, mascots, or a distinctive editorial voice.
  Skip for utility tools and standard SaaS chrome.

- **Internationalization Notes** — include when the product ships in multiple locales, supports RTL, or has CJK font
  requirements. Skip otherwise.

If you're unsure whether to include an optional section, ask the user briefly before drafting, or skip it.

### The metadata block

Place this right under the title, before the Overview, as a short bullet list (same shape as `assets/example.md` and
`assets/template.md`). **Omit any line you don't have a confident value for** — do not write "TBD" everywhere, do not
invent.

```markdown
- **Theme:** The Architectural Flow
- **Product:** Formbricks
- **Framework:** React + Next.js
- **Styling:** Tailwind CSS
- **UI library:** shadcn/ui (Base UI primitives)
- **Primary color:** `#006a61` (deep teal)
- **Supported color schemes:** light, dark
- **Platform:** Web (desktop-first, responsive, mobile-friendly)
```

If, say, you don't know the UI library and the user didn't mention one, drop that line entirely.

### Authoring guidance

- **Be opinionated.** "Borders are a design failure" is more useful than "consider whether borders are needed." A design
  guide exists to make decisions so the team doesn't have to relitigate them on every PR.
- **Explain the why.** Every rule should hint at the reasoning ("we reject 1px borders because they fragment the surface
  and make B2B tools feel like spreadsheets"). LLMs and humans both follow rules better when they understand the intent.
- **Use concrete tokens.** Hex codes, rem values, exact radii, exact spacing scales. Vague guides get ignored.
- **Tie rules to the framework when you know it.**
  - **Tailwind v4** (CSS-based config via `@theme`, no `tailwind.config.js`, no PostCSS required, `@tailwindcss/vite`
    for Vite): reference tokens as CSS custom properties (`var(--color-primary)`) and class names (`bg-primary`,
    `rounded-xl`). Don't tell the team to maintain a `tailwind.config.js` if they aren't using one.
  - **Tailwind v3**: reference theme keys defined in `tailwind.config.{js,ts}`.
  - **shadcn/ui**: reference component names _and_ whichever primitive layer the project actually imports. Some newer
    shadcn-style projects use Base UI; many existing ones still use Radix. Detect from imports — they have different
    APIs and the doc should match reality.
  - **Plain CSS / CSS Modules**: use CSS custom properties (`var(--surface-1)`).
  - **Stack unknown**: describe rules in plain English and leave token names abstract.
- **Pivot the Components section to the product type.** Lead with the components this product actually has. Use the
  matching starter list as a _prompt_, not a checklist — adapt to what's real:
  - **App / dashboard / admin / SaaS:** cards, buttons, forms (inputs, selects, toggles, validation), navigation
    (sidebar, top bar, tabs), tables, dialogs / sheets, empty / loading states, toasts.
  - **Marketing site:** hero, primary CTA, social-proof strip, feature blocks, pricing table, testimonials, FAQ, footer,
    blog post template.
  - **E-commerce:** product card, product detail page, image gallery, cart, checkout flow, search & filter, reviews,
    recommendations.
  - **Content / publication:** article header, body type rules (drop cap, pull quote, sidebar), TOC, image captions,
    related-articles strip.
  - **Data viz / analytics:** KPI tile, chart container, axis & legend rules, color scales (sequential / diverging /
    categorical), table density, empty / loading / error states for charts.
  - **Mobile-first SPA / native app:** tab bar, sheet, list row, action sheet, swipe gestures, safe-area handling, touch
    states. Avoid an encyclopedic checklist of every component that has ever existed — generic checklists are the reason
    design guides get ignored.
- **Don't import the example's signature moves.** The reference example's specific rules — the "no-borders" stance, the
  "Glass & Gradient" treatment, the `surface-container-*` token names — belong to one product. Pick _new_ signature
  moves that fit this product. Reuse the example's _energy_, not its rules.
- **Length.** Aim for 200–500 lines of markdown. Long enough to be useful, short enough that an LLM will load and
  respect the whole thing.

## Step 4 — Deliver

The default deliverable is a saved file. Inline output is also valid when the user clearly wants it pasted into chat.

- **File** (default, and always when the user says "save", "create the doc", "add to the project"): write `DESIGN.md` at
  the project root, or `docs/DESIGN.md` if a `docs/` directory exists. With no connected project folder, save to the
  outputs directory and share the link.
- **Inline** (when the user says "show me", "paste it here", "give me a draft"): return the document as a single fenced
  markdown block, no commentary above it.

After saving (or pasting), briefly tell the user (a) what you assumed (theme, framework, color, library version), and
(b) where they should push back if anything is wrong. Don't recap the whole document — they can read it.

## Notes on style

- Match the _energy_ of `assets/example.md` — confident, specific, willing to make aesthetic claims. A design guide that
  hedges every sentence is useless. (For _what not to copy_, see the "signature moves" bullet in authoring guidance
  above.)
- If the user asks for "just the basics" or "keep it short", you may shrink each section, but keep the structure
  recognizable. Don't drop the Accessibility or Implementation Notes sections — they are the parts most useful to future
  LLMs.
- If the user asks to update an existing design guide, read it first and preserve any decisions that already feel
  deliberate. Don't overwrite a coherent point of view just because you'd have written it differently.

## Quality checklist (before saving)

Before handing back the doc, verify:

- Metadata reflects only known facts. Unknown fields are omitted, not stubbed with "TBD".
- The doc has a clear creative point of view (theme + metaphor) — or, if there genuinely wasn't enough signal, a neutral
  voice that doesn't invent a fake personality.
- Rules cite the project's actual stack (specific Tailwind version, the right primitive layer for shadcn,
  framework-correct token names) when known, and stay abstract when not.
- The example's signature rules ("no borders", "Glass & Gradient", `surface-container-*`) are not copied unless the user
  asked for that aesthetic.
- The Components section reflects what this product actually has, not a generic checklist.
- Accessibility & UX Quality Bar and Implementation Notes for LLMs sections are present and concrete.
- The Director's Closing Note ends with a sentence the team would actually quote in a PR review.

## Reference files

- `assets/template.md` — skeleton with the canonical section order and placeholder prompts.
- `assets/example.md` — a full, real-feeling design guide. Read it before drafting, to calibrate tone.
