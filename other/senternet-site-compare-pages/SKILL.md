---
name: senternet-site-compare-pages
description: Create competitor alternative and versus pages for SEO.
---

# Competitor Alternative / Compare Pages

Create SEO-optimized "X alternative" and "X vs Y" pages to capture high-intent search traffic from users evaluating competitors.

## Why these pages work

"[Competitor] alternative" and "[Us] vs [Competitor]" searches have strong commercial intent — users are actively evaluating products. These pages rank well because:
- The keyword is explicit in the URL and title
- The content answers the searcher's actual question
- Internal links from these pages to your home page signal authority

## Page formats

### Format 1: "[Competitor] Alternative" — singular

URL: `/compare/competitor-alternative`
Title: `Best [Competitor] Alternative in [Year] - [Your App]`

Good for: targeting users specifically searching for an alternative to one product.

### Format 2: "[Competitor] Alternatives" — plural

URL: `/compare/competitor-alternatives`
Title: `[N] [Competitor] Alternatives for [Use Case] in [Year]`

Good for: ranking in listicle-format queries. Can mention multiple alternatives including you.

### Format 3: "[Your App] vs [Competitor]"

URL: `/compare/yourapp-vs-competitor`
Title: `[Your App] vs [Competitor]: Which is Better?`

Good for: users who already know both products and want a direct comparison.

### Format 4: "[Competitor] vs [Competitor]"

URL: `/compare/competitor-a-vs-competitor-b`
Title: `[Competitor A] vs [Competitor B]: Which is Better for [Use Case]?`

Good for: ranking when users search for a comparison you're not even in — you appear as a third option.

## Steps

### 1. Create a reusable `ComparePage` component

```tsx
// src/components/ComparePages.tsx
import { MetaTags } from './MetaTags';
import { Link } from 'react-router-dom';

interface Feature {
  name: string;
  yours: boolean | string;
  theirs: boolean | string;
}

interface ComparePageProps {
  title: string;
  description: string;
  heroHeadline: string;
  heroBody: string;
  competitorName: string;
  features: Feature[];
  verdict: string;
  ctaText: string;
  ctaUrl: string;
  image?: string;
}

export function ComparePage({ title, description, heroHeadline, heroBody, competitorName, features, verdict, ctaText, ctaUrl, image }: ComparePageProps) {
  return (
    <>
      <MetaTags title={title} description={description} image={image} />
      <main>
        <h1>{heroHeadline}</h1>
        <p>{heroBody}</p>

        <section>
          <h2>Feature Comparison</h2>
          <table>
            <thead>
              <tr>
                <th>Feature</th>
                <th>APPNAME</th>
                <th>{competitorName}</th>
              </tr>
            </thead>
            <tbody>
              {features.map(f => (
                <tr key={f.name}>
                  <td>{f.name}</td>
                  <td>{typeof f.yours === 'boolean' ? (f.yours ? '✓' : '✗') : f.yours}</td>
                  <td>{typeof f.theirs === 'boolean' ? (f.theirs ? '✓' : '✗') : f.theirs}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section>
          <h2>The Verdict</h2>
          <p>{verdict}</p>
        </section>

        <a href={ctaUrl}>{ctaText}</a>

        {/* Schema.org for compare pages */}
        <script type="application/ld+json">{JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Article",
          "headline": title,
          "description": description,
        })}</script>
      </main>
    </>
  );
}
```

### 2. Create individual compare page components

```tsx
export function CompetitorAlternativePage() {
  return (
    <ComparePage
      title="Best [Competitor] Alternative in 2026 - APPNAME"
      description="Looking for a [Competitor] alternative? APPNAME gives you [key differentiator]. [Short proof point]."
      heroHeadline="The [Competitor] Alternative That [Key Benefit]"
      heroBody="[Competitor] is great for [what they do well]. But if you want [what APPNAME does differently] — APPNAME [how it delivers that benefit]."
      competitorName="[Competitor]"
      features={[
        { name: '[Core feature both share]', yours: true, theirs: true },
        { name: '[Feature APPNAME has, competitor lacks]', yours: true, theirs: false },
        { name: '[Feature competitor has, be honest]', yours: false, theirs: true },
        { name: '[Another differentiator]', yours: true, theirs: false },
        { name: 'Free tier', yours: true, theirs: false },
      ]}
      verdict="[One-sentence honest verdict that explains when to pick APPNAME vs the competitor]."
      ctaText="Try APPNAME Free"
      ctaUrl="https://www.DOMAIN.com/signup"
      image="/share/compare-competitor.webp"
    />
  );
}
```

### 3. Add routes and prerender entries

For each compare page, add to:
1. `src/App.tsx` — `<Route path="/compare/competitor-alternative" element={<CompetitorAlternativePage />} />`
2. `scripts/prerender.mjs` — ROUTES array
3. `public/sitemap.xml` — URL entry with priority 0.7

### 4. Link compare pages from your site

- Add a "Comparisons" section to the footer
- Link from the home page ("See how we compare")
- Link between compare pages ("Also see: [Other Competitor] Alternative")

Internal linking is critical for Google to discover and rank these pages.

### 5. Generate share images

Add entries to `scripts/generate-share-images.mjs` for each compare page. Use the competitor's primary color or neutral branding.

## SEO guidelines for compare pages

- **URL**: use the keyword exactly — `/compare/competitorname-alternative` not `/compare/competitorname`
- **Title**: include the year (or "2026") — compare queries are time-sensitive
- **H1**: matches the primary keyword ("Best [Competitor] Alternative")
- **Content**: be genuinely useful — explain real differences, don't just say you're better at everything
- **Word count**: 600+ words; Google rewards depth for commercial comparison queries
- **Features table**: include features where the competitor wins — authenticity builds trust
- **CTA**: link to sign-up or your main CTA, not just the home page
- **Internal links**: link to 2–3 other compare pages ("Also considering [Other Competitor]? See our comparison.")
- **Update annually**: refresh the year in the title and revisit feature accuracy

## Framework: Next.js track

- `app/vs/[competitor]/page.tsx` and `app/alternatives/[competitor]/page.tsx`, each exporting `generateStaticParams()` from the competitor data file so every page is built statically.
- `generateMetadata({ params })` supplies the per-competitor title, description, canonical, and OG image. These pages live or die on unique metadata, so derive it from the data rather than templating one description across all of them.
- Import the same competitor list into `app/sitemap.ts` so every comparison URL is covered without a second array.
- The content, positioning, and factual-accuracy rules above are unchanged.

See `/senternet-site-framework` for the full convention map.
