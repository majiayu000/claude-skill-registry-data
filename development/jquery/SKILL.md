---
name: jquery
description: jQuery — legacy, server-rendered, WordPress, pre-framework codebases.
---

## Detection Signals

- `jquery` in `package.json` OR `<script src="...jquery...">` in HTML
- `$` or `jQuery` function calls in `.js` files
- `.ready()`, `$(document).on()`, `$(window)` patterns
- jQuery plugins: `.select2()`, `.dataTable()`, `.slick()`, `.datepicker()`
- `$.ajax()`, `$.get()`, `$.post()` calls

## MCP Setup

No official MCP server is available for jQuery.

> Reference the jQuery API at [api.jquery.com](https://api.jquery.com). A documentation search MCP (if configured) can retrieve specific API pages on demand.

## Context Rule

jQuery exists in this project for a reason — legacy, WordPress constraints, plugin ecosystem, or team familiarity. **Do not refactor jQuery to vanilla JS or a framework unless explicitly tasked.** Integrate with the existing pattern; flag modernization opportunities in code review notes only.

## Core Concepts

| Concept | Detail |
|---------|--------|
| **`$(selector)`** | Returns jQuery object wrapping matched elements; methods chain on it |
| **DOM ready** | `$(function() { ... })` — safe to access DOM after parsing |
| **Event delegation** | `.on('event', '.child', fn)` — works on dynamically added elements |
| **AJAX** | `$.ajax()`, `$.get()`, `$.post()` — callback or Promise (`.done()`, `.fail()`, `.always()`) |
| **Plugins** | Extend `$.fn` — called as `$('.el').pluginName(options)` |
| **Chaining** | Most methods return the jQuery object — enables `$el.hide().delay(200).fadeIn()` |

## Key Patterns

```js
// DOM ready
$(function () {
  // safe to access DOM here
})

// Event delegation — preferred; works on dynamic content
$(document).on('click', '.btn-submit', function () {
  const $form = $(this).closest('form')
  $form.find('.error').hide()
})

// Cache selectors — never re-query inside loops
const $modal = $('#confirmModal')
$modal.find('.modal-title').text('Are you sure?')
$modal.modal('show')

// AJAX with Promise style
$.get('/api/users')
  .done(function (data) { renderUsers(data) })
  .fail(function (xhr) { showError(xhr.responseJSON?.message) })

// Plugin initialization pattern
$('.select-field').select2({
  placeholder: 'Choose an option',
  allowClear: true,
})
```

## Coexistence with Modern Frameworks

When jQuery coexists with Vue, React, or Alpine:
- **Never let jQuery and the framework both manipulate the same DOM node** — one must own the element
- jQuery can manage areas outside the framework's root element (legacy sections, third-party widgets)
- Use custom events (`$.trigger()` / `$(document).on()`) to bridge jQuery and framework code if needed

## Critical Rules

- **Cache `$()` results** — `const $el = $('#id')` once; never re-query the same selector repeatedly, especially inside loops
- **Use `.on()`** not `.click()`, `.submit()`, `.hover()` — shorthand aliases are deprecated
- **Event delegation for dynamic content** — attach to a stable parent ancestor, not to elements that may not exist at bind time
- **`$(this)` in handlers** — cache as `const $self = $(this)` if used more than once in the same handler
- **Never use `$.get()` on unvalidated user-supplied URLs** — always whitelist or validate URLs before AJAX to prevent SSRF
- **Plugin options are cumulative** — calling `.select2()` twice initializes twice; always destroy before re-init if reconfiguring
