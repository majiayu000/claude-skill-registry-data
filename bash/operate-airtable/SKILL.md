---
name: operate-airtable
description: Use when scripting Airtable — scoped PATs, rate limits and 10-record batches, field IDs over names, expiring webhooks, per-environment bases with a schema diff, and tables owned by other systems left read-only.
---

# Operate Airtable

No CLI from Airtable — the Web API (v0) with a personal access token (PAT), plus `pyairtable` or
`curl`/`httpie` on top. Read-only by default. **Never change prd by hand when the base is
schema-managed by a deploy step; change the dev base, diff, promote.** Never write to a table
another system owns.

## 1. Audit — which token, which bases (change nothing)

```bash
command -v curl jq; pip show pyairtable 2>/dev/null | head -2        # tools present
curl -s -H "Authorization: Bearer $AIRTABLE_API_KEY" https://api.airtable.com/v0/meta/whoami | jq '.id'   # token works
curl -s -H "Authorization: Bearer $AIRTABLE_API_KEY" "https://api.airtable.com/v0/meta/bases" | jq '.bases[] | {id, name}'   # needs schema.bases:read
```

`whoami` proves the token without printing it — the token itself never appears in output, logs or
the ticket. Then map the environments: dev/stg/prd are **separate bases**; find their IDs
(`appXXXXXXXXXXXXXX`) in the repo's env config, not by guesswork. ID grammar: base `app…`,
table `tbl…`, field `fld…`, view `viw…`.

## 2. Decide

- **Read-only investigation (default)** — list records, metadata, webhook listings.
- **Schema change** (field, table, view) — make it on the dev base, then promote to stg and prd
  bases through the repo's deploy flow with a schema diff (step 6). A prd schema change made by
  hand is the thing this skill exists to prevent.
- **Data one-off with a record** — backfill, cleanup, migration script. Batched (step 5), dry-run
  first (`filterByFormula` count), output record IDs into the ticket.

## 3. Detect the track

| Signal | Track | Then |
|---|---|---|
| Repo holds base IDs per env and a schema-diff script | Managed bases | Change dev, diff, promote |
| Table has a writing system (automation, integration, sync) | Foreign-owned table | Read-only for you — coordinate with the owner |
| Interface-only collaborators on a base | Interface track | Data access needs a real PAT with base scope; interface changes are UI work |

```bash
curl -s -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  "https://api.airtable.com/v0/meta/bases/<base-id>/tables" | jq '.tables[] | {id, name}'    # what exists, by ID
```

## 4. Install only what is missing

```bash
brew install httpie jq                      # verify version before pinning (../_shared/stack-versions.md)
pip install pyairtable                      # includes a CLI — *unverified*
```

The Airtable MCP server, when present, is preferred for exploration; scripts stay on the API
([cli-toolbox](../_shared/cli-toolbox.md)).

## 5. Do the work

**Read records** (URL-encode formulas; page with `offset`):

```bash
curl -s -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  "https://api.airtable.com/v0/<base-id>/<table-id>?filterByFormula=%7B<field-id>%7D%3D%27<value>%27&maxRecords=10" \
  | jq '.records | length'
```

**Write in batches of at most 10 records per request** — larger batches are rejected; the rate
limit is **5 requests/second per base**, and a 429 means stop for 30 seconds, not retry faster:

```bash
curl -s -X POST -H "Authorization: Bearer $AIRTABLE_API_KEY" -H "Content-Type: application/json" \
  -d '{"records":[{"fields":{"<field-id>":"<value>"}}],"typecast":true}' \
  "https://api.airtable.com/v0/<base-id>/<table-id>" | jq '.records[].id'
```

`typecast: true` coerces values to field types — use it deliberately, not by default. **Use field
IDs (`fld…`), not names**: names change, names are duplicated across tables, and select options
can carry trailing spaces that make value matches fail invisibly.

**Metadata** (schema checks, the diff input): `GET /v0/meta/bases/<base-id>/tables` — some field
types expose no formula/count filter metadata; treat a missing filter spec as "no filter", never
as "field absent".

**Linked records** carry arrays of record IDs; writing one means writing the OTHER table's record
IDs — check ownership before you touch them.

**Webhooks** expire after ~7 days unless refreshed — *verify* the current refresh path in the
docs before relying on it; payloads are not pushed, they are fetched via the list-payloads
endpoint after the notification. A webhook URL pointed at the wrong base still returns 200 and
the run is simply skipped — verify with a test write and the payload list, not with the status
code. **Automations are not in the API**: deploying one is a manual UI step; record it in the
runbook as a step with an owner.

## 6. Wire

- **One PAT per integration**, scoped to the bases it needs (`data.records:read`,
  `data.records:write`, `schema.bases:read`) — never one god-PAT for every script.
- **PATs live in the secret store** ([manage-secrets](../../infra/manage-secrets/SKILL.md)) and
  reach scripts as `AIRTABLE_API_KEY`; base IDs per env live in the repo env config
  (`AIRTABLE_BASE_PRD=appXXXXXXXXXXXXXX` as the placeholder shape).
- **Dev/stg/prd as separate bases with a schema-diff check** — the metadata API output of each
  base, diffed in CI, so prd cannot drift from dev silently.
- Tools and versions: [cli-toolbox](../_shared/cli-toolbox.md), [stack-versions](../_shared/stack-versions.md).

## 7. Verify

```bash
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  https://api.airtable.com/v0/meta/whoami                       # 200
curl -s -H "Authorization: Bearer $AIRTABLE_API_KEY" "https://api.airtable.com/v0/meta/bases/<prd-base-id>/tables" \
  | jq '[.tables[].fields[].id] | length'                        # field count matches the dev base after promotion
```

A write script verifies by reading back the record IDs it created; a webhook verifies by one test
write and the payload listing. A migration verifies by record counts per table before and after.

## References
- [airtable-patterns.md](./airtable-patterns.md): the traps — scopes, IDs over names, batching
  and limits, webhooks, automations, table ownership, environment separation.
- [Airtable tool guide](../../../guides/tools/airtable/README.md): the picture version for people.
- [cli-toolbox](../_shared/cli-toolbox.md), [stack-versions](../_shared/stack-versions.md).
- [manage-secrets](../../infra/manage-secrets/SKILL.md).
- [security-baseline](../../core/_shared/security-baseline.md).
