---
name: semantic-html
description: Semantic HTML5 markup patterns for meaningful, accessible, and SEO-optimized content structure
sasmp_version: "1.3.0"
bonded_agent: html-expert
bond_type: PRIMARY_BOND
version: "2.0.0"

# Skill Metadata
category: semantics
complexity: intermediate
dependencies:
  - html-basics

# Parameter Validation
parameters:
  content_type:
    type: string
    required: true
    enum: [article, navigation, sidebar, header, footer, section, figure, list, table]
  semantic_level:
    type: string
    default: "strict"
    enum: [strict, moderate, minimal]
  include_landmarks:
    type: boolean
    default: true

# Retry Configuration
retry:
  max_attempts: 3
  backoff_ms: [1000, 2000, 4000]
  retryable_errors: [PARSE_ERROR, VALIDATION_ERROR]
---

# Semantic HTML Skill

Transform markup from presentation-focused to meaning-focused, enabling accessibility, SEO, and AI/voice interface compatibility.

## 🎯 Purpose

Provide atomic, single-responsibility operations for:
- Document outline and structure semantics
- Content sectioning (`<article>`, `<section>`, `<nav>`)
- Landmark roles and ARIA mapping
- Microdata and structured data hints
- SEO and accessibility improvements

---

## 📥 Input Schema

```typescript
interface SemanticHtmlInput {
  operation: 'analyze' | 'convert' | 'validate' | 'suggest';
  content_type: ContentType;
  markup?: string;           // Existing HTML to analyze/convert
  context?: {
    page_type: 'homepage' | 'article' | 'product' | 'contact' | 'search';
    has_sidebar: boolean;
    has_comments: boolean;
  };
  options?: {
    semantic_level: 'strict' | 'moderate' | 'minimal';
    include_landmarks: boolean;
    preserve_classes: boolean;
  };
}

type ContentType =
  | 'article'     // Blog post, news article
  | 'navigation'  // Nav menus, breadcrumbs
  | 'sidebar'     // Aside content
  | 'header'      // Page/section headers
  | 'footer'      // Page/section footers
  | 'section'     // Generic thematic sections
  | 'figure'      // Images, diagrams, code blocks
  | 'list'        // Lists of items
  | 'table';      // Tabular data
```

## 📤 Output Schema

```typescript
interface SemanticHtmlOutput {
  success: boolean;
  markup: string;
  semantic_score: number;      // 0-100
  improvements: Improvement[];
  landmark_map: LandmarkMap;
  outline: DocumentOutline;
}

interface Improvement {
  original: string;
  suggested: string;
  reason: string;
  impact: 'critical' | 'high' | 'medium' | 'low';
}
```

---

## 🛠️ Core Operations

### 1. Semantic Element Selection

```
┌─────────────────────────────────────────────────────────────┐
│                    Semantic Element Decision Tree            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Is it the main content?                                     │
│  └── Yes → <main>                                            │
│  └── No ↓                                                    │
│                                                              │
│  Is it independently distributable?                          │
│  └── Yes → <article>                                         │
│  └── No ↓                                                    │
│                                                              │
│  Is it a thematic grouping with a heading?                   │
│  └── Yes → <section>                                         │
│  └── No ↓                                                    │
│                                                              │
│  Is it navigation links?                                     │
│  └── Yes → <nav>                                             │
│  └── No ↓                                                    │
│                                                              │
│  Is it tangentially related content?                         │
│  └── Yes → <aside>                                           │
│  └── No ↓                                                    │
│                                                              │
│  Is it introductory or navigational content?                 │
│  └── Yes → <header>                                          │
│  └── No ↓                                                    │
│                                                              │
│  Is it footer/meta information?                              │
│  └── Yes → <footer>                                          │
│  └── No → <div>                                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2. Landmark Mapping

| HTML5 Element | ARIA Landmark Role | Implicit Role |
|---------------|-------------------|---------------|
| `<header>` (page) | `banner` | Yes |
| `<nav>` | `navigation` | Yes |
| `<main>` | `main` | Yes |
| `<aside>` | `complementary` | Yes |
| `<footer>` (page) | `contentinfo` | Yes |
| `<section>` | `region` | If has accessible name |
| `<article>` | `article` | Yes |
| `<form>` | `form` | If has accessible name |

### 3. Page Structure Patterns

#### Blog/Article Page

```html
<body>
  <header>
    <nav aria-label="Main">...</nav>
  </header>

  <main>
    <article>
      <header>
        <h1>Article Title</h1>
        <p>By <a rel="author" href="/author">Author</a></p>
        <time datetime="2025-01-15">January 15, 2025</time>
      </header>

      <section aria-labelledby="intro">
        <h2 id="intro">Introduction</h2>
        <p>Content...</p>
      </section>

      <section aria-labelledby="main-content">
        <h2 id="main-content">Main Content</h2>
        <p>Content...</p>
      </section>

      <footer>
        <p>Tags: <a href="/tag/html" rel="tag">HTML</a></p>
      </footer>
    </article>

    <aside aria-label="Related articles">
      <h2>Related Articles</h2>
      <ul>...</ul>
    </aside>
  </main>

  <footer>
    <nav aria-label="Footer">...</nav>
    <p>&copy; 2025</p>
  </footer>
</body>
```

#### E-commerce Product Page

```html
<body>
  <header>
    <nav aria-label="Main">...</nav>
    <nav aria-label="Breadcrumb">
      <ol>
        <li><a href="/">Home</a></li>
        <li><a href="/products">Products</a></li>
        <li><a href="/products/widgets" aria-current="page">Widget</a></li>
      </ol>
    </nav>
  </header>

  <main>
    <article itemscope itemtype="https://schema.org/Product">
      <h1 itemprop="name">Product Name</h1>

      <figure>
        <img itemprop="image" src="product.jpg" alt="Product description">
      </figure>

      <section aria-labelledby="description">
        <h2 id="description">Description</h2>
        <p itemprop="description">Product details...</p>
      </section>

      <section aria-labelledby="pricing">
        <h2 id="pricing">Pricing</h2>
        <p itemprop="offers" itemscope itemtype="https://schema.org/Offer">
          <span itemprop="price" content="29.99">$29.99</span>
        </p>
      </section>
    </article>

    <aside aria-label="Related products">
      <h2>You May Also Like</h2>
      <ul>...</ul>
    </aside>
  </main>

  <footer>...</footer>
</body>
```

---

## ⚠️ Error Handling

### Error Codes

| Code | Description | Recovery |
|------|-------------|----------|
| `SH001` | Missing document outline | Add proper heading hierarchy |
| `SH002` | No main landmark | Wrap primary content in `<main>` |
| `SH003` | Multiple main elements | Keep only one `<main>` |
| `SH004` | Section without heading | Add heading or use `<div>` |
| `SH005` | Article without heading | Add `<h1>`-`<h6>` |
| `SH006` | Nav without label | Add `aria-label` |
| `SH007` | Div soup detected | Suggest semantic alternatives |

### Recovery Procedures

```
Analyze Input → Identify Anti-Patterns → Suggest Fixes → Validate → Report
       ↓
 [If conversion requested]
       ↓
 Apply automatic fixes → Re-validate → Return improved markup
```

---

## 🔍 Troubleshooting

### Problem: Screen reader announces wrong structure

```
Debug Checklist:
□ Is <main> present and unique?
□ Are headings in logical order (h1→h2→h3)?
□ Do sections have accessible names?
□ Are nav elements labeled uniquely?
□ Is banner/contentinfo outside main?
```

### Problem: SEO not picking up content structure

```
Debug Checklist:
□ Is <article> used for main content?
□ Is author/date marked with rel/datetime?
□ Are headings used (not just styled divs)?
□ Is structured data (schema.org) present?
□ Are images in <figure> with <figcaption>?
```

### Problem: "Div soup" - too many divs

```
Conversion Guide:
<div class="header">      → <header>
<div class="nav">         → <nav>
<div class="main">        → <main>
<div class="article">     → <article>
<div class="sidebar">     → <aside>
<div class="footer">      → <footer>
<div class="section">     → <section>
<div class="figure">      → <figure>
```

---

## 📊 Semantic Score Calculation

| Factor | Weight | Measurement |
|--------|--------|-------------|
| Landmark coverage | 25% | banner, main, contentinfo present |
| Heading hierarchy | 25% | Correct h1→h6 nesting |
| Semantic ratio | 20% | semantic / (semantic + div + span) |
| Accessible names | 15% | Labeled sections and navs |
| Article structure | 15% | Proper article markup |

**Score Interpretation:**
- 90-100: Excellent semantic structure
- 70-89: Good, minor improvements possible
- 50-69: Moderate, significant improvements needed
- <50: Poor, major restructuring required

---

## 📋 Usage Examples

```yaml
# Analyze existing markup
skill: semantic-html
operation: analyze
markup: "<div class='main'><div class='post'>...</div></div>"

# Convert to semantic HTML
skill: semantic-html
operation: convert
content_type: article
markup: "<div class='blog-post'>...</div>"
options:
  semantic_level: strict
  include_landmarks: true

# Suggest improvements
skill: semantic-html
operation: suggest
content_type: navigation
context:
  page_type: homepage
  has_sidebar: true
```

---

## 🔗 References

- [MDN Semantic HTML](https://developer.mozilla.org/en-US/docs/Glossary/Semantics#semantics_in_html)
- [HTML Living Standard - Sections](https://html.spec.whatwg.org/multipage/sections.html)
- [W3C Using ARIA Landmarks](https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/)
- [Schema.org](https://schema.org/)
