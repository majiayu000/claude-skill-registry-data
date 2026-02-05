---
name: view-transitions
description: Creates smooth animated transitions between views using the native View Transitions API. Use when building page transitions, state changes, or morphing elements between different DOM states in SPAs and MPAs.
---

# View Transitions API

Native browser API for smooth animated transitions between different views. Works in SPAs (JavaScript-triggered) and MPAs (navigation-based).

## Browser Support

- **Same-document (SPA)**: Chrome 111+, Edge 111+, Safari 18+, Firefox 144+
- **Cross-document (MPA)**: Chrome 126+, Edge 126+, Safari 18.2+

## Quick Start - SPA

```javascript
// Check for support
if (!document.startViewTransition) {
  updateDOM();
  return;
}

// Trigger transition
document.startViewTransition(() => {
  updateDOM();
});
```

The API:
1. Captures snapshots of current state
2. Runs your callback to update DOM
3. Captures snapshots of new state
4. Animates between old and new states

## Quick Start - MPA

No JavaScript needed. Opt in with CSS on both pages:

```css
@view-transition {
  navigation: auto;
}
```

Transitions happen automatically on same-origin navigations.

## Basic CSS Customization

```css
/* Customize the default cross-fade */
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.5s;
}

/* Fade out old view */
::view-transition-old(root) {
  animation: fade-out 0.3s ease-out both;
}

/* Fade in new view */
::view-transition-new(root) {
  animation: fade-in 0.3s ease-in both;
}

@keyframes fade-out {
  to { opacity: 0; }
}

@keyframes fade-in {
  from { opacity: 0; }
}
```

## Named Transitions

Give specific elements their own transition behavior.

```css
/* Assign a name to an element */
.header {
  view-transition-name: header;
}

.main-image {
  view-transition-name: main-image;
}

/* Names must be unique! */
```

```css
/* Style transitions for named elements */
::view-transition-old(main-image),
::view-transition-new(main-image) {
  animation-duration: 0.4s;
}

/* Keep header fixed during transition */
::view-transition-group(header) {
  animation: none;
}
```

## Pseudo-Element Tree

When a view transition runs, this pseudo-element tree is created:

```
::view-transition
└─ ::view-transition-group(name)
   └─ ::view-transition-image-pair(name)
      ├─ ::view-transition-old(name)
      └─ ::view-transition-new(name)
```

| Pseudo | Purpose |
|--------|---------|
| `::view-transition` | Overlay containing all transitions |
| `::view-transition-group(name)` | Container for size/position animation |
| `::view-transition-image-pair(name)` | Contains old and new snapshots |
| `::view-transition-old(name)` | Screenshot of old state |
| `::view-transition-new(name)` | Live representation of new state |

## Transition Types

Categorize transitions for different styling:

```javascript
document.startViewTransition({
  update: () => updateDOM(),
  types: ['slide-left']  // Add type identifiers
});
```

```css
/* Style based on transition type */
html:active-view-transition-type(slide-left) {
  &::view-transition-old(root) {
    animation: slide-out-left 0.3s ease;
  }
  &::view-transition-new(root) {
    animation: slide-in-right 0.3s ease;
  }
}

@keyframes slide-out-left {
  to { transform: translateX(-100%); }
}

@keyframes slide-in-right {
  from { transform: translateX(100%); }
}
```

## JavaScript API

### ViewTransition Object

```javascript
const transition = document.startViewTransition(() => {
  // Update DOM here
});

// Promises for timing
transition.ready.then(() => {
  // Pseudo-elements created, animation about to start
});

transition.updateCallbackDone.then(() => {
  // DOM update callback finished
});

transition.finished.then(() => {
  // Animation complete
});

// Skip the animation
transition.skipTransition();
```

### Custom JavaScript Animation

```javascript
const transition = document.startViewTransition(() => updateDOM());

transition.ready.then(() => {
  // Use Web Animations API on pseudo-elements
  document.documentElement.animate(
    [
      { clipPath: 'circle(0% at 50% 50%)' },
      { clipPath: 'circle(100% at 50% 50%)' }
    ],
    {
      duration: 500,
      easing: 'ease-out',
      pseudoElement: '::view-transition-new(root)'
    }
  );
});
```

## React Integration

### Basic Hook

```jsx
function useViewTransition() {
  const startTransition = (callback) => {
    if (!document.startViewTransition) {
      callback();
      return;
    }
    document.startViewTransition(callback);
  };

  return { startTransition };
}

// Usage
function Component() {
  const { startTransition } = useViewTransition();
  const [page, setPage] = useState('home');

  const navigate = (newPage) => {
    startTransition(() => setPage(newPage));
  };

  return (
    <div>
      <nav>
        <button onClick={() => navigate('home')}>Home</button>
        <button onClick={() => navigate('about')}>About</button>
      </nav>
      {page === 'home' && <HomePage />}
      {page === 'about' && <AboutPage />}
    </div>
  );
}
```

### With React Router

```jsx
import { useNavigate } from 'react-router-dom';

function NavLink({ to, children }) {
  const navigate = useNavigate();

  const handleClick = (e) => {
    e.preventDefault();

    if (!document.startViewTransition) {
      navigate(to);
      return;
    }

    document.startViewTransition(() => {
      navigate(to);
    });
  };

  return <a href={to} onClick={handleClick}>{children}</a>;
}
```

### React 19+ (Experimental)

```jsx
import { unstable_ViewTransition as ViewTransition } from 'react';

function App() {
  const [page, setPage] = useState('home');

  return (
    <ViewTransition>
      {page === 'home' ? <Home /> : <About />}
    </ViewTransition>
  );
}
```

## Common Patterns

### Hero Image Morph

```css
/* List page */
.thumbnail {
  view-transition-name: hero-image;
}

/* Detail page */
.hero-image {
  view-transition-name: hero-image;
}

/* The image will smoothly morph between pages */
::view-transition-group(hero-image) {
  animation-duration: 0.4s;
}
```

### Shared Header

```css
.header {
  view-transition-name: header;
}

/* Keep header in place */
::view-transition-old(header),
::view-transition-new(header) {
  animation: none;
  mix-blend-mode: normal;
}
```

### Slide Transitions

```css
@keyframes slide-from-right {
  from { transform: translateX(100%); }
}

@keyframes slide-to-left {
  to { transform: translateX(-100%); }
}

/* Forward navigation */
html:active-view-transition-type(forward) {
  &::view-transition-old(root) {
    animation: slide-to-left 0.3s ease forwards;
  }
  &::view-transition-new(root) {
    animation: slide-from-right 0.3s ease forwards;
  }
}

/* Back navigation */
html:active-view-transition-type(back) {
  &::view-transition-old(root) {
    animation: slide-from-right 0.3s ease reverse forwards;
  }
  &::view-transition-new(root) {
    animation: slide-to-left 0.3s ease reverse forwards;
  }
}
```

### Circle Reveal

```javascript
function circleReveal(x, y) {
  const transition = document.startViewTransition(() => updateContent());

  transition.ready.then(() => {
    const maxRadius = Math.hypot(
      Math.max(x, window.innerWidth - x),
      Math.max(y, window.innerHeight - y)
    );

    document.documentElement.animate(
      {
        clipPath: [
          `circle(0px at ${x}px ${y}px)`,
          `circle(${maxRadius}px at ${x}px ${y}px)`
        ]
      },
      {
        duration: 500,
        easing: 'ease-in-out',
        pseudoElement: '::view-transition-new(root)'
      }
    );
  });
}

// Trigger from click position
button.addEventListener('click', (e) => {
  circleReveal(e.clientX, e.clientY);
});
```

### Grid Item Expansion

```css
/* In grid */
.card {
  view-transition-name: var(--card-id);
}

/* When expanded */
.card-detail {
  view-transition-name: var(--card-id);
}
```

```jsx
function Card({ id, onClick }) {
  return (
    <div
      className="card"
      style={{ '--card-id': `card-${id}` }}
      onClick={onClick}
    />
  );
}
```

## MPA Cross-Document Transitions

### Opt In

```css
/* Add to both pages */
@view-transition {
  navigation: auto;
}
```

### Customize by Page

```html
<!-- page1.html -->
<html class="page-home">

<!-- page2.html -->
<html class="page-about">
```

```css
/* Styles apply based on destination */
.page-about::view-transition-old(root) {
  animation: slide-out-left 0.3s;
}
```

### Match Elements Across Pages

Use the new `match-element` value (Chrome 126+):

```css
/* Automatically generate view-transition-name based on element identity */
.product-card {
  view-transition-name: match-element;
}
```

Or manually assign matching names:

```css
/* page1.html */
.product-thumbnail[data-id="123"] {
  view-transition-name: product-123;
}

/* page2.html */
.product-hero[data-id="123"] {
  view-transition-name: product-123;
}
```

## Accessibility

### Respect Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation: none !important;
  }
}
```

### Skip for Screen Readers

View transitions are purely visual; screen readers see the DOM update immediately.

## Debugging

Chrome DevTools:
1. Open Elements panel
2. Check "Show view transition pseudo-elements"
3. Inspect `::view-transition-*` elements

Add slow-mo for development:

```css
::view-transition-old(*),
::view-transition-new(*) {
  animation-duration: 3s !important;
}
```

## Best Practices

1. **Keep transitions short** - 200-400ms for most cases
2. **Use `view-transition-name` sparingly** - Too many can hurt performance
3. **Avoid layout shifts** - Elements should have stable sizes
4. **Test without transitions** - Ensure DOM updates work without the API
5. **Handle edge cases** - Elements only on one page need custom enter/exit
6. **Use types for direction** - Forward vs back navigation should feel different

## Fallback Strategy

```javascript
async function navigate(callback) {
  // Feature detection
  if (!document.startViewTransition) {
    callback();
    return;
  }

  try {
    await document.startViewTransition(callback).finished;
  } catch (e) {
    // Transition was skipped or errored
    // DOM is still updated, just not animated
  }
}
```
