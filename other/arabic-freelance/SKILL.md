---
name: arabic-freelance
description: Arabic freelance marketplaces specialist — Mostaql, Khamsat, Nabbesh, Bawaba, Bayt. RTL proposals, local pricing, feed analysis.
personas:
  - FREELANCE
triggers:
  - arabic freelance
  - mostaql
  - خمسات
  - nabbesh
  - bawaba
  - bayt
  - مستقل عربي
  - فري لانس عربي
tech_stack:
  - documenso/documenso
  - invoiceninja/invoiceninja
  - chatwoot/chatwoot

---
[SKILL] arabic-freelance
[OBJ] Master Arabic freelance platforms — Mostaql, Khamsat, Nabbesh, Bawaba, Bayt — with RTL-ready proposals, local-currency pricing (SAR/AED/EGP), and culturally fluent client communication.

[RULES]
1. [REQ] Platform map: Mostaql (escrow, per-project, KSA-led), Khamsat (micro-gigs $5-25, Egypt-led), Nabbesh (enterprise/corporate), Bawaba/Bayt (jobs/recruitment). Match tactic to platform.
2. [REQ] RTL proposal: full right-to-left typesetting, Arabic honorifics, clear scope, milestones. Reuse `freelance-platforms` structure but Arabic-first; mirror `proposal-writer` for copy.
3. [REQ] Local pricing: quote in SAR/AED/EGP with stated VAT (KSA 15%, UAE 5%) where applicable; show net after platform fees. Use `pricing-strategy` + `invoice-manager`.
4. [CMD] Context7 IDs: `documenso/documenso` (Arabic contract + sign), `invoiceninja/invoiceninja` (multi-currency invoice), `chatwoot/chatwoot` (Arabic inbox).
5. [REQ] ToS compliance: respect each platform's rules (no off-platform drainage on Mostaql/Khamsat — bans apply). Escrow protects both sides; never bypass.
6. [REQ] Feed analysis: scan Arabic feeds for keywords; score by budget realism + client verification + competition (mirror `freelance-platforms` scoring, Arabic labels).
7. [REQ] Cultural fluency: Friday/weekend awareness (Gulf Fri-Sat), Ramadan hours, formal vs casual per client; builds trust and `client-retention`.
8. [REQ] Contracts/invoicing: Arabic NDA/SOW via `contract-studio`; Arabic invoice via `invoice-manager`; VAT handled in `freelance-financials`.
9. [REQ] Payment: local rails (bank transfer, STC Pay, Fawry, UAE banks); track in `invoice-manager`; surface FX in `freelance-financials`.
10. [REQ] Cross-link: `freelance-platforms` (global), `dispute-resolution` (Arabic ToS), `local-seo` (Arabic GBP), `personal-branding` (Arabic stream).

[PROHIBIT]
1. No off-platform payment requests on Arabic marketplaces.
2. No LTR/broken-RTL deliverables for Arabic clients.
3. No omission of applicable VAT in quotes.
4. No contract/invoice without Arabic version available.
