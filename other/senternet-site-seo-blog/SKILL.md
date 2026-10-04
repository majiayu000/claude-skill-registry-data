---
name: senternet-site-seo-blog
description: Add a prerendered SEO blog with posts and tag pages.
---

# SEO Blog

Add an SEO-optimized blog section to drive organic search traffic. Each post gets its own prerendered route, sitemap entry, and share image.

## Before you start

Ask the user:

> **What URL path should the blog live at?** (e.g. `/blog`, `/insights`, `/news`, `/updates`)
> Default is `/blog` — press enter to keep it.

Use their answer as `$BLOG_PATH` throughout. If they skip or enter nothing, use `/blog`.

## Architecture

Posts live at `$BLOG_PATH/SLUG`. Each post is:
- A React component (or data-driven template) with unique content
- A prerendered static HTML page
- Listed on an index page at `/blog`
- Linked from a sitemap entry
- Given a programmatically generated share image

## Steps

### 1. Create the blog index page

Name the component after the path segment (e.g. `InsightsIndexPage` for `/insights`, `BlogIndexPage` for `/blog`).

```tsx
// src/components/BlogIndexPage.tsx  ← rename to match $BLOG_PATH
import { MetaTags } from './MetaTags';
import { Link } from 'react-router-dom';

const POSTS = [
  {
    slug: 'how-to-get-started-with-appname',
    title: 'How to Get Started with APPNAME',
    date: '2026-01-15',
    description: 'A step-by-step guide to setting up APPNAME and getting value on day one.',
    image: '/share/post-getting-started.webp',
  },
  // Add new posts here
];

export function BlogIndexPage() {
  return (
    <>
      <MetaTags
        title="Blog - APPNAME"
        description="Guides, tips, and updates from the APPNAME team."
        image="/share/blog-index.webp"
      />
      <main>
        <h1>Blog</h1>
        <ul>
          {POSTS.map(post => (
            <li key={post.slug}>
              <Link to={`$BLOG_PATH/${post.slug}`}>
                <h2>{post.title}</h2>
                <time dateTime={post.date}>{post.date}</time>
                <p>{post.description}</p>
              </Link>
            </li>
          ))}
        </ul>
      </main>
    </>
  );
}
```

### 2. Create individual post components

Each post is a standalone component:

```tsx
// src/components/PostGettingStarted.tsx
import { MetaTags } from './MetaTags';

export function PostGettingStarted() {
  return (
    <>
      <MetaTags
        title="How to Get Started with APPNAME - APPNAME Blog"
        description="A step-by-step guide to setting up APPNAME and getting value on day one."
        image="/share/post-getting-started.webp"
      />
      <article>
        <header>
          <h1>How to Get Started with APPNAME</h1>
          <time dateTime="2026-01-15">January 15, 2026</time>
        </header>

        <p>Getting started with APPNAME takes less than five minutes...</p>

        {/* Article body */}

        {/* Schema.org Article markup */}
        <script type="application/ld+json">{JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Article",
          "headline": "How to Get Started with APPNAME",
          "datePublished": "2026-01-15",
          "author": { "@type": "Organization", "name": "APPNAME" },
          "image": "https://www.DOMAIN.com/share/post-getting-started.png",
        })}</script>
      </article>
    </>
  );
}
```

### 3. Add routes to `src/App.tsx`

```tsx
<Route path="$BLOG_PATH" element={<BlogIndexPage />} />
<Route path="$BLOG_PATH/how-to-get-started-with-appname" element={<PostGettingStarted />} />
```

### 4. Add to `scripts/prerender.mjs`

```js
const ROUTES = [
  '$BLOG_PATH',
  '$BLOG_PATH/how-to-get-started-with-appname',
];
```

### 5. Add to `public/sitemap.xml`

```xml
<url>
  <loc>https://www.DOMAIN.com$BLOG_PATH</loc>
  <lastmod>2026-01-15</lastmod>
  <changefreq>weekly</changefreq>
  <priority>0.8</priority>
</url>
<url>
  <loc>https://www.DOMAIN.com$BLOG_PATH/how-to-get-started-with-appname</loc>
  <lastmod>2026-01-15</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.7</priority>
</url>
```

Or add post routes to `generate-sitemap.mjs` and regenerate.

### 6. Generate a share image for each post

Add a block to `scripts/generate-share-images.mjs`:

```js
const BLOG_POSTS = [
  { id: 'post-getting-started', title: 'How to Get Started with APPNAME', subtitle: 'January 15, 2026', color: '#00d4ff' },
];

for (const post of BLOG_POSTS) {
  const svg = buildPostSvg(post); // your SVG template
  await sharp(Buffer.from(svg)).png().toFile(`public/share/${post.id}.png`);
  await sharp(`public/share/${post.id}.png`).webp({ quality: 85 }).toFile(`public/share/${post.id}.webp`);
}
```

### 7. Tag / category index pages (for programmatic SEO at scale)

For apps with many content categories, create index pages per tag:

```
$BLOG_PATH/topics               → all topics
$BLOG_PATH/topics/guides        → all guide posts
$BLOG_PATH/topics/updates       → all product update posts
$BLOG_PATH/topics/tips          → posts tagged with tips
```

Data lives in `src/data/posts.ts`:

```typescript
export interface PostAppearance {
  slug: string;
  title: string;
  date: string;
  excerpt: string;
  accentColor: string;
}

export interface Topic {
  slug: string;
  label: string;
  posts: PostAppearance[];
}

export const TOPICS: Topic[] = [
  {
    slug: 'guides',
    label: 'Guides',
    posts: [
      {
        slug: 'how-to-get-started-with-appname',
        title: 'How to Get Started with APPNAME',
        date: '2026-01-15',
        excerpt: 'Set up APPNAME and get value on day one.',
        accentColor: '#00d4ff',
      },
    ],
  },
];
```

When adding a new post, update `posts.ts` for every topic it belongs to.

## SEO writing guidelines

- **Title format**: `[Topic] - [Date or Context] | APPNAME` — unique per post
- **Description**: 150–160 chars, includes the primary keyword naturally
- **H1**: matches the post title exactly (one per page)
- **Internal links**: each post should link to 2–3 related posts and the blog index
- **Publication date**: use `<time dateTime="YYYY-MM-DD">` for structured data
- **Alt text**: all images need descriptive alt text, not filename
- **Word count**: 400+ words minimum for Google to consider it substantive content
- **Freshness**: update `<lastmod>` in the sitemap when you revise a post

## Auto-publishing and social announcement (the control plane)

Once the blog exists, a scheduled Claude Code routine can write each new post, ship it, prove it is live, and announce it on social with no manual step. This is the same control-plane pattern every Senternet property uses. Set it up per repo.

**The invariant: announce a URL only after it is proven live.** Not "deployed", not "the cron ran". Live. A single-page-app site answers HTTP 200 for a post URL *before the page exists*, serving the HOMEPAGE `og:image` and `og:title`; a scraper that lands there caches the wrong card against the permalink and keeps serving it long after the real page ships. Gate every announcement on `scripts/verify-live.mjs <url>` in the `senternet` control-plane repo (check it out as a second git source in the routine). It prints `RELEASE-OK <url>` only when the page returns 200, declares its own `canonical` + `og:url`, carries a fetchable absolute `og:image`, and is not the homepage card. Publish only the URL on that line; if it exits non-zero, publish nothing.

### The routine flow (per site)

1. Write the post (mirror the newest existing one), wire it in, build.
2. Open a PR, then either merge it (squash) to trigger the deploy, or leave it for the owner to review and merge when the site wants a human gate.
3. Run verify-live against the new URL until `RELEASE-OK`.
4. Post to the brand's Buffer channels (rules below).
5. Optionally amplify from a personal account (quote-tweet below).

### Buffer posting rules

- **Reach Buffer over MCP; never put a Buffer token in a site repo.** Several sites share one Buffer org, so the credential exists once, in the control plane, not once per repo.
- **Never create a post with status `scheduled`.** A scheduled post fires on wall-clock time whether or not the deploy landed. Use `mode: 'shareNow'` (only after `RELEASE-OK`) for immediate posts. For a draft that a daily release routine publishes later, use `saveToDraft: true` with `mode: 'customScheduled'` and a **future** `dueAt` (the intended publish time). Do not use `addToQueue` (the `create_post` default): it silently drops `dueAt`, and a draft with no `dueAt` is invisible to the release routine forever.
- **Twitter / X:** put the post URL in the `text`. X has no link-attachment field.
- **LinkedIn: attach the share image as a NATIVE IMAGE ASSET and put the URL in the `text`. Do NOT use `metadata.linkedin.linkAttachment`.** LinkedIn does not auto-fetch `og:image` for API-posted shares the way Facebook does, so a link attachment renders a bare URL card with no image, even when the page's OG tags are perfect. Passing the image as a real asset makes it render, and native-image posts also outrank outbound-link posts in LinkedIn's feed. Use the PNG or JPG share image, not WebP (LinkedIn's image proxy is reliable on PNG/JPG and historically flaky on WebP).
  - **This applies to EVERY LinkedIn channel in the run, with no exceptions — company pages AND personal profiles.** The common failure is attaching the asset for one brand (e.g. `senternet`) and shipping a sibling channel (e.g. `beereadyinc`, `msenter`) in the same batch with `assets: []`; that sibling renders a bare link. Build the `assets` array once and pass it to every LinkedIn `create_post`; never send a LinkedIn post whose `assets` is empty.

  ```js
  create_post({
    channelId: <linkedin channel id>,
    schedulingType: 'automatic',
    mode: 'shareNow',                                  // or saveToDraft + customScheduled + future dueAt
    text: `${comment}\n\n${postUrl}`,                  // the URL is a plain clickable link
    assets: [{ image: {
      url: `https://www.DOMAIN.com/share/<share-id>.png`,   // absolute, PNG/JPG, not WebP
      metadata: { altText: '<describe the share card>' },
    } }],
    // NOTE: no metadata.linkedin.linkAttachment
  })
  ```

- **Facebook:** `metadata.facebook.type: 'post'` + `metadata.facebook.linkAttachment.url` works; Facebook does unfurl `og:image`.
- **Verify, do not assume.** `create_post` / `edit_post` may hit a ~10s client timeout but still succeed server-side. Confirm with `get_post` (status `sent`/`sending`) before retrying, or you will double-post. **For LinkedIn, also confirm the returned post's `assets` array is non-empty** — an empty `assets` means the card will render as a bare link and the image must be re-attached (a `sent` LinkedIn post cannot have media edited afterward; delete and re-post to fix).

### Cross-account amplification (optional)

To have a personal account quote-tweet a brand post on X: after the brand post is `sent`, read its `externalLink` (`https://x.com/<id>/status/<TWEET_ID>`), then create a post on the personal channel whose `text` is a short comment followed by `https://x.com/<brand-handle>/status/<TWEET_ID>`. Putting the tweet URL in the text is what makes X render a **quote-tweet with commentary**; Buffer's `metadata.twitter.retweet` field only does a plain retweet (no comment). Likes are not possible via Buffer at all: there is no like mutation.

## Framework: Next.js track

Same content model, same SEO requirements, different route mechanics.

- `app/blog/page.tsx` — the index. `app/blog/[slug]/page.tsx` — the post. `app/blog/tag/[tag]/page.tsx` — tag pages.
- Export `generateStaticParams()` from each dynamic route so every post and tag page is rendered at build time rather than per request.
- Export `generateMetadata({ params })` per post for title, description, canonical, and OG image. Add `Article` JSON-LD in the post page itself.
- Feed `app/sitemap.ts` from the same post list that `generateStaticParams` uses — import it, do not maintain a parallel array. Post URLs then reach IndexNow automatically.
- There is no prerender ROUTES array to extend, and adding a post does not require touching a build script.
- Publishing a post still requires a rollout, since the pages are built. If posts need to go live without a deploy, use `revalidate` on the route (ISR) and say so explicitly rather than switching the pages to dynamic.
- Share images: pre-generate per post into `public/share/blog/<slug>.png` with the Sharp script and reference them from `generateMetadata`.

See `/senternet-site-framework` for the full convention map.
