---
name: jx
description: Use this skill for anything Jx — the Python/Jinja2 component library. Covers BOTH (a) library mechanics and integration AND (b) authoring production-ready UI components. Trigger this skill on any mention of Jx, `.jx` files, "Jinja components" in a Python web app context, or requests to build/create UI components for such an app.
---

# Jx — Jinja2 component library

Jx is a Python package that lets you build server-rendered UIs from reusable component files (`.jx`). A `Catalog` loads components from one or more folders and renders them with explicit imports, typed props, an `attrs` pass-through, and a per-component CSS/JS asset system.

## Mental model

```
Catalog("components/")  ──►  loads .jx files
       │
       ├── catalog.render("page.jx", **kwargs)  ──►  HTML string
       │       └── walks the imported component tree
       │           └── collects assets (CSS/JS) automatically
       │
       └── catalog.add_folder(path, prefix="ui")  ──►  more component sources
```

A component file has up to four parts (all optional except the template):

```html+jinja
{#import "./icon.jx" as Icon #}     {# imports — PascalCase aliases #}
{#css card.css #}                    {# per-component assets #}
{#js card.js #}
{#def title, subtitle="" #}          {# typed props with defaults #}

<div {{ attrs.render(class="card") }}>
  <Icon name="star" />
  <h3>{{ title }}</h3>
  {{ content }}                      {# main slot #}
</div>
```

## Quick reference

**Install**: `uv add jx` (or `pip install jx`).

**Create a catalog**:

```python
from jx import Catalog
catalog = Catalog("components/", auto_reload=app.debug)
html = catalog.render("page.jx", user=user, title="Home")
```

**Component file**:

- `{#def name, count=0, items: list = [] #}` — required props have no default; types are runtime-checked for primitives.
- `{#import "path.jx" as Name #}` — alias must be PascalCase. Three flavors: absolute (`"button.jx"`), relative (`"./sibling.jx"`), prefixed (`"@ui/button.jx"`).
- `{#css ... #}` / `{#js ... #}` — comma-separated list of files (relative URLs, absolute paths, or full URLs).

**Using a component**: HTML-tag syntax, PascalCase, props with `key="literal"` or `key={{ expr }}`. Booleans support shorthand: `<Input required />` is `required={{ true }}`.

**`attrs`** collects every attribute *not* declared in `{#def}`. Render onto the root element with `{{ attrs.render(class="default") }}` — `class` merges, other attrs override.

**Slots** for multiple content areas:

```html+jinja
{% slot header %}default{% endslot %}   {# in component #}
{% fill header %}custom{% endfill %}    {# at call site #}
```

**Assets** are collected from the whole tree, deduplicated, in import order. Render with `{{ assets.render() }}` or split via `assets.render_css()` / `assets.render_js(module=True, defer=True)`.

**Validate**: `jx check myapp.setup:catalog` (or `path/to/file.py:catalog`). Catches missing imports, used-but-not-imported tags, typos with "did you mean".

## When to load which reference

The compact summary above is enough for many tasks. Pull a reference file when the user's question is squarely in that area — don't preload them.

| If the user is asking about… | Read |
|---|---|
| **Building a UI component** (button, card, modal, dropdown, form, table, layout, navigation, accordion, toast, etc.) — design choices, accessibility, native-HTML-first, color mode, when to use JS, the authoring checklist | `reference/authoring.md` (always pair with `reference/patterns.md` if the user asks for a specific category we already have a recipe for) |
| **Copy-paste recipes** for buttons, modals (`<dialog>`), dropdowns (Popover API), form inputs, data tables, sidebar layouts | `reference/patterns.md` |
| Catalog options (`jinja_env`, `extensions`, `filters`, `globals`, `asset_resolver`), `add_folder` prefixes, `render` vs `render_string`, introspection (`get_signature`, `list_components`), `collect_assets` | `reference/catalog.md` |
| Component anatomy in depth, prop types and defaults, slot vs `content` vs prop tradeoffs, naming conventions, the dash-to-underscore rule | `reference/components.md` |
| `attrs.render` / `set` / `setdefault` / `add_class` / `prepend_class` / `remove_class`, class merging rules, forwarding `attrs` to a child component, conditional attributes | `reference/attrs.md` |
| Declaring CSS/JS, asset URL strategies (relative, absolute, build-tool), collection order, deduplication, `asset_resolver` for installable packages | `reference/assets.md` |
| Wiring Jx into Flask / Django / FastAPI / htmx, sharing a Jinja env, passing `request`, CSRF, URL helpers, partial responses for htmx | `reference/frameworks.md` |
| Running `jx check`, JSON output, programmatic `check_all`, the VSCode extension (Go-to-Definition, diagnostics, snippets) | `reference/tools.md` |

## Idioms worth remembering

- **Component classes first.** When you call `attrs.render(class="Card")`, the component's own classes are emitted *before* anything the caller passed. Callers extend; they don't replace.
- **`attrs` is for HTML elements, not component tags.** `<Button attrs={{ attrs }} />` is the way to forward a parent's attrs into a child component — `<Button {{ attrs.render() }} />` does NOT work because component tags are preprocessed.
- **Underscores in attribute names become dashes** at render time: `data_user_id` → `data-user-id`, `aria_label` → `aria-label`, `hx_get` → `hx-get`. Useful for `data-*`, `aria-*`, htmx, Alpine, etc.
- **Boolean attrs**: `True` renders the attribute name alone (`disabled`); `False` removes it entirely.
- **Auto-reload off in production.** `Catalog(auto_reload=False)` skips the file-mtime check on every render.
- **`_get_random_id(prefix)`** is a built-in global — useful for components that need stable-but-unique IDs (popovers, label-for, etc.) without forcing the caller to pass one.
- **Components are fragments.** Don't emit `<!DOCTYPE>` / `<html>` / `<body>` from a leaf component — that belongs to a single `layout.jx`.
