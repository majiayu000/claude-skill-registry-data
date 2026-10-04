---
name: UI
description: Design clear, consistent, and visually polished user interfaces.
metadata: {"clawdbot":{"emoji":"🎨","os":["linux","darwin","win32"]}}
---

## Visual Hierarchy

- One focal point per screen—eye knows where to go first
- Size, color, weight establish importance—primary action most prominent
- Group related elements—proximity implies relationship
- White space is not wasted space—breathing room aids scanning

## Typography

- Maximum 2-3 font families—more creates visual noise
- Clear size scale: title > heading > body > caption—distinct steps, not gradual
- Line height 1.4-1.6 for body text—too tight or loose hurts readability
- Line length 45-75 characters—prevents eye fatigue
- Left-align body text—centered only for short headings

## Color Usage

- Primary color for primary actions—one dominant brand color
- Semantic colors consistent: red=error, green=success, yellow=warning
- Don't rely on color alone—add icons, text, patterns for accessibility
- Neutral palette for most UI—color for emphasis, not everywhere
- Test color blindness scenarios—8% of men affected

## Spacing System

- Use consistent scale: 4px, 8px, 16px, 24px, 32px, 48px
- Apply same spacing for same relationships—all card padding equal
- More space around groups than within—visual grouping through proximity
- Generous padding on touch targets—44px minimum for mobile

## Alignment

- Grid system for consistency—8px or 4px base grid
- Align to invisible lines—elements share edges, not scattered
- Left edge strongest for LTR—anchor content predictably
- Optical alignment when needed—visual center differs from mathematical

## Component States

- Default, hover, active, focus, disabled—all states designed
- Focus state visible and clear—keyboard users need this
- Disabled looks disabled—reduced opacity, no pointer cursor
- Loading state replaces content—not just overlay
- Error state in context—red border, inline message

## Icons

- Consistent style throughout—don't mix outlined and filled
- Recognizable at small sizes—simple shapes work better
- Labels when meaning ambiguous—icon + text clearer than icon alone
- Touch target larger than visual icon—44px tap area, 24px icon

## Imagery

- Consistent aspect ratios—don't stretch or skew
- Fallback for failed loads—placeholder, not broken image
- Alt text for content images—decorative images alt=""
- Compress appropriately—quality vs file size balance

## Responsive Design

- Design for smallest screen first—enhance for larger
- Breakpoints based on content—not arbitrary device widths
- Touch targets larger on touch screens—hover states only on desktop
- Consider landscape orientation—especially for tablets

## Dark Mode

- Not just color inversion—redesign depth and emphasis
- Reduce contrast slightly—pure white on black strains eyes
- Shadows don't work same—use lighter surfaces for elevation
- Test all states—errors, success, charts, images
- Respect system preference—but allow override

## Motion and Animation

- Duration 150-300ms for transitions—fast but perceptible
- Ease-out for entering—starts fast, settles in
- Ease-in for exiting—accelerates out of view
- Consistent timing across similar interactions
- Purpose: guide attention, show relationships, provide feedback

## Design Tokens

- Define tokens for colors, spacing, typography—single source of truth
- Semantic naming: `color-error` not `color-red`
- Enables theming and dark mode—swap token values
- Scales with product—change once, update everywhere

## Common Mistakes

- Too many font sizes—stick to the scale
- Inconsistent spacing—creates unpolished feel
- Low contrast text—4.5:1 minimum for accessibility
- Buttons that don't look clickable—affordance matters
- Different styles for same component—cards should match cards
