---
name: ssot-dashboard
description: Designs and structures the Movemental living SSOT dashboard (HTML/CSS/JS). Use when creating or refining the single-source-of-truth dashboard, sidebar and content structure, or when aligning Movemental vision and docs into a docs-first, token-based, agent-friendly dashboard.
---

# Movemental SSOT Dashboard

## When to Use

- User asks to design or refine the "SSOT dashboard," "living source of truth," or "dashboard as first link in the chain."
- User works in `ssot-dashboard/` or asks about sidebar structure, content sections, or Movemental vision in dashboard form.
- User wants to align `_docs` content into one navigable, well-designed dashboard for humans and agents.

## Instructions

1. **Ground in Movemental docs**  
   Read or reference: `_docs/site-docs/01_site_purpose_and_order.md`, `10_complete_site_map.md`, `_docs/type/11_PLATFORM_ARCHITECTURE_AT_A_GLANCE.md`, `_docs/ai-vision/01_ai-vision-overview.md`, `_docs/ai-vision/04_ui-ux-proposal.md`, `_docs/_guides/typography-2026.md`, `_docs/business-docs/00_foundation/README.md`.

2. **Propose or refine dashboard structure**  
   Sidebar sections should map to: Foundation (purpose, order), Site order & sitemap, Platform & type safety, AI vision, Design system & tokens. Main area shows one section at a time as the living doc.

3. **Apply docs-first design**  
   Use typography and spacing for hierarchy; token-based components (cards, sections); layout that is scannable and reading-optimized. Keep semantic HTML and clear headings/IDs for agents.

4. **Ensure dual audience**  
   Output must be usable by both humans (readable, clear nav) and agents (semantic structure, stable landmarks, optional meta like "Last updated").

## Sidebar Taxonomy (Canonical)

- **Foundation** — Why Movemental exists, scope, governance.
- **Core Story / VIM** — 500-word anchor story; Vision (what will change), Intention (what it will take), Means (how we'll do it); Dallas Willard VIM.
- **Site order & sitemap** — Fit → Why → Path → Credibility → Knowledge → Learning → Access → Homepage.
- **Platform & type safety** — Stack, six-layer chain, multi-tenant.
- **AI vision** — Movemental Intelligence, amplification not replacement, network-aware.
- **Design system & tokens** — Typography, color, component tokens.
- **Value proposition** — Primary/segment value props, one-liner, Start with Why.
- **Audience** — Who we serve, naming, demographics, psychographic, six archetypes.
- **Principles** — Four non-negotiables, ranked values (content guardrails).
- **Narrative & story** — Story we tell, pricing language, invitation.
- **Canonical copy** — Hero, Sound familiar, key page prose (master for React).
- **Voice & tone** — Platform voice; what we avoid; leader-specific refs.
- **Content types** — Article, course, book, video, podcast; creation rules.

## Output Conventions

- Edit or add files under `ssot-dashboard/`: `index.html`, `css/*.css`, `js/main.js`, `content/*.html`.
- Preserve token-based styling; do not hardcode colors or type sizes.
- For new content sections, add a corresponding sidebar entry and a `content/<section>.html` (or inlined section in `index.html`).

## Reference

- Full doc paths and persona: see project rule "SSOT dashboard co-creator" (globs: `**/ssot-dashboard/**`, `**/design-system/**`).
- For detailed Movemental pillars and governance: [reference.md](reference.md).
