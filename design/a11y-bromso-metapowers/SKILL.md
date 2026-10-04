---
description: Review work through the lens of an accessibility specialist
---

# Accessibility Coaching

Review "$ARGUMENTS" through the lens of an accessibility specialist. Provide mentorship feedback on inclusive design, WCAG compliance, and assistive technology compatibility.

## Prerequisites

None — this is a utility skill that can run anytime.

## Process

1. **Read the target:**
   - Read the file, component, or content specified in "$ARGUMENTS"

2. **Check for project accessibility context:**
   - Look for `.metapowers/accessibility/` directories for prior audit results
   - If the accessibility plugin's shared resources exist, read `plugins/accessibility/shared/wcag-21-aa-criteria.md`

3. **Read reference material:**
   - Read `plugins/coaching/shared/feedback-format.md` for output structure

4. **Evaluate for accessibility:**
   - **Perceivable:** Alt text, captions, contrast, text resize, content reflow
   - **Operable:** Keyboard access, focus management, no traps, timing, navigation
   - **Understandable:** Language, predictability, input assistance, error messages
   - **Robust:** Valid markup, ARIA usage, name/role/value, status messages
   - **Inclusive design:** Does it work for users with visual, auditory, motor, and cognitive disabilities?
   - **Assistive technology:** Will it work with screen readers, switch devices, voice control?

5. **Write the coaching report** to `.metapowers/coaching/$ARGUMENTS/a11y-review.md` following the feedback format.

## Output

The accessibility coaching report written to `.metapowers/coaching/$ARGUMENTS/a11y-review.md`. Present the score and top 3 suggestions to the user.
