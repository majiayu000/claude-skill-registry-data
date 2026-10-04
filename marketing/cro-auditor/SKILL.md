---
name: cro-auditor
description: Audit a website for CRO issues and AI automation opportunities, returning actionable findings with outreach hooks
tags: [cro, audit, conversion, ecommerce, outreach]
---

# CRO Auditor

Audits a website for conversion rate optimization issues AND AI automation opportunities. Returns specific, actionable findings that can be referenced in outreach messages. Each finding includes an impact assessment, recommended fix, and a natural outreach hook.

## Prerequisites

- WebSearch or browser automation tool available to visit and analyze the target website
- Target website URL
- Optional: `agency.config.json` for service-specific audit focus

## Phase 0: Intake

1. Read `agency.config.json` from the project root (if available).
2. Extract `services[]` to understand which CRO areas the agency specializes in.
3. Accept parameters:
   - `url` -- (required) the website to audit
   - `pages` -- (optional) specific pages to audit. Default: homepage, one product page, one collection page
   - `depth` -- `quick` (homepage only) | `standard` (home + product + collection) | `deep` (all pages + mobile + speed). Default: `standard`
   - `focus` -- (optional) specific area: `trust`, `navigation`, `product-pages`, `mobile`, `speed`, `checkout`, `cta`

## Phase 1: Homepage Audit

Visit the homepage and evaluate:

### Above the Fold
- **Hero clarity**: Is the value proposition clear within 3 seconds?
- **CTA visibility**: Is there a clear primary CTA above the fold?
- **Visual hierarchy**: Does the eye flow naturally from headline to supporting text to CTA?
- **Hero image/video**: Does it show the product in use or just a generic brand shot?
- **Navigation**: Is the menu clear, scannable, and well-organized?

### Trust Signals
- **Social proof**: Customer count, testimonials, trust badges visible?
- **Brand logos**: "As seen in" or partner logos present?
- **Reviews aggregate**: Overall rating visible on homepage?
- **Security badges**: SSL, payment security, money-back guarantee?
- **Contact info**: Phone number, email, or chat widget accessible?

### Content Structure
- **Sections flow**: Does the page tell a story (problem, solution, proof, CTA)?
- **Category access**: Can visitors find product categories within one click?
- **Featured products**: Are bestsellers or new arrivals prominently displayed?
- **Email capture**: Is there a popup or embedded signup with a compelling offer?

## Phase 2: Product Page Audit

Find and visit a representative product page. Evaluate:

### Product Information
- **Images**: Multiple angles? Lifestyle shots? Zoom capability? Video?
- **Description quality**: Features AND benefits? Or just specs?
- **Variant selector**: Clear size/color selection? Visual swatches or text dropdowns?
- **Size guide**: Present and easy to find? (critical for apparel/footwear)
- **Ingredients/materials**: Listed clearly? (critical for skincare/food)
- **Price clarity**: Price clearly visible? Compare-at price shown? EMI/payment plans?

### Trust and Confidence
- **Reviews**: Customer reviews present? With photos? Star rating visible?
- **Review count**: Enough reviews to be credible (>10)?
- **Q&A section**: Customer questions and answers available?
- **Return policy**: Clearly stated on the product page (not buried in footer)?
- **Shipping info**: Delivery estimate on the product page?
- **Guarantees**: Money-back guarantee, warranty info?

### Conversion Elements
- **Add to Cart button**: Prominent, contrasting color, sticky on mobile?
- **Buy Now / Express checkout**: Available for impulse buyers?
- **Urgency elements**: Stock count, limited edition, sale timer? (if appropriate)
- **Upsell/cross-sell**: Related products, "frequently bought together", bundles?
- **Sticky add-to-cart**: Does the ATC button stay visible on scroll?

### Social Proof on Product Page
- **UGC**: User-generated photos or videos?
- **Instagram feed**: Brand's Instagram embedded?
- **Influencer mentions**: Badges or callouts?

## Phase 3: Collection Page Audit

Visit a collection/category page. Evaluate:

### Browsing Experience
- **Filters**: Available? Relevant? (price, size, color, type)
- **Sort options**: Best selling, price, newest, rating?
- **Product card info**: Does each card show price, rating, variants, quick-add?
- **Grid layout**: Clean grid with consistent card sizes?
- **Pagination vs infinite scroll**: Which is used? Is it smooth?
- **Empty states**: What happens when filters return no results?

### Scanability
- **Product images**: Consistent style and ratio?
- **Quick view**: Can visitors see product details without leaving the collection?
- **Sale/badge indicators**: New, sale, bestseller badges on cards?

## Phase 4: Mobile Experience

Check the site on mobile viewport:

- **Responsive layout**: Does everything adapt properly?
- **Touch targets**: Are buttons/links large enough to tap?
- **Menu**: Hamburger menu works smoothly?
- **Product images**: Swipeable gallery?
- **Sticky ATC**: Add to cart visible without scrolling back up?
- **Form inputs**: Easy to fill on mobile? Auto-zoom issues?
- **Pop-ups**: Do they cover the entire screen? Easy to dismiss?
- **Page speed**: Does it feel fast on mobile?

## Phase 5: Cart and Checkout Friction

If accessible, evaluate:

- **Cart drawer vs page**: Slide-out cart or separate page?
- **Cart upsell**: Recommendations in cart?
- **Shipping calculator**: Can they estimate shipping before checkout?
- **Discount code field**: Visible? Does it discourage non-coupon buyers?
- **Guest checkout**: Available or forced account creation?
- **Checkout steps**: How many steps to complete purchase?
- **Trust signals in checkout**: Security badges, guarantees repeated?
- **Payment options**: Multiple options (cards, UPI, wallets, BNPL)?

## Phase 6: Page Speed Indicators

Observe or search for speed data:

- WebSearch: `site:pagespeed.web.dev "{{domain}}"` or `"{{domain}}" page speed`
- Observable indicators: Image optimization, lazy loading, font loading, script blocking
- Note any visible layout shifts or slow-loading elements

## Phase 6.5: AI Audit

Based on publicly visible data, assess AI automation opportunities for the store:

### AI-Powered Customer Experience
- **AI Product Recommendations**: Are they using basic "You may also like" or AI-powered personalization? Most stores use Shopify's basic recommendations.
- **AI Chatbot / Customer Service**: Is there a chat widget? Is it rule-based or AI-powered? Could Claude or an AI assistant handle their FAQ and product questions?
- **AI Search**: Is their site search basic keyword matching or AI-powered semantic search?

### AI-Powered Operations
- **Content Generation**: Could AI help with product descriptions, SEO content, social media posts?
- **Email Automation**: Are their email flows basic templates? Could AI personalize email content per customer?
- **Inventory Forecasting**: For brands with multiple SKUs, AI demand forecasting could reduce stockouts.

### AI-Powered Marketing
- **Ad Copy Generation**: Are they running ads? Could AI generate and A/B test ad variations?
- **Customer Segmentation**: Could AI identify high-LTV customer segments from purchase data?
- **Review Analysis**: Could AI analyze customer reviews to identify product improvement opportunities?

### AI Integration Opportunities
- **Claude-Based Systems**: What custom AI agents could improve their workflow?
  - Automated customer support agent
  - Content generation pipeline
  - Order management automation
  - Supplier communication automation
- **Workflow Automation**: What manual processes could be automated with AI?

### AI Audit Output

For each AI opportunity found, provide:
- **Opportunity**: What can be improved with AI
- **Current state**: What they're doing now (if visible)
- **Potential impact**: Revenue, efficiency, or customer experience improvement
- **Implementation**: How Plasho + Claude Code can set this up
- **Outreach hook**: Natural way to mention this in outreach

Example:
```json
{
  "area": "AI Customer Service",
  "opportunity": "Replace basic FAQ page with AI-powered chatbot",
  "current_state": "Static FAQ page with 12 questions, no live chat",
  "impact": "High -- reduce support tickets by 40-60%, 24/7 availability",
  "implementation": "Claude-powered chatbot trained on their product catalog and policies",
  "outreach_hook": "Noticed your FAQ page handles common questions statically. We've set up AI chatbots for D2C brands that handle 60% of support automatically."
}
```

## Phase 7: Score and Prioritize

Assign an overall score from 1-10 based on:
- 9-10: Excellent, minimal issues
- 7-8: Good, a few optimizations possible
- 5-6: Average, clear improvement areas
- 3-4: Below average, significant issues hurting conversion
- 1-2: Major problems, likely losing most potential customers

Score breakdown by area:
- Trust signals: X/10
- Product pages: X/10
- Navigation: X/10
- Mobile: X/10
- CTA clarity: X/10
- Checkout: X/10
- AI readiness: X/10

## Phase 8: Generate Outreach Hooks

For each issue found, craft a natural outreach hook. Rules:
- Be specific, not generic ("Your product pages are missing customer reviews" not "Your site could be improved")
- Frame as an observation, not a criticism
- Connect to revenue impact when possible
- Keep it to one sentence
- Make it conversational

Good examples:
- "I noticed your product pages don't show customer reviews, which typically increases conversion by 15-25%."
- "Your mobile add-to-cart button disappears on scroll, which means mobile shoppers have to scroll back up to buy."
- "Your collection pages don't have filters, so shoppers with 50+ products to browse might bounce."

Bad examples:
- "Your website needs work." (too vague)
- "I found 15 critical issues with your store." (sounds like a scare tactic)
- "Your conversion rate is probably terrible." (presumptuous and rude)

## Phase 9: Output

Return structured JSON:

```json
{
  "url": "https://example.com",
  "audited_at": "2024-01-15T14:30:00Z",
  "overall_score": "5/10",
  "score_breakdown": {
    "trust_signals": "4/10",
    "product_pages": "5/10",
    "navigation": "6/10",
    "mobile": "5/10",
    "cta_clarity": "6/10",
    "checkout": "5/10",
    "ai_readiness": "X/10"
  },
  "top_issues": [
    {
      "area": "Product Pages",
      "issue": "No customer reviews on product pages",
      "impact": "High -- reviews increase conversion by 15-25% and reduce return rates",
      "fix": "Add a reviews app (Judge.me, Loox, Stamped) and set up post-purchase review request emails",
      "effort": "Low (1-2 hours to install and configure)",
      "outreach_hook": "I noticed your product pages don't show customer reviews. For skincare brands, reviews with photos are the #1 conversion driver."
    },
    {
      "area": "Mobile",
      "issue": "Add-to-cart button not sticky on mobile",
      "impact": "Medium -- mobile shoppers must scroll back to the top to add items to cart",
      "fix": "Enable sticky ATC in theme settings or add a custom sticky bar",
      "effort": "Low (theme setting or 30-min code change)",
      "outreach_hook": "On mobile, your add-to-cart button disappears when someone scrolls down to read reviews. Quick fix that usually bumps mobile conversion."
    }
  ],
  "ai_opportunities": [
    {
      "area": "AI Customer Service",
      "opportunity": "...",
      "current_state": "...",
      "impact": "...",
      "implementation": "...",
      "outreach_hook": "..."
    }
  ],
  "ai_recommended_changes": [
    "Implement AI chatbot for customer support",
    "Add AI-powered product recommendations",
    "Set up AI content generation pipeline"
  ],
  "strengths": [
    "Clean, consistent product photography",
    "Good brand storytelling on the about page",
    "Fast page load on desktop"
  ],
  "recommended_changes": [
    "Add customer reviews with photo upload",
    "Implement sticky add-to-cart on mobile",
    "Add size guide to apparel product pages",
    "Show delivery estimate on product page",
    "Add trust badges near the add-to-cart button"
  ],
  "pages_audited": [
    "https://example.com",
    "https://example.com/products/example-product",
    "https://example.com/collections/all"
  ],
  "depth": "standard"
}
```

## Phase 10: Log

No approval gate. Results are written directly to CRM and passed to downstream skills.

## Example Usage

Trigger phrases:
- "Audit this website for CRO"
- "Check [url] for conversion issues"
- "Run a CRO audit on [company]'s store"
- "Find issues on [url] I can mention in my outreach"
- "Quick audit of [url]"

```
User: Audit https://brandx.com for CRO issues
Assistant: [visits homepage, product page, collection page, evaluates all dimensions, returns scored findings with outreach hooks]
```

```
User: Quick CRO check on example.com, just the product pages
Assistant: [visits product page only, returns focused findings]
```
