---
name: accessibility-checker
description: Ensure WCAG2AA accessibility compliance. Use when creating forms, adding images, building navigation, creating interactive elements, or any user-facing HTML content.
allowed-tools: Read, Write, Edit
---

# Accessibility Checker Skill

This skill ensures all HTML content meets WCAG2AA accessibility standards.

## Quick Reference

| Element | Requirement |
|---------|-------------|
| Images | Must have `alt` attribute |
| Form inputs | Must have associated `<label>` |
| Links | Must have descriptive text (not "click here") |
| Navigation | Use `<nav>` with `aria-label` |
| Main content | Use `<main>` with `id` for skip link |
| Headings | Follow hierarchy (h1 → h2 → h3) |
| Tables | Use `<th scope="col/row">` |

## Forms (MUST follow)

Every input MUST have a label:

```html
<!-- Method 1: for/id association -->
<label for="email">Email Address</label>
<input type="email" id="email" name="email"/>

<!-- Method 2: wrapping -->
<label>
  Email Address
  <input type="email" name="email"/>
</label>
```

Use fieldset for related inputs:

```html
<fieldset>
  <legend>Shipping Address</legend>
  <label for="street">Street</label>
  <input type="text" id="street" name="street"/>
  <label for="city">City</label>
  <input type="text" id="city" name="city"/>
</fieldset>
```

## Images (MUST follow)

All images MUST have alt text:

```html
<!-- Informative image -->
<img src="chart.png" alt="Sales increased 20% in Q4"/>

<!-- Decorative image (empty alt) -->
<img src="decoration.png" alt=""/>

<!-- Complex image (use figure) -->
<figure>
  <img src="diagram.png" alt="System architecture diagram"/>
  <figcaption>Figure 1: Three-tier architecture with load balancer</figcaption>
</figure>
```

## Navigation (MUST follow)

Provide skip links and landmarks:

```html
<body>
  <a href="#main" class="skip-link">Skip to main content</a>

  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>

  <main id="main">
    <!-- Content -->
  </main>
</body>
```

## Links (MUST follow)

Links need descriptive, unique text:

```html
<!-- Bad -->
<a href="/products">Click here</a>
<a href="/docs">Read more</a>

<!-- Good -->
<a href="/products">View all products</a>
<a href="/docs">Read the documentation</a>
```

## Headings

Follow logical hierarchy:

```html
<h1>Page Title</h1>
  <h2>Section One</h2>
    <h3>Subsection</h3>
  <h2>Section Two</h2>
```

Never skip levels (h1 → h3 is wrong).

## WCAG AAA Enhanced Accessibility (Optional)

WCAG AAA provides enhanced accessibility beyond the AA baseline. Use when targeting users with more significant accessibility needs.

### Contrast Requirements

| Level | Normal Text | Large Text |
|-------|-------------|------------|
| AA (default) | 4.5:1 | 3:1 |
| AAA (enhanced) | 7:1 | 4.5:1 |

Large text is 18pt+ (24px) or 14pt+ bold (18.5px).

### Enabling AAA in pa11y

Edit `.pa11yci` to use AAA standard:

```json
{
  "defaults": {
    "standard": "WCAG2AAA",
    "timeout": 30000,
    "wait": 1000
  }
}
```

### AAA-Specific Requirements

| Requirement | AAA Criterion |
|-------------|---------------|
| 7:1 contrast ratio | 1.4.6 Contrast (Enhanced) |
| No images of text | 1.4.9 Images of Text (No Exception) |
| Sign language for video | 1.2.6 Sign Language |
| Extended audio description | 1.2.7 Extended Audio Description |
| Live captions | 1.2.9 Audio-only (Live) |
| Reading level (lower secondary) | 3.1.5 Reading Level |
| Pronunciation help | 3.1.6 Pronunciation |
| Context-sensitive help | 3.3.5 Help |
| Error prevention (all) | 3.3.6 Error Prevention (All) |

### CSS for AAA Contrast

```css
:root {
  /* AAA-compliant color pairs */
  --text-color: #1a1a1a;        /* On white: 16.1:1 */
  --text-muted: #525252;        /* On white: 7.1:1 */
  --background: #ffffff;

  /* Links need 3:1 contrast against surrounding text */
  --link-color: #0047ab;        /* On white: 8.5:1 */
}

/* High contrast mode support */
@media (prefers-contrast: more) {
  :root {
    --text-color: #000000;
    --background: #ffffff;
    --border-color: #000000;
  }
}
```

### When to Use AAA

| Scenario | Recommendation |
|----------|----------------|
| Government/public services | Consider AAA |
| Healthcare applications | Consider AAA |
| Educational content | Consider AAA |
| Elderly user base | Consider AAA |
| Legal requirements | Check jurisdiction |
| General websites | AA is sufficient |

### Partial AAA Adoption

You can adopt specific AAA criteria without full compliance:

```json
{
  "defaults": {
    "standard": "WCAG2AA",
    "rules": [
      "WCAG2AAA.Principle1.Guideline1_4.1_4_6"
    ]
  }
}
```

### Testing AAA Compliance

```bash
# Run with AAA standard
npx pa11y --standard WCAG2AAA src/index.html

# Check specific criterion
npx pa11y --standard WCAG2AAA --include-notices src/index.html
```

See [FORMS.md](FORMS.md), [IMAGES.md](IMAGES.md), [NAVIGATION.md](NAVIGATION.md) for details.

## Related Skills

- **xhtml-author** - Write valid XHTML-strict HTML5 markup
- **forms** - HTML-first form patterns with CSS-only validation
- **custom-elements** - Define and use custom HTML elements
- **i18n** - Write internationalization-friendly HTML pages
