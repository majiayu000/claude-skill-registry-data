---
name: supporting-custom-elements
description: Teaches Web Components (Custom Elements) support in React 19, including property vs attribute handling and custom events. Use when integrating Web Components or working with custom HTML elements.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Web Components Support in React 19

<role>
This skill teaches you how to use Web Components (Custom Elements) in React 19, which now has full support.
</role>

<when-to-activate>
This skill activates when:

- Working with Web Components or Custom Elements
- Integrating third-party web components
- Passing props to custom elements
- Handling custom events from web components
- Migration from React 18 web component workarounds
  </when-to-activate>

<overview>
React 19 adds full support for Custom Elements and passes all Custom Elements Everywhere tests.

**New in React 19:**

1. **Automatic Property Detection** - React determines property vs attribute
2. **Custom Event Support** - Standard `on + EventName` convention
3. **Boolean Attributes** - Properly handled (added/removed as needed)
4. **No Ref Workarounds** - Pass props directly to custom elements

**Before React 19:**

```javascript
<web-counter
  ref={(el) => {
    if (el) {
      el.increment = increment;
      el.isDark = isDark;
    }
  }}
/>
```

**React 19:**

```javascript
<web-counter increment={increment} isDark={isDark} onIncrementEvent={() => setCount(count + 1)} />
```

</overview>

<workflow>
## Using Web Components

**Step 1: Define Custom Element** (or use third-party)

```javascript
class WebCounter extends HTMLElement {
  connectedCallback() {
    this.render();
  }

  set increment(fn) {
    this._increment = fn;
  }

  set isDark(value) {
    this._isDark = value;
    this.render();
  }

  handleClick() {
    this._increment?.();
    this.dispatchEvent(new CustomEvent('incremented'));
  }

  render() {
    this.innerHTML = `
      <button style="color: ${this._isDark ? 'white' : 'black'}">
        Increment
      </button>
    `;
    this.querySelector('button').onclick = () => this.handleClick();
  }
}

customElements.define('web-counter', WebCounter);
```

**Step 2: Use in React 19**

```javascript
function App() {
  const [count, setCount] = useState(0);
  const [isDark, setIsDark] = useState(false);

  const increment = () => setCount(count + 1);

  return (
    <div>
      <p>Count: {count}</p>

      <web-counter
        increment={increment}
        isDark={isDark}
        onIncremented={() => console.log('Incremented!')}
      />

      <button onClick={() => setIsDark(!isDark)}>Toggle Theme</button>
    </div>
  );
}
```

**Step 3: Handle Custom Events**

Custom events follow `on + EventName` convention:

```javascript
<my-button label="Click Me" onButtonClick={handleClick} />
```

If custom element dispatches `buttonClick` event, React automatically wires it up.

</workflow>

<examples>
## Example: Third-Party Web Component

```javascript
import '@material/mwc-button';

function MaterialButton() {
  return <mwc-button raised label="Click me" icon="code" onClick={() => alert('Clicked!')} />;
}
```

## Example: Custom Form Element

```javascript
class RatingInput extends HTMLElement {
  connectedCallback() {
    this.rating = 0;
    this.render();
  }

  setRating(value) {
    this.rating = value;
    this.dispatchEvent(
      new CustomEvent('ratingChange', {
        detail: { rating: value },
      })
    );
    this.render();
  }

  render() {
    this.innerHTML = `
      ${[1, 2, 3, 4, 5]
        .map(
          (i) => `
        <button data-rating="${i}">⭐</button>
      `
        )
        .join('')}
    `;

    this.querySelectorAll('button').forEach((btn) => {
      btn.onclick = () => this.setRating(+btn.dataset.rating);
    });
  }
}

customElements.define('rating-input', RatingInput);
```

```javascript
function ReviewForm() {
  const [rating, setRating] = useState(0);

  return (
    <form>
      <rating-input onRatingChange={(e) => setRating(e.detail.rating)} />
      <p>Rating: {rating}</p>
    </form>
  );
}
```

For comprehensive Custom Elements documentation, see: `research/react-19-comprehensive.md` lines 1034-1089.
</examples>

<constraints>
## MUST
- Use standard `on + EventName` for custom events
- Let React determine property vs attribute automatically
- Define custom elements before using in React

## SHOULD

- Prefer Web Components for framework-agnostic widgets
- Use TypeScript declarations for custom elements
- Test SSR vs CSR rendering differences

## NEVER

- Use ref workarounds (React 19 handles props directly)
- Forget to define custom elements (will render as unknown tag)
- Pass non-primitive values in SSR context (will be omitted)
  </constraints>
