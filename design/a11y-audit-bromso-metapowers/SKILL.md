---
description: Run a comprehensive WCAG accessibility audit on a Figma component or frame
---

# Accessibility Audit

Run a full WCAG accessibility audit on a Figma component or frame, covering design lint, contrast, color blindness, and focus order.

## Process

1. **Identify the target.** The user should provide a component name, node ID, or indicate the current selection.

2. **Run all accessibility checks:**
   - Call `figma_a11y_lint` with the target node ID to check text size, touch targets, and image alt text
   - Call `figma_a11y_scorecard` with the target node ID for an overall scorecard
   - Call `figma_a11y_focus_order` with the target node ID to validate tab order

3. **Check color contrast.** For each foreground/background pair found:
   - Call `figma_a11y_contrast_check` with the color values and size "normal"
   - Call `figma_a11y_contrast_check` with size "large" for large text

4. **Simulate color blindness.** For the primary color pairs:
   - Call `figma_a11y_color_blind_sim` for protanopia, deuteranopia, and tritanopia
   - Note any pairs that lose sufficient contrast under simulation

5. **Compile the audit report:**
   - Summary: total checks run, pass/fail counts
   - Lint issues (text too small, touch targets, missing alt text)
   - Contrast results (AA/AAA pass/fail per pair)
   - Color blindness results
   - Focus order analysis
   - Remediation recommendations

6. **Present the report** to the user.

## Output

A comprehensive accessibility audit report presented to the user with actionable remediation steps.
