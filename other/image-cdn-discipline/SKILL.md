---
name: image-cdn-discipline
description: Use when an app serves a large image catalog (hundreds to tens of thousands of images), when choosing where image bytes live, when grids scroll slowly or detail views load blurry art, or when standing up or migrating an image CDN (R2, Cloudinary, S3+CloudFront). Carries the two-tier thumbs/full layout, the one-helper-per-platform URL rule, images-never-in-git, the dev-domain-is-not-production caching trap, thumb-while-full-loads, image-first sorting, and client cache sizing. Triggers on image CDN, R2, thumbnails, image tiers, slow image loading, blurry images, cache miss, custom domain CDN, image hosting, "images in git", grid images.
---

# Image CDN Discipline

How a multi-platform app serves a large image catalog without slow
grids, blurry detail views, or a bloated repo. Distilled from serving
~18,000 card images to iOS, Android, and web from Cloudflare R2 (BOBA
Playbook), including the measured production failure of the dev
domain.

## The two-tier layout

Publish every image at two sizes, under two prefixes:

| Tier | Size | Weight | Used by |
|---|---|---|---|
| `thumbs/{file}` | ~200px WebP | ~10 KB | every grid cell |
| `full/{file}` | ≤1200px WebP | ~80 KB | detail views, share images |

- **Grids never load `full/`.** A 3-column grid scrolling 10k items
  on thumbs is smooth; on full images it's a network and memory
  disaster.
- **Detail views show the thumb immediately while full loads behind
  it.** The thumb is already in cache from the grid the user just
  tapped — a blurry-then-sharp swap beats a spinner every time.
- **Grid cells constrain BOTH width and height before clipping.**
  A cell constrained on one axis lets an odd-aspect image blow the
  layout.
- **Verify the tier's actual resolution before building features on
  its claim.** One project's docs said `full/` was "≤1200px"; the
  real files ranged 477–745px, and a 3D feature that rendered them at
  1080×1920 shipped "thumbnail blown up" blur. When a rendering
  feature needs more pixels, the authoritative fix is regenerating
  the tier at higher resolution — perceptual masking (upscalers,
  sharpening) is a stopgap that hides the defect, not a fix.

## One URL helper per platform

**Never hardcode CDN URLs.** Each platform gets exactly one pair of
helpers — `thumbUrl(f)` / `fullUrl(f)` in `js/api.js`, `CDN.swift`,
`Cdn.kt` — and every image load routes through them. The payoff is
concrete: flipping the CDN base (dev domain → custom domain, bucket
migration, provider change) is a one-line change per platform instead
of a repo-wide grep-and-pray.

## Images never live in git

The repo carries JSON metadata only; image bytes live exclusively on
the CDN. Reasons: clone speed, host storage caps (GitHub's soft 1 GB
limit), and the fact that images have their own lifecycle (re-
optimization, re-sourcing) that shouldn't churn git history. If the
optimizer needs source masters, they live on the maintainer's machine
or object storage — documented, not committed.

## The dev-domain trap (measured)

Provider dev/preview domains (e.g. `*.r2.dev`) are **rate-limited and
weakly cached by design** — they're documented as not-for-production,
and the docs mean it. Measured on a real catalog: 9 KB thumbnails took
**6.8–9.6 s on edge-cache misses** vs ~0.2 s on hits, with no cache
headers at all. With a large catalog, the long tail of rarely-viewed
images is *perpetual misses* — deep-catalog browsing crawls on every
platform and no client-side fix can help.

- Production requires a **custom domain attached to the CDN zone** so
  real edge caching applies. (For R2 that means the zone must be on
  Cloudflare DNS — check the nameserver prerequisite early; it can be
  the actual blocker.)
- **Do the domain move BEFORE any bulk asset regeneration**, so the
  new bytes land behind a real cache instead of warming a domain
  you're about to abandon.
- Client-side amplifiers (eager loading, main-thread decode,
  per-render full-catalog filters) make CDN latency look worse — fix
  them too, but don't mistake them for the root cause. Instrument and
  measure a cache miss directly before concluding.

## Trust the asset reference, not a flag

If a record has a non-empty asset field, load it — even when a
redundant `imageAvailable`-style boolean says false. Real catalogs
ship records with stale availability flags alongside perfectly valid
assets; gating on the flag hides good images. Let the CDN 404
gracefully for the truly-missing and show the placeholder then.

## Image-first sorting

**Every list and grid sorts items WITH images ahead of image-pending
placeholders** — as the primary sort key, on every surface. A wall of
placeholders at the top of a grid reads as "the app is broken," even
at 90% coverage. Coverage gaps belong at the bottom, where the user
scrolls into them already trusting the catalog.

## Client cache sizing

Defaults are sized for apps with a handful of images, not catalogs.
Configure deliberately at launch:

- **iOS**: `URLCache` ~100 MB memory / ~500 MB disk, shared by every
  image request path (including any `AsyncImage` session override).
- **Android**: Coil memory (~60 MB) + disk (~500 MB) caches sized to
  match the iOS budget, on the shared OkHttp client.
- **Web**: the browser handles it — but only if the CDN sends real
  cache headers, which is the custom-domain point above.

## Related

- One-asset-per-entity byte-collision guard (md5 pass before CDN
  sync): see `canonical-entity-identity`.
- Client-side recycled-cell image bugs: see `ios-production-gotchas`.
- Publishing the metadata catalog itself: see
  `shared-data-plane-contract`.

## Never put art you did not author into a box that reshapes it

A catalog whose images come from many sources does **not** have one aspect
ratio, and assuming it does is a defect that ships looking fine on the samples
you checked.

Measured across one real catalog's poster sources (width/height):

```
tmdb .67   omdb .68   tvdb .68   fanart .70   generated .67    <- poster-shaped
commons  .67-1.38     archive 1.28-1.76      wikidata 1.33-2.37 <- arbitrary stills
```

So the rule is not "everything is 2:3". It is **never reshape it**: fit at the
image's own intrinsic aspect, bound one dimension, let the other follow.

Two failure modes, and the second is the one that bites on the fix:

1. **Crop-scaling a portrait poster into a wide hero box.** A 2:3 poster
   center-cropped to ~2.4:1 is a horizontal sliver — unrecognizable as a
   poster, which also reads to users as "you are not using the good artwork."
   Live here on 85.7% of a catalog, because the hero did
   `backdrop ?? poster` and most items have no backdrop.
2. **"Fixing" it by forcing a 2:3 frame.** That letterboxes the landscape
   sources inside a floating black box. The first fix was this, and the device
   showed it immediately.

```kotlin
// WRONG — reshapes            // WRONG — assumes one shape
ContentScale.Crop              Modifier.aspectRatio(2f/3f)
// RIGHT — height-bounded, width from the image's own intrinsics
ContentScale.Fit
```

Practical companions:

- Fill the empty space with an **ambient wash**: the same image, crop-scaled
  and heavily blurred, behind the fit copy. It reads as intentional rather than
  as a gap.
- Draw the fit image **above** any scrim. Hero scrims usually end fully opaque,
  so art placed under one loses its bottom third.
- `backdrop ?? poster` is a bug anywhere the destination is not the poster's
  own aspect. Grep for that fallback specifically — it was live in five
  surfaces on one platform.
- **Gate curated shelves on professional artwork**, not the weaker
  "has *some* designed art" flag, which admits machine-generated frame grabs.
  Never gate a user's own **favorites** that way: hiding someone's saved title
  for its artwork is a different thing from curating a shelf.

Measure before assuming — one `HEAD`/decode pass over a sample per source
settles the aspect question in minutes and would have skipped the wrong fix.
