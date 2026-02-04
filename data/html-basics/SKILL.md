---
name: html-basics
description: Core HTML5 elements, document structure, and foundational markup patterns
sasmp_version: "1.3.0"
bonded_agent: html-expert
bond_type: PRIMARY_BOND
version: "2.0.0"

# Skill Metadata
category: markup
complexity: foundational
dependencies: []

# Parameter Validation
parameters:
  element_type:
    type: string
    required: true
    enum: [document, text, grouping, embedded, interactive, metadata]
  output_format:
    type: string
    default: "html"
    enum: [html, jsx, template]
  include_comments:
    type: boolean
    default: false

# Retry Configuration
retry:
  max_attempts: 3
  backoff_ms: [1000, 2000, 4000]
  retryable_errors: [NETWORK_ERROR, TIMEOUT]
---

# HTML Basics Skill

Core HTML5 elements and document structure patterns for production web development.

## 🎯 Purpose

Provide atomic, single-responsibility operations for:
- Document structure creation (`<!DOCTYPE>`, `<html>`, `<head>`, `<body>`)
- Text content elements (`<p>`, `<h1>`-`<h6>`, `<blockquote>`)
- Grouping content (`<div>`, `<main>`, `<section>`)
- Embedded content (`<img>`, `<iframe>`, `<video>`)
- Metadata elements (`<meta>`, `<link>`, `<title>`)

---

## 📥 Input Schema

```typescript
interface HtmlBasicsInput {
  operation: 'create' | 'validate' | 'convert' | 'explain';
  element_type: ElementCategory;
  content?: string;
  attributes?: Record<string, string>;
  options?: {
    doctype?: 'html5' | 'xhtml';
    lang?: string;           // Default: 'en'
    charset?: string;        // Default: 'UTF-8'
  };
}

type ElementCategory =
  | 'document'    // html, head, body, doctype
  | 'text'        // p, h1-h6, span, strong, em
  | 'grouping'    // div, main, section, article
  | 'embedded'    // img, video, audio, iframe
  | 'interactive' // a, button, details
  | 'metadata';   // meta, link, title, base
```

## 📤 Output Schema

```typescript
interface HtmlBasicsOutput {
  success: boolean;
  markup: string;
  validation: {
    valid: boolean;
    errors: string[];
    warnings: string[];
  };
  metadata?: {
    element_count: number;
    nesting_depth: number;
    has_required_attrs: boolean;
  };
}
```

---

## 🛠️ Core Operations

### 1. Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
</head>
<body>
  <!-- Content here -->
</body>
</html>
```

**Required Elements Checklist:**
- [ ] `<!DOCTYPE html>` declaration
- [ ] `<html lang="...">` with language attribute
- [ ] `<meta charset="UTF-8">`
- [ ] `<meta name="viewport">` for responsive design
- [ ] `<title>` element (60 chars max for SEO)

### 2. Text Content Elements

| Element | Purpose | Example |
|---------|---------|---------|
| `<h1>`-`<h6>` | Headings (one h1 per page) | `<h1>Main Title</h1>` |
| `<p>` | Paragraph text | `<p>Content...</p>` |
| `<strong>` | Strong importance | `<strong>Important</strong>` |
| `<em>` | Stress emphasis | `<em>emphasized</em>` |
| `<mark>` | Highlighted text | `<mark>highlighted</mark>` |
| `<blockquote>` | Extended quotation | `<blockquote cite="...">` |
| `<code>` | Code snippet | `<code>console.log()</code>` |
| `<pre>` | Preformatted text | `<pre>  formatted  </pre>` |

### 3. Grouping Elements

| Element | Purpose | When to Use |
|---------|---------|-------------|
| `<div>` | Generic container | No semantic meaning needed |
| `<main>` | Primary content | Once per page, unique content |
| `<section>` | Thematic grouping | With heading, related content |
| `<article>` | Self-contained | Blog post, news article |
| `<aside>` | Tangential content | Sidebars, callouts |

### 4. Embedded Content

```html
<!-- Image with required attributes -->
<img src="photo.jpg" alt="Description" width="800" height="600" loading="lazy">

<!-- Responsive image -->
<picture>
  <source media="(min-width: 800px)" srcset="large.jpg">
  <source media="(min-width: 400px)" srcset="medium.jpg">
  <img src="small.jpg" alt="Description">
</picture>

<!-- Video with fallback -->
<video controls width="640" height="360">
  <source src="video.mp4" type="video/mp4">
  <source src="video.webm" type="video/webm">
  <p>Your browser doesn't support video.</p>
</video>
```

---

## ⚠️ Error Handling

### Validation Errors

| Error Code | Description | Auto-Fix |
|------------|-------------|----------|
| `HB001` | Missing DOCTYPE | Add `<!DOCTYPE html>` |
| `HB002` | Missing lang attribute | Add `lang="en"` |
| `HB003` | Missing charset | Add `<meta charset="UTF-8">` |
| `HB004` | Missing alt on img | Prompt for alt text |
| `HB005` | Empty heading | Flag for content |
| `HB006` | Invalid nesting | Restructure elements |

### Recovery Procedures

```
Error Detected → Log Issue → Attempt Auto-Fix → Validate → Report
        ↓
   [If unfixable]
        ↓
   Return error with suggestion
```

---

## 🔍 Troubleshooting

### Problem: Page not rendering correctly

```
Debug Checklist:
□ DOCTYPE present and first line?
□ HTML tag has lang attribute?
□ Head contains charset meta?
□ All tags properly closed?
□ No duplicate IDs?
□ Valid nesting structure?
```

### Problem: Images not loading

```
Debug Checklist:
□ File path correct (relative/absolute)?
□ File exists at location?
□ Correct file extension?
□ Server MIME types configured?
□ Alt attribute present?
```

### Problem: Content not accessible

```
Debug Checklist:
□ Heading hierarchy correct?
□ Landmarks present (main, nav)?
□ Images have alt text?
□ Links have descriptive text?
□ Language attribute set?
```

---

## 📊 Quality Metrics

| Metric | Target | Tool |
|--------|--------|------|
| Valid HTML | 0 errors | W3C Validator |
| Nesting depth | ≤6 levels | html-validate |
| Required attrs | 100% | Custom linter |
| Semantic ratio | >70% | Manual audit |

---

## 📋 Usage Examples

```yaml
# Create document structure
skill: html-basics
operation: create
element_type: document
options:
  lang: "en"
  charset: "UTF-8"

# Validate existing markup
skill: html-basics
operation: validate
content: "<div><p>Test</div></p>"  # Will catch nesting error

# Convert to JSX
skill: html-basics
operation: convert
element_type: text
content: "<p class='intro'>Hello</p>"
output_format: jsx  # Returns: <p className="intro">Hello</p>
```

---

## 🔗 References

- [MDN HTML Elements Reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Element)
- [HTML Living Standard](https://html.spec.whatwg.org/multipage/)
- [W3C HTML Validator](https://validator.w3.org/)
