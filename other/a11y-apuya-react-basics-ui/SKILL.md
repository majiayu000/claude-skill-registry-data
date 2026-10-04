---
name: a11y
description: Audits and remediates web accessibility against WCAG 2.2 Level AA. Checks keyboard reachability, tab order, focus management, visible focus, screen-reader semantics (HTML, ARIA, name/role/value), color contrast, hit-target size, reduced motion, form labels and errors, live regions, heading and landmark structure, and image/media alternatives. Produces tiered findings — Blocker / High / Medium with success-criterion citations, plus a separate Polish tier for best-practice items below AA. Also writes accessibility specs for new components (keyboard model, ARIA pattern, focus order, error semantics) and explains why a pattern fails. Triggers on "accessibility", "a11y", "wcag", "keyboard navigation", "tab order", "skip link", "screen reader", "aria", "semantic html", "alt text", "color contrast", "focus ring", "focus order", "focus trap", "reduced motion", "hit target", "touch target", "live region", "landmark", "heading order", "a11y audit", "accessibility audit", "axe", "section 508".
---

# Accessibility Engineer

## Mode Router

Pick one mode per invocation. If ambiguous, ask.

| Mode | Use when | Output |
|------|----------|--------|
| **Audit** | A built page or component needs an a11y review | Tiered findings list with SC citations and fixes |
| **Fix** | Specific violations need remediation in code | Inline diffs with before/after and the SC each fix satisfies |
| **Spec** | A new component or pattern needs an a11y contract before implementation | Component a11y spec (keyboard model, ARIA, focus, errors) |
| **Educate** | The user is asking *why* a pattern fails or which approach is correct | Short explanation grounded in a specific SC and one prescribed fix |

The baseline is **WCAG 2.2 Level AA**. Every Blocker/High/Medium finding cites at least one success criterion. Best-practice findings that don't map to an AA failure go in the **Polish** tier.

---

## Scope in this project

`react-basics-ui` ships **primitives, not pages**. That splits WCAG into two piles,
and auditing the wrong pile produces findings nobody can act on.

**In scope — the library owns these.** They are baked into a component and every
consumer inherits them:

- Role, accessible name, and value for each component (`role="dialog"`, `combobox`, `listbox`, `columnheader`, …)
- The keyboard model of each interactive pattern (menu, listbox, tabs, dialog, tree)
- Focus visibility, focus order within a component, focus trap and restore for overlays
- Contrast of the semantic colour tokens, in **both** themes
- Hit-target size of interactive primitives
- `prefers-reduced-motion` handling (8 files use `motion-reduce:` today)
- Live-region semantics for components that announce — `Toast`, `Alert`, `BaseAlertBox`, `Skeleton`, `Table`
- Form label/description/error wiring (`FormField`, `FormGroup`, `generateFormId`)

**Out of scope — the consuming application owns these.** Do not file them as
findings against this repo:

- Skip links, landmark structure (`<main>`, `<nav>`), one-`<h1>`-per-page, heading order across a page
- Page `<title>` and route-change announcements
- Reading order of a full screen

`Heading` is the interesting boundary: this library provides the *element and
visual level* (`level` vs `as`), but only the consumer can know whether the
resulting document outline is correct. Make the component capable of correct
usage; don't try to enforce it.

### Tooling here

- **`@storybook/addon-a11y` is registered globally** in `.storybook/main.ts`, so axe runs on every story. `npm run storybook` → Accessibility panel. This is the primary automated check.
- **No `jest-axe` in the unit suite.** Assertions in `*.test.tsx` cover roles and names via Testing Library queries (`getByRole`, `getByLabelText`) — which is itself an accessibility check, since a query that fails means the accessible tree is wrong.
- **Focus rings come from tokens, not hand-written classes.** Use `FOCUS_RING` or `FOCUS_RING_TIGHT` from `@/components/shared/styles/focus.styles`. Writing a bespoke `focus-visible:ring-*` string is a finding.

## Severity Rubric

| Tier | Definition | Examples |
|------|------------|----------|
| **Blocker** | A user with a covered disability cannot complete a primary task. AA failure on a critical path. | Submit button unreachable by keyboard; form errors announced to no one; modal traps sighted users but releases focus on dismiss to `<body>`. |
| **High** | AA failure that degrades but does not prevent task completion, OR a failure on a non-primary path. | Decorative icons announced as "image"; one form field missing programmatic label; heading order skips a level inside a section. |
| **Medium** | AA failure with low real-world impact (rare path, redundant affordance available). | Visually-hidden text duplicated by `aria-label`; redundant `role="button"` on a `<button>`. |
| **Polish** | Below AA but degrades the experience: weak focus rings that pass contrast, hit targets between 24×24 and 44×44 with no documented rationale, missing skip-link on a long page, motion that respects `prefers-reduced-motion` but is still aggressive at default settings. | Listed separately so the reader can defer them. |

Polish findings do **not** cite SCs as failures — they may reference *advisory* techniques or 2.2 AAA criteria (e.g., 2.5.5 Target Size (Enhanced)).

---

## WCAG 2.2 AA Quick Reference

The criteria most often violated, with the threshold and a one-line check.

### Perceivable
- **1.1.1 Non-text Content** — Every `<img>` has `alt`; decorative images use `alt=""` or `role="presentation"`. Icons conveying meaning have an accessible name.
- **1.3.1 Info and Relationships** — Structure conveyed visually is also conveyed in the DOM (headings as `<h1–h6>`, lists as `<ul>/<ol>`, table headers as `<th scope>`).
- **1.3.5 Identify Input Purpose** — Common inputs use `autocomplete` (e.g., `email`, `name`, `tel`).
- **1.4.3 Contrast (Minimum)** — Text ≥ **4.5:1** against background; large text (≥ 18pt or 14pt bold) ≥ **3:1**.
- **1.4.10 Reflow** — Content at 320 CSS px wide / 256 px tall with no two-dimensional scrolling.
- **1.4.11 Non-text Contrast** — UI components and meaningful graphics ≥ **3:1** against adjacent colors. *Focus indicators are UI components.*
- **1.4.12 Text Spacing** — Layout survives user-applied: line-height 1.5×, paragraph spacing 2×, letter spacing 0.12em, word spacing 0.16em.
- **1.4.13 Content on Hover or Focus** — Hover/focus popups are dismissible, hoverable, and persistent until dismissed or invalid.

### Operable
- **2.1.1 Keyboard** — Every interactive element reachable and operable with keyboard alone.
- **2.1.2 No Keyboard Trap** — Focus can enter and leave every region with standard keys.
- **2.4.3 Focus Order** — Tab order matches reading/visual order.
- **2.4.4 Link Purpose (In Context)** — Link text or its accessible name explains the destination. "Click here" / "Read more" alone fails.
- **2.4.6 Headings and Labels** — Section headings and form labels describe topic or purpose.
- **2.4.7 Focus Visible** — A visible focus indicator on every keyboard-focusable element.
- **2.4.11 Focus Not Obscured (Minimum)** *(2.2, AA)* — Focused element not entirely hidden by author-created overlays (sticky headers, cookie banners).
- **2.5.7 Dragging Movements** *(2.2, AA)* — Drag operations have a single-pointer alternative (click, button, keyboard).
- **2.5.8 Target Size (Minimum)** *(2.2, AA)* — Pointer targets ≥ **24×24 CSS px**, OR have ≥ 24 px of clear spacing, OR are inline in a sentence, OR are essential. Best practice (AAA, 2.5.5) is **44×44**.

### Understandable
- **3.2.1 On Focus** — Focusing an element does not trigger a context change (navigation, form submit, focus jump).
- **3.2.2 On Input** — Changing a control's value does not trigger a context change unless the user has been warned.
- **3.3.1 Error Identification** — Errors are identified in text, not by color alone.
- **3.3.2 Labels or Instructions** — Inputs that require user data have a visible label or instruction.
- **3.3.3 Error Suggestion** — When the system knows the correction, it suggests it.
- **3.3.7 Redundant Entry** *(2.2, A)* — Don't re-ask for information given earlier in the same flow (autofill, pre-fill, or carry forward).
- **3.3.8 Accessible Authentication (Minimum)** *(2.2, AA)* — No cognitive-function test (puzzles, transcription) without an alternative or assistance.

### Robust
- **4.1.2 Name, Role, Value** — Every custom control has a programmatic name, role, and current state/value.
- **4.1.3 Status Messages** — Status/feedback that doesn't move focus is conveyed via `role="status"`, `role="alert"`, or `aria-live`.

---

## Keyboard Contract

Every interactive surface must answer:

1. **Reachable?** — Tab visits every actionable element. Hidden controls (display:none, visibility:hidden, `hidden`) are skipped; `inert` content is skipped.
2. **Operable?** — `Enter`/`Space` activates buttons; `Enter` follows links; arrow keys navigate composite widgets (menus, tabs, listboxes, grids) per the WAI-ARIA Authoring Practices pattern for that role.
3. **Escapable?** — `Esc` closes any transient overlay (modal, popover, menu) and returns focus to the trigger.
4. **Ordered?** — DOM order matches reading order. Never use positive `tabindex`.

### Patterns to memorize

| Widget | Activation | Inner navigation | Close |
|--------|-----------|------------------|-------|
| Button | Enter, Space | — | — |
| Link | Enter | — | — |
| Disclosure (collapsed/expanded) | Enter, Space | — | — |
| Tabs (manual) | Enter, Space on tab | ←/→ between tabs, Home/End | — |
| Tabs (auto-activate) | focus = activate | ←/→, Home/End | — |
| Menu / Menubar | Enter, Space | ↑/↓ items, ←/→ submenus, type-ahead | Esc |
| Listbox | Enter, Space | ↑/↓, Home/End, type-ahead | Esc (if popup) |
| Combobox | type to filter | ↓ into listbox, Enter selects | Esc clears or closes |
| Dialog (modal) | trigger Enter/Space | Tab cycles within dialog | Esc, close button |
| Tooltip | hover OR focus shows | — | Esc, blur |

---

## Focus Management

- **Move focus** when: a modal opens (to the dialog or first focusable element), a destructive confirmation appears (to the safe default), an async action completes and the next step is in a new region (to a status message that is focusable, or to the new region's heading with `tabindex="-1"`).
- **Restore focus** when: a modal/menu/popover closes — to the element that opened it. If that element is gone (e.g., deleted), move focus to the nearest sensible ancestor and announce the deletion via a live region.
- **Trap focus** only inside modal dialogs (`role="dialog" aria-modal="true"`). Non-modal popovers, tooltips, and inline disclosures must let Tab leave naturally.
- **Visible focus** must meet **1.4.11** (3:1 against adjacent colors) and be at least 2 CSS px thick or use an equivalent area indicator. Removing the default ring without replacing it fails **2.4.7**.

---

## Screen-Reader Semantics

### Prefer semantic HTML over ARIA

The first rule of ARIA: don't use ARIA. A native element gives you role, state, keyboard handling, and accessible name for free.

| Want | Use | Not |
|------|-----|-----|
| Clickable action | `<button type="button">` | `<div onclick>` with `role="button"` |
| Navigation | `<a href>` | `<span onclick>` with `role="link"` |
| Form input | `<input>`, `<textarea>`, `<select>` | contenteditable div |
| Toggle | `<input type="checkbox">` or `<button aria-pressed>` | `<div>` with class names |
| Region heading | `<h2>`–`<h6>` in document order | `<div class="heading">` |
| List of items | `<ul>` / `<ol>` / `<li>` | `<div>` siblings |
| Tabular data | `<table>` with `<th scope>` | grid of divs |

### When ARIA is correct

- Composite widgets the platform doesn't ship (combobox, tree, tablist, grid, listbox with custom rendering).
- Live status that the user did not initiate (`role="status"`, `aria-live="polite"`) or critical alerts (`role="alert"`, `aria-live="assertive"`).
- Programmatic relationships not expressible in HTML (`aria-controls`, `aria-describedby`, `aria-owns`).
- Disabling something for AT without the native `disabled` semantics (`aria-disabled="true"` when the control must remain focusable to expose tooltips/errors).

### Naming priority

For accessible name, in order:
1. The element's labeled content (`<button>Save</button>`, `<label for>`).
2. `aria-labelledby` referencing visible text.
3. `aria-label` (use sparingly — invisible names drift from visible UI).

A control without a name fails **4.1.2** and is reported by AT as the element type alone ("button," "edit text").

---

## Forms

- Every input has a programmatically associated label: `<label for="id">` + `id`, or a wrapping `<label>`, or `aria-labelledby` pointing to visible label text. `placeholder` is **not** a label (fails **3.3.2**).
- Required state is conveyed in text AND programmatically (`aria-required="true"` or native `required`). An asterisk alone is decorative.
- Error messages are associated via `aria-describedby` pointing at the message element's `id`. The message text explains *what is wrong* and *what to do* (3.3.3).
- Invalid state is exposed via `aria-invalid="true"` while the error is present, and removed when the user corrects it.
- Error summaries (multi-error forms) are announced via `role="alert"` on first appearance, then `aria-live="polite"` for updates. Focus moves to the first invalid field or to the summary.
- Group related fields with `<fieldset>` + `<legend>` (radio groups, address blocks). Don't use a heading inside a form to substitute for a legend.
- Use `autocomplete` tokens on common fields to satisfy **1.3.5** and to enable autofill.

---

## Color, Contrast, Motion

- Measure contrast against the **actual rendered background**, including overlays and gradients. Test the worst-case position.
- Never rely on color alone (**1.4.1**). Pair with icon, text, underline, pattern, or position.
- Focus rings must meet **1.4.11** (3:1) against every background they appear over. Two-color outlines (light + dark) survive both themes.
- Respect `prefers-reduced-motion: reduce` — non-essential motion is suppressed, not just slowed. Essential motion (e.g., a progress bar) is allowed but should be muted (smaller amplitude, lower frequency).
- Avoid content that flashes more than **3 times per second** (**2.3.1**).

---

## Headings, Landmarks, and Page Structure

- One `<h1>` per page or per primary view. Subsequent headings step down without skipping (no `<h2>` jumping to `<h4>`). *(Consumer-owned — see Scope. This library's `Heading` separates visual `level` from semantic `as` precisely so a consumer can satisfy this.)*
- Use landmarks: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`. Each instance of a repeated landmark needs a distinguishing `aria-label` (e.g., two `<nav>`s labeled "Primary" and "Section").
- Provide a **skip link** as the first focusable element on pages with repeated navigation: `<a href="#main">Skip to main content</a>` that targets `<main id="main" tabindex="-1">`.
- Page `<title>` describes the current view and is updated on client-side route changes (**2.4.2**).

---

## Tables, Lists, Media

- Data tables use `<th>` with `scope="col"` or `scope="row"`. Layout tables (rare) use `role="presentation"`.
- Complex tables (merged headers) use `headers` attribute referencing `id`s.
- Lists of items use `<ul>`/`<ol>` even when styled without bullets — assistive tech announces count.
- Video has captions (**1.2.2**) and, if it conveys info beyond the audio track, audio description (**1.2.5**).
- Audio-only has a transcript.
- Auto-playing media: avoid; if essential, provide pause control within reach (**1.4.2**).

---

## Common Anti-Patterns

These appear in audits repeatedly and a "fix" often creates a new violation. Flag and replace, don't paper over.

| Anti-pattern | Why it fails | Fix |
|--------------|--------------|-----|
| `<div onclick>` with no role/tabindex | Not focusable, not announced as actionable (**2.1.1**, **4.1.2**) | Replace with `<button type="button">`. |
| `role="button"` on `<a href>` | Conflicting semantics; activation keys mismatch (Enter vs. Space) | Use `<button>` for actions, `<a>` for navigation. |
| `tabindex="1"` (or any positive) | Breaks document order (**2.4.3**) | Remove. Use DOM order; `tabindex="0"` only to add a non-interactive element to tab order, `tabindex="-1"` only to make a programmatic focus target. |
| `aria-label` duplicating visible text | Either redundant or, worse, conflicts with the visible label | Remove `aria-label`; let the visible text be the name. |
| `aria-hidden="true"` on a focusable element | Element is in the tab order but invisible to AT — keyboard users land on "nothing" | Either remove `aria-hidden` or also remove the element from tab order (`inert`, or `tabindex="-1"` + hide). |
| Removing focus outline with no replacement | Fails **2.4.7** | Style a focus ring that meets **1.4.11** (3:1). |
| Toast that disappears in 3 seconds | Not enough time to read; not announced to AT | Use `role="status"` (or `alert` if critical), persist until user dismisses or for ≥ 20 s per **2.2.1**. |
| Modal with focus released to `<body>` on close | Keyboard user loses place (**2.4.3**) | Restore focus to the trigger. |
| Skeleton loader without an accessible "loading" announcement | Sighted users see progress; AT users hear silence | `aria-busy="true"` on the region + a `role="status"` "Loading…" message. |
| `placeholder` used as the only label | Fails **3.3.2**; vanishes on input | Add a real `<label>`. |
| Color-only required indicator (red asterisk, no text) | Fails **1.4.1** | Add text "required" or use `required` attribute + visible "Required" in the label. |
| Drag-and-drop with no keyboard alternative | Fails **2.5.7** (2.2) | Add a button menu ("Move up", "Move to…") or keyboard reorder. |

---

## Audit Workflow

When invoked in Audit mode:

1. **Scope** the audit — which component or set of components. If unspecified, ask. Skip the page-level walk below for library work; it applies to a consuming application.
2. **Identify the primary task** on that surface. Findings on the primary path escalate one tier.
3. **Walk the page** in this order, recording findings as you go:
   - Landmarks & heading order
   - Keyboard reachability (Tab from the top)
   - Focus visibility on each stop
   - Forms (labels, errors, required, autocomplete)
   - Interactive widgets (correct ARIA pattern + keys)
   - Images and icons (names vs. decorative)
   - Color contrast (text, icons, focus rings)
   - Motion and animation
   - Live regions and async announcements
4. **Render findings** in the format below.
5. **Definition of Done** at the end.

### Finding format

```
### [Blocker|High|Medium|Polish] <one-line title>
SC: 1.4.3 Contrast (Minimum)         ← omit for Polish, or cite advisory
Location: <selector | component name | screen + element>
Observed: <what is currently true>
Impact: <which user, which task, what breaks>
Fix: <one prescribed change; reference a token role or ARIA attribute by name>
```

Group findings by tier, then by region. Lead with Blockers.

### Definition of Done

```
- 0 Blockers → Ready; 1+ → Iterate; 3+ → Blocked
- Every High has a named owner or a fix proposal → Ready
- Keyboard path documented for the primary task → Ready
- Focus restoration verified for every overlay → Ready
- Contrast measured against rendered background, not source color → Ready
- All findings cite an SC (Polish may cite advisory) → Ready
```

---

## Fix Workflow

When invoked in Fix mode:

1. Confirm the failing SC and the user-visible impact before editing.
2. Prefer **semantic HTML** changes over ARIA additions.
3. Apply the minimum change that satisfies the SC. Don't refactor adjacent code.
4. For each diff, comment with `// a11y: <SC short title>` so future readers see why the construct exists.
5. Re-check related criteria — fixing a focus ring (2.4.7) often interacts with non-text contrast (1.4.11); adding `aria-describedby` interacts with `aria-invalid` (3.3.1).
6. Note any **Polish** items deferred and why.

---

## Spec Workflow (new component)

When invoked in Spec mode for a new component, produce:

```
# <Component> — Accessibility Spec

## Role and name
- Native element or role: <e.g., button, role="dialog", role="combobox">
- Accessible name source: <visible text | aria-labelledby | aria-label>
- Required state attributes: <e.g., aria-expanded, aria-selected, aria-invalid>

## Keyboard model
| Key | Action |
| ... | ... |

## Focus
- On open: <where focus moves>
- On close: <where focus returns>
- Trap: <yes (modal) | no>
- Visible focus: <which token role>

## Live regions
- Status changes announced via: <role="status" | role="alert" | none>

## States and their SCs
| State | Visual | Programmatic | Announced |
| ... | ... | ... | ... |

## Required SC coverage
- 4.1.2 Name, Role, Value — how satisfied
- 2.1.1 Keyboard — how satisfied
- 2.4.7 Focus Visible — how satisfied
- 1.4.11 Non-text Contrast — for focus and meaningful icons
- (any role-specific SCs)

## Reference pattern
Cite the ARIA Authoring Practices pattern this implements (e.g., "APG: Dialog (Modal)").
```

---

## Educate Workflow

When the user is asking *why* a pattern fails:

1. Name the SC and quote its intent in one sentence.
2. State the observed failure in one sentence.
3. Prescribe one fix (not three options).
4. Stop. Don't lecture.

---

## Testing

Treat tooling as a triage filter, not a verdict. Automated tools catch roughly a third of issues.

- **Automated** — here that is `@storybook/addon-a11y` (axe, registered globally, runs on every story). `axe-core` wrappers such as `@axe-core/playwright` or `jest-axe` are not installed.
- **Keyboard** — Unplug the mouse. Tab through the page. Every interactive element should be reachable, visible when focused, and operable.
- **Screen reader** — At minimum: VoiceOver on macOS/iOS, NVDA on Windows, TalkBack on Android. Walk the same path. Listen for: unnamed controls, missing state, missing announcements after async actions.
- **Zoom** — Browser zoom to 200% and 400% (**1.4.4**). Reflow check at 320 CSS px (**1.4.10**).
- **OS preferences** — `prefers-reduced-motion`, `prefers-contrast`, forced-colors (Windows High Contrast). The UI should adapt, not break.

---

## What This Skill Will Not Do

- Promise WCAG conformance from automated tools alone.
- Recommend `aria-*` to "patch" a semantic-HTML problem when an element swap is available.
- Output findings without a cited SC (Blocker/High/Medium) or an explicit Polish tag.
- Strip a focus ring without specifying its replacement.
- Approve a modal pattern without focus trap and restoration.
