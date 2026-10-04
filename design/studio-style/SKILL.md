---
name: studio-style
description: Generate a 1-pager style foundation prompt for AI Studio — hero, typography section, and card grid only. Establishes the visual language for any subsequent development (dashboards, e-readers, webpages, etc.) through three exemplary sections that showcase pattern, type, color, motion, and interaction decisions.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep
---

Generate an AI Studio style foundation prompt for: $ARGUMENTS

$ARGUMENTS should include:
- What domain or direction this style will serve (e.g., "a scholarly thought-leader platform", "a fintech product suite", "a wellness app ecosystem", "a dark mode developer tool")
- Optionally: mood/vibe hints ("warm and bookish", "bold and techy", "luxury minimal", "brutalist editorial")
- Optionally: a reference image directive — if the user provides a reference image, include a Reference Image Directive section at the top
- Empty — ask the user what visual direction they want to establish

## Purpose

This skill produces a **style foundation prompt** — a focused 1-pager for Google AI Studio Build mode (or any generative UI tool) that builds exactly **three sections**:

1. **A hero section** — establishes spatial hierarchy, color gravity, typography scale, and the emotional first impression
2. **A typography-driven longform section** — establishes reading rhythm, prose styling, heading hierarchy, pull-quote treatment, and content density
3. **A card grid section** — establishes component patterns, hover/interaction language, information density, and compositional rhythm

That's it. Three sections. No navigation, no footer, no CTAs beyond what lives naturally inside these three. The goal is not a complete page — it's a **style specimen** that makes the design language unmistakably clear. A developer or designer should be able to look at the output and say: "I know exactly how to build the next 20 sections in this language."

**This is the style-first complement to `/studio-design`** — that skill designs a complete page; this skill establishes the visual vocabulary that a complete page would use.

**The three sections must be exemplary.** They are not placeholders. They are the reference implementation. Every decision — type pairing, spacing rhythm, color weight, hover behavior, card anatomy, text hierarchy — should be considered and intentional because it will be replicated across everything built afterward.

## Elicitation — Before Generating

If the user's request is vague, ask **up to 2 targeted questions**:

1. **What world does this live in?** — Is this for a content platform, a SaaS tool, a creative portfolio, an educational experience, an e-commerce storefront? The domain shapes every decision.
2. **What's the temperature?** — Warm/cool, dense/spacious, serious/playful, light/dark?

Do NOT ask both if the request already provides enough context. If the user gives a clear brief, skip straight to generation.

## The 5-Dimension Framework (Applied to Three Sections)

Use the same AntiGravity 5-dimension framework as `/studio-design`, but applied with surgical focus to just three sections. Every dimension must be visible and exemplary in the output.

### Dimension 1: Pattern & Layout (The Skeleton)

**Section 1 — Hero:**
Choose a hero variant that best establishes the spatial language. Options:
- Cinematic (100vh, dramatic, layered entrance)
- Two-Column (copy + visual, balanced tension)
- Split (50/50, strong horizontal rhythm)
- Minimal (text-only, typographic authority)
- Asymmetric (40/60, dynamic composition)
- Card Overlay (full-bleed + floating element)

The hero sets the spatial grammar — margin scale, max-width behavior, vertical rhythm unit, and alignment philosophy. Whatever choices are made here become the law for everything after.

**Section 2 — Typography / Longform:**
A prose-driven section that reads like the opening of an essay, a product manifesto, or an editorial feature. Must include:
- A section heading (H2) that demonstrates heading weight and spacing
- At least 2-3 paragraphs of body text that demonstrate reading line-length, paragraph spacing, and font personality
- A pull-quote or blockquote that demonstrates emphasis treatment
- Optionally: a subheading (H3) to show heading hierarchy
- Optionally: a list or detail element to show secondary content patterns

This section proves the type system works for sustained reading. It's the hardest test — if the typography is beautiful here, it'll be beautiful everywhere.

**Section 3 — Card Grid:**
A grid of 3-4 cards that establishes the component vocabulary. Each card must demonstrate:
- Content hierarchy within a bounded container (image/icon, title, description, metadata, action)
- Surface treatment (background, border, shadow, radius)
- Information density decisions
- Hover/interaction behavior

The grid also establishes responsive column behavior and gap rhythm.

### Dimension 2: Style & Aesthetic (The Skin)

Draw from the style vocabulary (same 20+ styles as `/studio-design`):
Glassmorphism, Aurora UI, Soft UI, Linear/Vercel, Bento Grid, Liquid Glass, Brutalism, Y2K Revival, Claymorphism, Gradient Mesh, Minimalist Luxury, Cyberpunk, Organic/Biomorphic, Editorial, Scandinavian Minimal, Art Deco, Hand-Drawn/Sketch, Retro Terminal, Vaporwave, Swiss/International, Warm Academic.

Don't just name the style — **describe what the three sections feel like** in that style. The hero, the prose section, and the card grid should each demonstrate different facets of the same aesthetic DNA.

### Dimension 3: Color & Theme (The Palette)

Direct color through mood (same palette vocabulary as `/studio-design`). But here, be explicit about how color flows across the three sections:
- How does the hero use color? (dominant surface, text treatment, accent placement)
- How does the typography section use color? (background warmth, text weight, quote treatment)
- How do the cards use color? (surface vs. background contrast, hover state color shifts, metadata muting)

The three sections together should demonstrate the full 60-30-10 distribution.

### Dimension 4: Typography (The Voice)

This is the most critical dimension for this skill. The typography section exists specifically to prove the type system. Be detailed about:
- Display/headline personality (the hero heading and section heading)
- Body text personality (the longform prose)
- Supporting text (card descriptions, metadata, captions)
- Emphasis treatments (bold, italic, pull-quotes, blockquotes)
- Scale relationship between the three sections

### Dimension 5: Animation & Interaction (The Soul)

Each section demonstrates a different facet of the motion language:
- **Hero:** Entrance choreography — how do elements build on load? What's the sequence? What's the timing?
- **Typography section:** Scroll reveal — how does content enter as you scroll? Is it a gentle fade? A slide? Do paragraphs arrive together or in sequence?
- **Card grid:** Interaction design — what happens on hover? On focus? How do cards enter the viewport? Do they stagger?

These three interaction patterns — entrance, scroll-reveal, and hover — form the motion vocabulary for everything built afterward.

## Anti-Patterns — Always Include

Select relevant anti-patterns from:

**Design:**
- No more than 3 primary colors
- No more than 2 font families
- No inconsistent spacing (use an 8px grid)
- No pure black on pure white
- No low-contrast grey text

**UX:**
- No hover-dependent interactions on mobile
- Minimum 44x44px tap targets
- No layout shifts on load

**Content:**
- No lorem ipsum — use realistic placeholder content that matches the domain
- No walls of text without hierarchy
- Icons must have labels or be self-evident

**Accessibility:**
- WCAG AA compliance minimum
- Keyboard navigation must work
- Focus states must be visible
- Color alone must not convey information

## Responsive Expectations

All three sections must demonstrate responsive behavior:
- **Desktop (1440px+):** Full expression of the design language
- **Tablet (768px):** Graceful adaptation — column collapse, touch-friendly targets
- **Mobile (375px):** Single column, still beautiful, still exemplary
- Typography scales fluidly
- Cards reflow naturally

## The "Build From Here" Test

The generated prompt must pass this test: **Could a developer look at the three sections built from this prompt and confidently build any of the following without asking further design questions?**

- A dashboard with sidebar and widgets
- An article reading experience
- A course detail page
- A settings/admin panel
- A product listing page
- A pricing page

If the three sections establish type scale, color system, spacing rhythm, component anatomy, interaction patterns, and responsive behavior clearly enough — the answer should be yes.

## Output Format

Generate a single markdown document:

```markdown
# AI Studio Style Foundation: [Name / Direction]

## What This Establishes
[1-2 sentences: what domain, what mood, what this style foundation will be used to build]

## The Feeling
[2-3 sentences: what should it FEEL like to look at and interact with these three sections? Emotional, evocative, specific.]

---

## Section 1: Hero
[Hero variant, spatial decisions, content direction, entrance choreography. Be specific about structure, evocative about style.]

## Section 2: Typography & Prose
[Detailed prose section spec — heading hierarchy, body text personality, pull-quote treatment, reading rhythm. This is where the type system is proven.]

## Section 3: Card Grid
[Card anatomy, grid layout, surface treatment, hover behavior, information hierarchy. This is where the component language is established.]

---

## Visual Style
[Style direction with experiential language]

## Color Direction
[Color mood applied across all three sections]

## Typography System
[Type personality, scale, pairing — more detailed than studio-design because this is the type-proving skill]

## Motion & Interaction
[Three-part motion vocabulary: entrance (hero), scroll-reveal (prose), interaction (cards)]

## What to Avoid
[Selected anti-patterns]

## Responsive Behavior
[How all three sections adapt]

## Building From Here
[2-3 sentences: how a developer should use this style foundation to build subsequent pages and sections. What patterns to replicate, what to extend, what to never break.]

---
*Paste this prompt into AI Studio Build mode. Build only these three sections — nothing else. The result is your style foundation: the visual vocabulary for everything you build next.*
```

Save to: `_docs/studio-designs/[style-slug]-style-foundation.md`

Create the `_docs/studio-designs/` directory if it doesn't exist.

## Generation Rules

1. **Three sections only.** No navigation, no footer, no extra sections. The constraint is the point — these three must carry the entire style language.
2. **Be exemplary, not exhaustive.** Every detail in these three sections will be replicated. Make them worth replicating.
3. **Be evocative, not prescriptive.** Same rule as `/studio-design` — describe experiences, not implementations. No CSS, no HTML, no Tailwind.
4. **Prove the type system.** The typography section is the centerpiece. If the prose doesn't sing, the foundation fails.
5. **Show the interaction vocabulary.** Three different interaction patterns (entrance, scroll, hover) must be clearly described.
6. **Domain-appropriate content.** The placeholder text in all three sections should match the domain the user specified — scholarly text for education, product copy for SaaS, editorial prose for publishing, etc.
7. **Always include anti-patterns.** What NOT to do is as important as what to do.
8. **The "Build From Here" test must pass.** If a developer can't extrapolate a full design system from these three sections, the prompt needs more specificity.
