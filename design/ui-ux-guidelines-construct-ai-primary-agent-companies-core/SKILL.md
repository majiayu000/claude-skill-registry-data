---
name: ui-ux-guidelines
description: >
  Use when designing or building any user interface to ensure consistency, usability,
  and visual quality across all user-facing applications. This skill provides core
  UI/UX principles and standards for the enterprise ecosystem.
---

# UI/UX Guidelines

## Overview
This skill defines UI/UX standards for consistent, usable, and visually coherent interfaces across all user-facing applications. Good UI/UX reduces user errors, increases satisfaction, and reflects quality in the product.

## When to Use
- When designing new screens, pages, or components
- When building or modifying existing user interfaces
- When reviewing UI designs or implementations
- When creating or updating design systems
- **Don't use when:** Building backend-only services with no user interface

## Core Procedures

### Step 1: Visual Hierarchy
- Most important elements are most prominent
- Related elements grouped visually
- Clear distinction between primary and secondary actions
- Use size, color, spacing, and weight to guide attention
- Maximum 3 levels of hierarchy per screen

### Step 2: Layout Standards
- Consistent grid system across all screens
- Adequate whitespace (minimum 8px base unit)
- Content aligned to consistent columns
- Maximum content width for readability (80-100 characters per line)
- Responsive breakpoints: mobile (<768px), tablet (768-1024px), desktop (>1024px)

### Step 3: Interaction Patterns
- Buttons have clear primary/secondary/danger states
- Loading states always shown during async operations
- Success/error confirmation after user actions
- Undo available for destructive actions
- Consistent interaction for common patterns (forms, lists, dialogs, navigation)

### Step 4: Content Guidelines
- Use plain language, avoid technical jargon
- Error messages tell users what happened AND how to fix it
- Labels are action-oriented ("Save changes" not "Submit")
- Empty states explain what to do next
- Confirmation dialogs state what will happen clearly

### Step 5: Color and Typography
| Level | Usage | Example |
|-------|-------|---------|
| Primary Actions | Main call-to-action | Save, Submit, Create |
| Secondary Actions | Alternative actions | Cancel, Back, Skip |
| Danger Actions | Destructive actions | Delete, Remove, Revoke |
| Information | Status, hints, help text | Info boxes, tooltips |
| Success | Positive confirmations | "Saved", "Complete" |
| Warning | Caution, potential issues | "Unsaved changes" |

Typography:
- Maximum 3 typeface sizes per screen
- Body text minimum 14px, headings scale 1.25x

### Step 6: Component Consistency
- Use shared component library where available
- Custom components follow existing patterns
- Spacing, colors, and behavior consistent with design system
- States (disabled, loading, error) visually distinct

## Quality Checklist
- [ ] Visual hierarchy clearly guides user attention
- [ ] Layout is responsive and works at all breakpoints
- [ ] All interactive elements have visible states
- [ ] Error/success/loading states handled
- [ ] Content uses plain language
- [ ] Colors used semantically and consistently
- [ ] Typography follows type scale

## Error Handling
- **Error:** UI breaks at certain screen sizes
  **Response:** Test at all breakpoints, fix responsive behavior, add regression test
- **Error:** Component looks inconsistent with rest of app
  **Response:** Check design system, align with shared components, update custom styles

## Cross-Team Integration
**Related Skills:** accessibility-standards, element-styling-reference, testing-strategy, feedback-integration
**Used By:** Design agents, frontend developers, UX specialists, creative agents, UI agents, Dev (Loopy AI)