---
name: site-phase-5
description: >-
  Phase 5 — Create base components derived from blueprint, i18n setup
  (PT-BR + EN), SEO schema markup. No template copying.
allowed-tools: Read, Write, Edit, Bash
model: sonnet
effort: medium
context: fork
user-invocable: false
---

# Phase 5 — Base Components + i18n + SEO

## Objective

Create animation components derived from the blueprint, set up bilingual i18n, and add SEO schema markup. Every component must be unique to THIS site.

## Step 1 — Read references

```
Read: sites/_templates/i18n-setup.js
Read: sites/_templates/seo-templates.jsx
Read: sites/$LEAD_ID/mapa-encantamento.md
```

## Step 2 — Create blueprint-derived components

For EACH animation specified in the blueprint, create the corresponding component.

**Before building from scratch, check MCPs:**
- `magic-ui` — blur-fade, aurora-text, number-ticker, shimmer-button
- `aceternity-ui` — parallax-scroll, text-generate-effect, hero-highlight, 3D-card
- If the MCP has the component, USE IT. Customize colors/timings for this site.

**MANDATORY components (only 2):**
- `LanguageToggle.jsx` — functional (react-i18next changeLanguage). Visual can be unique.
- `Button.jsx` — with variants based on THIS site's color tokens.

**BANNED parameters (from old template):**
- ScrollReveal: y:60, duration:0.8, ease:'power3.out'
- AnimatedText: duration:0.5, delay:i*0.08, ease:[0.25, 0.46, 0.45, 0.94]
- ParallaxImage: speed:0.2, h-[120%]
- CountUp: duration:2, ease:'power2.out'

If you need similar functionality, use DIFFERENT parameters derived from the blueprint.

**Cleanup patterns (reference, don't copy):**
- GSAP: always `gsap.context()` with `ctx.revert()` in useEffect cleanup
- Motion: `viewport={{ once: true }}` for entry animations
- ScrollTrigger: kill on cleanup
- Lenis: destroy on cleanup
- prefers-reduced-motion: respect via CSS @media or JS matchMedia

Reference patterns (do NOT copy components, only patterns):
```
Read: sites/_templates/component-templates.jsx
```

## Step 3 — Layout base

Create `src/components/layout/Section.jsx` based on the template.

## Step 4 — i18n config

Create `src/i18n/index.js` exactly as in i18n-setup.js template.
Import BEFORE App in main.jsx.

## Step 5 — i18n PT-BR

Create `src/i18n/pt-BR.json` with ALL site strings, correct accents (a, e, c, o, i, u).
Structure: nav, hero, each section from Phase 3, contact, footer, lang.
Fill with REAL briefing data — ZERO placeholders.

## Step 6 — i18n EN

Create `src/i18n/en.json` with SAME structure as pt-BR.json. Naturally translated (not robotic).
Proper nouns stay in Portuguese.

## Step 7 — Structured data

Create `src/data/content.js` with all briefing data organized for components.

## Step 8 — SEO

Based on seo-templates.jsx:
- `src/components/seo/JsonLd.jsx` — schema.org with MOST SPECIFIC type. ALL data: address, coordinates, hours, reviews, social (sameAs), services, professional registry, knowsAbout, alumniOf, award, memberOf.
- `src/components/seo/FaqSchema.jsx` — SPECIFIC questions about this client (not generic).

## Exit Gate (blocking)

```bash
.claude/scripts/gate-i18n-keys.sh $LEAD_ID
```

## Constraints

| Rule | Enforced by |
|------|-------------|
| Same keys in pt-BR.json and en.json | gate-i18n-keys.sh |
| No banned animation parameters | Visual review in Phase 7 |
| Components derived from blueprint, not template | gate-anti-similarity.sh in Phase 6 |
| Correct PT-BR accents | playwright-validate.py (pt_br_accents) |

## Exit Criteria

- [ ] Animation components created per blueprint (NOT generic template)
- [ ] NO component with parameters identical to old template
- [ ] LanguageToggle and Button created
- [ ] pt-BR.json and en.json with same keys and correct accents
- [ ] JsonLd.jsx and FaqSchema.jsx with real data
- [ ] content.js with structured data
