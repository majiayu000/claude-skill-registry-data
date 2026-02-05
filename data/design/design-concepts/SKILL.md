---
name: design-concepts
description: Creates conceptual designs that illustrate design strategy and approach. Leverages research insights and design briefs to develop UI concepts, mood boards, and interactive prototypes. Translates strategic direction into visual design explorations that communicate intent and gather feedback.
triggers:
  keywords:
    - "mockup"
    - "wireframe"
    - "concept"
    - "concepts"
    - "mood board"
    - "visual direction"
    - "what should this look like"
    - "design options"
    - "explore designs"
    - "UI design"
    - "prototype"
    - "design exploration"
    - "visual style"
    - "layout options"
    - "design this"
    - "show me designs"
    - "create a design"
    - "design variations"
    - "look and feel"
  contexts:
    - "Have research insights or design brief ready"
    - "Starting visual design for a new feature/product"
    - "Need stakeholder buy-in on design direction"
    - "Exploring multiple approaches before committing"
    - "Major redesign or new product initiative"
    - "Refining a chosen design direction based on feedback"
    - "Need to communicate design intent visually"
  prerequisites:
    - "Research complete OR have clear design brief/requirements"
    - "Know target users and their needs (even if informally)"
    - "Not yet in production specification phase"
  anti_triggers:
    - "Need to understand users first (use design-research)"
    - "Concept already approved, need detailed specs (use design-production)"
    - "Reviewing implemented product (use design-qa)"
    - "Writing code or implementing features"
    - "Need pixel-perfect specifications for developers"
---

# Design - Concepts

This skill guides Claude through creating conceptual designs that bridge research insights and production-ready designs. Concepts communicate design direction, explore visual possibilities, and validate approaches before detailed production work begins.

## Core Methodology

### Purpose of Concept Design
Concept design is NOT final design - it's exploration and communication:
- **Explore possibilities**: Test multiple visual directions quickly
- **Communicate intent**: Show stakeholders what "good" could look like
- **Validate approach**: Get feedback before investing in detailed production
- **Build alignment**: Create shared understanding of design direction

### Concept Design Process
1. **Brief Review**: Understand goals, constraints, research insights
2. **Inspiration & Research**: Gather visual references, identify trends
3. **Ideation**: Sketch multiple directions (divergent thinking)
4. **Initial Concepts**: **ALWAYS develop 3 distinct concepts** for initial exploration (convergent thinking) unless explicitly told otherwise
5. **Presentation**: Create artifacts that tell the story and invite feedback
6. **Refinement** (if needed): Iterate on the chosen direction - refining ONE concept based on feedback

### Why Multiple Concepts? (For Initial Exploration)
Creating 3 concept variations is standard design practice **when initially exploring a product or feature**:
- **Divergent exploration**: Shows different strategic approaches, not just visual variations
- **Better decisions**: Stakeholders choose between meaningful alternatives, not yes/no
- **Reduced bias**: Presenting one concept feels like "approve this" vs. "which solves the problem best?"
- **Safety in numbers**: If one direction has fatal flaw, you have alternatives ready
- **Creative confidence**: Multiple directions show thorough exploration

**When to create 3 concepts vs. 1:**
- ✅ **3 concepts**: First time designing a product/feature, exploring strategic direction, major redesigns
- ✅ **1 concept**: Refining a chosen direction, iterating based on feedback, minor updates to existing designs

**What makes concepts "different"?**
- ❌ Same layout, different colors = NOT different concepts
- ❌ Same approach, different fonts = NOT different concepts
- ✅ Different information architecture = Different concepts
- ✅ Different interaction models = Different concepts
- ✅ Different navigation patterns = Different concepts
- ✅ Different content priorities = Different concepts

### Fidelity Levels
Match fidelity to the question being answered:
- **Low-fi wireframes**: Test layout, hierarchy, flow
- **Mid-fi mockups**: Test visual direction, branding, key interactions
- **High-fi prototypes**: Test detailed interactions, polish, feasibility

## Tool Usage Patterns

### Initial Setup & Brief Review

**Step 1: Gather Context**
```
Questions to ask user:
1. What research/insights should inform this concept?
2. What's the design challenge or goal?
3. Who's the audience for these concepts?
4. Any brand guidelines or design constraints?
5. What fidelity level? (wireframes/mockups/high-fi)
6. Is this initial exploration or refining an existing concept?

**Note**: For **initial concept development** (first time exploring a product/feature), default to creating **3 distinct concept variations** unless user explicitly requests a different number. For **refinement** (iterating on chosen direction), create 1 refined version based on feedback.

Use `view` to read:
- Research artifacts (personas, design principles)
- Existing brand guidelines
- Competitive analysis
- Design briefs or requirements
```

**Step 2: Inspiration Research**
Use web tools to gather current design patterns:
```
web_search: "best [industry] app ui design 2025"
web_search: "[design pattern] examples mobile"
web_fetch: Dribbble, Behance, Awwwards for visual inspiration

Create mood board HTML file documenting:
- Visual directions that align with brand/goals
- Interaction patterns that solve similar problems
- Color palettes (with actual color swatches, not just hex codes)
- Typography samples (rendered at size, not described)
- What works and why (tied to research insights)
- Interactive component examples where relevant
```

### Creating Concepts

**For Wireframes/Low-Fi Concepts:**
Create HTML prototypes with minimal styling:
```html
<!-- Focus on layout, hierarchy, content structure -->
<div style="max-width: 400px; margin: 0 auto; font-family: system-ui;">
  <!-- Use grayscale, simple shapes -->
  <!-- Annotate key decisions -->
</div>
```

**For Visual Mockups/Mid-Hi Fi:**
Create React artifacts with Tailwind CSS:
```jsx
// Use Tailwind's utility classes for rapid styling
// Import design tokens if design system exists
// Focus on key screens, not complete flows
// Include annotations explaining design decisions
```

**For Interactive Prototypes:**
```jsx
// Use React hooks for state management
// Create realistic interactions for key flows
// Use Tailwind for styling
// Add transition/animation for important interactions
// Keep data in memory (no localStorage)
```

### Mood Board Creation

**IMPORTANT: Mood boards MUST be visual HTML files, NOT markdown.**

A mood board is inherently visual - stakeholders need to SEE colors, typography, spacing, and visual examples, not just read about them. Create standalone HTML files that can be opened in a browser.

Mood boards should include:
1. **Color Palette**: Actual color swatches with hex values and usage descriptions
2. **Typography Samples**: Real text at different sizes showing the font in use
3. **Spacing Scale**: Visual representation of spacing units (e.g., 4px, 8px, 16px bars)
4. **Component Examples**: Interactive examples showing hover states, transitions
5. **Inspiration References**: Screenshots or links to tools/sites that inspired the direction
6. **Design Rationale**: Why these choices support user jobs and brand

**Format**: Static HTML file (save as `.html`, NOT `.md`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mood Board - [Project Name]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Inter', -apple-system, sans-serif;
      background: #0a0a0a;
      color: #f3f4f6;
      padding: 60px 40px;
    }
    .color-swatch {
      width: 100%;
      height: 120px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .type-sample {
      margin: 20px 0;
      padding: 20px;
      background: #1a1a1a;
      border-radius: 8px;
    }
    /* Add hover effects, transitions for interactive examples */
  </style>
</head>
<body>
  <h1>Mood Board - [Project Name]</h1>

  <section>
    <h2>Color Palette</h2>
    <div class="color-swatch" style="background: #2563eb;">
      Primary Blue - #2563eb
    </div>
    <!-- More color swatches -->
  </section>

  <section>
    <h2>Typography</h2>
    <div class="type-sample">
      <div style="font-size: 48px; font-weight: 700;">
        Display / 48px / Bold
      </div>
      <p style="font-size: 14px; color: #6b7280;">
        font-size: 48px | font-weight: 700 | line-height: 1.2
      </p>
    </div>
    <!-- More typography samples -->
  </section>

  <section>
    <h2>Component Examples</h2>
    <div class="card-example" style="padding: 20px; background: #1a1a1a; border-radius: 8px; transition: all 200ms;">
      <!-- Interactive component that shows hover effects -->
    </div>
  </section>
</body>
</html>
```

**Why HTML instead of Markdown:**
- ✅ Stakeholders can SEE actual colors, not hex codes
- ✅ Typography samples show the font rendered at size
- ✅ Interactive elements demonstrate hover states
- ✅ Spacing scale is visual, not described in text
- ✅ Can be opened directly in browser without conversion
- ✅ Easy to share and review

## Frontend Aesthetics Guidelines

**CRITICAL: Avoid "AI Slop" Aesthetics**

You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight. Focus on:

### Typography
Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.

**Examples of distinctive typography choices:**
- Serif fonts for elegance: Fraunces, Newsreader, Lora, Crimson Pro
- Display fonts for impact: Cabinet Grotesk, Clash Display, General Sans, Plus Jakarta Sans
- Monospace fonts for technical feel: JetBrains Mono, Fira Code, IBM Plex Mono
- Unique sans-serifs: Satoshi, Syne, Manrope, DM Sans, Outfit

**❌ Avoid these overused fonts:**
- Inter (extremely overused in AI-generated designs)
- Roboto
- Arial
- System fonts (unless specifically appropriate)
- Space Grotesk (becoming cliché despite being trendy)

### Color & Theme
Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.

**Strong palette approaches:**
- **Dominant + Accent**: 80% one color family, 20% sharp contrast accent
- **Dark with neon**: Deep backgrounds with vibrant, glowing accents
- **Monochrome + single hue**: Grayscale with one bold color for CTAs
- **Cultural aesthetics**: Draw from Brutalism, Memphis, Bauhaus, Vaporwave, etc.
- **IDE-inspired**: VSCode themes, terminal color schemes, syntax highlighting palettes

**❌ Avoid clichéd color schemes:**
- Purple gradients on white backgrounds (extremely overused)
- Generic blue + gray combinations
- Pastel everything (unless contextually appropriate)
- Rainbow palettes with equal distribution

### Motion
Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.

**High-impact animation moments:**
- Page load orchestration with staggered reveals
- Transition between major states (expanded/collapsed, light/dark)
- Hover effects on key interactive elements
- Success states (checkmarks, confirmations)
- Drag and drop feedback

**CSS-only animation examples:**
```css
/* Staggered reveal */
.item:nth-child(1) { animation-delay: 0ms; }
.item:nth-child(2) { animation-delay: 100ms; }
.item:nth-child(3) { animation-delay: 200ms; }

/* Smooth micro-interactions */
.button {
  transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
}
.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}
```

**For React, use Framer Motion:**
```jsx
import { motion } from 'framer-motion'

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ delay: 0.2, duration: 0.6 }}
>
  Content
</motion.div>
```

### Backgrounds
Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

**Atmospheric background techniques:**
- **Gradient meshes**: Multi-color gradient overlays with blur
- **Noise textures**: Subtle grain for depth
- **Geometric patterns**: Grid, dots, lines that don't overwhelm
- **Radial gradients**: Spotlight or vignette effects
- **Layered gradients**: Multiple semi-transparent gradients stacked
- **CSS backdrop filters**: Glassmorphism, blur effects

**Examples:**
```css
/* Gradient mesh background */
background:
  radial-gradient(at 20% 30%, #ff006e 0px, transparent 50%),
  radial-gradient(at 80% 70%, #8338ec 0px, transparent 50%),
  radial-gradient(at 50% 50%, #3a86ff 0px, transparent 50%),
  #000;

/* Noise texture overlay */
background: #0a0a0a;
background-image:
  url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.05'/%3E%3C/svg%3E");

/* Grid pattern */
background-size: 40px 40px;
background-image:
  linear-gradient(to right, rgba(255,255,255,0.05) 1px, transparent 1px),
  linear-gradient(to bottom, rgba(255,255,255,0.05) 1px, transparent 1px);
```

### Avoid Generic AI-Generated Aesthetics

**❌ DO NOT USE:**
- Overused font families: Inter, Roboto, Arial, system fonts (unless contextually appropriate)
- Clichéd color schemes: Purple gradients on white, generic blue/gray
- Predictable layouts: Cookie-cutter three-column grids
- Component patterns: Rounded corners everywhere, soft shadows on everything
- Cookie-cutter design: Lacks context-specific character

**✅ INSTEAD:**
- Interpret creatively and make unexpected choices that feel genuinely designed for the context
- Vary between light and dark themes
- Use different fonts across concepts
- Explore different visual aesthetics (not just rounded corners and soft shadows)
- Think outside the box - avoid converging on the same choices (even "trendy" ones like Space Grotesk)

**Concept variation strategy:**
- **Concept 1 (Safe/Refined)**: Polished, professional design that feels familiar but elevated - clean sans-serif (not Inter!), balanced whitespace, subtle color palette, smooth transitions. This is the "stakeholder-friendly" option that's easier to approve.
- **Concept 2 (Bold/Distinctive)**: Dark theme with bold neon accents, geometric sans-serif, sharp edges, high-contrast. This pushes creativity while staying functional.
- **Concept 3 (Experimental)**: Brutalist aesthetic with monospace fonts, unconventional layouts, cultural aesthetic influences (Memphis, Bauhaus, etc.). This explores the boundaries.

Each concept should feel like it was designed by a different designer with a different aesthetic sensibility, not just the same design in three color variations. The "safe" concept should still avoid AI clichés - it should be refined and polished, not generic.

## Quality Criteria

### Excellent Concepts:
- **Three distinct directions** (for initial exploration): Create 3 concepts when initially exploring a product/feature unless explicitly told otherwise
- **One refined direction** (for refinement): When refining, focus on iterating one chosen concept based on feedback
- **Tied to research**: Design decisions directly address user jobs/pain points
- **Strategically different**: Each initial concept explores a meaningfully different approach (not just color/font variations)
- **Appropriate fidelity**: Level of detail matches the questions being answered
- **Annotated**: Key decisions are explained, not just shown
- **Realistic**: Use real or realistic content, not Lorem Ipsum
- **Accessible baseline**: Even concepts consider color contrast, text size
- **Responsive-aware**: Show how designs adapt to different screens (if relevant)

### Excellent Mood Boards:
- **Cohesive**: Each direction feels unified and intentional
- **Distinctive**: Different directions are clearly different, not just color swaps
- **Contextual**: Visual choices connect to brand and user needs
- **Inspiring**: High-quality examples that elevate the conversation
- **Annotated**: Explain WHY these visuals, not just WHAT they are

### Excellent Prototypes:
- **Interactive key flows**: Focus on most important user journeys
- **Realistic interactions**: Buttons click, forms validate, states change
- **Performance**: Fast load, smooth transitions
- **Feedback mechanisms**: Show loading states, errors, success messages
- **Easy to understand**: Clear labels, obvious next steps

## Deliverable Formats

### File Organization

**IMPORTANT: Organize all deliverables by feature/assignment in dated folders.**

Each concept project should be saved in its own folder with the feature name:
```
docs/design/{feature-name}-concepts-{MMDDYY}/
```

**Feature Name Guidelines:**
- Use kebab-case (lowercase with hyphens)
- Examples: `checkout-flow`, `user-profile`, `dashboard-redesign`, `search-filters`
- Ask the user for the feature name if not provided
- Suggest a name based on their description if needed

**Examples:**
- Checkout flow concepts on Oct 24, 2025: `docs/design/checkout-flow-concepts-102425/`
- Checkout flow refinement on Oct 30, 2025: `docs/design/checkout-flow-concepts-103025/`
- Dashboard layout concepts on Nov 5, 2025: `docs/design/dashboard-layout-concepts-110525/`

**Why organize by feature:**
- **Immediate clarity**: Know what feature each file relates to
- **Version history**: Same feature can have multiple dated iterations
- **No conflicts**: Different features can have same-named files
- **Easy comparison**: Compare concepts across iterations for same feature
- **Organized**: All related files together (concepts, mood boards, overview)

**Folder structure:**
```
docs/design/{feature-name}-concepts-{MMDDYY}/
├── {feature-name}-mood-board.html
├── {feature-name}-concept-1-{variant}.html or .jsx
├── {feature-name}-concept-2-{variant}.html or .jsx
├── {feature-name}-concept-3-{variant}.html or .jsx
└── {feature-name}-overview.md
```

### UI Design Concepts
**Location**: `docs/design/{feature-name}-concepts-{MMDDYY}/`
**File**: `{feature-name}-concept-{number}-{variant}.jsx` or `.html`
**Format**: React artifact or HTML with Tailwind
**Include**:
- 2-3 key screens showing the concept
- Annotations explaining design decisions
- Responsive behavior (if applicable)

**Variant name examples**: `single-page`, `wizard`, `minimal`, `bold`, `experimental`

### Mood Boards
**Location**: `docs/design/{feature-name}-concepts-{MMDDYY}/`
**File**: `{feature-name}-mood-board.html`
**Format**: HTML artifact with images and descriptions
**Include**:
- 2-3 visual directions
- Color palettes, typography, visual style examples
- Rationale tied to research/brand
- References/inspiration sources

### Prototypes
**Location**: `docs/design/{feature-name}-concepts-{MMDDYY}/`
**File**: `{feature-name}-prototype-{variant}.jsx`
**Format**: React artifact with interactivity
**Include**:
- Interactive key flows (3-7 screens)
- Realistic content and data
- State management for interactions
- Annotations for non-obvious interactions

### Design Concept Document
**Location**: `docs/design/{feature-name}-concepts-{MMDDYY}/`
**File**: `{feature-name}-overview.md`
**Format**: Markdown summary document
**Include**:
- Links to all concept files for this feature
- Comparison of different directions
- Pros/cons of each approach
- Recommendation (if asked)
- Next steps and open questions

## Examples

### Good Concept Progression

**Initial Brief**: "Design a faster checkout flow for e-commerce"

**Concept 1: Single-Page Express**
- All checkout fields on one scrolling page
- Smart defaults from user history
- Rationale: Reduces clicks, addresses "too many steps" pain point
- Tradeoff: More scrolling, potentially overwhelming

**Concept 2: Progressive Sections**
- 3 clear steps: Shipping → Payment → Review
- Each section expands when ready
- Rationale: Maintains progress sense, reduces cognitive load
- Tradeoff: More clicks, but clearer mental model

**Concept 3: Inline Cart Checkout**
- Checkout overlays cart, doesn't navigate away
- Real-time shipping calculation
- Rationale: Maintains context, feels faster
- Tradeoff: Limited screen space, complex responsive behavior

### Good Annotation Example
```jsx
// ✅ Good: Explains WHY
<button className="bg-green-600 text-white px-8 py-4 text-lg">
  {/* Large, high-contrast CTA - Research showed 40% of users 
      abandoned on mobile due to small, hard-to-tap buttons */}
  Complete Purchase
</button>

// ❌ Poor: Just describes WHAT
<button className="bg-green-600 text-white px-8 py-4 text-lg">
  {/* Green button */}
  Complete Purchase
</button>
```

## Common Pitfalls to Avoid

### ❌ Designing in a Vacuum
**Problem**: Creating concepts without reviewing research or existing materials
**Instead**: Start every concept by reviewing personas, design principles, and competitive analysis

### ❌ Too Many Options (or Too Few)
**Problem**: Presenting 5+ concepts that overwhelm stakeholders, OR presenting only 1 concept during initial exploration that feels like "approve or reject"
**Instead**:
- **Initial exploration**: Default to 3 meaningfully different directions with clear tradeoffs - this is the sweet spot for decision-making
- **Refinement**: Focus on 1 concept, iterating the chosen direction based on feedback

### ❌ Premature Pixel-Perfect Polish
**Problem**: Spending hours on shadows/gradients before validating the approach
**Instead**: Match fidelity to the question - use low-fi until direction is validated

### ❌ Lorem Ipsum Syndrome
**Problem**: Using placeholder text that hides content design problems
**Instead**: Use realistic content that exposes real layout and hierarchy challenges

### ❌ Concepts That Look Identical
**Problem**: Three concepts that only differ in color or button shape (superficial variations)
**Instead**: Explore genuinely different strategic approaches:
- Different information architecture (what's shown where)
- Different navigation models (tabs vs. sidebar vs. bottom sheet)
- Different interaction patterns (single-page vs. multi-step)
- Different content priorities (what's emphasized)
- Different user flows (linear vs. flexible)

Example: For a checkout flow, don't show "same 3-step flow with different button colors" - instead show:
1. Single-page express checkout
2. Progressive disclosure wizard
3. Inline cart checkout overlay

### ❌ Missing the "Why"
**Problem**: Beautiful designs with no explanation of decisions
**Instead**: Annotate key decisions with rationale tied to research insights

### ❌ Designing for Desktop Only
**Problem**: Concepts that don't consider mobile or tablet experiences
**Instead**: Design mobile-first or show responsive behavior for key breakpoints

### ❌ Ignoring Technical Feasibility
**Problem**: Concepts requiring tech that doesn't exist or can't be built in timeline
**Instead**: Check technical constraints early, design within feasible boundaries

### ❌ Copying Without Adapting
**Problem**: Directly copying competitor designs without adapting to your users' jobs
**Instead**: Learn from patterns but customize for your specific user needs and context

## Design Patterns Library

### Common UI Patterns to Consider

**Navigation Patterns**:
- Tab bars (mobile): Quick access to 3-5 main sections
- Hamburger menu: Space-saving for many options
- Bottom sheets: Contextual actions without leaving screen
- Breadcrumbs: Show hierarchy, enable quick navigation

**Form Patterns**:
- Inline validation: Show errors as user types
- Progressive disclosure: Show fields as needed
- Smart defaults: Pre-fill when possible
- Multi-step wizards: Break complex forms into steps

**Content Patterns**:
- Cards: Scannable, contained content blocks
- Lists: Efficient for repeating content
- Grids: Visual browsing, discovery
- Feed: Infinite scroll for continuous content

**Feedback Patterns**:
- Toast notifications: Brief, non-blocking alerts
- Modal dialogs: Important confirmations
- Skeleton screens: Show structure while loading
- Empty states: Guide users when no content exists

## Integration Points

### Inputs from Other Teams
- **Design Research**: Personas, design principles, user insights, competitive analysis
- **Product/PM**: Feature requirements, business goals, timeline constraints
- **Engineering**: Technical constraints, API capabilities, performance requirements
- **Brand/Marketing**: Brand guidelines, messaging, visual identity

### Outputs for Other Teams
- **Design Production**: Validated direction to develop into production-ready designs
- **Product/PM**: Visual artifacts to communicate product vision to stakeholders
- **Engineering**: Interactive prototypes to validate technical feasibility
- **Marketing**: Visual concepts for early marketing/PR materials

### Related Skills
- Use **design-research** artifacts (personas, principles) to inform concepts
- Concepts feed into **design-production** for detailed specification
- Share concepts with **PM** teams for alignment on features and priorities

## Tips for Best Results

1. **Start with research review** - Read personas and design principles before sketching
2. **Explore before converging** - Generate many rough ideas before refining favorites
3. **Design with real content** - Placeholder text hides problems
4. **Test on devices** - Check mobile responsiveness, don't just assume
5. **Show your thinking** - Annotate WHY, not just WHAT
6. **Compare options clearly** - Make tradeoffs visible for stakeholders
7. **Prototype the hard parts** - If an interaction is complex, make it work
8. **Stay within brand guardrails** - Push creativity within constraints
9. **Consider accessibility early** - Color contrast, text size, keyboard nav
10. **Timebox concept work** - Perfect is the enemy of "good enough to get feedback"

## Concept Presentation Template

When presenting concepts, structure like this:

```markdown
# [Project Name] Design Concepts

## Design Challenge
[What problem are we solving? Who for? Why now?]

## Key Research Insights
1. [Insight from research that informs these concepts]
2. [Another key insight]
3. [Another key insight]

## Concept 1: [Descriptive Name]
**Approach**: [High-level strategy]
**Strengths**: [What this does well]
**Tradeoffs**: [What this sacrifices]
[Link to prototype/mockup]

## Concept 2: [Descriptive Name]
**Approach**: [High-level strategy]
**Strengths**: [What this does well]
**Tradeoffs**: [What this sacrifices]
[Link to prototype/mockup]

## Concept 3: [Descriptive Name]
**Approach**: [High-level strategy]
**Strengths**: [What this does well]
**Tradeoffs**: [What this sacrifices]
[Link to prototype/mockup]

## Recommendation
[If asked: Which concept to pursue and why]

## Next Steps
- [ ] Gather feedback from [stakeholders]
- [ ] Test [specific assumption] with users
- [ ] Refine chosen direction in production design
```

## Validation Checklist

Before delivering concept artifacts, verify:
- [ ] Reviewed research insights and design principles
- [ ] **For initial exploration**: Created 3 meaningfully different concepts (not just visual variations of the same approach)
- [ ] **For refinement**: Focused on iterating 1 chosen concept based on feedback
- [ ] Each initial concept explores a different strategic direction or interaction model
- [ ] Used realistic content, not Lorem Ipsum
- [ ] Annotated key design decisions with rationale
- [ ] Checked responsive behavior for mobile/tablet
- [ ] Verified color contrast meets minimum standards (4.5:1 for text)
- [ ] Files are in `/mnt/user-data/outputs/` with descriptive names
- [ ] Created overview document comparing concepts
- [ ] Interactive prototypes work smoothly (no broken interactions)
- [ ] Clearly communicated next steps and decisions needed
