---
name: Web Accessibility
description: This skill activates when users discuss WCAG compliance, screen readers, keyboard navigation, ARIA, semantic HTML, or accessibility issues. Provides guidance on making WordPress themes and web applications accessible to all users following WCAG 2.1 AA/AAA standards.
---

# Web Accessibility (A11y)

Build inclusive, accessible web experiences that work for everyone.

## When This Activates

- "accessibility", "a11y", "WCAG", "screen reader"
- "keyboard navigation", "ARIA", "semantic HTML"
- "color contrast", "focus states", "alt text"
- User asks about making site accessible
- Discussing inclusive design

---

## WCAG 2.1 Quick Reference

| Level | Requirement |
|-------|-------------|
| **A** | Basic accessibility (minimum legal requirement) |
| **AA** | Standard for most websites (Target: SkyyRose) |
| **AAA** | Enhanced accessibility (ideal, not always possible) |

**SkyyRose Target**: WCAG 2.1 AA compliance

---

## Semantic HTML

### Use the Right Element

```html
<!-- ❌ Bad: Divs for everything -->
<div class="header">
  <div class="nav">
    <div onclick="navigate()">Home</div>
    <div onclick="navigate()">Shop</div>
  </div>
</div>
<div class="main">
  <div class="article">...</div>
</div>

<!-- ✅ Good: Semantic elements -->
<header>
  <nav>
    <a href="/">Home</a>
    <a href="/shop">Shop</a>
  </nav>
</header>
<main>
  <article>...</article>
</main>
```

### Landmarks

```html
<!-- Screen readers use landmarks for navigation -->
<header role="banner">
  <nav role="navigation" aria-label="Primary">...</nav>
</header>

<main role="main">
  <article>...</article>
  <aside role="complementary">...</aside>
</main>

<footer role="contentinfo">...</footer>
```

---

## Keyboard Navigation

### Focus Management

```tsx
// All interactive elements must be keyboard accessible
function ProductCard({ product }: { product: Product }) {
  return (
    <article className="product-card">
      <a
        href={`/products/${product.id}`}
        className="product-card__link"
        // Focus styles in CSS
        aria-label={`View ${product.name}`}
      >
        <img src={product.image} alt={product.name} />
        <h3>{product.name}</h3>
        <p>${product.price}</p>
      </a>

      <button
        onClick={() => addToCart(product.id)}
        className="product-card__button"
        aria-label={`Add ${product.name} to cart`}
      >
        Add to Cart
      </button>
    </article>
  );
}
```

```css
/* Clear, visible focus states */
.product-card__link:focus,
.product-card__button:focus {
  outline: 3px solid #B76E79; /* SkyyRose brand color */
  outline-offset: 2px;
}

/* Never remove outline without replacement */
button:focus {
  outline: none; /* ❌ BAD - makes keyboard nav impossible */
}

button:focus-visible {
  /* ✅ GOOD - visible focus for keyboard, hidden for mouse */
  outline: 3px solid #B76E79;
  outline-offset: 2px;
}
```

### Skip Links

```tsx
// Allow keyboard users to skip repetitive content
function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <a
        href="#main-content"
        className="skip-link"
        // Position off-screen, visible on focus
      >
        Skip to main content
      </a>

      <Header />

      <main id="main-content" tabIndex={-1}>
        {children}
      </main>

      <Footer />
    </>
  );
}
```

```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #B76E79;
  color: white;
  padding: 8px 16px;
  text-decoration: none;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

---

## ARIA (Accessible Rich Internet Applications)

### When to Use ARIA

**First Rule of ARIA**: Don't use ARIA if you can use native HTML

```html
<!-- ❌ Bad: Unnecessary ARIA -->
<div role="button" tabindex="0" aria-label="Click me">Click</div>

<!-- ✅ Good: Native button -->
<button>Click me</button>
```

### ARIA Labels

```tsx
// When visual label isn't enough
<button
  onClick={handleAddToCart}
  aria-label="Add Diamond Ring to cart" // Context for screen readers
>
  <PlusIcon aria-hidden="true" /> {/* Hide decorative icons */}
  Add to Cart
</button>

// Form inputs
<label htmlFor="email">Email Address</label>
<input
  type="email"
  id="email"
  name="email"
  aria-required="true"
  aria-invalid={hasError}
  aria-describedby={hasError ? 'email-error' : undefined}
/>
{hasError && <p id="email-error" role="alert">Please enter valid email</p>}
```

### ARIA Live Regions

```tsx
// Announce dynamic changes to screen readers
function Cart() {
  const [items, setItems] = useState<CartItem[]>([]);
  const [message, setMessage] = useState('');

  const addItem = (item: CartItem) => {
    setItems([...items, item]);
    setMessage(`${item.name} added to cart`);
  };

  return (
    <>
      {/* Screen reader announcements */}
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only" // Visually hidden
      >
        {message}
      </div>

      <div aria-label="Shopping cart" role="region">
        <h2>Cart ({items.length})</h2>
        {items.map((item) => (
          <CartItem key={item.id} item={item} />
        ))}
      </div>
    </>
  );
}
```

```css
/* Screen reader only class */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

---

## Color & Contrast

### WCAG AA Contrast Requirements

| Text Size | Ratio |
|-----------|-------|
| **Normal text** (< 18px) | 4.5:1 |
| **Large text** (≥ 18px or ≥ 14px bold) | 3:1 |
| **UI components** (buttons, inputs) | 3:1 |

### Check Contrast

```typescript
// SkyyRose brand colors (#B76E79) on white background
// Contrast ratio: 3.8:1 (FAILS for normal text, PASSES for large text)

// Solutions:
const accessibleColors = {
  // Option 1: Darker variant for small text
  primaryDark: '#8B5663', // Contrast: 5.2:1 ✅

  // Option 2: Use primary for large text only
  primary: '#B76E79', // Use for headings (≥18px)

  // Option 3: Ensure text is large enough
  minFontSize: '18px', // When using #B76E79
};
```

### Never Rely on Color Alone

```tsx
// ❌ Bad: Color is the only indicator
<span style={{ color: 'red' }}>Error</span>

// ✅ Good: Icon + text + color
<span style={{ color: '#EF4444' }}>
  <ErrorIcon aria-hidden="true" />
  <span>Error: Invalid email address</span>
</span>
```

---

## Images & Media

### Alt Text

```tsx
// Descriptive alt text
<img
  src="/jewelry/diamond-ring.jpg"
  alt="18K rose gold engagement ring with 2-carat round diamond in cathedral setting"
  // NOT: alt="ring" or alt="image"
/>

// Decorative images
<img
  src="/divider.svg"
  alt="" // Empty alt for decorative
  role="presentation"
/>

// Complex images (charts, diagrams)
<figure>
  <img
    src="/sales-chart.png"
    alt="Bar chart showing sales growth"
    aria-describedby="chart-description"
  />
  <figcaption id="chart-description">
    Sales increased from $10k in January to $50k in December,
    with the largest jump in November ($40k to $50k).
  </figcaption>
</figure>
```

### Video Accessibility

```tsx
<video
  controls
  aria-label="Product showcase video"
>
  <source src="showcase.mp4" type="video/mp4" />

  {/* Captions for deaf/hard of hearing */}
  <track
    kind="captions"
    src="captions-en.vtt"
    srcLang="en"
    label="English"
    default
  />

  {/* Descriptions for blind users */}
  <track
    kind="descriptions"
    src="descriptions-en.vtt"
    srcLang="en"
    label="English descriptions"
  />

  Your browser doesn't support video.
</video>
```

---

## Forms

### Accessible Form Patterns

```tsx
function CheckoutForm() {
  return (
    <form aria-labelledby="checkout-heading">
      <h2 id="checkout-heading">Checkout</h2>

      {/* Required field indicator */}
      <p>
        <span aria-hidden="true">*</span>
        <span className="sr-only">Required field</span>
      </p>

      {/* Text input */}
      <div className="form-field">
        <label htmlFor="full-name">
          Full Name <span aria-label="required">*</span>
        </label>
        <input
          type="text"
          id="full-name"
          name="fullName"
          aria-required="true"
          aria-invalid={errors.fullName ? 'true' : 'false'}
          aria-describedby={errors.fullName ? 'name-error' : undefined}
        />
        {errors.fullName && (
          <p id="name-error" role="alert" className="error">
            {errors.fullName}
          </p>
        )}
      </div>

      {/* Radio buttons */}
      <fieldset>
        <legend>Shipping Method</legend>
        <div>
          <input
            type="radio"
            id="standard"
            name="shipping"
            value="standard"
          />
          <label htmlFor="standard">Standard (5-7 days) - Free</label>
        </div>
        <div>
          <input
            type="radio"
            id="express"
            name="shipping"
            value="express"
          />
          <label htmlFor="express">Express (2-3 days) - $15</label>
        </div>
      </fieldset>

      {/* Checkbox with description */}
      <div>
        <input
          type="checkbox"
          id="subscribe"
          name="subscribe"
          aria-describedby="subscribe-description"
        />
        <label htmlFor="subscribe">Subscribe to newsletter</label>
        <p id="subscribe-description" className="help-text">
          Receive updates about new collections and exclusive offers
        </p>
      </div>

      <button type="submit" aria-label="Complete purchase">
        Place Order
      </button>
    </form>
  );
}
```

---

## Modal Dialogs

```tsx
import { useEffect, useRef } from 'react';

function Modal({ isOpen, onClose, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (isOpen) {
      // Focus trap: Keep focus inside modal
      closeButtonRef.current?.focus();

      // Prevent body scroll
      document.body.style.overflow = 'hidden';

      // Handle Escape key
      const handleEscape = (e: KeyboardEvent) => {
        if (e.key === 'Escape') onClose();
      };
      document.addEventListener('keydown', handleEscape);

      return () => {
        document.body.style.overflow = '';
        document.removeEventListener('keydown', handleEscape);
      };
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      ref={modalRef}
      className="modal-overlay"
      onClick={(e) => {
        // Close on backdrop click
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="modal-content">
        <button
          ref={closeButtonRef}
          onClick={onClose}
          aria-label="Close modal"
          className="modal-close"
        >
          ×
        </button>

        <h2 id="modal-title">Modal Title</h2>

        {children}
      </div>
    </div>
  );
}
```

---

## WordPress Accessibility

### Theme Support

```php
// functions.php
function skyyrose_theme_support() {
    // Accessibility features
    add_theme_support('automatic-feed-links');
    add_theme_support('title-tag');
    add_theme_support('html5', [
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
    ]);

    // Skip link
    add_action('wp_body_open', function() {
        echo '<a class="skip-link screen-reader-text" href="#primary">Skip to content</a>';
    });
}
add_action('after_setup_theme', 'skyyrose_theme_support');
```

### Navigation Menus

```php
// Accessible navigation menu
wp_nav_menu([
    'theme_location' => 'primary',
    'container' => 'nav',
    'container_aria_label' => 'Primary Navigation',
    'menu_class' => 'primary-menu',
    'fallback_cb' => false,
]);
```

### Custom Elementor Widgets

```php
class Skyy_Product_3D_Widget extends \Elementor\Widget_Base {
    protected function render() {
        ?>
        <div
            class="skyy-product-3d"
            role="region"
            aria-label="3D Product Viewer"
        >
            <button
                class="product-3d__rotate"
                aria-label="Rotate product 360 degrees"
                aria-pressed="false"
            >
                <span aria-hidden="true">↻</span>
                Rotate
            </button>

            <canvas
                id="product-canvas"
                role="img"
                aria-label="3D model of <?php echo esc_attr($product_name); ?>"
            ></canvas>

            <!-- Fallback for users who can't see 3D -->
            <div class="product-3d__fallback">
                <img
                    src="<?php echo esc_url($product_image); ?>"
                    alt="<?php echo esc_attr($product_name); ?>"
                />
            </div>
        </div>
        <?php
    }
}
```

---

## Testing Accessibility

### Automated Tools

```bash
# axe-core (best automated testing)
npm install --save-dev @axe-core/cli

# Test page
axe https://skyyrose.co --tags wcag2aa

# Lighthouse (includes a11y audit)
lighthouse https://skyyrose.co --only-categories=accessibility

# Pa11y
npm install --save-dev pa11y
pa11y https://skyyrose.co --standard WCAG2AA
```

### Manual Testing

1. **Keyboard Navigation**
   - Tab through all interactive elements
   - Ensure focus is visible
   - Check modal/dropdown keyboard trapping

2. **Screen Reader**
   - macOS: VoiceOver (Cmd+F5)
   - Windows: NVDA (free) or JAWS
   - Test landmarks, headings, alt text

3. **Color Contrast**
   - Use browser DevTools contrast checker
   - Or: https://webaim.org/resources/contrastchecker/

4. **Zoom**
   - Zoom to 200% (browser zoom)
   - Ensure no horizontal scroll
   - Content remains readable

5. **Motion Preferences**
   - Test with `prefers-reduced-motion`

```css
/* Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## SkyyRose Accessibility Checklist

For every page/component:

- [ ] **Semantic HTML**: Proper headings, landmarks, lists
- [ ] **Keyboard**: All interactive elements keyboard accessible
- [ ] **Focus**: Visible focus indicators (3px #B76E79 outline)
- [ ] **Color**: 4.5:1 contrast for text, 3:1 for UI components
- [ ] **Alt Text**: Descriptive alt for images, empty for decorative
- [ ] **Forms**: Labels, error messages, fieldsets
- [ ] **ARIA**: Only when needed, labels for icon buttons
- [ ] **Motion**: Respect `prefers-reduced-motion`
- [ ] **Screen Reader**: Test with VoiceOver/NVDA
- [ ] **Zoom**: Works at 200% zoom

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| **Missing alt text** | Add descriptive alt to all images |
| **Poor contrast** | Use darker colors or larger text |
| **No focus indicators** | Add visible :focus styles |
| **Keyboard trap** | Implement proper focus management in modals |
| **Missing labels** | Add labels to all form inputs |
| **Non-semantic HTML** | Use button/nav/main instead of divs |
| **Icon-only buttons** | Add aria-label |
| **Auto-playing videos** | Provide pause button, captions |

---

## When User Asks About Accessibility

1. **Identify issues**: Run automated scan (axe, Lighthouse)
2. **Prioritize**: Fix critical issues first (keyboard, contrast)
3. **Implement**: Use semantic HTML, ARIA sparingly
4. **Test manually**: Keyboard, screen reader, zoom
5. **Document**: Note accessibility features in README

Always aim for WCAG 2.1 AA compliance as baseline, AAA where possible.
