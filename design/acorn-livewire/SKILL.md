---
name: superpowers-sage:acorn-livewire
description: >
  Livewire v3 in WordPress via Acorn: Livewire component, wire:model, wire:model.live,
  @livewire directive, reactive component, livewire component, make:livewire,
  Alpine + Livewire, wire:click, wire:submit, WithFileUploads, computed properties,
  mount lifecycle, hydrate, Acorn Livewire, roots/acorn-livewire, real-time UI,
  reactive forms — interactive server-driven UI without writing JavaScript in Sage themes
user-invocable: false
---

# Livewire in WordPress via Acorn

## When to Use Livewire

| Approach | Best for |
|---|---|
| **Livewire** | Interactive server-driven UI, forms with validation, real-time filtering, pagination, file uploads |
| **Blade Component** | Static display, no interactivity |
| **Alpine.js** | Client-only UI (dropdowns, modals, tabs) — no server needed |
| **REST API + JS** | High-frequency updates (> 1/sec), large datasets, offline support |
| **ACF Block** | Editor-managed Gutenberg content |

## Prerequisites

- Sage + Acorn installed
- `roots/acorn-livewire` and `livewire/livewire` installed

```bash
lando theme-composer require roots/acorn-livewire livewire/livewire
lando acorn vendor:publish --tag=livewire:config
```

Add to `resources/views/layouts/app.blade.php`:

```blade
<head>
    @livewireStyles
    ...
</head>
<body>
    ...
    @livewireScripts
</body>
```

## Quick Start

```bash
# Check installed versions
bash skills/acorn-livewire/scripts/check-versions.sh

# Create a component (validates PascalCase, checks lando availability)
bash skills/acorn-livewire/scripts/create-component.sh ContactForm
# → app/Livewire/ContactForm.php
# → resources/views/livewire/contact-form.blade.php
```

Use the component in any Blade template:

```blade
<livewire:contact-form />
<livewire:contact-form :post-type="$postType" />
```

## Component Anatomy

```php
class PostSearch extends Component
{
    public string $query = '';

    public function mount(string $postType = 'post'): void
    {
        // wp_set_current_user(get_current_user_id()); // if WP user context needed
        $this->postType = $postType;
    }

    #[Computed]
    public function posts(): array
    {
        return get_posts(['s' => $this->query, 'posts_per_page' => 10]);
    }

    public function render(): \Illuminate\View\View
    {
        return view('livewire.post-search');
    }
}
```

```blade
{{-- resources/views/livewire/post-search.blade.php --}}
<div>  {{-- single root element required --}}
    <input wire:model.live.debounce.300ms="query" placeholder="Search..." />

    @forelse ($this->posts as $post)
        <a href="{{ get_permalink($post) }}">{{ $post->post_title }}</a>
    @empty
        <p>No results.</p>
    @endforelse
</div>
```

## wire:model Variants

| Directive | When to use |
|---|---|
| `wire:model="name"` | Default — syncs on form submit (no extra requests) |
| `wire:model.live="name"` | Real-time — sends request on every keystroke |
| `wire:model.blur="name"` | Field-level validation on focus loss |
| `wire:model.live.debounce.300ms="name"` | Real-time search (debounced) |

## Scripts

```bash
# Create a Livewire component (PascalCase name required)
bash skills/acorn-livewire/scripts/create-component.sh <ComponentName>

# Check package versions (Livewire, Acorn, PHP)
bash skills/acorn-livewire/scripts/check-versions.sh
```

Scripts: [`scripts/create-component.sh`](scripts/create-component.sh) · [`scripts/check-versions.sh`](scripts/check-versions.sh)

## Assets

Boilerplate templates with `{{PLACEHOLDER}}` tokens. Copy and replace placeholders.

- **[component.php.tpl](assets/component.php.tpl)** — Standard component class: `extends Component`, `WithPagination` commented out, `mount()` stub, `wp_set_current_user` stub, `render()`.
- **[view.blade.php.tpl](assets/view.blade.php.tpl)** — Livewire Blade view: single `<div>` root, `wire:loading` spinner, `wire:model` input example, Tailwind v4 note.

## References

Deep content loaded on demand — zero tokens until needed.

- **[sage-integration.md](references/sage-integration.md)** — Acorn boot, `@livewireStyles`/`@livewireScripts`, layout setup, Blade tag syntax, View Composer data passing, `sage-html-forms` comparison.
- **[state-patterns.md](references/state-patterns.md)** — `wire:model` variants, `#[Computed]` properties, lifecycle hooks (`mount`, `hydrate`, `updated`), loading states, Form objects (v3), component events.
- **[alpine-interop.md](references/alpine-interop.md)** — `$wire.entangle`, combining Alpine + Livewire, `$wire.propertyName`, Tailwind v4 coordination, dynamic class names, skeleton loaders.
- **[file-uploads.md](references/file-uploads.md)** — `WithFileUploads` trait, `media_handle_sideload()`, Lando storage paths, S3 driver, temporary file cleanup, validation rules.
- **[common-errors.md](references/common-errors.md)** — "Unable to find component", hydration errors, 419 CSRF, Alpine conflicts, missing root `<div>`, 404 on Livewire endpoint, `wire:model` not syncing.

## Verification

- Render the component in a Blade template and confirm it appears with the correct initial state.
- Interact with `wire:click`, `wire:submit`, or `wire:model` bindings and confirm the component updates reactively without a full page reload.
- Open browser DevTools Network tab and verify Livewire AJAX requests return 200 with the expected payload.

## Failure modes

### Problem: Component not found / blank render

- **Cause:** Blade tag does not match the class name, or the class is in the wrong namespace.
- **Fix:** Verify the class is in `app/Livewire/` with namespace `App\Livewire`. Tag convention: `ContactForm` → `<livewire:contact-form />`. Always generate with `lando acorn make:livewire`.

### Problem: Hydration errors

- **Cause:** A public property holds a non-serializable value (`WP_Post`, closures, resource handles).
- **Fix:** Store only scalar values. Use `#[Computed]` for derived data. See `references/common-errors.md`.

For all other failure modes (419 CSRF, Alpine conflicts, 404 on Livewire endpoint) see [`references/common-errors.md`](references/common-errors.md).

## Critical Rules

1. **Always wrap component views in a single root `<div>`.** Livewire requires exactly one root element per component view — multiple roots or naked text break hydration.
2. **Use `lando acorn make:livewire` — never create component files manually.** The generator sets correct namespaces, file paths, and naming conventions.
3. **`wire:model.live` for real-time; `wire:model` for form submit.** Each `.live` event is an HTTP request. Default to `wire:model` and use `.live` only when the UX genuinely requires instant server feedback.
4. **`wp_set_current_user` for user context.** If the component calls `current_user_can()` or any WP function that relies on the current user, call `wp_set_current_user(get_current_user_id())` in `mount()`.
5. **Never store large collections in public properties.** Livewire serializes all public properties on every request. Use `#[Computed]` for post lists and other derived data.
6. **Do not load Alpine separately.** Livewire bundles Alpine. A second Alpine instance causes conflicts. See `references/alpine-interop.md`.
7. **`@livewireStyles` in `<head>`, `@livewireScripts` before `</body>`.** Both are required. Missing either causes Livewire to silently fail.

## Query First — MCP Integration

Before creating or referencing a Livewire component, query the live environment:

```
discover-abilities
execute-ability livewire/components
```

Use real class names from the query. Do not invent component names.
If the stack is not installed, run `/ai-setup` first.
See [`sageing/references/mcp-query-patterns.md`](../sageing/references/mcp-query-patterns.md) for the full pattern.
