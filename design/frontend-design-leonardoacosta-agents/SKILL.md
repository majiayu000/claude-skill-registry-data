---
name: frontend-design
description:
  Create distinctive, production-grade frontend interfaces with high design quality. Use when asked
  to build web components, pages, artifacts, posters, or applications (websites, landing pages,
  dashboards, React components, HTML/CSS layouts), when styling/beautifying any web UI, when
  applying a color/font theme to slides/docs/HTML, or when reviewing UI against Vercel Web Interface
  Guidelines (accessibility, UX audit, design review). For changes to existing interfaces, defaults
  to a low-fidelity before-and-after comparison and an approval gate before implementation. Generates
  creative polished code, applies pre-built themes, and avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, WebFetch
---


This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic
"AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details
and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They
may include context about the purpose, audience, or technical constraints.

## Project Design Source of Truth (check FIRST)

Before committing to any aesthetic direction, check for a `DESIGN.md` at the project root:

```bash
[ -f DESIGN.md ] && echo "DESIGN.md present — it is the source of truth" || echo "no DESIGN.md — free creative direction"
```

**When `DESIGN.md` is present**, it is the **normative** design system — not a suggestion. It uses
the [`google-labs-code/design.md`](https://github.com/google-labs-code/design.md) format (YAML
token frontmatter + prose). You MUST:

- Parse the tokens (`colors`, `typography`, `spacing`, `rounded`, `components`) and use those exact
  values — do NOT invent palette or typography the file already defines.
- Honor the prose sections (Overview, Colors, Typography, Layout, Shapes, Components) for *how* to
  apply tokens, and treat **Do's and Don'ts** as hard guardrails.
- Generate consumable tokens from it rather than hand-writing CSS:
  `npx @google/design.md export --format tailwind DESIGN.md` (Tailwind v3 JSON) or `--format dtcg`.
  For Tailwind v4 `@theme`, mirror the YAML token values directly into the `@theme` block.
- Validate your output's contrast/refs against the system: `npx @google/design.md lint DESIGN.md`.

In this mode, the "BOLD aesthetic direction" guidance below is **constrained by** the design
system — express creativity in layout, composition, motion, and detail, NOT by overriding the
defined tokens.

**When no `DESIGN.md` exists**, proceed with the full creative-direction flow below. (If the work
is establishing a project's first design system, consider emitting a `DESIGN.md` so future frontend
work has a source of truth — `/bootstrap:design` produces one automatically, though it's now
bootstrap-profile only, `wsenv --profile bootstrap`.)

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural,
  luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric,
  soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for
  inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and
refined minimalism both work - the key is intentionality, not intensity.

## Operating Modes

This skill is not just a generator — it is a diagnostic. Three modes:

1. **Create** (default) — building new UI. Read the Aesthetics Guidelines + Canon of Slop first,
   then produce work that avoids every listed pattern.
2. **Audit** — the user shares existing UI/copy. If the project has a `DESIGN.md`
   (see § Project Design Source of Truth), audit against it FIRST — deviations from the committed
   token system are `STRUCTURAL` findings and outrank generic slop. Then run the Canon of Slop
   ([`references/anti-slop-canon.md`](references/anti-slop-canon.md)) + microcopy sins
   ([`references/microcopy.md`](references/microcopy.md)). Call out every pattern **by name**,
   then suggest the specific replacement.
3. **Spot-fix** — the user points at one element. Diagnose it, explain why it's slop, rewrite it.

**Always name the sin before fixing it.** "This is a purple-gradient hero (#7c3aed→#2563eb), the
default AI palette" builds more trust than "let's improve the colors."

## Default: Compare Before Implementing

When changing an existing interface, assume the user wants to approve the direction before code is
modified. The default deliverable is a **low-fidelity before-and-after comparison**, not an immediate
production implementation.

1. Inspect the real current interface and relevant source. Do not reconstruct the "before" state
   from memory or generic placeholders.
2. Create a self-contained comparison artifact in `docs/diagrams/` with side-by-side **Before** and
   **After** panels. Show desktop and mobile when responsive behavior matters.
3. Keep the mockups low fidelity. Communicate information hierarchy, grouping, labels, actions,
   responsive behavior, and interaction states without spending time on production polish.
4. Include a concise verdict, ranked findings, 2–3 viable approaches with trade-offs, and a clearly
   marked recommendation. End with explicit approval choices such as **Approve**, **Revise**, or
   **Choose another approach**.
5. Open or publish the artifact so the user can review it. Then stop at the approval gate. Do not
   edit production UI until the user approves a direction.

Model the comparison shape on a practical design-review page: anchored summary, paired desktop and
mobile screens, findings tied to visible evidence, alternatives, recommendation, and a final approval
section. The artifact should make the proposed behavioral and information-hierarchy changes obvious
without pretending to be the finished interface.

Skip this gate only when the user explicitly asks for direct implementation, explicitly approves an
already-presented design, or requests a tightly scoped spot-fix with no meaningful design choice.
When uncertain, present the comparison first.

### Severity (audit/spot-fix)

Rank every finding, then fix structural first — never polish a broken foundation:

| Token | Meaning |
|---|---|
| `STRUCTURAL` | Requires redesign/rewrite. Fundamental. |
| `SURFACE` | Easy fix — wrong font, color, or word. |
| `COSMETIC` | Minor polish pass. |

## Rationalizations (do not accept these from yourself)

| Rationalization | Reality |
|---|---|
| "Users are used to this kind of UI anyway" | Familiarity with mediocrity isn't a license to propagate it. |
| "It's faster to use the default AI-generated look/copy" | Fast slop is still slop. Quality needs considered editing. |
| "This doesn't need to be unique, it just needs to work" | Distinctiveness IS part of working — it builds trust and memorability. |

## File Output

All generated HTML, CSS, and standalone frontend files MUST be written to `docs/diagrams/` in the
current working directory. NEVER write to `/tmp`, project root, or any other location.

```bash
mkdir -p docs/diagrams
# Write to: docs/diagrams/my-diagram.html
```

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:

- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

**Raster imagery (hero shots, textures, mockup photos, social cards).** When a design needs a
real raster asset that CSS/SVG can't produce, generate it with the **`ai-media-gen`** skill
(`scripts/bin/ai-media image …`, Vercel AI Gateway) and match the prompt to your chosen palette
and aesthetic direction (style + dominant token colors). Logos remain `svgl`'s job; vector
diagrams remain `wayfinder`'s. See the `ai-media-gen` skill for usage.

## Frontend Aesthetics Guidelines

Focus on:

- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like
  Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics;
  unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant
  colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for
  HTML. Use Motion library for React when available. Focus on high-impact moments: one
  well-orchestrated page load with staggered reveals (animation-delay) creates more delight than
  scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking
  elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid
  colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms
  like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic
  shadows, decorative borders, custom cursors, and grain overlays.

### The Canon of Slop (NEVER)

These are the highest-signal markers of the 2024–2026 AI-generated design monoculture. NEVER ship
them. Name the pattern when you spot it.

| Pattern | Signature | Do instead |
|---|---|---|
| Purple gradient hero | `#7c3aed → #2563eb` on white | Real color theory for the context |
| Default "modern" sans | Inter / Roboto / DM Sans / Space Grotesk | Distinctive pairing (display + quiet body) |
| Glassmorphism cards | `backdrop-blur`, `bg-white/10` | Intentional depth via shadow tiers + meaningful borders |
| Rounded everything | `border-radius: 24px+` on all | Vary radius by role; let elements have edges |
| Emoji-as-icons in headers | "✨ Supercharge 🚀" | Real icon set (Phosphor) or none |
| Three-column feature grid | icon + label + 1 line ×3 | Let content shape the layout |
| Dark mode = black + purple | `#0f0f0f` + `#8b5cf6` | A considered dark palette + accent |
| "Get started for free" CTA | generic primary button | A label that says what happens |

The full 16-pattern canon, font alternatives by context, and non-state UX interaction
anti-patterns live in [`references/anti-slop-canon.md`](references/anti-slop-canon.md) — read it
in audit mode or when you need a specific replacement. The canon covers TASTE; for EXECUTION
craft failures (clipped content, off-center elements, misaligned columns, botched glass/shadow,
image seams, grain placement, contrast) with verify-before-ship checks, see
[`references/execution-craft.md`](references/execution-craft.md). For OKLCH palette generation,
APCA/WCAG contrast thresholds, fix-contrast-via-L, and gamut/P3 fallback mechanics, see
[`references/oklch-color-craft.md`](references/oklch-color-craft.md). For typography mechanics —
properties-over-raw-tags, font-synthesis, type scale, line-height/letter-spacing/measure,
truncation, punctuation, underline craft, iOS inputs, RTL, and selection — see
[`references/typography-craft.md`](references/typography-craft.md).

**Precedence:** when a project `DESIGN.md` defines tokens (see § Project Design Source of Truth),
it WINS over these defaults — even if it picks a font this canon would otherwise flag. The canon
governs *free* creative direction; a committed design system governs *constrained* direction.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No
design should be the same. Vary between light and dark themes, different fonts, different
aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need
elaborate code with extensive animations and effects. Minimalist or refined designs need restraint,
precision, and careful attention to spacing, typography, and subtle details. Elegance comes from
executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be
created when thinking outside the box and committing fully to a distinctive vision.

### The Signature (uniqueness is a method, not an adjective)

"Be distinctive" is not actionable on its own — a design that passes every canon row above and
still reads as boring picked a nonstandard font and called it done. Decide the **signature
artifact FIRST** — one deliberate, memorable element the whole design builds around — then layer
the other six components onto it: atmosphere (a considered mood, not a generic gradient wash),
layered depth (real z-axis relationships, not a flat stack), a character display face (not the
canon's rejected rotation), one bespoke silhouette (a shape/cutout/frame unique to this build),
a treated nav (not a bare default header), and real specifics (actual numbers, names, content —
not lorem-ipsum-shaped placeholders).

Field notes: **cohesion is the whole game** — one palette, one type voice, one world; a design
with six good ideas that don't belong together loses to one idea executed completely. Take the
design **language** from references (mood, construction, materials), never the content itself.
**Calm is allowed, dead is not** — restraint is a valid aesthetic choice, but "correct and inert"
is still a failure. Clean is the floor, never the achievement — reaching clean is not the same as
reaching distinctive.

## Aesthetic Decisions → Code

| Design Decision       | CSS/Tailwind Implementation                                                                            |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| Asymmetric layout     | `grid-cols-[2fr_1fr]`, `col-span-2`, offset margins (`ml-[15%]`)                                       |
| Overlap elements      | `relative`/`absolute` positioning, negative margins (`-mt-8`), `z-10`/`z-20` layering                  |
| Dramatic whitespace   | `py-32`, `gap-24`, `min-h-[80vh]` for sections                                                         |
| Controlled density    | `grid-cols-3 gap-2`, tight `leading-tight`, compact `p-2`                                              |
| Diagonal flow         | `skew-y-3` on section dividers, `clip-path: polygon(...)`                                              |
| Grid-breaking element | One child with `col-span-full -mx-8` breaking out of the grid                                          |
| Layered depth         | Stacked `box-shadow` (`shadow-xl shadow-primary/10`), backdrop blur, gradient overlays                 |
| Noise texture         | `bg-[url('/noise.svg')] opacity-5 mix-blend-overlay` on a pseudo-element                               |
| Grain overlay         | `before:content-[''] before:absolute before:inset-0 before:bg-noise before:opacity-[0.03]`             |
| Typography contrast   | Display font at `text-7xl font-black tracking-tighter` vs body at `text-base font-light tracking-wide` |

### Quick Recipes

**Hero with depth:**

```css
.hero {
  @apply relative min-h-[90vh] flex items-center;
  background: radial-gradient(ellipse at 30% 50%, hsl(var(--primary) / 0.15), transparent 70%);
}
.hero::before {
  @apply content-[''] absolute inset-0 bg-[url('/noise.svg')] opacity-5 mix-blend-overlay pointer-events-none;
}
```

**Staggered reveal on scroll:**

```tsx
<div className="space-y-6">
  {items.map((item, i) => (
    <div
      key={item.id}
      className="animate-in fade-in slide-in-from-bottom-4"
      style={{ animationDelay: `${i * 80}ms`, animationFillMode: "both" }}
    />
  ))}
</div>
```

## Implementation Checklist by Direction

**Minimalist:**

- [ ] Max 2 font weights, 1 accent color
- [ ] Generous whitespace (`gap-16`+ between sections)
- [ ] No shadows, no gradients, no borders -- rely on spacing alone
- [ ] Typography does ALL the heavy lifting (size contrast, weight contrast)

**Maximalist:**

- [ ] 3+ layered backgrounds (gradient + noise + blur)
- [ ] Multiple animation entry points (stagger, parallax, hover)
- [ ] Bold color blocking -- no neutral zones
- [ ] Intentional visual overload -- every element earns its complexity

**Dark luxury:**

- [ ] `bg-zinc-950` or darker, accent in gold/warm tones
- [ ] Subtle grain texture overlay at 3-5% opacity
- [ ] `backdrop-blur-xl` on glass cards
- [ ] Thin borders (`border border-white/5`) for depth without weight

**Editorial:**

- [ ] Dominant serif display font (`Playfair Display`, `Fraunces`, `DM Serif`)
- [ ] Asymmetric 2-column layout with oversized images
- [ ] Pull quotes and drop caps
- [ ] High contrast black/white with one editorial accent color

## Pre-Built Themes

10 ready-to-apply professional themes are available in `references/themes/`. Each defines a complete
color palette + font pairing. Show `assets/theme-showcase.pdf` to the user for visual selection,
then read the chosen theme file and apply it.

**Available themes:** Ocean Depths, Sunset Boulevard, Forest Canopy, Modern Minimalist, Golden Hour,
Arctic Frost, Desert Rose, Tech Innovation, Botanical Garden, Midnight Galaxy.

To generate a custom theme on-the-fly: extract colors/tone from user description and create a new
theme spec in the same format as `references/themes/*.md`.

**Matching a specific brand's aesthetic** ("make it look like Linear", "Stripe-style checkout")
is a different task from picking a pre-built theme — read
[`references/brand-design-catalogue.md`](references/brand-design-catalogue.md) for the 66-brand
DESIGN.md catalogue (fetch commands, section-scan guide, one-brand-per-page rule). Use this only
when the user names a specific brand as the target; for generic "modern/minimal/professional"
requests, stay with the Design Thinking flow above instead.

## CSS Microinteractions (motion-and-transitions)

For UI state changes — modals, dropdowns, panels, badges, page slides, icon swaps, number pop-ins,
card resizes — load the `motion-and-transitions` skill. It ships nine copy-ready CSS snippets (from
[transitions.dev](https://transitions.dev)) with a unified curve language (out-quint for ambient,
spring-overshoot for attention) and mandatory `prefers-reduced-motion` guards. This is the **first
stop** for any "make X open/close smoothly" request before reaching for GSAP or WebGL.

**When to use:** Any UI component that transitions between two states — open/closed, visible/hidden,
active/idle. Does not require React; works in plain HTML + CSS.

**How to load:** `Skill({ skill: "motion-and-transitions" })`

## Motion & Animation Components (Motion Core)

For designs needing interactive animations, 3D effects, text reveals, scroll-driven motion, or
physics-based interactions, read `references/motion-core.md`. This provides React porting patterns
for 36 production-ready animation components spanning:

- **Text animations:** Split reveals, scramble effects, weight waves, text loops
- **3D/WebGL effects:** Glass refraction, god rays, globes, fluid simulation, dithering
- **Interaction:** Magnetic cursor, macOS dock, image trails, interactive grids
- **Layout animation:** FLIP grids, card stacks, slideshows, marquees
- **Atmosphere:** Halo, lava lamp, neural noise, plasma, glitter cloth

**When to suggest:** Hero sections needing interactive depth, scroll-driven reveals, hover effects
with physics, image galleries with 3D transitions, navigation with micro-interactions, or any design
where motion would elevate the aesthetic beyond static CSS. Pair with Radiant shaders for layered
depth.

**Stack:** React Three Fiber (`@react-three/fiber`) for WebGL, GSAP (`@gsap/react`) for DOM
animations. Shaders are framework-agnostic GLSL — copy verbatim from reference.

## Generative Shader Effects (Radiant)

For designs needing animated backgrounds, hero effects, or visual depth beyond static CSS, read
`references/radiant-shaders.md`. This provides access to 91 production-ready, zero-dependency shader
effects (Canvas 2D + WebGL) embeddable via iframe.

**When to suggest:** Hero sections, full-viewport backgrounds, dark-themed interfaces, or any design
where generative motion would elevate the aesthetic. Especially effective with the Mono, Blue, or
Arctic color schemes for tech/corporate contexts.

A React/Next.js wrapper component is available at `~/.claude/recon/radiant-react-wrapper/` — copy
into the target project and use `<RadiantShader html={...} colorScheme="blue" loading="lazy" />`.

## Icon Sourcing (UI chrome, brand logos, cloud/infra marks)

For any icon need — generic UI chrome, brand logos (dev/SaaS or real-world consumer/enterprise),
or cloud/infra service marks — read [`references/icon-sourcing.md`](references/icon-sourcing.md).
It consolidates the decision ladder + full API/usage reference for four sourcing libraries:

- **Phosphor Icons** — default library for generic UI chrome (nav, buttons, status, forms).
  6 weights, one weight per region.
- **svgl.app** — first choice for dev/SaaS brand logos (Stripe, GitHub, Vercel, AWS...). Official
  press-kit fidelity; never guess CDN paths, search the API.
- **Boxicons `bxl-*`** — community-drawn brand-logo fallback when svgl doesn't have it.
- **thesvg** — cloud architecture icons (739 AWS + 627 Azure + 214 GCP, svgl carries none of
  these) plus a ~4,500-logo long tail for real-world brands (BMW, Delta, Coca-Cola...). Carries a
  load-bearing licensing table — AWS marks are `CC-BY-ND` (no derivatives), GCP is `Apache-2.0`.

**Never use emojis as brand or UI-icon placeholders.**

## Dithering, Halftone & ASCII Effects

For retro/CRT/1-bit aesthetics — Bayer/Floyd-Steinberg dithering, ASCII art cards, halftone
textures — read [`references/dithering-recipes.md`](references/dithering-recipes.md). Covers the
approach-selection ladder (`react-ascii-ui` drop-in -> React Bits `Dither` -> zero-dep Canvas 2D +
Bayer matrix -> R3F/GLSL shader for full-motion), with copy-ready code for each tier and a
skip-to-shader signal table (CRT/scanlines/video briefs skip straight past the drop-in libraries).

**When to suggest:** brutalist/zine layouts, monochrome hero imagery needing texture, ASCII
quote/portrait cards, or any brief invoking classic Mac/Amiga/CRT references.

## Related Skills

When building frontend interfaces, also consider these complementary skills and reference files:

- **`references/icon-sourcing.md`** — icon and brand-logo sourcing (generic UI iconography, brand
  logos, cloud/infra service marks). Use for navigation, actions, status indicators, and any
  brand-iconography need.
- **[`references/algorithmic-art/README.md`](references/algorithmic-art/README.md)** —
  generative/algorithmic art patterns (p5.js, seeded randomness, flow fields, particle systems).
  Use for creative backgrounds, data visualizations, and decorative elements.
- **[`references/brainless/README.md`](references/brainless/README.md)** — recreating Claude
  Code / Codex / Grok terminal chrome (40-component shadcn registry) for docs/demo/marketing
  pages only — not production app UI.

### Folded-in reference material (formerly standalone skills)

Demoted here (`skill-classification-and-trial-lifecycle`, 2026-07-18, plus `algorithmic-art` +
`brainless` via `remediate-below-floor-skills`, 2026-07-18) because each was lookup/catalog-shaped
content, not decision-shaping knowledge — see each file's header note for the specific rationale:

- **[`references/geist-design.md`](references/geist-design.md)** — Vercel Geist design system:
  tokens, typography, materials, brand guidelines.
- **[`references/design-system-starter/README.md`](references/design-system-starter/README.md)**
  — design-system scaffolding: tokens, component architecture, accessibility checklists,
  documentation templates.
- **[`references/componentry/README.md`](references/componentry/README.md)** and
  **[`references/aceternity/README.md`](references/aceternity/README.md)** — prebuilt animated
  React component catalogs (shadcn-compatible); componentry's README covers when to reach for
  one vs the other.
- **[`references/ui-ux-pro-max/README.md`](references/ui-ux-pro-max/README.md)** — searchable
  design-intelligence database (161 color palettes, 57 font pairings, 99 UX guidelines, 25 chart
  types across 10 stacks).
- **[`references/ai-media-generation.md`](references/ai-media-generation.md)** — generating
  raster images/video via the `ai` CLI, for assets mermaid/wayfinder/excalidraw (all vector)
  cannot produce.
- **[`references/algorithmic-art/README.md`](references/algorithmic-art/README.md)** — p5.js
  generative-art authoring guide (algorithmic philosophy → seeded-randomness implementation).
- **[`references/brainless/README.md`](references/brainless/README.md)** — install pointer +
  component catalogue for `theswerd/brainless`'s agent-terminal-chrome shadcn registry.

### Skill boundaries (do not duplicate)

- **`state-handling`** owns loading / empty / error STATE patterns. The non-state UX interaction
  anti-patterns (modals, wizards, hamburger-on-desktop, toast spam, hover-only) live in this
  skill's [`references/anti-slop-canon.md`](references/anti-slop-canon.md); for *state* behavior,
  defer to `state-handling`.
- **Repository-local writing guidance** owns general prose voice (Teams / Slack / email / chat replies). This
  skill's [`references/microcopy.md`](references/microcopy.md) covers UI microcopy ONLY — error
  messages, CTA labels, empty-state text, form labels. For human-facing prose, load
  that guidance instead.

## Validation

To check UI code against Vercel's Web Interface Guidelines, fetch:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Apply all rules from the fetched content and report findings as `file:line` violations.
