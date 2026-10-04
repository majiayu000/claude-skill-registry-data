---
name: frontend-design
description: Create or improve frontend interfaces with high design quality. Use when asked to build, style, improve, or refactor web components, pages, dashboards, or applications — in any framework (React, Next.js, Vue, HTML/CSS). Triggers for greenfield UI creation and for improving existing components within a design system. Use even when the request doesn't say "design" but involves any visual output.
---

# Frontend Design

Produce production-grade frontend interfaces with exceptional attention to visual quality — whether creating from scratch or working within an existing design system.

## First: Detect the Context

Before writing a single line, determine which mode applies:

**Existing design system** — signs include: `tailwind.config.*`, a `components/ui/` directory, CSS custom properties for color/spacing, shadcn/ui or another component library, consistent token usage across files.
→ Use **Design System Mode**

**Greenfield** — no established components, no design tokens, starting fresh, or the user explicitly wants something new with no constraints.
→ Use **Creative Mode**

When unsure, check the codebase. A wrong aesthetic direction creates rework; 30 seconds of reading saves that.

---

## Design System Mode

Your job here is enhancement, not reinvention. The visual language is already decided — your value is executing within it with precision and filling the gaps the design system hasn't addressed yet.

### How to approach it

Read before writing. Understand:
- What tokens exist: color variables, spacing scale, type scale
- What component patterns are already established: how buttons, cards, inputs are styled
- What states are missing: hover, focus, empty, loading, error
- Where the current implementation diverges from its own stated system (inconsistencies are your primary target)

Then work within those constraints — use the project's tokens, match existing className patterns, respect the component architecture. Enhancement lives in execution quality, not in redirecting the aesthetic.

### What you're solving

- **Missing states**: interactive elements without hover/focus/disabled, data screens with no empty state, forms with no error styling
- **Inconsistencies**: same logical component styled differently across files, padding values that almost match, icons sized differently per file
- **Hierarchy gaps**: multiple elements competing for the same visual weight, primary actions not visually distinct from secondary
- **Density problems**: screens that feel cramped or, conversely, underuse the space they have
- **Motion gaps**: state changes that are instant when a transition would feel intentional

### What you're not doing

- Introducing new typefaces or color values without a clear reason tied to the existing system
- Overriding design system tokens with one-off values
- Making things "look different" for the sake of variety

If a genuine system-level gap exists (a missing token, an undefined component), propose it explicitly before using it: "There's no `text-caption` token — I'd recommend adding one at 0.75rem/1rem line-height. Should I proceed?"

### Supplementary tool

For comprehensive design system generation or when you need detailed typography/color/style recommendations: use the `ui-ux-pro-max` skill with `--stack shadcn` (or the relevant stack) and `--design-system` flag. It can generate a `design-system/MASTER.md` that persists across sessions.

---

## Creative Mode (Greenfield)

Full latitude. No existing system to honor.

### Design thinking

Before coding, commit to a direction:

- **Purpose**: What problem does this interface solve? Who uses it, in what context?
- **Tone**: Pick a lane and go deep — brutally minimal, maximalist, retro-futuristic, organic/natural, luxury/refined, editorial/magazine, brutalist/raw, art deco, soft/pastel, industrial. Use these as starting points, not end states.
- **Differentiation**: What makes this memorable? Identify the one thing someone will still recognize in a screenshot five years from now.

Choose a clear direction and execute it with precision. Bold maximalism and quiet minimalism both work — what fails is indecision.

### Implementation

Produce working code (HTML/CSS/JS, React, Vue, Svelte, etc.) that is:
- Production-grade and fully functional
- Visually distinctive — it should be identifiable, not interchangeable
- Internally cohesive — every element references the same aesthetic logic
- Refined in the details — spacing, rhythm, state transitions, the things most people skip

### Aesthetics

- **Typography**: Choose fonts with character. Avoid Inter, Roboto, Arial, and system fonts for creative work — they flatten everything. Pair a distinctive display font with a complementary body font. Vary your choices — no two designs should share a font stack.
- **Color**: Commit to a palette. Dominant colors with sharp accents outperform timid, evenly-distributed schemes. Use CSS variables for consistency. Aim for a palette someone could name ("the moss-and-rust one") not just describe ("it has some green").
- **Motion**: Focus on high-impact moments — one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions. Use CSS-only where possible; use Motion (Framer Motion) for React when available. Hover states should surprise, not just confirm.
- **Spatial composition**: Try asymmetry, overlap, diagonal flow, grid-breaking elements. Generous negative space or controlled density — but never the comfortable middle.
- **Atmosphere**: Solid color backgrounds are the default; they shouldn't be the choice. Gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, grain overlays — use what fits the direction.

Match implementation complexity to the vision. Maximalist designs need elaborate code. Minimalist designs need restraint, precision, and ruthless attention to spacing — elegance is not the absence of complexity, it's complexity resolved.

Never converge on predictable combinations (Space Grotesk + purple gradient is the new Comic Sans). Each design should be a deliberate choice, not a familiar default.
