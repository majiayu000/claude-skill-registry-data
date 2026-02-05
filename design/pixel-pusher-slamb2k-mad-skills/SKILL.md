---
name: pixel-pusher
description: Comprehensive UI/UX design system for creating professional web interfaces through structured multi-stage process. Use when users request website designs, landing pages, web apps, UI mockups, design systems, or interface prototypes. Guides through requirements gathering, design system creation from references/screenshots, HTML mockup generation, iterative refinement, and final design delivery. Ideal for "design me a website", "create a landing page", "build a UI for X", or providing design inspiration screenshots/URLs.
---

# Pixel Pusher Design System

Professional UI/UX design skill that transforms vague requirements into polished web interfaces through systematic design thinking and iterative refinement.

## Design Philosophy

Never accept vague design requests. Transform "make it beautiful" into concrete design systems with specific colors, typography, spacing, and component patterns. Work systematically through discovery, design system creation, mockup generation, and iterative refinement.

## Multi-Stage Design Process

### Stage 1: Discovery & Requirements Gathering

Begin by understanding what the user wants to create and gathering design inspiration.

**Initial questions to ask if not provided:**

1. **Purpose**: What is this interface for? (landing page, web app, dashboard, portfolio, etc.)
2. **Audience**: Who will use this? (consumers, professionals, internal team, etc.)
3. **Key features**: What are the 3-5 most important elements? (hero section, forms, data visualization, etc.)
4. **Inspiration**: Do you have reference designs? (URLs, screenshots, or describe style preferences)
5. **Brand elements**: Do you have existing brand colors, fonts, or logo?
6. **Technical constraints**: Any specific frameworks or technologies? (React, Vue, vanilla HTML, etc.)

**Critical assets to request:**

- Screenshots or URLs of designs they like
- Existing brand guidelines or assets
- Content examples (copy, images, data)
- Specific interactions or animations they envision

**Do not proceed to design system creation until you have:**
- Clear understanding of purpose and audience
- At least 2-3 reference designs (screenshots or URLs)
- Key features and content requirements
- Any brand constraints

### Stage 2: Design System Extraction

Extract a comprehensive JSON design system from reference materials. If user provides URLs, fetch them first to analyze the design patterns.

**For each reference, analyze and extract:**

1. **Color palette** - All colors with hex values, usage context (primary, secondary, accent, surface, text)
2. **Typography** - Font families, sizes, weights, line heights for each text level
3. **Spacing system** - Margin/padding patterns (identify the base unit: 4px, 8px, etc.)
4. **Component styles** - Buttons, cards, inputs, navigation patterns
5. **Layout patterns** - Grid systems, container widths, breakpoints
6. **Shadows & effects** - Elevation values, gradients, borders
7. **Interaction patterns** - Hover states, transitions, animations

**Create design-system.json** (see `assets/design-system-template.json` for structure)

Document decisions with rationale:
- Why these colors work together
- How typography creates hierarchy
- Why this spacing rhythm feels cohesive
- How components maintain consistency

### Stage 3: Mockup Generation

Generate 2-3 distinct HTML mockups that explore different interpretations of the requirements using the design system.

**Mockup variations should differ in:**
- Layout approach (single vs multi-column, vertical vs horizontal flow)
- Visual emphasis (bold vs minimal, playful vs professional)
- Component styling (rounded vs sharp, flat vs elevated)

**Each mockup must:**
- Use only colors from the design system
- Apply typography scale consistently
- Follow spacing system religiously
- Include responsive behavior (mobile-first)
- Show all requested key features
- Include hover/interaction states

**Technical implementation:**
- Create standalone HTML files with inline CSS
- Use modern CSS (Grid, Flexbox, CSS variables)
- Include minimal JavaScript only if interactions require it
- Ensure accessibility (semantic HTML, ARIA labels, keyboard navigation)

**File structure:**
```
mockup-1-bold.html     - Bold, high-contrast approach
mockup-2-minimal.html  - Clean, spacious, minimal approach
mockup-3-playful.html  - Dynamic, engaging approach
```

Save all mockups to `design-outputs/` directory in the current project and present them with:
- Brief description of each approach
- Key differentiators
- Recommended use cases for each style
- Full file paths so users can open them in their browser

### Stage 4: Feedback & Refinement

Present mockups and gather specific feedback:

**Ask directed questions:**
- Which mockup's overall aesthetic resonates most?
- What specific elements do you like/dislike?
- Does the color palette feel right? Too bold/muted?
- Is the typography readable and appropriate?
- Does the spacing feel comfortable?
- Any components that need redesign?

**Based on feedback:**
- If user likes one mockup: Refine that design
- If user likes elements from multiple: Combine best aspects
- If user dislikes all: Return to Stage 2 with new direction

**Refinement iterations:**
1. Make requested changes
2. Update design system if patterns change
3. Generate refined mockup(s)
4. Gather feedback
5. Repeat until satisfied

**Maximum 3-4 refinement rounds** before suggesting a consultation about requirements.

### Stage 5: Final Design Delivery

Once design is approved, deliver:

1. **Final HTML/CSS files** - Production-ready code
2. **Design system documentation** - Complete JSON + visual guide
3. **Component library** - Reusable HTML components
4. **Style guide** - Visual reference document (see `references/style-guide-template.md`)
5. **Assets** - Extracted colors, fonts, spacing variables as CSS/SCSS

**Optional enhancements:**
- Convert to React components if requested
- Add advanced animations with Framer Motion
- Integrate with component libraries (shadcn/ui, React Bits)
- Provide dark mode variations
- Create responsive breakpoint variations

## Design System Components

For detailed guidance on each design system layer, read:
- `references/design-system-layers.md` - Comprehensive component breakdown
- `references/accessibility-guidelines.md` - WCAG compliance checklist
- `references/design-best-practices.md` - Professional design principles

## Critical Reminders

**Always create files, never just show code:**
- Generate actual HTML files users can open in browsers
- Save all outputs to `design-outputs/` directory in the current project
- Provide full file paths so users can open files directly in their browser

**Maintain design system integrity:**
- Every color used must be in the design system
- Every spacing value must follow the scale
- Typography must use defined sizes/weights
- No arbitrary design decisions

**Prioritize user feedback:**
- Never defend design choices over user preferences
- Ask clarifying questions before assuming
- Offer alternatives when users express dissatisfaction
- Balance professional guidance with user vision

**Professional quality standards:**
- All designs must be responsive (mobile, tablet, desktop)
- Accessibility must meet WCAG 2.1 Level AA
- Performance-conscious (minimize CSS, optimize images)
- Cross-browser compatible (modern browsers)

## Advanced Features

### Persona Development

When user requests, create user personas to guide design decisions:
- Demographics and psychographics
- Goals and pain points
- Technical proficiency
- Design preferences

See `references/persona-template.md` for structure.

### User Flow Mapping

For complex applications, map user journeys:
- Entry points and goals
- Decision points and paths
- Pain points and friction
- Success metrics

See `references/user-flow-template.md` for structure.

### A/B Testing Variations

Generate multiple variations for testing:
- Different CTA placements
- Color scheme variations
- Layout alternatives
- Copy variations

## Integration with Claude Code Workflow

This skill aligns with Claude Code best practices:

**Use Planning Mode** (Shift+Tab) before generating mockups to:
- Research current design trends
- Outline implementation approach
- Identify technical considerations

**Leverage image analysis** (Control+V) to:
- Analyze provided screenshots
- Extract design patterns
- Identify visual hierarchy

**Create custom commands** for reusable design tasks:
- Design system validation
- Accessibility checks
- Responsive testing

**Use sub-agents** for complex projects:
- One agent for design system
- One agent per mockup variation
- One agent for component library

## Example Workflows

### Example 1: Landing Page from Scratch

```
User: "Create a landing page for my SaaS product"

1. Ask about product, audience, competitors
2. Request 2-3 competitor URLs for inspiration
3. Fetch and analyze competitor designs
4. Extract design system (colors, typography, components)
5. Generate 3 mockup variations
6. Gather feedback
7. Refine chosen mockup
8. Deliver final design + system documentation
```

### Example 2: Redesign from Screenshot

```
User: [Provides screenshot] "Make something similar but more modern"

1. Analyze screenshot (colors, layout, typography)
2. Ask what "more modern" means to them
3. Research current design trends
4. Extract design system from screenshot
5. Modernize system (updated colors, typography, spacing)
6. Generate 2-3 modern variations
7. Iterate based on feedback
8. Deliver final design
```

### Example 3: Design System from Brand Guidelines

```
User: "Create website designs using our brand guidelines" [provides PDF]

1. Extract brand colors, fonts, logo from guidelines
2. Ask about website purpose and features
3. Request competitor/inspiration references
4. Build design system extending brand guidelines
5. Generate mockups that honor brand identity
6. Validate brand consistency
7. Deliver with brand compliance documentation
```

## Quality Checklist

Before delivering final designs, verify:

- [ ] All colors from design system only
- [ ] Typography scale applied consistently
- [ ] Spacing follows system (no arbitrary values)
- [ ] Responsive across breakpoints (320px, 768px, 1024px, 1440px)
- [ ] Accessibility: color contrast, focus states, semantic HTML
- [ ] Interactive states: hover, active, focus, disabled
- [ ] Loading states for dynamic content
- [ ] Error states for forms
- [ ] Empty states with helpful messaging
- [ ] Consistent component styling
- [ ] Browser compatibility (Chrome, Firefox, Safari, Edge)
- [ ] Performance: optimized CSS, minimal dependencies

## Common Pitfalls to Avoid

**Don't:**
- Generate designs without gathering requirements first
- Use random colors not in the design system
- Skip the design system extraction phase
- Provide only one mockup without alternatives
- Ignore accessibility requirements
- Assume user technical knowledge
- Over-complicate simple requests
- Use heavy frameworks for simple pages

**Do:**
- Ask clarifying questions upfront
- Create systematic, reusable design tokens
- Generate multiple alternatives for comparison
- Explain design decisions with rationale
- Make designs accessible by default
- Provide clear documentation
- Start simple, add complexity as needed
- Use vanilla HTML/CSS unless frameworks requested
