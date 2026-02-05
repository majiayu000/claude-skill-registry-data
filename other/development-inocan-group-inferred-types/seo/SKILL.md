---
name: seo
description: Generate SEO-optimized code snippets for websites. Use when asked to optimize SEO, generate meta tags, create structured data (JSON-LD/schema.org), fix heading hierarchy, or audit page SEO. Outputs implementation-ready code for handoff to developers. Supports multilingual sites (Ukrainian/English) and industry-specific schemas for construction equipment, aquaculture, and engineering services.
---

# SEO Optimization Skill

Generate implementation-ready SEO code snippets. Analyze content first, then output clean code suitable for developer handoff.

## Workflow

1. **Analyze** — Examine provided content/URL to identify SEO gaps
2. **Recommend** — Determine which elements need optimization
3. **Generate** — Output copy-paste ready code snippets
4. **Format** — Structure output for coder agent implementation

## Core Outputs

### Meta Tags

Generate complete meta tag sets. Always include:

```html
<!-- Primary Meta Tags -->
<title>{60 chars max, keyword-front-loaded}</title>
<meta name="description" content="{150-160 chars, compelling, includes CTA}">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical URL}">
<meta property="og:title" content="{same as title or slightly varied}">
<meta property="og:description" content="{same as meta description}">
<meta property="og:image" content="{1200x630px image URL}">
<meta property="og:locale" content="uk_UA">
<meta property="og:locale:alternate" content="en_US">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{image URL}">

<!-- Canonical -->
<link rel="canonical" href="{canonical URL}">
```

### Multilingual SEO (hreflang)

For Ukrainian/English sites:

```html
<link rel="alternate" hreflang="uk" href="https://example.com/uk/page">
<link rel="alternate" hreflang="en" href="https://example.com/en/page">
<link rel="alternate" hreflang="x-default" href="https://example.com/en/page">
```

Rules:
- x-default points to primary language (usually English for international audience)
- Self-referencing hreflang required on each language version
- Use country codes when targeting specific regions: uk-UA, en-US, en-GB

### Structured Data (JSON-LD)

Always output as complete script block. See references/schemas.md for full schema templates.

**Organization** (homepage/about):
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "",
  "url": "",
  "logo": "",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "",
    "contactType": "customer service",
    "availableLanguage": ["Ukrainian", "English"]
  },
  "sameAs": []
}
</script>
```

**Product** (equipment pages):
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "",
  "description": "",
  "image": [],
  "brand": {"@type": "Brand", "name": ""},
  "offers": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "price": "",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```

**Service** (service pages):
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "",
  "description": "",
  "provider": {"@type": "Organization", "name": ""},
  "areaServed": {"@type": "Country", "name": ""},
  "serviceType": ""
}
</script>
```

### Heading Hierarchy

Analyze and fix heading structure:
- Single H1 per page (contains primary keyword)
- H2s for main sections
- H3-H6 for subsections (no skipping levels)

Output format:
```
Current: H1 → H2 → H4 [ISSUE: skipped H3]
Fixed:   H1 → H2 → H3
```

## Output Format for Coder Agent

```markdown
## SEO: [Page Name]

### Meta Tags
\`\`\`html
[complete meta tag block]
\`\`\`

### Structured Data
\`\`\`html
[complete JSON-LD script]
\`\`\`

### Heading Changes
- Line X: Change H4 to H3
- Line Y: Update H1 to include keyword

### Notes
- [critical implementation details only]
```

## Industry Keywords

**Construction/Heavy Machinery**: excavator, loader, bulldozer, crane, hydraulic, specifications, model, manufacturer, condition, warranty

**Aquaculture**: RAS, recirculating aquaculture, fish farming, water treatment, hatchery, fingerlings, biomass, feeding systems

**Engineering Services**: feasibility study, project design, technical consulting, implementation, commissioning, optimization

## Quality Rules

- Title: ≤60 characters, keyword first
- Description: 150-160 characters, include CTA
- JSON-LD: valid syntax, no trailing commas
- hreflang: bidirectional references
- Headings: single H1, no level skips
- Canonical: absolute URL
- OG image: 1200x630px
