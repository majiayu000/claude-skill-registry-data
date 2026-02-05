---
name: landing-page-architect
description: Generate content strategy and component recommendations for landing pages. Analyzes implementations to create StoryBrand-structured pages with brand-aligned Shadcn component queries.
---

# Landing Page Architect Skill

Transform product implementations into compelling landing pages with content strategy, visual storytelling structure, and Shadcn component recommendations aligned with the Maslow AI design system.

## When to Use This Skill

Invoke when you need to:
- Create a landing page for a new feature or tool
- Generate marketing copy that tells a coherent story
- Map content sections to appropriate UI components
- Ensure recommendations follow brand guidelines

## Workflow

```
1. Analyze implementation code → Extract value proposition
2. Apply StoryBrand framework → Structure page sections
3. Generate content → Headlines, copy, CTAs for each section
4. Recommend components → Shadcn queries aligned with brand
5. Output strategy → Structured markdown ready for implementation
```

## Input

The implementation you want to create a landing page for. This can be:
- A tool or feature codebase
- A product description
- An API or service

## Output Format

For each landing page, output a structured strategy document:

```markdown
## Landing Page Strategy for [Product Name]

### Value Proposition
[One-liner extracted from analyzing the implementation]

### Target Audience
[Who this product serves]

### Page Sections

#### 1. Hero Section
**Story Element:** Character + Aspiration
**Content:**
- Eyebrow: [Category label]
- Headline: [Main message - use bold/light pattern]
- Subheadline: [Supporting detail]
- Primary CTA: [Action text]
- Secondary CTA: [Alternative action]

**Shadcn Query:** `hero section 2-column asymmetric layout with CTA`
**Anti-patterns Avoided:** [List what NOT to do]
**Brand Alignment:**
- Layout: 2-column grid with visual on right
- Background: var(--silver-bg) #E6EAF3 or var(--dark-blue) #121D35
- Accent line: 3px height, 60px width, tool accent color
- Typography: Manrope 800 for headline
- CTA: #333333 primary button, #6DC4AD accent button

[Continue for all 7 StoryBrand sections...]
```

---

## StoryBrand Framework Reference

Load `frameworks/storybrand.md` for the complete 7-part framework. Key sections:

| # | Section | Story Element | Page Purpose |
|---|---------|--------------|--------------|
| 1 | Hero | Character + Aspiration | Hook with transformation promise |
| 2 | Stakes | The Problem | Create urgency with pain points |
| 3 | Guide | Authority + Empathy | Establish credibility |
| 4 | Plan | The Process | Show clear path (3 steps max) |
| 5 | CTA | Call to Action | Direct + transitional actions |
| 6 | Success | Transformation | Paint the outcome picture |
| 7 | Failure | What's at Risk | Gentle urgency reminder |

---

## Design Integration (Critical)

### Anti-Patterns to AVOID

These patterns signal "generic AI output" - never recommend them:

| Pattern | Why It's Bad | Alternative |
|---------|-------------|-------------|
| Glass-morphism | Overused, lacks character | Solid surfaces with subtle shadows |
| Fade-up animations on everything | Lazy, predictable | Staggered reveals on key elements only |
| Purple/blue gradients (#a855f7, #8b5cf6) | Screams "AI generated" | Brand purple #401877 or tool accent |
| Centered hero + two buttons | Generic, forgettable | Asymmetric 2-column with visual |
| Heroicons on every card | Template-like | Minimal icons, let content speak |
| Emoji icons (👁️, 💡, 🔍, etc.) | AI Slop, unprofessional | Shadcn icons from @lucide-animated or @animate-ui |
| Inter, Arial, Roboto fonts | No character | Manrope (headings), Graphik (body) |
| Rounded corners everywhere | Soft, uncommitted | Sharp corners with intentional radius |

Load `design-integration/anti-patterns.md` for the complete list.

### Maslow Brand Tokens

Always align recommendations with these tokens:

**Primary Colors:**
- Teal #6DC4AD - Primary CTA, Technology
- Pink #EE7BB3 - Strategy, accents
- Purple #401877 - Premium, hero moments

**Backgrounds:**
- Light mode: #E6EAF3 (silver)
- Dark band: #121D35 (for emphasis sections within light pages)
- Surface: #FFFFFF (cards)

**Typography:**
- Headings: Manrope (weights 600-800)
- Body: Graphik (weight 400)
- Code: JetBrains Mono

**Signature Elements:**
- Accent lines: 3px height, brand colors
- Selection state: #EBF7F4 background + #6DC4AD left border
- Focus rings: 2px #6DC4AD outline

Load `design-integration/maslow-tokens.md` for the complete token reference.

---

## Component Query Templates

When recommending Shadcn components, use semantic queries:

### Hero Sections
```
hero section 2-column asymmetric with headline and CTA
hero with gradient text and email capture
hero minimal with single CTA centered
```

### Feature/Stakes Sections
```
feature cards 3-column grid with icons
bento grid layout for features
stats section with large numbers
```

### Social Proof
```
testimonial carousel with avatars
logo cloud with grayscale hover
quote block with attribution
```

### Process/Plan Sections
```
steps section with numbered cards
timeline vertical with icons
process flow horizontal
```

### CTA Sections
```
CTA banner with heading and button
newsletter signup with input
pricing cards comparison
```

### Icons (NEVER use emojis)
```
icon search magnifying glass
icon chart bar analytics
icon lightbulb idea
icon target goal
icon flask experiment
icon check circle success
icon alert triangle warning
```
Query registries: `@lucide-animated` (367 icons), `@animate-ui` (518 icons)

Load `component-patterns/section-types.md` for comprehensive query templates per section type.

---

## Example Output

For a tool called "Hypothesis" (scientific reasoning):

```markdown
## Landing Page Strategy for Hypothesis Tool

### Value Proposition
Guide complex problem-solving through formal scientific method with structured hypothesis testing.

### Target Audience
Developers, researchers, and analysts who need systematic approaches to testing ideas.

### Page Sections

#### 1. Hero Section
**Story Element:** Character + Aspiration
**Content:**
- Eyebrow: THINK-MCP TOOLS
- Headline: **Test ideas** with scientific rigor
- Subheadline: Apply formal hypothesis testing to any problem. Design experiments, predict outcomes, and iterate based on evidence.
- Primary CTA: Try Hypothesis
- Secondary CTA: See Example

**Shadcn Query:** `hero section 2-column with code preview`
**Anti-patterns Avoided:** ❌ Generic centered layout, ❌ Purple gradient
**Brand Alignment:**
- Background: #E6EAF3 (silver-bg)
- Accent: Tool-specific color (e.g., #469DBB blue for scientific tools)
- Accent line: 3px, 60px width, animated grow on load
- Typography: Manrope 800 headline, Manrope 300 subheadline

#### 2. Stakes Section
**Story Element:** The Problem
**Content:**
- Headline: Assumptions kill products
- Points:
  1. Gut feelings aren't evidence
  2. Confirmation bias blinds teams
  3. Expensive pivots from untested ideas

**Shadcn Query:** `feature cards 3-column with warning icons`
**Anti-patterns Avoided:** ❌ Glass cards, ❌ Fade-up on each card
**Brand Alignment:**
- Background: #FFFFFF (surface)
- Card borders: 1px #D0D5E0, hover reveals 3px left accent
- Icon style: Minimal line icons, not filled Heroicons

[... continues for remaining sections]
```

---

## Checklist Before Output

Before finalizing recommendations, verify:

- [ ] Every section maps to a StoryBrand element
- [ ] No anti-patterns in component recommendations
- [ ] **No emoji icons** - use @lucide-animated or @animate-ui components only
- [ ] All colors reference Maslow brand tokens
- [ ] Typography uses Manrope/Graphik only
- [ ] CTAs use correct button hierarchy (#333333 primary, #6DC4AD accent)
- [ ] Dark band sections use #121D35 (not arbitrary dark colors)
- [ ] Component queries are semantic, not specific component names
