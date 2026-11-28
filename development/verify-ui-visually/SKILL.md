---
name: verify-ui-visually
description: Verify UI changes by rendering and looking — screenshot, browser, or running app — never by reading the markup and imagining it. Use after any change to components, styles, CSS, layouts, templates, charts, emails, PDFs, or generated documents/images, and when a user says "it looks wrong", "check the page", or asks for a visual fix. Not for pure logic changes with no rendered output.
---

# verify-ui-visually

Weak UI verification looks like: edit the markup, run the type-check, imagine the result, report "done". Strong verification puts pixels in front of your eyes and reports what they show. Code that compiles tells you nothing about what the user sees.

1. **Capture a baseline first.** Before editing, screenshot the affected screen (or its unchanged sibling) at the viewport you will test. Without a before, you cannot tell a regression you introduced from a quirk that was already there.
2. **Render it and look at it.** Run the dev server and take a screenshot (browser tooling, `mcp__chrome-devtools__take_screenshot`, or the project's snapshot setup); open the generated PDF/image/email HTML in a real viewer. Reading the diff is not seeing the output.
3. **Confirm you are looking at your change.** Find a string or selector from your diff in the rendered DOM or page text before judging pixels. An unchanged screenshot means a stale build, cached page, or wrong route until proven otherwise — fix that before concluding the change is a no-op.
4. **Look at the actual pixels critically:** overflow and truncation, misalignment, spacing collapse, z-index sandwiches, contrast, loading and empty states — the bugs no test asserts and every user notices instantly.
5. **Check the states, not just the happy render:** empty (zero items), loaded (typical), overloaded (long strings, many items — "WWWWWWWW" and a 200-char title), error, and loading. Most layout breaks live in empty and overloaded.
6. **Check both themes and at least two widths** when the project supports them: light/dark, mobile/desktop breakpoint. A change verified only in dark-mode desktop ships broken for half the users.
7. **Interact, don't just render:** click the button you changed, submit the form, tab through for focus order. Console errors during the interaction count as failures even when the screen looks fine.
8. **When you can't render** (no display, missing env), say so explicitly and downgrade the claim: "markup changed as requested; not visually verified — needs a look at /settings in the browser."

**Report format:** name the screenshot files, the viewport(s) and theme(s) checked, and describe in words what you saw ("badge now sits on the baseline; long titles truncate with an ellipsis at 320px"). "Screenshot taken, looks good" is not a verification — it is the claim you were supposed to check.

Rule: a UI change reported as done carries either a screenshot-verified description or a stated inability to verify. Never the silent middle.
