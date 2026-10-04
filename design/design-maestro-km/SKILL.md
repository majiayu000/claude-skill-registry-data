---
name: design-maestro_KM
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when building web components, pages, artifacts, dashboards, landing pages, games, simulations, or any web UI. Produces creative, polished code that avoids generic AI aesthetics. Includes intent-first design philosophy, anti-slop detection, product domain exploration, curated typography, visual themes for simulations, animation recipes, advanced CSS/WebGL effects, UI pattern library, data visualization patterns, dark mode guide, self-critique protocol, designer-grade polish details, and accessibility enforcement. Triggers on any frontend design, styling, or UI/UX task.
---
<!-- Supersedes frontend-design (archived 2026-04-01). -->

# Design Maestro

> Frontend design skill that produces distinctive, production-grade web interfaces. Anti-template, anti-AI-slop. Every output should look like it was built by a senior designer-developer, not generated.

---

## Design Calibration

Default output targets: **DESIGN_VARIANCE 8 · MOTION_INTENSITY 6 · VISUAL_DENSITY 4**

| Axis | 1–3 (low) | 4–6 (mid) | 7–10 (high) |
|---|---|---|---|
| **DESIGN_VARIANCE** | Conventional layout, standard patterns, familiar structure | Intentional asymmetry, varied card sizes, one signature element | Bold layout choices, distinctive structure, multiple signature elements |
| **MOTION_INTENSITY** | CSS hover/active states only, no JS animation | CSS transitions, stagger reveals, subtle scroll effects | Spring physics, Framer Motion, GSAP, perpetual micro-animations |
| **VISUAL_DENSITY** | Gallery mode — massive spacing, large type, minimal chrome | Balanced — breathing room with purposeful grouping | Cockpit mode — tight spacing, monospace data, 1px separators, compressed type |

Override by describing what you want. Map user language to axes and load relevant references:
- "more airy" / "minimal" → low VISUAL_DENSITY → load `references/design-foundations.md` (spacing)
- "no animations" / "still" → MOTION_INTENSITY 0 → skip motion references
- "more playful" / "animated" → high MOTION_INTENSITY → load `references/motion-library.md`
- "dense data" / "dashboard" → high VISUAL_DENSITY → load `references/patterns-and-recipes.md`

---

## Always-On Rules

1. **No AI slop.** Catch and replace: three-card centered rows → Bento grid with varied spans. Purple/blue gradient on white → domain-derived palette. Inter/Roboto as sole typeface → deliberate pairing from `references/themes.md`. Uniform spacing → rhythmic variation. Cookie-cutter SaaS layout → structure derived from the product's information hierarchy. See `references/aesthetic-principles.md` for the full checklist.
2. **Asymmetry by default.** Vary card sizes, spacing, column spans — visual rhythm over visual uniformity. Exception: comparison views, data grids, pricing tables, and other contexts where symmetry communicates equivalence.
3. **Typography is design.** Every project gets a deliberate font pairing that reflects its personality. See `references/themes.md` for curated pairings.
4. **Motion with purpose.** Every animation needs a reason — stagger reveals, spring physics, scroll-triggered transitions. Include `prefers-reduced-motion` support on all motion.
5. **Dark mode done right.** Elevated surfaces get lighter, not darker. Reduce saturation. Shadows become glows. Base on `#0a0a0a`, not `#000000`.
6. **Accessibility is non-negotiable.** WCAG AA contrast, focus indicators, keyboard nav, touch targets ≥44px, ARIA labels, reduced-motion fallbacks.
7. **Performance-conscious.** Animate only `transform` and `opacity`. Lazy load below-fold. `font-display: swap`. CSS containment where applicable.

---

## Complexity Matching

Match implementation depth to request scope. A single-use demo gets sensible defaults and clean code — it doesn't need a full token system, custom animation library, or exhaustive domain exploration. A production dashboard gets the full treatment. Read the request and calibrate accordingly.

---

## Multi-Turn Behavior

On iteration turns, verify changes align with the established design direction. Re-run the self-critique squint test silently. Flag conflicts with earlier design decisions rather than silently overriding them.

---

## Feedback Loop

**Read `FEEDBACK.md` when loading this skill.** It captures observed issues and successful patterns.

**During use:**
1. **Detect** — notice when output quality drops or a pattern doesn't land
2. **Search** — check if the issue is already logged in FEEDBACK.md
3. **Scope** — identify which category and reference file is relevant
4. **Draft-and-ask** — propose a FEEDBACK.md entry and ask the user before writing
5. **Write-on-approval** — add the entry only when confirmed
6. **Compact-at-75** — when FEEDBACK.md approaches 75 entries, merge older entries into condensed summaries

---

## Design Foundations

For from-scratch builds and full redesigns, load `references/design-foundations.md` — contains token architecture, designer-grade polish details, surface quality targets, and craft principles.

For pattern vocabulary (dock magnification, bento grid, parallax tilt, etc.), load `references/creative-arsenal.md`.

---

## Reference Loading

### Always load (every design task)

1. `FEEDBACK.md` — observed issues and successful patterns from prior use
2. `references/aesthetic-principles.md` — anti-slop checklist, color generation, visual hierarchy

### Load by task type

| Task Type | Load These References |
|---|---|
| **New project from scratch** | `references/design-foundations.md` + `references/design-philosophy.md` + `references/from-scratch.md` + `references/themes.md` |
| **Full design process** (domain exploration, checkpoints, self-critique) | `references/design-philosophy.md` |
| **Editing existing project** | `references/existing-project.md` |
| **Need UI patterns** (heroes, navs, cards, forms, dashboards) | `references/patterns-and-recipes.md` |
| **Need visual effects** (CSS atmosphere, WebGL, shaders) | `references/advanced-effects.md` |
| **Need animations** (which animation, choreography, aesthetic decisions) | `references/motion-library.md` |
| **Need animation implementation** (tool selection, GSAP/FM/WAAPI code, failure modes) | Load **ui-motion-wiki** skill |
| **Need AI/chat UI** (streaming, citations, tool use, agents) | `references/ai-ui-patterns.md` |
| **Need data visualizations** | `references/patterns-and-recipes.md` (data viz section) |
| **Need fonts/theming** | `references/themes.md` |
| **Need a complete visual theme** (merged theme library plus extraction workflow) | `design-extraction/` |
| **Iterating on a design** | `references/design-iteration.md` |
| **Received vague/conflicting feedback** | `references/design-feedback.md` |
| **Design review** (formal visual QA) | `references/design-review.md` |
| **CSS/layout debugging** | `references/design-debugging.md` |
| **Animated dashboard, Bento 2.0, perpetual motion** | `references/deep/motion-performance.md` |
| **Need pattern vocabulary** | `references/creative-arsenal.md` |

### Deep References

The `references/deep/` folder contains ~15K lines of full implementation code. These files are **never auto-loaded.** Compressed references contain section pointers (grep commands for Claude Code, offset/limit for claude.ai).

---

## Output Principles

- **Artifacts:** Single-file HTML or JSX. React + Tailwind preferred. All CSS/JS inline.
- **Code files:** Create in `/home/claude`, copy final to `/mnt/user-data/outputs/`.
- **Font loading:** Always use Google Fonts `<link>` in HTML or `@import` in CSS. Never assume fonts are available.
- **CDN imports:** Three.js r128 from cdnjs. D3 from cdnjs. No npm imports in artifacts.
- **Color format:** Prefer `oklch()` or `hsl()` over hex for better perceptual uniformity.
