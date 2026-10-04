---
name: provider-access-expand
description: "Discovery batch that grows the Provider Access Launch queue. Use when asked to find more user-connected OAuth, API, API-key, remote MCP, marketplace, or partner-access campaigns for a capability, provider family, MCP/plugin catalog, or competitive gap. NOT for client Local Listings distribution."
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/provider-access-expand/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# Expand Provider Access

Add a researched, deduplicated batch to the normal AI Matrx `Provider Access Launch` Project. This
skill discovers work; it does not create a parallel spreadsheet, register external accounts, request
permissions, or claim that a provider is easy before scouting.

**Keep Local Listings separate.** This queue is for integrations a user connects to AI Matrx.
Listing claims, location publishers, and data aggregators belong to
`common-docs/systems/marketing/local-listings/PLAN.md` and its own project. Never add Data Axle, Localeze,
Foursquare listing distribution, Yelp Listing Management, Apple business listings, or Google
Business Profile here. If a listings-only seed already exists, mark it `superseded` and point to the
Local Listings work; preserve its history.

## Defaults

- Add 15–25 campaigns for a named vertical or capability class.
- Use the AI Matrx tenant organization `5dc930e9-bd65-44a1-8369-af773f6e1a5b`.
- One campaign is one independently approvable access boundary, not necessarily one provider.
- Stable key: lowercase `provider.capability`.
- Title: `P0 | Provider | Capability`.
- New tasks start canonical `inbox` with `Phase: discovered` and no due check until scouting starts.
  The Projects JSON importer may store legacy `incomplete`; the product normalizes it to `inbox`.

## Workflow

1. Read `common-docs/systems/integrations/provider-access/FEATURE.md` when the workspace contains it.
2. Open the live `Provider Access Launch` Project and inventory all existing campaign keys.
3. Search the platform inventory before the public web:
   - installed/recommended plugins;
   - live `tool.mcp_server` and related `tool.definition` rows;
   - `users.integration_connections` and `tool.mcp_user_conn`;
   - provider code and integration UI;
   - Unified Credential Vault definitions, never secret values;
   - CRM provider parties/interactions;
   - `common-docs/projects/*` and existing task evidence.
4. Use current official provider sources to confirm that each proposed capability or developer
   program exists. Do not turn search-result snippets, marketplace SEO pages, or memory into facts.
5. Split providers where scopes, reviewer stories, production activation, or owners differ. Merge
   aliases that lead to the same authorization and implemented outcome.
6. Assign priority:
   - `P0`: launch parity, existing MCP/plugin, social, enterprise, marketing/ads, core cloud,
     productivity, identity, or payments.
   - `P1`: major legal, medical, education, CRM, commerce, communications, or observability value.
   - `P2`: useful long-tail advantage.
7. Create each campaign through the normal Projects/Tasks product path. If an exact key exists,
   enrich the existing task; never create a duplicate.
8. End with counts by priority/category, the campaigns added, aliases collapsed, and any candidate
   rejected because no official/current route could be established.

## Minimum new-task card

```text
Campaign: provider.capability
Phase: discovered
Category: <category>
Access path: <oauth_review|oauth_self_service|api_key|remote_mcp|partner|marketplace|research>
Easy candidate: <yes|no|research> (unverified until scouting)
Existing asset: <link/identity or none found>
Source seed: <official URL or official sources required during scouting>
Next action: Run $provider-access-scout for this campaign.
Next check: none until scouting completes
```

Do not put secrets, copied access tokens, guessed requirements, or a submission recommendation in a
new discovery task. “Easy candidate” is a scouting hypothesis only.

## Deduplication decisions

- Same provider + same authorization + same implemented outcome: one campaign.
- Same provider + unrelated scope family or materially different review: separate campaigns.
- Official remote MCP and a distinct first-party OAuth/API product: separate if they produce
  independently useful connections.
- Developer sandbox and production activation: one campaign with separate gates unless either can
  be useful and verified independently; then split them.
- Existing detailed plan: link it. Do not re-copy its history into the task.
- Existing connected integration: create or update the task only if verification/follow-through is
  incomplete; otherwise mark it verified with evidence.

## Example requests

- “Use `$provider-access-expand` to add legal-practice and e-discovery providers.”
- “Use `$provider-access-expand` to reconcile every recommended plugin against the launch queue.”
- “Use `$provider-access-expand` to find another 20 education access campaigns.”
