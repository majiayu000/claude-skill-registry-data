---
name: technical-architecture-simplification
description: Choose and document the simplest reliable technical architecture for Exorex client work, AI automations, dashboards, apps, backend systems, and operational tools. Use when Codex needs to avoid overengineering, compare Google Sheets vs database, no-code vs custom app, Firebase vs PostgreSQL, manual approval vs full automation, simple dashboard vs full admin portal, monolith vs microservices, or write an architecture decision record with trade-offs and upgrade path.
---

# Technical Architecture Simplification

Use this skill to solve the business problem with the simplest system that works reliably.

## Core Principle

Start simple, but do not build something careless.

Simple means appropriate: reliable enough, secure enough, maintainable, explainable, affordable, upgradeable, and aligned with the client's current stage.

## Workflow

1. Define the real business problem.
2. Identify the business stage:
   - early stage
   - growing
   - scaling
   - high-scale or enterprise
3. Choose the lowest architecture level that can solve the current problem reliably.
4. Compare at least one simpler and one more advanced alternative.
5. Explain trade-offs in business language.
6. Define what should remain manual for safety.
7. Define an upgrade path so the system can grow later.
8. Document the decision using an architecture decision record.

Read `references/architecture-decision-guide.md` for architecture levels, decision guides, checklist, and ADR template.

## Architecture Levels

Use the simplest viable level:

1. Manual or spreadsheet-based system.
2. No-code or low-code automation.
3. Simple web dashboard.
4. Custom app or full system.
5. Scalable cloud architecture.

Do not jump to a higher level unless the current business need, risk, users, data volume, security, or reliability requirement justifies it.

## Overengineering Warnings

Challenge the design if it includes:

- mobile app before workflow validation
- microservices for a small internal tool
- complex AI where simple rules are enough
- full CRM when lead tracking is enough
- advanced analytics before reliable data collection
- full automation where manual approval is safer
- custom backend before a form, sheet, Airtable, or n8n flow is tested

## Output Contract

When using this skill, provide:

1. Recommended architecture level.
2. Why it fits the client's current stage.
3. Alternatives considered.
4. Trade-offs and accepted risks.
5. What to build now and what not to build yet.
6. Upgrade path.
7. Architecture decision record draft when the decision is significant.
