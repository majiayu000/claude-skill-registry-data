---
name: legal-pages
description: "Scaffolds production-ready legal page templates for a website: Privacy Policy, Terms of Service, Cookie Policy, Cookie Consent banner, Refund Policy, Contact / Imprint. Templates are clearly marked as a starting point — the user must customize and have a lawyer review before going live."
---

# /legal-pages

Scaffolds the legal pages a public website needs. Output is a **starting template** — clearly marked at the top of each file: "This is a template. Have a lawyer review before going live."

## Why this exists

Almost every public website needs at least: a Privacy Policy, Terms of Service, and (for EU/UK visitors or any tracking) a Cookie Policy plus consent banner. Without these:

- You expose yourself to GDPR / CCPA / PIPEDA / LGPD fines.
- You can't legally collect any user data, including IP/cookies/analytics.
- App stores reject mobile apps.
- Payment processors reject your account.
- Search engines (and your users) treat you as low-trust.

This skill produces baseline templates so you can launch — but they're **templates, not legal advice**. You always need a lawyer to review for your jurisdiction and business model.

## When to use

- Starting a new website project.
- An existing site has no legal pages.
- Adding a new feature that changes data handling (analytics, payments, user accounts, cookies).
- After a `/web-launch-check` flagged missing legal pages.

## What it produces

### 1. Privacy Policy (`/privacy` or `/privacy-policy`)

Sections every privacy policy needs:

- **Who we are** — legal entity name, address, contact email.
- **What data we collect** — categorized:
  - Information you give us (name, email, payment, content uploaded).
  - Information we collect automatically (IP, browser, device, cookies, usage).
  - Information from third parties (OAuth providers, analytics, advertisers).
- **Why we collect it** — legitimate interest, contract performance, consent, legal obligation. Be specific.
- **Who we share it with** — sub-processors (hosting, analytics, email, payment, support). List by category if not by name.
- **How long we keep it** — retention periods.
- **Your rights** — access, correction, deletion, portability, objection, withdraw consent.
- **How to exercise rights** — email address or DSAR endpoint, response within 30 days.
- **International transfers** — if servers are in another country, name the safeguards (SCCs, adequacy).
- **Children's privacy** — if not for under 13/16, say so explicitly.
- **Cookie policy** — link to the dedicated page or include a section.
- **Changes** — how you'll notify users of changes.
- **Contact** — DPO if you have one, or general contact.
- **Effective date** — last updated date at the top.

### 2. Terms of Service (`/terms` or `/terms-of-service`)

- **Acceptance** — by using the site, you accept these terms.
- **Eligibility** — minimum age, geographic restrictions.
- **Account** — registration, security, termination.
- **Acceptable use** — what users may and may not do (no harassment, no scraping, no IP infringement).
- **User content** — who owns it, what license you take, content moderation.
- **Payments** — pricing, billing, refunds, taxes.
- **Intellectual property** — your IP, trademarks, copyright.
- **Disclaimers** — service "as is," limitations of liability, indemnification.
- **Termination** — when you can suspend or terminate accounts.
- **Governing law** — which jurisdiction's law applies, dispute resolution (arbitration clauses are tricky — consult a lawyer).
- **Changes** — how you'll notify users.
- **Contact** — for legal notices.

### 3. Cookie Policy (`/cookies`) and consent banner

- **What cookies we use** — categorized:
  - Strictly necessary (always on, no consent needed).
  - Functional (preferences, language).
  - Analytics (Plausible/GA/etc.).
  - Marketing (Meta Pixel, Google Ads, etc.).
- **Per-cookie table** — name, purpose, expiry, first-party / third-party.
- **How to manage** — link to settings UI, browser settings.

Banner pattern:

```
┌─────────────────────────────────────────────────────────────┐
│ We use cookies to make this site work.                      │
│ Optional: analytics + marketing cookies (only with consent).│
│                                                             │
│ [Accept all]  [Reject all]  [Customize]                     │
└─────────────────────────────────────────────────────────────┘
```

Rules the banner must follow:
- "Reject all" must be as easy as "Accept all" (no hidden behind clicks).
- No tracking/analytics scripts load until consent is given.
- Choice persisted (cookie or localStorage) so the user isn't asked again.
- Settings page lets the user change their mind.

### 4. Refund / Cancellation Policy (`/refunds`)

For any e-commerce or paid product:

- **Refund window** — typical 14–30 days, longer is friendlier.
- **What's refundable** — and what's not (digital goods consumed? services rendered?).
- **How to request** — link or email.
- **Processing time** — when the user gets their money back.
- **Cancellation** — for subscriptions, how to cancel and when it takes effect.

EU-specific: 14-day cooling-off period for distance contracts (Consumer Rights Directive).

### 5. Contact / Imprint (`/contact` or `/imprint`)

- **Legal entity name** (e.g., "Acme Inc.", "Acme GmbH").
- **Registered address.**
- **Email** — at least one human-monitored.
- **Phone** — required in some jurisdictions.
- **Tax / company registration number** — required in EU (Impressum), UK (Companies House number).
- **VAT number** — if EU/UK.
- **Responsible person** — director / managing partner — required in some EU countries.

### 6. (Recommended) Accessibility Statement (`/accessibility`)

- WCAG conformance level (AA target).
- Known issues being worked on.
- Contact for accessibility complaints.

Required by the European Accessibility Act for many sites in the EU. Strongly encouraged elsewhere.

### 7. (Recommended) Security disclosure (`/.well-known/security.txt`)

```
Contact: mailto:security@example.com
Expires: 2027-01-01T00:00:00.000Z
Preferred-Languages: en
Canonical: https://example.com/.well-known/security.txt
Acknowledgments: https://example.com/security-thanks
```

## Operating method

1. **Detect the framework** — Next.js, Astro, plain HTML, etc.
2. **Detect what exists** — don't overwrite an existing privacy policy.
3. **Ask the user** for the minimum information needed:
   - Legal entity name
   - Contact email
   - Registered address (or "remote / TBD")
   - Jurisdiction (US, EU, UK, other)
   - What data is collected (none / analytics-only / accounts / payments / content)
   - Age requirement (none / 13+ / 16+ / 18+)
4. **Generate the pages** with placeholders clearly marked `[REPLACE: ...]`.
5. **Wire them into the layout** — footer links to all required pages.
6. **Add the cookie banner** if any tracking is used.
7. **Print a "still to do" list** — every placeholder, every legal review needed.

## Output format

Each file starts with:

```html
<!--
  TEMPLATE ONLY — NOT LEGAL ADVICE.
  Have a lawyer in your jurisdiction review before going live.
  Last template update: {{date}}
  Generated by Claude Code Toolkit's /legal-pages skill.
-->
```

After generation, summary:

```
## Generated
- /src/pages/privacy.mdx — Privacy Policy template
- /src/pages/terms.mdx — Terms of Service template
- /src/pages/cookies.mdx — Cookie Policy template
- /src/components/CookieBanner.tsx — Cookie consent banner
- /src/pages/refunds.mdx — Refund Policy template (because you mentioned payments)
- /src/pages/contact.mdx — Imprint / Contact

## Wired into layout
- Footer now links to /privacy, /terms, /cookies, /contact

## Placeholders to fill in (search for [REPLACE:)
1. [REPLACE: legal entity name] — appears in 4 places
2. [REPLACE: registered address] — privacy.mdx, contact.mdx
3. [REPLACE: data retention period] — privacy.mdx
4. [REPLACE: governing law jurisdiction] — terms.mdx

## Before launch
- [ ] Have a lawyer review.
- [ ] Check that no tracking scripts load before consent.
- [ ] Confirm sitemap.xml includes the legal pages.
- [ ] Set the effective date on each page.
```

## Boundaries

- **Templates only.** Always remind the user this is not legal advice.
- **Don't pretend to be a lawyer.** Flag any time the user is making a choice that has real legal weight (arbitration clauses, GDPR lawful basis, content moderation policy).
- **Don't generate jurisdiction-specific clauses without asking.** EU/UK/CA/US/Brazil/etc. have meaningfully different requirements.
- **Default to the friendly choice** when ambiguous — easier refund, longer cooling-off, plain language. Aggressive ToS clauses are user-hostile and often unenforceable.
- **Never fabricate a real address or phone number.** Use `[REPLACE: ...]` placeholders.
