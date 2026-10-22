---
name: seo
description: Optimize for search engine visibility and ranking. Use when asked to "improve SEO", "optimize for search", "fix meta tags", "add structured data", "sitemap optimization", or "search engine optimization". Do NOT use for accessibility (use web-accessibility), performance (use core-web-vitals), or comprehensive site audits covering multiple areas (use web-quality-audit).
license: MIT
metadata:
  author: web-quality-skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# SEO optimization

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Optimize for search engine visibility and ranking.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [SEO fundamentals](references/instructions/02-seo-fundamentals.md) — when this domain or mode is in scope.
- 3. [Technical SEO](references/instructions/03-technical-seo.md) — when this domain or mode is in scope.
- 4. [On-page SEO](references/instructions/04-on-page-seo.md) — when this domain or mode is in scope.
- 5. [Structured data (JSON-LD)](references/instructions/05-structured-data-json-ld.md) — when this domain or mode is in scope.
- 6. [Mobile SEO](references/instructions/06-mobile-seo.md) — when this domain or mode is in scope.
- 7. [International SEO](references/instructions/07-international-seo.md) — when this domain or mode is in scope.
- 8. [SEO audit checklist](references/instructions/08-seo-audit-checklist.md) — when this domain or mode is in scope.
- 9. [Tools](references/instructions/09-tools.md) — when this domain or mode is in scope.
- 10. [References](references/instructions/10-references.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
