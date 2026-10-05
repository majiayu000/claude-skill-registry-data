---
name: cross-crm-opportunity-sync
description: Coordinate opportunities and customer records across multiple CRMs while preserving attribution, visibility, commissions, and governance.
---

# Cross-CRM Opportunity Sync

Use this skill when a company runs multiple CRMs and needs one deal, account, or customer relationship to stay understandable across systems.

## Workflow

1. Detect a new opportunity or approved stage-change event in a connected CRM.
2. Match the account against a master customer record or matching rules.
3. Determine whether the deal touches another CRM, business unit, product line, or customer relationship.
4. Mirror or link the opportunity in the relevant CRM with approved fields only.
5. Surface cross-CRM context to the rep through an internal note, briefing, or team notification.
6. Write an audit trail for every cross-CRM write.
7. Route low-confidence matches, old conflicts, and revenue-sensitive updates for human review.

## Zapier MCP And SDK Role

- Use Zapier MCP to read and write approved CRM fields, call an LLM for matching and enrichment, look up a master customer record, and route rep notifications.
- Use Zapier SDK for developer-led implementations that need durable workflow execution, retries, logs, schedules, sandbox-to-production promotion, and audit trails.
- Keep production writes, fuzzy matches, revenue-touching workflows, and customer-data workflows approval-gated.

## Master Customer Record Patterns

- **Canonical CRM:** one CRM is the source of truth and other CRMs sync from it.
- **Warehouse-driven:** a warehouse creates a shared customer ID that all CRMs reference.
- **Match-on-the-fly:** the agent uses email domain and company-name matching with confidence scoring and human review.

## Known Gotchas

- Sync loops require a `synced_from` marker.
- Historic duplicates require a separate one-time cleanup pass before go-live.
- Bulk migration can hit CRM rate limits.
- Field types differ across CRMs and need translation maps.
- Stage names drift across CRMs and need a canonical taxonomy.
- Currency and FX rules must be explicit before syncing pipeline or revenue values.

## Guardrails

- Do not sync raw text notes between CRMs without explicit approval.
- Do not sync intermediate stage changes by default.
- Do not sync owner changes by default.
- Do not auto-promote low-confidence matches.
- Do not touch production without sandbox review and designated approval.
- Always write an audit row for cross-CRM writes.

## Inspired By

This skill is generalized from [When operators get the keys to the integration stack](https://zapier.com/blog/voltt-operators-integration), a customer story with Voltt founder William Ascough. The reference implementation runs across multiple CRMs at a global multi-product business with operator-built workflows governed through a sandbox-to-production model.
