---
name: snaap-sections
description: >
  Use when working on homepage sections, promo cards, the Safaricom Corner or the Lipa Mdogo Mdogo
  section. Covers the extended HomepageSection model, server-authoritative scheduling and the
  stock-validation rule.
---
# Homepage sections

Built on the existing `/homepage-sections` API (SafaricomCorner already consumes it). P3 extends
it — do not build a parallel system.

**Scheduling is server-authoritative.** Expiry is evaluated in `getStaticProps` in Africa/Nairobi
time (no DST), never in the browser. Publishing or expiring triggers ISR revalidation. An expired
card must not render even from a stale page.

**Exactly one H1.** The announcement card owns the homepage `<h1>`. If none is scheduled, fall back
to the evergreen H1. Never zero, never two.

**Stock validation is a hard requirement.** A card is publishable only if its CTA resolves to
something real:
- `ctaType: "product"` → a published product that exists.
- `ctaType: "browse"` → a filter URL returning ≥ 1 in-stock product.
- `ctaType: "whatsapp"` → allowed with no stock (we sell to order), but then the badge must say
  PRE-ORDER or ORDER ON REQUEST, never NEW IN STOCK.

Prefer deep links (`/products/<id>`) over `?brand=` filters — they convert better and give Google
internal links straight to product pages. Show the resolved product count in admin and flag any
card that has fallen to zero.

**Lipa Mdogo Mdogo section:** driven by a per-product `lipaMdogoMdogoEligible` boolean (plus an
optional one-line summary), never by string-matching the description. No global figures anywhere.

**Images:** placeholders served from our Cloudinary cloud (`dltfgasbb`), never
`res.cloudinary.com/demo`; surface a "placeholder, needs replacing" flag in the admin list.
