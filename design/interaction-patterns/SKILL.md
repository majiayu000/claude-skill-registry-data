---
name: interaction-patterns
description: Use when deciding how users interact with UI elements — expand vs navigate, modal vs bottom sheet, swipe gestures, tap targets, optimistic UI, loading patterns, or undo for destructive actions. Use before features get built so every screen inherits the same rules.
---

# Interaction Patterns

## Overview

Define the canonical interaction for every UI primitive *before* features get built. Output is `.forge/interaction-patterns.md` — the decision tree for each interaction (expand vs navigate, modal vs bottom sheet, optimistic vs pessimistic UI, undo vs confirm), the tap-target minimums, the keyboard and scroll behavior, and the documented anti-patterns. Paired with `design-system` (which defines the look) and `accessibility` (which defines the floor).

## When to Use

- A new product or major feature is being designed and no interaction conventions exist
- Mobile and desktop are drifting (centered modals on mobile, no swipe affordances)
- Destructive actions have inconsistent UX (some have confirm, some have undo, some have neither)
- A new component category is being introduced (e.g., first time adding command palette, drawer, popover)
- Loading states are inconsistent (skeletons on one page, spinners on another)

## When NOT to Use

- A single interaction tweak inside one screen — that's `incremental-implementation`
- Backend-only services
- Accessibility-specific decisions (those go in `accessibility`)

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "Desktop patterns work on mobile" | Centered dialogs on mobile are unreachable with one thumb. Modal trap UX on a touchscreen is hostile. |
| "Users will figure it out" | If it needs figuring out, it's broken. Every interaction that needs explanation costs a support ticket. |
| "We don't need loading states for fast operations" | Fast on your dev machine is slow on a train in rural India. The user can't see your machine. |
| "Undo is too complex" | Undo is cheaper than a confirmation dialog and faster than user anxiety. The only complex undo is the one nobody designed for. |
| "Swipe is obvious from native apps" | Swipe with no visual affordance is a hidden feature. Discoverability requires a hint. |
| "Optimistic UI is risky" | The risk is *rollback messaging*, not optimism. Pessimistic UI is a 300ms spinner every interaction. |

## Red Flags

- A centered dialog on mobile (should be a bottom sheet or full-screen)
- Tap targets smaller than 44pt on touch
- An async action with no loading state (the button "completes" but nothing visibly changed)
- A destructive action (delete, archive, send) with neither undo nor confirmation
- A swipe gesture with no visual affordance hinting it's swipeable
- A horizontal scroll container with no scroll indicator or fade edge
- A modal stacked on top of another modal
- A list item that's both tappable and has tappable children with no clear hierarchy

## Core Process

### Step 1: Inventory the interaction primitives in the product

List every distinct interaction shape: expand vs navigate, modal, bottom sheet, drawer, popover, toast, command palette, swipe action, long-press, drag-to-reorder, pull-to-refresh, infinite scroll, paginated load, optimistic update, undo, confirm dialog, inline edit, keyboard shortcut.

### Step 2: Assign one canonical pattern per category

Examples (project decides the actual values):

- **Modal vs bottom sheet:** desktop = centered modal. Mobile = bottom sheet, always. No exceptions.
- **Expand vs navigate:** 1-3 fields of detail → expand inline. More than that → navigate to a detail view.
- **Confirm vs undo for destructive:** reversible within 30s → optimistic + undo toast. Irreversible (account delete, payment send) → confirm dialog with typed confirmation for the highest-stakes ones.
- **Loading:** content-shaped wait (lists, cards) → skeleton. Action-shaped wait (button click) → spinner-in-button + disabled state. Page-shaped wait → skeleton page, never a centered spinner.
- **Optimistic UI:** allowed when the failure mode is rollback-friendly (revert + toast). Forbidden for payments, identity, security.

### Step 3: Tap target + touch rules

- Minimum 44pt tap target on touch devices (Apple HIG / Material baseline).
- Hit areas can exceed visual size — a 24pt icon can have a 44pt invisible padding.
- No two tap targets within 8pt of each other.
- Hover-only interactions are forbidden — every hover must have a touch-equivalent (tap, long-press, or explicit action).

### Step 4: Keyboard + scroll behavior

- `Esc` closes any modal, drawer, popover, command palette.
- `Tab` order is visual order; never tab-trap inside disabled regions.
- Focus returns to the trigger when a modal closes.
- Scroll restoration on back-navigation — the user returns to where they were.
- Horizontal scroll has a visual affordance (fade edge, indicator dots, or "next" button).

### Step 5: Decision tree, in `.forge/interaction-patterns.md`

For every interaction the product uses, write the decision logic that engineers can apply without asking design. Format: "When X, do Y, because Z."

Example excerpts:
- "When showing a confirmation on mobile, do bottom sheet. Because: thumb-reachable, native-feeling, no accidental dismissal."
- "When a list item has 5+ fields of detail, do navigate. Because: expand obscures siblings, navigate gives breathing room and a back button."
- "When the action is reversible within 30 seconds, do optimistic + undo toast. Because: confirm dialog interrupts; undo respects momentum."

### Step 6: Document the anti-patterns

In the same file, the list of things that look reasonable but are wrong: modal on top of modal, spinner inside button without disabling, swipe without affordance, hover-only interactions, irreversible action behind a single click.

## Verification

- [ ] `.forge/interaction-patterns.md` written
- [ ] Every modal on mobile is a bottom sheet (or has an ADR explaining why)
- [ ] Every destructive action has either undo (reversible) or confirm (irreversible) — never neither
- [ ] No tap target smaller than 44pt (verified via Storybook accessibility addon or manual audit)
- [ ] Every list-with-detail has an "expand vs navigate" decision logged
- [ ] Every async action has a loading state appropriate to its shape (skeleton, spinner-in-button, or page skeleton)
- [ ] `Esc` closes every overlay
- [ ] Focus returns to the trigger when an overlay closes
- [ ] No hover-only interaction in the codebase (grep `:hover` for forbidden patterns)
- [ ] Horizontal scroll containers all have a visual affordance
