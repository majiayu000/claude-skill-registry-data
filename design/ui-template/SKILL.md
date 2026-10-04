---
name: ui-template
description: Atomic-design guidance for Templates — page-level wireframes that arrange organisms into layout slots (hero/main/sidebar/footer) without fetching data. Use when authoring components under ui/templates, defining reusable page skeletons, or keeping layout decisions out of pages and organisms.
when_to_use: Creating a reusable page layout that accepts content via slots/props; keeping data fetching out of templates (it belongs in pages); defining responsive breakpoints at the layout level; separating layout concerns from organism concerns.
paths:
  - "**/ui/templates/**/*.{jsx,tsx,vue,js,ts}"
  - "**/components/templates/**/*"
  - "**/templates/**/*"
  - "**/layouts/**/*"
---

# Template

## What is a Template?

Templates are page-level wireframe structures that define layout without real content—blueprints showing "hero goes here, nav goes here, grid goes here." They're reusable across many pages with different data.

## Key Principles

1. **Structure Over Content**: Templates define WHERE things go, not WHAT they contain. Use placeholder props or slots—actual data comes from pages.

2. **Layout Orchestration**: Templates handle page-level layout, responsive grid systems, and spatial relationships between organisms.

3. **Content Agnostic**: A ProductTemplate works for any product (t-shirts, electronics, books) by accepting different data. Same structure, different content.

## Best Practices

✅ **DO**:
- Accept content via props/slots (children, header, sidebar, etc.)
- Define responsive layout breakpoints
- Compose organisms into page structure
- Keep templates reusable across different content types
- Document expected prop shapes/slot contracts

❌ **DON'T**:
- Fetch data in templates—that's the page's job
- Hardcode specific content
- Include business logic
- Connect to state management directly
- Mix template concerns with page concerns

## Code Patterns

### Recommended

```jsx
// ProductTemplate.jsx - Reusable page structure
const ProductTemplate = ({ 
  hero,
  productInfo,
  specifications,
  reviews,
  relatedProducts 
}) => (
  <div className="product-template">
    <header className="product-template__hero">
      {hero}
    </header>
    
    <main className="product-template__content">
      <section className="product-template__info">
        {productInfo}
      </section>
      <aside className="product-template__specs">
        {specifications}
      </aside>
    </main>
    
    <section className="product-template__reviews">
      {reviews}
    </section>
    
    <footer className="product-template__related">
      {relatedProducts}
    </footer>
  </div>
);

// Usage in a page
const IPhonePage = ({ product }) => (
  <ProductTemplate
    hero={<ProductHero images={product.images} />}
    productInfo={<ProductInfo data={product} />}
    specifications={<SpecsTable specs={product.specs} />}
    reviews={<ReviewSection productId={product.id} />}
    relatedProducts={<RelatedGrid category={product.category} />}
  />
);
```

### Avoid

```jsx
// ❌ WRONG - Template fetching data
const ProductTemplate = ({ productId }) => {
  const product = useFetch(`/api/products/${productId}`);
  // Templates shouldn't fetch!
};

// ✅ CORRECT - Template receives data via props
const ProductTemplate = ({ product }) => (
  // Pure layout structure
);
```

## Related Terminologies

- **Page** (Server) - Fills templates with actual data
- **Organism** (UI) - Complex sections templates arrange
- **SSR/SSG** (Server) - How pages get their data
- **Router** (Server) - Maps URLs to pages using templates

## Quality Gates

- [ ] No data fetching
- [ ] Content received via props/slots
- [ ] Reusable across different content
- [ ] Responsive breakpoints defined
- [ ] Clear slot/prop contracts documented
- [ ] Layout-focused, not logic-focused

**Source**: `/docs/ui/template.md`
