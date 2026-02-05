---
name: javascript
description: Use when writing JavaScript for Discourse core, themes, or plugins - covers jQuery phaseout, Ember patterns, singleton imports, lifecycle hooks, and cleanup requirements
---

# Discourse JavaScript Patterns

## Overview

Required patterns for JavaScript in Discourse (Ember-based application). These patterns are **prescriptive** - don't follow every pattern you see in existing code. Follow these rules instead.

## Critical: Don't Follow All Existing Patterns

**Just because code exists in the codebase doesn't mean you should copy it.**

Discourse is actively modernizing JavaScript. Old patterns remain while being phased out. When you see conflicting patterns, follow this skill's guidance.

## Never Use jQuery

**Rule:** Never use jQuery in new code. Use native DOM methods instead.

**Why:** Browsers now support jQuery's functionality natively. jQuery is being phased out.

| jQuery                | Native Equivalent                     |
| --------------------- | ------------------------------------- |
| `$('.selector')`      | `document.querySelector('.selector')` |
| `$('.class')`         | `document.querySelectorAll('.class')` |
| `.addClass('foo')`    | `.classList.add('foo')`               |
| `.removeClass('foo')` | `.classList.remove('foo')`            |
| `.on('click', fn)`    | `.addEventListener('click', fn)`      |
| `.fadeIn()`           | CSS transitions + `.classList`        |

**Example - Button click handler:**

```javascript
// ❌ NEVER - jQuery
$(".submit-btn").on("click", function () {
  $(".success").fadeIn();
});

// ✅ ALWAYS - Native DOM
const btn = document.querySelector(".submit-btn");
btn.addEventListener("click", () => {
  document.querySelector(".success").classList.add("visible");
});
```

## Never Import Singletons

**Rule:** Use dependency injection, not singleton imports.

**Why:** Singletons bypass Ember's container and make testing difficult.

```javascript
// ❌ NEVER - Singleton import
import Site from "discourse/models/site";
console.log(Site.currentProp("top_menu_items"));

// ✅ ALWAYS - Dependency injection
// In components, routes, controllers - site is auto-injected:
console.log(this.site.top_menu_items);

// In initializers:
let site = container.lookup("site:main");
console.log(site.top_menu_items);
```

**The site model is automatically injected** into components, routes, and controllers. Just use `this.site`.

**For services, use @service decorator:**

```javascript
import { service } from "@ember/service";

export default class extends Component {
  @service router;
  @service currentUser;
  @service store;

  navigateToProfile() {
    this.router.transitionTo("user", this.currentUser.username);
  }
}
```

**Common services:** `router`, `store`, `currentUser`, `site`, `siteSettings`, `session`, `dialog`, `modal`.

## Never Use self = this

**Rule:** Use arrow functions, not `self = this`.

**Why:** Arrow functions preserve context automatically and are widely supported.

```javascript
// ❌ NEVER - self = this pattern
let self = this;
setTimeout(function () {
  self.doSomething();
}, 1000);

// ✅ ALWAYS - Arrow function
setTimeout(() => {
  this.doSomething();
}, 1000);
```

**When you can't use arrow functions** (passing to library expecting function object):

```javascript
import { bind } from "discourse-common/utils/decorators";

@bind
myMethod() {
  console.log(this.property);
}

// Pass bound method reference
library.setup({ callback: this.myMethod });
```

## Lifecycle Hooks: Use Explicit Methods

**Rule:** Write explicit lifecycle methods. Never use `@on` decorators.

**Why:** Glimmer doesn't support `@on`. Explicit methods make execution order obvious.

```javascript
// ❌ NEVER - @on decorator
@on("init")
setupComponent() {
  this.set("data", []);
}

@on("init")
setupOther() {
  this.loadData();
}

// ✅ ALWAYS - Explicit lifecycle method
init() {
  this._super(...arguments);
  this.data = [];
  this.loadData();
}
```

**Execution order is clear** with explicit methods. Multiple `@on("init")` methods have unclear execution order.

## Always Clean Up

**Rule:** Remove listeners and cancel timers in willDestroyElement.

**Why:** Prevents memory leaks and zombie listeners.

```javascript
export default Component.extend({
  didInsertElement() {
    this._super(...arguments);
    this.clickHandler = () => this.handleClick();
    document.addEventListener("click", this.clickHandler);

    this.timerId = setTimeout(() => {
      this.doSomething();
    }, 5000);
  },

  willDestroyElement() {
    this._super(...arguments);
    // Clean up listener
    document.removeEventListener("click", this.clickHandler);

    // Cancel timer
    clearTimeout(this.timerId);
  },
});
```

**Always store references** to listeners and timer IDs so you can clean them up.

## Never Use Default Objects or Arrays

**Rule:** Initialize objects and arrays in `init()`, not as default values.

**Why:** Default objects/arrays are shared across all instances (shared reference).

```javascript
// ❌ NEVER - Default objects/arrays
export default EmberObject.extend({
  items: [],      // SHARED REFERENCE
  config: {}      // SHARED REFERENCE
});

// ✅ ALWAYS - Initialize in init() (EmberObject)
export default EmberObject.extend({
  items: null,
  config: null,

  init() {
    this._super(...arguments);
    this.items = [];
    this.config = {};
  }
});

// ✅ OR - Use native classes (no issue)
export default class {
  items = [];   // Each instance gets own array
  config = {};  // Each instance gets own object
}
```

## Private Fields: Use # Syntax

**Rule:** Make fields truly private with `#` unless decorator needed or used in template.

```javascript
export default class extends Component {
  // Public - used in template
  @tracked count = 0;

  // Public - decorator doesn't work on private
  @action
  increment() {
    this.#updateCount();
  }

  // Private - not used in template
  #internalState = null;

  #updateCount() {
    this.count++;
  }
}
```

**Don't use underscore prefix** (`_field`) - that's the old way. Use `#` for true privacy.

## Avoid Array Prototype Extensions

**Rule:** Use native Array methods, not Ember's prototype extensions.

**Why:** Ember's prototype extensions are deprecated.

```javascript
const items = [{ name: "foo" }, { name: "bar" }];

// ❌ NEVER - Ember prototype extension
items.findBy("name", "foo");

// ✅ ALWAYS - Native method
items.find((item) => item.name === "foo");
```

For arrays that need reactivity, use `TrackedArray` instead of native array.

## Avoid Observers

**Rule:** Use action handlers for user events. Use native getters for derived data.

**Why:** From Ember docs: "Observers are often over-used by new Ember developers. Most of the time, you will be observing an action the user took, such as clicking a button. Instead of an observer, consider putting that code in the action handler itself."

```javascript
// ❌ NEVER - Observer
@observes('userInput')
inputChanged() {
  this.processInput();
}

// ✅ ALWAYS - Action handler for user events
<input {{on "input" this.processInput}} />
```

**When you need derived data** (not side effects), use native getters:

```javascript
// ✅ Native getter for computed values
get fullName() {
  return `${this.firstName} ${this.lastName}`;
}
```

**Don't use getters for side effects** - use action handlers instead.

## Common Mistakes

| Mistake                                  | Fix                                                               |
| ---------------------------------------- | ----------------------------------------------------------------- |
| Using jQuery because it exists           | Use native DOM methods - jQuery is being phased out               |
| Importing singletons "just to check"     | Use dependency injection - `this.site`, `this.siteSettings`, etc. |
| "self = this for backward compatibility" | Arrow functions are widely supported - use them                   |
| Following @on pattern from old code      | Use explicit lifecycle methods - better for Glimmer               |
| Skipping cleanup "it's just a demo"      | Always clean up - prevents real bugs in production                |
| underscore prefix for "private"          | Use # for true private fields                                     |

## Rationalization Red Flags

These thoughts mean STOP - check this skill:

| Rationalization                        | Reality                                                        |
| -------------------------------------- | -------------------------------------------------------------- |
| "jQuery is already in the codebase"    | Being present ≠ permission to use. Use native methods.         |
| "Need backward compatibility"          | Arrow functions are ES6 (2015). Widely supported. Use them.    |
| "Matching codebase style I saw"        | Not all existing patterns should be copied. Follow this skill. |
| "Standard pattern in older JavaScript" | Modern alternatives exist. Don't use old patterns.             |
| "This code works fine"                 | Working ≠ best practice. Follow current patterns.              |
| "It's technically correct"             | Technically correct but wrong approach. Check alternatives.    |

**All of these mean: Review this skill and use current patterns.**
