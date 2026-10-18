---
name: forge-website
description: "Forge: websites, landing pages, and frontend UI: website, landing page, responsive, mobile layout, SEO, accessibility, Lighthouse, React, Vue, Tailwind."
---

# Forge playbook — Website / landing / frontend

**Do not duplicate ECC skills — defer to:** `design-is` (design audit), `browser` (screenshot loop). This file is orchestration only.

## Hard rules
- Mobile **and** desktop layout verified by screenshot before claiming done.
- No placeholder/Lorem/test/mock content in anything headed for prod.
- Forms validate input and hit a real endpoint; clear error + success states.
- Any analytics/form keys live in env, never in the committed bundle.
- Meta and sharing basics: every page has a unique title and meta description, a canonical URL, Open Graph title/description/image, and JSON-LD (Organization or WebSite) where it fits — checked in the built HTML.
- Performance proof: run Lighthouse or PageSpeed on the built site and report LCP, CLS and INP; numbers measured on localhost are labelled "local, indicative".

## Team (conditional by stack/level)
- Lead: `planner` / `architect`.
- Build review: `react-reviewer` **or** `vue-reviewer` (by stack).
- Audits (parallel): `a11y-architect`, `seo-specialist`, `performance-optimizer`.
- Copy/CTA: `marketing-agent`.

## Skills / commands / MCP
`design-is` (pick a real style direction first — see `~/.claude/rules/ecc/web/design-quality.md`), `browser` (mobile+desktop screenshots), `/react-build` + `/react-review` (or the Vue equivalents), `/test-coverage`. Canva MCP only if asset generation is explicitly requested. `humanizer` skill (`.claude/skills/humanizer/SKILL.md`) MAY run as an on-demand rewrite pass on client-facing marketing/landing copy — never on exact-command setup docs or forge-report output, and not always-on (34KB context cost).
When a build uses GSAP/ScrollTrigger for scroll-driven or compositor-friendly motion (per `~/.claude/rules/ecc/web/performance.md`), load the relevant `gsap` skill (`.claude/skills/gsap/<skill-name>/SKILL.md`) on demand for correct API usage — not always-on.

## Fan-out & flow
L2 for a single page, L3 for a multi-page site.
**Serial:** design direction (`design-is`) → build → audits → fixes → review gate.
**Parallel:** a11y ∥ seo ∥ performance ∥ copy audits on the built artifact (independent).

## Domain gates
Accessibility pass; SEO meta/OG + canonical; performance budget (see `~/.claude/rules/ecc/web/performance.md`); responsive at ~360/768/1280; CTA clarity; no broken links.

## Ship-readiness (unique)
Screenshots at mobile+desktop breakpoints; no test copy; all CTAs/links resolve; forms submit to a real endpoint with validation; favicon/meta/OG present; 404 route; secrets in env. The `ship-readiness` website checklist is advisory; optionally run `codex-reviewer` (Codex) on important code — not a blocker.
