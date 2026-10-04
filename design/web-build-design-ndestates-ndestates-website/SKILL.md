---
name: web-build-design
description: 'Web build & design specialist for NDestates-io marketing sites, SaaS landings, pricing pages, gated download portals, and customer-facing flows using Laravel + Livewire + Blade + Tailwind (Filament 5 for admin). Creative-tim inspired modern SaaS aesthetics, pricing tables, conversion-focused CTAs, PayPal integration UX, license delivery. Use for public marketing pages, trial flows, download UX, and design system consistency.'
user-invocable: true
disable-model-invocation: false
---

# Web Build & Design for NDestates IO (SaaS Marketing + Portal)

**Scope for this project**: Public marketing website (introduction/hero, products & pricing, downloads, licensing) + customer license/trial experiences. Admin is Filament 5 (Products, Licenses, Customers, Orders). Public uses Blade + Livewire + Tailwind for speed and beautiful conversion-focused UI. Payments via PayPal.

## Core Principles (always apply)

- **Conversion first, beauty second**: Hero with clear value + primary CTA ("Start free trial"), prominent pricing, frictionless trial claim (email only for demo), instant gratification on download page (license key shown + "download" affordance).
- **Creative-tim / modern SaaS inspiration** (https://www.creative-tim.com):
  - Clean white + strong indigo/blue primary (#1e40af).
  - Generous whitespace, rounded-3xl / rounded-2xl cards.
  - 3-column pricing with "MOST POPULAR" ribbon on middle/high-value tier.
  - Subtle shadows + hover lift on cards.
  - Feature lists with green check icons.
  - Prominent PayPal branding on buy buttons + "demo mode" callouts during bootstrap.
  - Trust bar (logos or "Used by Jersey Property, Premier Estates..." etc).
  - Clear "No credit card for trial" messaging.
- Mobile first, fast, accessible. Use Tailwind via CDN for rapid public prototypes (switch to Vite + Tailwind build for prod).
- License gating: Download page shows trial/purchase forms; after success, flash success + license key. Real version would verify PayPal webhook before showing download buttons or protected links.
- Livewire where interactive: pricing interval toggle (monthly/yearly), trial form with validation feedback, "claim trial for X product" modals.
- Keep marketing completely independent of Filament admin styles where possible (or share a design token layer).

## Page Structure (ndestates-io)

1. **Home / Introduction** (`/`)
   - Hero with project name + tagline ("Professional software for modern real estate").
   - Value props (e-sign closes, orchestrator connects, simple licensing).
   - Teaser product cards + "See pricing" / "Start trial" CTAs.
   - Trust logos, final CTA bar.

2. **Products & Pricing** (`/products`)
   - Detailed descriptions per product (ND E-Sign, Orchestrator, Bundle).
   - Pricing cards (see above).
   - Inline email + "Start trial" and "Buy with PayPal" forms (POST to controller).
   - Feature comparison if >3 products later.

3. **Downloads** (`/download`)
   - Central place for all software access.
   - Quick global trial form.
   - Per-product cards with "Buy (demo)" and "Free trial" actions.
   - Success state: show newly issued license key prominently + "Download / Activate" instructions.
   - Note on real fulfillment (PayPal + storage protected downloads or S3 presigned).

4. **Licensing** (`/licensing`)
   - Simple legal + product terms (trial length, what "per license" means, PayPal refunds, audit/compliance notes for e-sign).
   - Link back to downloads.

## PayPal + Trial Integration UX (see paypal-billing-integration skill)

- Trial: email capture → instant License record (status=trial, expires_at). Flash key. In future: queue email via Amazon SES skill.
- Purchase: form collects email → simulate or call PayPal Orders API / Invoicing. On success (or webhook) create License (status=active, paypal_capture_id, expires +1yr). Fulfill by showing key + download.
- Always surface the license_key to the user immediately (they copy it for activation in the actual e-ndsign`.github/prompts/orchestrator-v2.prompt.md` apps).
- Future: customer dashboard (auth) listing "My Licenses", re-download, renew via PayPal.

## Implementation Tips for this stack

- Blade components or includes for pricing-card, trial-form, license-success-banner.
- Tailwind play CDN in marketing layout for zero-build iteration (see current implementation).
- For production marketing: `npm install -D tailwindcss` + vite.config, extract to app.css, purge properly.
- Livewire components recommended for:
  - `TrialForm` (with real-time validation, product selector).
  - `PricingToggle` (if introducing monthly/annual prices).
  - `DownloadGate` (license key input → validate against DB → unlock links).
- Filament only for back-office (admin resources for Product/License already scaffolded).
- Keep copy short, benefit-led, real-estate specific ("closes deals", "audit for compliance", "connects your listings to signatures").

## Files of Note (current + future)

- `resources/views/layouts/marketing.blade.php` — shared nav, flash success, footer, Tailwind CDN.
- `resources/views/marketing/home.blade.php`, `products.blade.php`, `download.blade.php`, `licensing.blade.php`
- `app/Http/Controllers/MarketingController.php` — home/products/download/licensing + claimTrial / purchaseDemo (replace purchaseDemo with real PayPal).
- `app/Models/Product.php`, `License.php`
- Filament: `app/Filament/Resources/Products/ProductResource.php`, same for Licenses.
- Future Livewire: `app/Livewire/TrialForm.php` etc.
- New skill usage: invoke via `/web-build-design` or spawn subagent with this SKILL.md when doing landing/pricing work.

## Security & Polish

- All public forms: validate + rate limit (add throttle middleware later).
- Run security checklist after changes to forms or PayPal flows.
- After any design iteration: test on mobile + ddev + real browser.
- Accessibility: labels, focus states, sufficient contrast (blue-900 on white is strong).

Use this skill when the user asks for design changes, new landing sections, pricing experiments, download UX improvements, or "make it look like creative-tim".

Created during ndestates-io initial website build (2026-06-14).
