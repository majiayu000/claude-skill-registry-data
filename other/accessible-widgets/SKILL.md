---
name: accessible-widgets
description: Builds and repairs keyboard- and screen-reader-accessible interactive React components to the WAI-ARIA Authoring Practices (APG) - modal dialogs, menu buttons, comboboxes / autocomplete with a listbox popup, tabs, disclosures and accordions. Gives the exact roles, states, keyboard contracts and focus rules (roving tabindex vs aria-activedescendant, focus return, what Tab and Escape must do), React 19 implementation patterns (useId, refs and focus timing, inert, native dialog) and how to test them with Testing Library, user-event and axe-core in jsdom. Use when making a custom widget accessible, fixing an accessibility audit finding, adding keyboard navigation or ARIA attributes, or reviewing role/aria-* usage. Keywords - a11y, WCAG 2.1.1 keyboard, ARIA, role="menu", role="combobox", role="tablist", aria-expanded, aria-controls, aria-activedescendant, aria-selected, focus trap, focus management, screen reader.
license: MIT
---

# Accessible interactive widgets in React

The WAI-ARIA Authoring Practices Guide (APG) is the contract assistive-technology users rely on. A role
is a promise: `role="menu"` tells a screen reader user that arrow keys work, Escape closes, and focus is
managed for them. Ship the whole promise or don't make it. Bad ARIA is worse than no ARIA, because it
lies to the user about how the page behaves.

Work in this order: pick the right element or pattern, apply its contract exactly (roles, states,
keys, focus), implement it with the React mechanics below, then prove it with role- and focus-based
tests.

## 1. Pick the element before writing ARIA

| You need | Use | Not |
| --- | --- | --- |
| An action | `<button type="button">` | `div`/`span` with `onClick` |
| Navigation | `<a href>` | a button that sets `location` |
| Show/hide a section | disclosure: `<button aria-expanded>` + region, or `<details>`/`<summary>` | a menu |
| Site navigation dropdown | disclosure button + list of links | `role="menu"` (menus are for app-style action lists) |
| One value from a short fixed list | native `<select>` | a custom listbox |
| Free text with suggestions | ARIA combobox ([combobox.md](references/combobox.md)); `<input list>` + `<datalist>` if you can live with browser styling | `role="listbox"` alone |
| A list of actions behind a button | menu button ([menu-button.md](references/menu-button.md)) | `ul` of clickable `li` |
| Layered panels, one visible | tabs ([tabs-and-disclosure.md](references/tabs-and-disclosure.md)) | links that look like tabs, if they navigate |
| Blocking task over the page | `<dialog>` + `showModal()` ([dialog.md](references/dialog.md)) | a `div` overlay with `role="dialog"` you trap by hand, unless you must |

Native elements bring keyboard support, focusability and semantics for free. Every custom widget
you write instead owes the user all three.

## 2. Contract every composite widget owes

Checklist. Run it against any widget before calling it done.

- [ ] **One Tab stop per composite.** A tablist, menu, listbox or toolbar is one stop in the page Tab
      sequence. Arrow keys move inside it. Items inside get `tabIndex={-1}`; never `0` on every item.
- [ ] **One focus strategy, chosen on purpose** (table below). DOM focus or `aria-activedescendant`
      must always identify the active item; a CSS highlight alone is invisible to assistive tech.
- [ ] **States are present in both directions.** `aria-expanded="false"` when closed, not omitted:
      an absent `aria-expanded` means "not expandable". In React pass a boolean
      (`aria-expanded={open}` renders `"true"`/`"false"`), never `aria-expanded={open || undefined}`.
- [ ] **Every IDREF resolves.** `aria-controls`, `aria-labelledby`, `aria-activedescendant` must name an
      element that exists right now. Generate ids with `useId()`; hard-coded ids break the second
      instance on the page.
- [ ] **Everything interactive has a name**: the widget container (`tablist`, `menu`, `listbox`,
      `dialog`) via `aria-labelledby` or `aria-label`, inputs via `<label>`.
- [ ] **Keys by `event.key`** (`'ArrowDown'`, `'ArrowUp'`, `'ArrowLeft'`, `'ArrowRight'`, `'Home'`,
      `'End'`, `'Enter'`, `' '`, `'Escape'`, `'Tab'`). `keyCode`/`which` are deprecated.
      `preventDefault()` only keys you handle (arrows and Space scroll the page otherwise). In
      text inputs, ignore keys while `event.nativeEvent.isComposing` (IME input).
- [ ] **Focus moves are explicit.** Opening moves focus into the popup; closing by the user returns it
      to the invoker; if the invoker is gone, move it somewhere logical, never to `<body>`.
- [ ] **Hidden means hidden.** Closed popups and inactive panels are unmounted or `hidden`, so they
      are neither read nor tabbable.
- [ ] **Mouse and keyboard share one state machine.** Hover may move the highlight; click and Enter
      run the same `activate()`.

### Roving tabindex or aria-activedescendant

| | Roving tabindex | `aria-activedescendant` |
| --- | --- | --- |
| How | active item `tabIndex=0` (or `-1` + `.focus()`), others `-1`, call `.focus()` on move | DOM focus stays on the container or input; it carries `aria-activedescendant="<active id>"` |
| Use for | tabs, menus, toolbars, radio groups, grids | **combobox popups (required: typing must keep going to the input)**, listboxes with huge virtual lists |
| Free | browser scrolls the item into view, `:focus-visible` styling | no focus churn, input keeps caret and IME |
| You must | keep refs to items and focus after render | style the active item yourself, scroll it into view, keep the id pointing at a mounted element |

The referenced element must be a descendant of the focused element or be owned by it (`aria-owns`),
or, for a combobox, live in the popup it `aria-controls`.

## 3. Pattern contracts

Unmarked rules come from the APG pattern or the ARIA 1.2 Recommendation; "(APG example)" marks
behaviour the APG's reference example implements that the pattern text leaves open, and
"(optional)" marks extras. Implement optional behaviour when the product asks, never instead of a
rule.

### Disclosure

- `<button aria-expanded={open} aria-controls={regionId}>` (aria-controls optional), panel `hidden`
  when closed. Enter and Space toggle; a native button already does both.

### Tabs

- `role="tablist"` (named), children `role="tab"`, panels `role="tabpanel"`.
- Selected tab `aria-selected="true"`, every other tab `aria-selected="false"`.
- Each tab `aria-controls` its panel; each panel `aria-labelledby` its tab. Render all panels with
  `hidden`, or put `aria-controls` only on tabs whose panel is mounted.
- Tab enters the list **on the selected tab** and the next Tab leaves the list (to the panel).
- Left/Right Arrow move to previous/next tab and **wrap**. Home/End (optional) go to first/last.
- Automatic activation (selection follows focus) is recommended when panels render instantly;
  otherwise manual activation with Enter/Space. Vertical tablist: `aria-orientation="vertical"`
  and Up/Down instead.
- Panel `tabIndex={0}` when it has no focusable content of its own.

### Menu button and menu

- Trigger: a `button` with `aria-haspopup="menu"` (or `"true"`) and `aria-expanded` true/false;
  `aria-controls` to the menu is optional.
- Popup: `role="menu"` labelled by the button (`aria-labelledby`) or `aria-label`; children are
  `menuitem` / `menuitemcheckbox` / `menuitemradio`. No `li` or wrapper with an implicit role
  between `menu` and its items: use `<ul role="menu"><li role="menuitem">`, or `role="none"` on
  wrappers.
- Enter or Space on the button: open and focus the **first** item. Down Arrow (optional): first item;
  Up Arrow (optional): last item.
- In the menu: Down/Up move to next/previous (wrapping is optional; if you don't wrap, Home/End are
  required). Enter activates the item and **closes the menu**; focus then returns to the button
  (APG example). Escape closes and **returns focus to the button**. **Tab closes the menu** and focus moves on
  normally. Printable characters may jump to the next item starting with that letter (optional).
- Items are never Tab stops (`tabIndex={-1}`).

### Combobox with listbox popup (ARIA 1.2)

- `role="combobox"` goes **on the `<input>` itself**, labelled by its `<label>`. The ARIA 1.0/1.1
  shapes (combobox on a wrapper `div` with `aria-owns`, or a textbox inside a combobox) are
  non-conforming now; replace them.
- `aria-expanded` true/false (required), `aria-controls` = listbox id (required by ARIA 1.2 and the
  APG; set it at least while expanded), `aria-autocomplete="list"` when typing filters suggestions
  (`"both"` with inline completion, `"none"` if the list never changes). Implicit
  `aria-haspopup` is `listbox`; set it only for grid, tree or dialog popups.
- Popup `role="listbox"`, children `role="option"`. DOM focus **stays on the input**; the input's
  `aria-activedescendant` names the highlighted option, and that option alone has
  `aria-selected="true"` (selection follows focus in a combobox listbox).
- Down Arrow highlights the first (or next) option; Up Arrow the previous (or last). Enter accepts
  the highlighted option, puts its text in the input, closes the popup and keeps focus in the
  input; `preventDefault()` it so it doesn't also submit a surrounding form. Escape closes the popup (clearing the input on a second
  Escape is optional). Printable keys keep editing the input. Alt+Down/Alt+Up open/close
  (optional).
- Options and any open button are excluded from the Tab sequence.

### Modal dialog

- Prefer native `<dialog>` opened with `showModal()`: the browser makes everything else inert, puts
  the dialog in the top layer, closes it on Escape (`cancel` then `close` events), moves focus in, and
  on close returns focus to the element that was focused before it opened.
- Custom dialogs must do all of that by hand: `role="dialog"`, `aria-modal="true"`, a name via
  `aria-labelledby` (visible title) or `aria-label`, focus inside on open, Tab and Shift+Tab cycle
  inside, Escape closes, focus returns to the invoker, background `inert`.
- Initial focus: first focusable control by default; a `tabIndex={-1}` heading or first paragraph
  when content is long or structured; the least destructive button for irreversible actions.
- In React, `autoFocus` does not choose a native dialog's initial focus: on the client React calls
  `focus()` once at mount and never writes the `autofocus` attribute, so the browser's dialog
  focusing steps can't see it. Call `.focus()` on the intended element right after `showModal()`.
- Include a visible close/cancel button in the Tab sequence. Only mark a dialog modal if it really
  blocks the page, for everyone.

Full code and edge cases: [dialog.md](references/dialog.md), [menu-button.md](references/menu-button.md),
[combobox.md](references/combobox.md), [tabs-and-disclosure.md](references/tabs-and-disclosure.md).

## 4. React mechanics that decide whether it works

**Focus after render, not before.** The element you want to focus often does not exist yet in the
handler that opens the popup. Move focus in an effect keyed on the state that rendered it:

```tsx
useEffect(() => {
  if (expanded) optionRefs.current[focusIndex]?.focus()
}, [expanded, focusIndex])
```

React flushes effects from discrete events (key presses, clicks) before the next event, so this is
synchronous enough for keyboard users. Don't reach for `setTimeout`/`requestAnimationFrame` unless
something (an animation, a portal mounted later) really requires it; deferred focus can steal focus
back after the user has already tabbed away.

**Refs to many items.** Keep an array or `Map` of elements filled by callback refs:
`ref={(el) => { optionRefs.current[i] = el }}`. As of React 19 a callback ref may return a cleanup
function, so TypeScript rejects implicit returns (`ref={(el) => (x = el)}`): use a block body.
Function components receive `ref` as a normal prop in React 19, so new components don't need
`forwardRef`.

**Ids from `useId()`.** Call it once per instance and derive suffixes (`${id}-popup`,
`${id}-row-${row.id}`). The format is an implementation detail (React 19.2 emits `_r_1_`;
19.1 used `«r1»`; earlier versions used `:r1:`). Never parse it, and pass it through `CSS.escape()`
before using it in a selector. Never use it for list `key`s.

**`inert` is a boolean prop in React 19** (`<main inert={dialogOpen}>`). React 18 needed `inert=""`.
Inert subtrees can't be focused, clicked or read; it is the right tool to block the page behind a
custom modal or an off-canvas drawer.

**Portals.** React events bubble through the React tree, so a parent's `onKeyDown` sees keys from a
portaled menu; the DOM, focus order and Tab order follow the DOM tree. A popup portaled to the end of
`<body>` is not "after" its trigger for Tab, so manage focus explicitly or render the popup next to
its trigger. Native top layer (`<dialog>`, `popover`) avoids z-index portals altogether.

**Blur and pointer.** Close on blur only when focus left the widget:
`if (!root.contains(event.relatedTarget as Node)) close()`. In a combobox, `preventDefault()` on the
option's `mousedown` so the input never blurs before the click lands.

**Derive, don't duplicate.** `aria-expanded`, `hidden` and the rendered popup must come from the same
state variable, and the active option must be derived from the current suggestions so it can never
point at an unmounted element.

## 5. Anti-patterns and fixes

| Anti-pattern | Why it fails | Fix |
| --- | --- | --- |
| `<div onClick>` as a button or tab | not focusable, no role, no Enter/Space | `<button type="button">` (with `role="tab"` / `"menuitem"` where the pattern says) |
| Every tab/menu item tabbable | Tab walks through items instead of leaving the widget | roving tabindex: one `0`, the rest `-1` |
| Arrow handler updates state but never calls `.focus()` | screen reader and keyboard focus stay on the old item | focus in an effect, or use `aria-activedescendant` |
| `aria-expanded={open \|\| undefined}` | closed state reads as "not expandable" | `aria-expanded={open}` |
| `<ul role="menu"><li><button role="menuitem">` | `li` (listitem) between menu and item breaks the required structure | `li role="menuitem"`, or `li role="none"` |
| Combobox role on a wrapper `div`, `aria-owns` | ARIA 1.1 shape, no longer conforming | `role="combobox"` on the input, `aria-controls` to the listbox |
| Moving DOM focus into combobox options | typing stops reaching the input, caret is lost | keep focus on the input, use `aria-activedescendant` |
| Highlight only as a CSS class | assistive tech can't see it | `aria-activedescendant` + `aria-selected="true"` on the option |
| Hard-coded `id="listbox"` | second instance points at the first instance's popup | `useId()` |
| Escape closes but focus is lost | keyboard user is dumped at the top of the page | return focus to the trigger on every user-initiated close |
| Menu stays open on Tab | open popup floats over content the user moved to | close on Tab (and on blur outside) |
| `role="menu"` for site navigation | screen readers switch to application keys, links behave oddly | disclosure button + list of links |
| `aria-hidden="true"` on a focusable element or an ancestor of the dialog | focus lands on something that "doesn't exist" | `inert` or `hidden`; keep the dialog outside any hidden subtree |
| Positive `tabIndex` values | rewrites the page's Tab order | `0` or `-1` only |
| `keyCode === 13` | deprecated, wrong for some layouts | `event.key === 'Enter'` |

## 6. Prove it with tests

Test the contract the way a user meets it: by role and name, by keys, by where focus is.

```tsx
const user = userEvent.setup()
render(<ActionMenu actions={rowActions} onAction={handleAction}>Row actions</ActionMenu>)
const button = screen.getByRole('button', { name: 'Row actions' })
expect(button.getAttribute('aria-expanded')).toBe('false')
button.focus()
await user.keyboard('{Enter}')
expect(screen.getByRole('menuitem', { name: 'Duplicate' })).toBe(document.activeElement)
await user.keyboard('{Escape}')
expect(document.activeElement).toBe(button)
```

- To accept both focus strategies, compute the "effectively focused" element: `document.activeElement`,
  or the element named by its `aria-activedescendant`.
- Run axe-core on the open and the closed state, with the WCAG A/AA tags and `color-contrast`
  disabled (jsdom has no layout).
- Know the jsdom gaps before you trust a red or green test: as of jsdom 30 there is no
  `HTMLDialogElement.showModal()`/`close()`, no Popover API, no `scrollIntoView`, no `matchMedia`,
  and user-event's Tab ignores `inert`. Native-dialog behaviour needs a browser test (Playwright,
  Vitest browser mode) or an explicit test double.

Details, helpers and an axe setup: [testing.md](references/testing.md).

## References

- [references/dialog.md](references/dialog.md): native `<dialog>` component, custom fallback, focus rules.
- [references/menu-button.md](references/menu-button.md): full menu button, typeahead, activedescendant variant.
- [references/combobox.md](references/combobox.md): ARIA 1.2 autocomplete, select-only variant, pitfalls.
- [references/tabs-and-disclosure.md](references/tabs-and-disclosure.md): tabs (automatic and manual), disclosure, accordion.
- [references/testing.md](references/testing.md): Testing Library, user-event, axe-core, jsdom gaps.
- [references/sources.md](references/sources.md): the specifications and docs this skill was checked against.
