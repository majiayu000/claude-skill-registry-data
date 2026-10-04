---
name: scbe-github-pages-funnel-builder
description: Build or update SCBE GitHub Pages marketing surfaces under docs/ so they are discoverable, SEO-aware, and wired into the right funnel. Use when adding a new demo, free tool, product page, research surface, or support/manual page that must be linked from the homepage, demo hub, Polly sidebar, and sitemap without overstating claims.
---

# SCBE GitHub Pages Funnel Builder

## Workflow

1. Classify the page before editing.
- `launch-surface`: homepage, product page, pricing page, lead capture page
- `demo-surface`: interactive demo or free tool under `docs/demos/`
- `research-surface`: evidence, math explainer, benchmark, or theory page under `docs/research/`
- `support-surface`: manual, delivery, support, or recovery page

2. Edit the smallest coherent packet.
- Read the target page.
- Read the parent discovery page that should send traffic to it.
- Read shared discovery surfaces only if the page should appear there.
- Default mutable set:
  - `docs/index.html`
  - `docs/demos/index.html`
  - `docs/research/index.html`
  - `docs/static/polly-sidebar.js`
  - `docs/sitemap.xml`
  - the target page itself

3. Build the page as one funnel packet.
- Audience: who this page is for
- Pain: what problem they are trying to solve
- Proof: what concrete evidence or utility the page gives them
- CTA: what exact next action they should take
- Use one primary CTA and at most one secondary CTA.
- Do not leave pages as orphan destinations with no inbound links.

4. Fix metadata every time.
- Add or update `title`.
- Add a direct `meta description`.
- Add canonical URL.
- Add Open Graph and Twitter tags when the page is public-facing.
- Add structured data only when it clarifies the page type.
- Keep metadata matched to the actual page claims.

5. Wire discovery surfaces deliberately.
- New public pages should usually appear in `docs/sitemap.xml`.
- Demo/free-tool pages should usually appear in `docs/demos/index.html`.
- Homepage links belong only when the page is a true entry point, offer, or flagship proof surface.
- Update `docs/static/polly-sidebar.js` when Polly should route users toward the new page.

## SCBE-specific route rules

- GitHub Pages in this repo lives under `docs/`.
- Pages inside `docs/demos/` should usually link back to `../index.html` for home and `index.html` for the demo hub.
- If a page in `docs/demos/` uses the Polly sidebar, set `data-polly-root=".."`.
- Homepage-level pages usually use `data-polly-root="."`.
- Keep free tools, paid products, research evidence, and buyer support separated so the site does not collapse into one undifferentiated wall of claims.

## Claim discipline

- Separate `implemented`, `documented`, and `research` claims.
- Do not present discontinued services as active competitors.
- Do not imply legal guarantees you do not actually provide.
- For notarization/proof pages, prefer:
  - `proof of existence`
  - `integrity`
  - `claimed timestamp`
- Do not claim:
  - inventorship
  - novelty
  - patent priority
  - legal outcome guarantees
- Sacred Tongue is a signature/brand layer, not the evidentiary core.

## Page patterns

### Free tool / demo page
- State the problem in one sentence.
- Show the tool immediately.
- Add a short trust-model explanation.
- Add one monetization or contact path, not five.
- Link back to the parent hub.

### Product / launch page
- Put the offer, price, proof, and CTA above the fold.
- Keep lore and research links secondary.
- Make delivery/support paths explicit.

### Research / evidence page
- Keep the strongest confirmed result first.
- Distinguish live code from theory language.
- Link back to the relevant product or demo only if it helps the reader act.

## Output contract

Return:
- the files changed
- the page type chosen
- the primary CTA path
- the discovery surfaces updated
- any claim-boundary notes the user should know about

## GitLab cross-pond hook (evidence + lore)

If a page needs long-form evidence/lore that shouldn't live in GitHub Pages:
- keep canonical research in GitLab
- publish a stable excerpt + entrypoint page on GitHub Pages
- link explicitly and avoid implying GitLab content is "part of" the deployed site
