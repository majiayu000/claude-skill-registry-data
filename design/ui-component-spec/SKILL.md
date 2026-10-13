---
name: ui-component-spec
description: Specify a single interactive UI component (button, input, datepicker, dropdown, modal, table, form, card, etc.) in exhaustive detail — anatomy, props, content slots, every state, every behavior, validation rules, and accessibility requirements — so it can be implemented without the model inventing edge cases. Use this skill whenever the user asks to "design", "build", "spec", or "make" a specific interactive component, or when a screen blueprint is approved and individual components need to be nailed down before code. Always use it before ui-generate-code for any non-trivial interactive widget, because component code generated without an explicit state matrix is the single most common source of edge-case bugs.
status: stable
---

# UI Component Spec

Specifies a single interactive component in enough detail that code generation cannot drift. Output is a structured spec that exhaustively maps anatomy, every visual state, every behavior, validation, and accessibility — the things the model otherwise silently invents.

## When to use this skill

Use this skill when:
- A blueprint is approved and the user wants to nail down a specific component (e.g. "now spec the date range picker").
- The user asks to "design", "build", or "make" a specific interactive widget.
- A previously generated component has missed an edge case (loading state, empty state, error state) — re-spec the component before fixing.

Do **not** use this skill when:
- The user wants the whole screen specced. Use `ui-blueprint` first.
- The component is a static, non-interactive piece of layout (e.g. a footer, a logo block). Those don't need a state matrix.

## Core principle

**The state matrix is the artifact.** Most UI bugs are missed states, not missed visuals. A component spec without an exhaustive state matrix is just a sketch. Force every state to be either specified or explicitly marked "not applicable" — never silently omitted.

## Pre-flight check

Before drafting, confirm:

1. **A blueprint or brief exists** that places this component in context. If neither exists, ask: "On what screen does this component live, and what is the primary user action it serves?" Document the answer at the top of the spec.
2. **The component's role is clear.** Is it the primary action element, a secondary control, a navigation element, a data display? This affects how prominently states should be expressed (e.g. a primary CTA needs richer hover/focus feedback than a tertiary link).
3. **Data shape is known.** If the component displays or consumes data (e.g. a list, a table, a select), what does that data look like? Empty (0 items)? Sparse (1–3)? Full (N items)? Loading? Errored? Without this, the empty/loading/error states will be invented.

If any of the three is missing, ask. Do not guess.

## The mandatory state matrix

Every interactive component must address every state in this matrix. If a state does not apply, write "N/A — <reason>". Do not silently omit.

| State | Visual change | Behavior | Triggered by |
|---|---|---|---|
| **Default** | resting appearance | none | initial render |
| **Hover** | visual feedback | none (cursor change) | mouse over (desktop only) |
| **Focus** | visible focus ring | keyboard input becomes possible | tab key, programmatic focus |
| **Focus-visible** | focus ring shown | same as focus | keyboard navigation only (not mouse click) |
| **Active / pressed** | depressed appearance | action triggers on release | mousedown / touchstart / Enter / Space |
| **Disabled** | muted, low-contrast | non-interactive, no events fire | `disabled` prop or condition |
| **Loading / busy** | spinner or skeleton | non-interactive while loading | async action in flight |
| **Error** | error styling, error message | as defined | validation failure or async error |
| **Success** | success styling | as defined | validation pass or async success |
| **Empty** | empty state UI | as defined | data array length === 0 |
| **Read-only** | non-editable but visible | input blocked, content shown | `readonly` prop |
| **Selected / active-state** | indicates selection | as defined | user selection (for togglable components) |

For some components, additional states apply: `expanded` / `collapsed` for accordions, `open` / `closed` for modals and dropdowns, `pinned` / `sticky` for headers, `dragging` for sortable items, `editing` / `viewing` for inline-editable fields.

## Workflow

### Step 1 — Identify the component and its role

Name it precisely. "Button" is too vague — is it a primary CTA, a destructive action, a icon-only utility button, a toggle? Pick a precise name.

### Step 2 — Map the anatomy

Break the component into its atomic parts. Each part is a slot — something that may be filled, styled, or extended. Use the convention: `Container > Slot > Atom`.

For a password input, anatomy looks like:
```
PasswordInput
├── Label
├── InputContainer
│   ├── InputField
│   ├── VisibilityToggle (button with icon)
│   └── ValidationIcon (success or error)
├── HelperText (optional, default state)
└── ErrorText (replaces HelperText on error)
```

### Step 3 — Define props / content slots

What can be passed in? Required vs. optional. Default values. Type/shape. Use a table — see template.

### Step 4 — Fill in the state matrix

Address every row in the mandatory matrix above. For each state, describe both the visual change and the behavior change. If a state is N/A, say why.

### Step 5 — Specify behavior beyond states

What happens when the user interacts? Click, double-click, long-press, drag, keyboard shortcut. Any side effects (focus moves elsewhere, scroll happens, modal closes)? Any animations / transitions (and timing)?

### Step 6 — Validation rules (if applicable)

For inputs and form components: when does validation fire (on blur, on submit, on change)? What's the rule? What's the error message? Does the error block submission?

### Step 7 — Accessibility requirements

Every interactive component must have:
- Correct semantic HTML element OR appropriate ARIA role.
- Keyboard operability (and explicit keyboard shortcuts table).
- Focus management on appearance/dismissal (especially for modals, popovers).
- Screen reader announcements for state changes.
- Color contrast meeting WCAG AA at minimum (specify which tokens are used so this is checkable later).

### Step 8 — Confirm with the user

End with a list of decisions and assumptions. Ask for sign-off before moving to `ui-generate-code` or `ui-acceptance`.

## Output template

Always produce output in this exact structure.

```markdown
---
spec_type: component
spec_id: <slug, e.g. "password-input">
based_on: blueprint-<slug>  # or brief-<slug> if no blueprint
created: <YYYY-MM-DD>
status: draft
---

# Component spec: <precise component name>

## 1. Context
- **Lives on screen(s):** <screen name(s) from blueprint>
- **Role on those screens:** <primary action | secondary action | navigation | data display | input | feedback>
- **Data it consumes:** <type / shape / null cases — or "none, this is a presentational component">

## 2. Anatomy

```
ComponentName
├── Part1
├── Part2
│   ├── Subpart
│   └── Subpart
└── Part3 (optional)
```

For each part, one line on what it is and whether it's required or optional.

## 3. Props / content slots

| Prop / slot | Type | Required | Default | Notes |
|---|---|---|---|---|
| `id` | string | yes | — | for label association |
| `value` | string | yes | — | controlled value |
| `onChange` | function | yes | — | called on every change |
| `disabled` | boolean | no | false | |
| `error` | string \| null | no | null | when present, switches to error state |
| ... | ... | ... | ... | ... |

## 4. State matrix

| State | Visual | Behavior | Trigger |
|---|---|---|---|
| Default | <describe visually using token references where possible — e.g. "1px border in `border-default`, background `surface-1`"> | accepts focus and input | initial |
| Hover | <e.g. "border becomes `border-strong`, cursor `text`"> | none | mouse enter |
| Focus / Focus-visible | <e.g. "2px focus ring in `focus-ring-color`, offset 2px"> | input is active | tab or click |
| Active / pressed | N/A — inputs do not have a pressed state | — | — |
| Disabled | <e.g. "border `border-muted`, background `surface-disabled`, text `text-muted`, cursor `not-allowed`"> | no events fire, no focusable | `disabled` prop |
| Loading | <e.g. "right-aligned spinner replaces visibility toggle"> | input blocked while loading | `loading` prop |
| Error | <e.g. "border `border-error`, error icon visible, ErrorText visible"> | invalid value submitted to onChange but flagged | `error` prop is non-null |
| Success | <e.g. "checkmark icon visible, no border change"> | none | optional `success` prop |
| Empty | N/A — single-value input | — | — |
| Read-only | <e.g. "no border, background `surface-1`, cursor `default`"> | input blocked but value visible | `readonly` prop |

## 5. Behavior

- **On click in input area:** focus moves to input; cursor placed at clicked position.
- **On blur:** validation fires (see Validation Rules).
- **On Enter:** triggers `onSubmit` if inside a form; otherwise no-op.
- **On Escape:** clears the field if not empty (optional — confirm with user).
- **Animations / transitions:** <list each, with duration. e.g. "Border color transitions 150ms ease on hover/focus.">

## 6. Validation rules (if applicable)

| Rule | When fires | Message | Blocks submit |
|---|---|---|---|
| Required | on blur and on submit | "This field is required." | yes |
| Min length 8 | on blur | "Must be at least 8 characters." | yes |
| ... | ... | ... | ... |

**Validation timing rule:** specify when first validation appears (typically on blur, not on every keystroke — but confirm).

## 7. Accessibility

| Requirement | How met |
|---|---|
| Semantic element | `<input type="password">` |
| Label association | `<label htmlFor>` linked to input `id` |
| Error association | `aria-describedby` points to error text id |
| Required indicator | `aria-required="true"` and visible asterisk in label |
| Visibility toggle | `<button>` with `aria-label="Show password"` / `"Hide password"` based on state, `aria-pressed` reflects state |
| Focus ring | visible at WCAG AA contrast against adjacent surface |
| Color contrast | text and border use tokens that meet AA |

### Keyboard map
| Key | Action |
|---|---|
| Tab | move focus to next focusable |
| Shift+Tab | move focus to previous focusable |
| Enter | submit (if in form) |
| Escape | (optional) clear |

### Screen reader announcements
- On focus: "<label>, password input, required" (if required).
- On error: error message announced via `aria-live="polite"` region or via `aria-describedby` linkage.

## 8. Open questions
- <Numbered, specific.>

## 9. Assumptions made
- ⚠️ <Each flagged.>
```

## Concrete example — a "danger button" spec

```markdown
# Component spec: Danger button (destructive action)

## 1. Context
- Lives on screen(s): User profile, Team settings, Project settings
- Role: secondary destructive action (e.g. "Delete account", "Remove member")
- Data consumed: none

## 2. Anatomy

```
DangerButton
├── IconSlot (optional, leading)
├── Label (required)
└── LoadingSpinner (visible during loading state, replaces icon)
```

## 3. State matrix (excerpt)

| State | Visual | Behavior |
|---|---|---|
| Default | red text, transparent background, 1px red border | clickable |
| Hover | red background, white text | clickable, cursor pointer |
| Focus-visible | red focus ring offset 2px | clickable, keyboard-actionable |
| Active | darker red background, slight depress | onClick fires on release |
| Disabled | muted red text, muted border, no background | not clickable |
| Loading | spinner replaces icon, label dims | onClick blocked |

## 5. Behavior
- On first click: opens confirmation dialog (does NOT immediately destroy).
- On confirm: enters loading state, fires `onConfirm` async.
- Animation: hover transitions background 100ms; click transitions 50ms.
```

## Rules that prevent hallucinated decisions

1. **Never silently omit a state.** Every row of the state matrix must be addressed — even if the answer is "N/A — <reason>".
2. **Never invent a token value.** If the spec says "border `border-default`", that token must exist in the design system. If `ui-system` hasn't run, refer to tokens by name and flag them as undefined.
3. **Never invent behavior the user didn't specify.** "Should pressing Escape clear the field?" is an open question, not a default. Ask.
4. **Never invent validation rules.** Rules come from the user or from the brief. If neither says, ask.
5. **Never specify timing values (animation durations) without a basis.** Either reference a system token (e.g. `motion.fast = 150ms`) or ask the user.
6. **Never write "etc." or "and similar".** Every state, every prop, every behavior is enumerated explicitly. If you find yourself wanting to write "etc.", you have not finished thinking.

## Acceptance criteria for this skill's output

A component spec produced by this skill is acceptable only if every one of these is true:

- [ ] Frontmatter links to a blueprint or brief.
- [ ] Component name is precise (not "Button" but e.g. "Primary CTA button" or "Danger button").
- [ ] Anatomy tree includes every visible part, marked required or optional.
- [ ] Props table has at least one row per prop, with type / required / default / notes columns filled.
- [ ] State matrix addresses every row of the mandatory matrix (default, hover, focus, focus-visible, active, disabled, loading, error, success, empty, read-only, plus any component-specific states).
- [ ] No state is silently omitted — N/A entries have a reason.
- [ ] Validation section is present for any input component, or marked N/A with reason.
- [ ] Accessibility section includes: semantic element, label/error associations, keyboard map, screen reader announcements.
- [ ] Keyboard map enumerates every relevant key, not just "supports keyboard navigation".
- [ ] No invented timing, color, or token values — every value is either from the system or flagged as a question.
- [ ] No "etc." or "and similar" appears in the spec.

If any check fails, revise before delivering.
