---
name: heuristic-analysis
description: Evaluate a page or component against Nielsen's 10 Usability Heuristics and produce a structured findings report. Use when asked for a heuristic analysis, UX review, or usability check.
icon: fact_check
displayDescription: "Evaluates a page or component against Nielsen's 10 Usability Heuristics. Takes screenshots in light and dark mode, reads the source code, then produces a structured findings table with severity ratings (Pass / Minor / Moderate / Critical) and specific fix suggestions."
invoke: ["heuristic analysis of [page]","UX review of [page]","usability check on [component]"]
---

# heuristic-analysis

Evaluate a page or component against Nielsen's 10 Usability Heuristics and produce a structured findings report.

## When invoked

Use this skill when asked to run a UX or usability review — phrases like "heuristic analysis of [page]", "UX review of [page]", "usability check on [component]", "how does [X] score on usability".

## Instructions

1. **Determine scope.** Accept one of:
   - A website URL path (e.g. `/components/button`) → review the live page
   - A component name (e.g. `AlertDialog`) → review the component source and its rendered output

2. **Gather visual evidence.** Start the preview server and screenshot the target in both light and dark mode (follow the `visual-review` skill pattern). Stop the server when done.

3. **Read the source code** for the page or component to understand the full implementation, not just what's visible in screenshots.

4. **Evaluate against each of Nielsen's 10 Heuristics.** For each, assign a severity:
   - ✅ **Pass** — fully satisfied, no issues
   - ⚠️ **Minor** — small gap, low user impact
   - 🔶 **Moderate** — noticeable issue, degrades experience
   - 🔴 **Critical** — breaks usability, must fix

   **The 10 Heuristics:**
   1. **Visibility of system status** — Does the UI communicate what's happening? (loading states, active states, progress indicators, feedback on interaction)
   2. **Match between system and real world** — Do labels, icons, and concepts match the user's mental model? (plain language, familiar metaphors, no jargon)
   3. **User control and freedom** — Can users undo, cancel, go back, or exit? (close buttons, undo actions, Escape key support on overlays — for modal overlays, check against the shared contract in design.md's Components intro before raising a finding: a non-dismissible top layer swallowing Escape, and a lower overlay not closing through a blocking modal, are both by design)
   4. **Consistency and standards** — Are patterns applied uniformly? (same component behaves the same way everywhere, no contradictory conventions)
   5. **Error prevention** — Does the UI prevent mistakes before they happen? (confirmation dialogs for destructive actions, disabled states, validation hints before submission)
   6. **Recognition rather than recall** — Are options visible rather than requiring memory? (labels on icon-only buttons, visible choices, no hidden commands)
   7. **Flexibility and efficiency of use** — Can experienced users work faster? (keyboard shortcuts, compact modes, sensible defaults)
   8. **Aesthetic and minimalist design** — Is every element necessary? (no redundant labels, no visual noise, appropriate information density)
   9. **Help users recognise, diagnose, and recover from errors** — Are error messages plain, specific, and constructive? (not just "Something went wrong")
   10. **Help and documentation** — Are tooltips, placeholder text, or inline guidance provided where genuinely needed?

5. **Produce a structured report:**

   ```
   ## Heuristic Analysis: [Page/Component Name]

   | # | Heuristic | Severity | Finding |
   |---|-----------|----------|---------|
   | 1 | Visibility of system status | ✅ Pass | — |
   | 2 | Match with real world | 🔶 Moderate | Submit button gives no feedback after click — add loading state |
   ...

   ### Findings requiring action
   [Only Minor/Moderate/Critical items, each with a specific fix suggestion]

   ### Summary
   X critical · Y moderate · Z minor · W passing
   ```

6. **Be specific.** Reference the exact element, prop, or file where possible. A finding like "the Dismiss button in Gadget has no visible focus ring (Gadget.css:47)" is more useful than "focus styles are missing". (The component in that example is fictional by design — a factual claim about a real component inside an example rots silently.)
