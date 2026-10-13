---
name: ui-acceptance
description: Convert an approved UI spec (brief, blueprint, component spec, or any combination) into a testable implementation checklist — concrete, machine-checkable-where-possible criteria for layout, responsiveness, every state, accessibility, visual polish, and microcopy. Use this skill whenever the user has approved a spec and is about to start building, or has just finished building and wants to verify the result. Always use it before shipping any UI feature, because without explicit acceptance criteria the only judge of "done" is vibes — and vibes drift between sessions.
status: stable
---

# UI Acceptance

Converts an approved spec into a checklist that says "the implementation is done if and only if every one of these is true." This is the contract that closes the loop between spec and implementation. It is the document `ui-redline` checks against, and the document a user runs through manually before saying "ship it".

## When to use this skill

Use this skill when:
- A spec (brief + blueprint + component specs, or any subset) has been approved and the user is ready to build or has just built.
- The user says "what should I check before shipping" or "how do I know if this is done".
- A previous build was declared "done" but later turned out to be broken — re-run acceptance to find what wasn't checked.

Do **not** use this skill when:
- No spec exists. The output would be free-floating quality criteria not anchored to anything. Run `ui-brief` and `ui-blueprint` first.
- The user only wants high-level QA. This skill produces detailed line-item checklists — overkill for a quick sanity check.

## Core principle

**Every criterion must be testable.** "The form is accessible" is not a criterion — it is a vibe. "Every input has a programmatically associated `<label>`" is a criterion — you can check it with a script or a 30-second manual pass. Replace every vague criterion with one that has a clear pass/fail.

## Pre-flight check

Before drafting, confirm:

1. **At least one upstream spec exists.** Brief, blueprint, component spec, or system. Without one, there is nothing to derive criteria from.
2. **Scope of acceptance.** Is this for a single component, a single screen, a feature, or a whole product? The scope determines how many sections the checklist needs.
3. **Build context.** Has the implementation already happened (acceptance = QA pass), or is this pre-build (acceptance = guidance for the implementer)? Affects tone of the criteria — pre-build: imperatives; post-build: questions.

If any is missing, ask. Do not produce a checklist for an unknown spec.

## Workflow

### Step 1 — Walk the spec(s) and extract every claim

For each section of the upstream spec, find every concrete claim and convert it into a testable criterion. Use these mapping rules:

| Spec source | Becomes acceptance criterion |
|---|---|
| Brief — primary action | "Primary action is reachable in ≤ 2 taps/clicks from initial render." |
| Brief — success criterion | Restated as a measurable post-build check. |
| Blueprint — hierarchy ranking | "Element ranked 1 is the largest visual element on the screen and is the first focusable on tab." |
| Blueprint — wireframe layout | "Layout matches the wireframe at the primary breakpoint (visual diff acceptable within 5%)." |
| Blueprint — responsive behavior | One criterion per breakpoint, each describing the agreed reflow. |
| Component spec — every state | One criterion per state ("Hover state shows X", "Focus-visible state shows ring of width Y"). |
| Component spec — keyboard map | One criterion per key ("Pressing Escape closes the dialog and returns focus to the trigger."). |
| Component spec — validation rules | One criterion per rule, including timing and message. |
| System spec — tokens used | "All colors, spacings, and font sizes resolve to tokens defined in the system spec — no inline literals." |

### Step 2 — Group criteria into the standard sections

The standard sections are: Layout, Responsive, States, Behavior, Accessibility, Visual polish, Microcopy, Performance (optional). Place every criterion in exactly one section.

### Step 3 — Mark each criterion machine-checkable or manual

Some criteria can be checked with a script or a linter (e.g. "every `<input>` has an associated label" — checkable with a DOM query). Others require human eyes (e.g. "the empty state message is friendly and on-brand").

Do not use generic `[A]`.
Use explicit automation labels:
- `[A:playwright]` for browser interaction and runtime DOM checks
- `[A:axe]` for axe accessibility automation
- `[A:lint]` for static lint or code scanning checks
- `[A:unit]` for unit or integration test assertions
- `[M]` for manual verification

### Step 4 — Add severity

Each criterion has a severity: **blocker**, **major**, **minor**, **polish**. Blockers prevent shipping. Polish issues are nice-to-haves. This lets the user prioritize fixes during `ui-redline`.

### Step 5 — Confirm with the user

Show the checklist. Ask: "Is anything missing? Is any severity wrong?" Iterate.

## Output template

```markdown
---
spec_type: acceptance
spec_id: <slug, ideally matching the brief slug>
based_on:
  - brief-<slug>
  - blueprint-<slug>
  - component-<slug-1>
  - component-<slug-2>
  - system-<slug>
created: <YYYY-MM-DD>
status: draft
---

# Acceptance checklist: <descriptive title>

## How to use this checklist
- Each item has a severity: **blocker** (must fix before ship), **major** (should fix before ship), **minor** (fix before next milestone), **polish** (fix when time permits).
- Each item is marked with an explicit automation source: **[A:playwright]**, **[A:axe]**, **[A:lint]**, **[A:unit]**, or **[M]**.
- Where a criterion traces back to a specific spec section, the source is noted in `[source]`.

## 1. Layout

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] Visual layout matches the wireframe at the primary breakpoint (allow ≤5% visual diff). | blueprint §4 |
| ☐ | blocker | [M] Element ranked 1 in the hierarchy is the most visually prominent on the screen. | blueprint §3 |
| ☐ | blocker | [A:playwright] Element ranked 1 is the first focusable element when tabbing through. | blueprint §3 |
| ☐ | major | [M] Whitespace decisions from blueprint are honored (generous whitespace where specified, tight grouping where specified). | blueprint §4 |
| ☐ | major | [A:lint] All spacing values resolve to tokens defined in `space.*`. No inline padding/margin literals. | system §2 |

## 2. Responsive

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] At <descriptions of each non-primary breakpoint>, the layout reflows as specified using the verbs `<stack/collapse/hide/move/resize/swap>`. | blueprint §5 |
| ☐ | blocker | [M] Primary action stays in the top half of the viewport at every breakpoint. | blueprint §5 |
| ☐ | major | [A:playwright] No horizontal scroll appears at the smallest specified breakpoint. | blueprint §5 |
| ☐ | major | [M] Touch targets are at least 44×44px on mobile breakpoints. | accessibility default |

## 3. States (per component)

For each component spec, expand into a sub-table. Example for a primary CTA button:

### 3.1 Primary CTA button

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] Default state matches the spec's default visual. | component §4 |
| ☐ | blocker | [M] Hover state shows specified color change with `motion.fast` transition. | component §4 |
| ☐ | blocker | [A:playwright] Focus-visible state shows a focus ring at WCAG AA contrast against adjacent surface. | component §7 |
| ☐ | blocker | [M] Active/pressed state shows specified color change. | component §4 |
| ☐ | blocker | [A:unit] Disabled state has `aria-disabled="true"` (or native `disabled`) and prevents click. | component §4, §7 |
| ☐ | blocker | [M] Loading state replaces label with spinner and prevents repeat clicks. | component §4 |
| ☐ | major | [M] Error state renders only when error prop is non-null. | component §4 |
| ☐ | minor | [M] Success state visible only when success prop is true. | component §4 |

(Repeat sub-section for every component in scope.)

## 4. Behavior

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] On submit, primary action triggers exactly once even on rapid double-click. | component §5 |
| ☐ | blocker | [M] On Enter inside the form, submission triggers (does not navigate). | component §5 |
| ☐ | major | [A:playwright] Animations honor `prefers-reduced-motion` (collapse to instant when set). | system §8 |

## 5. Accessibility

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [A:playwright] Every interactive element is reachable by Tab. | a11y default |
| ☐ | blocker | [A:playwright] Tab order matches visual reading order. | a11y default |
| ☐ | blocker | [A:lint] Every input has an associated `<label>` (programmatically via `for`/`htmlFor` or wrapping). | component §7 |
| ☐ | blocker | [A:lint] Error messages are linked to their inputs via `aria-describedby`. | component §7 |
| ☐ | blocker | [A:axe] All text has at least 4.5:1 contrast (or 3:1 for large text) against background. | a11y default |
| ☐ | blocker | [M] Screen reader announces the agreed text on focus and on state change. | component §7 |
| ☐ | blocker | [M] Modal dialogs trap focus and return focus to the trigger on close. | component §5 |
| ☐ | major | [M] Pressing Escape closes any open popover/menu/modal and returns focus. | component §7 |
| ☐ | major | [A:lint] No element has `tabindex` greater than 0. | a11y default |

## 6. Visual polish

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | major | [M] Alignment: text baselines, icon centers, and button heights align to the spacing grid. | system §2 |
| ☐ | major | [M] All borders use `color.border.*` semantic tokens. | system §5 |
| ☐ | major | [A:lint] All colors used in the implementation are present in the system spec. (Run a script to scan stylesheets/computed styles for off-system values.) | system §4–5 |
| ☐ | minor | [M] Icons share a consistent stroke width and corner style. | system §1 |
| ☐ | polish | [M] Visual rhythm — repeated elements feel evenly spaced, not arbitrary. | system §2 |

## 7. Microcopy

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] Primary action button label is an action verb (not "Submit" or "OK" by default). | microcopy spec |
| ☐ | major | [M] Error messages explain the problem and suggest a fix (not "Invalid input"). | microcopy spec |
| ☐ | major | [M] Empty-state copy is friendly and tells the user what to do next. | microcopy spec |
| ☐ | major | [M] Loading copy reflects the actual operation (not generic "Loading…" if a more specific verb fits). | microcopy spec |
| ☐ | minor | [M] Tooltip text is short (under ~10 words) and describes value, not behavior. | microcopy spec |

## 8. Performance (optional)

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | major | [A:playwright] Largest Contentful Paint at primary breakpoint is under 2.5s on a 4G connection. | performance default |
| ☐ | major | [A:playwright] Cumulative Layout Shift below 0.1. | performance default |
| ☐ | minor | [A:unit] Total JS bundle for this feature under <user-specified budget>. | brief §7 |

## 9. Items intentionally NOT checked

(Some things are deliberately deferred. List them so the user knows.)
- <e.g. "Internationalization — feature is English-only for v1, per brief §8 non-goals.">
- <e.g. "Print styles — out of scope.">

## 10. Open questions
- <Numbered. e.g. "Should microcopy be reviewed by a copywriter before declaring 'ship'? Or is dev review sufficient?">
```

## Examples

### Example 1 — small component, focused checklist

**Input:** Component spec for a search input with autocomplete.

**Output:** A 30–50 item checklist heavy on States and Accessibility. Layout is small. Performance is minimal (an input shouldn't be performance-bound). Microcopy section covers placeholder, no-results message, loading text.

### Example 2 — full screen, broad checklist

**Input:** Brief + blueprint + 4 component specs + system spec for an admin settings page.

**Output:** A 80–150 item checklist with all 7 sections meaningfully populated. States section has a sub-table per component.

## Rules that prevent vague criteria

1. **Banned phrasings.** "Looks good", "feels right", "is clean", "is intuitive", "works well", "is polished" — all banned. Replace with a concrete property.
2. **Every criterion must have a clear pass/fail.** If two reviewers might disagree, rewrite to be more specific.
3. **Source every criterion.** Every line ends with `[source]` pointing to the spec section it derives from. If you can't, you've invented a criterion that wasn't in the spec — either remove it or add it to the spec first.
4. **Don't add criteria that aren't in the spec.** This includes "obvious" things. If the spec doesn't say "buttons should be at least 44px tall", don't add it. Surface as an open question instead.
5. **Severity is not optional.** Every item gets a severity. "Everything is a blocker" is also banned — it means severity wasn't actually thought about.

## Acceptance criteria for this skill's own output

A checklist produced by this skill is acceptable only if every one of these is true:

- [ ] Frontmatter links to at least one upstream spec.
- [ ] Every section that applies to the scope has at least one criterion (no empty sections — if a section doesn't apply, omit the section and note in §9).
- [ ] Every criterion has a severity (blocker / major / minor / polish).
- [ ] Every criterion has one explicit label: [A:playwright], [A:axe], [A:lint], [A:unit], or [M].
- [ ] Every criterion has a `[source]` reference to the spec.
- [ ] No banned phrasings appear (looks good, feels right, is clean, intuitive, etc.).
- [ ] If a feature is intentionally not checked, it appears in §9 with a reason.
- [ ] At least one criterion in §5 (Accessibility) is present — accessibility cannot be skipped.

If any check fails, revise before delivering.
