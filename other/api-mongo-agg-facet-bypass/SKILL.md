---
name: api-mongo-agg-facet-bypass
description: >
  Bypass a MongoDB aggregation-pipeline stage allowlist by nesting disallowed read stages
  inside $facet, then $unionWith/$lookup sibling collections to exfiltrate secrets
  (invite tokens, creds, hashes). Load when: an endpoint accepts a user-supplied `pipeline`
  (or errors like "operator-form queries not accepted, use the pipeline parameter"), a
  Node/Express + MongoDB backend, 24-hex `_id`s, or an "advanced query" API. Authorized targets only.
domain: api
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A03:2021-Injection]
cwe: [CWE-943]
schema_version: 1
---

# MongoDB aggregation injection — $facet allowlist bypass → cross-collection read

## When it applies
- An API runs a user-controlled **aggregation pipeline** on a fixed collection
  (`db.collection('x').aggregate(userPipeline)`), usually exposed as a `pipeline`
  query/body parameter for "advanced" search.
- The server defends with a **stage allowlist** — only screens the *top-level* stage
  names (`$match/$project/$sort/$limit/$facet` allowed; `$lookup/$unionWith/$group/…`
  rejected with something like `"invalid or disallowed pipeline stage"`).
- Tell-tale that a `pipeline` param even exists: sending the normal search term as a
  Mongo **operator object** (`?q[$ne]=x`) returns a hint such as
  `"Operator-form queries not accepted on 'q'. Use the 'pipeline' parameter…"`.

## Why it works
The allowlist inspects only the outermost stage keys. **`$facet` runs sub-pipelines
whose stages are never re-screened** by the app, so a disallowed read stage placed
inside a `$facet` sub-pipeline reaches MongoDB unchecked. MongoDB itself still forbids
a few stages inside `$facet` (`$out/$merge/$collStats/$indexStats/$listCatalog/$documents`),
but it **permits `$lookup` and `$unionWith`** there — and those read *other collections
in the same database*. That turns a "search our metadata" endpoint into "read any
collection in this DB".

## Method
1. **Confirm the pipeline sink & allowlist.** Baseline `?pipeline=[{"$limit":1}]` returns
   docs; `?pipeline=[{"$count":"n"}]` / `$group` / top-level `$unionWith` → "disallowed stage".
2. **Leak the namespace.** Trigger a Mongo error (e.g. `$facet` containing a stage Mongo
   rejects) — the 500 body usually includes `"ns":"<db>.<collection>"`. Now you know the DB.
3. **Read a sibling collection** (drop the base docs first so output is only the target):
   ```json
   [{"$facet":{"r":[
       {"$match":{"<anyfield>":"__none__"}},
       {"$unionWith":{"coll":"<target_collection>","pipeline":[{"$limit":20}]}}
   ]}}]
   ```
   `$unionWith` here is legal ONLY inside `$facet` (top-level → allowlist rejects it).
4. **Enumerate collection names** you don't know: build one `$facet` with many sub-pipelines,
   each `$unionWith`-ing a candidate name + `$limit:1`; names that return docs exist & are
   non-empty. **Brute the same naming style as any collection you already know**
   (e.g. known `mds_entries` ⇒ try `pending_invites`, `operator_accounts`, `invite_tokens`).
5. **Loot** the target collection (invite tokens, password hashes, session docs, API keys)
   and pivot (register/login, crack hashes, forge sessions).

## Tools
- `curl -G --data-urlencode 'pipeline=…'` (single-quote so the shell doesn't eat `$`), or a
  short Python `urllib` helper that JSON-encodes and URL-encodes the pipeline (cleaner for
  building big `$facet` maps and parsing results). See `aegis/exploit-dev/*.py` for a worked helper.

## Gotchas
- **Shell `$` expansion**: `"?q[$ne]=x"` in double quotes becomes `?q[]=x` in bash/zsh —
  you'll wrongly conclude "not injectable". Use single quotes / `--data-urlencode`.
- **`$unionWith`/`$lookup` are same-database only.** Cross-DB `{from:{db,coll}}` is a hard
  MongoDB block ("not supported for db: X") for everything except a couple of `config.*`
  system namespaces (empty on standalone). If the app data seems missing, it's almost always
  a *collection-name* you haven't guessed in the *same* DB — not a different DB.
- `$collStats/$listCatalog/$documents` can't nest in `$facet` (Mongo rejects) — so you can't
  cheaply list empty collections; rely on `$unionWith` name-brute for non-empty ones.
- Empty `$unionWith`/`$lookup` result = collection empty *or* absent; the two look identical.

## Verify success
Step 3/4 returns documents whose **fields differ from the base collection** (e.g. a
`token`/`password`/`session` field where the endpoint should only ever return metadata).
That is data exfiltration from a collection the endpoint never intended to expose.

## Learned on
**AEGIS lab, 2026-08** — `GET /api/v1/aegis-mds/search?pipeline=` on `aegis_mds.mds_entries`;
`$facet`→`$unionWith pending_invites` leaked an unredeemed 64-hex WebAuthn invite token →
`register/begin` (attestation:"none") → software authenticator → login. Full worked example
in `aegis/notes.md` (§4–6).
