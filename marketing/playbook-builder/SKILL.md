---
name: playbook-builder
description: "Generate comprehensive, interactive single-page HTML playbooks that establish domain authority for any industry. Spawns 3 parallel research agents (30+ min deep research), generates 13-section interactive content (maturity model, self-assessment, AI prompts, readiness checklist), deploys to Vercel, and tracks in a registry. Use when user says 'build a playbook', 'playbook for [industry]', 'authority playbook', 'industry playbook', 'create playbook for', or 'update playbook'. Supports JICATE Solutions branding (default) and white-label for paid clients. Do NOT use for blog posts or articles (use content-pipeline), single-page websites (use vibe-coder), or marketing campaigns (use creative-strategist)."
metadata:
  author: JICATE Solutions
  version: 1.0.0
  category: content-generation
  structure: skill-graph
---

# Playbook Builder

Generate authority-establishing, interactive single-page HTML playbooks for any industry. One command produces a fully deployed, lead-generating playbook with self-assessments, AI prompts, readiness checklists, and maturity models — backed by 30+ minutes of deep research.

## 5-Phase Workflow

1. **Research** — 3 parallel agents (Pain Hunter, Stat Collector, Trend Scanner) gather 30+ substantiated data points
2. **Content** — Generate 13-section playbook using research output (problem-first, no generic advice, real numbers only)
3. **HTML** — Build interactive single-page HTML matching the notebook/paper template design system
4. **Analytics** — Inject tracking script (or no-op stub if Supabase not configured)
5. **Deploy** — Human review gate, then Vercel deployment + registry update

## Quick Interview (Ask Before Building)

1. **Industry/domain:** "What industry is this playbook for?" (e.g., pharmacy chains, dental clinics)
2. **Target audience:** "Who reads this? What's their title?" (e.g., chain owners, clinic directors)
3. **Geography:** "India-focused, or global?" (affects stats, compliance, currency)
4. **Insider knowledge:** "Any specific pain points, stats, or insights from this industry?" (optional)
5. **Branding:** "JICATE Solutions branding, or white-label for a client?" — If white-label: client name, primary color hex, CTA email/URL

## Pre-Flight Checks

1. **Concurrency guard:** Read `/Users/omm/PROJECTS/jicate-playbooks/registry.json` — abort if same industry slug has `"status": "in-progress"`
2. **Industry scoping:** If industry is a top-level category (healthcare, manufacturing, education, retail, agriculture, finance, logistics, construction, hospitality, media), ask user to narrow to a segment
3. **Firecrawl credits:** Run `firecrawl --status` to verify sufficient credits before committing to 30+ minutes of research
4. **Bootstrap:** If `/Users/omm/PROJECTS/jicate-playbooks/` does not exist, create it with empty `registry.json` and `registry-config.json`

## Knowledge Graph

Start with `references/phase-1-research.md` — it defines the 3 parallel research agents, fallback chains, and the research output schema that feeds all subsequent phases.

When generating section content, read `references/phase-2-content.md` for the 13-section structure, content quality rules, and how to reference JICATE OS capabilities and the case study.

When building the HTML file, read `references/phase-3-html.md` for the template structure, interactive element specs, and white-label sanitization rules. Also read `references/design-system.md` for exact colors, fonts, and component styles.

When injecting analytics, read `references/phase-4-analytics.md` for the tracking script, Supabase schema, Edge Function security, and privacy/consent requirements.

When deploying and packaging, read `references/phase-5-deploy.md` for the human review gate, Vercel deployment, registry management, and paid client deliverables.

Before marking any phase complete, read `references/quality-gates.md` for the 9 quality gates, banned phrases, retry limits, and failure handling.

For SEO metadata and social sharing tags, read `references/seo-metadata.md` before finalizing the HTML.

For `--update` invocations, read `references/phase-5-deploy.md` for version management — old version archived, new version deployed to same URL.
