---
name: web-components
description: "Native Web Components, Custom Elements, Shadow DOM encapsulation, and framework-agnostic UI libraries."
---

# Native Web Components Protocol

Author framework-agnostic, zero-dependency browser components.

---

## 1. Custom Elements & Lifecycle

1. Extend `HTMLElement` and register with `customElements.define('app-widget', AppWidget)`.
2. Implement `connectedCallback` for DOM insertion and `disconnectedCallback` for cleanup.
3. Observe attributes with `static get observedAttributes()` and `attributeChangedCallback`.

---

## 2. Shadow DOM Encapsulation

Use `this.attachShadow({ mode: 'open' })` to isolate styles and DOM trees from global namespace collision.
