---
name: design-polish
description: Use when building or changing a user interface (HTML, CSS, JSX/TSX, Vue, Svelte, a Creator artifact). Run Shodh's design check, fix what it finds in order of harm, keep the project's own look, and finish with a clean check.
license: Apache-2.0
metadata:
  bundled-by: Shodh
  sources: pbakaus/impeccable (polish, audit)
---

# Design polish

A page that works can still be hard to read, impossible to use with a
keyboard, or look like every other generated page. Polish is refinement, not
a hidden redesign: keep the project's look, words and behaviour, and fix what
is wrong.

Fourth of Shodh's six building skills, for UI work (plan-before-building →
test-first → debug-systematically → **design-polish** → verify-before-done →
fresh-eyes-review). It comes before verify-before-done, so the design fixes are
built, tested and reviewed like any other change.

## The check

Shodh's `design_check` tool reads UI files with fixed rules (no model) and
shows its findings to the user in the code pane. Shodh also runs it on the UI
files you changed after you write them, so the user sees a "Design check: 3
issues" badge either way.

- Give it a file or folder (`path`), or an artifact (`artifact_id`).
- Each finding has a rule, a severity, a file:line and a suggested fix. Some
  carry an exact one-line replacement: a proposal, made only with your edit
  tool, never without the edit's normal approval.
- A finding is evidence to check, not proof. Read the cited line before
  changing it, and say so when a rule is wrong for this case.

If `design_check` is not among your tools, ask the user to run "Design check"
from the code pane or the Artifacts page.

## Order of work

Fix in this order, and do not perfect one corner while the rest stays broken:

1. **People cannot use it** (errors): images without alt text, fields without
   labels, buttons with no name, clickable divs, focus outlines removed.
2. **People cannot read it**: low contrast, text under 12px, tight line
   height, crushed or wide letter spacing, justified or all-caps paragraphs.
3. **It looks unfinished or generated**: Lorem ipsum, placeholder images,
   emoji used as icons, purple-to-blue gradients, gradient text, side-tab
   borders, glows, marketing buzzwords.
4. **It is not one system**: too many radii, type sizes or the same spacing
   everywhere. Use the project's scale; add a value to it only when it is
   reused.

## How to fix

- Use the project's own tokens, components and icon set first. Classify each
  problem: a missing token, a one-off that a shared component should replace,
  or a local slip. Fix it at the narrowest level that is right.
- Text is at least 12px everywhere; body text 14px to 16px.
- Plain words on labels and buttons. An icon sits to the left of its label;
  an icon alone needs `aria-label`.
- Every control has a visible focus style, a hover style and a disabled
  style. Keyboard order follows the reading order.
- Show the shortcut a control has (from the app's shortcut list) next to it,
  never a made-up one.
- Never undo what the user explicitly asked for (a font, a colour, a gradient,
  an emoji they chose), even when a rule flags it. Keep it, and say which
  findings you left for that reason.
- Ask before changing claims, product copy or anything outside the request.

## Finish

1. Run `design_check` on the files you changed. Repeat until no errors or
   warnings remain, or each one left is explained.
2. Then follow verify-before-done: build, run the checks and the tests.
3. Tell the user what you fixed, what you left and why. A clean check does
   not replace looking at the page: say what you could not see.

## Rules that do not bend

- The design check changes nothing. Every fix goes through your edit tool and
  its approval.
- Never remove a feature, a state or content to make a finding go away.

## Sources and credit

Rewritten for Shodh from **pbakaus/impeccable**, commands `polish` and `audit`
(https://github.com/pbakaus/impeccable, commit
a90602e9f6fed600d6d9b18cf78275d66cac7a6c), Apache License 2.0, Copyright 2025
Paul Bakaus. See `LICENSE-impeccable.txt`. Changed by Shodh: the polish pass
and the audit's accessibility and integrity checks are condensed into one
order of work, the detector is Shodh's own Rust port run through
`design_check` (impeccable's scripts, browser capture, critique snapshots and
scores are not used), and the user's interface rules (12px floor, plain words,
icons left of labels, shortcut hints) are added.
