---
name: bb-graphql
description: Hunt GraphQL-specific vulnerabilities — introspection, field-level authorization (BOLA via node IDs), mutation abuse, batching/aliasing bypasses, GraphQL CSRF, and collaborator/invite mutations leaking user data. Use whenever the user mentions GraphQL, introspection, queries/mutations, graphql BOLA, node IDs, or a target whose API is GraphQL.
---

# GraphQL Hunter

GraphQL concentrates the whole API in one endpoint — one authz mistake leaks everything. Find it first: `/graphql`, `/graphql/`, `/api/graphql`, `/api/mktplace-portal/frontend/bff/graphql/`, or sniff POSTs with `"query":` bodies.

## Real-bug anchors (what actually paid — query bb-disclosures for more)
- **$12,500** View any user's email via the **`/SaveCollaboratorsMutation`** operation — one mutation missing an ownership check on an ID argument.
- **$25,000** (REST sibling) `/reports/:id.json` disclosed sensitive user attributes — fat JSON objects by ID.
Delta lesson: the paid GraphQL bugs are **mutations/queries taking an ID argument without an ownership check**, especially invite/collaborator/save operations. The names to probe: `Save*`, `Invite*`, `Collaborat*`, `Transfer*`, `Accept*`.

## Recon
1. **Introspection**: `{"query":"{__schema{types{name,fields{name}}}}"}`. Disabled? Note it (introspection alone is a rejected finding on most programs) — operations are in the JS bundles anyway (js-recon extracts every `query`/`mutation` name).
2. **Map mutations by risk**: anything named update*, delete*, create*, upload*, cancel*, accept*, save*, invite* is the authz test list. Queries named getUser*, orders*, documents* are the data-exfil candidates.
3. **Auth model**: session cookie vs bearer vs both; CSRF headers required?

## The four bug classes
1. **Field-level BOLA (the payer)**: object IDs as arguments. `query { order(id: OTHER) { ... } }` — with two own accounts, swap every ID type. Also global node IDs: `node(id: base64("Order:123"))`, `node(id: base64("User:456"))` — decode/encode ID formats freely.
2. **Mutation authz**: can account A run `updateCompanyDetails(id: B)` / `cancelOrder(id: B)` / `saveCollaborators(id: B)`? Positive control with the owner first (idor-runner handles the discipline).
3. **Batching/aliasing abuse**: aliases to fetch N objects in one request (`{a:order(id:1){..} b:order(id:2){..}}`) — bypasses rate limits and 1-per-request authz logging; depth-nesting for DoS is FORBIDDEN (program rules) — cap depth ~5.
4. **GraphQL CSRF**: if auth is cookie-based and no CSRF token/custom header required, a cross-origin `fetch` with `content-type: text/plain` + `{"query":"mutation{...}"}` from an attacker page executes mutations as the victim. Prove with a harmless mutation (update own-test-field on your own account via simulated victim page).

## Verdict + evidence
- Foreign ID returns data / mutation succeeds → full request body + response as PoC (exactly reproducible cURL with `-d '{"query":"..."}'`).
- "Introspection enabled", "depth limit missing" alone → rejected; only as supporting detail of a real authz bug.
- Test with the same throttle discipline (1-2 req/s); batching counts as multiple logical requests.
