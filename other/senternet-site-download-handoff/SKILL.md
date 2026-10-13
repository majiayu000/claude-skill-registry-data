---
name: senternet-site-download-handoff
description: Add mobile-to-desktop download handoff to a desktop app marketing site, offering email, native share, copy, and an explicit download-anyway option.
---

# Desktop download handoff

Keep mobile visitors interested in a desktop app by helping them reach its download page on a compatible computer. Apply this to desktop-only app downloads; preserve existing mobile app or web app flows.

## Adapt to the product

Inspect supported operating systems, every download CTA (including footer, pricing, install, and post-purchase pages), download aliases, analytics consent, transactional email, abuse controls, and rendering conventions. Reuse existing infrastructure. Do not infer the target desktop OS from the phone OS. A Mac-only app should say “your Mac”; a cross-platform app should list its supported desktop systems.

Use one shared panel in two contexts: inline on the download/install destination for mobile visitors, and in an accessible dialog or bottom sheet opened by mobile download CTAs. Desktop download links remain direct, crawlable anchors; modified clicks retain normal behavior. Detect phones and tablets, including iPadOS desktop user agents, without treating a narrow desktop window as a phone. Server/prerender output and the first client render must agree; perform detection after hydration or at click time.

## The four options

Explain briefly that the app runs on a computer and offer these in order:

1. **Email me the download link** — primary action, with a labeled email field and Send link button. Use the existing transactional sender when available. State that the address is used only for this email, with no mailing-list signup or account required. Show pending, invalid, success, throttled, and failed states; only report sent after the service accepts the request. Identify the sender domain and suggest checking spam.
2. **Share download link** — invoke native Share immediately within the user gesture. Do not await a backend call first. Cancellation is neutral; an unavailable or failed Share API falls back to Copy.
3. **Copy download link** — independently visible even when Share exists. Report success only after clipboard success; if unavailable or denied, expose a selectable read-only link with manual-copy instructions.
4. **Download here anyway** — an explicit expandable last option. Explain that the installer can be saved to Files/cloud storage and transferred later. Label each supported platform/format; do not silently choose a desktop platform for a phone. Actual downloads retain existing download measurement and bypass the handoff interception.

All methods share a stable first-party download/install *page* URL, not a versioned installer, expiring asset, localhost URL, or license/activation URL. Reuse an existing suitable destination; a new route must follow the site's route, sitemap, metadata and prerender contracts. Never include recipient addresses or purchase secrets in handoff links. If an existing attribution system uses opaque tokens, keep the same token across methods, honor consent, and retain a working plain URL when minting fails. Token infrastructure is optional, not a prerequisite for the UX.

## Delivery and interaction

For server-sent email, restrict the payload to the address and any explicitly supported attribution fields. The server owns sender, subject, body and destination; never accept arbitrary content or redirect URLs. Validate addresses, reuse App Check or equivalent abuse controls, and enforce atomic per-recipient and per-source limits before sending. Fail closed if limits cannot be checked. Avoid logging raw addresses or provider payloads; retain only necessary abuse records with an explicit cleanup policy. Email is transactional and must work without analytics consent. Update the site's privacy explanation and backend operations documentation.

Use existing button and surface styles. Support keyboard focus containment, Escape, focus restoration, background scroll locking, accessible names and live status feedback. Keep controls at least 44px high and mobile inputs at least 16px. Avoid loading anti-abuse services or sending requests during prerender; initialize email dependencies when the user needs them.

Measure handoff views and method selection separately from completed method actions and actual installer clicks, through the existing consent gate. Do not count opening the panel, manual-copy instructions, or a canceled share as a completed download. Never include email addresses or personal URLs in analytics.

## Verify

Exercise the actual browser flow on a phone, Android tablet, iPadOS desktop UA, and a narrow desktop viewport. Cover all CTA placements, inline destination, dialog dismissal/focus restoration, no-overflow layout, email success/failure/rate-limit, Share cancellation, denied clipboard/manual copy, and download-anyway escape. Check desktop links and hydration. Test server validation, replay/abuse limits, provider failure, and trusted destination. Use mocks for delivery tests; real email requires an explicitly authorized recipient. Report local verification separately from deployment and real email receipt. Do not infer deployment authorization from a request to implement the feature.

## Framework: Next.js track

Use a small client component for detection and browser APIs. Keep initial SSR markup deterministic; never access navigator while rendering on the server. Use the existing route handler/server email service and metadata conventions instead of Firebase Hosting rewrites or Puppeteer prerender steps. The four-option behavior and verification contract are unchanged.
