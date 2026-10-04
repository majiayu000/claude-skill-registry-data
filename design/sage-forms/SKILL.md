---
name: superpowers-sage:sage-forms
description: >
  HTML Forms + Sage integration — log1x/sage-html-forms, hf_get_form,
  addPostObject html-form, Blade form views, x-form.* shared components,
  hf-validation JS module, hf-success hf-error hf-submitted events,
  Constraint Validation API, form traps pattern escaping type-tel
  ValidityState non-enumerable — stateless contact forms with progressive
  JS validation on top of the HTML Forms WordPress plugin.
  Invoke for: contact form with HTML Forms plugin, hf_get_form usage, form validation
  with Constraint API, pattern escaping trap, type=tel Chrome bug, form audit.
user-invocable: false
---

# HTML Forms + Sage Integration

Stateless form rendering via the HTML Forms WordPress plugin, bridged into Sage by `log1x/sage-html-forms`. Forms live as a CPT (`html-form`), are referenced from ACF blocks via `addPostObject`, and render through a Blade filter that routes to project-controlled form views.

## When to Use

| Approach | Best for |
|---|---|
| **HTML Forms + sage-html-forms** | Stateless contact/lead forms; editors pick the form from a dropdown; submissions handled by the HF plugin |
| **Livewire form** | Reactive state, multi-step wizards, inline validation tied to server state |
| **Blade + native `<form>`** | Single-field or trivial forms with no submission pipeline |

## When NOT to Use

- Form requires multi-step state → use Livewire (`acorn-livewire` skill)
- Form payload drives a Laravel controller action → Acorn Routes + Blade form, not HTML Forms
- Form must be embedded outside a block context (e.g. header newsletter) → Blade component + native `<form>` is simpler

## Prerequisites

- Sage 11+ / Acorn 4+ on Bedrock with Lando
- ACF Composer installed (for the block field declaration)
- Shared `x-form.*` components present in `resources/views/components/form/` (the design-system form primitives)

## Installation Summary

```bash
lando composer require wpackagist-plugin/html-forms
lando theme-composer require log1x/sage-html-forms
```

Acorn's package discovery auto-registers the service provider — no manual wiring. Full details: [references/installation.md](references/installation.md).

## Integration Pattern Summary

The form is a `html-form` CPT post. A block exposes an ACF `addPostObject` field scoped to that CPT so the editor picks the form. The block view renders it via `hf_get_form($form->ID)->get_html()`, which the sage-html-forms provider intercepts and routes to a Blade view at `resources/views/forms/{form-slug}.blade.php`. The Blade form view uses the project's `x-form.*` components.

```blade
{{-- Block view (snippet) --}}
@if ($form)
    {!! hf_get_form($form->ID)->get_html() !!}
@endif
```

```blade
{{-- resources/views/forms/{form-slug}.blade.php --}}
<x-html-forms :form="$form">
    <x-form.field label="Name" for="name" :required="true">
        <x-form.input type="text" name="name" :required="true" minlength="2" />
    </x-form.field>
    {{-- ...more fields... --}}
    <x-button type="submit" variant="primary" class="w-full">Send</x-button>
</x-html-forms>
```

Full walkthrough: [references/blade-form-views.md](references/blade-form-views.md).

## Validation Module Summary

Client-side validation is a reusable ES module imported by the block's JS — never globally enqueued. The module exposes one function:

```js
initHfValidation(formEl, { messages, validators, onSuccess, onError });
```

Four layers: native HTML5 constraints, `blur` validation, `input` lazy re-validation while `aria-invalid="true"`, and post-submit scroll via the HTML Forms plugin's DOM events (`hf-success`, `hf-error`, `hf-submitted`).

Full API and implementation: [references/hf-validation.md](references/hf-validation.md).

## Traps (Critical)

Three documented bugs that silently break forms in this stack. Full symptom/root cause/fix for each: [references/traps.md](references/traps.md).

- **T1 — `pattern` attribute backslash escaping in Blade components.** `$attributes->merge()` double-escapes backslashes; `patternMismatch` never fires. Symptom: form submits even though `pattern` regex doesn't match user input. Workaround: use a JS validator, not a `pattern` attribute.
- **T2 — `type="tel"` skips `patternMismatch` in Chrome.** Use `type="text" inputmode="tel"` instead. Symptom: phone format validator silently no-ops in Chrome (works in Firefox/Safari).
- **T3 — `ValidityState` is non-enumerable.** Spread (`{ ...field.validity }`) and `Object.keys()` return empty. Symptom: your error-message lookup object is always empty. Access named properties directly: `validity.valueMissing`, `validity.patternMismatch`, `validity.tooShort`, `validity.customError`, etc.

## File Map (canonical per form integration)

| File | Role |
|---|---|
| `app/Blocks/{ClassName}.php` | ACF block — `addPostObject` field + `with()` mapping |
| `resources/views/blocks/{slug}.blade.php` | Block view — calls `hf_get_form($form->ID)->get_html()` |
| `resources/views/forms/{form-slug}.blade.php` | Form view — `x-html-forms` + `x-form.*` structure |
| `resources/js/blocks/{slug}.js` | Block custom element — imports `initHfValidation`, configures per form |
| `resources/js/modules/hf-validation.js` | Reusable validation module (one per project, not per form) |

## Consumers

- `agents/forms.md` (user-invocable specialist — analyzes and refactors existing forms, or scaffolds new ones)
- `skills/block-scaffolding/SKILL.md` Phase 0c (coordinated scaffold when a block embeds a form)

Both consumers treat this skill as authoritative — no pattern, template, or trap is documented outside this skill.
