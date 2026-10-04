---
name: design
description: Design user interfaces with exceptional UX patterns. Use when implementing screens, reviewing UI code, choosing loading states, handling errors gracefully, placing interactive elements, adding animations, or ensuring the app feels polished and intuitive. Focuses on user experience details that make apps feel professional.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Design - UI/UX Implementation

Create interfaces that feel intuitive, responsive, and delightful. Focus on the small details that distinguish polished apps from mediocre ones.

## When to Use This Skill

- Implementing new screens or components
- Reviewing UI code for UX issues
- Deciding between loading state patterns
- Placing buttons, CTAs, and interactive elements
- Handling errors and edge cases gracefully
- Adding animations and transitions
- Choosing animation timing and curves

## The Golden Rules

1. **Thumb-first design** - Primary actions in the bottom 2/3 of the screen
2. **Immediate feedback** - Every tap/action should have visible response
3. **Smart defaults** - Auto-focus, pre-fill, remember preferences
4. **Graceful failures** - Errors should guide, not blame
5. **Platform respect** - iOS swipe-back, Android gestures, Material patterns
6. **Purposeful motion** - Animate to communicate, not to impress

## Core Principles

### Every Action Deserves Feedback
Users should never wonder "did that work?" - provide visual press states, haptics, loading indicators, and success/error messages. See [interaction-guide.md](interaction-guide.md) for details.

### Auto-Focus Intelligence
Focus the right field at the right time - login screens should auto-focus email, search screens should auto-focus the search field. See [interaction-guide.md](interaction-guide.md) for the complete decision table.

### Error Recovery, Not Error Display
Errors should help users succeed. Instead of "Error: Invalid input", show "Email needs an @ symbol". See [visual-guide.md](visual-guide.md) for error state patterns.

### Touch Targets
Minimum 48×48dp for all interactive elements. See [interaction-guide.md](interaction-guide.md) for sizing guidelines.

### Purposeful Animation
Animation should communicate change, not decorate. Use 300ms for transitions, match curves to motion direction, and always respect reduced motion preferences. See [animation-guide.md](animation-guide.md) for timing, curves, and patterns.

## Quick Decisions

| Question | Answer |
|----------|--------|
| Loading for <300ms? | No indicator needed |
| Loading for 1-3s? | Skeleton screen |
| Button action? | Inline button loader |
| Full page load? | Skeleton matching layout |
| File upload? | Progress bar with percentage |
| Page transition duration? | 300ms (default) |
| Element entering screen? | Use `easeOutCubic` curve |
| Element leaving screen? | Use `easeInCubic` curve |
| Simple property change? | Use implicit animation (`AnimatedContainer`) |
| Complex animation? | Use explicit (`AnimationController`) |

## Workflow

1. **Before implementing**: Where will the user's thumb be? What's the primary action? What if it fails? What animations are needed?
2. **During implementation**: Touch targets ≥48dp, visual press states, appropriate loading pattern, natural animations.
3. **After implementation**: Review against the checklists below and test with reduced motion enabled.

## Guides

| Guide | Use For |
|-------|---------|
| [interaction-guide.md](interaction-guide.md) | Touch targets, gestures, focus, keyboard, haptics |
| [visual-guide.md](visual-guide.md) | Colors, loading states, dark mode, empty states |
| [animation-guide.md](animation-guide.md) | Timing, curves, page transitions, Hero, performance |
| [platform-guide.md](platform-guide.md) | iOS vs Android conventions |
| [examples.md](examples.md) | Complete Flutter code patterns |

## UX Checklist

- [ ] Primary action in thumb-friendly zone
- [ ] All touch targets ≥48dp
- [ ] Every interactive element has feedback
- [ ] Loading state matches operation type
- [ ] Error messages explain AND guide
- [ ] Works in light and dark mode
- [ ] iOS swipe-back not blocked
- [ ] Accessibility: labels, focus order, reduced motion (see [interaction-guide.md](interaction-guide.md))

### Animation Checklist

- [ ] Page transitions feel natural (300ms default)
- [ ] Curves match motion type (easeOut for enter, easeIn for exit)
- [ ] List items animate in (staggered for many items)
- [ ] Loading → content transition is smooth
- [ ] Reduced motion preference respected
- [ ] AnimationControllers properly disposed

## Accessibility Integration

This skill focuses on visual/interaction design. For comprehensive accessibility:

- **Semantic labels**: Use `/a11y` skill for Semantics widget patterns
- **Screen reader testing**: See [../a11y/testing-guide.md](../a11y/testing-guide.md)
- **WCAG compliance**: See [../a11y/SKILL.md](../a11y/SKILL.md) for guidelines

Key accessibility requirements covered by design:
- Touch targets ≥48dp (see [interaction-guide.md](interaction-guide.md))
- Color contrast ≥4.5:1 (see [visual-guide.md](visual-guide.md))
- Reduced motion support (see [animation-guide.md](animation-guide.md))

## Related Skills

- `/a11y` - Comprehensive accessibility (Semantics widgets, screen readers)
- `/feature-init` - Initialize feature scaffold before polishing
- `/i18n` - Localize user-facing text, error messages
- `/testing` - Widget tests for UI interactions
