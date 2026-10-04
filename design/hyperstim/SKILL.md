---
name: hyperstim
description: Personal HyperStim guidelines. Use when working with HyperStim (data attribute-driven frontend framework).
---

When working with HyperStim (data attribute-driven frontend framework), fetch and read the README from https://github.com/myfavshrimp/hyperstim before making any changes.

HyperStim data attributes are evaluated as JavaScript **expressions**, not statements. Constructs like `if`, `for`, `while`, `return`, `let`, and `const` will error at evaluation time.

**Conditional logic — use expression forms:**

```html
data-effect="condition && doThing()"
data-effect="condition ? doThing() : doOtherThing()"
data-effect="!condition || doThing()"
```

**Multiple expressions — separate with commas:**

```html
data-init="this.x = 0, this.y = 0"
```

**Avoid statements (these will error):**

```html
data-effect="if (condition) doThing()"
data-on-click="for (let i of items) ..."
```

For anything more complex than what fits in an expression, define a helper method on the component (`data-init="this.handle = () => { ... }"`) and call it from the attribute (`data-on-click="this.handle()"`).

In HyperStim data attributes (`data-init`, `data-on-click`, `data-on-scroll`, `data-effect`, etc.), expressions must be separated by commas, not semicolons. HyperStim's expression parser uses comma as the statement separator.

**Yes:**

```html
data-init="this.x = 1, this.y = 2"
```

**No:**

```html
data-init="this.x = 1; this.y = 2"
```

When a single button triggers a server action and there are no form inputs to submit, do not wrap it in `<form data-hijack>`. Use `data-init` + `data-on-click` directly on the button:

```html
<button
    data-init="this.fetch = fetch('/endpoint', { method: 'POST' })"
    data-on-click="this.fetch.trigger()">
    Label
</button>
```

Reserve `<form data-hijack>` for cases that genuinely need form inputs (`<input>`, `<select>`, `<textarea>`) submitted as form data.

HyperStim fetch actions expose `.state()`, which returns `'pending'` during the request and `'success'` on completion. Use this directly — don't add custom boolean flags like `clicked`, `triggered`, `completed`.

**Example:** to close a dialog after a successful POST:

```html
<button
    data-init="this.fetch = fetch('/save', { method: 'POST' })"
    data-on-click="this.fetch.trigger()"
    data-effect="this.fetch.state() === 'success' && dialog.close()">
    Save
</button>
```

Not: setting a `this.didClick = true` flag and reading it elsewhere.
