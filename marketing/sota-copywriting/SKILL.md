---
name: sota-copywriting
description: >-
  State-of-the-art marketing copywriting and content guidance (2026) covering
  positioning and value propositions, headlines and landing-page copy, CTAs
  and social proof, SEO content (search intent, E-E-A-T, Google spam
  policies), and the accuracy/legal layer — claim substantiation, FTC
  Endorsement Guides (2023) and the Consumer Reviews Rule (2024), testimonial
  consent, dark-pattern avoidance, and email-marketing law (CAN-SPAM, GDPR
  consent). Use when writing or reviewing ANY outward-facing content —
  landing pages, marketing sites, product pages, launch announcements,
  app-store listings, newsletters, cold/lifecycle email — AND when auditing
  existing copy for conversion quality, honesty, and legal exposure. Trigger
  keywords: copywriting, marketing copy, landing page, headline, CTA, value
  proposition, positioning, tagline, SEO, meta description, E-E-A-T,
  testimonial, social proof, case study, newsletter, email marketing, app
  store listing, launch post, pricing page, brand voice.
---

# SOTA Copywriting & Marketing Content

## Purpose

Expert-level rules for the *words that face the market*: landing pages,
product marketing, SEO content, launch posts, and lifecycle email. The core
thesis: **conversion copy is a claim-making machine, and every claim is both a
persuasion asset and a legal/trust liability — the craft is being specific
enough to convince while staying provable.**

Boundaries: this skill owns outward-facing content. In-product interface text
is `sota-ux-writing`; technical documentation is `sota-docs-workflow`; the
visual/layout layer of marketing pages is `sota-frontend-design`; consent and
privacy-notice engineering is `sota-privacy-compliance`.

## BUILD mode

When writing marketing/content copy:

1. **Define audience, awareness stage, and the one action** before drafting —
   a page without a single primary conversion goal is a brochure (`rules/01`).
2. **Lead with the outcome the reader buys**, prove it with features and
   evidence — benefit → mechanism → proof, in that order (`rules/01` §3).
3. **Draft headlines last, pick from ≥5 variants**, test against the 4 U's
   heuristic, and keep the above-fold contract: what it is, who it's for,
   what to do next (`rules/02`).
4. **Run the accuracy gate before publishing** (`rules/04` §1): every
   objective claim substantiated, every superlative provable or cut, every
   testimonial consented and typical, every disclosure placed where it's
   seen.
5. For anything meant to rank: **match search intent and write people-first**
   — E-E-A-T signals on the page, no scaled low-value content (`rules/03`).
6. Before finishing, run each loaded rules file's **Audit checklist**
   against the draft.

## AUDIT mode

When reviewing existing marketing content:

1. Inventory the surface: landing pages, pricing page, comparison pages,
   blog/SEO content, email templates/sequences, app-store listings, social
   proof assets.
2. **Claims-first pass** (`rules/04`): list every objective claim, superlative,
   statistic, testimonial, and urgency device; demand the substantiation for
   each. Legal exposure outranks conversion polish.
3. **Conversion pass** (`rules/01`–`02`): above-fold contract, message
   hierarchy, CTA quality, proof placement, scannability.
4. **SEO pass** (`rules/03`) where organic traffic matters: intent match,
   E-E-A-T, spam-policy exposure, title/meta/heading hygiene.

### Severity conventions

- **Critical** — legal/deception exposure: unsubstantiated objective claims,
  fake or undisclosed-material-connection testimonials, fabricated reviews or
  social-proof counts, fake urgency (countdown timers that reset), missing
  unsubscribe/consent basis in email, dark patterns.
- **High** — trust or ranking damage: superlatives without proof, "results
  not typical" testimonials presented as typical, spam-policy-violating
  content (scaled/doorway), misleading comparison tables, meta/title bearing
  no relation to page content.
- **Medium** — conversion damage: no clear above-fold value proposition,
  feature-first copy with no benefit framing, generic CTAs ("Learn more"),
  proof present but unspecific, intent-mismatched SEO content.
- **Low** — polish: weak headline variants, wall-of-text sections, missing
  message match between ad and landing page, stale dates.

### Finding format

`file:line | rule violated | severity | effort | fix` — for claim findings,
state what substantiation would be sufficient; for copy findings, propose the
rewritten line.

## Rules index

| File | Read this when... |
|---|---|
| `rules/01-positioning-value-proposition.md` | Deciding what the copy argues: audience and awareness stages, value-proposition structure, benefit-vs-feature discipline, message hierarchy, differentiation claims, evidence types, we-vs-you framing. |
| `rules/02-headlines-landing-pages.md` | Writing the page: headline craft and variants, above-fold contract, section flow (attention→interest→desire→action as a heuristic), scannability, CTA wording and placement, social-proof presentation, pricing-page honesty (incl. EU prior-price rule). |
| `rules/03-seo-content.md` | Content meant to be found: search-intent matching, people-first content and E-E-A-T, Google spam policies (scaled content abuse, site reputation policy, doorway abuse), titles/meta as display heuristics, structured-data honesty, AI-assisted content discipline, generative-AI search surfaces (AI Overviews/AI Mode — still SEO, no GEO folklore), content maintenance. |
| `rules/04-claims-legal-trust.md` | The accuracy/legal gate: claim substantiation, puffery vs objective claims, FTC Endorsement Guides (16 CFR 255) and Consumer Reviews Rule (16 CFR 465), testimonial consent and typicality, EU review-verification and green-claims bans (UCPD Annex I), dark patterns and the EU withdrawal function, email law (CAN-SPAM, GDPR/ePrivacy), security/uptime claim hygiene, app-store metadata policies. |

## Top-10 non-negotiables

1. **Every objective claim is substantiated before it ships** — numbers have
   sources, "only/first/fastest" has evidence, or the claim is cut.
   (rules/04 §1)
2. **No fake anything**: reviews, testimonials, follower counts, urgency
   timers, "X people are viewing this". Fabricated social proof is a
   Critical finding and, for reviews, a civil-penalty violation (16 CFR 465).
   (rules/04 §3–4)
3. **Material connections are disclosed** clearly and proximately — paid,
   gifted, employee, or affiliate relationships behind any endorsement.
   (rules/04 §2)
4. **Benefit first, feature as proof** — every section passes the "so what?"
   test from the reader's chair. (rules/01 §3)
5. **One page, one primary action**; every CTA is verb + outcome
   ("Start free trial"), never "Submit" or a bare "Learn more". (rules/02 §4)
6. **The above-fold contract holds**: a first-time visitor can answer
   "what is it, who's it for, what do I do next" without scrolling.
   (rules/02 §2)
7. **Skim test passes**: reading only headings tells the page's whole
   argument. (rules/02 §3)
8. **Search content matches intent and adds first-hand value** — no scaled
   thin content, no doorway pages, no ranking-borrowed third-party content
   (Google spam policies). (rules/03 §1, §3)
9. **Email requires a basis and an exit**: consent (or a lawful basis) to
   send, accurate subject/sender, and a working unsubscribe honored promptly.
   (rules/04 §5)
10. **Friction reducers must be true**: "No credit card required",
    "Cancel anytime", "5-minute setup" are claims, not decorations — verify
    or delete. (rules/02 §4, rules/04 §1)
