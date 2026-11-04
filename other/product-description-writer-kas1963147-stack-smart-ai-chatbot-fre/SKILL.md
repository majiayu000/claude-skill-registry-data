---
name: product-description-writer
description: Create compelling, SEO-optimized product descriptions for WooCommerce. Includes benefit-focused copy, feature highlights, and conversion optimization.
tools_required: [woo_product_manage, woo_product_details, ecommerce_search_products, seo_meta, seo_schema, wp_media]
always_on: false
group: woocommerce
order: 2
requires: [shopping-assistant]
suggests: [seo-optimizer, content-creator]
---

# Product Description Writer

Create compelling, SEO-optimized product descriptions for WooCommerce stores.

## When to Use This Skill

- Writing new product descriptions
- Improving existing product copy
- Optimizing product SEO
- Creating product comparison content
- Developing product category descriptions
- Bulk product description updates

## Core Capabilities

### Copywriting
- Benefit-focused descriptions
- Feature to benefit translation
- Emotional connection
- Trust building elements
- Call-to-action placement

### SEO Optimization
- Keyword-rich descriptions
- Meta title and description
- Product schema markup
- Image alt text optimization
- Internal linking

### Conversion Focus
- Pain point addressing
- Objection handling
- Social proof integration
- Urgency elements
- Clear value proposition

## Product Description Structure

### Short Description (50-150 words)
```
[Hook - grab attention]
[Key benefit 1]
[Key benefit 2]
[Call to action]
```

### Long Description (300-500 words)

1. **Opening Hook** (1-2 sentences)
   - Address customer pain point
   - Promise solution

2. **Key Benefits** (3-5 bullet points)
   - Focus on outcomes
   - Use customer language
   - Quantify when possible

3. **Features** (3-5 bullet points)
   - Technical specifications
   - Materials/components
   - Dimensions/sizing

4. **Social Proof**
   - Customer testimonials
   - Usage statistics
   - Awards/certifications

5. **Call to Action**
   - Clear next step
   - Urgency element
   - Risk reversal (guarantee)

## Workflow

### Writing a Product Description

1. **Research Phase**
   - Get product details with `woo_product_details`
   - Review category positioning
   - Identify target keywords

2. **Writing Phase**
   - Create short description
   - Write long description
   - Add technical specifications

3. **Optimization Phase**
   - Set SEO meta with `seo_meta`
   - Add product schema with `seo_schema`
   - Update images with `wp_media`

4. **Publication**
   - Update product with `woo_product_manage`
   - Verify display
   - Check mobile appearance

### BuIk Updates

1. **Search Products**
   - Find products needing updates with `ecommerce_search_products`
   - Filter by category or attribute
   - Prioritize by traffic/sales

2. **Batch Process**
   - Update descriptions systematically
   - Maintain consistent voice
   - Apply SEO templates

## Writing Formulas

### AIDA Formula
- **A**ttention: Hook with benefit
- **I**nterest: Expand on benefits
- **D**esire: Create emotional connection
- **A**ction: Clear CTA

### PAS Formula
- **P**roblem: Identify pain point
- **A**gitate: Amplify the problem
- **S**olution: Present product as answer

### FAB Framework
- **F**eature: What it is
- **A**dvantage: Why it matters
- **B**enefit: What customer gains

## Best Practices

1. **Lead with benefits** - Not features
2. **Use sensory words** - Help customers imagine
3. **Be specific** - Details build trust
4. **Keep paragraphs short** - Easy to scan
5. **Include keywords naturally** - No stuffing
6. **Use bullet points** - Easy to skim
7. **Add images** - Show, don't just tell
8. **Test and iterate** - A/B test descriptions

## SEO Checklist

- [ ] Primary keyword in first sentence
- [ ] Secondary keywords throughout
- [ ] Meta title (50-60 chars)
- [ ] Meta description (150-160 chars)
- [ ] Alt text on all images
- [ ] Product schema enabled
- [ ] Internal links to related products
