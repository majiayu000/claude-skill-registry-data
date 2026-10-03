---
name: accessibility-standards
description: >
  Use when creating any user-facing interface, content, or experience to ensure
  accessibility for users with disabilities. This skill provides WCAG-aligned
  standards for accessible design and development.
---

# Accessibility Standards

## Overview
This skill defines accessibility standards for creating inclusive user experiences. Accessibility is not optional - it's a legal requirement and moral obligation that also improves usability for everyone.

## When to Use
- When designing or building any user interface
- When creating documents or content for users
- When reviewing UI changes or designs
- When creating forms, navigation, or interactive elements
- **Don't use when:** Building purely backend services with no user interface

## Core Procedures

### Step 1: Accessible Markup
- All images have descriptive `alt` text
- Headings are hierarchical (h1 → h2 → h3, no skipping)
- ARIA labels on interactive elements without visible text
- Focus outlines are visible and logical
- Color is never the only indicator of state or meaning
- Language is specified in HTML/document

### Step 2: Keyboard Access
- All interactive elements operable via keyboard
- Tab order is logical and matches visual order
- Keyboard focus is always visible
- No keyboard traps (users can't get stuck)
- Shortcuts are documented and don't conflict with screen readers

### Step 3: Content Standards
- Text contrast ratio minimum 4.5:1 (3:1 for large text)
- Text resizeable up to 200% without loss of function
- Language is clear and avoids unnecessary jargon
- Links are descriptive (not "click here")
- Forms have associated labels and error messages
- Error messages identify the field and suggest correction

### Step 4: Testing
- [ ] Automated accessibility scan (aXe, Lighthouse)
- [ ] Keyboard-only navigation test
- [ ] Screen reader test (VoiceOver, NVDA, or TalkBack)
- [ ] Color contrast validation on all text/interactive elements
- [ ] Zoom test (200% zoom, no horizontal scroll required)

### Step 5: Documentation
Document any known accessibility limitations:
```
ACCESSIBILITY NOTE
==================
Issue: [what accessibility concern exists]
Affected Users: [who is impacted - screen reader, keyboard, visual]
Workaround: [what alternative is available]
Planned Fix: [if fix is planned, when]
```

## Quality Checklist
- [ ] Automated accessibility scan passes with zero errors
- [ ] Keyboard navigation works completely
- [ ] Screen reader announces content meaningfully
- [ ] Color contrast meets minimum standards
- [ ] Text is readable at 200% zoom
- [ ] All images have alt text
- [ ] Forms have labels and error handling

## Error Handling
- **Error:** Accessibility issue discovered after release
  **Response:** Triage severity, fix critical issues immediately, document known issues with workarounds
- **Error:** Third-party component has accessibility issues
  **Response:** Report to vendor, implement workaround, evaluate alternatives

## Cross-Team Integration
**Related Skills:** ui-ux-guidelines, testing-strategy, documentation-quality-check, feedback-integration
**Used By:** Design agents, frontend developers, UX agents, Content agents, QA testers