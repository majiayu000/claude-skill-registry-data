---
name: ai-seo
description: 'Assimilated TLC AI SEO skill (1.0.0). Programmatic SEO, competitor-alternative pages, AI Overviews/GEO, keyword strategy and content ops. Triggers: SEO, programmatic SEO, AI Overviews, DataForSEO, keyword strategy, organic traffic. Do not use for application code review or software architecture.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# AI SEO

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Assimilated from installed `ai-seo` 1.0.0 (Chad Boyda / Felipe Rodrigues). Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity.

## Mission

Plan and produce AI-assisted SEO systems: BOFU alternative pages, programmatic templates, GEO/AI Overview optimization, and measurement. Strategy and content contracts, not app-code architecture.

## Activation

- User asks for SEO, programmatic pages, competitor alternatives, AI Overviews, or keyword strategy.

## Non-activation

- Technical implementation of the product (`spec-driven`, language experts).
- Web security/compatibility only (`best-practices`).

## Critical rules

1. Confirm stack, goal, domain authority, CMS, and competitor set before recommending spend or scale.
2. Never paste API keys, GSC tokens, or DataForSEO credentials into prompts, files, or notebook.
3. Verify current tool pricing and SERP behavior with dated search; do not treat the 2025 table as live truth.
4. Quality floor for programmatic pages: unique helpful content, not boilerplate swaps.
5. Follow playbooks in `references/ORIGINAL_SKILL.md`.

## Continuity

Do not store customer PII or SEO API secrets in `.notebook/` or `.specs/`.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
