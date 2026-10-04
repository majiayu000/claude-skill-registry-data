---
name: interaction-feedback
description: This skill should be used when the user wants clear visual feedback for async actions and state changes — triggers like "add loading and error states", "show a success message", "add a toast/notification", "inline form validation", "optimistic UI", "empty state for this list", "this button gives no feedback", or "add a skeleton loader". It implements loading/empty/error/success states, toasts, micro-interactions, and their accessibility announcements, adapted to the detected stack.
version: 0.1.0
---

# Interaction feedback

Tell users what happened. Every view that depends on data or an async action must communicate its state — loading, empty, error, success — and confirm the result of every interaction. Never leave a dead state where the UI silently does nothing.

## When to use

Use this skill for requests such as:

- "Add loading and error states" / "add a skeleton loader" / "add a spinner"
- "Show a success message" / "add a toast / notification"
- "Inline form validation" / "show validation errors"
- "Optimistic UI" / "update immediately and roll back on failure"
- "Empty state for this list"
- "This button gives no feedback when clicked"

## The core model: handle every state

Any component backed by data or an async action must explicitly handle four states, plus partial/optimistic transitions:

1. **Empty** — no data yet (first run, cleared filters, new account).
2. **Loading** — request in flight.
3. **Error** — the request or action failed.
4. **Success / ideal** — data is present, action confirmed.

Treat "no design for this state" as a bug. A blank screen during loading, a list that shows nothing with no explanation, or a button that does nothing on click are all dead states.

## Patterns

1. **Loading**
   - **Skeletons** for content whose layout is known (cards, tables, profiles) — they preserve layout and reduce perceived wait.
   - **Spinners** for short, indeterminate waits where layout is unknown.
   - **Inline button-busy** (disabled + `aria-busy` + label like "Saving…") for in-place actions; keep the button's size stable to avoid layout shift.
   - **Delay spinners ~200–300ms** so fast responses don't flash a spinner. Reserve space so content doesn't jump when it arrives.

2. **Success**
   - Prefer **in-context confirmation** (the row updates, a checkmark appears, the field shows saved) over a detached message.
   - Use a **toast** for transient, low-importance confirmations ("Copied", "Saved").
   - Keep it brief and don't block the next action.

3. **Error**
   - Place errors **near the cause** (inline at the field/section), not only in a global banner.
   - Make them **actionable and recoverable**: say what went wrong and offer a next step (Retry, Edit, Contact support). Never a dead-end.
   - Preserve the user's input on failure.

4. **Empty**
   - Explain the **value** of the area and offer a **primary action** ("No projects yet — create your first project"). Don't just print "No data".
   - Distinguish first-use empty from filtered/cleared empty (offer "Clear filters").

5. **Optimistic UI**
   - Update the UI **immediately** on the user's action, then reconcile with the server.
   - On failure, **roll back** to the prior state and show a clear, recoverable message ("Couldn't save — changes reverted. Retry?").
   - Use only where the action is very likely to succeed and rollback is cheap and clear.

6. **Toasts / status messages**
   - Announce via `aria-live`: **polite** for routine status, **assertive** / `role="alert"` for errors and urgent messages.
   - Auto-dismiss neutral toasts (~4–6s); **don't auto-dismiss errors** the user must read or act on.
   - Never put a **critical or only** action inside a toast — toasts disappear and aren't reliably reachable by keyboard/screen-reader users.

7. **Micro-interactions**
   - Provide `:hover`, `:active`, and `:focus-visible` feedback on interactive elements.
   - Tie transitions/animation to **motion tokens** (duration, easing).
   - **Always gate non-essential motion** behind `@media (prefers-reduced-motion: reduce)` — disable or reduce animation, never make it required to understand state.

## Accessibility of feedback

- **Announce changes** screen readers can't otherwise perceive: wrap status text in `role="status"` / `aria-live="polite"`, and errors in `role="alert"` / `aria-live="assertive"`. Live regions must exist in the DOM **before** their content updates.
- **Move focus on error** to the first invalid field (or an error summary linking to fields) on submit, so keyboard users land at the problem.
- **Don't rely on color alone** — pair red/green with an icon and text.
- **Disabled vs busy**: use `aria-busy="true"` for in-progress controls rather than fully removing them from the tab order; use `disabled` only when the control genuinely cannot be used.
- Mark invalid fields with `aria-invalid="true"` and associate the message via `aria-describedby`.

## Adapt to the stack

Read `../ux-foundations/references/stack-detection.md` and run that procedure before writing code; report the detected `framework`, `styling`, and `language` in one line. With no project, fall back to the framework-agnostic pattern in `examples/toast-aria-live.html`.

**Reuse what exists.** Before adding dependencies, check for existing toast/notification libraries (e.g. `react-hot-toast`, `sonner`, `vue-toastification`, `svelte-french-toast`), form/validation libraries (`react-hook-form`, `zod`, `vee-validate`, `formik`), and state/data libraries (`@tanstack/react-query`, `swr`, `redux-toolkit`, Pinia) — they often already model loading/error/success states. Wire feedback into those rather than introducing parallel systems. Style via design tokens, not hardcoded values.

## References and examples

- `references/states-and-feedback.md` — decision table (situation → pattern → a11y mechanism → timing), the four states in depth, toast accessibility, validation timing, skeleton vs spinner, optimistic rollback UX, reduced-motion, and an anti-patterns list.
- `examples/toast-aria-live.html` — working framework-agnostic accessible toast system (polite status region + assertive alert region, pause-on-hover, reduced-motion aware).
