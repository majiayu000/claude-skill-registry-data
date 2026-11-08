---
name: page-review
description: "One-pass quality review of the user's pages, print templates and the Claude panels: accessibility, layout, readability, color contrast, motion, print, and interface copy. Use after any change to how one of them looks or behaves, or when the user asks whether a page looks right."
user-invocable: false
---

# Page review

Review against `.claude/skills/page-design/SKILL.md` and its `references/` (the rules) and report evidence, not taste. A deliberate design choice you'd have made differently is not a finding; a failed check below is, even if a style rule allowed it. Read-only unless the user asked for fixes.

Scope: name exactly what you reviewed (which pages, which panel, which states). Cover the empty, loading, error and narrow-width states where they exist. At most 15 findings; blockers always come first and are never cut by the cap.

## Severity

- **HIGH** (blocker, fix before the user sees it): blocks a task, misleads, hides content or a control, risks losing data, or repeats across pages.
- **MEDIUM:** makes something meaningfully harder to read, use or keep consistent.
- **LOW:** isolated polish.

These are always HIGH:
- A control with no visible/accessible name, or text the same color as its background (check `@layer components`).
- Something reachable by mouse but not keyboard; no visible focus ring; focus lost after an action.
- Text below its contrast target (`.claude/skills/page-design/references/color.md`) in light **or** dark; state or meaning shown by color alone; a status color used against its meaning (danger red on a harmless button).
- Content cut off with no way to read it; horizontal page scroll at 320px or 200% zoom; content hidden past a scroll edge or in a collapsed section with no cue.
- Motion that ignores reduced-motion; content invisible until an animation runs; a change shown only by motion.
- A destructive action (discard, clear, send, delete) with no confirmation or undo.
- An error that doesn't say how to fix it; a button that does nothing.
- The brief printing on more than one page in the `sheet` layout (or more than two in `detailed`), or the resume running past the length `tailor-resume` set for it (one page by default).
- A resume or cover letter that breaks its ATS rules, or a designed resume made instead of (not alongside) the ATS one.
- A made-up fact about the user (run `truth-checker` on page text built from their files).
- A photo, date of birth or marital status on a resume or CV the user didn't choose to add (ground rule 4).

## Which checks to load

Read only the file for the surface you are reviewing, plus the copy rules:
- Pages (dashboard, flashcards, portfolio, interview briefs) and print templates (resume, cover letter, designed resume, academic CV, US federal resume, Europass-style CV): `references/pages-and-print.md` (15 checks: structure, keyboard, names, hit areas, forms, color, type, layout, motion, print, theme and audience, every layout, offline assets, data block safety).
- Panels (Outbox, Pipeline, Contacts, Job Inbox, Apply Kit, Interview Room, Insights, Routines, Celebration, due alerts): `references/panels.md` (copy, keyboard, hit areas, states, terminal colors, limits, plugin validate/test).
- Always: `references/copy.md` (buttons, confirmations, errors, tone, empty states, one word per thing, plurals).

## Fixing

Prefer the cheapest fix that works, in this order: delete (a line, an animation, an ARIA attribute the native element already covers) → use the platform (native element, browser focus ring) → reuse an existing token or shared class → correct a value → add something new. Fix the root cause (usually a token or shared class) once, then re-check every place it appears.

## Verifying in a browser (when available)

In the Claude Desktop app, the built-in browser is the easiest way to look: open the page there, take a screenshot, and check both light and dark mode. Some versions only open web addresses, not files on the computer; if a page won't open there, don't keep trying: use headless Chrome below, or give the user the file path to double-click (on a Mac, `open <file>`).

If Chrome is installed, Claude can render without opening a window, e.g. on a Mac:
`"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --virtual-time-budget=6000 --window-size=1280,1400 --screenshot=out.png file:///path/to/page.html`
Add `--blink-settings=preferredColorScheme=0` for dark, or use `--no-pdf-header-footer --print-to-pdf=out.pdf` for print. Headless windows are at least ~500px wide, and animations may be captured mid-flight, which is a reason to keep resting states readable. Mark anything you couldn't check as "Not verified"; never report it as a finding or as passing.

## Report

Scope line (what you looked at, which states). Then one table, blockers first, one row per root cause listing every place it occurs: Severity · Where (file:line) · Problem · Fix. Then what you verified (the command or steps and the result) and what you couldn't. End with "Ready" (no HIGH left) or "Needs fixes". With nothing to report, say so and list what you checked.
