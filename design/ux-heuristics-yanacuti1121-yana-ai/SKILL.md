---
name: ux-heuristics
description: >
  Evaluate a UI against Nielsen's 10 Usability Heuristics — score each heuristic,
  flag violations with severity ratings, and produce a prioritized fix list.
  Use when the user asks for a "UX review", "usability audit", "heuristic evaluation",
  or "why is this UI confusing to users".
  Do NOT use for code quality or accessibility — use output-enforcement or
  accessibility-audit for those.
origin: yamtam
version: 1.0.0
compatibility: "Any UI — web, mobile, desktop. Works from code, screenshot, or description."
---

<!-- Heuristics based on Nielsen's 10 Usability Heuristics (public domain, Jakob Nielsen 1994/2020).
     YAMTAM skill structure, severity scoring, and Anti-Fake-Pass section are original. -->

## When to Use

- Use when: user says "why is this confusing", "users keep making mistakes", "UX review"
- Use when: reviewing a design before user testing
- Use when: diagnosing a specific UX complaint ("users can't find X")
- Do NOT use for visual aesthetics — use `ui-redesign` or `design-taste-frontend`
- Do NOT use for accessibility compliance — use `accessibility-audit`

## The 10 Heuristics

### H1 — Visibility of System Status
*The system always keeps users informed about what is going on.*

Check for:
- Loading states present on async operations
- Progress indicators for multi-step processes
- Clear feedback after actions (success/error messages)
- Active states on navigation items

### H2 — Match Between System and Real World
*The system speaks the users' language.*

Check for:
- Technical jargon used where plain language would work
- Icons whose meaning is not universally understood (no tooltips)
- Dates, numbers, currencies in non-user locale format
- Metaphors that don't match user mental models

### H3 — User Control and Freedom
*Users can undo mistakes and exit unwanted states.*

Check for:
- No undo/cancel on destructive actions
- No way to exit a flow mid-way
- Modals/dialogs with no close option
- Back button behavior inconsistent with user expectation

### H4 — Consistency and Standards
*Users should not have to wonder whether different words, situations, or actions mean the same thing.*

Check for:
- Same action labeled differently in different places
- Similar UI elements that behave differently
- Platform conventions broken (right-click, swipe, keyboard shortcuts)
- Inconsistent button placement across screens

### H5 — Error Prevention
*Design carefully to prevent problems from occurring.*

Check for:
- Forms allow invalid input with no real-time validation
- Destructive actions with no confirmation step
- Ambiguous options that users might misclick
- No constraints on inputs that have known valid ranges

### H6 — Recognition Rather than Recall
*Minimize the user's memory load.*

Check for:
- Actions or options only available from memory (no visible affordances)
- Form fields don't show what format is expected
- No breadcrumbs or context indicators in complex flows
- Commands that must be remembered rather than recognized

### H7 — Flexibility and Efficiency of Use
*Accelerators for expert users, not at the expense of novices.*

Check for:
- No keyboard shortcuts for power users
- Repetitive tasks with no shortcut or bulk action
- Advanced options completely hidden from everyone (not just collapsed)
- No way to customize frequent workflows

### H8 — Aesthetic and Minimalist Design
*Dialogues should not contain irrelevant or rarely needed information.*

Check for:
- Every visible element serves a purpose or an action
- Information hierarchy unclear — secondary info competes with primary
- Marketing copy in UI flow (task completion ≠ marketing moment)
- Visual noise that dilutes important content

### H9 — Help Users Recognize, Diagnose, and Recover from Errors
*Error messages should be expressed in plain language, precisely indicate the problem, and constructively suggest a solution.*

Check for:
- Error messages that say what went wrong but not how to fix it
- Error codes shown without human explanation
- Errors that disappear before the user can read them
- Form errors not linked to the specific field that caused them

### H10 — Help and Documentation
*Even though it is better if the system can be used without documentation, it may be necessary.*

Check for:
- Complex features with no help text or tooltip
- Empty states with no guidance on what to do
- Onboarding that assumes prior knowledge
- Help content that requires leaving the current task

---

## Severity Scale

Score each violation 0–4:

| Score | Label | Meaning |
|-------|-------|---------|
| 0 | Not a problem | Can be ignored |
| 1 | Cosmetic | Fix only if time permits |
| 2 | Minor | Low priority |
| 3 | Major | High priority — fix before ship |
| 4 | Catastrophic | Must fix — blocks usability |

## How It Works

1. **Read or view the UI** — code, screenshot, or description
2. **Evaluate each of the 10 heuristics** — one by one, no skipping
3. **Record violations** with severity 1–4 (severity 0 = skip)
4. **Sort by severity** — 4 first, then 3, then 2, then 1
5. **Produce fix list** — specific, actionable, one fix per violation

## Output Format

```
## UX Heuristics Evaluation

H1 — Visibility of System Status        PASS
H2 — Match Between System and World     VIOLATION (severity 2)
  Issue: "Submit" button on invoice form — users unfamiliar with accounting
         don't know if this sends or just saves.
  Fix: Rename to "Send Invoice" — makes action explicit.
H3 — User Control and Freedom           VIOLATION (severity 4)
  Issue: No way to cancel a payment once "Confirm" is clicked.
  Fix: Add 30-second undo window with toast notification.
...

## Summary
Violations: 6  (1× severity-4, 2× severity-3, 2× severity-2, 1× severity-1)
Must fix before ship: H3 (catastrophic), H9 (major), H1 (major)
```

## Gotchas

- H8 (minimalist design) is about information density, not visual aesthetics — a visually busy UI can pass H8 if every element serves a purpose
- Evaluate from the user's perspective, not the developer's — "it's obvious" is not evidence
- A single screen may have violations of multiple heuristics simultaneously
- Severity 4 must block delivery — do not report it and move on

## Anti-Fake-Pass Rules

Before claiming the evaluation is done, you MUST show:
- [ ] All 10 heuristics evaluated — none skipped without explicit N/A reason
- [ ] Each violation has: heuristic number, severity score, specific UI element, concrete fix
- [ ] Summary: total violations by severity level
- [ ] Must-fix list identified (severity 3–4)

Reference: `gates/anti-fake-pass-gate.md`
