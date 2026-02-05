---
name: state-management
description: Client-side state patterns for Web Components. Use when building interactive applications requiring state synchronization, reactive updates, or undo/redo functionality.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# State Management Skill

Client-side state management using vanilla JavaScript patterns that work seamlessly with Web Components.

## Philosophy

1. **State should be explicit** - Not hidden in DOM attributes or CSS classes
2. **Prefer composition** - Build from small, reusable patterns
3. **Changes trigger re-renders** - Don't directly manipulate DOM
4. **No frameworks required** - Use native browser APIs

---

## Simple Reactive Store

A minimal pub/sub store using native `EventTarget`:

```javascript
/**
 * Create a reactive store
 * @template T
 * @param {T} initialState
 * @returns {{getState: () => T, setState: (partial: Partial<T>) => void, subscribe: (fn: (state: T) => void) => () => void}}
 */
function createStore(initialState) {
  let state = { ...initialState };
  const target = new EventTarget();

  return {
    getState() {
      return state;
    },

    setState(partial) {
      state = { ...state, ...partial };
      target.dispatchEvent(new CustomEvent('change', { detail: state }));
    },

    subscribe(callback) {
      const handler = (e) => callback(e.detail);
      target.addEventListener('change', handler);
      // Return unsubscribe function
      return () => target.removeEventListener('change', handler);
    }
  };
}
```

### Usage

```javascript
// Create a store
const store = createStore({ count: 0, user: null });

// Subscribe to changes
const unsubscribe = store.subscribe((state) => {
  console.log('State changed:', state);
});

// Update state
store.setState({ count: 1 });
store.setState({ user: { name: 'Alice' } });

// Get current state
console.log(store.getState()); // { count: 1, user: { name: 'Alice' } }

// Clean up
unsubscribe();
```

---

## Signals-Like Pattern

A lightweight reactive primitive inspired by Solid.js signals:

```javascript
/**
 * Create a reactive signal
 * @template T
 * @param {T} initialValue
 * @returns {{value: T, subscribe: (fn: (value: T) => void) => () => void}}
 */
function createSignal(initialValue) {
  let value = initialValue;
  const subscribers = new Set();

  return {
    get value() {
      return value;
    },

    set value(newValue) {
      if (newValue !== value) {
        value = newValue;
        subscribers.forEach(fn => fn(value));
      }
    },

    subscribe(callback) {
      subscribers.add(callback);
      return () => subscribers.delete(callback);
    }
  };
}

/**
 * Create a computed signal (derived state)
 * @template T
 * @param {() => T} computeFn
 * @param {Array<{subscribe: Function}>} dependencies
 * @returns {{value: T, subscribe: (fn: (value: T) => void) => () => void}}
 */
function createComputed(computeFn, dependencies) {
  const signal = createSignal(computeFn());

  dependencies.forEach(dep => {
    dep.subscribe(() => {
      signal.value = computeFn();
    });
  });

  return signal;
}
```

### Usage

```javascript
const count = createSignal(0);
const doubled = createComputed(() => count.value * 2, [count]);

doubled.subscribe(val => console.log('Doubled:', val));

count.value = 5; // Logs: "Doubled: 10"
```

---

## Web Component State Integration

Pattern for managing state within Custom Elements:

```javascript
class CounterElement extends HTMLElement {
  /** @type {number} */
  #count = 0;

  connectedCallback() {
    this.render();
    this.addEventListener('click', this.#handleClick);
  }

  disconnectedCallback() {
    this.removeEventListener('click', this.#handleClick);
  }

  /**
   * Get current state
   * @returns {number}
   */
  get count() {
    return this.#count;
  }

  /**
   * Update state and re-render
   * @param {Partial<{count: number}>} updates
   */
  setState(updates) {
    if ('count' in updates) {
      this.#count = updates.count;
    }
    this.render();
    this.dispatchEvent(new CustomEvent('state-change', {
      detail: { count: this.#count },
      bubbles: true
    }));
  }

  #handleClick = () => {
    this.setState({ count: this.#count + 1 });
  };

  render() {
    this.innerHTML = `
      <button type="button">Count: ${this.#count}</button>
    `;
  }
}

customElements.define('counter-element', CounterElement);
```

### Attribute-to-State Synchronization

```javascript
class UserCard extends HTMLElement {
  static observedAttributes = ['user-id'];

  /** @type {{id: string, name: string} | null} */
  #user = null;

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === 'user-id' && oldValue !== newValue) {
      this.#loadUser(newValue);
    }
  }

  async #loadUser(id) {
    this.#user = await fetch(`/api/users/${id}`).then(r => r.json());
    this.render();
  }

  render() {
    if (!this.#user) {
      this.innerHTML = '<p>Loading...</p>';
      return;
    }
    this.innerHTML = `<p>${this.#user.name}</p>`;
  }
}
```

---

## Cross-Component Communication

### Parent-Child: Custom Events

```javascript
// Child dispatches event
class ChildComponent extends HTMLElement {
  #notifyParent(data) {
    this.dispatchEvent(new CustomEvent('item-selected', {
      detail: data,
      bubbles: true,
      composed: true // Cross shadow DOM boundaries
    }));
  }
}

// Parent listens
class ParentComponent extends HTMLElement {
  connectedCallback() {
    this.addEventListener('item-selected', this.#handleSelection);
  }

  #handleSelection = (event) => {
    console.log('Child selected:', event.detail);
  };
}
```

### Siblings: Shared Store

```javascript
// stores/app-store.js
export const appStore = createStore({
  selectedItem: null,
  items: []
});

// component-a.js
import { appStore } from './stores/app-store.js';

class ComponentA extends HTMLElement {
  #unsubscribe = null;

  connectedCallback() {
    this.#unsubscribe = appStore.subscribe(state => {
      this.render(state);
    });
  }

  disconnectedCallback() {
    this.#unsubscribe?.();
  }

  selectItem(item) {
    appStore.setState({ selectedItem: item });
  }
}
```

### Global Events (Window)

For truly global state changes:

```javascript
// Dispatch
window.dispatchEvent(new CustomEvent('app:theme-change', {
  detail: { theme: 'dark' }
}));

// Listen anywhere
window.addEventListener('app:theme-change', (e) => {
  document.documentElement.dataset.theme = e.detail.theme;
});
```

---

## Undo/Redo Stack

Command pattern for reversible operations:

```javascript
/**
 * @typedef {Object} Command
 * @property {() => void} execute
 * @property {() => void} undo
 */

/**
 * Create an undo/redo manager
 * @returns {{execute: (cmd: Command) => void, undo: () => void, redo: () => void, canUndo: () => boolean, canRedo: () => boolean}}
 */
function createUndoManager() {
  /** @type {Command[]} */
  const history = [];
  let cursor = -1;

  return {
    execute(command) {
      // Clear any redo history
      history.splice(cursor + 1);
      // Execute and add to history
      command.execute();
      history.push(command);
      cursor++;
    },

    undo() {
      if (cursor >= 0) {
        history[cursor].undo();
        cursor--;
      }
    },

    redo() {
      if (cursor < history.length - 1) {
        cursor++;
        history[cursor].execute();
      }
    },

    canUndo() {
      return cursor >= 0;
    },

    canRedo() {
      return cursor < history.length - 1;
    }
  };
}
```

### Usage with Text Editor

```javascript
const undoManager = createUndoManager();
let text = '';

function insertText(position, content) {
  undoManager.execute({
    execute() {
      text = text.slice(0, position) + content + text.slice(position);
    },
    undo() {
      text = text.slice(0, position) + text.slice(position + content.length);
    }
  });
}

insertText(0, 'Hello');  // text = 'Hello'
insertText(5, ' World'); // text = 'Hello World'
undoManager.undo();       // text = 'Hello'
undoManager.redo();       // text = 'Hello World'
```

---

## LocalStorage Persistence

Persist store state across sessions:

```javascript
/**
 * Create a persisted store
 * @template T
 * @param {string} key - localStorage key
 * @param {T} defaultState
 * @returns {ReturnType<typeof createStore<T>>}
 */
function createPersistedStore(key, defaultState) {
  // Hydrate from localStorage
  const stored = localStorage.getItem(key);
  const initialState = stored ? JSON.parse(stored) : defaultState;

  const store = createStore(initialState);

  // Persist on every change
  store.subscribe((state) => {
    localStorage.setItem(key, JSON.stringify(state));
  });

  return store;
}
```

### Usage

```javascript
const userPrefs = createPersistedStore('user-prefs', {
  theme: 'light',
  fontSize: 16,
  notifications: true
});

// State persists across page reloads
userPrefs.setState({ theme: 'dark' });
```

For more complex persistence, see the `data-storage` skill.

---

## When NOT to Use State Management

### Use CSS-Only Solutions

For UI state that's purely visual:

```css
/* Checkbox hack for toggles */
input[type="checkbox"]:checked + .panel {
  display: block;
}

/* :has() for conditional styling */
form:has(:invalid) button[type="submit"] {
  opacity: 0.5;
  pointer-events: none;
}
```

See the `progressive-enhancement` skill for more CSS-only patterns.

### Use URL State

For state that should be bookmarkable/shareable:

```javascript
// Read from URL
const params = new URLSearchParams(location.search);
const page = params.get('page') || '1';

// Update URL without reload
const newParams = new URLSearchParams(location.search);
newParams.set('page', '2');
history.pushState({}, '', `?${newParams}`);
```

### Just Re-Fetch

For server state that doesn't need client caching:

```javascript
// Don't cache - just fetch when needed
async function loadData() {
  return fetch('/api/data').then(r => r.json());
}
```

See the `api-client` skill for caching patterns when needed.

---

## State Management Checklist

When implementing state:

- [ ] State changes create new objects (immutable updates)
- [ ] Subscriptions are cleaned up in `disconnectedCallback`
- [ ] No mutable global state (except intentional singletons)
- [ ] State is JSON-serializable for persistence
- [ ] Events bubble for parent notification
- [ ] Consider URL state for shareable UI state
- [ ] Consider CSS-only solutions for visual state

## Related Skills

- **custom-elements** - Define and use custom HTML elements
- **data-storage** - Implement client-side data storage with localStorage, Ind...
- **api-client** - Fetch API patterns with error handling, retry logic, and ...
- **javascript-author** - Write vanilla JavaScript for Web Components with function...
