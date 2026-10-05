---
name: vois-patterns
description: Structural decision trees for container types, form states, table layouts, and page-level patterns. Use before vois-tokens. Routes to righter skill for all microcopy (labels, errors, buttons, helpers). Use when building pages, forms, features, workflows.
version: 1.13.1
---

# Vois Patterns Skill

You are building the *structure* of pages and containers for a design system. This skill defines the architectural decisions that come *before* implementation (tokens, components, styling).

**Read this skill first.** After you determine structure here, read `vois-tokens` for implementation details (spacing, typography, components, tokens).

This skill routes to `righter` skill for all microcopy (button labels, error messages, field descriptions, helper text). Don't guess at words—follow the righter skill.

---

## Before You Write Anything

1. **What is the user trying to accomplish?** (Dashboard overview? Edit a record? Confirm an action?)
2. **Pick the container type** from the decision tree below.
3. **Read the matching reference file** for full template rules.
4. **If a `vois_record_pattern_choice` tool is available in your environment**, call it once you have picked a path, before writing any code. If it isn't available, this step is optional telemetry, not a gate — proceed to the next step.

   ```
   Tool: vois_record_pattern_choice
   Arguments:
     skillVersion: <this skill's version, from SKILL.md frontmatter>
     pathId: <one of the path IDs listed in the decision tree below, e.g. "PATH-A" or "PATH-C-MEDIUM">
     userGoal: <plain-English description of the user goal this path addresses>
     thresholdInputs: <key decision inputs used to walk the tree, e.g. { "sectionCount": 3, "reversible": false }>
     microcopyUsed: <optional array of contextKeys for any righter microcopy consulted while applying this pattern>
   ```

   There is no `confidence` argument on the real tool — decide fit using the thresholds in the decision tree itself. If no path fits well and a `vois_report_pattern_gap` tool is available, call it instead of forcing a match:

   ```
   Tool: vois_report_pattern_gap
   Arguments:
     skillVersion: <this skill's version, from SKILL.md frontmatter>
     userGoal: <plain-English description of the goal that didn't fit>
     attemptedFallback: <closest path ID used as a fallback, even though it doesn't fit>
     reasoning: <why the available decision tree didn't fit this goal>
   ```

   If neither tool is available, just proceed with your best-fit path and note the low confidence in your own output.

5. **For every word that appears in UI**, check `righter` skill. See `references/microcopy-routing.md` for the full list of what counts as copy.
6. Then read `vois-tokens` for implementation (tokens, spacing, components).

---

## Decision Tree: What Container Type Should I Build?

```
START: What is the user trying to accomplish?

├─ PATH A: Manage settings or account preferences
│  └─ → read references/settings-pages.md, then references/settings-interactions.md
│     ├─ IF: 2–3 sections only      → [PATH-A-DEPTH-SHALLOW]
│     └─ IF: 4+ sections            → [PATH-A-DEPTH-DEEP]
│
├─ PATH B: View, filter, and act on a list of items
│  └─ → read references/table-list.md, then references/table-interactions.md   [PATH-B]
│
├─ PATH C: Create a new item OR edit an existing item
│  └─ → read references/forms.md, then references/form-field-groups.md
│     ├─ IF: 1–6 fields             → [PATH-C-SIMPLE]
│     ├─ IF: 7–15 fields            → [PATH-C-MEDIUM]
│     └─ IF: 15+ fields / complex   → [PATH-C-COMPLEX]
│
├─ PATH D: Quick input, confirmation, or selection
│  └─ → read references/dialogs-and-action-sheets.md         [PATH-D]
│
├─ PATH E: View details of a single item (read-only or view state)
│  └─ → read references/detail-pages.md                      [PATH-E]
│
├─ PATH F: Show what it costs and help someone choose a plan
│  └─ → read references/pricing-pages.md
│     ├─ IF: flat, one plan                    → [PATH-F-FLAT-1]
│     ├─ IF: seat-based, 1 / 2-3 / 4 plans     → [PATH-F-SEAT-1] / [PATH-F-SEAT-3] / [PATH-F-SEAT-4]
│     ├─ IF: usage-based, 1 plan / tiered / PAYG → [PATH-F-USAGE-1] / [PATH-F-USAGE-TIERED] / [PATH-F-USAGE-PAYG]
│     ├─ IF: seat fee + included usage         → [PATH-F-HYBRID]
│     └─ IF: consumer subscription             → [PATH-F-CONSUMER-WEB] / [PATH-F-CONSUMER-PAYWALL]
│
└─ PATH G: Show what a product or business offers to people not yet using it (landing page, homepage)
   └─ → read references/marketing-pages.md                   [PATH-G]
```

Read the reference file for the path you picked. Paths A and C each have a companion file. Read the companion when the work involves it.

**If the brief doesn't name a container type directly** (it names a
product-specific feature instead — "approval queue," "impersonate a user,"
"bulk edit"), read `references/composition.md` before assuming it needs new
structure. Most of those translate to a direct fit or a combination of two
existing paths.

**Structured lookup:** `data/patterns-rules.json` holds every tagged `[PATH-X]`/`[PATH-X-Y]` node from the tree above as `{ id, condition, outcome, source_file }` (nodes may also carry optional `pattern_name`, `builds_on`, `basis`, `basis_note`, and `evidence`) — useful for a quick condition/outcome check by `pathId` without reading a whole file. It doesn't replace the reference files: worked examples, righter-routing call-outs, and untagged conditional branches (e.g. table-list.md's table-or-list choice) only exist in the `.md` files.

**Source of truth:** `data/patterns-rules.json` is canonical for a path's `condition`/`outcome`. `references/*.md` may restate a path for readability and carries the worked examples JSON doesn't — but if the two ever disagree, the JSON wins. `scripts/check-rule-sync.mjs` (repo root) checks in CI that every `[PATH-*]` tag cited in `references/*.md` resolves to a real entry in `patterns-rules.json` and vice versa.

---

## Reference Files

| File | Covers | Path ID(s) |
|---|---|---|
| `references/settings-pages.md` | Profile, workspace, billing, notifications, members sections; view/edit state | `[PATH-A]` |
| `references/settings-interactions.md` | Save model, notifications, members, integrations, removal, danger zone, email change with one-time code | rules for settings interactions (see `data/patterns-rules.json`) |
| `references/table-list.md` | Table or list, simple vs complex, row open (drawer, full page, dialog), where editing happens, pagination, narrow layout | `[PATH-B]` `[PATH-B-SIMPLE]` `[PATH-B-COMPLEX]` `[PATH-B-ROW-OPEN]` `[PATH-B-EDIT]` `[PATH-B-ROW-ACTIONS]` `[PATH-B-ROW-ACTIONS-REVEAL]` `[PATH-B-NARROW]` |
| `references/table-interactions.md` | Selection and bulk actions, sort, filters, columns, density, saved views, URL state, keyboard, inline edit and save model, loading, empty and error states, partial failures | `PATH-TABLE-*` rules (see `data/patterns-rules.json`) |
| `references/forms.md` | Create/edit forms by complexity tier, validation, save behavior | `[PATH-C]` |
| `references/form-field-groups.md` | Field widths, columns, spacing, name, address, phone, email, one-time code, auto-growing textareas, AI chat input | rules for form field groups (see `data/patterns-rules.json`) |
| `references/dialogs-and-action-sheets.md` | Modal vs action sheet by breakpoint, confirmation/selection dialogs | `[PATH-D]` `[PATH-D-SIZE]` |
| `references/detail-pages.md` | Read-only single-record views | `[PATH-E]` |
| `references/pricing-pages.md` | Pricing pages by billing model (flat, seat, usage, hybrid, consumer) and tier count (1 to 4), calculators, comparison tables, trial timelines | `[PATH-F]` `[PATH-PRICE-U1]` to `[PATH-PRICE-C11]` |
| `references/marketing-pages.md` | Landing pages and homepages: one idea per section, three blocks max, detail behind a link, image tiles, no dividers, one primary button. Taste rules for marketing surfaces only | `[PATH-G]` `[PATH-G-*]` |
| `references/permissions-and-conditional-logic.md` | Hide vs disable by role, parent/child input dependencies, accordions | `[PATH-PERM-*]` `[PATH-COND-*]` (cross-cutting) |
| `references/composition.md` | A brief doesn't name a container type directly, or seems to need more than one at once | `[PATH-COMPOSITION-*]` (cross-cutting) |
| `references/content-density.md` | Deciding how much breathing room a screen should have — admin grid vs. everyday form vs. onboarding/confirmation moment | `[PATH-DENSITY-*]` (cross-cutting) |
| `references/microcopy-routing.md` | Full list of what counts as UI copy and must route to righter | — (cross-cutting) |

---

# Spacing Rules (Quick Reference)

These are implemented via vois-tokens; listed here for context.

- 24px vertical: heading ↔ body text
- 24px horizontal: between two input fields
- 40px vertical: body content ↔ primary action button
- 20px horizontal: between primary/secondary buttons (bottom right anchored)
- Use gap tokens on container div instead of margin-bottom on elements

For exact class/style syntax (Tailwind or StyleX) and token values, see vois-tokens.

---

# Quick Checklist Before Implementation

- [ ] Container type selected (settings / table / form / dialog / detail / pricing) — or, if the brief didn't map directly, checked `references/composition.md` for a fit or combination before designing new structure
- [ ] Content density tier picked deliberately (dense / standard / spacious) — see `references/content-density.md`, not defaulted to whatever the mid-range spacing tokens produce
- [ ] `vois_record_pattern_choice` called with `skillVersion`, `pathId`, `userGoal`, and `thresholdInputs`, if that tool is available
- [ ] Page structure sketched (what sections, what's visible, what's hidden by role)
- [ ] Permissions applied (hide/disable rules — see `references/permissions-and-conditional-logic.md`)
- [ ] All copy routed to righter skill and reviewed
- [ ] Ready to read vois-tokens for tokens, spacing, components
- [ ] Mobile breakpoint behavior defined (action sheets vs dialogs, sidebar vs hamburger, etc.)

---

# Relationship to Other Skills

**This skill ↔ vois-tokens:**

- Read this first (what to build)
- Then read vois-tokens (how to code it correctly)
- vois-tokens handles tokens, spacing, components, animation, accessibility
- This skill handles structural decisions and microcopy routing

**This skill ↔ vois-components:**

- After picking a container type here, read vois-components to select specific components
- vois-components resolves ambiguous pairs — Dialog vs Drawer, Toast vs Banner, Select vs Combobox
- If a `vois_record_component_choice` tool is available, call it after selecting; if not, this step is optional telemetry

**This skill ↔ vois-dataviz:**

- If the screen is a dashboard, an analytics view, or contains charts, KPI tiles, sparklines or maps, decide the page structure here, then read vois-dataviz for what goes inside it
- vois-dataviz picks the chart forms, chart colors, filters and data states; it does not decide the page container

**This skill ↔ conversion-patterns:**

- PATH-F decides layout and structure of a pricing page
- Paywall timing, placement, trial-vs-no-trial, and other test-backed conversion questions route to conversion-patterns

**This skill ↔ righter skill:**

- Every word in UI comes from righter
- This skill tells you which container type
- Righter skill tells you what words go in that container
- Always check righter for: button labels, error messages, field descriptions, status copy, confirmations
