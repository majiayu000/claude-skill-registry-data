---
name: copy-frameworks
description: Persuasive copywriting generator using AIDA, PAS, BAB, 4Ps, and StoryBrand frameworks. For ads, emails, landing pages, and proposals. Arabic-aware (RTL) output. Reusable inside proposal-writer and marketing-strategy.
personas:
  - MARKETING
  - SALES
  - BRAND
triggers:
  - copy frameworks
  - copywriting
  - AIDA
  - صياغة إعلان
  - نص اقناعي
  - copy
  - storybrand
tech_stack:
  - brevo
  - ga4

---
[SKILL] copy-frameworks
[OBJ] Generate persuasive marketing and sales copy on demand using proven frameworks (AIDA, PAS, BAB, 4Ps, StoryBrand), with Arabic RTL parity. Produce ready-to-use drafts for emails, ads, landing pages, and proposals.

[DOMAINS]
- Frameworks: AIDA (Attention-Interest-Desire-Action), PAS (Problem-Agitate-Solution), BAB (Before-After-Bridge), 4Ps (Picture-Promise-Prove-Push), StoryBrand (SB7).
- Surfaces: subject lines, ad copy, landing H1/body/CTA, email sequences, proposal hooks.
- Languages: English + Arabic (RTL layout, Arabic copy tone).

[CMD] Context7 IDs:
- knadh/listmonk (email template patterns): `knadh/listmonk`
- Brevo templating: `brevo/python-sdk` (fallback `sendinblue/bravo`)

[RULES]
1. [REQ] Pick the framework by intent:
   - AIDA → general ads/landing/email flow.
   - PAS → problem-led pitches, cold/outbound, pain offers.
   - BAB → transformation stories, case-study style.
   - 4Ps → product/feature launch.
   - StoryBrand → brand narrative, long-form, positioning.
2. [REQ] Output structure: state the chosen framework, then a filled template with each section labeled, then 2-3 variants. Keep each variant tight (subject ≤40 chars, ad ≤90 chars primary text hook).
3. [REQ] Arabic/RTL: when target is Arabic, set `dir="rtl" lang="ar"`, mirror CTA alignment, use natural Arabic persuasive tone (لا تترجم حرفياً). Provide Arabic + English side-by-side when bilingual audience.
4. [REQ] Hooks first: lead with the customer's stated problem or desire; proof must be specific (number/result), not vague.
5. [REQ] CTA explicit: every piece ends with one clear next step (subscribe, book, buy, reply).
6. [REQ] Reuse: delegate channel placement to `email-marketing` (drip) and `social-media-marketing` (posts); feed strategy to `marketing-strategy`.
7. [REQ] Measurement tie-in: suggest the metric to watch (CTR, open, conversion) and feed to GA4 (ga4-1).
8. [REQ] Approval gate: no publishing copy to any channel without explicit user `yes`.
9. [REQ] Anti-generic: refuse fluff ("best-in-class", "synergy"); every claim tied to a benefit or proof.

[PROHIBIT]
1. No publishing copy to any channel without user approval.
2. No literal machine translation of Arabic copy — rewrite for native tone + RTL.
3. No vague claims without proof.
4. No storing credentials or PII in code, logs, prompts, or commits.
