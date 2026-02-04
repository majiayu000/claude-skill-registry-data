---
name: vanilla-rails-hotwire
description: Use when writing Hotwire (Turbo/Stimulus) code in Rails - enforces dom_id helpers, morph updates, focused Stimulus controllers, and JavaScript private methods
---

# Vanilla Rails Hotwire

37signals conventions for Hotwire beyond the official documentation.

## Turbo Streams

### ALWAYS Use dom_id Helper (NEVER String Interpolation)

**WRONG:**
```erb
<%= turbo_stream.replace "card_#{@card.id}" do %>
```

**RIGHT:**
```erb
<%# Both syntaxes acceptable %>
<%= turbo_stream.replace dom_id(@card) do %>
<%= turbo_stream.replace [ @card ] do %>
```

### Use Prefixes for Targetable Sections

Prefixed dom_id enables granular updates to specific parts:

```ruby
dom_id(@card)                    # "card_abc123"
dom_id(@card, :header)           # "header_card_abc123"
dom_id(@card, :comments)         # "comments_card_abc123"
dom_id(@card, :status_badge)     # "status_badge_card_abc123"

# Array syntax (Rails shorthand)
[ @card, :header ]               # Same as dom_id(@card, :header)
```

**Example:**
```erb
<%= turbo_stream.replace dom_id(@card, :status_badge), method: :morph do %>
  <%= render "cards/status_badge", card: @card %>
<% end %>
```

### ALWAYS Use method: :morph for Updates

Morph avoids layout shift and preserves scroll position.

**WRONG:**
```erb
<%= turbo_stream.replace dom_id(@card) do %>
  <%= render @card %>
<% end %>
```

**RIGHT:**
```erb
<%= turbo_stream.replace dom_id(@card), method: :morph do %>
  <%= render @card %>
<% end %>
```

**When to use morph:**
- Updating existing content (cards, comments, headers)
- Replacing sections that users might be reading
- Any update where layout shift would be jarring

**When NOT to use morph:**
- Adding new items to lists (use `append`/`prepend`)
- Removing items (use `remove`)
- First-time rendering

## Stimulus Controllers

### Keep Controllers Small and Focused

**One purpose per controller.** Split large controllers.

**WRONG:**
```javascript
// card_controller.js - does too much
export default class extends Controller {
  connect() { }
  fadeIn() { }
  handleClick() { }
  validateForm() { }
  submitForm() { }
  showNotification() { }
}
```

**RIGHT:**
```javascript
// status_animation_controller.js - focused
export default class extends Controller {
  connect() {
    this.#fadeIn()
  }

  #fadeIn() {
    // Use CSS transitions, minimal JS
    this.element.classList.add('fade-in')
  }
}
```

### ALWAYS Mark Private Methods and Fields with # Prefix

Use JavaScript private fields syntax for methods/fields not called from HTML.

**WRONG:**
```javascript
export default class extends Controller {
  debounceTimer = null  // Public field (shouldn't be)

  copy() {
    navigator.clipboard.writeText(this.sourceTarget.value)
    this.showNotification()  // Public method (shouldn't be)
  }

  showNotification() {
    this.element.classList.add('success')
  }
}
```

**RIGHT:**
```javascript
export default class extends Controller {
  #debounceTimer = null  // Private field

  copy() {
    navigator.clipboard.writeText(this.sourceTarget.value)
    this.#showNotification()
  }

  #showNotification() {
    this.element.classList.add('success')
  }
}
```

### Decision Tree: Public vs Private

Ask yourself: **"Is this method called from HTML via data-action?"**

- **YES** → Keep it public (no #)
- **NO** → Make it private (#)

**Public methods:** Only those in `data-action="controller#method"` OR Stimulus lifecycle methods

**Private methods:** Everything else - helpers, callbacks, utilities

**Example:**
```html
<!-- This means mouseEnter and mouseLeave are public -->
<div data-controller="preview"
     data-action="mouseenter->preview#mouseEnter mouseleave->preview#mouseLeave">
```

```javascript
export default class extends Controller {
  // Public - called from data-action
  mouseEnter() { this.#show() }
  mouseLeave() { this.#hide() }

  // Public - Stimulus lifecycle (framework calls these)
  connect() { this.#initialize() }
  disconnect() { this.#cleanup() }

  // Private - only called internally
  #initialize() { }
  #cleanup() { }
  #show() { }
  #hide() { }
  #fetch() { }
}
```

**Stimulus lifecycle methods** (always public, no #):
- `connect()`, `disconnect()`
- `[name]TargetConnected()`, `[name]TargetDisconnected()`
- `[name]ValueChanged()`

### Red Flags - Methods That Should Be Private

If you write any of these without `#`, STOP:

- Helper methods: `show`, `hide`, `toggle`, `clear`, `reset`, `update`
- Fetch/API methods: `fetch`, `load`, `save`, `submit`
- Callback methods called only from `connect()` or other methods
- Any method not referenced in HTML `data-action`

**Check:** Search your HTML for `data-action`. If the method isn't there, add `#`.

### NO Business Logic in Stimulus

Controllers coordinate UI behavior only. No data transformations, validations, or domain logic.

**WRONG:**
```javascript
export default class extends Controller {
  submit() {
    // Don't validate/transform data in JS
    if (this.priceValue < 0) {
      this.priceValue = 0
    }
    this.element.submit()
  }
}
```

**RIGHT:**
```javascript
export default class extends Controller {
  submit() {
    // Just coordinate the UI
    this.element.submit()
  }
}
```

Let Rails controllers and models handle business logic.

## View Organization

### Container Pattern for Granular Updates

Structure partials with prefixed dom_id for targetable sections:

```erb
<%# app/views/cards/_card.html.erb %>
<article id="<%= dom_id(card) %>" class="card">
  <div id="<%= dom_id(card, :status) %>">
    <%= render "cards/status", card: card %>
  </div>

  <div id="<%= dom_id(card, :header) %>">
    <%= render "cards/header", card: card %>
  </div>

  <div id="<%= dom_id(card, :comments) %>">
    <%= render "cards/comments", card: card %>
  </div>
</article>
```

This enables targeted updates:

```erb
<%# app/views/cards/closures/create.turbo_stream.erb %>
<%= turbo_stream.replace dom_id(@card, :status), method: :morph do %>
  <%= render "cards/status", card: @card %>
<% end %>
```

## Common Violations

| Violation | Fix |
|-----------|-----|
| `"card_#{@card.id}"` | `dom_id(@card)` or `[ @card ]` |
| `turbo_stream.replace dom_id(@card)` | `turbo_stream.replace dom_id(@card), method: :morph` |
| `fadeIn() { }` | `#fadeIn() { }` |
| `debounceTimer = null` | `#debounceTimer = null` |
| Animation logic in Stimulus | Use CSS transitions, minimal JS |
| One controller doing many things | Split into focused controllers |
| Validations in Stimulus | Move to Rails models/controllers |
| Helper methods without # | Add # to all helpers not in data-action |

## Quick Reference

**Turbo Stream with morph:**
```erb
<%= turbo_stream.replace dom_id(@record, :section), method: :morph do %>
  <%= render "partial", record: @record %>
<% end %>
```

**Stimulus with private methods and fields:**
```javascript
export default class extends Controller {
  #privateField = null

  publicAction() {
    this.#privateHelper()
  }

  #privateHelper() {
    // Implementation
  }
}
```

**View containers:**
```erb
<div id="<%= dom_id(record, :prefix) %>">
  <%= render "partial", record: record %>
</div>
```
