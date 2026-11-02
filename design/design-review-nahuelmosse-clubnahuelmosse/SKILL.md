---
name: design-review
description: Review UI implementation for design consistency, visual quality, AI-slop detection, and responsive behavior. Use when evaluating how a built UI looks and feels. For accessibility use /accessibility-audit; to build new components use /ui-component-builder.
user-invocable: true
---

# Design Review

## Core Rule

Compare implementation to the design source of truth. Flag divergence with screenshots and component refs; never auto-apply visual fixes.

## When to Use

Invoke with `/design-review` when:

- After implementing UI changes and want to verify visual quality
- Checking for design inconsistencies across the application
- Detecting AI-generated design patterns ("AI slop") that look generic
- Reviewing responsive behavior across viewport sizes
- Before shipping user-facing UI changes

## Default Behavior

When the user asks to audit, scan, review, or "give me a report" for design consistency / UI, produce the full design-review report automatically using the Process and Output Format sections below. Do not require the user to specify fields.

Only modify files when the user explicitly requests implement / fix / apply / refactor. By default, this skill is **report-only**.

## Process

### Phase 1: Inventory (first-pass leads)

This pass produces **candidates**, not findings. Treat counts as leads for deeper inspection in later phases. Do not report Phase 1 raw output as the final result.

Identify the project's design foundations:

1. **Check for DESIGN.md** — if it exists, use it as the single source of truth for design tokens, colors, typography, spacing, and component styles
2. **Read style config** — Tailwind config, CSS variables, theme files, design tokens
3. **Identify patterns** — component library in use (shadcn, MUI, Chakra, custom)
4. **Check for design tokens** — colors, spacing, typography, border-radius, shadows
5. **Cross-reference** — compare style config against DESIGN.md (if present) and flag any deviations
6. **Note inconsistencies** — multiple sources of truth, conflicting tokens

### Phase 2: Visual Consistency Audit

Check for design coherence:

**Spacing & Layout**
- Consistent spacing scale (4px/8px grid, Tailwind spacing)
- Alignment of elements within and across pages
- Consistent padding/margin patterns for similar components
- Proper whitespace — neither cramped nor wasteful

**Typography**
- Font scale is hierarchical and consistent
- Line heights appropriate for each text size
- Font weights used purposefully (not randomly bold)
- Text colors have sufficient contrast
- No more than 2-3 font families

**Color**
- Color palette is cohesive (not random hex values)
- Semantic color usage (success=green, error=red, warning=yellow)
- Sufficient contrast ratios (WCAG AA: 4.5:1 normal text, 3:1 large text)
- Dark mode consistency (if applicable)
- No color-only information (icons/text supplement color)

**Components**
- Buttons have consistent sizing, padding, and border-radius
- Form inputs follow a uniform style
- Cards/containers have consistent shadows and borders
- Icons are from the same family and consistently sized
- Interactive states (hover, focus, active, disabled) are uniform

### Phase 3: AI Slop Detection

Flag generic AI-generated design patterns that look templated:

**Common AI Slop Patterns**
- Uniform border-radius on everything (all rounded-xl or all rounded-lg)
- Generic 3-column grid layouts with identical cards
- Overuse of gradients, especially blue-to-purple
- Drop shadows on every element
- Generic stock-photo hero sections
- "Dashboard" layouts that look like every AI demo
- Excessive use of emojis as icons
- Perfectly symmetric layouts with no visual hierarchy
- Cookie-cutter component styling (every card identical)

**How to Fix**
- Vary border-radius based on component size and context
- Create visual hierarchy through size, weight, and spacing variation
- Use color purposefully, not decoratively
- Add intentional asymmetry and visual rhythm
- Replace generic elements with purposeful, context-specific design

### Phase 4: Responsive Behavior

Check responsive design across breakpoints:

- **Mobile (320-480px)** — single column, touch targets ≥44px, no horizontal scroll
- **Tablet (768-1024px)** — appropriate layout adaptation, not just scaled-down desktop
- **Desktop (1280+)** — proper use of space, readable line lengths (45-75 chars)
- **Edge cases** — very small screens (320px), very large screens (2560px+)
- **Content overflow** — long text, many items, empty states

### Phase 5: Interaction Quality

Review interactive elements:

- **Loading states** — skeleton screens or spinners, not blank spaces
- **Empty states** — helpful message and action, not blank page
- **Error states** — clear, actionable error messages
- **Transitions** — smooth, purposeful animations (not jarring or excessive)
- **Feedback** — visual response to user actions (button press, form submit)

## Output Format

```markdown
# Design Review Report

## Design System Health
- Tokens defined: Yes/Partial/No
- Consistency score: High/Medium/Low
- Component library: [name or custom]

## Issues Found

### Critical (Breaks usability)
| # | Category | Location | Issue | Fix |
|---|----------|----------|-------|-----|
| 1 | Contrast | header.tsx:12 | Text contrast 2.1:1 | Use text-gray-900 instead of text-gray-400 |

### Major (Hurts quality)
| # | Category | Location | Issue | Fix |
|---|----------|----------|-------|-----|

### AI Slop (Looks generic)
| # | Pattern | Location | Fix |
|---|---------|----------|-----|
| 1 | Uniform border-radius | All cards use rounded-xl | Vary: rounded-lg for cards, rounded-md for buttons |

### Minor (Polish)
| # | Category | Location | Issue | Fix |
|---|----------|----------|-------|-----|

## Responsive Check
| Breakpoint | Status | Issues |
|------------|--------|--------|
| Mobile (375px) | Pass/Fail | ... |
| Tablet (768px) | Pass/Fail | ... |
| Desktop (1280px) | Pass/Fail | ... |

## Positive Patterns
[Well-implemented design decisions worth preserving]
```

## Notes

- This review focuses on implementation quality, not design direction — it won't redesign your UI
- AI slop detection is about identifying patterns that look unintentionally generic, not banning specific styles
- If the project has a `DESIGN.md`, compare implementation against its defined tokens, colors, and component styles
- If the project has a Figma/design spec, compare implementation against it
- For accessibility-specific review, use `/accessibility-audit` which covers WCAG compliance in depth
- Requires reading the actual component/template code — not just CSS
