---
name: seo-guidelines
description: |
  Load when optimizing content for search engines, performing keyword research,
  writing meta tags, analyzing SEO performance, or any task related to organic
  search visibility. Contains comprehensive SEO best practices for 2024-2025.
---

# SEO Guidelines Skill

## Core Philosophy

> "The best SEO is creating content so valuable that people want to link to it."

SEO in 2024-2025 is about user intent, quality content, and technical excellence. Search engines prioritize content that genuinely helps users over content optimized purely for algorithms.

## Fundamental Principles

### 1. User Intent First
- Understand what the searcher actually wants
- Match content format to intent (informational, transactional, navigational)
- Answer the question completely, then add value

### 2. E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)
- **Experience**: Show first-hand experience with the topic
- **Expertise**: Demonstrate deep knowledge
- **Authoritativeness**: Build reputation in your niche
- **Trustworthiness**: Be accurate, cite sources, be transparent

### 3. Mobile-First
- Google uses mobile-first indexing
- Test all content on mobile devices
- Ensure fast load times on mobile networks
- Use responsive design

## Keyword Research

### Types of Keywords

| Type | Description | Example | Competition |
|------|-------------|---------|-------------|
| Head | 1-2 words, broad | "python" | Very High |
| Body | 2-3 words, moderate | "python tutorial" | High |
| Long-tail | 4+ words, specific | "python pandas groupby tutorial beginners" | Lower |

### Intent Classification

```
Informational: "how to", "what is", "guide", "tutorial"
  → Create educational content, how-tos, guides

Navigational: "[brand name]", "[product] login"
  → Ensure brand pages are optimized

Transactional: "buy", "price", "download", "subscribe"
  → Optimize conversion pages, CTAs

Commercial Investigation: "best", "review", "comparison", "vs"
  → Create comparison content, reviews
```

### Spanish Keyword Research

For tacosdedatos, consider:

```
Regional Variations:
- Mexico: "tutorial de python", "cómo usar pandas"
- Spain: "curso de python", "aprende pandas"
- Argentina: "guía de python", "pandas para principiantes"

Common Spanish Search Patterns:
- "qué es [concepto]" (what is)
- "cómo [hacer algo]" (how to)
- "tutorial de [tecnología]" (tutorial for)
- "guía de [tema]" (guide to)
- "[herramienta] en español" (tool in Spanish)
```

### Keyword Research Process

1. **Seed Keywords**: Start with your core topics
2. **Expand**: Use tools (Ahrefs, Semrush) to find related keywords
3. **Analyze**: Check search volume, difficulty, and intent
4. **Prioritize**: Balance volume with competition
5. **Map**: Assign keywords to specific content pieces

### Recommended Tools

| Tool | Best For | Notes |
|------|----------|-------|
| Ahrefs | Deep analysis, historical data | Paid, comprehensive |
| Semrush | Competitor analysis | Paid, excellent for competitors |
| Google Search Console | Your own data | Free, essential |
| AnswerThePublic | Question-based keywords | Free tier available |
| Google Trends | Trending topics | Free, great for timing |

## On-Page SEO

### Title Tags

**Best Practices:**
- 15-60 characters (optimal: 15-40 for higher CTR)
- Primary keyword front-loaded
- Compelling for humans, not just search engines
- Unique for every page

**Format Templates:**
```
Tutorial: [Primary Keyword]: Tutorial Completo [Año]
Guide: Guía de [Topic]: [Benefit] | tacosdedatos
List: [Number] [Topic] que Debes Conocer en [Year]
How-to: Cómo [Action] con [Tool] - Paso a Paso
```

**Examples:**
```
✅ "Pandas GroupBy: Tutorial Completo con Ejemplos (2024)"
✅ "Cómo Visualizar Datos en Python: Guía para Principiantes"
❌ "Python Tutorial" (too vague)
❌ "The Complete Ultimate Comprehensive Guide to Learning Python Programming for Data Science" (too long)
```

### Meta Descriptions

**Best Practices:**
- 150-160 characters (avoid truncation)
- Include primary keyword naturally
- Compelling call-to-action
- Unique for every page
- Note: Google rewrites ~63% of meta descriptions

**Format Template:**
```
Aprende [topic] con este [type] completo. [Benefit]. [CTA: Incluye ejemplos, código, etc.]
```

**Examples:**
```
✅ "Domina pandas groupby en 15 minutos. Tutorial práctico con ejemplos de código que puedes copiar. Incluye casos de uso reales y errores comunes."

❌ "Este es un tutorial de pandas. Haz clic aquí para aprender más."
```

### Heading Structure

**Hierarchy:**
```html
<h1>Main Title (Only One per Page)</h1>
  <h2>Major Section</h2>
    <h3>Subsection</h3>
      <h4>Detail</h4>
    <h3>Another Subsection</h3>
  <h2>Another Major Section</h2>
```

**Best Practices:**
- One H1 per page (usually the title)
- Use H2 for main sections
- Include keywords naturally
- Make headings scannable
- Use for structure, not styling

### URL Structure

**Best Practices:**
```
✅ /tutorial/pandas-groupby-ejemplos
✅ /guia/visualizacion-datos-python
❌ /post?id=12345
❌ /2024/01/15/mi-nuevo-tutorial-de-pandas-para-principiantes-en-espanol
```

**Rules:**
- Use hyphens, not underscores
- Keep short and descriptive
- Include primary keyword
- Use lowercase
- Avoid dates unless necessary
- Remove stop words when possible

### Content Optimization

**Structure for SEO:**
```markdown
# Primary Keyword in H1

Brief intro paragraph with **primary keyword** in first 100 words.

## H2 with Secondary Keyword

Content answering user intent...

### H3 for Details

More specific information...

## H2 with Another Angle

[Continue pattern...]

## Conclusión / Próximos Pasos

Summary and call-to-action.
```

**Content Checklist:**
- [ ] Primary keyword in title, H1, first paragraph
- [ ] Secondary keywords in H2s
- [ ] Natural keyword usage (no stuffing)
- [ ] Comprehensive coverage of topic
- [ ] Internal links to related content
- [ ] External links to authoritative sources
- [ ] Images with alt text
- [ ] Code blocks properly formatted
- [ ] Minimum 1,500 words for comprehensive topics

### Image Optimization

**Checklist:**
- [ ] Descriptive file names (`pandas-groupby-example.png`, not `image1.png`)
- [ ] Alt text describing the image
- [ ] Compressed for web (WebP format preferred)
- [ ] Appropriate dimensions (don't use CSS to resize)
- [ ] Lazy loading for below-fold images

**Alt Text Examples:**
```
✅ alt="Gráfico de barras mostrando ventas por categoría usando pandas"
❌ alt="image"
❌ alt="pandas python data science visualization chart graph tutorial example"
```

### Internal Linking

**Strategy:**
- Link to related content naturally
- Use descriptive anchor text (not "click here")
- Prioritize links to important pages
- Keep a reasonable number (not excessive)
- Create topic clusters

**Example:**
```markdown
✅ "Para más detalles, consulta nuestro [tutorial de visualización con matplotlib](/tutorial/matplotlib-basico)."

❌ "Haz [clic aquí](/tutorial/matplotlib-basico) para más información."
```

## Technical SEO

### Core Web Vitals

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤2.5s | ≤4s | >4s |
| FID (First Input Delay) | ≤100ms | ≤300ms | >300ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | ≤0.25 | >0.25 |

### Schema Markup

**Essential Schema Types for Technical Content:**

```json
// Article schema
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "Pandas GroupBy: Tutorial Completo",
  "author": {
    "@type": "Person",
    "name": "Sergio Sánchez"
  },
  "datePublished": "2024-01-15",
  "dateModified": "2024-06-01",
  "publisher": {
    "@type": "Organization",
    "name": "tacosdedatos"
  }
}
```

```json
// HowTo schema for tutorials
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "Cómo hacer groupby en pandas",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Importar pandas",
      "text": "Primero importa la librería pandas..."
    }
  ]
}
```

```json
// FAQ schema
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "¿Qué es pandas groupby?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "pandas groupby es una función que..."
    }
  }]
}
```

### Robots.txt and Sitemap

**robots.txt:**
```
User-agent: *
Allow: /

Sitemap: https://tacosdedatos.com/sitemap.xml
```

**Sitemap Requirements:**
- Include all important pages
- Update when content changes
- Priority for key pages
- Submit to Google Search Console

### HTTPS and Security

- Always use HTTPS
- Redirect HTTP to HTTPS
- Ensure all resources load over HTTPS
- Security headers (HSTS, CSP)

## SEO Audit Checklist

### Quick Audit

```markdown
## Page: [URL]

### Title & Meta
- [ ] Title tag present and optimized (15-60 chars)
- [ ] Meta description present (150-160 chars)
- [ ] Primary keyword in both

### Content
- [ ] H1 present and matches title
- [ ] Heading hierarchy correct
- [ ] Primary keyword in first 100 words
- [ ] Content length appropriate for topic
- [ ] Internal links present
- [ ] External links to authoritative sources

### Technical
- [ ] URL is clean and descriptive
- [ ] Page loads in <3 seconds
- [ ] Mobile-friendly
- [ ] Images have alt text
- [ ] Schema markup present

### Issues Found
1. [Issue]: [Recommendation]
2. [Issue]: [Recommendation]
```

## Output Format for SEO Analysis

When analyzing content for SEO:

```markdown
# SEO Analysis: [Title]

**URL**: [Proposed/Current URL]
**Target Keyword**: [Primary keyword]
**Search Intent**: Informational / Commercial / Transactional

## Score: X/10

### Title Tag
**Current**: [Current title]
**Recommended**: [Optimized title]
**Character count**: X/60

### Meta Description
**Current**: [Current description]
**Recommended**: [Optimized description]
**Character count**: X/160

### Content Optimization
- Primary keyword density: X%
- Secondary keywords found: [list]
- Word count: X (recommended: Y)
- Heading structure: ✅/⚠️/❌

### Technical Issues
- [ ] [Issue and fix]

### Recommendations
1. **High Priority**: [Recommendation]
2. **Medium Priority**: [Recommendation]
3. **Nice to Have**: [Recommendation]
```

## Resources

- [Google Search Central](https://developers.google.com/search)
- [Backlinko SEO Guide](https://backlinko.com/on-page-seo)
- [Moz Beginner's Guide](https://moz.com/beginners-guide-to-seo)
- [Ahrefs Blog](https://ahrefs.com/blog/)
- [Search Engine Land](https://searchengineland.com/)
