---
name: shopify-theme-pro
description: 覆盖Shopify主题的全流程开发、部署和设计系统管理，支持 Liquid 模板编写、Online Store 2.0 架构、性能优化与主题发布。
title: Shopify主题开发
example: 在本地启动 Shopify 主题开发服务器以实时预览我的页面修改，并在确认无误后将更新推送至指定主题。
version: 1.0.0
---
# Shopify Theme Development Pro

End-to-end Shopify theme development, deployment, and design system management. Covers Liquid templating, Online Store 2.0 architecture, performance optimization, deployment workflows, and CSS design systems.

## When to Use

Apply this skill when:
- Building new Shopify themes or theme sections
- Writing or refactoring Liquid templates
- Implementing theme customization features
- Deploying theme changes to development or live stores
- Optimizing theme performance (speed, accessibility, SEO)
- Creating or maintaining a CSS design system for Shopify
- Reviewing theme code for quality and standards
- Migrating themes to Online Store 2.0
- Working with Shopify CLI (development, push, pull)

## Quick Start

### Local Development

Start a local dev server with hot reload:

```bash
shopify theme dev --store=your-store.myshopify.com
```

Visit `http://localhost:9292` to preview changes in real-time.

### Deploy to Store

Push local changes to a theme:

```bash
shopify theme push --theme <THEME_ID>
```

See `references/deployment.md` for the full pre-flight checklist and deployment workflow.

### Create New Section

Generate a section scaffold:

```bash
mkdir -p sections
touch sections/my-section.liquid
```

See `references/liquid-patterns.md` for common section patterns and schemas.

## Core Concepts

### Theme Architecture

**Directory Structure:**
```
theme/
├── assets/          # CSS, JavaScript, images
├── config/          # Theme settings (settings_schema.json, settings_data.json)
├── layout/          # Template wrappers (theme.liquid required)
├── sections/        # Reusable, customizable content modules
├── snippets/        # Reusable code fragments
├── templates/       # Page-type templates (JSON or Liquid)
└── locales/         # Translation files (en.default.json, etc.)
```

**Key Principles:**
- **Sections** are merchant-customizable modules (can include blocks)
- **Snippets** are reusable code fragments (not directly customizable)
- **Templates** wrap sections and define page layouts
- **Layouts** provide recurring elements (header, footer, scripts)
- **Online Store 2.0** uses JSON templates to wrap sections (preferred)

### Online Store 2.0 Architecture

✅ **DO:**
- Use JSON templates (allows sections on any page)
- Design for app block integration
- Enable merchant customization via settings schemas
- Allow sections to be reordered and toggled

❌ **DON'T:**
- Lock sections to specific templates
- Hardcode content that should be editable
- Use legacy Liquid-only templates for new themes

**JSON Template Example:**
```json
{
  "sections": {
    "header": {
      "type": "header"
    },
    "main": {
      "type": "main-product"
    }
  },
  "order": ["header", "main"]
}
```

### Liquid Templating Essentials

**Basic Syntax:**
```liquid
{%- # Output variables -%}
{{ product.title }}
{{ product.price | money }}

{%- # Control flow -%}
{% if product.available %}
  <button type="submit">Add to Cart</button>
{% else %}
  <span class="sold-out">Sold Out</span>
{% endif %}

{%- # Loops -%}
{% for variant in product.variants limit: 10 %}
  {{ variant.title }}: {{ variant.price | money }}
{% endfor %}

{%- # Filter chaining (processes left to right) -%}
{{ product.description | strip_html | truncate: 150 | upcase }}
```

**Performance Tips:**
- Use `{%- -%}` to strip whitespace and reduce HTML size
- Chain filters efficiently
- Limit loops where possible (`{% for item in array limit: 10 %}`)
- Use the `liquid` tag for nested logic blocks

See `references/liquid-patterns.md` for advanced patterns.

## Development Workflow

### 1. Setup

Initialize a new theme from a template:

```bash
shopify theme init
```

Or clone an existing theme:

```bash
shopify theme pull --theme <THEME_ID>
```

### 2. Local Development

Run the dev server:

```bash
shopify theme dev --store=your-store.myshopify.com
```

Changes auto-sync to the dev theme and reload the browser.

### 3. Quality Checks

Run Theme Check linter:

```bash
shopify theme check
```

Fix any errors or warnings before deploying.

### 4. Deployment

See the full deployment workflow in `references/deployment.md`. Key steps:
- Pre-flight checks (target theme, credentials, git status)
- Artifact scan (debug code, TODOs, localhost URLs)
- Push to store
- Post-push verification

```bash
shopify theme push --theme <THEME_ID>
```

**IMPORTANT:** Never push to live theme without `--allow-live` flag and explicit confirmation.

### 5. Publish

Promote a theme to live:

```bash
shopify theme publish --theme <THEME_ID>
```

## Performance Optimization

See `references/performance.md` for detailed optimization strategies.

**Quick Wins:**
- Minimize JavaScript usage (prefer native browser features)
- Lazy load images (`loading="lazy"`)
- Defer non-critical CSS
- Use responsive images (`srcset`)
- Compress assets (minify CSS/JS, optimize images)
- Implement resource hints (`preload`, `dns-prefetch`)
- Test on real mobile devices and slow connections

**Avoid:**
- Synchronous scripts in `<head>`
- Heavy JavaScript libraries for simple interactions
- Uncompressed images
- Render-blocking CSS

## Accessibility Standards

Build accessibility from the ground up:
- Use semantic HTML elements
- Provide ARIA labels and roles where needed
- Ensure keyboard navigation works
- Maintain sufficient color contrast (WCAG AA minimum)
- Test with screen readers (VoiceOver, NVDA)
- Support reduced motion preferences

**Example:**
```liquid
<button
  type="button"
  aria-label="{{ 'cart.add_to_cart' | t }}"
  aria-describedby="variant-{{ variant.id }}"
>
  {{ 'cart.add' | t }}
</button>
```

## Design System Management

See `references/design-system.md` for building and maintaining a CSS design system.

**Key Components:**
- Brand colors (primary, secondary, accent, neutral scales)
- Typography scale (headings, body, labels)
- Spacing system (4px or 8px base unit)
- Component library (buttons, cards, grids, forms)
- Responsive breakpoints
- CSS custom properties (variables)

**Approach:**
- Define design tokens in `assets/variables.css` or `config/settings_schema.json`
- Build reusable component classes
- Document component usage in `references/design-system.md`
- Keep components merchant-customizable via theme settings

## Merchant Customization

Enable merchants to customize themes without code:

**Theme Settings (`config/settings_schema.json`):**
```json
{
  "name": "Colors",
  "settings": [
    {
      "type": "color",
      "id": "color_primary",
      "label": "Primary Color",
      "default": "#000000"
    },
    {
      "type": "font_picker",
      "id": "font_heading",
      "label": "Heading Font",
      "default": "helvetica_n4"
    }
  ]
}
```

**Section Settings:**
```liquid
{% schema %}
{
  "name": "Featured Collection",
  "settings": [
    {
      "type": "collection",
      "id": "collection",
      "label": "Collection"
    },
    {
      "type": "range",
      "id": "products_to_show",
      "min": 2,
      "max": 12,
      "step": 1,
      "default": 4,
      "label": "Products to show"
    }
  ],
  "blocks": [
    {
      "type": "heading",
      "name": "Heading",
      "settings": [
        {
          "type": "text",
          "id": "heading",
          "label": "Heading"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Featured Collection"
    }
  ]
}
{% endschema %}
```

## Shopify CLI Reference

**Development:**
- `shopify theme init` — Create new theme from template
- `shopify theme dev` — Local dev server with hot reload
- `shopify theme list` — List all themes on the store
- `shopify theme open` — Open theme in Shopify admin

**Deployment:**
- `shopify theme push` — Push local changes to store
- `shopify theme pull` — Pull remote changes to local
- `shopify theme publish` — Set theme as live
- `shopify theme share` — Generate shareable preview link
- `shopify theme package` — Create distributable ZIP

**Quality:**
- `shopify theme check` — Run linter
- `shopify theme check --auto-correct` — Auto-fix issues

**Flags:**
- `--store <store.myshopify.com>` — Target store
- `--theme <THEME_ID>` — Target specific theme
- `--allow-live` — Allow pushing to live theme (requires confirmation)
- `--only <glob>` — Push specific files only
- `--ignore <glob>` — Skip specific files
- `--nodelete` — Don't delete remote files missing locally

## Ajax API for Interactivity

Common use cases:
- Add to cart without page reload
- Update cart counter dynamically
- Product quick view
- Search suggestions

**Example (Add to Cart):**
```javascript
fetch(`${window.Shopify.routes.root}cart/add.js`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    id: variantId,
    quantity: 1
  })
})
.then(response => response.json())
.then(item => {
  console.log('Added to cart:', item);
  // Update cart UI
})
.catch(error => console.error('Error:', error));
```

**Get Cart Contents:**
```javascript
fetch(`${window.Shopify.routes.root}cart.js`)
  .then(response => response.json())
  .then(cart => console.log('Cart:', cart));
```

See Shopify Ajax API docs for all endpoints and response schemas.

## Code Quality Standards

✅ **DO:**
- Use version control (Git)
- Write clear, maintainable code
- Document complex logic with comments
- Follow Liquid style conventions
- Use Theme Check in CI/CD pipelines
- Test on multiple devices and browsers

❌ **DON'T:**
- Obfuscate code
- Manipulate search engines deceptively
- Hardcode merchant-specific data
- Ignore Theme Check warnings
- Skip accessibility testing

## Testing Checklist

Before deploying to production:
- [ ] Run `shopify theme check` with no critical errors
- [ ] Test on mobile devices (iOS and Android)
- [ ] Verify accessibility with screen reader
- [ ] Check performance scores (Lighthouse: 90+ recommended)
- [ ] Test all customization options in theme editor
- [ ] Verify translations in all supported locales
- [ ] Test cart and checkout flow end-to-end
- [ ] Validate on slow 3G network
- [ ] Check browser compatibility (last 2 major versions)
- [ ] Review security best practices (HTTPS, CSP headers)

## Common Patterns

See `references/liquid-patterns.md` for detailed examples:
- Modular section development
- Reusable snippet patterns
- Product card components
- Dynamic section rendering
- Metafield access patterns
- Custom form handling

## Resources

- **Official Docs:** https://shopify.dev/docs/themes
- **Liquid Reference:** https://shopify.dev/docs/api/liquid
- **Theme Check:** https://shopify.dev/docs/storefronts/themes/tools/theme-check
- **CLI Reference:** https://shopify.dev/docs/themes/tools/cli
- **Ajax API:** https://shopify.dev/docs/api/ajax
- **Best Practices:** https://shopify.dev/docs/themes/best-practices

## Navigation

- `references/liquid-patterns.md` — Common Liquid patterns and section schemas
- `references/design-system.md` — CSS design system guidelines
- `references/deployment.md` — Full deployment workflow and pre-flight checklist
- `references/performance.md` — Performance optimization strategies

---

**Version:** 1.0 (Combined from shopify-theme-dev + shopify-theme-push)
**Last Updated:** 2026-03-13
