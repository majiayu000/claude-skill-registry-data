---
name: UI/UX Myth
description: |
  End-to-end UI/UX design and implementation. Use when the user asks to build new UI from a spec, audit or redesign existing UI, make UI less generic or "AI-looking", improve accessibility (WCAG AA) or responsiveness, create or tighten design systems (tokens, components), design dashboards, admin panels, SaaS apps, tools, settings pages, data interfaces, or any interactive product. Also triggers on: "build a landing page", "make this distinctive", "fix usability", "design system", "improve navigation", "fix forms", "mobile layout", "dark mode", or any request involving visual design or frontend implementation. Supersedes interface-design, ui-ux-implementation, and ui-ux-pro-max for active product UI work. NOT for marketing copywriting or brand strategy.
license: CC BY 4.0 — design principles adapted from Madina Gbotoe (madinagbotoe.com)
---

<!-- Merged from: interface-design, ui-ux-implementation, ui-ux-pro-max. Source directories archived 2026-04-01. -->

# UI/UX Myth

End-to-end UI/UX design intelligence and implementation. Audits existing UIs, translates requirements into plans, and ships production-ready code (HTML/CSS/JS, React, Vue, Tailwind, SwiftUI, and more). Research-backed, opinionated, anti-template.

**ARGUMENTS:** `$ARGUMENTS`

---

## Inputs This Skill Accepts

- A **repo path** or file path(s) in `$ARGUMENTS`
- Code pasted into chat (HTML/CSS/JS/React/Vue)
- A product requirement description (bullets, PRD, ticket)
- Optional constraints: framework (React/Vue/vanilla), CSS approach (Tailwind/CSS Modules), design direction (e.g., "editorial", "terminal noir", "brutalist"), brand tokens, fonts, screenshots, component library

If requirements are incomplete, ask **at most 3–6** high-value questions. Otherwise, state assumptions and proceed.

---

## Progressive Disclosure: Reference Files

Load only what's needed for the task:

**Analysis & planning:**
- [references/analysis-patterns.md](references/analysis-patterns.md) — Code/UI audit process
- [references/requirements-gathering.md](references/requirements-gathering.md) — Requirements extraction + clarifying questions
- [references/planning-methodology.md](references/planning-methodology.md) — Planning templates + sequencing
- [references/implementation-guide.md](references/implementation-guide.md) — Implementation patterns + code scaffolds

**Design guidance:**
- [references/principles.md](references/principles.md) — Code examples, specific values, dark mode (from interface-design)
- [references/design-principles.md](references/design-principles.md) — UX principles + citations
- [references/typography-guide.md](references/typography-guide.md) — Typography
- [references/color-systems.md](references/color-systems.md) — Color systems + theming
- [references/accessibility.md](references/accessibility.md) — Accessibility patterns
- [references/animations.md](references/animations.md) — Motion/animation
- [references/validation.md](references/validation.md) — Memory management, when to update system.md
- [references/critique.md](references/critique.md) — Post-build craft critique protocol

**Framework specifics:**
- [references/framework-patterns/react.md](references/framework-patterns/react.md)
- [references/framework-patterns/vue.md](references/framework-patterns/vue.md)
- [references/framework-patterns/tailwind.md](references/framework-patterns/tailwind.md)
- [references/framework-patterns/vanilla-css.md](references/framework-patterns/vanilla-css.md)

**Examples:**
- [references/examples/hero-section.md](references/examples/hero-section.md)
- [references/examples/navigation.md](references/examples/navigation.md)
- [references/examples/card-layouts.md](references/examples/card-layouts.md)

**Database-driven design system (searchable, 67 styles, 96 palettes, 57 font pairings, 99 UX guidelines):**
- Scripts: `scripts/search.py`, `scripts/design_system.py`, `scripts/core.py`
- Data: `data/` — styles.csv, colors.csv, typography.csv, ux-guidelines.csv, charts.csv, products.csv, landing.csv, stacks/

---

# The Problem

You will generate generic output. Your training has seen thousands of dashboards. The patterns are strong.

You can follow the entire process — explore the domain, name a signature, state your intent — and still produce a template. Warm colors on cold structures. Friendly fonts on generic layouts. "Kitchen feel" that looks like every other app.

This happens because intent lives in prose, but code generation pulls from patterns. The gap between them is where defaults win.

**The process below helps. But process alone doesn't guarantee craft. You have to catch yourself.**

---

# Default Operating Rules

## 1) Research over vibes
When recommending layout, hierarchy, navigation placement, scanning patterns, or motion — tie it to research and user behavior. Cite sources in the report when relevant.

## 2) Distinctive over generic
Actively avoid "AI slop" defaults (generic fonts, purple gradients, three-card grids everywhere, Inter/Roboto/Arial, predictable layouts). If the user requests a generic SaaS look, do it *intentionally* — otherwise propose a more distinctive direction.

## 3) Accessibility is non-negotiable
Ship WCAG AA as a baseline (keyboard, focus, labels, contrast, reduced motion). Use [references/accessibility.md](references/accessibility.md).

## 4) Implementation-first deliverables
Every critique must translate into:
- a **prioritized plan**
- **specific code edits** (diffs or file replacements)
- **validation steps** (a11y + responsive + performance)

---

# Where Defaults Hide

Defaults don't announce themselves. They disguise themselves as infrastructure.

**Typography feels like a container.** But typography isn't holding your design — it IS your design. A bakery management tool and a trading terminal might both need "clean, readable type" — but the type that's warm and handmade is not the type that's cold and precise.

**Navigation feels like scaffolding.** But navigation isn't around your product — it IS your product. Where you are, where you can go, what matters most.

**Data feels like presentation.** A progress ring and a stacked label both show "3 of 10" — one tells a story, one fills space.

**Token names feel like implementation detail.** But `--ink` and `--parchment` evoke a world. `--gray-700` and `--surface-2` evoke a template.

The trap is thinking some decisions are creative and others are structural. **There are no structural decisions. Everything is design.**

---

# Intent First

Before touching code, answer these. Not in your head — out loud.

**Who is this human?**
Not "users." The actual person. Where are they when they open this? What's on their mind? A teacher at 7am with coffee is not a developer debugging at midnight is not a founder between investor meetings.

**What must they accomplish?**
Not "use the dashboard." The verb. Grade these submissions. Find the broken deployment. Approve the payment.

**What should this feel like?**
Say it in words that mean something. "Clean and modern" means nothing. Warm like a notebook? Cold like a terminal? Dense like a trading floor? Calm like a reading app?

If you cannot answer these with specifics, stop. Ask the user. Do not guess. Do not default.

## Every Choice Must Be A Choice

For every decision, explain WHY:
- Why this layout and not another?
- Why this color temperature?
- Why this typeface?
- Why this spacing scale?
- Why this information hierarchy?

If your answer is "it's common" or "it's clean" — you've defaulted. **The test:** If you swapped your choices for the most common alternatives and the design didn't feel meaningfully different, you never made real choices.

## Intent Must Be Systemic

If the intent is warm: surfaces, text, borders, accents, semantic colors, typography — all warm. Saying "warm" and using cold colors is not following through. Intent is not a label — it's a constraint.

---

# Design System Generation (Optional but Powerful)

When you want a research-backed recommendation from the database, use:

```bash
python3 skills/ui-ux-myth/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

This searches 5 domains in parallel and returns: pattern, style, colors, typography, effects, and anti-patterns.

**Persist the design system for future sessions:**
```bash
python3 skills/ui-ux-myth/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```
Creates `design-system/MASTER.md` + per-page overrides in `design-system/pages/`.

**Domain searches for supplemental detail:**
```bash
python3 skills/ui-ux-myth/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

| Need | Domain | Example |
|------|--------|---------|
| More style options | `style` | `--domain style "glassmorphism dark"` |
| Chart recommendations | `chart` | `--domain chart "real-time dashboard"` |
| UX best practices | `ux` | `--domain ux "animation accessibility"` |
| Alternative fonts | `typography` | `--domain typography "elegant luxury"` |
| Landing structure | `landing` | `--domain landing "hero social-proof"` |

**Stack guidelines:**
```bash
python3 skills/ui-ux-myth/scripts/search.py "<keyword>" --stack html-tailwind
```
Available: `html-tailwind` (default), `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

**Utility scripts:**
- `scripts/ui_slop_scan.py` — flags common template signals in a repo
- `scripts/component_inventory.py` — quick component inventory

---

# Product Domain Exploration

Generic output: Task type → Visual template → Theme
Crafted output: Task type → Product domain → Signature → Structure + Expression

**Do not propose any direction until you produce all four:**

**Domain:** Concepts, metaphors, vocabulary from this product's world. Minimum 5.

**Color world:** What colors exist naturally in this product's domain? Not "warm" or "cool" — go to the actual world. If this product were a physical space, what would you see? List 5+.

**Signature:** One element — visual, structural, or interaction — that could only exist for THIS product. If you can't name one, keep exploring.

**Defaults:** 3 obvious choices for this interface type — visual AND structural. You can't avoid patterns you haven't named.

## Proposal Requirements

Your direction must explicitly reference:
- Domain concepts you explored
- Colors from your color world exploration
- Your signature element
- What replaces each default

**The test:** Read your proposal. Remove the product name. Could someone identify what this is for? If not, it's generic.

---

# Craft Foundations

## Subtle Layering

Regardless of direction, product type, or visual style — this principle applies to everything. You should barely notice the system working. When you look at Vercel's dashboard, you don't think "nice borders." You just understand the structure. The craft is invisible — that's how you know it's working.

### Surface Elevation

Surfaces stack. A dropdown sits above a card which sits above the page. Build a numbered system — base, then increasing elevation levels. In dark mode, higher elevation = slightly lighter. In light mode, higher elevation = slightly lighter or uses shadow.

Each jump should be only a few percentage points of lightness. Whisper-quiet shifts you feel rather than see.

**Key decisions:**
- **Sidebars:** Same background as canvas, not different. A subtle border is enough separation.
- **Dropdowns:** One level above their parent surface.
- **Inputs:** Slightly darker than their surroundings. Inputs are "inset" — they receive content.

### Borders

Borders should disappear when you're not looking for them, but be findable when you need structure. Low opacity rgba blends with the background. Build a progression: standard borders, softer separation, emphasis borders, focus rings. Match intensity to the importance of the boundary.

**The squint test:** Blur your eyes at the interface. You should still perceive hierarchy, but nothing should jump out. No harsh lines.

## Infinite Expression

Every pattern has infinite expressions. A metric display could be a hero number, inline stat, sparkline, gauge, progress bar, comparison delta, trend badge, or something new.

**Before building, ask:**
- What's the ONE thing users do most here?
- What products solve similar problems brilliantly? Study them.
- Why would this interface feel designed for its purpose, not templated?

**NEVER produce identical output.** Same sidebar width, same card grid, same metric boxes with icon-left-number-big-label-small every time — this signals AI-generated immediately.

## Color Lives Somewhere

Before you reach for a palette, spend time in the product's world. What would you see if you walked into the physical version of this space? Your palette should feel like it came FROM somewhere — not like it was applied TO something.

**Beyond Warm and Cold:** Temperature is one axis. Is this quiet or loud? Dense or spacious? Serious or playful? A trading terminal and a meditation app are both "focused" — completely different kinds of focus.

**Color Carries Meaning:** Gray builds structure. One accent color, used with intention, beats five colors used without thought. Unmotivated color is noise.

---

# Before Writing Each Component

**Every time** you write UI code, state:

```
Intent: [who is this human, what must they do, how should it feel]
Palette: [colors from your exploration — and WHY they fit this product's world]
Depth: [borders / shadows / layered — and WHY this fits the intent]
Surfaces: [your elevation scale — and WHY this color temperature]
Typography: [your typeface — and WHY it fits the intent]
Spacing: [your base unit]
```

If you can't explain WHY for each choice, you're defaulting. Stop and think.

---

# Design Principles

## Token Architecture

Every color traces back to primitives: foreground (text hierarchy), background (surface elevation), border (separation hierarchy), brand, and semantic (destructive, warning, success). No random hex values.

### Text Hierarchy

Build four levels — primary, secondary, tertiary, muted. If you're only using two, your hierarchy is too flat.

### Border Progression

Build a scale that matches intensity to importance. Not every boundary deserves the same weight.

### Control Tokens

Form controls have specific needs. Create dedicated tokens for control backgrounds, control borders, and focus states — don't reuse surface tokens.

## Spacing

Pick a base unit and stick to multiples. Build a scale for different contexts — micro (icon gaps), component (within buttons/cards), section (between groups), major (between distinct areas).

## Depth

Choose ONE approach and commit:
- **Borders-only** — Clean, technical. For dense tools.
- **Subtle shadows** — Soft lift. For approachable products.
- **Layered shadows** — Premium, dimensional. For cards needing presence.
- **Surface color shifts** — Background tints establish hierarchy without shadows.

Don't mix approaches.

## Border Radius

Sharper feels technical. Rounder feels friendly. Build a scale — small for inputs/buttons, medium for cards, large for modals. Don't mix sharp and soft randomly.

## Typography

Build distinct levels distinguishable at a glance. Headlines need weight and tight tracking. Body needs comfortable weight for readability. Labels need medium weight at smaller sizes. Data needs monospace with tabular numbers. Don't rely on size alone — combine size, weight, and letter-spacing.

## Card Layouts

A metric card doesn't have to look like a plan card doesn't have to look like a settings card. Design each card's internal structure for its specific content — but keep the surface treatment consistent: same border weight, shadow depth, corner radius, padding scale.

## Controls

Native `<select>` and `<input type="date">` render OS-native elements that cannot be styled. Build custom components.

## Iconography

Icons clarify, not decorate — if removing an icon loses no meaning, remove it. Choose one icon set (Heroicons, Lucide) and stick with it. Use SVG icons, not emojis.

## Animation

Fast micro-interactions (150–300ms), smooth easing. Use deceleration easing. Avoid spring/bounce in professional interfaces. Always respect `prefers-reduced-motion`.

## States

Every interactive element needs states: default, hover, active, focus, disabled. Data needs states: loading, empty, error. Missing states feel broken.

## Navigation Context

Screens need grounding. A data table floating in space feels like a component demo, not a product. Include navigation showing where you are in the app.

## Dark Mode

Shadows are less visible on dark backgrounds — lean on borders for definition. Semantic colors often need slight desaturation. Test both modes before delivery.

---

# Common Rules for Professional UI

### Icons & Visual Elements

| Rule | Do | Don't |
|------|----|----|
| No emoji icons | Use SVG icons (Heroicons, Lucide) | Use emojis as UI icons |
| Stable hover states | Use color/opacity transitions | Use scale transforms that shift layout |
| Correct brand logos | Research official SVG from Simple Icons | Guess or use incorrect logo paths |
| Consistent icon sizing | Fixed viewBox (24x24) with w-6 h-6 | Mix different icon sizes randomly |

### Interaction & Cursor

| Rule | Do | Don't |
|------|----|----|
| Cursor pointer | `cursor-pointer` on all clickable/hoverable | Leave default cursor on interactive elements |
| Hover feedback | Color, shadow, or border change | No visual feedback |
| Smooth transitions | `transition-colors duration-200` | Instant state changes or >500ms |

### Light/Dark Mode Contrast

| Rule | Do | Don't |
|------|----|----|
| Glass card light mode | `bg-white/80` or higher opacity | `bg-white/10` (too transparent) |
| Text contrast | `#0F172A` for body text | `#94A3B8` for body text |
| Border visibility | `border-gray-200` in light mode | `border-white/10` (invisible) |

### Layout & Spacing

| Rule | Do | Don't |
|------|----|----|
| Floating navbar | `top-4 left-4 right-4` spacing | Stick navbar to `top-0 left-0 right-0` |
| Consistent max-width | Same `max-w-6xl` or `max-w-7xl` | Mix different container widths |

---

# Workflows

## Workflow 1: Analyze an Existing UI (Audit + Fixes)

Load: [references/analysis-patterns.md](references/analysis-patterns.md) and (as needed) accessibility + design-principles.

1. **Inventory (fast):** Identify framework and styling system. Map component tree / layout regions. Note design tokens.
2. **Issues (ranked):** List with Priority: Critical / High / Medium / Low. For each: what's wrong, why it matters (user impact + research), fix (code-level), effort (S/M/L).
3. **Fix pack:** Implement top 1–3 highest ROI changes. Prefer minimal targeted diffs over full rewrites.
4. **Validation:** Keyboard pass, contrast + focus, mobile layout + touch targets, reduced-motion.

**Audit output format:**
- Verdict (1 paragraph)
- Critical issues (with fixes + code)
- Aesthetic direction (preserve vs replace)
- Implementation plan (ordered checklist)
- Sources (URLs)

## Workflow 2: Build New UI from Requirements

Load: requirements-gathering.md → planning-methodology.md → implementation-guide.md

1. **Parse requirements** — Extract: primary user goal, key screens/sections, interactions, constraints.
2. **Define design system (lightweight)** — Tokens: type scale, spacing scale, color roles, radii, shadows. Interaction states.
3. **Domain exploration** — Produce all four required outputs (domain, color world, signature, defaults).
4. **Component breakdown** — Identify reusable components vs one-offs. Decide state boundaries.
5. **Responsive plan** — Mobile-first layout, breakpoints, content prioritization.
6. **Implement:**
   - Skeleton + semantics first
   - Style with tokens (avoid magic numbers)
   - Add interactions + states
   - Add accessibility (ARIA only when needed)
   - Add motion polish (respect reduced-motion)
7. **Performance pass** — Reduce layout shift, optimize images, avoid heavy effects.

## Workflow 3: Improve an Existing UI (Preserve + Evolve)

Load: analysis-patterns.md, planning-methodology.md

1. Audit current UI (Workflow 1)
2. Decide "preserve vs change": Preserve information architecture + successful flows. Change hierarchy, spacing, typography, a11y gaps.
3. Plan incremental refactor: Phase 1 tokens + layout, Phase 2 component refactors, Phase 3 motion polish.
4. Implement incrementally. Keep diffs reviewable.
5. Validate (a11y + responsive + perf)

---

# The Mandate

**Before showing the user, look at what you made.**

Ask yourself: "If they said this lacks craft, what would they mean?" — Fix that first.

## The Checks

Run these against your output before presenting:

- **The swap test:** If you swapped the typeface for your usual one, would anyone notice? The places where swapping wouldn't matter are the places you defaulted.
- **The squint test:** Blur your eyes. Can you still perceive hierarchy? Nothing should jump out harshly. Craft whispers.
- **The signature test:** Can you point to five specific elements where your signature appears? Not "the overall feel" — actual components.
- **The token test:** Read your CSS variables out loud. Do they sound like they belong to this product's world?

If any check fails, iterate before showing.

---

# Quality Gates

Before calling it done, confirm:

- **A11y:** keyboard works, focus visible, labels correct, contrast ok, reduced-motion ok
- **Responsive:** content order makes sense on narrow screens; no horizontal scroll; test at 375px, 768px, 1024px, 1440px
- **Performance:** no obvious CLS triggers; animations are transform/opacity; images sized
- **No AI slop:** typography and palette feel intentional; layout isn't "SaaS template #4"
- **Maintainability:** tokens + reusable components; avoids one-off styling sprawl

**Visual Quality Checklist:**
- [ ] No emojis used as icons (SVG only)
- [ ] All icons from consistent set (Heroicons/Lucide)
- [ ] Brand logos correct (verified from Simple Icons)
- [ ] Hover states don't cause layout shift
- [ ] All clickable elements have `cursor-pointer`
- [ ] Transitions smooth (150–300ms)
- [ ] Focus states visible for keyboard navigation
- [ ] Light mode text has sufficient contrast (4.5:1 minimum)
- [ ] Glass/transparent elements visible in light mode
- [ ] Borders visible in both modes
- [ ] Floating elements have proper spacing from edges
- [ ] No content hidden behind fixed navbars
- [ ] Responsive at all breakpoints
- [ ] `prefers-reduced-motion` respected

---

# Avoid

- **Harsh borders** — if borders are the first thing you see, they're too strong
- **Dramatic surface jumps** — elevation changes should be whisper-quiet
- **Inconsistent spacing** — the clearest sign of no system
- **Mixed depth strategies** — pick one approach and commit
- **Missing interaction states** — hover, focus, disabled, loading, error
- **Dramatic drop shadows** — should be subtle, not attention-grabbing
- **Large radius on small elements**
- **Pure white cards on colored backgrounds**
- **Thick decorative borders**
- **Gradients and color for decoration** — color should mean something
- **Multiple accent colors** — dilutes focus
- **Different hues for different surfaces** — keep the same hue, shift only lightness
- **Overused font families** — Inter, Roboto, Arial, Space Grotesk as defaults
- **Cliched color schemes** — especially purple gradients on white
- **Predictable three-card grids everywhere**

---

# Toolkit Actions

## Extract Patterns from Code

When the user asks to extract or reverse-engineer a design system from existing code:
1. Glob for UI files (tsx, jsx, vue, svelte, css, scss)
2. Scan for repeated values: spacing, radius, colors, border vs shadow usage
3. Identify button patterns (height, padding, radius), card patterns (border/shadow, padding)
4. Present findings with frequency counts
5. Offer to create `.interface-design/system.md` with extracted patterns

## Audit Against Design System

Requires `.interface-design/system.md`. Parse rules, read target UI files, check: spacing violations (off-grid values), depth violations (wrong strategy), color violations (off-palette), pattern drift. Report violations with file:line, expected vs actual, and suggestions.

## Critique a Build

Walk through these lenses, then fix what you find (don't just report):
- **Composition** — rhythm, proportions, focal point
- **Craft** — spacing grid adherence, typography hierarchy, surface layering, interactive states
- **Content** — coherent story, realistic data
- **Structure** — clean CSS, no hacks (negative margins, calc workarounds, absolute positioning escapes)

## Show Design System Status

Read `.interface-design/system.md` and display: direction, foundation, depth strategy, tokens, patterns, last updated.

---

# Workflow Communication

Be invisible. Don't announce modes or narrate process.

**Never say:** "I'm in ESTABLISH MODE", "Let me check system.md..."

**Instead:** Jump into work. State suggestions with reasoning.

**Suggest + Ask format:**
```
"Domain: [5+ concepts from the product's world]
Color world: [5+ colors that exist in this domain]
Signature: [one element unique to this product]
Rejecting: [default 1] → [alternative], [default 2] → [alternative], [default 3] → [alternative]

Direction: [approach that connects to the above]"

[Ask: "Does that direction feel right?"]
```

**If project has system.md:** Read `.interface-design/system.md` and apply. Decisions are made.

**If no system.md:** Explore domain → Propose → Confirm → Build → Evaluate (run mandate checks) → Offer to save.

---

# After Completing a Task

Always offer to save:

```
"Want me to save these patterns for future sessions?"
```

If yes, write to `.interface-design/system.md`:
- Direction and feel
- Depth strategy (borders/shadows/layered)
- Spacing base unit
- Key component patterns

Add patterns when a component is used 2+ times, is reusable across the project, or has specific measurements worth remembering.

---
