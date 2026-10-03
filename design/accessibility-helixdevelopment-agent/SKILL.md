---
name: accessibility
description: Implement web accessibility (a11y) best practices following WCAG guidelines. Ensure inclusive design for users with disabilities.
triggers:
- /a11y
- /accessibility
---

# Web Accessibility (a11y)

This skill guides you through implementing web accessibility best practices following WCAG guidelines to create inclusive experiences for users with disabilities.

## When to use this skill

Use this skill when you need to:
- Audit and fix accessibility issues
- Design accessible user interfaces
- Implement keyboard navigation
- Create screen reader compatible content
- Meet WCAG compliance requirements

## Prerequisites

- Understanding of WCAG 2.1 guidelines
- Accessibility testing tools (axe, Lighthouse, WAVE)
- Screen reader (NVDA, JAWS, VoiceOver)
- Keyboard-only navigation testing

## Guidelines

### WCAG Principles (POUR)

**Perceivable**
- Text alternatives for images
- Captions/transcripts for media
- Color not sole means of conveying info
- Resizable text up to 200%

**Operable**
- All functionality available via keyboard
- No time limits or adjustable
- No seizure-inducing content
- Clear navigation

**Understandable**
- Readable text (simple language)
- Predictable behavior
- Input error prevention
- Helpful error messages

**Robust**
- Compatible with assistive technologies
- Valid HTML
- Consistent implementation

### Semantic HTML

**Structure**
```html
<!-- ✅ Good: Semantic structure -->
<header>
  <nav aria-label="Main">
    <ul>
      <li><a href="/" aria-current="page">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>

<main>
  <h1>Page Title</h1>
  <section aria-labelledby="products-heading">
    <h2 id="products-heading">Products</h2>
    <!-- content -->
  </section>
</main>

<footer>
  <p>&copy; 2024 Company</p>
</footer>

<!-- ❌ Bad: Div soup -->
<div class="header">
  <div class="nav">
    <div class="nav-item">Home</div>
  </div>
</div>
```

**Form Labels**
```html
<!-- ✅ Good: Associated labels -->
<label for="email">Email Address</label>
<input type="email" id="email" name="email" required>

<!-- Or using aria-label -->
<input type="search" aria-label="Search products" placeholder="Search...">

<!-- Or using aria-labelledby -->
<span id="username-label">Username</span>
<input type="text" aria-labelledby="username-label">

<!-- ❌ Bad: No label association -->
<input type="email" placeholder="Enter email">
```

### Keyboard Navigation

**Focus Management**
```css
/* Visible focus indicators */
:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* Skip links */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
}

.skip-link:focus {
  top: 0;
}
```

```html
<!-- Skip navigation link -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<main id="main-content">
  <!-- Page content -->
</main>
```

**Focus Trap in Modals**
```javascript
// Manage focus within modal
function openModal() {
  modal.show();
  firstFocusableElement.focus();
  document.addEventListener('keydown', trapFocus);
}

function trapFocus(e) {
  if (e.key === 'Tab') {
    if (e.shiftKey && document.activeElement === firstFocusableElement) {
      e.preventDefault();
      lastFocusableElement.focus();
    } else if (!e.shiftKey && document.activeElement === lastFocusableElement) {
      e.preventDefault();
      firstFocusableElement.focus();
    }
  }
  if (e.key === 'Escape') {
    closeModal();
  }
}
```

### ARIA Attributes

**Landmarks**
```html
<header role="banner">...</header>
<nav role="navigation">...</nav>
<main role="main">...</main>
<aside role="complementary">...</aside>
<footer role="contentinfo">...</footer>
```

**Dynamic Content**
```html
<!-- Live regions for announcements -->
<div aria-live="polite" aria-atomic="true" id="status-region">
  <!-- Status messages inserted here -->
</div>

<!-- Progress indication -->
<div role="progressbar" aria-valuenow="50" aria-valuemin="0" 
     aria-valuemax="100" aria-label="Upload progress">
  50%
</div>
```

**Accessible Components**
```html
<!-- Button vs Link -->
<button type="button" onclick="submitForm()">Submit</button>
<a href="/page">Navigate to Page</a>

<!-- Tabs -->
<div role="tablist">
  <button role="tab" aria-selected="true" id="tab-1" 
          aria-controls="panel-1">Tab 1</button>
  <button role="tab" aria-selected="false" id="tab-2"
          aria-controls="panel-2">Tab 2</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">...</div>
```

### Images and Media

**Alt Text Guidelines**
```html
<!-- Decorative image: empty alt -->
<img src="decorative-border.png" alt="">

<!-- Informative image: descriptive alt -->
<img src="chart.png" alt="Sales increased 50% from January to June">

<!-- Complex image: long description -->
<img src="complex-diagram.png" alt="Workflow diagram" 
     aria-describedby="diagram-desc">
<div id="diagram-desc" class="sr-only">
  Detailed description of the workflow...
</div>

<!-- SVG icons -->
<svg role="img" aria-label="Close">
  <use href="#icon-close">
</svg>
```

**Media**
```html
<!-- Video with captions -->
<video controls>
  <source src="video.mp4" type="video/mp4">
  <track kind="captions" src="captions.vtt" srclang="en" label="English">
  <track kind="descriptions" src="descriptions.vtt" srclang="en">
</video>

<!-- Audio with transcript -->
<audio controls>
  <source src="podcast.mp3" type="audio/mpeg">
</audio>
<a href="transcript.html">Read transcript</a>
```

### Color and Contrast

**Contrast Requirements**
- Normal text: 4.5:1 ratio
- Large text (18pt+): 3:1 ratio
- UI components: 3:1 ratio

```css
/* ✅ Good: Sufficient contrast */
.text {
  color: #333; /* Dark gray on white: 12.6:1 */
}

.button {
  background: #0066cc;
  color: #ffffff; /* 4.6:1 */
}

/* Don't rely on color alone */
.error {
  color: #d32f2f;
}
.error::before {
  content: "✕ "; /* Visual indicator */
}
```

### Testing

**Automated Testing**
```bash
# axe-core CLI
axe https://example.com

# Lighthouse CI
lighthouse https://example.com --only-categories=accessibility

# Pa11y
pa11y https://example.com
```

**Manual Testing**
- Keyboard-only navigation (Tab, Enter, Space, Arrow keys)
- Screen reader testing (NVDA, VoiceOver, JAWS)
- Zoom to 200% and 400%
- Color contrast analyzer

## Examples

See the `examples/` directory for:
- `accessible-components/` - ARIA-compliant components
- `form-patterns/` - Accessible form implementations
- `focus-management/` - Focus handling utilities
- `testing-checklist.md` - Accessibility testing checklist

## References

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [WebAIM](https://webaim.org/)
- [A11y Project](https://www.a11yproject.com/)
- [axe DevTools](https://www.deque.com/axe/)
