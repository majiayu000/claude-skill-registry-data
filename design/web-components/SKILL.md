---
name: web-components
description: Creates reusable custom HTML elements using Web Components standards including Custom Elements, Shadow DOM, templates, and slots. Use when building framework-agnostic components, creating design systems, or when user mentions web components, custom elements, or shadow DOM.
---

# Web Components

Native browser APIs for creating reusable, encapsulated custom HTML elements.

## Quick Start

```html
<!-- Use the component -->
<user-card name="Alice" role="Admin"></user-card>

<script>
class UserCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>
        .card { padding: 1rem; border: 1px solid #ddd; border-radius: 8px; }
        h2 { margin: 0 0 0.5rem; }
        .role { color: #666; font-size: 0.9rem; }
      </style>
      <div class="card">
        <h2>${this.getAttribute('name')}</h2>
        <span class="role">${this.getAttribute('role')}</span>
      </div>
    `;
  }
}

customElements.define('user-card', UserCard);
</script>
```

## Custom Elements

### Basic Definition

```javascript
class MyButton extends HTMLElement {
  // Called when element is created
  constructor() {
    super();
    // Initialize state, attach shadow DOM
  }

  // Called when element is added to DOM
  connectedCallback() {
    console.log('Element added to page');
    this.render();
  }

  // Called when element is removed from DOM
  disconnectedCallback() {
    console.log('Element removed from page');
    this.cleanup();
  }

  // Called when element is moved to new document
  adoptedCallback() {
    console.log('Element moved to new document');
  }

  // Called when observed attribute changes
  attributeChangedCallback(name, oldValue, newValue) {
    console.log(`Attribute ${name} changed from ${oldValue} to ${newValue}`);
    this.render();
  }

  // List of attributes to observe
  static get observedAttributes() {
    return ['variant', 'disabled', 'size'];
  }
}

customElements.define('my-button', MyButton);
```

### Extending Built-in Elements

```javascript
class FancyButton extends HTMLButtonElement {
  constructor() {
    super();
    this.addEventListener('click', this.handleClick);
  }

  handleClick() {
    this.classList.add('clicked');
  }
}

customElements.define('fancy-button', FancyButton, { extends: 'button' });

// Usage: <button is="fancy-button">Click me</button>
```

## Shadow DOM

### Open vs Closed Mode

```javascript
class OpenComponent extends HTMLElement {
  constructor() {
    super();
    // Accessible via element.shadowRoot
    this.attachShadow({ mode: 'open' });
  }
}

class ClosedComponent extends HTMLElement {
  #shadow;

  constructor() {
    super();
    // Not accessible from outside
    this.#shadow = this.attachShadow({ mode: 'closed' });
  }
}
```

### Style Encapsulation

```javascript
class StyledComponent extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    this.shadowRoot.innerHTML = `
      <style>
        /* Styles only apply inside shadow DOM */
        :host {
          display: block;
          padding: 1rem;
          border: 1px solid #ccc;
        }

        /* Style based on host attributes */
        :host([variant="primary"]) {
          background: #007bff;
          color: white;
        }

        :host([disabled]) {
          opacity: 0.5;
          pointer-events: none;
        }

        /* Style when host matches selector */
        :host-context(.dark-theme) {
          background: #333;
          color: white;
        }

        /* Internal elements */
        .title {
          font-size: 1.5rem;
          font-weight: bold;
        }

        /* Style slotted content */
        ::slotted(p) {
          margin: 0.5rem 0;
        }

        ::slotted(*) {
          color: inherit;
        }
      </style>

      <div class="title"><slot name="title"></slot></div>
      <div class="content"><slot></slot></div>
    `;
  }
}
```

### CSS Parts for External Styling

```javascript
class PartComponent extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    this.shadowRoot.innerHTML = `
      <style>
        .header { padding: 1rem; }
        .body { padding: 1rem; }
      </style>

      <div class="header" part="header">
        <slot name="header"></slot>
      </div>
      <div class="body" part="body">
        <slot></slot>
      </div>
    `;
  }
}

customElements.define('part-component', PartComponent);
```

```css
/* External CSS can style parts */
part-component::part(header) {
  background: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

part-component::part(body) {
  background: white;
}
```

### CSS Custom Properties (Theming)

```javascript
class ThemableComponent extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          /* Defaults with fallbacks */
          --button-bg: var(--theme-primary, #007bff);
          --button-color: var(--theme-text, white);
          --button-radius: var(--theme-radius, 4px);
        }

        button {
          background: var(--button-bg);
          color: var(--button-color);
          border-radius: var(--button-radius);
          border: none;
          padding: 0.5rem 1rem;
          cursor: pointer;
        }
      </style>

      <button><slot></slot></button>
    `;
  }
}
```

```css
/* Theme the component from outside */
:root {
  --theme-primary: #6366f1;
  --theme-text: white;
  --theme-radius: 8px;
}
```

## Templates and Slots

### HTML Template

```html
<template id="user-card-template">
  <style>
    .card {
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 1rem;
      border: 1px solid #e5e7eb;
      border-radius: 8px;
    }
    .avatar {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      object-fit: cover;
    }
    .info h3 {
      margin: 0;
      font-size: 1rem;
    }
    .info p {
      margin: 0.25rem 0 0;
      color: #6b7280;
      font-size: 0.875rem;
    }
  </style>

  <div class="card">
    <img class="avatar" src="" alt="">
    <div class="info">
      <h3><slot name="name">Unknown User</slot></h3>
      <p><slot name="email">No email</slot></p>
    </div>
    <div class="actions">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script>
class UserCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    const template = document.getElementById('user-card-template');
    this.shadowRoot.appendChild(template.content.cloneNode(true));
  }

  connectedCallback() {
    const img = this.shadowRoot.querySelector('.avatar');
    img.src = this.getAttribute('avatar') || '/default-avatar.png';
    img.alt = this.getAttribute('name') || 'User avatar';
  }
}

customElements.define('user-card', UserCard);
</script>

<!-- Usage -->
<user-card avatar="/alice.jpg">
  <span slot="name">Alice Johnson</span>
  <span slot="email">alice@example.com</span>
  <button slot="actions">Follow</button>
</user-card>
```

### Named Slots

```javascript
class TabPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    this.shadowRoot.innerHTML = `
      <style>
        .tabs {
          display: flex;
          border-bottom: 1px solid #ddd;
        }
        .panels {
          padding: 1rem;
        }
      </style>

      <div class="tabs">
        <slot name="tab"></slot>
      </div>
      <div class="panels">
        <slot name="panel"></slot>
      </div>
    `;
  }
}

// Usage:
// <tab-panel>
//   <button slot="tab">Tab 1</button>
//   <button slot="tab">Tab 2</button>
//   <div slot="panel">Content 1</div>
//   <div slot="panel">Content 2</div>
// </tab-panel>
```

### Slot Events

```javascript
class SlotContainer extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `<slot></slot>`;

    const slot = this.shadowRoot.querySelector('slot');
    slot.addEventListener('slotchange', (e) => {
      const assigned = slot.assignedElements();
      console.log('Slotted elements:', assigned);

      // React to content changes
      this.updateLayout(assigned);
    });
  }

  updateLayout(elements) {
    elements.forEach((el, i) => {
      el.style.order = i;
    });
  }
}
```

## Reactive Properties

### Property/Attribute Reflection

```javascript
class ReactiveElement extends HTMLElement {
  static get observedAttributes() {
    return ['count', 'disabled'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._count = 0;
  }

  // Reflect property to attribute
  get count() {
    return this._count;
  }

  set count(value) {
    this._count = Number(value);
    this.setAttribute('count', this._count);
    this.render();
  }

  // Boolean attribute
  get disabled() {
    return this.hasAttribute('disabled');
  }

  set disabled(value) {
    if (value) {
      this.setAttribute('disabled', '');
    } else {
      this.removeAttribute('disabled');
    }
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === 'count' && oldValue !== newValue) {
      this._count = Number(newValue);
      this.render();
    }
  }

  render() {
    this.shadowRoot.innerHTML = `
      <button ${this.disabled ? 'disabled' : ''}>
        Count: ${this.count}
      </button>
    `;
  }
}
```

### Form-Associated Custom Elements

```javascript
class CustomInput extends HTMLElement {
  static formAssociated = true;

  constructor() {
    super();
    this.internals = this.attachInternals();
    this.attachShadow({ mode: 'open' });

    this.shadowRoot.innerHTML = `
      <style>
        input {
          padding: 0.5rem;
          border: 1px solid #ccc;
          border-radius: 4px;
        }
        input:focus {
          outline: 2px solid #007bff;
        }
        :host(:invalid) input {
          border-color: red;
        }
      </style>
      <input type="text">
    `;

    this.input = this.shadowRoot.querySelector('input');
    this.input.addEventListener('input', () => this.handleInput());
  }

  handleInput() {
    this.internals.setFormValue(this.input.value);

    // Validation
    if (this.hasAttribute('required') && !this.input.value) {
      this.internals.setValidity(
        { valueMissing: true },
        'This field is required',
        this.input
      );
    } else {
      this.internals.setValidity({});
    }
  }

  // Form lifecycle
  formAssociatedCallback(form) {
    console.log('Associated with form:', form);
  }

  formDisabledCallback(disabled) {
    this.input.disabled = disabled;
  }

  formResetCallback() {
    this.input.value = '';
    this.internals.setFormValue('');
  }

  // Expose validity state
  get validity() { return this.internals.validity; }
  get validationMessage() { return this.internals.validationMessage; }
  checkValidity() { return this.internals.checkValidity(); }
  reportValidity() { return this.internals.reportValidity(); }
}

customElements.define('custom-input', CustomInput);

// Usage in form
// <form>
//   <custom-input name="username" required></custom-input>
//   <button type="submit">Submit</button>
// </form>
```

## Event Handling

### Custom Events

```javascript
class CounterElement extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._count = 0;
    this.render();
  }

  increment() {
    this._count++;
    this.render();

    // Dispatch custom event (bubbles through shadow DOM)
    this.dispatchEvent(new CustomEvent('count-changed', {
      detail: { count: this._count },
      bubbles: true,
      composed: true  // Crosses shadow DOM boundary
    }));
  }

  render() {
    this.shadowRoot.innerHTML = `
      <button id="btn">Count: ${this._count}</button>
    `;
    this.shadowRoot.getElementById('btn')
      .addEventListener('click', () => this.increment());
  }
}

// Listen from outside
document.querySelector('counter-element')
  .addEventListener('count-changed', (e) => {
    console.log('New count:', e.detail.count);
  });
```

### Event Retargeting

```javascript
class EventDemo extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    this.shadowRoot.innerHTML = `
      <button id="inner">Click me</button>
    `;

    // Event target inside shadow DOM
    this.shadowRoot.getElementById('inner')
      .addEventListener('click', (e) => {
        console.log('Inside shadow:', e.target); // <button>
      });
  }
}

// Outside shadow DOM, target is retargeted to host
document.querySelector('event-demo')
  .addEventListener('click', (e) => {
    console.log('Outside shadow:', e.target); // <event-demo>
    console.log('Composed path:', e.composedPath()); // Full path
  });
```

## Complete Example: Modal Component

```javascript
class AppModal extends HTMLElement {
  static get observedAttributes() {
    return ['open'];
  }

  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: none;
        }

        :host([open]) {
          display: block;
        }

        .backdrop {
          position: fixed;
          inset: 0;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
        }

        .modal {
          background: white;
          border-radius: 8px;
          max-width: 500px;
          width: 90%;
          max-height: 90vh;
          overflow: auto;
          box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        }

        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1rem;
          border-bottom: 1px solid #e5e7eb;
        }

        .close-btn {
          background: none;
          border: none;
          font-size: 1.5rem;
          cursor: pointer;
          padding: 0.25rem;
        }

        .body {
          padding: 1rem;
        }

        .footer {
          padding: 1rem;
          border-top: 1px solid #e5e7eb;
          display: flex;
          justify-content: flex-end;
          gap: 0.5rem;
        }
      </style>

      <div class="backdrop" part="backdrop">
        <div class="modal" part="modal" role="dialog" aria-modal="true">
          <div class="header" part="header">
            <slot name="title"><h2>Modal</h2></slot>
            <button class="close-btn" aria-label="Close">&times;</button>
          </div>
          <div class="body" part="body">
            <slot></slot>
          </div>
          <div class="footer" part="footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    `;

    this.backdrop = this.shadowRoot.querySelector('.backdrop');
    this.closeBtn = this.shadowRoot.querySelector('.close-btn');

    this.closeBtn.addEventListener('click', () => this.close());
    this.backdrop.addEventListener('click', (e) => {
      if (e.target === this.backdrop) this.close();
    });
  }

  get open() {
    return this.hasAttribute('open');
  }

  set open(value) {
    if (value) {
      this.setAttribute('open', '');
    } else {
      this.removeAttribute('open');
    }
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === 'open') {
      if (newValue !== null) {
        this.trapFocus();
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
      }
    }
  }

  show() {
    this.open = true;
    this.dispatchEvent(new CustomEvent('modal-open', { bubbles: true, composed: true }));
  }

  close() {
    this.open = false;
    this.dispatchEvent(new CustomEvent('modal-close', { bubbles: true, composed: true }));
  }

  trapFocus() {
    const focusable = this.shadowRoot.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    first?.focus();

    this.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.close();
      }
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    });
  }
}

customElements.define('app-modal', AppModal);
```

```html
<!-- Usage -->
<button onclick="document.querySelector('app-modal').show()">
  Open Modal
</button>

<app-modal>
  <h2 slot="title">Confirm Action</h2>
  <p>Are you sure you want to proceed?</p>
  <div slot="footer">
    <button onclick="this.closest('app-modal').close()">Cancel</button>
    <button onclick="handleConfirm()">Confirm</button>
  </div>
</app-modal>
```

## Reference Files

- [lit-integration.md](references/lit-integration.md) - Using Lit for simpler web components
- [testing.md](references/testing.md) - Testing web components
