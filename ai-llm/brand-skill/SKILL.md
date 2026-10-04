---
name: Brand
description: Complete brand development system with emotive foundation. Triggers on requests for brand identity, logos, visual systems, or design guidelines. Creates distinctive, anti-AI-slop design from strategy through delivery.
---

# Brand Skill

Build complete brand identities that are coherent, distinctive, and impossible to confuse with generic AI output.

## What Makes This Different

**Anti-AI-Slop Focus:** This process creates brands that are:
- **Emotionally grounded** — Every visual choice connects to human meaning
- **Systematically distinctive** — Coherent systems, not random "modern" aesthetics
- **Intentionally crafted** — Expert-level refinement, not first-draft defaults

**The secret:** Start with **emotive narrative** before any visual work. This creates deep LLM memory that prevents generic drift.

---

## Structure

```
brand-skill/
├── SKILL.md                      # Overview and routing (you are here)
├── TOOLS-REQUIRED.md             # Prerequisites checklist
├── ADDENDUM-4-WEB-PRESENCE.md    # Convergence theory (why LLMs revert to mean)
├── SKILL-AUDIT.md                # Gap analysis from AutonoLabs build
├── Workflows/
│   ├── 00-EmotiveNarrative.md    # Soul of the brand
│   ├── 01-Discovery.md            # Strategy and positioning
│   ├── 02-VisualDirection.md      # Reference exploration
│   ├── 03-MarkDevelopment.md      # Logo via tracing or hand-coding
│   ├── 04-Wordmark.md             # Typography and lockups
│   ├── 05-DesignSystem.md         # Complete system (web + iOS)
│   ├── 05A-CompositionIdentity.md # Evolutionary diverge/kill/mutate process
│   ├── 06-DesignMdCreation.md     # Consolidate to DESIGN.md
│   └── 07-Packaging.md            # Final delivery
├── Templates/
│   ├── DESIGN-template.md         # Comprehensive DESIGN.md template
│   ├── philosophy-template.md
│   ├── visual-philosophy-template.md
│   ├── design-guidelines-template.md
│   └── readme-template.md
└── Examples/
    └── sorted-brand-kit/          # Real-world example (Sorted.fund)
```

---

## Getting Started

**Before anything else:**
1. Read `Workflows/00-Orchestrator.md` — controls phase progression and state tracking
2. Read `TOOLS-REQUIRED.md` — verify prerequisites
3. Create `.brand-progress.md` in the project directory using the checklist from `00-Orchestrator.md`. This is the living progress tracker — update it at each gate check.

## Triggers

- "Build a brand for [project]"
- "Create brand guidelines"
- "Design a logo and visual system"
- "I need a complete identity that doesn't look like AI slop"
- "Help me create a design system with iOS and web specs"

---

## The Process (8 Phases)

### Phase 0: Emotive Narrative ⭐ NEW
**Create the soul before the visuals**

**Output:** Beautiful emotive narrative in 4-6 paragraphs
- The human moment (why this matters)
- The transformation (what becomes possible)
- The ethos (values and principles)
- The personality (how it moves through the world)
- The north star (guiding light for decisions)

**Why first:** This becomes the emotional context that every subsequent phase references. It prevents generic "clean and modern" drift by grounding all choices in human meaning.

**Time:** 20-30 minutes

---

### Phase 1: Discovery
**Establish strategic foundation**

**Output:** Brand positioning, voice guidelines
- Positioning statement
- Core metaphor
- Brand personality traits
- Voice and tone principles

**Context-aware:** If you have codebase access, read project files first and draft a positioning hypothesis. Don't open with a questionnaire.

**Time:** 15-20 minutes

---

### Phase 2: Visual Direction
**Generate reference images to find aesthetic territory**

**Output:** Reference images (PNG) exploring directions
- 3-4 prompts exploring different interpretations
- User picks direction(s)
- Generate refinements if needed

**Optional:** Can skip and go straight to SVG iteration (Phase 3)

**Time:** 10-15 minutes

---

### Phase 3: Mark Development
**Develop logo via tracing or hand-coded SVG**

**Output:** `[brand]-mark-final.svg`, favicon PNG
- **Primary path:** Generate reference → trace to SVG (vtracer) → refine
- **Secondary path:** Hand-code simple geometric marks
- Render-verify loop after every change (rsvg-convert)
- Iteration limit: 5-8 rounds, then pivot approach
- Test at favicon sizes (32px, 16px)

**Time:** 20-60 minutes

---

### Phase 4: Wordmark
**Pair the mark with typography**

**Output:** `[brand]-wordmark-final.svg`, variants
- Horizontal, stacked, text-only lockups
- Refine alignment through iteration
- Test in real-world contexts

**Time:** 30-45 minutes

---

### Phase 5: Design System ⭐ UPDATED
**Define complete visual language for web AND iOS**

**Output:** `[brand]-design-guidelines.md`
- Colors (web CSS + iOS Swift)
- Typography (web + iOS with Dynamic Type)
- Spacing (unified 8pt/px base)
- Components (web + iOS implementations)
- Motion and animation principles
- Platform-specific considerations

**Includes iOS specifications:**
- SwiftUI components
- Asset Catalog setup
- Dynamic Type support
- Safe area handling
- Touch target guidelines

**Time:** 30-60 minutes

---

### Phase 5.5: Composition & Visual Identity ⭐ NEW
**Define how this brand uniquely occupies space**

**Output:** Compositional framework + 3-5 named structural variants deployed for comparison

This is where the evolutionary process lives. Tokens (Phase 5) define materials; composition defines what to build with them. Without this phase, every brand converges to the same layout regardless of tokens.

**Process:**
1. Create anti-reference board (sites/patterns to explicitly avoid)
2. Generate 3-5 structurally different page variants — each fighting a named convention
3. Deploy to comparison page for user to evaluate visually
4. User kills variants (no blending). Surviving direction gets mutated.
5. Repeat until the composition is distinctive under the blur test (at 20% visibility, the layout silhouette is distinguishable from the anti-references)

**Critical:** The user's reference images and gut reactions drive this phase entirely. The LLM generates; the user selects. See `05A-CompositionIdentity.md` for full process.

**Time:** 60-120 minutes (most important phase for distinctiveness)

---

### Phase 6: DESIGN.md Creation
**Consolidate everything into one master reference**

**Output:** `DESIGN.md` (comprehensive, living document)

**Contains:**
1. Emotive Narrative (from Phase 0)
2. Strategic Foundation (from Phase 1)
3. Visual Philosophy (from Phase 1/2)
4. Logo System (from Phase 3/4)
5. Design Tokens (colors, type, spacing — web + iOS)
6. Components (implementation for web + iOS)
7. Implementation Guidelines (platform-specific specs)
8. Anti-AI-Slop Principles (quality validation)

**Why critical:** Single source of truth. Any LLM can read DESIGN.md and understand the complete brand — preventing generic drift forever.

**Time:** 20-30 minutes

---

### Phase 7: Packaging
**Collect assets for handoff**

**Output:** `[brand]-brand-kit/` folder (or .zip)
- All final assets organized
- Quick-start README
- DESIGN.md as master reference

**Time:** 10-15 minutes

---

## Total Time Investment

- **Fast track:** 3-4 hours (clear direction, minimal iteration)
- **Full process:** 5-7 hours (exploration and refinement)
- **Complex brands:** 8+ hours (multiple concepts, extensive iteration)

---

## Key Outputs

### During Process
- `[brand]-emotive-narrative.md` (Phase 0)
- `[brand]-philosophy.md` (Phase 1)
- `[brand]-visual-philosophy.md` (Phase 1/2)
- Reference images (Phase 2)
- `[brand]-mark-final.svg` + favicon (Phase 3)
- `[brand]-wordmark-*.svg` (Phase 4)
- `[brand]-design-guidelines.md` (Phase 5)

### Final Deliverable
- **`DESIGN.md`** — The single source of truth (Phase 6)
- **Brand kit folder** — All assets packaged (Phase 7)

---

## On LLM Design Limitations — Read This First

**Be honest with the user about this at the start of every brand engagement.**

This skill produces excellent *ingredients* — emotive narratives, color palettes, typography systems, design tokens. What it cannot produce on its own is a distinctive *composition* — how those ingredients come together into something that doesn't look like every other well-designed page.

### Why this happens

An LLM generates output by predicting the most probable next token. This is a statistical averaging operation. The output doesn't drift toward the average — it starts there, because the average is what the mechanism is optimized to find. "Good design" in the training data is overwhelmingly polished, balanced, finished, conventional. Every brand that asks for "good" gets the same good.

Specifically:

- **The LLM can't see what it's producing.** It writes HTML/CSS/SVG as text tokens with no visual feedback loop. It's painting blindfolded.
- **It optimizes for coherence.** Deliberately unfinished, misaligned, or rule-breaking design goes against its training weights. It will "fix" anything that looks like an error, even when the error was the point.
- **It can't feel tension.** Great design creates productive discomfort. The LLM can't calibrate this — it either produces something comfortable (convergent) or breaks things randomly.
- **It doesn't have taste.** Taste is judgment that isn't reducible to rules. The LLM approximates taste with heuristics, and heuristics are generalizations, and generalizations converge to the mean.

### What this means for the process

**The user's direction, references, and gut reactions are not optional — they ARE the design.** The LLM is the hand. The user is the eye.

Prescribing techniques doesn't help: "be bold" converges to the average of bold. "Break the grid" converges to the average of grid-breaking. Even "surprise me" converges to the average of surprise. Any instruction specific enough to produce a distinctive result becomes a new center of convergence.

**The only escape is process, not instruction:**
1. **Diverge** — Generate 3-5 structurally different variants (not color swaps — different spatial logic). Each must name what design convention it's "fighting."
2. **Kill** — User makes binary decisions. Alive or dead. No blending — blending is averaging.
3. **Mutate** — Within the surviving direction, introduce deliberate named "breaks" (violations of convention).
4. **Repeat** — Each cycle moves further from the center. The user's selections are the creative act.

This evolutionary process is encoded in Phase 5.5 (Composition). See also: `ADDENDUM-4-WEB-PRESENCE.md` for the full theoretical framework.

### What this skill still prevents

The above doesn't mean the brand phases are pointless. The emotive narrative, philosophy, and tokens do critical work:

- **Emotive narrative** grounds every choice in meaning (prevents arbitrary decisions)
- **Visual philosophy** defines a specific aesthetic movement (prevents "clean and modern")
- **Systematic tokens** create coherence (prevents random sizing/spacing)
- **DESIGN.md** embeds the philosophy (prevents drift over time)

But tokens alone cannot prevent compositional convergence. The skill produces excellent ingredients. The user + evolutionary process determines the meal.

---

## Guidelines

### On Iteration

Don't aim for perfection on the first try. The process is evolutionary:
- **Diverge** — Generate structurally different options, not variations on a theme
- **Kill** — User picks survivors. Dead means dead. No blending.
- **Mutate** — Push survivors in unexpected directions
- **Repeat** — Each cycle gets more distinctive

Version 15 is usually much better than version 3 — but only if the iterations are driven by human selection pressure, not by the LLM refining toward its own center.

### On User Input

You bring expertise; they bring taste. Present options with your reasoning, but let them choose. Use `AskUserQuestion` when you genuinely need direction, not for validation.

### On Emotive Foundation

**Phase 0 is not optional.** Skipping it leads to soulless design. The narrative creates:
- Deep LLM memory (prevents generic drift)
- Decision framework (test choices against the narrative)
- Emotional coherence (visual system expresses the story)

### On Testing

Logos exist at multiple sizes: hero (200px+), app icon (64px), favicon (32px, 16px). Test all of them. If it falls apart small, simplify.

### On Color

Dark backgrounds should have warmth — pure #000 feels lifeless. Functional colors (green for success, red for error) carry meaning; don't use them decoratively.

### On Platform Specificity

**Web and iOS should feel like "the same brand" but native to their platforms:**
- Web can be more expressive (gradients, shadows)
- iOS should use system conventions (SF Pro, native navigation)
- Color palette and spacing rhythm stay identical
- Components recognizably "the same" but platform-appropriate

### On Typography and Lockup Development

**Font pairing requires methodology, not instinct.** When selecting body fonts to pair with display fonts:
- Research what similar brands actually use (fintech, technical, luxury contexts differ dramatically)
- Use professional pairing databases to understand proven combinations
- Apply x-height analysis - similar x-heights create cohesion, contrast creates hierarchy
- Present rationale with each option: explain *why* this pairing works, not just *what* it is
- For technical/institutional brands, sans-serif body text is non-negotiable - screen readability trumps editorial styling

**On lockup refinement:** Show 3-4 spacing and sizing variants before finalizing. Text should be 60-75% of mark height for optical balance. Gap between mark and text: tight spacing (0.25x mark height) creates density, loose spacing (0.75x) creates breathing room. Let the brand philosophy guide which feels right.

**On technical execution:** Test typography rendering early - SVG text, web fonts, and export formats each have quirks that break differently. Validate before presenting to catch issues the user shouldn't see. If decorative elements are part of the concept, position them at natural boundaries (end of word, underlines, separate marks) rather than trying to align them with specific glyph features.

### On Quality

Avoid generic patterns: purple-blue gradients, overly rounded shapes, meaningless geometric decorations. Create something distinctive that the brand can own.

**Remember:** Generic is easy. Distinctive takes intention.

---

## Dependencies

**See `TOOLS-REQUIRED.md` for the complete checklist with installation commands.**

### Required

- **Node.js** — Required for SVGO optimization
- **SVGO** — SVG optimization (`npx svgo@latest` — no global install needed)
- **Browser** — SVG/HTML preview

### Recommended

- **rsvg-convert** (librsvg) — SVG→PNG rendering for the render-verify loop (fallback: browser or `qlmanage` on macOS)
- **vtracer** — PNG→SVG tracing (primary path for Phase 3 mark development)
- **potrace** — Bitmap tracing (simpler alternative to vtracer)

### Fallback

- **[freeconvert.com/png-to-svg](https://www.freeconvert.com/png-to-svg)** — Browser-based PNG→SVG tracing when local tools aren't available or aren't producing faithful results. Larger file sizes than vtracer — that's fine, fidelity to the reference matters more.
- **qlmanage** (macOS) — Built-in SVG rendering for visual verification

### Image Generation (Optional)

Phase 2 can use AI image generation for reference exploration. Requires API keys — see `TOOLS-REQUIRED.md` for setup.

1. **Any text-to-image tool** — Gemini, DALL-E, Midjourney, Flux, etc.
2. **Manual references** — User provides mood board images or links
3. **Skip to SVG** — Go directly to Phase 3 with more initial variations (8-10)

**Phases 0-1 work without any image generation.** You only need API keys when you reach Phase 2 Mode A.

### Fonts

Selected in Phase 4 based on brand personality. No defaults prescribed.

---

## Workflow Files

Each phase has detailed instructions in `Workflows/`:

- `00-EmotiveNarrative.md` — Create the soul and emotional foundation ⭐ NEW
- `01-Discovery.md` — Full discovery process with context-aware mode
- `02-VisualDirection.md` — Reference image generation guide
- `03-MarkDevelopment.md` — SVG iteration techniques
- `04-Wordmark.md` — Typography pairing and alignment
- `05-DesignSystem.md` — Token and component definitions (web + iOS)
- `05A-CompositionIdentity.md` — How the brand occupies space (evolutionary process) ⭐ NEW
- `06-DesignMdCreation.md` — Consolidate to master DESIGN.md
- `07-Packaging.md` — Asset collection and handoff

Read the relevant workflow file when executing each phase.

---

## The DESIGN.md Advantage

**Why this matters:**

Traditional brand systems:
- Scattered across multiple files
- Knowledge lives in people's heads
- Design drift happens over time
- Generic patterns creep in

**With DESIGN.md:**
- ✅ One file, complete system
- ✅ Any LLM can read and maintain consistency
- ✅ Emotive narrative embedded (prevents generic drift)
- ✅ Platform-specific implementations (web + iOS)
- ✅ Anti-AI-slop validation built in
- ✅ Onboarding is instant
- ✅ Brand stays distinctive forever

**This is the insurance policy against generic design.**

---

## Example Usage

### Starting Fresh

```
"Use the brand-skill to build a complete brand identity for [project].
Start with Phase 0: create the emotive narrative that captures the soul
of what we're building."
```

### Resuming Mid-Process

```
"Continue Phase 3 of the brand process. Here's feedback on v1-v5:
[your feedback]. Create the next iteration batch."
```

### Skipping Phases

```
"I already have a logo. Skip to Phase 5 and create a design system
(web + iOS) that complements this mark: [describe logo]."
```

### Final Consolidation

```
"We've completed Phases 0-5. Now create the master DESIGN.md file
that consolidates everything into one comprehensive reference."
```

---

## Quality Standards

Every brand created with this skill should:

1. **Have emotional depth** (not just visual style)
2. **Be systematically coherent** (not random choices)
3. **Feel distinctive in composition, not just tokens** (different colors on the same layout is not distinctive)
4. **Survive the blur test** (at 20% visibility, the layout silhouette should be recognizable)
5. **Work cross-platform** (web + iOS implementations)
6. **Be implementable** (copy-paste ready code)
7. **Stay consistent** (DESIGN.md prevents token drift; compositional identity prevents layout drift)

**If it could be any "clean and modern" brand with different hex values, we failed. Distinctiveness lives in composition — how the brand occupies space — not in tokens alone.**

---

## Real-World Examples

This skills library was used to create:

1. **Compost.fi** — "Quiet Infrastructure" brand
   - Process documented at: `compost.fi/process.html`
   - ~2,600 API calls from philosophy to production
   - 26 logo iterations, full design system

2. **Sorted.fund** — "Utility Sublime" brand
   - Example included at: `Examples/sorted-brand-kit/`
   - Warm infrastructure aesthetic
   - Dense, functional design language

Both show the full 7-phase process in action, with distinctive results.

---

*Last Updated: February 2026 — Version 3.0*
*Added: LLM design limitations honesty, Phase 5.5 Composition (evolutionary process), bitmap tracing for marks, font exploration, convergence framework*
