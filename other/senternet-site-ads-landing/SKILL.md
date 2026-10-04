---
name: senternet-site-ads-landing
description: Create conversion-focused campaign landing pages for paid ads.
---

# Ad Landing Pages

Create conversion-optimized landing pages for paid ad campaigns (Reddit, Google, Meta) with campaign-specific messaging and tracking.

## Architecture

Landing pages live at `/landing/CAMPAIGN-NAME` routes. Each is a stripped-down, conversion-focused version of the site with:
- No site navigation (reduces distraction, keeps users on page)
- Campaign-specific headline and body copy matched to the ad creative
- Single prominent CTA (App Store / website link)
- Reddit Pixel conversion tracking on CTA click
- No external links except the primary CTA
- Prerendered like all other routes

## Steps

### 1. Create a generic `LandingPage` component

```tsx
// src/components/LandingPage.tsx
import { MetaTags } from './MetaTags';
import { trackRedditEvent } from './RedditPixel';

interface LandingPageProps {
  headline: string;
  body: string;
  ctaText: string;
  ctaUrl: string;
  badge?: string;       // e.g. "Featured on BetaList"
  metaTitle: string;
  metaDescription: string;
  shareImage?: string;
}

export function LandingPage({ headline, body, ctaText, ctaUrl, badge, metaTitle, metaDescription, shareImage }: LandingPageProps) {
  return (
    <>
      <MetaTags
        title={metaTitle}
        description={metaDescription}
        image={shareImage}
      />
      <main className="min-h-screen bg-[#0a0a0f] flex flex-col items-center justify-center px-6 text-center">
        {badge && (
          <span className="mb-6 text-sm font-medium text-cyan-400 border border-cyan-400/30 rounded-full px-4 py-1">
            {badge}
          </span>
        )}
        <h1 className="text-4xl md:text-6xl font-bold text-white max-w-2xl mb-6">
          {headline}
        </h1>
        <p className="text-xl text-gray-400 max-w-xl mb-10">
          {body}
        </p>
        <a
          href={ctaUrl}
          onClick={() => trackRedditEvent('Lead')}
          className="bg-cyan-400 text-black font-bold px-8 py-4 rounded-full text-lg hover:bg-cyan-300 transition-colors"
        >
          {ctaText}
        </a>
      </main>
    </>
  );
}
```

### 2. Create campaign-specific landing page routes

```tsx
// src/components/LandingPages.tsx
import { LandingPage } from './LandingPage';

export function RedditCampaignLanding() {
  return (
    <LandingPage
      headline="[Your Core Value Proposition]"
      body="APPNAME helps you [key benefit]. No account needed."
      ctaText="Try It Free"
      ctaUrl="https://www.DOMAIN.com/signup"
      metaTitle="APPNAME - [Short Value Prop]"
      metaDescription="[150-char description of what APPNAME does and why to try it]"
    />
  );
}

export function RetargetingLanding() {
  return (
    <LandingPage
      headline="[Objection-handling or urgency headline]"
      body="[Reinforce the benefit. Address the hesitation from the first visit.]"
      ctaText="Get Started"
      ctaUrl="https://www.DOMAIN.com/signup"
      metaTitle="APPNAME - [Campaign-Specific Title]"
      metaDescription="[Alternate description targeting this audience segment]"
    />
  );
}
```

### 3. Add landing routes to `src/App.tsx`

```tsx
<Route path="/landing/reddit" element={<RedditCampaignLanding />} />
<Route path="/landing/retargeting" element={<RetargetingLanding />} />
<Route path="/landing/betalist" element={<BetaListLanding />} />
```

### 4. Add landing pages to `scripts/prerender.mjs`

```js
const ROUTES = [
  '/',
  // ... other routes
  '/landing/reddit',
  '/landing/retargeting',
  '/landing/betalist',
];
```

### 5. Add landing pages to `public/sitemap.xml`

Consider whether ad landing pages should be indexed by Google. Options:
- Include in sitemap (Google can find and rank them organically)
- Exclude from sitemap + add `<MetaTags robots="noindex">` (keeps them purely for paid traffic)

Typically: index them — organic search for long-tail queries is free traffic.

### 6. Use campaign-specific UTM params in the CTA URL

```tsx
const ctaUrl = "https://apps.apple.com/app/...&pt=CAMPAIGN_ID&ct=reddit_pro_landing&mt=8";
```

For web-to-web redirects (not App Store), append UTM params:
```
https://www.DOMAIN.com?utm_source=reddit&utm_medium=cpc&utm_campaign=reddit-pro
```

### 7. Create ad creative assets

For Reddit campaigns, create HTML ad assets in `ads/`:

```
ads/
├── banner.html      # 728x90 leaderboard
├── reddit.html      # Reddit-specific feed ad format (300x250)
├── story.html       # Reddit story ad (1080x1920)
├── square.html      # Square format (1200x1200)
└── capture.js       # Puppeteer script to screenshot HTML → PNG
```

The `capture.js` script uses Puppeteer to screenshot each HTML file at the correct dimensions:
```js
import puppeteer from 'puppeteer';

const ADS = [
  { file: 'reddit.html', width: 300, height: 250, name: 'reddit-300x250' },
  { file: 'banner.html', width: 728, height: 90,  name: 'banner-728x90' },
  { file: 'square.html', width: 1200, height: 1200, name: 'square-1200x1200' },
  { file: 'story.html',  width: 1080, height: 1920, name: 'story-1080x1920' },
];

const browser = await puppeteer.launch();
for (const ad of ADS) {
  const page = await browser.newPage();
  await page.setViewport({ width: ad.width, height: ad.height });
  await page.goto(`file://${process.cwd()}/ads/${ad.file}`);
  await page.screenshot({ path: `ads/out/${ad.name}.png` });
  await page.close();
}
await browser.close();
```

## Checklist for each new landing page

- [ ] Route added to `src/App.tsx`
- [ ] Route added to `scripts/prerender.mjs` ROUTES array
- [ ] `<MetaTags>` called with page-specific title and description
- [ ] Reddit pixel `Lead` event fires on CTA click
- [ ] No site navigation (stripped-down layout)
- [ ] Single, prominent CTA
- [ ] Mobile-first design tested at 375px width
- [ ] Page loads fast on mobile (no heavy images above fold)

## Framework: Next.js track

- The shared `LandingPage` component lives in `components/`; each campaign is `app/lp/<campaign>/page.tsx`.
- Campaign pages are almost always `noindex`: set `robots: { index: false, follow: true }` in the page's `metadata` **and** mark the route `indexable: false` in `config/routes.mjs` in the same change, so it never reaches the sitemap or IndexNow.
- Keep the page a server component. The only parts that need `'use client'` are the CTA click tracking and any form.
- UTM parameters read via `useSearchParams()` must sit inside a `<Suspense>` boundary in a client component, or the whole page opts into dynamic rendering — which turns a static landing page into a cold start on the exact traffic you are paying for.
- Conversion pixels are wired as described in `/senternet-site-ads-reddit-pixel` on this track.

See `/senternet-site-framework` for the full convention map.
