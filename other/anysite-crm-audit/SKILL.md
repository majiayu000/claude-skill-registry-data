---
name: anysite-crm-audit
description: Read-only data quality audit of the connected CRM - field completeness per mapped property, duplicate candidates, stale records, enrichability estimate. Produces a report and a concrete fix plan, never writes anything - run it first when you don't yet know what's broken; the actual fixing happens in anysite-crm-enrich. Use when the user asks "what's the state of my CRM", wants a data quality report, duplicate check, or a safe first run after connecting a CRM. Requires an active CRM connection.
---

# CRM Audit

The safe first date with a user's CRM: read everything, write nothing, show what's broken
and what enrichment would fix. Also the natural funnel into `anysite-crm-enrich`.

## Prerequisites

Active CRM connection. No profile needed (works better with one — gap analysis follows the
mapped fields).

## Flow

### 1. Inventory

```
crm_get_schema(object_type="contacts") / (object_type="companies")
```
Use `properties` filtering when you only need specific fields — the full schema is large.
Then page through records:
```
crm_query_records(object_type=..., properties=[key fields], after=<cursor>)
```
Audit scope: whole portal if small; else the working list + a stated sample. Say which.

### 2. Analyze (all local — no further API calls)

- **Completeness:** % filled per mapped/target field (email, title, company, domain,
  industry, size, linkedin_url). Rank by gap size.
- **Match-key coverage:** how many contacts have email / linkedin_url / neither (the
  "neither" group is unenrichable and un-dedupable — flag it).
- **Duplicate candidates:** same normalized email; same domain with several company records;
  same person name + company. Candidates only — never auto-merge.
- **Email ↔ employer mismatch:** contact's email domain vs their linked company's domain.
  A mismatch has THREE causes needing different handling (all seen live): the person changed
  jobs; the COMPANY rebranded/changed domain (old domain usually still receives mail — the
  contact is fine); or the email is genuinely stale. Free discriminator already in the data:
  if crunchbase under the domain-derived alias returns a different company NAME than the
  LinkedIn page of that same domain — that's a rebrand, not a departure. FLAG ONLY, never
  auto-fix in either direction — in two causes out of three there is nothing to "fix", and
  "correcting" the company from the email domain overwrites good data with stale. Job-change
  suspects go to anysite-crm-champions.
- **Staleness:** if `anysite_last_enriched_at` (or similar) is mapped — age distribution;
  contacts with no activity fields; companies with dead domains (spot-check a few via
  `webparser/parse` only if the user asks).
- **Association health:** contacts without a company link (visible as missing company
  fields when queried).

### 3. Report

Lead with the 3 numbers that matter: enrichable-now count, duplicate-candidate count,
unenrichable count. Then per-field completeness table, then the fix plan:

- "N contacts have linkedin_url but no title → `anysite-crm-enrich` fills them (~cost)"
- "N companies missing industry/size → enrich via company lookup (~cost)"
- "N duplicate candidates → list for manual review (merging is a CRM-side operation)"

Cost estimates come from the anysite-mcp source map (credits per call × volume). Offer to
run the enrichment as the next step — do not run it from this skill.

## Hard rule

This skill performs zero writes: no upserts, no dry-runs, no "small fixes". Its value is
that it is provably safe to run on day one.
