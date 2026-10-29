---
name: frontend-a11y
description: "Use when building or reviewing accessible UI in a Laravel app — semantic Blade markup, accessible forms, keyboard navigation with Alpine, focus and live-region management for Livewire updates, contrast, and Filament accessibility."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/laravel/livewire.md` — keep Blade presentation-only; use `wire:model` for bindings; components stay slim.
- Apply `@rules/laravel/filament.md` — reuse Filament's built-in accessible form/action components rather than rebuilding them.
- Apply `@rules/security/frontend.md` — sanitize any dynamic content before DOM insertion; prefer `textContent`/`setAttribute` over `innerHTML`.
- Stack is Blade + Livewire + Alpine.js + Filament + Tailwind. No React/Vue/Next — never output `useState`/`useEffect`/`useRef`/JSX.

## Modes

This skill runs in one of two modes, selected by the caller via `MODE` (default `build`):

- **`build` (default)** — full accessibility work: write and correct Blade markup, add ARIA attributes and focus management, and adjust Alpine keyboard handlers. Every section below behaves as written unless it is explicitly flagged for `MODE=cr`.
- **`cr` (read-only lens — invoked by `@skills/code-review/SKILL.md`, `code-review-github`, `code-review-jira`, and `code-review-bugsnag` when the diff touches a frontend surface)** — **never modify a view or a component, never author a test, never stage / commit / push, never run fixers or checkers, and never chain a follow-up review.** Scope the analysis to the lines added or modified by the PR diff and return the findings as markdown only, carrying the reproducer fields the CR folds into its standard Critical / Moderate buckets.
Every instruction below that would touch a file — add, connect, replace, trap, announce, or any other such verb — is emitted as a written proposal carrying a concrete Blade / Alpine snippet, never applied to the project. The Checklist at the end of this file is the walk-through: run it against the changed markup and raise one finding per unmet item.

> **What this lens owns in a CR:** every accessibility finding on the diff — semantic markup, label / error association, keyboard operability, focus management, live-region announcement of Livewire updates, and contrast of the token pairs the markup uses. It is the **sole** owner of that surface: `@skills/frontend-patterns/SKILL.md` and `@skills/design-system/SKILL.md` defer here rather than raising an accessibility finding of their own.

## Use when
- Building or reviewing forms (`<input>`, `<select>`, `<textarea>`).
- Creating interactive elements (modals, dropdowns, tabs, tooltips) with Alpine.
- Adding `<div>`/`<span>` with `wire:click` or `x-on:click` instead of a button.
- Adding any `aria-*` attribute.
- Managing focus or announcing async updates after a Livewire round-trip.
- Acting on accessibility feedback from a review tool.

---

## Form accessibility

Missing `for`/`id` pairing and disconnected error messages are the most commonly flagged issues. Livewire's `@error` directive pairs naturally with `aria-describedby`.

### Label connection

```blade
{{-- BAD: no association --}}
<label>Email</label>
<input type="email" wire:model="email">

{{-- GOOD: for matches id --}}
<label for="email">Email</label>
<input id="email" type="email" wire:model="email">
```

### Required fields

```blade
{{-- visual asterisk hidden from SR; required + aria-required convey state --}}
<label for="email">Email <span aria-hidden="true">*</span></label>
<input id="email" type="email" required aria-required="true" wire:model="email">
```

### Error association with Livewire

```blade
<label for="email">Email <span aria-hidden="true">*</span></label>
<input
    id="email"
    type="email"
    wire:model.blur="email"
    autocomplete="email"
    @error('email') aria-invalid="true" aria-describedby="email-error" @enderror
>
@error('email')
    <span id="email-error" role="alert" class="text-danger">{{ $message }}</span>
@enderror
```

`@error` controls both the `aria-invalid`/`aria-describedby` wiring and the message, so the link is always consistent with the validation state. Use `fieldset`/`legend` to group related controls (radio sets, address blocks).

**Filament forms** already emit connected labels, `aria-describedby` error wiring, and required markers. Reuse Filament form components instead of hand-rolling markup; do not strip their generated attributes.

---

## ARIA — only when native HTML is insufficient

Wrong ARIA is worse than none.

```blade
{{-- aria-label: when no visible text exists --}}
<button type="button" aria-label="Close" wire:click="close">
    <x-heroicon-o-x-mark aria-hidden="true" class="h-5 w-5" />
</button>

{{-- aria-labelledby: when a visible heading exists --}}
<section aria-labelledby="orders-title">
    <h2 id="orders-title">Recent Orders</h2>
</section>
```

Expandable trigger:

```blade
<button type="button" aria-expanded="false" aria-controls="panel"
        x-data x-on:click="$el.setAttribute('aria-expanded', $el.getAttribute('aria-expanded') === 'true' ? 'false' : 'true')">
    Details
</button>
<div id="panel" x-show="open" hidden>…</div>
```

---

## Keyboard navigation with Alpine

Every interactive element must be reachable and operable by keyboard alone. Build custom widgets with Alpine event modifiers.

```blade
<div x-data="{ open: false, active: 0, options: @js($options) }"
     role="combobox" :aria-expanded="open" aria-haspopup="listbox" tabindex="0"
     x-on:keydown.arrow-down.prevent="active = Math.min(active + 1, options.length - 1)"
     x-on:keydown.arrow-up.prevent="active = Math.max(active - 1, 0)"
     x-on:keydown.enter.prevent="$wire.select(options[active]); open = false"
     x-on:keydown.escape="open = false"
     x-on:click="open = !open">
    <span x-text="options[active]"></span>
    <ul x-show="open" role="listbox">
        <template x-for="(opt, i) in options" :key="opt">
            <li role="option" :aria-selected="i === active" x-text="opt"
                x-on:click="$wire.select(opt); open = false"></li>
        </template>
    </ul>
</div>
```

### Modal / dialog with focus trap

```blade
<div x-data="{ open: @entangle('showModal') }" x-show="open" x-cloak
     role="dialog" aria-modal="true" aria-labelledby="modal-title"
     x-on:keydown.escape.window="open = false"
     x-trap.noscroll="open"
     {{-- x-trap (Alpine focus plugin) cycles Tab/Shift+Tab inside and restores focus on close --}}
     tabindex="-1">
    <h2 id="modal-title">{{ $title }}</h2>
    {{ $slot }}
    <button type="button" wire:click="$set('showModal', false)">Close</button>
</div>
```

`x-trap` from the official Alpine Focus plugin handles the trap and restoring focus to the opener. If the plugin is not installed, save `document.activeElement` on open and call `.focus()` on it when closing.

---

## Focus & live regions for Livewire updates

A Livewire request swaps DOM fragments; focus and announcements must survive it.

- **Loading feedback:** `wire:loading` / `wire:target` toggle visible state without script.
- **Announce async results** with a polite live region so screen readers hear them:

```blade
<div aria-live="polite" aria-atomic="true" class="sr-only">
    <span wire:loading wire:target="save">Saving…</span>
</div>
@if (session('status'))
    <div role="status" aria-live="polite">{{ session('status') }}</div>
@endif
```

- **Urgent errors** use `aria-live="assertive"` (or `role="alert"`), nothing else.
- **Return focus after a modal closes** — dispatch a Livewire/Alpine event and `.focus()` the trigger, or rely on `x-trap`.
- **Preserve focus across re-render** — give moving elements a stable `wire:key`; without it Livewire may discard the focused node.
- **Disable controls during requests** with `wire:loading.attr="disabled"` so double-submits are blocked accessibly.

---

## Images, icons, contrast, motion

```blade
<img src="/decoration.png" alt="" aria-hidden="true">                {{-- decorative --}}
<img src="/chart.png" alt="Revenue rose 23% from Jan to Mar">       {{-- meaningful --}}
<button type="button" aria-label="Delete"><x-heroicon-o-trash aria-hidden="true" /></button>
```

- **Contrast:** ensure Tailwind text/background token pairs meet WCAG AA (4.5:1 body, 3:1 large). Verify both light and `dark:` variants. Never rely on color alone to convey state — pair with text or an icon.
- **Reduced motion:** gate animation with Tailwind's `motion-safe:`/`motion-reduce:` variants instead of always-on transitions.

```blade
<div class="transition-transform motion-reduce:transition-none">…</div>
```

For Alpine transitions, branch on the media query:

```blade
<div x-data="{ reduce: window.matchMedia('(prefers-reduced-motion: reduce)').matches }"
     x-transition:enter="reduce ? '' : 'transition duration-300'">…</div>
```

---

## WCAG 2.2 success criteria

These criteria are the ones templated Blade/Livewire UI most often misses. They complement the patterns above.

### Target size — SC 2.5.8 (AA)

Interactive targets must be at least **24×24 CSS px** (or have 24px spacing around them). Icon-only buttons and tight table-row actions are the usual offenders.

```blade
{{-- BAD: 16px hit area --}}
<button type="button" class="h-4 w-4" aria-label="Edit" wire:click="edit">
    <x-heroicon-o-pencil aria-hidden="true" />
</button>

{{-- GOOD: 24px minimum hit area (padding counts toward the target) --}}
<button type="button" class="h-6 w-6 p-1 -m-1" aria-label="Edit" wire:click="edit">
    <x-heroicon-o-pencil aria-hidden="true" class="h-4 w-4" />
</button>
```

### Focus visible — SC 2.4.7 (AA)

Every focusable element needs a clearly visible focus indicator. Never strip the outline without replacing it; prefer `focus-visible:` so the ring shows for keyboard users without firing on mouse click.

```blade
{{-- BAD: focus removed, keyboard users lose their place --}}
<button class="focus:outline-none" wire:click="save">Save</button>

{{-- GOOD: high-contrast ring, keyboard-only --}}
<button class="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-600 focus-visible:ring-offset-2"
        wire:click="save">Save</button>
```

### Redundant entry — SC 3.3.7 (A)

Within one process (multi-step form, checkout) never ask the user to re-enter information they already provided. Persist it on the Livewire component (or session) and prefill, offering an explicit "same as …" shortcut instead of a blank field.

```blade
<label><input type="checkbox" wire:model.live="billingSameAsShipping"> Billing address same as shipping</label>
@unless ($billingSameAsShipping)
    {{-- billing fields, prefilled from the shipping step --}}
@endunless
```

### Dragging movements — SC 2.5.7 (AA)

Any drag-to-reorder/drag-to-move interaction must have a single-pointer alternative (move up/down buttons or a position field), so users who cannot drag can still operate it.

```blade
<li>
    {{ $item->name }}
    <button type="button" aria-label="Move up" wire:click="moveUp({{ $item->id }})"><x-heroicon-o-arrow-up aria-hidden="true" /></button>
    <button type="button" aria-label="Move down" wire:click="moveDown({{ $item->id }})"><x-heroicon-o-arrow-down aria-hidden="true" /></button>
</li>
```

### Error suggestions — SC 3.3.3 (AA)

When validation fails and a fix is known, the message must suggest the correction, not just report invalidity. Keep the suggestion generic enough not to leak sensitive data (see `@rules/security/backend.md`).

```php
// BAD: 'date' => 'Invalid value.'
// GOOD: 'date' => 'Enter the date as YYYY-MM-DD, e.g. 2026-06-15.'
```

---

## Anti-patterns

```blade
<div wire:click="save">Save</div>                  {{-- non-interactive element with handler --}}
<div aria-label="Navigation">…</div>               {{-- aria-label on element with no role --}}
<input placeholder="Email">                        {{-- placeholder used instead of label --}}
<button tabindex="3">Submit</button>               {{-- positive tabindex breaks tab order --}}
<button aria-hidden="true">Open</button>           {{-- aria-hidden on a focusable element --}}
```

---

## Checklist

- [ ] Every `<input>`/`<select>`/`<textarea>` has a connected `<label for>`.
- [ ] Errors link via `@error` → `aria-describedby` and carry `role="alert"`.
- [ ] No `wire:click`/`x-on:click` on a `<div>`/`<span>` without role, `tabindex`, and key handling.
- [ ] Icon-only buttons have `aria-label`; their icons are `aria-hidden`.
- [ ] Decorative images use `alt=""` and `aria-hidden="true"`.
- [ ] Modals trap focus and restore it on close (`x-trap` or manual save/restore).
- [ ] Async Livewire results announce via `aria-live`; controls disable during requests.
- [ ] Moving elements have a stable `wire:key` so focus survives re-render.
- [ ] Token color pairs meet AA contrast in light and dark; state is not color-only.
- [ ] Animations respect `motion-reduce:` / `prefers-reduced-motion`.
- [ ] Interactive targets are at least 24×24 CSS px (SC 2.5.8).
- [ ] Focus indicators are visible via `focus-visible:` and never stripped without replacement (SC 2.4.7).
- [ ] Multi-step flows never re-ask data already entered (SC 3.3.7).
- [ ] Drag-to-reorder interactions have a single-pointer alternative (SC 2.5.7).
- [ ] Validation messages suggest the correction without leaking sensitive data (SC 3.3.3).
- [ ] Filament's generated accessibility attributes are left intact.

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
