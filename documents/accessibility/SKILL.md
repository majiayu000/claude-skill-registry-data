---
name: accessibility
description: Make anything a person reads or operates accessible. Apply when building or changing an interface, or writing a document, dashboard, notebook, report, or Markdown page.
---

<!--
This file is part of Agentprise
Copyright © 2026 The Regents of the University of Michigan
Licensed under the GNU Free Documentation License v1.3 or later.
See <https://www.gnu.org/licenses/fdl-1.3.html>. See README for full license information.
-->

# Agentprise

## Accessibility

This skill expands section 9 of [AGENTS.md](../../AGENTS.md), which is
non-negotiable. Read that section and the
[project-preferences skill](../project-preferences/SKILL.md) first. This skill adds
detail; it cannot lower the target or waive a requirement.

Target WCAG 2.1 AA or 2.2 AA. The structure, perception, and reading rules below
apply to everything a person reads. The operation rules apply only to interfaces a
person drives, so skip them for command-line tools, scripts, and data pipelines
with no human interface.

### Structure

Structure comes from real structural elements, never from visual styling. Bold text
is not a heading in any format.

- **HTML:** use semantic elements such as `<main>`, `<nav>`, `<button>`, and
  `<table>` with `<th>` and `scope`. Never put a click handler on a `<div>` where a
  `<button>` belongs.
- **Markdown and documents:** real headings in order with no skipped levels, one H1
  per page, real lists, and tables with header rows. Standard pipe tables are
  accessible, so do not hand-write HTML tables in Markdown. Write descriptive link
  text such as "EFDC README template" rather than "click here".
- **Notebooks, Word, PowerPoint, and PDF:** use the built-in heading and list
  styles, set the document title and language, mark table header rows, and check
  reading order.
- **Images and diagrams:** give informative images meaningful `alt` text and
  decorative images empty `alt`. Every diagram, including Mermaid, needs an
  adjacent text description that carries the same information, because the rendered
  image carries none to a screen reader.

### Perception

Never use color alone to carry state, meaning, or a data series. Add text, shape,
pattern, or position as well. Keep contrast at 4.5:1 or better for normal text and
3:1 for large text, interface components, and graphical objects. Support 200% text
resize, and reflow at 320 CSS pixels wide without losing content or forcing
horizontal scrolling.

### Operation

Assume the person uses a keyboard only, a switch, voice control, or has a tremor or
limited fine motor control.

- Everything works from the keyboard, with no traps, a logical focus order, and a
  visible focus indicator.
- Pointer targets are at least 24 by 24 CSS pixels, which is the WCAG 2.2 AA
  minimum. Use 44 by 44 for touch when you can, and keep targets well separated.
- Any drag, swipe, or pinch gesture needs a single-pointer alternative such as a
  button or a text input.
- Complete actions on pointer-up so a mis-press can be aborted.
- Avoid time limits, and allow an extension where one is unavoidable. Do not
  auto-advance carousels, auto-dismiss important messages, or hide essential
  content behind hover.

### Reading and cognition

These help everyone, including dyslexic and ADHD readers.

- Chunk the content: short paragraphs, descriptive headings, one idea per
  paragraph, numbered steps, and a summary before the detail. Long unbroken prose
  is the biggest barrier.
- Left-align body text with a ragged right edge. Justified text creates uneven word
  spacing that is measurably harder to track.
- Keep lines around 80 characters or shorter. Use line height of at least 1.5
  within a paragraph and 2 between paragraphs, and never defeat a reader's own
  text-spacing settings.
- Choose a clean font with unambiguous letterforms for I, l, 1 and O, 0, such as a
  system interface font, Atkinson Hyperlegible, Verdana, or Tahoma. Evidence for
  specialized dyslexia fonts such as OpenDyslexic is weak and mixed, so offer a
  font choice rather than mandating one. Spacing, line length, alignment, and
  contrast matter more.
- Avoid all-caps beyond short labels, and avoid italics for long passages.
- In multi-step flows, show progress and state, preserve what the person typed,
  allow save and resume, and confirm destructive actions.
- Respect `prefers-reduced-motion`. Nothing flashes more than three times per
  second. Anything that moves or updates on its own needs pause, stop, and hide
  controls.
- Write plainly, following section 12 of `AGENTS.md` and the "Interface text"
  section of the [response-style skill](../response-style/SKILL.md).

### Verification

Automated tools such as axe, Lighthouse, and `pa11y` catch roughly a third of
issues, so always add manual checks: keyboard-only traversal, visible focus, 200%
zoom, and a screen reader pass on the main flows.

Report what you tested and what still needs a human, and never claim a check you
did not run. Put anything a person must still verify by hand under the
Accessibility heading of the response format in `AGENTS.md` section 14.

### Additional resources

- [Project instructions](../../AGENTS.md)
- [Response style skill](../response-style/SKILL.md)
- [Skills index](../../SKILLS.md)
- [WCAG 2.2 quick reference](https://www.w3.org/WAI/WCAG22/quickref/)
