---
name: snaap-perf
description: >
  Use when touching images, bundles or fonts. Enforces the 200KB gzipped budget, mandatory
  next/image sizes, and the "measure the KES cost on 4G" rule.
---
# Snaap performance

Audience: mid-range Android, Slow 4G, metered data. **Payload size is a business metric — every KB
costs the customer KES.**

**Budget:** initial JS ≤ 200KB gzipped, LCP ≤ 2.5s on Slow 4G, CLS < 0.1. The budget beats
aesthetics; state what you cut.

**Images:** every `next/image` passes a correct `sizes` — never ship a `w=3840` rendition for a
220px card. The Cloudinary cloud is `dltfgasbb`. Convert plain `<img>` galleries to `next/image`
with a responsive srcset. Export the logo small (SVG or ~80px), not a 500px JPEG at 40px.

**Bundles:** keep admin-only libraries (e.g. `@mui/x-charts`) out of the storefront bundle — prove
it, dynamic-import if needed. Don't statically import heavy client-only libs into `_app.js`.

**Data:** fetch what you display (the homepage fetched 120 to show 48). Prefer static / ISR.

**Always report before/after gzipped KB and the KES-per-view saved on 4G.**
