---
name: ui-design-direction-builder
description: Builds an implementation-ready visual and interaction direction for a web interface. Use when the user asks to establish an art direction, redesign a page, improve an inconsistent UI, define visual foundations, translate product requirements into design rules, or prevent an implementation from becoming generic or visually fragmented.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: planner
  audience: frontend-developers-designers-product-engineers
  tags:
    - ui-design
    - art-direction
    - visual-system
    - interaction-design
    - design-tokens
    - frontend
  status: draft
  side_effects: none
---

# UI Design Direction Builder

## Purpose

Create a coherent and implementation-ready design direction for a web interface.

This skill translates product goals, user needs, existing brand material, repository evidence, and technical constraints into concrete visual and interaction rules.

It should prevent vague outputs such as:

- “Use a modern design.”
- “Add more whitespace.”
- “Make the cards cleaner.”
- “Use subtle animations.”
- “Add a premium gradient.”

The result must explain what the interface should look and feel like, why those decisions fit the product, and how they should be implemented consistently.

This is a design-direction skill, not a full visual design generator or a generic UI audit.

## When to use this skill

Use this skill when:

- The user asks for a visual direction for a new interface.
- A project has product requirements but no coherent design language.
- An existing interface feels inconsistent, generic, unfinished, or template-driven.
- The user asks to redesign a page, dashboard, demo, portfolio, product flow, or component collection.
- A frontend implementation needs typography, layout, color, hierarchy, component, and motion guidance.
- Multiple screens or components need to feel like one product.
- A project needs a design brief before implementation begins.
- The user uses phrases such as:
  - “Make this UI more polished.”
  - “Give this project a visual direction.”
  - “This looks too generic.”
  - “Create a modern design system.”
  - “Improve the art direction.”
  - “How should this interface look?”
  - “Turn this product brief into a design.”
  - “Define the UI before coding it.”

Do not use this skill when:

- The user only wants a WCAG or accessibility compliance audit.
- The task is limited to fixing one CSS defect.
- The user has supplied a finalized design that should be reproduced exactly.
- The request is solely about animation implementation.
- The user only needs brand naming, marketing copy, or logo generation.
- Another skill already covers a narrower task, such as a component-specific accessibility review.

## Inputs to inspect

Inspect the smallest useful set of available inputs.

### Product context

- Product or project brief
- Intended audience
- Primary user tasks
- Business or portfolio goals
- Content types
- Expected device classes
- Technical constraints
- Required states and workflows

### Existing interface evidence

- Screenshots
- Design files
- Current website or application
- Existing prototypes
- Demo pages
- Component previews
- Storybook stories
- Recorded interactions

### Repository files

When repository access is available, inspect relevant files such as:

- `README.md`
- `package.json`
- `src/`
- `app/`
- `pages/`
- `components/`
- `layouts/`
- `styles/`
- `public/`
- `assets/`
- `tokens/`
- `theme/`
- `tailwind.config.*`
- CSS, Sass, or CSS-in-JS theme files
- Existing component-library configuration
- Existing screenshots and demo media

### Existing visual foundations

Look for:

- Color variables
- Typography rules
- Font loading
- Spacing variables
- Border-radius patterns
- Container widths
- Grid definitions
- Shadows and elevation
- Icon sources
- Illustration or photography styles
- Motion durations and easing
- Focus and interaction states
- Light and dark themes

Do not assume that existing values are intentional. Treat them as evidence to evaluate.

## Core principles

### Design from product meaning

Visual decisions must reflect:

- What the product does
- Who uses it
- How frequently it is used
- How much information it contains
- Which actions carry the most importance or risk
- Whether the experience should feel efficient, expressive, calm, technical, playful, editorial, or authoritative

Do not select an aesthetic merely because it is currently fashionable.

### Prefer decisions over option dumps

The skill should recommend one primary direction.

Alternatives may be included only when:

- There is a genuine unresolved product constraint.
- Two valid directions serve materially different goals.
- The user explicitly requests multiple concepts.

Do not return five interchangeable mood-board descriptions and leave all decisions unresolved.

### Build a system, not isolated screens

Every recommendation should contribute to a repeatable visual language.

The direction must cover:

- Foundations
- Layout
- Components
- Interaction states
- Content hierarchy
- Motion
- Accessibility
- Responsive behavior

### Separate evidence from proposals

Label important decisions as one of:

- Existing: already established by the product or repository
- Derived: inferred from product goals or user needs
- Proposed: a new design recommendation

Do not present invented preferences as established requirements.

### Avoid default design clichés

Do not automatically recommend:

- Excessive gradients
- Glassmorphism
- Large rounded cards around every section
- Decorative blobs
- Oversized hero typography without content justification
- Low-contrast gray text
- Hover-only interaction
- Animation on every element
- Dense shadow stacks
- Generic purple-and-blue AI branding
- Dashboard layouts for products that are not dashboards
- Dark mode merely to make the interface appear technical
- Bento grids without a meaningful information hierarchy

These patterns may still be used when the product context supports them.

## Workflow

1. Establish the product frame.

   Summarize:

   - What is being designed
   - Who it serves
   - The primary task
   - The most important action
   - The main content type
   - The expected usage frequency
   - The technical environment
   - The current design problem

   Reduce the product to a concise design problem statement.

   Example:

   > Design a high-density but approachable interface for developers who repeatedly inspect accessibility findings and need to move quickly between evidence, severity, remediation guidance, and source code.

   Do not begin choosing colors before the product frame is clear.

2. Identify constraints and fixed decisions.

   Record what cannot or should not change.

   Examples:

   - Existing brand color
   - Required logo
   - Current framework
   - Existing component library
   - Required browser support
   - Content-management limitations
   - Accessibility requirements
   - Existing information architecture
   - Required light or dark theme
   - Performance constraints
   - Available assets

   Distinguish true constraints from inherited implementation accidents.

3. Audit the current visual language.

   When an existing interface or repository is available, identify:

   - Repeated patterns
   - Conflicting patterns
   - Missing foundations
   - One-off values
   - Weak hierarchy
   - Unclear actions
   - Layout inconsistencies
   - Excessive visual noise
   - Under-designed empty or loading states
   - Inconsistent responsive behavior
   - Inaccessible interaction states

   Create a concise current-state summary.

   Do not turn this section into a full code or accessibility audit.

4. Define the design attributes.

   Select three to five attributes that describe the intended experience.

   Good attribute combinations:

   - Precise
   - Calm
   - Technical
   - Approachable

   Or:

   - Editorial
   - Expressive
   - Structured
   - Cinematic

   For each attribute, define what it means in interface terms.

   Example:

   | Attribute | Interface implication |
   |---|---|
   | Precise | Strong alignment, explicit labels, restrained decoration, predictable states |
   | Calm | Limited accent usage, stable layout, controlled motion, comfortable spacing |
   | Technical | Data-friendly typography, visible system status, clear structure |
   | Approachable | Plain language, forgiving controls, useful empty states, moderate density |

   Also define two or three anti-attributes.

   Example:

   - Not playful
   - Not corporate-luxury
   - Not visually noisy

   The anti-attributes prevent the implementation from drifting.

5. Choose the primary art direction.

   Define one primary visual direction with a short, memorable name.

   Examples:

   - Quiet Technical Editorial
   - Structured Utility
   - Soft Industrial
   - Precision Workspace
   - Accessible Product Laboratory
   - Cinematic Documentation
   - Calm Operational Interface

   Explain:

   - Why the direction fits the product
   - What it should communicate
   - What it should avoid
   - How it differs from a generic template

   The name is an internal design shorthand, not necessarily public-facing branding.

6. Define visual foundations.

   Specify practical rules for the following areas.

   **Typography**

   Define:

   - Display or heading character
   - Body-text character
   - UI-label character
   - Recommended font categories or existing font usage
   - Type scale behavior
   - Line-length guidance
   - Weight hierarchy
   - Numeric or code typography requirements
   - Rules for uppercase text
   - Responsive heading behavior

   Do not recommend a typeface solely because it is popular.

   **Color**

   Define:

   - Base surface strategy
   - Text hierarchy
   - Accent-color role
   - Semantic colors
   - Border and divider behavior
   - Selected, active, warning, success, and error states
   - Light and dark theme expectations
   - Contrast requirements

   Use accent colors intentionally. The accent should identify priority, state, or action rather than decorate every section.

   **Spacing and density**

   Define:

   - Base spacing rhythm
   - Section spacing
   - Component padding
   - Dense versus comfortable regions
   - Relationship between spacing and hierarchy
   - Mobile spacing behavior

   Do not use excessive whitespace where users need to compare information.

   **Shape**

   Define:

   - Border-radius range
   - Border style
   - Divider usage
   - Control shape
   - Container shape
   - Whether cards are primary structural elements or used selectively

   **Elevation**

   Define:

   - Whether shadows are necessary
   - Which elements may appear elevated
   - How overlays, dialogs, popovers, and sticky regions separate from content
   - When borders should replace shadows

   **Iconography and imagery**

   Define:

   - Icon style
   - Stroke or fill preference
   - Size and alignment rules
   - Illustration style
   - Photography treatment
   - Screenshot framing
   - Empty-state artwork policy
   - Decorative-image limits

7. Define the layout system.

   Document:

   - Main container behavior
   - Maximum content width
   - Grid strategy
   - Sidebar behavior
   - Reading-width regions
   - Full-bleed regions
   - Section rhythm
   - Alignment rules
   - Sticky or fixed regions
   - Mobile stacking order
   - Breakpoint behavior

   Explain how layout reflects content priority.

   Avoid arbitrary breakpoint lists unless the repository already establishes them.

8. Define hierarchy and composition.

   For each important page or view, identify:

   - Primary message
   - Primary action
   - Secondary action
   - Supporting information
   - Persistent navigation
   - Status information
   - Contextual controls
   - Optional or tertiary content

   Specify which element should visually dominate and which elements should recede.

   Flag competing focal points.

9. Define component expression.

   Describe how key component families should express the direction.

   Relevant families may include:

   - Navigation
   - Buttons
   - Links
   - Inputs
   - Selects
   - Filters
   - Search
   - Cards
   - Tables
   - Lists
   - Tabs
   - Accordions
   - Dialogs
   - Toasts
   - Alerts
   - Empty states
   - Loading states
   - Code blocks
   - Charts
   - Media
   - Pagination
   - Command palettes

   For each relevant family, define:

   - Visual role
   - Hierarchy
   - Density
   - State treatment
   - Responsive behavior
   - Interaction considerations

   Do not attempt to redesign components that are irrelevant to the product.

10. Define interaction states.

    Cover at least:

    - Default
    - Hover
    - Focus
    - Active or pressed
    - Selected
    - Disabled
    - Loading
    - Success
    - Warning
    - Error
    - Empty
    - Offline, when relevant

    Focus states must be intentional parts of the visual system, not browser defaults removed and forgotten.

    Do not communicate state through color alone.

11. Define motion behavior.

    Describe motion as functional behavior.

    Specify:

    - What motion communicates
    - Which elements may animate
    - Which transitions should remain instant
    - Duration ranges
    - Easing character
    - Entrance and exit relationships
    - Layout-transition rules
    - Feedback behavior
    - Reduced-motion alternatives

    Good motion purposes include:

    - Confirming state change
    - Maintaining spatial context
    - Revealing hierarchy
    - Connecting trigger and result
    - Reducing perceived abruptness

    Avoid decorative motion that delays frequent tasks.

    Do not prescribe GSAP, Motion, CSS transitions, or another implementation tool unless the repository or user requires one.

12. Apply accessibility constraints.

    Integrate accessibility into the direction.

    Check that recommendations account for:

    - Text contrast
    - Non-text contrast
    - Visible focus
    - Keyboard interaction
    - Zoom and reflow
    - Reduced motion
    - Touch-target sizing
    - Error communication
    - Status communication
    - Color-independent state
    - Readable type size and line height
    - Content order
    - Responsive navigation
    - High-contrast or forced-colors behavior where relevant

    Do not treat accessibility as a final visual cleanup step.

13. Translate the direction into implementation rules.

    Convert abstract recommendations into instructions a frontend developer can follow.

    Include:

    - Suggested design-token groups
    - Existing variables to preserve
    - Values or patterns to consolidate
    - Components to update first
    - Screens to use as reference implementations
    - Reusable layout primitives
    - Reusable state patterns
    - Areas where one-off styling should be removed
    - Recommended implementation sequence

    Prefer semantic token roles such as:

    - `--color-surface-primary`
    - `--color-text-muted`
    - `--color-action-primary`
    - `--space-section`
    - `--radius-control`
    - `--duration-feedback`

    Avoid generating a complete token file unless implementation is requested.

14. Identify risks and unresolved decisions.

    Record issues that could materially change the design direction.

    Examples:

    - Unknown content volume
    - Missing brand assets
    - Unclear mobile priority
    - Unconfirmed localization requirements
    - Missing chart requirements
    - Undefined dark-mode support
    - Conflicting product goals
    - Dependence on unavailable imagery

    Do not use minor unknowns as an excuse to avoid recommending a direction.

15. Validate the direction.

    Check that:

    - The design reflects the product rather than current fashion.
    - The direction can be recognized across multiple screens.
    - Visual hierarchy supports the primary user task.
    - Recommendations are implementable in the current stack.
    - States are defined, not just static appearance.
    - Responsive behavior is considered.
    - Accessibility is integrated.
    - The direction avoids unnecessary decoration.
    - The output contains concrete decisions.
    - A developer could begin implementation without inventing the design from scratch.

## Output format

Return the result using this structure:

```md
# UI Design Direction

## 1. Design problem

- Product:
- Audience:
- Primary task:
- Current problem:
- Constraints:

## 2. Recommended direction

**Direction name:** ...

One-paragraph explanation.

### Design attributes

| Attribute | Interface implication |
|---|---|

### Anti-attributes

- Not ...
- Not ...

## 3. Current-state observations

| Observation | Evidence | Design consequence |
|---|---|---|

Omit this section when no existing interface was provided.

## 4. Visual foundations

### Typography

- ...

### Color

- ...

### Spacing and density

- ...

### Shape and elevation

- ...

### Iconography and imagery

- ...

## 5. Layout and hierarchy

- ...

## 6. Component direction

| Component family | Direction | Important states |
|---|---|---|

## 7. Motion and interaction

- Motion purpose:
- Duration character:
- Spatial behavior:
- Reduced-motion behavior:

## 8. Accessibility requirements

- ...

## 9. Implementation guidance

### Suggested token groups

- ...

### Priority components

1. ...
2. ...
3. ...

### Suggested implementation sequence

1. ...
2. ...
3. ...

## 10. Risks and unresolved decisions

- ...

## 11. Validation checklist

- [ ] The primary action is visually clear.
- [ ] Typography roles are consistent.
- [ ] Accent color has a defined purpose.
- [ ] Components share the same visual language.
- [ ] Interaction states are defined.
- [ ] Responsive behavior is covered.
- [ ] Motion supports usability.
- [ ] Reduced motion is supported.
- [ ] Focus and contrast requirements are included.
- [ ] The direction is specific enough to implement.
```

## Implementation mode

By default, this skill produces design direction and implementation guidance only.

Apply repository changes only when the user explicitly asks for implementation.

When implementation is requested:

1. Identify the smallest representative screen or component set.
2. Establish or normalize the foundational tokens.
3. Implement one reference pattern.
4. Validate responsive and interaction states.
5. Propagate the system to related components.
6. Avoid rewriting unrelated application logic.
7. Report every file changed.
8. Separate completed work from remaining design recommendations.

Do not redesign the entire repository in one uncontrolled pass.

## Quality bar

The task is complete only when:

- One clear primary design direction is recommended.
- The direction is tied to actual product goals.
- Existing evidence and new proposals are distinguishable.
- Design attributes have concrete interface implications.
- Typography, color, spacing, shape, and layout rules are covered.
- Relevant component families are addressed.
- Interaction states are included.
- Motion has a functional purpose.
- Accessibility is integrated throughout the direction.
- Recommendations can be implemented in the identified technology stack.
- The output avoids vague “modern UI” language.
- The result does not depend on blindly copying a trend or competitor.
- Risks and unresolved decisions are disclosed.
- No files are modified unless implementation was requested.

## Edge cases

### No existing design exists

Create the direction from:

- Product purpose
- Audience
- Main workflows
- Content structure
- Technical constraints
- Desired positioning

Clearly label all visual decisions as proposed.

### The brief only says “modern”

Interpret “modern” as a request for:

- Clear hierarchy
- Consistent foundations
- Appropriate density
- Responsive behavior
- Complete interaction states
- Restrained visual effects
- Current but durable interface patterns

Do not treat “modern” as a visual style by itself.

### Existing branding is weak or inconsistent

Preserve recognizable brand assets where practical, but distinguish brand continuity from accidental inconsistency.

Recommend consolidation rather than silently discarding existing identity.

### The product contains dense data

Prioritize:

- Comparison
- Scanability
- Alignment
- Stable layouts
- Explicit status
- Compact controls
- Table and list alternatives

Do not inflate every data item into a large card.

### The project is a portfolio or experimental demo

Allow stronger art direction, composition, typography, and motion, but preserve:

- Readable content
- Keyboard access
- Reduced-motion support
- Clear navigation
- Reasonable loading performance

### The interface uses a third-party component library

Work with the library’s architecture.

Define:

- Theme overrides
- Token mappings
- Variant rules
- Components requiring wrappers
- Components that should remain unchanged

Do not recommend replacing the library without evidence that it blocks the required design.

### Screenshots are available but source files are not

Base findings on visible evidence and state that implementation assumptions remain unverified.

### The interface has multiple audiences

Identify the primary audience and task.

Create secondary adaptations only where the audiences have materially different needs.

## Related skills

No related skills are required. If referencing related skills in this library, first verify that those skill names exist in the target catalog.
