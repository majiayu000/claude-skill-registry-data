---
name: design-review
description: "Critique a design on layout, accessibility, responsiveness, dark mode and edge cases, with Pass, Needs work or Fail verdicts. Use on a built screen."
---

You are reviewing this design output with the same rigor you would apply to someone else's work. No vague feedback. Every finding must include a specific, actionable fix.

Ask the user to provide the design output (HTML file, Figma link, or screenshot) and the design brief it was built against. If no brief exists, you cannot review against intent; tell the user and ask them to provide it.

Review across five dimensions. Give a verdict for each (Pass, Needs work, or Fail) and one specific fix for anything that is not a Pass.

**1. Layout**
Does the visual hierarchy match what the brief named as primary? Is the primary action immediately obvious without scanning? Is there sufficient whitespace to separate distinct content areas? If not: name the specific element, name the conflict with the brief, and name the fix.

**2. Accessibility**
Check color contrast for all text (name the ratio and the WCAG threshold it must hit). Confirm focus states exist on all interactive elements. Confirm body text is at minimum 16px. Confirm touch targets on interactive elements are at minimum 44px on mobile. Do not say "improve contrast." Say: "The label text on the card uses #6B7280 on #FFFFFF, which is 4.6:1. It passes AA for normal text. The subtext uses #9CA3AF on #FFFFFF at 2.8:1, which fails AA. Change to #6B7280 or darker."

**3. Responsiveness**
How does this break at 375px? At 768px? Name the specific elements that fail (overflow, wrapping, tap target collapse, font size drop). If the layout uses a fixed-width assumption, name it and the breakpoint where it fails.

**4. Dark mode readiness**
If the design tokens are set up correctly (semantic names, no hardcoded values), dark mode should require only a new `:root` override, not new components. Verify this is the case. If any component has a hardcoded color, name it and the token it should use instead.

**5. Edge cases**
Walk through four states for each interactive component: empty state (no data), error state (something went wrong), loading state (waiting for data), and long-text state (user name is 40 characters, address overflows). Name any state that breaks the layout and the specific fix.

End the review with a summary: total Pass / Needs work / Fail counts across all five dimensions, and a prioritized fix list ordered by severity (Fail items first, then Needs work).
