---
name: design-engineering
description: >
  Premium design engineering skill for agentic workflows — produces high-end, distinctive
  UI designs using DESIGN.md as the portable contract across Pencil MCP (in-IDE canvas),
  Figma MCP (team handoff + design tokens), and Google Stitch (vibe exploration + AI generation).
  Enforces anti-generic principles, WCAG 2.2 AA accessibility, perceptually uniform color,
  tiered animation timing, and screenshot-driven visual validation at every stage.
  Use when: (1) creating or reviewing UI designs from an agent, (2) generating DESIGN.md for
  a project, (3) implementing designs from Pencil .pen files or Figma URLs, (4) enforcing
  visual quality standards on AI-generated interfaces, (5) setting up a multi-tool design
  pipeline, (6) converting between design tools and production code.
  Triggers on: 'design engineering', 'design system', 'DESIGN.md', 'premium design',
  'high-end UI', 'pencil design', 'figma to code', 'stitch design', 'vibe design',
  'visual design review', 'glass design', 'design tokens', 'UI quality'.
version: 1.0.0
category: design
tags:
  - design-engineering
  - design-system
  - pencil
  - figma
  - stitch
  - design-md
  - glass-morphism
  - accessibility
  - visual-validation
  - design-tokens
dependencies:
  - arcan-glass
---

# Design Engineering

Premium design engineering for agentic workflows. Produce distinctive, high-end interfaces — not generic AI output — using DESIGN.md as the portable design contract across three complementary tools.

```
DESIGN.md (contract) ─────────────────────────────────────────────────
    │                         │                        │
    ▼                         ▼                        ▼
  Stitch                   Pencil                    Figma
  (explore)              (design in IDE)         (refine + handoff)
    │                         │                        │
    └─────────────────────────┴────────────────────────┘
                              │
                              ▼
                    Production Code
                 (validated via screenshots)
```

## Quick Start

### 1. Create or Load DESIGN.md

Every project needs a DESIGN.md at its root. Generate one from an existing project:

```bash
# From existing code (read globals.css, extract tokens)
# Agent analyzes CSS → generates DESIGN.md in Stitch spec format

# From a reference website (via Stitch)
# Use stitch-design skill → extract_design_context → synthesize DESIGN.md

# From a Figma file
# Use Figma MCP → get_variable_defs + get_design_context → synthesize DESIGN.md
```

### 2. Design Pipeline

| Stage | Tool | Action |
|-------|------|--------|
| **Explore** | Stitch | Vibe-design multiple directions from a goal/feeling/inspiration |
| **Design** | Pencil MCP | Create .pen files in IDE — batch_design, get_style_guide, set_variables |
| **Refine** | Figma MCP | Team review, design token management, Code Connect mapping |
| **Build** | Coding Agent | Generate production code referencing DESIGN.md tokens |
| **Validate** | Screenshots | get_screenshot (Pencil), visual diff, layout inspection |

### 3. Validate Design Quality

After every major design step, run the **Premium Design Checklist**:

- [ ] No generic AI aesthetic (purple gradients on white, stock photos, identical cards)
- [ ] Consistent atmospheric hue across all neutral surfaces (never pure gray)
- [ ] Maximum 2-3 saturated brand colors + semantic states
- [ ] Custom typography (not Inter/Roboto/Arial defaults)
- [ ] Glass/material metaphor with deliberate restraint (3-5 glass surfaces per viewport)
- [ ] Tiered animation timing (150ms hover → 250ms transition → 500ms morph → 1500ms ambient)
- [ ] WCAG 2.2 AA: 4.5:1 text contrast, visible focus indicators, 24x24px touch targets
- [ ] Reduced motion: `prefers-reduced-motion` disables all animation
- [ ] Mobile-first: 16px min font on inputs, responsive breakpoints tested

## The DESIGN.md Specification

DESIGN.md is a **portable, agent-friendly markdown file** following Google Stitch's five-section format. It captures a project's visual identity in terms readable by both humans and AI agents.

### Required Sections

| # | Section | Content |
|---|---------|---------|
| 1 | **Visual Theme & Atmosphere** | Evocative mood descriptors, density, aesthetic philosophy |
| 2 | **Color Palette & Roles** | Descriptive Name + color value + functional purpose for every color |
| 3 | **Typography Rules** | Font families, weight/size hierarchy, rendering settings |
| 4 | **Component Stylings** | Buttons, cards, navigation, inputs — shape, color, behavior, states |
| 5 | **Layout Principles** | Spacing system, grid, whitespace, responsive behavior, animation |
| 6 | **Generation Notes** (optional) | Prompt templates, iteration constraints, tool-specific guidance |

### Writing Rules

- **Evocative names**: "Resonant AI Blue" not "blue"; "Abyssal Indigo" not "dark background"
- **Precise values in parens**: `oklch(0.55 0.25 260)` / `#0066ff` after every descriptive name
- **Functional purpose**: Every color/component explains *what it's used for*
- **Physical descriptions**: "Pill-shaped" not `rounded-full`; "Whisper-soft shadows" not `shadow-sm`
- **Never raw CSS class names**: Translate all technical values into design language

### How Agents Use DESIGN.md

1. **Read DESIGN.md** at the start of every design or frontend task
2. **Apply tokens** — use the exact color values, font stacks, spacing units, and animation timings
3. **Follow component patterns** — buttons, cards, inputs should match the described styling
4. **Validate against it** — every generated component should pass a visual audit against the spec
5. **Update it** — when the design system evolves, keep DESIGN.md current

## Multi-Tool Pipeline

### Pencil MCP (Design in IDE)

Agent-native vector design on an infinite canvas. `.pen` files are JSON, live in Git, and are read/written via MCP tools.

**Core workflow:**
1. `get_editor_state()` — understand current context
2. `get_guidelines("web-app")` — load design rules for your project type
3. `get_style_guide_tags` → `get_style_guide(tags)` — choose aesthetic direction
4. `set_variables(...)` — set design tokens from DESIGN.md
5. `find_empty_space_on_canvas(...)` — locate placement for new frames
6. `batch_design(operations)` — create/modify design (max 25 ops per call)
7. `get_screenshot(nodeId)` — validate visually after every major step
8. `snapshot_layout()` — verify computed positions, detect clipping/overflow

**Design-to-code:** Agent reads .pen tree via `batch_get`, extracts layout/styling, generates React + Tailwind components referencing DESIGN.md tokens.

**Key rules:**
- Always take screenshots after major design steps
- Keep batch_design to max 25 operations per call
- Use realistic content, never "Lorem ipsum"
- Name layers semantically ("UserAvatarImage" not "Rectangle 12")
- Desktop-first at 1440px unless mobile-first specified
- Mark reusable patterns with `reusable: true`

### Figma MCP (Refine + Handoff)

Industry-standard design tool with official MCP server for agent integration.

**Setup:**
```bash
# Official Figma MCP (hosted, OAuth)
claude mcp add --transport http figma https://mcp.figma.com/mcp

# Framelink (community, most popular, 90% payload compression)
claude mcp add figma-framelink -- npx figma-developer-mcp --figma-api-key=YOUR_KEY
```

**Core workflow:**
1. `get_design_context(url)` — extract layout/styling for a frame (React + Tailwind default)
2. `get_variable_defs(url)` — read design tokens (colors, spacing, typography)
3. `get_code_connect_map(url)` — map Figma components → codebase components
4. `get_screenshot(url)` — visual snapshot for fidelity validation
5. `create_design_system_rules(url)` — generate agent-readable rules file

**Design tokens pipeline:**
```
Figma Variables → REST API / plugin → DTCG JSON → Style Dictionary → CSS / iOS / Android
```

### Google Stitch (Vibe Exploration)

AI-native design platform for rapid UI exploration from natural language.

**Setup:**
```bash
# Install skills (already done globally)
npx skills add google-labs-code/stitch-skills --yes --global

# MCP server
npx @_davideast/stitch-mcp init
# or set STITCH_API_KEY and configure manually
```

**Core workflow:**
1. Describe a *goal*, *feeling*, or *inspiration* — not a wireframe
2. Stitch generates multiple high-fidelity UI directions
3. Extract design DNA via `extract_design_context`
4. Synthesize into DESIGN.md via the `design-md` skill
5. Export to Figma (with Auto Layout) or download HTML/CSS

**DESIGN.md generation pipeline (5 stages):**
Retrieval → Extraction → Translation → Synthesis → Alignment

## Premium Design Principles

### What Makes Design Look Premium

1. **Deliberate restraint** — every element earns its place; nothing is there by default
2. **Material metaphor** — surfaces feel like glass, paper, stone, or metal — not flat rectangles
3. **Atmospheric hue** — never pure gray; always a subtle color tint in neutrals (e.g., 275-hue blue-purple)
4. **Micro-detail precision** — kerning, line spacing ratios, shadow angles, border opacities all consciously chosen
5. **Custom typography** — distinctive font pairing that immediately separates from generic defaults
6. **Interaction choreography** — tiered animation timing creates rhythm and hierarchy
7. **Light simulation** — top-edge gradient highlights on glass surfaces simulate physical light
8. **Dominant + accent** — one strong brand color with sharp accents, never evenly distributed

### What Makes Design Look Generic AI (Avoid These)

| Anti-Pattern | Fix |
|---|---|
| Purple gradients on white | Commit to one atmospheric hue throughout |
| Inter/Roboto/Arial defaults | Use distinctive font pairing (e.g., CalSans + Geist) |
| 3-column identical card grids | Vary card treatment, use asymmetry, break the grid |
| Even color distribution | Dominant/accent hierarchy with 2-3 saturated colors max |
| Stock team photos | AI-generated contextual imagery or abstract patterns |
| Identical component treatment | Vary emphasis with glass tiers, shadow depth, border weight |
| Over-detailed maximalism | One effect per surface, not stacked gradients + shadows + blur |
| Missing atmospheric coherence | Shared hue undertone + consistent token usage across all components |

### Color System Principles

- Define all colors in **OKLCH** (perceptually uniform lightness)
- Provide **hex fallbacks** via `@supports not (color: oklch())`
- Enhance brand colors on **P3 displays** via `@media (color-gamut: p3)`
- Limit saturated colors to **2-3 brand + 4 semantic** (success, warning, error, info)
- Maintain a **consistent hue undertone** across all neutral surfaces

### Typography Principles

- Pair a **confident display face** (headings) with a **precise body face**
- Establish explicit **weight hierarchy**: Display (SemiBold), Body (Regular), UI Labels (Medium)
- Set `text-rendering: optimizeLegibility`, antialiased smoothing
- Use `text-wrap: balance` for headlines
- Minimum **16px font on mobile inputs** to prevent iOS Safari zoom

## Accessibility Enforcement (WCAG 2.2 AA)

These are **non-negotiable** in every design:

### Color Contrast
- Normal text: **4.5:1** minimum contrast ratio
- Large text (18pt+ or 14pt+ bold): **3:1** minimum
- UI components and graphics: **3:1** minimum

### Focus Indicators
- Visible focus on all interactive elements (2px solid outline, 2px offset)
- **3:1** contrast between focused and unfocused states
- Never trap or hide focus

### Keyboard & Navigation
- All functionality available via keyboard
- Logical tab order
- Skip navigation links on content-heavy pages

### Touch Targets
- Minimum **24x24 CSS pixels** (WCAG 2.2 AA)
- Recommended **44x44px** (Apple HIG) / **48x48dp** (Material)

### Motion
- Comprehensive `prefers-reduced-motion` support
- Collapse all animation to `0.01ms` duration
- Disable hover transforms in reduced motion mode

### Semantic HTML
- `aria-invalid` for error identification
- `required` / `aria-required` for required fields
- ARIA live regions for status messages

## Visual Validation Workflow

### After Every Major Design Step:

1. **Screenshot** — use Pencil `get_screenshot` or browser screenshot tools
2. **Layout inspection** — use Pencil `snapshot_layout(problemsOnly: true)` to detect clipping/overflow
3. **Token audit** — use `search_all_unique_properties` to find raw hex values that should be tokenized
4. **Contrast check** — verify all text/background combinations meet WCAG ratios
5. **Responsive test** — validate at 375px (mobile), 768px (tablet), 1440px (desktop)
6. **Dark/light mode** — verify both themes maintain contrast and readability

### Design Token Audit

```
search_all_unique_properties → find leaked raw values
replace_all_matching_properties → tokenize to variable references
get_variables → verify all tokens are defined
```

## Animation System

### Timing Tiers

| Tier | Duration | Easing | Use Case |
|------|----------|--------|----------|
| **Instant** | 0ms | — | Reduced motion fallback |
| **Fast** | 150ms | ease | Button hover, link color, focus ring |
| **Normal** | 250ms | ease | Card lift, border change, surface shift |
| **Slow** | 350ms | ease | Panel expand, content reveal |
| **Morph** | 500ms | cubic-bezier(0.4, 0, 0.2, 1) | Shape/size transformation |
| **Ambient** | 1500ms | ease-in-out | Pulsing glow, loading state |

### Rules

- Every animation must serve **navigation, feedback, or attention** — no decorative-only motion
- Use **CSS transitions** for standard elements; Motion library for React orchestration
- Never animate `width`, `height`, `top`, `left` — use `transform` and `opacity` only
- Use `will-change` sparingly and remove after animation completes
- Stagger entrance animations by 50-100ms per element for cascading reveals

## Design Token Architecture

Three-layer token structure (Martin Fowler's framework):

| Layer | Name | Example |
|-------|------|---------|
| **Option** (what) | Available choices | `--color-blue-500: oklch(0.55 0.25 260)` |
| **Decision** (how) | Semantic mapping | `--ag-ai-blue: var(--color-blue-500)` |
| **Component** (where) | Usage binding | `--button-primary-bg: var(--ag-ai-blue)` |

### Token Flow

```
DESIGN.md (specification)
    ↓
globals.css (CSS custom properties)
    ↓
@theme inline (Tailwind v4 mapping)
    ↓
Component code (utility classes + cva variants)
```

### Cross-Tool Sync

| Direction | Flow |
|-----------|------|
| DESIGN.md → Pencil | `set_variables` with tokens from DESIGN.md |
| DESIGN.md → Code | CSS custom properties in globals.css |
| Pencil → Code | `get_variables` → generate CSS |
| Figma → Code | `get_variable_defs` → Style Dictionary → CSS |
| Code → DESIGN.md | Extract tokens from globals.css → regenerate DESIGN.md |
| Code → Figma | `generate_figma_design` captures rendered UI |

## Resources

### references/
- `design-md-spec.md` — Full DESIGN.md specification with examples and writing rules
- `pencil-mcp-reference.md` — Complete Pencil MCP tool reference, batch_design syntax, .pen format
- `figma-mcp-reference.md` — Figma MCP ecosystem (official + community), Code Connect, Variables API
- `stitch-integration.md` — Stitch MCP server, SDK, skills, vibe design methodology
- `premium-design-principles.md` — Anti-generic patterns, material metaphors, atmospheric coherence
- `accessibility-enforcement.md` — WCAG 2.2 AA checklist, automated enforcement strategies
- `visual-validation.md` — Screenshot workflows, layout inspection, token auditing, responsive testing
