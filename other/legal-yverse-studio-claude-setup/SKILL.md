---
name: legal
description: "Use when planning, before launch, or adding tracking, embeds, AI, logins or uploads. German law for any app: Impressum, Datenschutz, cookies, accessibility, accounts, licences, naming, checking tools."
---

# Legal

Not legal advice. This team says what must exist, writes the texts and checks them. Claude
writes Impressum and Datenschutz in-house from the plan's data and processor list, and uses
official model texts word for word where they exist (Widerrufsbelehrung, Muster-
Widerrufsformular), as in yverse-studio/duo-test. A paid legal-text service (eRecht24, IT-Recht Kanzlei)
that keeps texts current and helps with warning letters (Abmahnungen) comes in once sales do.
Markers: **[S]** search
results and legal publishers agree, **[K]** known but not re-read. Checked 2026-10-05.

Selling anything: the `sell` skill's `legal-de.md` adds the shop law. Ads, social posts,
newsletters: the `market` skill's section 4.

## 1. In the plan (legal research subagent)

Answer each line for this project in `PLAN.md`, and turn every "yes" into an acceptance
criterion in `features.json`:

| Topic | Rule | What the app needs |
|---|---|---|
| Impressum | § 5 DDG for any site that is business-like, which includes ads or a price [K] | Name, postal address, email, a second fast channel; reachable from every page within two clicks |
| Datenschutz | Art. 13 DSGVO | Names every processor (Cloudflare, Stripe, Resend, PostHog, Sentry, the AI provider...) and an AVV/DPA with each, taken in their settings [K] |
| Cookies and storage | § 25 TDDDG: consent before anything not strictly necessary, localStorage included [K] | Prefer no banner: session cookie only, cookieless analytics, self-hosted fonts, two-click embeds |
| Google Fonts and embeds | Loading them from Google sends the IP: LG München I, 3 O 17493/20 [S] | Self-host fonts; YouTube, Maps, social embeds load only after a click |
| Accessibility | BFSG since 2025-06-28 for consumer e-commerce; micro-enterprises are exempt for services [S] | Build to WCAG 2.2 AA anyway (`a11y-architect`) |
| Accounts | DSGVO Art. 15-17, 20 | Delete account and export data in the app; for subscriptions the Kündigungsbutton (§ 312k BGB) |
| Children | Art. 8 DSGVO: consent-based processing needs a parent below 16 in Germany [K] | Ask for age or don't target under-16s |
| AI features | EU AI Act Art. 50 transparency duties from 2026-08-02 [S] | Say it is AI where users talk to it; label AI-generated images, audio, video; name the AI provider in Datenschutz |
| User content | Digital Services Act for hosting services: contact point, notice-and-action, reasons for removals [K] | A report button, a contact address, terms that say what gets removed |
| Licenses | Dependencies, fonts, images, music, AI output | License check below; no copyrighted music or images without a license; TikTok sounds stay inside TikTok |
| The name | Trademark and domain | Search below before the name goes on anything |

## 2. Tools

- **Privacy scan** of a running page (cookies, storage, third-party requests before consent,
  Impressum and Datenschutz links). `fail:` lines exit 1; `note:` lines (first-party cookies,
  storage) pass only when strictly necessary:
  ```
  node <legal skill folder>/scripts/privacy-scan.mjs <preview url> / /pricing /app
  ```
- **Dependency licenses:** `npx license-checker-rseidelsohn --production --summary` in the project.
  Copyleft (GPL, AGPL) in a closed app is a stop; ask before shipping.
- **Name / trademark:** search the name in [DPMAregister](https://register.dpma.de/DPMAregister/marke/einsteiger)
  (German marks) and [TMview](https://www.tmdn.org/tmview/) (EU and national marks), classes 9, 35,
  41, 42 for apps. A conflict means a new name, not a lawyer.
- **Anthropic's legal plugins** (Anthropic Directory, `anthropics/claude-for-legal`; US/in-house
  flavoured, use them as checklists, German law wins): `privacy-legal` (PIA, DPA review, gap
  analysis), `ip-legal` (trademark clearance, open-source review), `ai-governance-legal`
  (AI use-case triage). Turn one on per project only when its topic is in the plan; in cloud
  threads find them with `SearchPlugins`.
- **Texts:** Claude writes them from `PLAN.md` (Impressum data from the brainstorm, every
  processor with what data goes there and why); official model texts word for word; nothing
  invented. Once the app sells, move to a paid service's generated texts.

## 3. Before launch

The `legal-reviewer` agent checks the preview against the plan's legal lines and the privacy
scan; its result goes into brief (c) and check 5 of the 5/5 gate (`operator` skill).

yskills does, once per project, inside brief (c): read the legal texts, and accept the AVV/DPA
in each processor's settings (the agent lists the deep links).
