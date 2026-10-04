---
name: site-phase-2
description: >-
  Phase 2 — Deep client immersion. Analyzes briefing data_points to extract
  identity, narrative, content inventory, gaps, audience, and site scope.
allowed-tools: Read, Bash, WebSearch
model: sonnet
effort: medium
context: fork
user-invocable: false
---

# Phase 2 — Client Immersion

## Objective

Deeply understand the client beyond their niche. Extract what makes THIS client unique, inventory all available content, identify gaps, define target audience, and decide site scope (SPA vs multi-page).

## Step 1 — Who is this client really?

Not "a dentist." What makes THIS client unique — story, differentiator, trajectory. Use: identity, history, professional_registry, brand data_points.

## Step 2 — What narrative can ONLY this client tell?

The site's guiding thread in 1 sentence.

## Step 3 — Content inventory

Catalog everything available from data_points:
- **Text:** name, story, services/specialties, slogan, differentiator
- **Images:** ALL URLs (classify: portrait/logo/banner/product/venue)
- **Contact:** phones, email, address, hours, WhatsApp, coordinates
- **Numbers:** followers, ratings, years, awards, certifications
- **Social:** Instagram, Facebook, LinkedIn, TikTok (URLs + metrics)
- **Menu/Services:** items with name, description, price
- **Reviews:** aggregate rating, total reviews, testimonials by platform
- **Competitors:** ONLY their colors (to avoid repetition). Benchmark = curated catalog (`sites/_templates/design-references.md`), NOT competitors

## Step 4 — Gaps and fallbacks

- No colors → derive from real images + avoid competitor colors
- No images → bold typographic design (gradients, shapes, CSS textures)
- No story → synthesize from CNPJ, education, awards
- No testimonials → visual badges from platform ratings
- No slogan → create from differentiator
- 40+ items → dedicated page with filters

## Step 5 — Target audience

Who visits? Emotional journey? What are they looking for? What action do we want?

## Step 6 — Scope decision

- Distinct services deserving their own pages?
- Multiple locations?
- Blog/articles?
- Extensive menu (40+)?
- Portfolio/gallery?

If YES to any: React Router with dedicated routes.
If simple: robust SPA with depth in each section.

Show decided structure to user.

## Exit Criteria

- [ ] 6 items written and shown to user
- [ ] Site structure defined (SPA or multi-page)
- [ ] Complete inventory of available content
