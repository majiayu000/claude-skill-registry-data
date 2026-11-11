---
name: visual-review
description: End-to-end visual QA of work that was just done or of a named part of the app. Discovers how to run, log in to, and exercise the app from the codebase, captures screenshots with agent-browser, reports severity-ranked findings, and implements the fixes. Use whenever the user asks to check how changes look, verify UI work in a real browser, visually review a screen or feature, or run visual QA — even if they never say "visual QA" or "screenshots".
---

# Visual Review

Review **real rendered UI** in a browser, judge it against the project's own
visual standards, and fix what is clearly wrong. The output is working,
verified UI plus a severity-ranked report — not a pile of design advice.

## 1. Establish scope

Decide what to review before opening anything:

- **Explicit area named** ("the settings page", "the onboarding flow"):
  locate its routes, screens, and components in the codebase.
- **No area named**: default to the changes just made. Use `git status`,
  `git diff`, and recent commits to find touched UI files, then map them to
  the routes and screens where they render. Review only those screens — a
  full-app sweep when the user asked about their change wastes time and
  buries the relevant findings.

Note which UI states the scope implies (empty, loading, error, populated,
selected) so you exercise them deliberately rather than only the happy path.

## 2. Discover how to test it

Before any browser work, learn the project's own way of running and judging
its UI. Answer three questions from the codebase:

**How do I run it and log in?**
Check, in rough priority order: a visual QA or testing runbook in the repo
root or `docs/` (e.g. `VISUAL_QA.md`, `TESTING.md`); README, `AGENTS.md`,
`CLAUDE.md`, `CONTRIBUTING`; package scripts (`dev`, `start`, `storybook`,
`ladle`); e2e test setups (Playwright/Cypress configs often contain working
login helpers, test users, and seed commands); `.env.example` for required
config. Reuse an already-running dev server if one is up.

**How should it look?**
Look for design and UX documentation: files like `UX.md`, `DESIGN.md`,
`docs/ux/*`, style guides, design tokens, and theme definitions. Treat
documented rules as the source of truth. Existing screens are useful
evidence of intended patterns, but documented rules win over observed
habits.

**What components should it use?**
Identify the project's component library (MUI, shadcn, an internal design
system, a shared `components/` directory) and its conventions. A change that
hand-rolls a button or table when the project has a canonical one is a
finding, even if it renders fine.

Hard limits — these protect the validity of the review:

- Only use login/session flows that the project documents or its own tests
  use for automation. Never bypass auth, invent credentials, or ask for or
  expose secrets.
- Render through real app routes or a documented component explorer with the
  app's actual providers, theme, router, and data setup. Do not build an ad
  hoc render harness — it will not show what users see.
- If running or logging in is genuinely impossible from what the codebase
  provides, stop and report exactly what is missing (and suggest documenting
  it in a project runbook) instead of guessing.

## 3. Run and capture

Use `agent-browser` for browser automation. If an agent-browser skill or
reference doc is available, load it first; otherwise check
`agent-browser --help` for the current CLI workflow. Then:

1. Start the documented dev command (or reuse the running server).
2. Navigate to each in-scope route and drive the UI to each relevant state.
3. Screenshot every screen/state you evaluate. Capture desktop by default,
   and a narrow viewport (~375px) whenever the scope includes layout, nav,
   forms, or anything that must wrap or stack. Capture both themes if the
   app ships dark and light modes and the change touches themed surfaces.

Findings must be grounded in a captured screenshot — if you did not see it
rendered, it is a hypothesis, not a finding.

## 4. Evaluate

Judge the screenshots against the discovered UX docs, tokens, and component
conventions first, then against these fundamentals:

- Alignment and spacing: row/centerline alignment, regional edge alignment,
  related elements closer than unrelated groups.
- Hierarchy: one clear primary action per screen or region; typography scale
  and readable line lengths; scannable focal points.
- States: default, hover/focus, disabled, loading, empty, error, selected —
  each clear and distinct where the scope covers it.
- Responsive behavior: rows, filters, nav, forms, and actions wrap or stack
  sanely; long labels, values, chips, and URLs truncate or wrap on purpose.
- Accessibility basics: contrast, focus visibility, touch-target size,
  labels on icon-only controls.
- Color semantics: error/warning/success/destructive/primary used
  consistently with the rest of the app.
- Component consistency: repeated roles use the same component; the change
  uses the project's canonical components rather than one-off lookalikes.

Also flag generic AI/SaaS tropes unless the user, the project's design
docs, tokens, or a clearly consistent existing pattern justifies them:
unexplained gradients and glows, glassmorphism, gratuitous cards and
shadows, oversized pills, bento grids, fake stats or filler copy,
decorative motion. Treat these as real findings, not optional polish.

## 5. Rank findings by severity

Classify every finding:

- **Critical** — broken or unusable: content unreadable or clipped away,
  control unreachable, layout collapsed, action impossible.
- **High** — clearly wrong: violates documented UX rules or component
  conventions, failing contrast, broken responsive behavior, misleading
  state.
- **Medium** — noticeably off: misalignment, spacing inconsistencies, weak
  hierarchy, missing hover/focus/empty states.
- **Low** — polish: minor visual nits a careful reviewer would mention.

Each finding records: severity, the screenshot showing it, the screen/state,
what was expected (citing the doc/token/convention when one exists), what
was observed, and the proposed fix. Mark a finding **Needs decision** instead
of assigning a fix when the right answer depends on intent — e.g. an
undocumented pattern that might be deliberate.

## 6. Implement the fixes

Fixing is the default ending, not an optional extra. Skip it only when the
user asked for a report/review only.

- Fix Critical and High findings, and Medium ones whose fix is unambiguous.
  Follow the project's conventions and components — a fix that introduces a
  new pattern creates the next finding.
- Leave **Needs decision** items and judgment-call Lows unfixed; surface them
  for the user instead.
- After fixing, re-capture screenshots of the affected screens and confirm
  the issue is gone without regressing neighbors. A fix is only done when
  verified in the browser.
- Keep changes small and reviewable — group fixes by screen or concern, not
  one sweeping diff.

## 7. Report

End with a concise report:

1. **Scope reviewed** — routes/screens, states, viewports, screenshot paths.
2. **How it was tested** — run/login path used; UX docs, tokens, and
   component conventions consulted (or "none found").
3. **Findings** — severity-ordered list, each marked `Fixed (verified)`,
   `Needs decision`, or `Not fixed` with the reason.
4. **Blockers** — anything that limited the review: missing docs, auth,
   data, states that could not be reached.
