---
name: stimulus
description: Best practices for using Stimulus controllers to add JavaScript behavior to HTML
---

# Stimulus Best Practices for Rails Applications

Rule updated on 12/15/2025 to Stimulus version 3.2.2

Stimulus is a modest JavaScript framework designed to augment your HTML with just enough behavior. It connects JavaScript to the DOM via data attributes, keeping your HTML as the source of truth.

For full reference see [https://stimulus.hotwired.dev/](https://stimulus.hotwired.dev/)

## Core Concepts

| Concept    | Purpose                                  | Data Attribute                     |
| ---------- | ---------------------------------------- | ---------------------------------- |
| Controller | JavaScript class that adds behavior      | `data-controller="name"`           |
| Target     | Important elements referenced in JS      | `data-name-target="targetName"`    |
| Action     | Event handlers connecting DOM to methods | `data-action="event->name#method"` |
| Value      | Reactive data stored in HTML             | `data-name-value-name="value"`     |
| Class      | CSS classes toggled by the controller    | `data-name-class-name="class"`     |
| Outlet     | References to other controllers          | `data-name-outlet-name="selector"` |

---

## When to Use Stimulus

**Use Stimulus for:**

- Toggle visibility (dropdowns, modals, accordions)
- Form enhancements (character counters, auto-submit, validation UI)
- Copy to clipboard
- Keyboard shortcuts
- Animations and transitions
- Client-side filtering/sorting (small datasets)
- Debounced input handlers
- Any behavior that doesn't require server data

**Don't use Stimulus for:**

- Data that should come from the server (use Turbo Streams instead)
- Complex state management (consider if your approach is right)
- Things Turbo already handles (form submission, navigation)

---

## Controller Structure

### File Naming & Location

Controllers that live in `app/javascript/controllers/` and follow the naming convention below are automatically registered.

| File Name                 | Controller Name       | HTML Reference                |
| ------------------------- | --------------------- | ----------------------------- |
| `hello_controller.js`     | `HelloController`     | `data-controller="hello"`     |
| `clipboard_controller.js` | `ClipboardController` | `data-controller="clipboard"` |
| `user_form_controller.js` | `UserFormController`  | `data-controller="user-form"` |

### Basic Controller Template

```javascript
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "output"]
  static values = { url: String, count: Number, active: Boolean }
  static classes = ["hidden", "active"]

  connect() {
    // Called when controller is connected to DOM
  }

  disconnect() {
    // Called when controller is removed from DOM
    // Clean up event listeners, timers, etc.
  }

  // Action methods
  toggle() {
    this.outputTarget.classList.toggle(this.hiddenClass)
  }
}
```

---

## Targets

Targets provide named references to important elements within the controller's scope.

### Defining Targets

```javascript
export default class extends Controller {
  static targets = ["input", "submit", "error"]

  validate() {
    if (this.inputTarget.value.length < 3) {
      this.errorTarget.textContent = "Too short"
      this.submitTarget.disabled = true
    }
  }
}
```

### HTML Usage

```erb
<div data-controller="form">
  <input data-form-target="input" data-action="input->form#validate">
  <span data-form-target="error"></span>
  <button data-form-target="submit">Submit</button>
</div>
```

### Target Properties

| Property              | Returns                           | Example           |
| --------------------- | --------------------------------- | ----------------- |
| `this.inputTarget`    | First matching element (or error) | Single element    |
| `this.inputTargets`   | Array of all matching elements    | `[el1, el2, el3]` |
| `this.hasInputTarget` | Boolean if target exists          | `true` / `false`  |

---

## Values

Values are reactive data attributes that automatically sync between HTML and JavaScript.

### Defining Values

```javascript
export default class extends Controller {
  static values = {
    url: String,
    count: Number,
    active: Boolean,
    config: Object,
    items: Array,
  }

  countValueChanged(value, previousValue) {
    // Called automatically when count value changes
    console.log(`Count changed from ${previousValue} to ${value}`)
  }
}
```

### HTML Usage

```erb
<div data-controller="counter"
     data-counter-count-value="0"
     data-counter-url-value="<%= api_path %>"
     data-counter-config-value="<%= { limit: 10 }.to_json %>">
</div>
```

### Value Benefits

- **Reactive**: Changes trigger `*ValueChanged` callbacks
- **Type coercion**: Automatic conversion to declared type
- **Default values**: `static values = { count: { type: Number, default: 0 } }`
- **HTML as source of truth**: State is visible in the DOM

---

## Actions

Actions connect DOM events to controller methods.

### Action Syntax

```
data-action="event->controller#method"
```

### Common Patterns

```erb
<!-- Click event (default for buttons) -->
<button data-action="dropdown#toggle">Menu</button>

<!-- Explicit event -->
<input data-action="input->search#filter">

<!-- Multiple actions -->
<input data-action="focus->form#highlight blur->form#unhighlight">

<!-- Keyboard events with filters -->
<input data-action="keydown.enter->form#submit keydown.escape->form#cancel">

<!-- Window/document events -->
<div data-controller="modal" data-action="keydown.escape@window->modal#close">

<!-- Form events -->
<form data-action="submit->form#validate">
```

### Event Modifiers

| Modifier   | Effect                            |
| ---------- | --------------------------------- |
| `:prevent` | Calls `event.preventDefault()`    |
| `:stop`    | Calls `event.stopPropagation()`   |
| `:self`    | Only fires if target is element   |
| `:once`    | Removes listener after first fire |

```erb
<a href="#" data-action="click->nav#toggle:prevent">Toggle</a>
```

---

## Classes

Classes let you reference CSS classes from your controller without hardcoding them.

### Defining Classes

```javascript
export default class extends Controller {
  static classes = ["active", "hidden", "loading"]

  toggle() {
    this.element.classList.toggle(this.activeClass)
  }

  load() {
    if (this.hasLoadingClass) {
      this.element.classList.add(this.loadingClass)
    }
  }
}
```

### HTML Usage

```erb
<div data-controller="toggle"
     data-toggle-active-class="bg-blue-500 text-white"
     data-toggle-hidden-class="hidden">
</div>
```

---

## Lifecycle Callbacks

```javascript
export default class extends Controller {
  initialize() {
    // Called once when controller is first instantiated
    // Use for one-time setup that doesn't depend on DOM
  }

  connect() {
    // Called each time controller connects to DOM
    // Set up event listeners, fetch data, start timers
  }

  disconnect() {
    // Called when controller disconnects from DOM
    // ALWAYS clean up: remove listeners, clear timers, abort fetches
  }
}
```

### Cleanup Example

```javascript
export default class extends Controller {
  connect() {
    this.interval = setInterval(() => this.refresh(), 5000)
    this.abortController = new AbortController()
  }

  disconnect() {
    clearInterval(this.interval)
    this.abortController.abort()
  }

  async refresh() {
    const response = await fetch(this.urlValue, {
      signal: this.abortController.signal,
    })
    // ...
  }
}
```

---

## Common Controller Patterns

### Toggle Controller

```javascript
// toggle_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["content"]
  static classes = ["hidden"]

  toggle() {
    this.contentTarget.classList.toggle(this.hiddenClass)
  }

  show() {
    this.contentTarget.classList.remove(this.hiddenClass)
  }

  hide() {
    this.contentTarget.classList.add(this.hiddenClass)
  }
}
```

### Clipboard Controller

```javascript
// clipboard_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["source"]
  static values = { successDuration: { type: Number, default: 2000 } }

  copy() {
    navigator.clipboard.writeText(this.sourceTarget.value)
    this.showCopiedState()
  }

  showCopiedState() {
    this.element.dataset.copied = true
    setTimeout(() => delete this.element.dataset.copied, this.successDurationValue)
  }
}
```

### Debounce Controller

```javascript
// search_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input", "form"]
  static values = { delay: { type: Number, default: 300 } }

  search() {
    clearTimeout(this.timeout)
    this.timeout = setTimeout(() => {
      this.formTarget.requestSubmit()
    }, this.delayValue)
  }

  disconnect() {
    clearTimeout(this.timeout)
  }
}
```

---

## Integration with Turbo

### Persisting Controllers Across Navigation

Turbo Drive preserves `<head>` but replaces `<body>`. Controllers on body elements disconnect and reconnect. Use values to persist state:

```erb
<!-- State survives Turbo navigation because it's in HTML -->
<div data-controller="sidebar" data-sidebar-open-value="true">
```

### Responding to Turbo Events

```javascript
export default class extends Controller {
  connect() {
    document.addEventListener("turbo:before-cache", this.cleanup)
  }

  disconnect() {
    document.removeEventListener("turbo:before-cache", this.cleanup)
  }

  cleanup = () => {
    // Reset state before Turbo caches the page
    this.element.classList.remove("is-active")
  }
}
```

### Working with Turbo Frames

```javascript
export default class extends Controller {
  connect() {
    this.element.addEventListener("turbo:frame-load", this.onFrameLoad)
  }

  onFrameLoad = (event) => {
    // React to frame content loading
    this.updateUI()
  }
}
```

---

## Best Practices Summary

1. **Keep controllers small** — One responsibility per controller (< 100 lines ideally)
2. **Use values for state** — Don't store state in instance variables; keep it in data attributes
3. **Always clean up** — Clear timers, abort fetches, remove listeners in `disconnect()`
4. **Prefer HTML over JS** — Use data attributes to configure behavior, not JavaScript
5. **Name actions clearly** — `toggle`, `submit`, `validate` not `handleClick`, `onClick`
6. **Use targets over querySelector** — More explicit and self-documenting
7. **Compose with multiple controllers** — Combine small controllers rather than building monoliths
8. **Let Turbo handle server communication** — Stimulus is for client-side behavior only

---

## Anti-Patterns to Avoid

| Don't                              | Do Instead                               |
| ---------------------------------- | ---------------------------------------- |
| Store state in instance variables  | Use values (`static values = {}`)        |
| Use `querySelector` in controllers | Use targets (`static targets = []`)      |
| Hardcode CSS classes               | Use classes (`static classes = []`)      |
| Forget to clean up in `disconnect` | Always clean up timers, listeners, etc.  |
| Make controllers too large         | Split into multiple focused controllers  |
| Use Stimulus for data fetching     | Use Turbo Frames/Streams for server data |
| Duplicate controller logic         | Extract shared behavior to base class    |
