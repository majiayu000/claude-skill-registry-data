---
name: design
description: |
  Create distinctive, non-generic UI designs with aesthetic direction and wireframes,
  or polish existing UI code after implementation.
  Use when asked to "design the UI", "create a layout", "wireframe this", or when building
  UI that should be memorable rather than generic. Also handles "clean this up",
  "componentize this", and other post-implementation polish work. Avoids AI slop patterns.
license: MIT
metadata:
  author: howells
website:
  order: 8
  desc: Visual design direction
  summary: Visual direction plus code polish. Establish UI identity, reusable Tailwind patterns, critique loops, and post-implementation cleanup guidance.
  what: |
    Design now has explicit mode detection. In design mode it walks through visual decisions, references persistent design context, researches examples, and produces a design direction document for implementation. In polish mode it tightens UI code after implementation: extracting reusable pieces, deduplicating patterns, and cleaning up Tailwind class authoring without changing the product direction.
  why: |
    AI-generated UI tends toward the same safe choices—the same gradients, the same card layouts, the same hero sections. Design fights this by forcing you to make distinctive choices upfront and documenting them. The references help you avoid common pitfalls and give the AI better taste.
  decisions:
    - Mode-aware. Full design flow for new UI, focused polish flow for cleanup.
    - Opinionated references built in. Font choices, spacing scales, animation patterns—not starting from scratch.
    - WireText when available, ASCII when not. Focus on structure before fidelity.
    - Visual verification via screenshots. Catches when implementation drifts from intent.
  workflow:
    position: branch
    joins: implement
---

<tool_restrictions>

# MANDATORY Tool Restrictions

## BANNED TOOLS — calling these is a skill violation:

- **`EnterPlanMode`** — BANNED. Do NOT call this tool. This skill has its own multi-phase design process. Execute the phases below directly.
- **`ExitPlanMode`** — BANNED. You are never in plan mode.
  </tool_restrictions>

<arc_runtime>
This workflow requires the full Arc bundle, not a prompts-only install.

Paths in this skill use these conventions:

- `agents/...`, `references/...`, `disciplines/...`, `templates/...`, `scripts/...`, `rules/...`, `skills/<name>/...` are Arc-owned files at the plugin root. Resolve the plugin root from this skill's filesystem location — it's the directory containing `agents/` and `skills/`.
- `./...` is local to this skill's directory.
- `.ruler/...`, `docs/...`, `src/...`, or any project-relative path refers to the user's project repository.
  </arc_runtime>

# Design Workflow

Create distinctive, non-generic UI. Avoids AI slop (purple gradients, cookie-cutter layouts).

**Announce at start:** "I'm using the design skill to create distinctive, non-generic UI."

## Tailwind-First Constraint

Arc UI design assumes **Tailwind is the implementation target**.

- Design decisions MUST be expressible as **Tailwind v4 `@theme` tokens** plus utility classes
- Spacing, sizing, radius, typography, and interaction states MUST map cleanly to Tailwind utilities
- Component patterns MUST be described in a way `ui-builder` can implement with Tailwind classes
- Do NOT produce framework-agnostic styling plans as the primary output
- Do NOT default to bespoke CSS, CSS Modules, styled-components, or emotion when Tailwind utilities and tokens are sufficient
- Raw CSS is only for unavoidable global primitives or capabilities Tailwind does not express directly

<important>
**This skill is user-interactive. Do NOT spawn agents to do design work.**

- This skill walks through design decisions WITH the user — it's collaborative, not delegated
- There is no `arc:design:designer` agent — design creation happens through this skill
- `arc:review:designer` exists but is for REVIEWING implementations AFTER they're built, not for creating designs
- If asked to "design X", follow this skill's phases; don't try to spawn an agent
  </important>

---

## Agents

**This skill works with these agents (reuse, don't duplicate):**

| Agent              | Location       | When to Use                                                       |
| ------------------ | -------------- | ----------------------------------------------------------------- |
| `ui-builder`       | agents/build/  | Build UI from the change spec you create                          |
| `figma-builder`    | agents/build/  | Build UI when Figma URL is provided                               |
| `design-specifier` | agents/build/  | Quick design decisions during implement (empty states, dropdowns) |
| `designer`         | agents/review/ | Review implemented UI for AI slop                                 |

**Workflow:**

```
/arc:design (this skill)
     ↓ creates change spec
ui-builder or figma-builder (builds it)
     ↓ implements
designer (reviews for AI slop)
```

## Mode Detection

Decide which path applies before loading the heavy reference set.

**Design mode (default):**

- The user wants visual direction, layout exploration, wireframes, or a design doc.

**Polish mode:**

- The user asks to clean up, componentize, deduplicate, organize, or polish existing UI code.

**Component fast-path:**

- The user is designing a single component or small UI fragment rather than a page or product surface.
- Use targeted rules and skip the heavier reconnaissance / research flow.

Announce the chosen mode before continuing.

## Phase 0: Load References & Design Context

In full design mode, read the full reference set below. The component fast-path overrides this and loads only the relevant targeted rules.

**In full design mode, you MUST read these files before proceeding.**

<required_reading>
**Read ALL of these using the Read tool:**

1. `references/frontend-design.md` — UI fonts, anti-patterns, design review checklist. **Critical.**
2. `references/brand-identity.md` — Brand typography, color psychology, visual character (if no brand-system.md exists)
3. `references/design-philosophy.md` — Timeless principles from Refactoring UI
4. `references/ux-laws.md` — Psychology-based design principles: Fitts's, Hick's, Gestalt, Jakob's Law, Doherty Threshold
5. `references/typography-opentype.md` — OpenType features, tracking, text-wrap, fluid sizing
6. `references/ascii-ui-patterns.md` — Wireframe syntax and patterns
7. `references/wiretext.md` — When to use WireText vs ASCII vs browser review
8. `references/tailwind-v4.md` — Tailwind v4 syntax and token patterns

**Then load interface rules:** 9. `rules/interface/index.md` — Interface rules index 10. `rules/interface/tailwind-authoring.md` — Tailwind class-level discipline 11. `rules/interface/buttons.md` — Button sizing and hierarchy 12. `rules/interface/surfaces.md` — Surface hierarchy and card usage 13. `rules/interface/sections.md` — Page section composition

**And relevant domain rules based on what you're designing:**

- `rules/interface/design.md` — Visual principles
- `rules/interface/colors.md` — Color palettes, OKLCH, tinted neutrals
- `rules/interface/spacing.md` — Spacing system, container queries
- `rules/interface/typography.md` — Typography rules, OpenType features
- `rules/interface/layout.md` — Layout patterns, z-index
- `rules/interface/responsive.md` — Responsive design, input detection
- `rules/interface/animation.md` — If motion is involved
- `rules/interface/forms.md` — If designing forms
- `rules/interface/interactions.md` — Interactive states, popover API
- `rules/interface/marketing.md` — If designing marketing pages
- `rules/interface/app-ui.md` — If designing app UI (dashboards, settings, data views)
  </required_reading>

### Brand System & Design Context

**Check for `docs/brand-system.md` first, then `docs/design-context.md`.**

If `brand-system.md` exists (created by `/arc:brand`), load it — this is the canonical source for palette, typography, tone, and visual character. **Do not re-ask brand questions.** Inherit all identity decisions and focus this skill on feature-level UI design.

If only `design-context.md` exists, load it — this file contains project-wide aesthetic decisions (brand colors, chosen fonts, spacing scale, tone) that all design work should inherit. **Do not re-ask questions that are already answered in design-context.md.** Skip to Phase 1 for any established decisions.

If it does NOT exist, offer to create one:

**Use the AskUserQuestion interaction pattern:**

```
Question: "No project-wide design context found. Want to establish one? This saves brand decisions (colors, fonts, tone) so every future design session inherits them."
Header: "Design context"
Options:
  1. "Yes, establish context" (Recommended) — Create docs/design-context.md with persistent aesthetic decisions
  2. "No, one-off design" — Proceed without persistent context
```

**If creating context, gather and save to `docs/design-context.md`:**

````markdown
# Design Context

Persistent aesthetic decisions for this project. All design work inherits these choices.

## Brand

- **Name**: [project name]
- **Personality**: [e.g., confident and technical, warm and approachable]
- **Tone**: [chosen from tone options]

## Typography

- **Display font**: [specific font]
- **Body font**: [specific font]
- **Mono font**: [specific font, if applicable]

## Color Palette (Tailwind @theme)

```css
@theme {
  --color-brand-500: oklch(.........);
  /* Full shade scale */
  --color-gray-500: oklch(.........);
  /* Tinted neutral scale */
}
```
````

## Spacing

- **Base unit**: 4px
- **Scale**: Tailwind default (p-1=4px through p-16=64px)

## UI System Snapshot

### Tokens

- **Depth model**: [borders-only / subtle shadows / layered surfaces]
- **Surface ladder**: [canvas, surface, raised, overlay]
- **Radius scale**: [e.g., 4px, 8px, 12px]
- **Control heights**: [e.g., 32px, 40px, 48px]

### Canonical Patterns

- **Primary button**: [height, padding, radius, emphasis]
- **Default card/panel**: [padding, border/shadow treatment, radius]
- **Input/select**: [height, padding, border/fill treatment]
- **Dense data treatment**: [table row height, stat card rhythm, list spacing]

## Motion Philosophy

- **Style**: [e.g., snappy and confident, smooth and refined]
- **Library**: [CSS transitions / motion/react]

## Memorable Element

- [What makes this project's UI distinctive]

## Anti-Patterns (Project-Specific)

- [Anything specifically to avoid for this project]

```

After creating, proceed to Phase 1.

<progress_context>
**Use Read tool:** `docs/arc/progress.md` (first 50 lines)

Check for related prior design work and aesthetic decisions.
</progress_context>

**Internal consistency rule:** if any later design choice conflicts with the stored design context, brand system, or interface rules, resolve that conflict before moving on. Do not let the spec say one thing and the implementation guidance imply another.

---

## Phase 0.5: Component Fast-Path

If the request is for a single component rather than a page or product flow:
- Load only the 2-3 relevant rules files for that component type
- Skip visual reconnaissance unless the component already exists and is being redesigned
- Skip external inspiration research
- Compress direction gathering to 1-2 questions
- Continue with wireframe -> spec -> critique -> handoff as normal

## Phase 1: Visual Reconnaissance

**Before designing anything, see what exists.**

### If Redesigning Existing UI:

**Prefer Chrome MCP to capture current state. If unavailable, use `agent-browser`. If neither is available, ask for screenshots or review the code directly.**

```

1. mcp**claude-in-chrome**tabs_context_mcp (get available tabs)
2. mcp**claude-in-chrome**tabs_create_mcp (create new tab if needed)
3. mcp**claude-in-chrome**navigate to the local dev URL
4. mcp**claude-in-chrome**computer action=screenshot

```

**Analyze the screenshot against the Design Review Checklist from frontend-design.md:**
- Does it have any Red Flags (AI slop indicators)?
- What's the current aesthetic direction (if any)?
- What's working? What's not?

**Report findings to user:** "Here's what I see in the current UI: [observations]. The main issues are: [problems]."

### If Designing From Scratch:

- Confirm dev server is running (or will be)
- Ask if there's any existing brand/style guide to reference
- Check if there are reference designs or inspiration URLs to screenshot

---

## Phase 1.5: Design Mode

**Before gathering direction, establish what kind of UI you're designing.**

**Use the AskUserQuestion interaction pattern:**
```

Question: "What are you designing?"
Header: "Design mode"
Options:

1. "Marketing page" — Landing page, homepage, pricing, about, blog. Goal: persuade and convert.
2. "App UI" — Dashboard, settings, forms, data views. Goal: enable and orient.

```

**After selection:**
- **Marketing** → Load `rules/interface/marketing.md` as mandatory reference
- **App UI** → Load `rules/interface/app-ui.md` as mandatory reference

This mode context informs all subsequent phases — questions, research sources, wireframe patterns, and checklist items adapt accordingly.

---

## Phase 2: Gather Direction

### Question 0: Exploration Mode (Conditional)

**Offer this option when circumstances allow:**
- New project with no established design system
- Homepage, landing page, or marketing site design
- User seems uncertain about direction
- Greenfield UI with creative freedom

**Do NOT offer when:**
- Strict brand guidelines exist
- Designing a small component or iteration
- User has already specified a clear direction
- Adding to an existing design system

**If circumstances allow, use the AskUserQuestion interaction pattern:**
```

Question: "Would you like me to create 5 vastly different design directions, each at its own route? This lets you compare radically different approaches before committing."
Header: "Exploration"
Options:

1. "Yes, explore 5 directions" — Create /design-1 through /design-5 with completely different aesthetics
2. "No, single direction" (Recommended) — Focus on one well-crafted design

```

**If exploration mode is chosen:**
- Each route (/design-1, /design-2, etc.) gets a completely different aesthetic
- Vary: color palette, typography, layout structure, tone, spatial composition
- Don't just tweak—make them *unrecognizable* from each other
- Write a style definition brief for each direction before building it:
  - Layout structure
  - Typography character
  - Color direction
  - Spacing strategy
  - Surface treatment
  - Shape language
  - Personality
- After building all 5, ask user which direction resonates
- Then proceed with full design doc for the chosen direction

---

Ask the remaining questions **one at a time**:

### Question 1: Tone
"What tone fits this UI?"
- Minimal, bold, playful, editorial, luxury, brutalist, retro, organic, industrial, art deco, soft/pastel

### Question 1.5: Mode-Specific Question

**If Marketing mode:**
"How does the page tell its story?"
- Hero → problem → solution → proof → CTA (classic)
- Immersive scroll narrative (one idea per viewport)
- Feature showcase (dense, scannable)
- Minimal single-screen (everything above the fold)
- Editorial long-form (article-like)

**If App UI mode:**
"How information-dense should this be?"
- Sparse — generous whitespace, one focus per screen (e.g., onboarding)
- Balanced — comfortable density, clear hierarchy (e.g., settings)
- Dense — lots of data visible at once (e.g., dashboard, table views)

### Question 2: Memorable Element
"What should be memorable about this?"

**If Marketing:** The animation? Typography drama? Layout surprise? Photography style? Scroll behavior?

**If App UI:** The navigation paradigm? Micro-interactions? Information density approach? Empty state creativity? Data visualization style?

### Question 3: Existing Constraints
"Any existing brand/style to match, or fresh start?"

### Question 4: Inspiration
"Any reference designs or inspiration?"
- If provided, **screenshot them immediately using Chrome MCP** for visual reference

### Question 5: UI Chrome
"Should this have standard website chrome (header, footer, navigation), or feel more like an app?"

Consider:
- **Standard website chrome** — Fixed header with logo/nav, footer with links. Good for content sites, marketing pages, multi-page experiences where users need to navigate.
- **App-like experience** — Minimal or no persistent chrome. Content takes full focus. Good for tools, dashboards, immersive experiences, single-purpose flows.
- **Hybrid** — Minimal header (maybe just a logo), no footer. Common for SaaS apps.

**The default shouldn't always be "header + footer".** If the experience is focused (a tool, a game, a single flow), standard chrome can feel clunky and distract from the core experience. Let the purpose guide the frame.

---

## Phase 3: Research Inspiration (Optional)

**Use WebFetch to explore curated design examples based on the chosen direction.**

This phase is optional but recommended when:
- Starting from scratch with no existing references
- The user wants to see examples matching their chosen tone
- You need concrete visual patterns to inform decisions

### Siteinspire (Website/Homepage Design)

Siteinspire curates high-quality website designs. Use WebFetch to explore based on the chosen tone:

```

WebFetch URL patterns by tone:

- Minimal: https://www.siteinspire.com/websites?style=minimal
- Bold: https://www.siteinspire.com/websites?style=bold
- Playful: https://www.siteinspire.com/websites?style=playful
- Editorial: https://www.siteinspire.com/websites?style=editorial
- Luxury: https://www.siteinspire.com/websites?style=luxury
- Brutalist: https://www.siteinspire.com/websites?style=brutalist
- Retro: https://www.siteinspire.com/websites?style=retro
- Organic: https://www.siteinspire.com/websites?style=organic

By page type:

- Homepage: https://www.siteinspire.com/websites?page=homepage
- Portfolio: https://www.siteinspire.com/websites?page=portfolio
- E-commerce: https://www.siteinspire.com/websites?page=e-commerce
- Blog: https://www.siteinspire.com/websites?page=blog

```

**WebFetch prompt:** "List the website names, their URLs, and a brief description of their visual style. Focus on typography choices, color palettes, and layout patterns."

### Mobbin (UI/Mobile Design Patterns)

Mobbin collects UI patterns from real apps. Use for component and interaction inspiration:

```

WebFetch URL patterns:

- iOS apps: https://mobbin.com/browse/ios/apps
- Android: https://mobbin.com/browse/android/apps
- Web apps: https://mobbin.com/browse/web/apps

By screen type:

- Onboarding: https://mobbin.com/browse/ios/screens?screen=onboarding
- Dashboard: https://mobbin.com/browse/ios/screens?screen=dashboard
- Settings: https://mobbin.com/browse/ios/screens?screen=settings
- Profile: https://mobbin.com/browse/ios/screens?screen=profile
- Search: https://mobbin.com/browse/ios/screens?screen=search

```

**WebFetch prompt:** "List the apps shown and describe their UI patterns—navigation style, card layouts, typography hierarchy, and interaction patterns."

### Research Workflow

1. **Based on user's chosen tone**, fetch 1-2 relevant Siteinspire pages
2. **Based on what you're designing** (homepage, dashboard, form), fetch relevant Mobbin screens
3. **Summarize findings** to user: "I found these patterns that match your direction: [observations]"
4. **Ask:** "Any of these resonate? Should I explore a specific site further with Chrome MCP?"

### Deep Dive with Chrome MCP

If a specific example catches interest, use Chrome MCP for detailed inspection:

```

1. mcp**claude-in-chrome**navigate to the specific site URL
2. mcp**claude-in-chrome**computer action=screenshot
3. Analyze: typography, colors, spacing, layout patterns
4. Report specific values observed (font names, color relationships, spacing) and translate them into Tailwind-friendly tokens/utilities

```

**Note:** WebFetch provides quick overview; Chrome MCP provides detailed visual inspection. Use both strategically.

---

## Phase 4: Make Concrete Visual Decisions

**Capture SPECIFIC visual decisions, not conceptual themes.**

<principle>
**Complexity Matching:** Design complexity should align with aesthetic vision. Maximalist designs warrant elaborate code and rich details. Minimalist designs require restraint and precision—every element must earn its place. Don't add flourishes to a minimal design; don't under-build a maximalist one.
</principle>

Apply knowledge from the loaded references to make these decisions:

### Typography Selection
Using the font recommendations from `frontend-design.md`:
- **Display font:** [specific font name]
- **Body font:** [specific font name]
- **Mono font (if needed):** [specific font name]

**Never use:** Roboto, Arial, system-ui defaults, Instrument Serif (AI slop)

**Eyebrow / label discipline (anti-overuse rule):**
- Do **not** default to `uppercase tracking-wide`/`tracking-widest` eyebrows above headings. This is the typographic equivalent of a purple-to-blue gradient — overused on every AI-built section.
- Only use `uppercase` on eyebrow/label text when the font is **monospace**, and only then pair it with `tracking-wide`.
- For sans/serif eyebrows, prefer alternatives: a numeric label (`01 / Pricing`), a kicker in the display font at smaller weight, a colored dot + label in sentence case, or just remove the eyebrow entirely.
- One uppercase-tracked eyebrow style across an entire page is a code smell — the choice is doing nothing, so cut it.

### Color Palette
- **Define in Tailwind v4 `@theme` with OKLCH, not hex-only values**
- **Background token:** [e.g., `--color-gray-950: oklch(...)`]
- **Surface token:** [e.g., `--color-gray-900: oklch(...)`]
- **Text primary token:** [e.g., `--color-gray-50: oklch(...)`]
- **Text secondary token:** [e.g., `--color-gray-400: oklch(...)`]
- **Accent token:** [e.g., `--color-brand-500: oklch(...)`]
- **Accent hover token:** [e.g., `--color-brand-600: oklch(...)`]

**Never use:** Purple-to-blue gradients (AI cliché)
**Never use:** Hex-only palettes with no OKLCH/Tailwind token mapping

### Spacing System
Define the scale being used:
- **Base unit:** 4px or 8px
- **Common values:** 4, 8, 12, 16, 24, 32, 48, 64
- **Component padding:** [e.g., 16px default, 24px for cards]
- **Section spacing:** [e.g., 64px between major sections]

### Spatial Composition
Beyond basic layout, make deliberate choices about:
- **Asymmetry:** Not everything needs to be centered or perfectly balanced
- **Overlap:** Elements can break grid boundaries, bleed off edges, layer on top of each other
- **Unexpected layouts:** Break the "header → hero → 3-column features → footer" pattern
- **Negative space:** Generous whitespace creates breathing room and draws focus to what matters

**Ask:** "Where can the layout do something unexpected?"

### Motion Philosophy
- **Where animation is used:** [specific locations]
- **Animation style:** [e.g., ease-out for enters, springs for interactive]
- **Duration range:** [e.g., 150-300ms]

### UI System Snapshot
Capture the reusable system that implementation should preserve:
- **Depth model:** [borders-only / subtle shadows / layered surfaces]
- **Surface ladder:** [canvas → surface → raised → overlay]
- **Radius scale:** [e.g., 4px / 8px / 12px]
- **Control heights:** [e.g., 32px compact, 40px default, 48px prominent]
- **Primary button pattern:** [height, padding, radius, fill/border treatment, core Tailwind utility shape]
- **Card/panel pattern:** [padding, border/shadow, radius, core Tailwind utility shape]
- **Input/select pattern:** [height, padding, border/background treatment, core Tailwind utility shape]

---

## Phase 5: Wireframe

**Create a structural wireframe before any code.**

Prefer WireText MCP when available for low-fidelity wireframes. If WireText is unavailable, create ASCII wireframes using patterns from `ascii-ui-patterns.md`.

If WireText is used:
- save the editable URL in the design doc
- capture the exported wireframe text or a short structural summary
- treat it as the source of layout structure, not visual fidelity

```

┌─────────────────────────────────────┐
│ Logo [Search...] [Menu] │
├─────────────────────────────────────┤
│ │
│ [Main Content Area] │
│ │
└─────────────────────────────────────┘

````

**Include:**
1. Primary layout structure
2. Key interactive elements
3. Mobile version if responsive
4. States: empty, loading, error (where relevant)

**If App UI mode:** You MUST include at least one state variant beyond the populated state (empty, loading, or error). App UI without state design is incomplete.

**Ask:** "Does this structure feel right before I continue?"

---

## Phase 5.5: Create Change Spec

**THIS IS CRITICAL.** Translate aesthetic direction into **specific, measurable changes**:

```markdown
## Change Spec

### Typography
| Element | Before | After | Rule Reference |
|---------|--------|-------|----------------|
| h1 | `text-2xl font-normal` | `text-5xl font-semibold tracking-tight` | typography.md: display hierarchy |
| body | `text-sm font-normal` | `text-base/7 font-normal` | typography.md: body readability |

### Colors
| Element | Before | After | Rule Reference |
|---------|--------|-------|----------------|
| background | `bg-white` | `bg-gray-50` backed by `--color-gray-50: oklch(...)` | colors.md: warmth |
| accent | none | `bg-brand-500 hover:bg-brand-600` backed by `--color-brand-500/600` | colors.md: accent strategy |

### Spacing
| Element | Before | After | Rule Reference |
|---------|--------|-------|----------------|
| section padding | p-4 (16px) | p-12 (48px) | spacing.md: generous whitespace |

### Layout
| Element | Before | After | Rule Reference |
|---------|--------|-------|----------------|
| hero | centered text | asymmetric split with image overlap | layout.md: break the grid |

### Motion (if applicable)
| Element | Before | After | Rule Reference |
|---------|--------|-------|----------------|
| page load | none | staggered fade-up, 50ms delay | animation.md: entrance sequence |
````

**Rules for change specs:**

- Every change references a rule from the interface rules
- Changes must be **substantial**, not tweaks
- Specific values, tokens, and Tailwind utility shapes, not vague descriptions

**Self-check:**

- [ ] At least 3 typography changes?
- [ ] Color palette actually different?
- [ ] Spacing significantly adjusted?
- [ ] Memorable element clearly identified and designed?

**If you're only changing padding values, STOP. That's not a redesign.**

---

## Phase 6: Produce Design Document

**Create the design direction document at `docs/arc/specs/design-[component-name].md`:**

```markdown
# Design Direction: [Component/Page Name]

## Aesthetic Direction

- **Tone:** [chosen - e.g., "minimal", "bold", "editorial"]
- **Memorable element:** [specific - e.g., "oversized typography", "micro-interactions on hover"]

## Typography

- **Display:** [font name] — [where used]
- **Body:** [font name] — [where used]
- **Mono:** [font name] — [where used, if applicable]

## Color Palette

| Role           | Value                           | Usage           |
| -------------- | ------------------------------- | --------------- |
| Background     | `--color-gray-950: oklch(...)`  | Page background |
| Surface        | `--color-gray-900: oklch(...)`  | Cards, panels   |
| Text primary   | `--color-gray-50: oklch(...)`   | Headings, body  |
| Text secondary | `--color-gray-400: oklch(...)`  | Labels, hints   |
| Accent         | `--color-brand-500: oklch(...)` | CTAs, links     |
| Accent hover   | `--color-brand-600: oklch(...)` | Hover states    |

## Spacing

- Base unit: 4px
- Tailwind spacing scale: `p-4` / `p-6` / `p-8`, `gap-4` / `gap-6` / `gap-8`
- Section gaps: `gap-12` (tight), `gap-16` (normal), `gap-24` (generous)

## Motion

- Page transitions: fade, 200ms ease-out
- Interactive elements: spring (stiffness: 400, damping: 25)
- Hover states: 150ms ease-out

## Layout

### Desktop

[ASCII wireframe]

### Mobile

[ASCII wireframe]

## Implementation Notes

- [Any specific technical considerations]
- Tailwind-first implementation: express decisions as `@theme` tokens plus utilities
- [Component library preferences]
- [Animation library: CSS-only vs motion/react]
- Avoid bespoke CSS when utilities/tokens are sufficient; extract components before reaching for custom styling

## UI System Snapshot

### Tokens

| Token           | Value                             | Usage                              |
| --------------- | --------------------------------- | ---------------------------------- |
| Depth model     | borders-only                      | Global surface strategy            |
| Surface ladder  | canvas / panel / raised / overlay | Layering hierarchy                 |
| Radius scale    | 4px / 8px / 12px                  | Controls, cards, dialogs           |
| Control heights | 32px / 40px / 48px                | Dense, default, prominent controls |

### Canonical Patterns

| Pattern        | Spec                                                   | Usage             |
| -------------- | ------------------------------------------------------ | ----------------- |
| Primary button | `h-10 px-4 rounded-lg bg-brand-500 hover:bg-brand-600` | Main CTA          |
| Default card   | `rounded-xl border border-gray-200 p-5`                | Content container |
| Input/select   | `h-10 px-3 rounded-lg border border-gray-300`          | Form controls     |
| Dense data row | `h-11 px-3 tabular-nums border-b border-gray-200`      | Tables/lists      |

## Anti-Patterns to Avoid

- [Specific things NOT to do for this design]

## Complexity Guardrails

Keep implementation simple. Flag these during code review:

- Wrapper divs that add no styling, semantics, or layout purpose
- More than 3-4 levels of nesting for simple content
- Cards within cards (use spacing and dividers instead)
- More than 5 distinct font sizes (muddy hierarchy)
- More than 3 distinct colors plus neutrals (visual noise)
- Elements with 15+ Tailwind classes (simplify or extract)
- Arbitrary spacing values (p-[13px]) instead of scale values
- Decorative elements that don't aid comprehension

## Interactive States

Every interactive element must address all 8 states:
| State | Requirement |
|-------|-------------|
| Default | Base styling |
| Hover | Subtle feedback (gated to `hover:hover` for touch) |
| Focus | Visible ring for keyboard (`focus-visible:ring-2`) |
| Active | Press feedback (`active:scale-[0.97]`) |
| Disabled | Reduced opacity, no pointer events |
| Loading | Spinner or skeleton (`aria-busy`) |
| Error | Red border + message (`aria-invalid`) |
| Success | Confirmation feedback |

## Contrast Requirements

- Body text: 4.5:1 against background
- Large text (≥18px bold, ≥24px): 3:1
- UI components (borders, icons): 3:1
- No pure black on pure white
```

---

## Phase 6.5: Critique the Draft

Before handoff, critique the draft like a design lead reviewing a first pass. Do this even if the wireframe and change spec already look coherent.

### Composition

- Does the layout have rhythm, or is every block the same weight and spacing?
- Are proportions saying something intentional about priority?
- Is there a clear focal point for the primary task?

### Craft

- Is hierarchy carried by weight, spacing, and contrast, not size alone?
- Do surfaces whisper structure without relying on harsh lines?
- Are interactive elements visibly alive across hover, focus, and press?

### Content

- Do labels, examples, and sample data tell one coherent product story?
- Would a real user in this product domain recognize this as plausible?

### Structure

- Are there any “looks right but held together with tape” decisions in the planned implementation?
- Does the UI system snapshot actually match the wireframe and change spec, or is it generic filler?
- Could `ui-builder` implement this cleanly with Tailwind tokens/utilities, or did the spec drift into generic CSS language?

If any answer is weak, revise the design doc before proceeding. Do not hand off a “correct enough” draft when the weakness is already visible in the spec.

---

## Phase 7: Verify Against Checklist

**Run the Design Review Checklist from frontend-design.md:**

### Red Flags (must be zero)

- [ ] Uses default system fonts
- [ ] Purple-to-blue gradient present
- [ ] White background + gray cards throughout
- [ ] `uppercase` + wide tracking eyebrow above section headings (only allowed on monospace eyebrows, sparingly)
- [ ] Could be mistaken for generic AI output

### Green Flags (should have most)

- [ ] Clear aesthetic direction documented
- [ ] Typography is deliberate
- [ ] At least one memorable element
- [ ] Layout has unexpected decisions
- [ ] UI system snapshot is specific enough to keep buttons/cards/inputs consistent
- [ ] Complexity guardrails defined (max nesting, class budget)
- [ ] All 8 interactive states specified
- [ ] Contrast requirements met (4.5:1 body, 3:1 large/UI)

### If Marketing Mode, also check:

- [ ] **Red Flag:** Cookie-cutter hero → features → testimonials → CTA layout
- [ ] **Red Flag:** No clear narrative structure
- [ ] **Green Flag:** Section rhythm creates breathing room
- [ ] **Green Flag:** Would pass the "screenshot test" — distinctive in a grid of competitors

### If App UI Mode, also check:

- [ ] **Red Flag:** No empty state designed
- [ ] **Red Flag:** Generic admin template feel
- [ ] **Red Flag:** Fails the swap test — choices are defaults, not decisions (see app-ui.md)
- [ ] **Green Flag:** Could use this for 8 hours without visual fatigue
- [ ] **Green Flag:** All critical states designed (empty, loaded, error)

**If any Red Flags are present, revise before proceeding.**

---

## Phase 8: Hand Off

**Use the AskUserQuestion interaction pattern:**

```
Question: "Design documented. What's next?"
Header: "Next step"
Options:
  1. "Create detailed plan" (Recommended) — Run /arc:detail for task breakdown
  2. "Save and stop" — Return to this later
```

**IMPORTANT: Do NOT automatically invoke other skills.**

- **If option 1:** Tell user: "Design saved. Run `/arc:detail` to create implementation tasks."
- **If option 2:** Tell user: "Design saved to `docs/arc/specs/design-[name].md`. Return anytime."

---

## During Implementation (Reference for /arc:implement)

When implementing this design (via /arc:implement), use Chrome MCP continuously when available. Outside Claude Code, prefer `agent-browser`, then Playwright.

### After Every Significant Change

```
mcp__claude-in-chrome__computer action=screenshot
```

### Check Responsive Behavior

```
mcp__claude-in-chrome__resize_window width=375 height=812  # Mobile
mcp__claude-in-chrome__computer action=screenshot
mcp__claude-in-chrome__resize_window width=1440 height=900 # Desktop
mcp__claude-in-chrome__computer action=screenshot
```

### Verify Against Design Doc

- Does the typography match what was specified?
- Are the colors exactly as documented?
- Does spacing feel consistent with the system?
- Is the memorable element actually memorable?

**Never commit UI code without visually verifying it looks correct.**

---

## Anti-Patterns (Quick Reference)

From `frontend-design.md`:

**🚫 Never use sparkles/stars to denote AI features.** Overused, meaningless, dated.

**🚫 Never propose conceptual themes with metaphors.** No "Direction: Darkroom / Metaphor: Photo emerging from developer bath". Instead: "Use `bg-gray-950` with `text-gray-50` and restrained `brand-600` accents backed by `@theme` tokens."

**🚫 Never use these:**

- Roboto/Arial/system-ui defaults
- Purple-to-blue gradients
- White backgrounds with gray cards
- Rounded corners on everything
- Mixed icon styles
- `uppercase` + `tracking-wide`/`tracking-widest` eyebrows on sans/serif fonts. Reserve uppercase eyebrows for **monospace only**, and even then use them sparingly — one per page, not above every heading. See `rules/interface/typography.md`.

---

<arc_log>
**After completing this skill, append to the activity log.**
See: `references/arc-log.md`

Entry: `/arc:design — [Component/page] design ([aesthetic direction])`
</arc_log>

<success_criteria>
Design is complete when:

- [ ] Design mode identified (marketing or app UI)
- [ ] All mandatory references were loaded and applied (including mode-specific reference)
- [ ] Current UI was screenshotted (if redesigning)
- [ ] Aesthetic direction established with SPECIFIC values
- [ ] Typography selected from recommended fonts
- [ ] Color palette defined as Tailwind v4 `@theme` tokens in OKLCH
- [ ] Spacing system documented
- [ ] UI system snapshot documented with reusable patterns
- [ ] Wireframes created and approved
- [ ] Design document saved to docs/arc/specs/
- [ ] Critique pass completed and revisions applied
- [ ] Red flag checklist passed (zero red flags)
- [ ] Progress journal updated
      </success_criteria>

## Interop

- Produces design doc consumed by **/arc:implement**
- Reads/creates **docs/design-context.md** for persistent project-wide aesthetic decisions and reusable UI patterns
- Can invoke **web-design-guidelines** skill for compliance review (if available)
- Can invoke **vercel-composition-patterns** skill for component architecture review (if available)
- Uses **WireText MCP** for low-fidelity wireframes when available
- Uses **Chrome MCP** (`mcp__claude-in-chrome__*`) as the preferred rendered-page capture path in Claude Code
- Uses **agent-browser** as the preferred browser fallback outside Claude Code
- Uses **WebFetch** to research design inspiration from Siteinspire and Mobbin
- References feed into implementation to maintain design fidelity

### Related Skills

## Polish Workflow

Use this when the request is to clean up UI code after implementation rather than create new visual direction.

### P.1: Scan Current State

- Identify large components that should be split
- Identify repeated shells, heading groups, buttons, and form controls
- Identify components that bake in margins instead of accepting layout from the caller
- Search for existing shared components before proposing new ones

### P.2: Extract Components

- Break large page components into smaller reusable pieces
- Consolidate duplicated form controls and repeated section wrappers
- Ensure every reusable component accepts `className`

### P.3: Clean Tailwind Classes

- Verify `npx @tailwindcss/cli canonicalize --help`
- If available, canonicalize repeated or messy class strings
- If unavailable, clean manually using `tailwind-authoring.md`

### P.4: Verify

- No broken imports
- No duplicate component names
- Tests and lint still pass

## Progress Updates

During longer design sessions, post a one-line status update before each major phase so the user can follow the flow.
