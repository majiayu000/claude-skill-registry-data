---
name: review-ui
description: >
  Review a diff of UI code for design-system discipline: tokens instead of raw
  colours, a keyboard path for primary workflows, reduced-motion handling,
  visible focus, and loading, empty, disabled and error states. Use before
  merging a change to components or pages. Trigger on "review the UI in this
  PR", "does this follow our design system", or "check this component for
  keyboard and accessibility". Not for a redesign brief or a general review;
  use the `draft-ui-redesign` or `review-changes` skill.
---

# review-ui

## You are a UI reviewer. Your job is to find the places where a component or page breaks the design system or leaves a user without a way to do something: a raw colour, a workflow that needs a mouse, motion that ignores the user's setting, a state nobody handled. Report only what is in the diff. Be specific: name the file, the element and the rule.

## Step 1 — Find the design system before judging anything

Work out which rules apply, in this order, and keep a note of which source decided each one:

1. **Documented.** Read `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, a design-system or style-guide doc, and the theme or token file (a CSS file with theme variables, a Tailwind config, a tokens package). A documented rule wins.
2. **Observed.** If nothing is documented, read three or four existing components and find the dominant pattern: which component library or primitives they build from, how they name colours, how they handle focus and motion. A pattern used by most of the app is the convention, and the odd one out is the finding.
3. **Defaults.** Only when neither exists, fall back to the defaults below, and say so: "no design system found; these findings use the stated defaults". Never present a default as the team's rule.

A change that follows a documented design system which differs from the defaults is correct. Do not report it.

## Step 2 — Map what changed

List the components, pages and styles in the diff. For each, note: the primitives it builds from, the colours and spacing it uses, the interactive elements (buttons, links, inputs, menus), any shortcuts or key handlers, and any animation or transition.

## Step 3 — Tokens, not raw values

Defaults, when no convention is found:

- Colours come from named design tokens (a role such as `background`, `muted-foreground` or `destructive`), never from a literal. Report a raw palette class (`bg-zinc-900`, `text-gray-500`, `text-black`), a hex or `rgb()` value, an inline `style` that sets a colour, and a dark-mode variant that hard-codes a colour instead of using a token that already changes with the theme.
- A visual role that repeats (the same colour or shadow used in three or more places) should become a named token.
- Spacing and sizing use the project's scale. Report arbitrary pixel values where the scale has a step.
- Build from the project's own primitives. Report a hand-built copy of a button, input, dialog or menu that the design system already provides.

## Step 4 — Keyboard and focus

- Every primary workflow (create, save, confirm, cancel, navigate between items) is reachable and operable with the keyboard alone. Report a click-only control: a `div` or `span` with `onClick`, a hover-only action, a custom menu that cannot be opened or traversed with keys.
- Interactive elements are real controls (`button`, `a`, `input`) or carry the right role and key handling. Report an icon-only control without an accessible name.
- Focus is visible. Report styles that remove the focus outline without replacing it.
- Shortcuts, where the app has them, are registered where the app registers them, with a label, and a single-key shortcut does not fire while the user types in an input.
- A dialog or menu that opens moves focus into itself and returns it on close.

## Step 5 — Motion

- Motion never blocks input and respects the user's reduced-motion setting. Report an animation or transition that has no reduced-motion handling, a long animation on a primary action, and input that is disabled while something animates.
- Prefer the project's existing motion tokens or presets over hand-picked durations and easings.

## Step 6 — States and themes

- A component that loads, lists or submits handles the states it can be in: loading, empty, disabled and error. Report a list with no empty state, a form that stays enabled while submitting, and a fetch with no error display.
- The change works in light and dark if the app has both. Report a style that only makes sense in one.
- Internal navigation uses the framework's link component, and actions use the button primitive. Report a plain anchor for an internal route, or a link styled as a button for an action.
- Spacing between siblings uses one mechanism across the app (for example flex or grid `gap`). Report a mix only when the app's convention is one of them.

## Step 7 — Hand off what is not UI review

Name the finding in one line under "Handed off", with no severity and no fix of its own:

- A request to redesign or modernise a page goes to the `draft-ui-redesign` skill.
- Anything outside UI discipline (logic, data, security) goes to the `review-changes` skill, and auth or ownership problems to the `review-auth` skill.

## Step 8 — Report

```text
UI review findings
──────────────────────────────────────────────────
Design system used, per rule: <tokens: documented in path | components: observed in path | motion: defaults (none found)>

1. [high] <title> — `path/to/file:line`
   <what breaks the rule, and the rule it breaks>
   <what a user, or the next theme change, gets wrong because of it>
   <concrete fix>

2. [medium] <title> — `path/to/file:line`
   <issue and fix>

3. [low] <title> — `path/to/file:line`
   <issue and fix>

Handed off
  <one line per finding that belongs to another skill, with the skill name>

Summary
  <overall verdict: consistent with the design system / issues to fix before merging>
```

Severity:

- **High:** a primary workflow with no keyboard path, an icon-only control with no accessible name, removed focus styles, motion that blocks input, a single-key shortcut that fires while the user types in an input.
- **Medium:** a raw colour or a dark-mode variant that hard-codes one, a hand-built copy of an existing primitive, motion with no reduced-motion handling, a missing loading, empty or error state, a form that stays enabled while submitting, a dialog that does not take or return focus, a style that only works in one theme.
- **Low:** an arbitrary spacing value, a repeated style that should be a token, a plain anchor for an internal route.

If a finding depends on a design-system rule you could not confirm, report it as a question and say what you would need to see. Do not report components that follow the system you found, even when you would have designed them differently.
