---
name: laws-of-ux-checklist
description: >
  Quick 12-point UX pre-ship checklist with pass/fail verdict.
  Use when user says "UX checklist", "pre-ship check", "ready to ship?",
  "quick UX check", "laws-of-ux checklist", or "ship check".
---

# Laws of UX — Pre-Ship Checklist

Fast 12-point verification before shipping frontend code. No theory, just pass/fail.

## Process

### Step 1: Read the Component

Read the target file(s). If not specified, check the most recently modified frontend file.

### Step 2: Run the 12-Point Check

For each item, verify by reading the actual code. Mark PASS or FAIL.

```markdown
# Pre-Ship UX Check: [Component Name]

| # | Check | Law | Result | Fix |
|---|-------|-----|--------|-----|
| 1 | **Primary action is the most prominent element** — largest CTA, high contrast, easy to reach | Fitts's, Von Restorff | ✅/❌ | [one-line fix if ❌] |
| 2 | **No more than 7 visible options at once** — nav items, menu choices, filter options | Hick's, Miller's | ✅/❌ | [fix] |
| 3 | **Related elements are visually grouped** — tight spacing within groups, generous between | Proximity, Common Region | ✅/❌ | [fix] |
| 4 | **Feedback within 400ms** — loading states, optimistic updates, skeleton loaders exist | Doherty Threshold | ✅/❌ | [fix] |
| 5 | **Follows platform conventions** — nav placement, form patterns, table behavior match expectations | Jakob's Law | ✅/❌ | [fix] |
| 6 | **Interactive elements have hover/focus states** — transitions on buttons, links, inputs | Aesthetic-Usability, Flow | ✅/❌ | [fix] |
| 7 | **Progress visible for multi-step flows** — stepper, progress bar, "step X of Y" | Goal-Gradient, Zeigarnik | ✅/❌ | [fix] |
| 8 | **Touch targets ≥ 44x44px** — buttons, links, toggles, checkboxes on mobile | Fitts's Law | ✅/❌ | [fix] |
| 9 | **Empty states are handled** — not blank screens, has illustration/message/CTA | Peak-End Rule | ✅/❌ | [fix] |
| 10 | **Information is chunked** — sections have headers, lists are grouped, long forms are divided | Chunking, Cognitive Load | ✅/❌ | [fix] |
| 11 | **Visual hierarchy is clear** — title > subtitle > body > caption, varying sizes and weights | Selective Attention, Prägnanz | ✅/❌ | [fix] |
| 12 | **Complexity is hidden from user** — smart defaults, advanced options tucked away | Tesler's Law, Occam's | ✅/❌ | [fix] |
```

### Step 3: Verdict

```
PASSED: [X]/12 checks
```

| Result | Verdict |
|--------|---------|
| 12/12 | **SHIP IT** — UX is solid |
| 10-11/12 | **SHIP WITH NOTES** — minor issues, can fix post-ship |
| 7-9/12 | **FIX FIRST** — address failures before merging |
| 0-6/12 | **BLOCK** — significant UX issues, needs rework |

### Step 4: Quick Fixes (if any FAIL)

For each failed check, provide a single code block with the minimum change needed:

```markdown
## Fixes

### Check #[N]: [Check name]
```[language]
// [file:line] — add/change this
[code fix]
```
```

## Rules

1. **Read the code** — don't guess, verify each check against actual source
2. **Binary results only** — PASS or FAIL, no "partial" or "maybe"
3. **One-line fixes** — if the fix takes more than 5 lines, reference the full review (`/laws-of-ux review`)
4. **Skip N/A checks** — if it's a static component with no multi-step flow, check #7 is N/A (mark as ✅)
5. **Be fast** — this is a quick check, not a full audit. Under 2 minutes.
