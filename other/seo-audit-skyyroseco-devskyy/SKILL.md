---
name: seo-audit
description: "Conducts on-page SEO analysis with title tags, meta descriptions, heading structure, keyword gaps, and technical recommendations. Use when a user wants to improve their website's search rankings, is launching a new site, or needs to diagnose why their pages aren't ranking."
---

# SEO Audit

## When to Use This Skill

- Website pages aren't ranking for target keywords
- Launching a new website and want to start with solid SEO
- Redesigning a site and need to preserve/improve SEO
- Haven't reviewed SEO in 6+ months
- Competitor is outranking you and you want to know why

## Core Principle

**SEO IS ABOUT MATCHING SEARCH INTENT, NOT STUFFING KEYWORDS. Google rewards pages that best answer the searcher's question.**

## Workflow

### Step 1: Gather Inputs

Ask the user:
1. What's the URL or page content to audit?
2. What keywords do you want to rank for? (1-3 primary keywords)
3. Who's your target audience?
4. Who are your top 2 competitors?

**Minimum needed: question 1. If no keywords provided, infer from the page content.**

### Step 2: On-Page SEO Audit

Analyze each element and score as PASS, NEEDS WORK, or FAIL:

| Element | What to Check | Best Practice |
|---------|--------------|---------------|
| Title Tag | Length, keyword placement, uniqueness | 50-60 chars, primary keyword near front |
| Meta Description | Length, CTA, keyword inclusion | 150-160 chars, includes keyword + action verb |
| H1 Tag | Exists, contains keyword, only one per page | One H1 per page, includes primary keyword |
| Heading Structure | H2s and H3s use logical hierarchy | Keywords in H2s, no skipped levels |
| URL Structure | Short, descriptive, includes keyword | /primary-keyword, no dates or IDs |
| Internal Links | Links to/from other relevant pages | 3-5 internal links per 1,000 words |
| Image Alt Text | Descriptive, includes keywords where natural | Every image has alt text |
| Content Length | Sufficient for topic depth | Match or exceed top-ranking competitor length |
| Keyword Density | Natural usage, not stuffed | 1-2% for primary keyword |
| Mobile Friendliness | Responsive, readable without zoom | All content accessible on mobile |

### Step 3: Content Gap Analysis

Compare the page against top-ranking competitors:
1. What subtopics do competitors cover that this page doesn't?
2. What questions do competitors answer that this page skips?
3. What content formats do competitors use (tables, lists, videos)?

### Step 4: Deliver Recommendations

Prioritize fixes by impact:

**Critical (do first):**
- Missing or duplicate title tags
- No H1 or multiple H1s
- Missing meta description
- Thin content (under 300 words for a topic that needs depth)

**High Impact:**
- Keyword not in title tag or H1
- No internal links
- Missing alt text on images
- URL contains unnecessary parameters

**Medium Impact:**
- Meta description too long/short
- Heading hierarchy issues
- Content gaps vs. competitors

**Low Impact (nice to have):**
- Schema markup missing
- Open Graph tags incomplete
- Minor keyword density adjustments

## Examples

### Example 1: Coaching Business Homepage

**URL content analysis:**

```
AUDIT RESULTS — www.sarahcoaching.com

Title Tag: "Sarah Johnson — Life Coach"
→ NEEDS WORK — Missing primary keyword "executive coaching."
  Recommended: "Executive Coaching for Women Leaders | Sarah Johnson"

Meta Description: (none found)
→ FAIL — No meta description. Google will auto-generate one.
  Recommended: "Transform your leadership with 1-on-1 executive coaching
  for women in corporate roles. Book a free discovery call with Sarah Johnson."

H1: "Welcome to My Website"
→ FAIL — Generic, no keywords.
  Recommended: "Executive Coaching for Women Who Lead"

Heading Structure:
  H2: "About Me" → NEEDS WORK — Should be "About Your Executive Coach"
  H2: "Services" → PASS
  H2: "Testimonials" → PASS
  H3: (none) → NEEDS WORK — Add H3s under Services for each offering

URL: www.sarahcoaching.com → PASS (homepage)

Internal Links: 0 links to blog or service pages
→ FAIL — Add links to service pages, blog posts, and booking page

Content Length: 247 words
→ FAIL — Homepage should have 500-800 words minimum for a service business

PRIORITY FIXES:
1. Add meta description (5 min fix, immediate impact)
2. Rewrite H1 with primary keyword (5 min fix)
3. Rewrite title tag (5 min fix)
4. Add 300+ words of content about services and outcomes
5. Add internal links to service pages and blog
```

### Example 2: E-commerce Product Category Page

**URL content analysis:**

```
AUDIT RESULTS — www.greenleafcandles.com/soy-candles

Title Tag: "Soy Candles — GreenLeaf Candles"
→ NEEDS WORK — Add modifier. Recommended: "Hand-Poured Soy Candles |
  Natural & Non-Toxic | GreenLeaf Candles"

Meta Description: "Buy soy candles from GreenLeaf Candles."
→ NEEDS WORK — Too short (43 chars), no differentiation.
  Recommended: "Shop hand-poured soy candles made with 100%
  natural wax and cotton wicks. Free shipping on orders over $50.
  12 signature scents available."

H1: "Soy Candles" → PASS

Content: Product grid only, no descriptive text
→ FAIL — Add 200-300 words above the product grid explaining
  what makes your soy candles different.

CONTENT GAP (vs. top 3 competitors):
- Competitors have "What is a soy candle?" educational section
- Competitors have scent guide / comparison table
- Competitors have FAQ section on the category page
- Competitors average 600+ words of content on category pages

PRIORITY FIXES:
1. Expand meta description to 150-160 characters
2. Add 300 words of category description above products
3. Add FAQ section (3-5 questions about soy candles)
4. Add schema markup for Product type
```

## Recovery & Fallbacks

- **User can't share their URL:** Ask them to paste the page's HTML source or just the visible text content. Audit what you can see.
- **User has hundreds of pages:** Start with the 5 highest-traffic or highest-revenue pages. An 80/20 audit beats a full audit that never happens.
- **User doesn't know target keywords:** Suggest 3-5 based on the page content and business type. Let them confirm before auditing.
- **Technical SEO issues found:** Flag them but clarify that technical SEO (site speed, crawlability, redirects) requires developer tools. This audit focuses on on-page content SEO.

## Constraints

- **NEVER guarantee specific rankings or traffic numbers** — SEO results depend on many factors
- Focus on actionable, specific recommendations — not generic advice
- Always prioritize fixes by impact (don't overwhelm with 50 low-priority items)
- Distinguish between on-page SEO (this audit) and technical SEO (different scope)
- Include the specific recommended text for title tags, meta descriptions, and H1s — don't just say "improve it"
