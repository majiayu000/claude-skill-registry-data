---
name: google-ads
description: >-
  Use when pulling Google Ads campaign, ad group, or keyword performance for paid media or Phase 18–19 work.
---

# Google Ads

Thin adapter for digital workers. See `skills/org/TOOL-REGISTRY.md`.

## Preferred access
Google Ads API or Ads MCP if connected; else UI exports

## Env / secrets
`GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CUSTOMER_ID`, `GOOGLE_ADS_LOGIN_CUSTOMER_ID` + google-auth OAuth/SA as configured

Resolve via `skills/integrations/obsidian-secrets/` then `.env.local`.

## MCP
Google Ads MCP if present — discover via GetMcpTools

## Primary ops
1. Pull spend, clicks, conversions, CPA/ROAS by campaign
2. Map UTM/campaign names to GA4 for reconciliation
3. Never invent ROAS — degrade to export stubs if API missing

## Fallback
CSV export from Ads UI into the phase artifact

## Common failures
Developer token / MCC access errors → ask human for Ads API enablement
