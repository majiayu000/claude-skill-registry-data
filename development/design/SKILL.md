---
name: design
description: Expert UI/UX design guidance for evaluating, building, or updating user interfaces. Applies typography principles (hierarchy, readability, interactivity), visual design patterns, and Shift Nudge best practices. Use when designing screens, reviewing layouts, styling components, or improving UX. Use this skill if prompted with "design" or "ux".
allowed-tools: Read, Grep, Glob, Edit, Write
---

# UI Design Expert

Expert guidance for evaluating and building exceptional user interfaces, based on Shift Nudge design principles.

## When to Use This Skill

**Automatic activation when:**
- Evaluating UI/UX design
- Building or styling interface components
- Reviewing layouts, typography, or visual hierarchy
- Improving readability or user experience
- Creating design systems or component libraries

**Key capabilities:**
- Typography analysis and implementation
- Visual hierarchy evaluation
- Component design guidance
- Accessibility compliance
- Design system creation

## Core Design Principles

### 1. Visual Hierarchy First
Before applying any styling rules, define:
- **User Goal**: What is the user trying to accomplish?
- **Intended Action**: What's the primary action?
- **Information Priority**: What's most critical? Second? Third?

### 2. Systematic Consistency
- Limit complexity through constraints (Rule of Four for font sizes)
- Create reusable, documented patterns
- Ensure similar elements look similar
- Build systems that users can learn

### 3. Progressive Refinement
- Start simple, refine through iteration
- Test with real content (especially edge cases)
- Balance aesthetics with usability
- Prioritize readability over decoration

## Typography Reference Guides

Comprehensive typography guides available in `.claude/skills/design/references/`:

### @.claude/skills/design/references/hierarchy.md
Visual hierarchy and the Rule of Four
- Establishing type scales (max 4 distinct sizes)
- Creating emphasis through weight and visual weight
- Organizing information priority
- Font weight vs visual weight concepts

### @.claude/skills/design/references/text-elements.md
Core text styling best practices
- Title weights, line heights, alignment
- Body copy readability (16px default, 45-75 char line length, 125-175% line height)
- Letter-spacing rules (only for ALL CAPS)
- Responsive text considerations

### @.claude/skills/design/references/interactive.md
Buttons, links, and interactive elements
- Indicating interactivity (color, weight, decoration, background)
- Button hierarchy (primary, secondary, tertiary, destructive)
- Links vs buttons distinction
- Interactive states (hover, focus, active, disabled)
- Accessibility requirements (underlines in body text, focus states)

### @.claude/skills/design/references/callouts.md
Featured content and emphasis
- Blockquotes, pull quotes, testimonials
- Scale and case variations
- Color and background treatments
- Breaking the grid for visual interest

### @.claude/skills/design/references/combination.md
Text with icons, images, and other elements
- Negative space and breathing room
- Baseline alignment techniques
- Balance at all levels (component, section, page)
- Common patterns (icon+label, avatar+text, stats)

### @.claude/skills/design/references/systems.md
Design system creation
- Defining text style purposes
- Naming conventions (semantic, scale-based, hybrid)
- Token systems (foundational and semantic)
- Documentation and maintenance

## Design Analysis Workflow

When evaluating or building UI:

1. **Establish Hierarchy**
   - Identify primary, secondary, tertiary content
   - Check visual weight matches importance
   - Verify 4 or fewer font sizes (per section)

2. **Check Typography**
   - Titles: 2-3 weights heavier than body, 100-120% line height
   - Body: 16px+ size, 125-175% line height, 45-75 char line length
   - Interactive: Clear indication via color, weight, decoration, or background
   - Letter-spacing: Only on ALL CAPS (never on lowercase)

3. **Verify Interactivity**
   - Users can identify clickable elements
   - Primary actions are most prominent
   - Destructive actions use warning colors
   - All states defined (hover, focus, active, disabled)

4. **Test Readability**
   - Sufficient contrast (WCAG AA minimum)
   - Line lengths constrained (max-width: 65ch)
   - Adequate spacing and padding
   - Works with longer/shorter content

5. **Check Consistency**
   - Similar elements look similar
   - Reusable patterns documented
   - Spacing system followed
   - Design tokens applied

## Common UI Patterns

### Form Actions
```
Primary: Solid background, high contrast (Submit, Save, Continue)
Secondary: Outline or subtle background (Cancel, Back)
Tertiary: Minimal styling (Help, Learn More)
```

### Text Hierarchy
```
Hero Title: 48-72px, Bold (700), tight line height (110%)
Section Heading: 24-32px, Semibold (600), 120% line height
Body: 16px, Regular (400), 160% line height, max-width 65ch
Metadata: 12-14px, Medium (500), 140% line height
```

### Interactive States
```
Base: Normal appearance
Hover: Slight brightness/scale change
Focus: 3px outline, 2px offset (accessibility)
Active: Pressed appearance
Disabled: Reduced opacity, no interaction
```

## Design Review Checklist

Use when reviewing existing designs:

**Visual Hierarchy:**
- [ ] Most important info immediately identifiable
- [ ] Clear primary/secondary/tertiary differentiation
- [ ] Visual weight matches importance
- [ ] Negative space used effectively

**Typography:**
- [ ] 4 or fewer distinct font sizes per section
- [ ] Titles 2-3 weights heavier than body
- [ ] Body text 16px+, readable weight
- [ ] Line heights appropriate (titles 100-120%, body 125-175%)
- [ ] Line lengths 45-75 characters
- [ ] Letter-spacing only on ALL CAPS

**Interactivity:**
- [ ] Clickable elements clearly identified
- [ ] Primary action is most prominent
- [ ] Links in body text underlined
- [ ] All states defined (hover, focus, active, disabled)
- [ ] Focus visible for keyboard users
- [ ] Destructive actions use warning colors

**Consistency:**
- [ ] Similar elements styled similarly
- [ ] Spacing system consistent
- [ ] Color usage systematic
- [ ] Patterns reusable and documented

**Accessibility:**
- [ ] Contrast meets WCAG AA (4.5:1 text, 3:1 large text)
- [ ] Focus states visible
- [ ] Interactive elements 44x44px minimum
- [ ] Links distinguishable without color alone

## Integration with Tech Stack

### React Router v7 + TailwindCSS
- Use `cn()` utility for composing classes
- Apply responsive design via Tailwind breakpoints
- Leverage type-colors for thematic styling
- Document patterns in component libraries

### shadcn/ui Components
- Review component variants for hierarchy
- Ensure consistent spacing/sizing
- Verify accessibility compliance
- Extend with custom design tokens

### Common Files to Reference
- `app/components/ui/*` - UI primitives
- `app/lib/utils.ts` - `cn()` utility
- `app/lib/type-colors.ts` - Color system
- `app.css` - Custom animations, base styles

## Output Format

When providing design feedback:

1. **Specific references** - Use `file_path:line_number` for code locations
2. **Before/After** - Show current state vs recommended changes
3. **Rationale** - Explain why (hierarchy, readability, accessibility)
4. **Code examples** - Provide Tailwind classes or CSS
5. **Checklists** - Use for systematic reviews

## Reference Documentation

For detailed guidance on specific topics, read:
- **Hierarchy & Scale**: `.claude/skills/design/references/hierarchy.md`
- **Text Elements**: `.claude/skills/design/references/text-elements.md`
- **Interactive Elements**: `.claude/skills/design/references/interactive.md`
- **Callouts & Features**: `.claude/skills/design/references/callouts.md`
- **Element Combination**: `.claude/skills/design/references/combination.md`
- **Design Systems**: `.claude/skills/design/references/systems.md`

---

**Remember**: Design is about solving user problems, not decoration. Every choice should serve the user's goals and the interface's purpose.
