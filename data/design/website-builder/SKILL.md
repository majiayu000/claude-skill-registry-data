---
name: website-builder
description: Complete SEO-optimized website creation workflow orchestrator. Coordinates SEO analysis (keywords, competitors), sitemap planning, shadcn component selection, theme application, and content optimization. Use when building websites, creating landing pages, designing web interfaces, optimizing for search engines, planning site architecture, or requesting homepage/website builds with SEO considerations.
version: 1.0.0
dependencies: sitemap-analyst agent, shadcn-ui-blocks skill, shadcn-ui-theme skill, shadcn-website-builder agent, WebFetch
allowed-tools: Read,Write,Edit,Bash,WebFetch
---

# SEO-Optimized Website Builder

Orchestrates complete website creation workflow: SEO analysis → sitemap planning → component selection → theme application → SEO integration → verification.

---

## 5-Step Workflow

### Step 1: SEO Analysis
**Create SEO research foundation (if nothing specified by user):**

1. Create `/planning/seo/` directory
2. Analyze target website (if provided via WebFetch):
   - Extract current SEO metadata
   - Identify primary/secondary keywords
   - Analyze page structure, headings, content
3. Create `/planning/seo/analysis.md`:
   - Current state assessment
   - SEO audit findings
   - Key opportunities
4. Create `/planning/seo/keywords.md`:
   - Primary keywords (search volume, difficulty)
   - Secondary keywords
   - Long-tail variations
   - Keyword mapping to pages
5. Create `/planning/seo/competitors.md`:
   - Top 3-5 competitors
   - Their keyword focus
   - Content gaps you can fill
   - Unique positioning strategy

**Use WebFetch when user provides target URL:**
```
Fetch: <user-provided-url>
Prompt: "Extract SEO metadata, primary keywords, page structure, content themes"
```

### Step 2: Sitemap Creation
**Delegate to sitemap-analyst agent:**

Call sitemap-analyst with:
- Business goals (from user or inferred)
- Target audience personas
- Primary conversion objectives
- Use only sections from shadcn-ui-blocks skill
- Constraints/preferences

Agent outputs `/planning/sitemap.yaml` with:
- Page hierarchy (path, title, priority)
- Purpose & SEO focus per page
- CMS collections (if applicable)
- Internal linking strategy
- User journey mapping

Example invocation:
```
Use sitemap-analyst agent:
Context: [Business goals, audience, conversion targets]
Output destination: /planning/sitemap.yaml
```

### Step 3: Website Build
**Select & configure components:**

**IMPORTANT:** The sitemap-analyst from Step 2 decides the pages and structure. You only implement the design and SEO aspects here.

1. Review sitemap structure
2. For each page type, use **shadcn-ui-blocks** skill:
   - Homepage → hero1-50 + feature + pricing/cta
   - Feature pages → feature1-266 (largest category)
   - Pricing → pricing1-35
   - Testimonials → testimonial1-28
   - FAQ → faq1-16
   - Blog → blog1-22 + blogpost1-6
   - Contact → contact1-17
   - Footer → footer1-21
   - Navigation → navbar1-16

3. Use **shadcn-ui-theme** skill:
   - Select theme matching brand
   - Apply CSS variables
   - Test light/dark modes
   - Verify accessibility

4. Coordinate with **shadcn-website-builder agent**:
   - Provide sitemap + component selections
   - Get built pages with responsive layouts
   - Review and refine

### Step 4: SEO Integration
**Optimize for search engines:**

1. **Meta Tags**:
   - Title (50-60 chars): Primary keyword + brand
   - Description (150-160 chars): Call-to-action + benefit
   - Canonical URLs (prevent duplicates)
   - Open Graph (social sharing)

2. **Structured Data**:
   - JSON-LD Schema.org markup
   - Organization schema (homepage)
   - BreadcrumbList (navigation)
   - Product schema (if applicable)
   - FAQPage schema (FAQ sections)

3. **Content Optimization**:
   - H1: Single, primary keyword
   - H2-H4: Secondary keywords, natural flow
   - Image alt text: Descriptive, keyword-relevant
   - Internal links: Anchor text with keywords
   - Meta descriptions: Unique per page

4. **Performance Optimization**:
   - Core Web Vitals (LCP, FID, CLS)
   - Image optimization (next/image component)
   - CSS/JS minification
   - Mobile responsiveness verification
   - Page speed analysis

5. **Technical SEO**:
   - XML sitemap: `/sitemap.xml` list of all pages
   - robots.txt: Control crawler access
   - Canonical tags: Prevent duplicate content
   - Mobile-first indexing: Responsive design
   - No broken links (404 audit)

### Step 5: Verification
**Test implementation:**

1. **Page Testing**:
   - Load all pages in browser
   - Verify responsive on mobile/tablet/desktop
   - Check navigation, links, forms work
   - Validate HTML (W3C validator)

2. **SEO Verification**:
   - Meta tags present and unique (view source)
   - Structured data valid (schema.org validator)
   - Robots.txt accessible
   - Sitemap.xml valid XML
   - Page titles/descriptions follow best practices

3. **Performance Check**:
   - Google PageSpeed Insights score
   - Core Web Vitals status
   - Mobile usability test
   - Accessibility audit (WCAG 2.1 AA)

4. **Content Audit**:
   - Keyword presence verified (tool or manual)
   - H1-H6 hierarchy correct
   - Image alt text present
   - Internal links functioning
   - CTA buttons visible and clickable

---

## SEO Best Practices

### Meta Tags
```html
<head>
  <title>Primary Keyword | Brand (50-60 chars)</title>
  <meta name="description" content="Action-oriented description with secondary keyword (150-160 chars)">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://example.com/page">
  <meta property="og:title" content="Social title">
  <meta property="og:description" content="Social description">
  <meta property="og:image" content="Social image URL">
</head>
```

### Structured Data (JSON-LD)
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Brand Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/brand",
    "https://linkedin.com/company/brand"
  ]
}
```

### Content Structure
- **H1**: One per page, primary keyword
- **H2-H4**: Secondary keywords, logical hierarchy
- **Paragraphs**: 2-4 sentences, natural keyword integration
- **Images**: Descriptive alt text, WebP format, lazy loading
- **Internal Links**: 3-5 contextually relevant per page

### Core Web Vitals Targets
- **Largest Contentful Paint (LCP)**: < 2.5 seconds
- **First Input Delay (FID)**: < 100ms (or Interaction to Next Paint INP < 200ms)
- **Cumulative Layout Shift (CLS)**: < 0.1

### Mobile SEO
- Responsive design (no fixed widths)
- Touch-friendly buttons (44x44px minimum)
- Readable font size (16px base minimum)
- Avoid intrusive interstitials
- Fast mobile page load

---

## Keywords to Trigger This Skill

Primary: website, SEO, landing page, web design, sitemap, homepage, site builder, web development
Secondary: website creation, website build, web page design, search optimization, site structure, information architecture, web layout, digital presence

---

## Integration Summary

| Component | Purpose | Link |
|-----------|---------|------|
| sitemap-analyst | Site structure & IA | Use when designing page hierarchy |
| shadcn-ui-blocks | 959 pre-built components | Use for visual pages |
| shadcn-ui-theme | 17 color themes | Use for design system |
| shadcn-website-builder | Implementation agent | Coordinates build phase |
| WebFetch | Target site analysis | Use when user provides URL |

---

## Example Request Triggers

- "Build me a website with SEO"
- "Create a landing page optimized for search"
- "Design a website for my SaaS product"
- "Help me structure my site for better rankings"
- "Build a homepage that converts and ranks"
- "Create a website with proper site architecture"
- "Design a landing page with sitemap planning"

---

## Output Artifacts

After workflow completion, user receives:

1. `/planning/seo/analysis.md` - SEO research summary
2. `/planning/seo/keywords.md` - Keyword strategy & targeting
3. `/planning/seo/competitors.md` - Competitive analysis
4. `/planning/sitemap.yaml` - Site structure (YAML format)
5. Website code with:
   - Responsive shadcn components
   - Applied theme
   - Optimized meta tags
   - Structured data
   - Performance-tuned images
   - Internal linking strategy

---

**Note:** This is an orchestrating skill. It delegates analysis to sitemap-analyst and building to shadcn-website-builder + component skills. Your role is coordinating the workflow, not implementing every step directly.
