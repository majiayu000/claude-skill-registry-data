---
name: image-seo
description: Audit and fix a page's images for search, speed and accessibility. Covers alt text, filenames, WebP/AVIF, sizes and srcset, lazy loading, the LCP image, image sitemaps, og:image and licence metadata. Use for "write alt text", "optimize my images", "images not in Google Images", "LCP is my hero image", "properly size images".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/image-seo
---

# Image SEO

Review every image on a page or template for the three jobs images do in search: being understood (alt text, context, filenames), being found (indexable markup, sitemaps, social previews) and not slowing the page down (format, size, loading). You hand back per-image fixes with priorities and an alt-text batch the user can paste straight into their CMS.

> **Romeo's rule:** Every image is content, decoration or a button; write its alt text for the job it does, not for the keyword you wish it ranked for.

## Use this when

- Someone asks to "write alt text", "optimize images" or "compress images" for a page, a blog or a product catalogue.
- PageSpeed Insights flags image audits ("Improve image delivery", "Properly size images", "Image elements do not have explicit width and height") or names an image as the LCP element.
- The site's images don't appear in Google Images, or image search traffic dropped after a redesign or CDN change.
- Shared links show the wrong image, a cropped logo or no preview on LinkedIn, Slack, WhatsApp or X.
- A shop's product photos need a consistent standard before a catalogue launch.
- A photographer, illustrator or publisher wants credit and licensing information shown in Google Images.

## Don't use this for

- Page speed problems beyond images (JavaScript, fonts, server response, third-party tags) → `technical-seo-audit`.
- Product feeds, Merchant Center image disapprovals and category-page structure → `ecommerce-seo-audit`.
- A full structured data graph for the page (images are only one property) → `schema-markup`.
- Reviewing the whole page against its target query → `on-page-seo-review`.

## What you need

### Required

- The page URL(s) or HTML, and for each page the topic or target query (alt text depends on context).
- For the alt-text batch: the list of images (file URL plus where it appears) or the images themselves, so you can see what they show.

### Helpful

- A crawler export with image data (for example Screaming Frog's Images tab: source, alt, file size, dimensions, inlinks).
- PageSpeed Insights or Lighthouse results for mobile, including the LCP element, and Chrome UX Report field data.
- Search Console Performance with search type "Image", to see which images already earn traffic before renaming anything.
- The CMS and image pipeline: WordPress media library, Shopify, Next.js `<Image>`, an image CDN (Cloudflare, Cloudinary, imgix) and its settings.
- Original image files, if licence metadata or product photo standards are in scope.

### No tools?

Open the page in Chrome, then DevTools → Network → filter "Img" to see each image's format, transferred size and dimensions. In the Console, this one line lists every `<img>` with what you need: `console.table([...document.images].map(i=>({src:i.currentSrc,alt:i.getAttribute('alt'),natural:i.naturalWidth+'x'+i.naturalHeight,shown:i.clientWidth+'x'+i.clientHeight,loading:i.loading,priority:i.fetchPriority,w:i.getAttribute('width'),h:i.getAttribute('height')})))`. PageSpeed Insights names the LCP element for free. Facebook's Sharing Debugger and LinkedIn's Post Inspector show the social preview. If you can only see view-source, review the `<img>` tags and `og:` meta tags and mark everything else "not checked".

## Ground rules

- Alt text follows the image's job. Content image: describe what it shows that matters in this context. Decorative image: `alt=""` (empty, not missing; with no alt at all, many screen readers read out the filename). Linked or button image: describe the destination or action ("Download the 2026 price list"), not the picture. Image of text: the alt contains the text. Chart: a short alt plus the numbers in nearby text or a table.
- Write alt text for people first. The query goes in only when it honestly describes the image. Keyword-stuffed alt text is an accessibility failure, and Google's image guidelines warn it can be seen as spam.
- Google indexes images from `<img src>` (including inside `<picture>`), not CSS backgrounds. Anything that should appear in image search, or that is the page's main image, goes in `<img>`. CSS backgrounds are fine for decoration.
- Never lazy-load the LCP image. Give it `fetchpriority="high"`, a plain `src` in the HTML, and no carousel or JavaScript between it and the browser.
- Every `<img>` gets `width` and `height` attributes (or a CSS `aspect-ratio`) so the browser reserves space. Image-driven layout shift is the cheapest CLS fix there is.
- Dimensions usually save more bytes than formats. A 4000 px photo shown at 800 px is wrong in any format.
- Don't rename or move images that already earn image search traffic unless you redirect the old URLs; filename fixes are for new uploads.
- Original images (your screenshots, products, team, data charts) are worth more than stock photos that appear on hundreds of other sites.
- Keep one URL per image. Google asks for the same image URL wherever the image is reused so it can be cached; random cache-busting query strings or per-page copies waste crawl and browser cache.

## Steps

1. **Inventory.** For every image on the page or template, record: file URL, format, transferred bytes, natural size, displayed size at a 390 px phone width and a 1366 px desktop width, `alt`, `loading`, `fetchpriority`, `width` / `height`, whether it's inside a link, whether it's `<img>` or a CSS background, its caption, and its job (content, decorative, functional, text, chart).
2. **Find the LCP image.** Use PageSpeed Insights (mobile) "Largest Contentful Paint element", or the Performance panel.
   - If it's an image: no `loading="lazy"`, has `fetchpriority="high"`, is in the initial HTML (not `data-src` swapped in by script, not a CSS background), served at the right size for mobile.
   - If it's a CSS background or injected late, add `<link rel="preload" as="image" fetchpriority="high">` (with `imagesrcset` / `imagesizes` for responsive images) or move it into an `<img>`.
   - `loading="lazy"` on the LCP image = `Fix now` when field LCP is over 2.5 s, otherwise `Fix next`. Lazy loading on other images likely in the first mobile viewport = `Fix next`.
3. **Alt text.** Classify each image and check it.
   - Missing `alt` on content images = `Fix next` (accessibility and missed context). Filename or camera alt ("IMG_2034", "image", "photo") = `Fix next`.
   - Same alt on every product photo, or the query pasted into every alt = `Fix next`.
   - Alt on decorative icons and dividers ("icon", "arrow") = `Worth doing`: set `alt=""`.
   - A linked image with empty alt and no text in the link means the link has no accessible name = `Fix next`.
   - Length: say what matters and stop. Most good alts are one short sentence; if it needs a paragraph, put that in a caption or the body text.
4. **Filenames.** Descriptive, lowercase, hyphenated: `IMG_2034.jpg` → `grey-cat-asleep-on-laptop.jpg`. Localise for localised pages. Set the rule for future uploads (`Worth doing`); leave old filenames alone (`Leave it`) unless the image earns no traffic and is being replaced anyway.
5. **Format and compression.** Google Search supports BMP, GIF, JPEG, PNG, WebP, SVG and AVIF.
   - Photos: AVIF or WebP, with a JPEG fallback through `<picture>` or CDN content negotiation (`Accept` header, with `Vary: Accept`). Current major browsers support both; keep the fallback for older devices, email and some crawlers.
   - Screenshots and flat graphics: WebP (lossless if text looks soft), or PNG when transparency is needed. Logos and icons: SVG (sanitised, with `<title>` when inline and meaningful).
   - Animated GIFs over about 1 MB: convert to MP4 or WebM in `<video autoplay muted loop playsinline>`.
   - Working byte targets at the displayed size (judgement, not a Google rule): hero or LCP image under roughly 150 to 200 KB on mobile, in-content images under about 100 KB, thumbnails under about 30 KB. Over 500 KB on a key template = `Fix next`; over 1 MB = `Fix now`. Start around quality 50 to 60 for AVIF, 75 to 80 for WebP and JPEG, then check by eye.
6. **Dimensions and responsive images.** Natural width should be no more than about 2× the largest displayed width.
   - Use `srcset` with width descriptors (for example 480w, 800w, 1200w, 1600w) and a `sizes` value that matches the layout. A common bug: `sizes="100vw"` on an image shown at a third of the screen makes phones and desktops download roughly 3× the bytes they need.
   - Pattern for a below-the-fold content image:

   ```html
   <picture>
     <source type="image/avif" srcset="/img/audit-report-800.avif 800w, /img/audit-report-1600.avif 1600w" sizes="(min-width: 960px) 720px, 100vw">
     <source type="image/webp" srcset="/img/audit-report-800.webp 800w, /img/audit-report-1600.webp 1600w" sizes="(min-width: 960px) 720px, 100vw">
     <img src="/img/audit-report-800.jpg" srcset="/img/audit-report-800.jpg 800w, /img/audit-report-1600.jpg 1600w" sizes="(min-width: 960px) 720px, 100vw" width="1600" height="900" alt="SEO audit report listing three crawl errors, each marked Fix now" loading="lazy" decoding="async">
   </picture>
   ```

   - For the LCP image use the same markup without `loading="lazy"` and with `fetchpriority="high"` on the `<img>`.
7. **Layout shift.** Every `<img>` has `width` and `height` matching its aspect ratio, with CSS `max-width: 100%; height: auto;`. Missing dimensions on above-the-fold images = `Fix next`; elsewhere `Worth doing`. Check field CLS ≤ 0.1 at the 75th percentile.
8. **Lazy loading and discovery.** Native `loading="lazy"` for images below the fold. Script-based lazy loaders that leave a placeholder in `src` and the real URL in `data-src` are a discovery risk: check URL Inspection's crawled HTML shows the real image URLs. If not, switch to native lazy loading = `Fix next`.
9. **Indexability.** Image URLs return 200, aren't blocked in robots.txt (check the CDN host's own robots.txt too), carry no `X-Robots-Tag: noindex` and don't need cookies. A page-level `noimageindex` keeps its images out. Verify a separate image CDN host in Search Console to see its crawl errors. WordPress attachment pages (one thin page per image) should redirect to the file or parent post; WordPress 6.4+ turns them off on new installs, but older sites and some plugins still expose them.
10. **Context.** Put images next to the text they illustrate, under a relevant heading. Captions help readers where an image needs explaining; don't add them only for SEO. The page title, heading and surrounding text all feed how Google understands the image.
11. **Image sitemap (only where it helps).** Useful when images load via JavaScript, live on a CDN host, or image search matters to the business (photography, recipes, products, property). Only `<image:image>` and `<image:loc>` are supported; caption, title, geo_location and licence tags were deprecated in 2022. Up to 1,000 images per `<url>`. A typical blog with images in plain HTML doesn't need one (`Leave it`).
12. **Preferred image and social previews.**
    - `og:image`: absolute URL, at least 1200 px wide, 1.91:1 (1200×630 is the safe default), JPEG or PNG for the widest platform support, plus `og:image:alt`. Add `twitter:card` = `summary_large_image`. Missing or the logo on key pages = `Fix next`.
    - Allow large previews with `<meta name="robots" content="max-image-preview:large">`. Google Discover wants images at least 1200 px wide, over 300,000 pixels, ideally 16:9, and not a logo or text-heavy graphic.
    - To suggest the page's main image to Google, use `og:image`, schema.org `primaryImageOfPage`, or the `image` of the page's main entity. Pick a representative image; avoid logos, text-heavy images and extreme aspect ratios.
13. **CDN and caching.** Fingerprinted image URLs served with `Cache-Control: public, max-age=31536000, immutable`. One canonical URL per image and size, with no session or tracking parameters. Check the CDN's automatic format conversion actually serves AVIF or WebP (look at the response `content-type`, not the file extension).
14. **Licensing metadata (when credit or licensing matters).** Embed IPTC fields once per file: Creator, Credit Line, Copyright Notice, Web Statement of Rights (required for the "Licensable" badge in Google Images) and Licensor URL. Or use `ImageObject` structured data on each page: `contentUrl` plus `license`, `acquireLicensePage`, `creditText`, `creator`, `copyrightNotice`. If both exist and disagree, Google uses the structured data. Many CMSs and CDNs strip metadata when compressing; check a served file still carries it. For AI-generated images, the IPTC Digital Source Type value `trainedAlgorithmicMedia` declares it.
15. **Product images (shops).** Several images per product: a clean main shot on a plain background with no watermark, promotional text or borders (Merchant Center rejects those for the main image; check its current image requirements), then angles, scale, detail and in-use shots. High resolution so zoom works. Each variant (colour, finish) gets its own images and alt text naming the variant. The same main image in the `Product` `image` property, the page and the feed. Category thumbnails are real `<img>` elements with alt text naming the product.

## What to hand back

Per-image fixes first, then the alt-text batch.

```markdown
# Image review: <page or template> (<date>)

**What I found:** <one plain-English sentence>
**What matters most:** <one sentence>
**What to do first:** <one sentence>

## Page-level findings
- LCP element: <image file or "text"> · lazy-loaded: yes / no · fetchpriority: <value> · field LCP: <value or "not checked">
- Total image bytes on mobile: <KB> across <n> images · largest: <file, KB>
- og:image: <URL, size> or "missing" · max-image-preview: <value>

## Fixes (priority order)
### 1. <file name> · `Fix now`
- Problem: <plain English, then the term in brackets>
- Evidence: <bytes, dimensions, attribute seen> · seen / tool / inferred · confidence: high / medium / low
- Fix: <exact change, e.g. remove loading="lazy", add fetchpriority="high", export at 1200 px AVIF q55>
- Markup: <before → after snippet when the HTML changes>

## Alt-text batch (paste into the CMS)
- <file URL> | content | "<current alt or MISSING>" → "<new alt>"
- <file URL> | decorative | "<current alt>" → "" (empty)
- <file URL> | link to <destination> | "<current alt>" → "<action or destination>"

## Leave it
- <thing>: <why it isn't worth changing>

## What I could not check
- <item>: <what would verify it>
```

## Stop and flag if

- You can't see an image you're asked to write alt text for. Don't guess from the filename; ask for the image or a description, or mark that line "needs a look".
- An alt-text request is really "put our keyword in every alt". Explain why it hurts and write honest alts instead.
- A fix means renaming, moving or re-compressing images that already earn image search traffic. Flag the traffic risk and propose redirects first.
- Changes need edits to the live theme, CDN, robots.txt or media library. Draft them; apply nothing without explicit permission for that change.
- Output with generic advice ("compress your images", "add alt text") instead of named files, exact attribute changes and pasteable alts is not acceptable.

## Next step

- LCP still slow after the image fixes → `technical-seo-audit` with the PageSpeed Insights report and the LCP breakdown.
- Product images feed a shop → `ecommerce-seo-audit`, passing the product image standard you set here.
- Images fixed as part of a page refresh → `on-page-seo-review` on the same URL and target query.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
