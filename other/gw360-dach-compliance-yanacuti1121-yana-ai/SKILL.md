---
name: dach-compliance
description: Cover Germany, Austria, and Switzerland compliance requirements that have security implications. Covers Impressum content per TMG/MStV/ECG, Datenschutzerklärung per DSGVO/TTDSG/DSG, AGB and Widerrufsbelehrung, AVV/DPA for sub-processors, technical-organizational measures (TOMs), and cookie consent that satisfies all three jurisdictions. Invoke when launching a DACH-facing site, adding third-party services, or reviewing an inherited DACH site.
---

# DACH Compliance (DE / AT / CH)

DACH markets — Germany, Austria, Switzerland — have a stricter and more enforced compliance regime than most jurisdictions. The good news: a small set of pages plus a cookie banner satisfies the common case. The bad news: missing any one of them is a real risk, particularly in Germany where commercial cease-and-desist (Abmahnung) is a small industry.

This skill is about the **technical implementation** of these requirements. It is not legal advice. For non-trivial cases (especially regulated industries, B2B SaaS at scale, or anything cross-border), retain a DACH-qualified lawyer.

## When to invoke

- Launching a website or web app to a DACH audience
- Adding new third-party services (analytics, ads, chat, AI, CRM, CDN)
- Reviewing an inherited DACH site for compliance gaps
- After an Abmahnung or Datenschutz inquiry
- Periodic review (annually is reasonable)

## The four pages every DACH site needs

| Page | Slug convention | What it is |
|---|---|---|
| **Impressum** | `/impressum` | Legal identification of the operator. Required by §5 TMG (DE), §25 MedienG (AT), and §3 lit. s UWG (CH). |
| **Datenschutzerklärung** | `/datenschutz` or `/datenschutzerklaerung` | Privacy policy compliant with GDPR + national law (TTDSG / TKG 2021 / FADP). |
| **AGB** | `/agb` | General Terms and Conditions — required for online sale of goods/services in B2C, strongly recommended in B2B. |
| **Cookie banner** | site-wide overlay | Consent UI for non-essential cookies/tracking. |

The Impressum and Datenschutzerklärung must be reachable from every page with no more than two clicks and the link text must be unambiguous. Footer links named exactly "Impressum" and "Datenschutz" are the safe pattern.

## Impressum — what must be in it

The legally required content varies slightly by jurisdiction. A safe combined Impressum for a site targeting all three:

```
Anbieter / Verantwortlich

[Vor- und Nachname / Firmenname mit Rechtsform]
[Straße Hausnummer]
[PLZ Ort]
[Land]

Kontakt
Telefon: +43 ...
E-Mail:  info@example.com
[Optional: Kontaktformular-Link]

Vertretungsberechtigte
[Bei juristischen Personen: Geschäftsführer / Vorstand mit Vor- und Nachname]

Handelsregister / Firmenbuch
[Registergericht / Firmenbuchgericht]
[Registernummer / Firmenbuchnummer]

Umsatzsteuer-Identifikationsnummer
[UID / USt-IdNr.]

Aufsichtsbehörde
[Sofern Gewerbe mit Behördenaufsicht]

Berufsbezeichnung und Kammer
[Bei reglementierten Berufen — Ärzte, Anwälte, Steuerberater etc.]

Online-Streitbeilegung (EU)
Die EU-Kommission stellt eine Plattform zur Online-Streitbeilegung bereit:
https://ec.europa.eu/consumers/odr/

Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV (DE) bzw. § 25 MedienG (AT)
[Vor- und Nachname, Anschrift]
```

Implementation rules:

- **Plaintext, not behind login.** Search engines and regulators must reach it.
- **No `noindex`**, no `robots.txt` block.
- **No "click here for Impressum" — name the link "Impressum"** literally.
- **Email address must be reachable**, not a contact form alone. Plaintext is fine — yes, scrapers will grab it, that's been the legal position for years.
- **Updated when responsibilities change.** Wrong Impressum is the same as no Impressum for liability purposes.

## Datenschutzerklärung — must match what the site actually does

A static template copied from a generator is a finding, not compliance. The privacy policy must reflect every processing operation actually happening on the site.

Per **processing activity**, document:

- **What data** is collected (form fields, automatic data, cookies, fingerprinting)
- **Why** (legal basis: consent / contract / legitimate interest / legal obligation)
- **Where** it's stored (own systems, processors, location)
- **Retention period** specifically
- **Recipients** (every third-party processor named with link to their privacy policy)
- **User rights** (access, rectification, deletion, portability, objection, supervisory authority complaint)

Common DACH-site processing to enumerate:

- Web server logs (IP, user-agent, referrer, path, status, timestamp)
- Contact form / inquiry handling
- Newsletter / mailing list subscription with double opt-in
- Cookies & local storage (essential + optional)
- Analytics (Matomo, GA4 — needs consent in DACH)
- Maps (Google Maps, OpenStreetMap, Mapbox)
- Embedded videos (YouTube/Vimeo — pre-consent variants exist: `youtube-nocookie.com`)
- Fonts (self-hosted vs Google Fonts — Google Fonts CDN was the subject of multiple AT/DE judgments; self-host is the safe path)
- Payment processors (Stripe, PayPal, Klarna)
- AI / LLM services that receive user content

Sync the privacy policy with the [data inventory from `gdpr-technical-controls`](../gdpr-technical-controls/SKILL.md) — they should never disagree.

## Cookie / consent banner — the requirement

Under **TTDSG §25 (DE)** / **§165 TKG 2021 (AT)** / **DSG (CH, more permissive)**, you may only store or read information on the user's device **with prior, informed, opt-in consent** — except for strictly necessary cookies.

The banner must:

- **Block non-essential cookies/scripts until consent.** A banner that just says "by using this site you agree" while Google Analytics already loaded is non-compliant.
- **Offer "Accept", "Reject all", and "Settings" with equal prominence.** "Reject" cannot be a tiny grey link under a large green "Accept".
- **Provide granular categories** — typically "Essential", "Analytics", "Marketing", "Functional" — that users can toggle individually.
- **Be revocable.** A persistent re-open link (small "Cookie-Einstellungen" in the footer) is the standard pattern.
- **Log consent** with timestamp and what was consented to — you may need to prove it later.

Acceptable banner stacks:

- **Self-hosted**: Klaro!, Cookiebot (paid), Iubenda (paid)
- **WordPress-hosted**: Real Cookie Banner, Borlabs Cookie, Complianz
- **DIY**: a small implementation is fine if you cover the requirements above

Wire it to actual script-loading: scripts that depend on a category only run after the user opts in. A consent record without enforced gating is theater.

## AGB — Terms of Service

Required for B2C e-commerce; strongly recommended for B2B and for SaaS. AGB must:

- **Be accepted before purchase** — typically a checkbox on the order page with a clear link to the AGB text
- **Be persistently available** at a stable URL (`/agb`)
- **Match the actual fulfillment process** — delivery timelines, return windows (14-day right-of-withdrawal for B2C distance contracts under DE/AT law), warranty
- **Not include surprise clauses** — DE has aggressive jurisprudence against unfair contract terms (AGB-Kontrolle)
- **Include a Widerrufsbelehrung (withdrawal notice)** for B2C — there are statutory templates; deviating is risky

Templates are a starting point, not the finished product. Have a DACH e-commerce lawyer review the AGB before launch if you sell B2C.

## AVV / DPA — for every processor

Every third party that processes personal data on your behalf needs an **Auftragsverarbeitungsvertrag (AVV)** under Art. 28 GDPR (in EN: Data Processing Agreement / DPA).

Engineering side:

- **Sign before integration**, not after launch. Most providers offer a standard AVV in their privacy/legal portal.
- **Track which AVV covers which processor** — when you onboard a new tool, the AVV is part of the onboarding checklist
- **Some major providers' standard AVVs are good enough** (AWS, Stripe, Cloudflare, Mailgun, HubSpot). Smaller vendors sometimes need an actual draft.
- **Inform users in the Datenschutzerklärung** that data goes to this processor and link their privacy policy

## TOMs — Technical and Organizational Measures

Art. 32 GDPR requires you to implement appropriate TOMs. For an audit, you need a written document. For your security posture, you need the underlying controls to actually exist. The two should match.

Typical TOMs sections (with the skills in this repo that implement them):

| TOM area | Implementation |
|---|---|
| **Zutrittskontrolle** (physical access) | Office locks, server location (cloud DC ISO 27001 etc.) |
| **Zugangskontrolle** (system access) | Strong auth, MFA — see [`auth-hardening`](../auth-hardening/SKILL.md) |
| **Zugriffskontrolle** (data access) | Role separation, RLS — see [`postgres-hardening`](../postgres-hardening/SKILL.md) |
| **Weitergabekontrolle** (transit) | TLS, encrypted backups — see [`site-server-audit`](../site-server-audit/SKILL.md), [`postgres-hardening`](../postgres-hardening/SKILL.md) |
| **Eingabekontrolle** (audit) | Audit logging — see [`log-strategy`](../log-strategy/SKILL.md) |
| **Auftragskontrolle** (processor) | DPAs/AVVs, processor vetting |
| **Verfügbarkeitskontrolle** (availability) | Backups, restore tests, monitoring |
| **Trennungsgebot** (purpose separation) | Tenant isolation, separate environments |

Write this document early — once your stack is set, generate the TOMs from what you've actually built.

## CH-specific notes (FADP / DSG)

Switzerland's revised FADP (2023) is close to GDPR but not identical:

- **Notification deadline differs** — without undue delay rather than 72h
- **Record of processing activities** required for entities ≥250 staff or for high-risk processing
- **Cross-border transfers** to non-adequate countries need additional safeguards (similar to SCCs)
- **Data Protection Impact Assessment (DPIA)** required for high-risk processing
- **Privacy Icon** convention is recommended but not mandatory

For sites targeting EU + CH together, GDPR-compliant is generally CH-compliant; document the small deltas if you operate from Switzerland.

## Common findings

When auditing a DACH site:

- Impressum missing the Vertretungsberechtigte (juristic person) or Handelsregister number
- Datenschutzerklärung references services that aren't actually integrated, or omits services that are
- Google Fonts loaded from `fonts.googleapis.com` (instead of self-hosted) — Munich and Vienna courts have ruled against this
- YouTube embeds load before consent (use `youtube-nocookie.com` and gate behind consent)
- "Accept" cookie button is large+colored; "Reject" is hidden in settings — non-compliant under TTDSG/TKG
- Newsletter signup without double opt-in
- Contact form transmits over HTTP, or stores submissions plaintext in a CMS that allows wide access
- Site has no `/agb` despite selling to consumers
- The Datenschutz page links to outdated processor privacy policies

## Quick checklist

Before launching or relaunching a DACH-facing site:

- [ ] `/impressum` exists, complete, reachable from every page
- [ ] `/datenschutz` matches actual processing, lists every processor
- [ ] `/agb` exists for any B2C selling; Widerrufsbelehrung included
- [ ] Cookie banner blocks non-essential scripts until consent; categories are granular
- [ ] "Reject" is as prominent as "Accept"; settings revocable from footer
- [ ] Consent decisions logged with timestamp + categories
- [ ] AVVs signed with every processor; tracked in a central list
- [ ] Google Fonts self-hosted (or use a privacy-respecting alternative)
- [ ] YouTube/Vimeo embeds gated behind consent (or use nocookie variant)
- [ ] Newsletter uses double opt-in
- [ ] TOMs document written and reflects actual security controls
- [ ] No analytics fires before consent
- [ ] Footer links named exactly "Impressum" and "Datenschutz"

## What this skill will not do

- Provide legal advice — talk to a DACH-qualified lawyer for borderline cases
- Generate Impressum / AGB content as a substitute for review
- Endorse dark-pattern cookie banners that bury the reject option
