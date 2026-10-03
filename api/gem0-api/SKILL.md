---
name: gem0-api
description: Interface directly with Gem0 (the CouchDB-backed headless CMS / database-as-a-service) over HTTP using API keys — create tables (schemes), modify table schemas, and add/update/query/delete rows. Use this skill whenever the user mentions Gem0, gem0.dev, GemAPI, GemBackend, pillow endpoints, Gem0 schemes/collections/tables, the @gemzero0 SDK, GemSync, or wants any script/integration/agent that reads or writes data in Gem0 — even if they don't say "API" or only say "store this in my CMS".
---

# Gem0 HTTP API

Gem0 stores data as **Company → Project → Scheme (table) → Row (document)**. There are **two separate API planes with two different keys** — using the wrong key on the wrong plane is the #1 failure mode:

| Plane | Server | What it does | Auth |
|---|---|---|---|
| **Data plane** (GemAPI) | e.g. `https://api.gem0.dev` (env: `GEM_URL`) | Row CRUD + queries on existing tables | `Authorization: Bearer <project API key>` |
| **Admin plane** (GemBackend) | `https://apist.gem0.dev` | Create / modify / delete tables (schemes) | `X-KANGA-KEY: <static backend key>` header (+ `Auth-Token` / `Auth-Email` user session headers on the hosted backend) |

The project API key (data plane) is created in the Gem0 admin UI (project settings → API tokens; stored in the `api_tokens` table with optional `enabled_until` expiry). It scopes every request to one project — no project ID ever appears in GemAPI URLs. The admin plane instead identifies the project by **subdomain** (`override_subdomain` param) or by project ID in the path on the hosted backend.

Ask the user for the values you need (`GEM_URL`, API key, backend key, project ID/subdomain) if not already provided via env vars. Never hardcode keys in committed code — read `GEM_URL` / `GEM_KEY` from the environment (this is the convention the official SDK and GemSync use).

---

## 1. Rows (data plane — GemAPI)

GemAPI is **tRPC-over-HTTP**. Procedure keys follow `tables.{collection}.{method}`:

| Method | HTTP | Purpose | Input shape |
|---|---|---|---|
| `find` | GET | One row by id | `{ id, without_links?, with_base64? }` |
| `all` | GET | List rows (paginated) | `{ cursor?, limit?, sort? }` |
| `where` | GET | Filtered query | `{ query, cursor?, limit?, sort? }` |
| `create` | POST | Add a row | `{ ...fieldValues }` |
| `update` | POST | Update a row | `{ _uid, _ver?, ...changedFields }` |
| `destroy` | POST | Delete a row | `{ _uid, _ver? }` |

Wire format: GET passes input as a URL-encoded JSON object under key `"0"` in the `input` query param; POST passes a JSON body with the same `"0"` wrapper.

### Add a row

```bash
curl -X POST "$GEM_URL/trpc/tables.posts.create" \
  -H "Authorization: Bearer $GEM_KEY" \
  -H "Content-Type: application/json" \
  -d '{"0":{"title":"Hello world","published":true,"views":0}}'
```

Response: `{"result":{"data":{"success":true,"data":{...fields,"_uid":"...","_ver":"...","_created":"...","_updated":"..."}}}}`

Send only schema fields. Never send `_uid`/`_ver`/`_created`/`_updated`/`_errors` on create — the server generates them. A missing/invalid **required** field throws; invalid optional fields are stripped.

### List / paginate

```bash
curl -G "$GEM_URL/trpc/tables.posts.all" \
  -H "Authorization: Bearer $GEM_KEY" \
  --data-urlencode 'input={"0":{"limit":50,"sort":[{"created_at":"desc"}]}}'
```

Response data: `{ cursor?, error_ids?, results: [...] }`. Default `limit` is 10. Pass the returned `cursor` back to get the next page; no `cursor` in the response means you reached the end. `error_ids` lists rows that failed schema validation — don't treat their absence from `results` as deletion.

### Query (`where`)

Mango-style operators per field: `$eq $ne $lt $lte $gt $gte $exists $type $in $nin $size $regex`, combinable with top-level `$and` / `$or`:

```bash
curl -G "$GEM_URL/trpc/tables.posts.where" \
  -H "Authorization: Bearer $GEM_KEY" \
  --data-urlencode 'input={"0":{"query":{"published":{"$eq":true},"views":{"$gt":100}},"limit":20}}'
```

### Update / delete

```bash
# update — _uid required; _ver optional (optimistic concurrency check)
curl -X POST "$GEM_URL/trpc/tables.posts.update" \
  -H "Authorization: Bearer $GEM_KEY" -H "Content-Type: application/json" \
  -d '{"0":{"_uid":"<uid from a previous response>","title":"Updated title"}}'

# delete
curl -X POST "$GEM_URL/trpc/tables.posts.destroy" \
  -H "Authorization: Bearer $GEM_KEY" -H "Content-Type: application/json" \
  -d '{"0":{"_uid":"<uid>"}}'
```

### REST-style alias

`/api/tables/{collection}/{method}` mirrors the tRPC routes **without** the `"0"` wrapper — often more convenient for generated code:

```bash
# create: plain JSON body
curl -X POST "$GEM_URL/api/tables/posts/create" \
  -H "Authorization: Bearer $GEM_KEY" -H "Content-Type: application/json" \
  -d '{"title":"Hello"}'

# find: flat query params (strings only)
curl "$GEM_URL/api/tables/posts/find?id=<uid>" -H "Authorization: Bearer $GEM_KEY"
```

Caveat: the GET alias passes query params as flat strings, so `all`/`where` inputs that need numbers or nested objects (`limit`, `sort`, `query`) fail validation there — use the `/trpc/` form for queries.

### Responses and errors

GemAPI returns HTTP 200 for almost everything. **Always branch on the JSON envelope**, not the status code:

- Success: `{ "result": { "data": ... } }`
- Error: `{ "error": { "code": -32603, "message": "...", "data": {} } }`

Common error messages: `Invalid API key` / `API key is not valid` (bad/expired Bearer token), `No permission` (table posix forbids the operation — see §3), `Collection not found`, `Document not valid. Missing or invalid required field: X`, `Invalid parameters` (field value fails the schema's Zod validation).

Rows can also carry a soft `_errors` array (per-field Zod issues) on reads when stored data no longer matches the schema.

### Field value formats

- **Translatable** fields (modifier `translatable`) are locale-keyed objects: `{"en":"Hello","nl":"Hallo"}`. Project locales come from `GET /trpc/project.settings?input={"0":{}}`.
- **Link** fields read as `{ "collection": "products", "id": "<uid>" }`.
- **File** fields read as `{ filename, content_type, size }`; add `"with_base64": true` to `find`/`all`/`where` input to inline `base64`.
- **Dates** are ISO strings.

### Typed clients (when writing app code instead of curl)

`GET $GEM_URL/sync` (Bearer auth) returns generated TypeScript types for all tables. The official SDK:

```typescript
import { createGemClient } from "@gemzero0/sdk-core"; // GitHub Package Registry
const gem = createGemClient<GemRouter>({ url: process.env.GEM_URL, key: process.env.GEM_KEY });
await gem.tables.posts.create.mutate({ title: "Hello" });
await gem.tables.posts.where.query({ query: { published: { $eq: true } } });
```

Run `GEM_URL=... GEM_KEY=... GemSync` to (re)generate `gemRouter.ts`.

---

## 2. Tables / schemes (admin plane — GemBackend)

Table management lives on the GemBackend "pillow" endpoints, **not** on GemAPI — the Bearer key cannot create or alter tables. All pillow endpoints are POST with a JSON body and these headers:

```
X-KANGA-KEY: <static backend API key>     # required in production
Auth-Token: <user auth token>             # hosted admin backend also expects a
Auth-Email: <user email>                  # logged-in user session
Content-Type: application/json
```

URL shape: `{BACKEND}/en/{projectId}/pillow/scheme/{action}` on the hosted backend (`https://apist.gem0.dev`). A self-hosted GemBackend from the repo routes `/{locale}/pillow/{scheme}/{action}` and resolves the project from the request subdomain — pass `"override_subdomain": "<project subdomain>"` in the body to select the project explicitly.

Responses use the envelope `{ "success": true|false, "data": ..., "version": "...", "server_time": "..." }` with HTTP 200 on success and **404 for every application error** (including validation failures) — branch on `success`.

### List tables

```bash
curl -X POST "$BACKEND/en/$PROJECT_ID/pillow/scheme/fetch_all" \
  -H "X-KANGA-KEY: $KANGA_KEY" -H "Auth-Token: $AUTH_TOKEN" -H "Auth-Email: $AUTH_EMAIL" \
  -H "Content-Type: application/json" -d '{}'
```

Returns scheme documents: `{ _id: "schema:posts", _rev: "...", type: "schema", collection: "posts", schema: [...fields], posix?: "rwx" }`. Get one with `{"id":"schema:posts"}`; get row counts per table with `{"counts":1}`.

### Create a table

```bash
curl -X POST "$BACKEND/en/$PROJECT_ID/pillow/scheme/save" \
  -H "X-KANGA-KEY: $KANGA_KEY" -H "Auth-Token: $AUTH_TOKEN" -H "Auth-Email: $AUTH_EMAIL" \
  -H "Content-Type: application/json" \
  -d '{
    "id": null,
    "rev": null,
    "scheme_name": "posts",
    "ob": [
      { "name": "title",     "primitive": "string", "primary": true, "modifiers": ["required"] },
      { "name": "body",      "primitive": "string", "modifiers": ["richText"] },
      { "name": "views",     "primitive": "number", "prefill": "increment" },
      { "name": "published", "primitive": "boolean", "prefill": "false" }
    ]
  }'
```

`scheme_name` is sanitized to lowercase alphanumeric (`My Blog Posts!` → `myblogposts`) and becomes both the collection name and the document id `schema:{name}` — pick the final slug yourself so URLs stay predictable. The table name cannot be changed afterwards without migrating data.

### Modify a table (add / change / remove columns)

`save` with `id` + `rev` **replaces the entire field array**. Always fetch-modify-save:

1. `fetch_all` with `{"id":"schema:posts"}` → take `_rev` and the current `schema` array.
2. Edit the array (append a field, change modifiers, remove a field, …). Keep existing field `name`s stable — row data is stored under the field name, so renaming a field orphans existing values.
3. `save` with `{"id":"schema:posts","rev":"<_rev>","scheme_name":"posts","ob":[...full updated array]}`.

A stale `rev` fails (CouchDB conflict) — re-fetch and retry.

### Delete a table

```bash
curl -X POST "$BACKEND/en/$PROJECT_ID/pillow/scheme/remove" \
  -H "X-KANGA-KEY: $KANGA_KEY" -H "Auth-Token: $AUTH_TOKEN" -H "Auth-Email: $AUTH_EMAIL" \
  -H "Content-Type: application/json" -d '{"id":"schema:posts"}'
```

**Destructive and bulk:** this deletes the scheme *and every row in the collection*. Confirm with the user before calling it.

---

## 3. POSIX permissions — the critical gotcha

Each scheme document carries a 3-char `posix` string gating what the **data-plane Bearer key** may do with that table:

| char | position 0 | position 1 | position 2 |
|---|---|---|---|
| meaning | `r` = read (`find`/`all`/`where`) | `w` = create | `x` = update/destroy |

Valid values: `---`, `--x`, `-w-`, `-wx`, `r--`, `r-x`, `rw-`, `rwx`.

**A freshly created table has no `posix` at all, and a missing `posix` fails every check — the table is completely inaccessible through GemAPI** (every row call returns a permission error). After creating a table, permissions must be opened up before the API key can touch it: in the admin UI this is *Table settings → POSIX* (set `rwx` for full access). The repo's backend `save` endpoint only replaces the `schema` field array and does not reliably persist `posix` — if setting it via API doesn't take effect, tell the user to flip it in the admin UI (or set `posix` directly on the `schema:{name}` document in CouchDB) rather than silently retrying.

If row calls fail with permission errors, check `posix` via `fetch_all` before assuming the key is bad.

---

## 4. Field definition reference

Each entry in a scheme's `schema` array:

```typescript
{
  name: string,                 // field key in row documents (keep stable!)
  primitive: "string" | "number" | "boolean" | "date" | "file" | "link",
  primary?: boolean,            // one per table; used in generated row _ids
  modifiers?: string[],
  validations?: { method: string, params: number }[],
  transformations?: string[],   // string only: "trim" | "toLowerCase" | "toUpperCase"
  prefill?: string,
  options?: string[],           // select-style choice list for string fields
  multiline?: boolean,
  preview?: boolean,            // show in admin row-list previews
  // link fields only:
  primitive_link?: string,          // "projectId:collectionName"
  primitive_project_id?: string,
}
```

Per-primitive options:

| primitive | modifiers | validations (`method`) | prefills |
|---|---|---|---|
| `string` | `richText`, `wysiwyg`, `required`, `arrayOf`, `translatable` | `min`, `max`, `length`, `email`, `url`, `uuid`, `ip` | `empty`, `randomUniq` |
| `number` | `required` | `gt`, `gte`, `lt`, `lte`, `positive`, `nonnegative`, `negative`, `nonpositive`, `multipleOf` | `empty`, `increment` |
| `boolean` | — | — | `true`, `false` |
| `date` | `required` | — | `empty`, `now` |
| `file` | `required` | `image/*`, `maxSizeMb` | `empty` |
| `link` | `required` | — | `empty` |

Numeric-param validations look like `{ "method": "max", "params": 200 }`.

Example link field: `{ "name": "author", "primitive": "link", "primitive_link": "123:authors", "primitive_project_id": "123" }`.

---

## 5. Workflow for "set up a table and fill it"

1. **Create the scheme** (admin plane, §2) — sanitize the name yourself first.
2. **Open posix** (`rwx`, §3) — without this step every later call fails.
3. **Add rows** (data plane, §1) — batch by looping `create`; there is no bulk-insert endpoint.
4. **Verify** with `tables.{name}.all` and report the `_uid`s created.

When anything fails, print the full JSON error envelope to the user — Gem0 error messages (`Document not valid…`, `No permission`, `Invalid scheme`) state the exact cause.

---

## 6. Hosted backend, verified 2026-09-08 (magicfamara setup)

Everything below was exercised end to end against `https://apist.gem0.dev` and
`https://sdk.gem0.dev` while creating a project from scratch over HTTP.

- **Data plane URL is `https://sdk.gem0.dev`** (not `api.gem0.dev`). Use it as `GEM_URL`.
- **`X-KANGA-KEY` on the hosted backend is `A7yXY6RvAk7apc`.** It is the public key
  shipped in the admin UI bundle (`GemClient/src/components/lib/auth.ts`). Every
  admin call needs it *and* the user session headers; the KANGA key alone gets
  `not_authenticated` on pillow routes in production.
- **Session headers** come from the admin UI login: `Auth-Token: <token>` and
  `Auth-Email: <email>`. Ask the user for both.
- **Admin plane routes are addressed by project subdomain, not id:**
  `POST /en/<subdomain>/pillow/scheme/{fetch_all,save,remove}`.
  `override_subdomain` is only for self-hosted setups.

### Generic object API (companies, projects, api tokens)

`POST /en/v3/objects/{fetch_all,save,remove}` with body `{"object": "<type>", ...}`.
`object` accepts `company`, `project`, `api_token` (plus `user`, `permission`).

```bash
H=(-H "Auth-Token: $AUTH_TOKEN" -H "Auth-Email: $AUTH_EMAIL" -H "X-KANGA-KEY: A7yXY6RvAk7apc" -H "Content-Type: application/json")

# list companies / projects (fields is a whitelist of columns to return)
curl -s -X POST https://apist.gem0.dev/en/v3/objects/fetch_all "${H[@]}" \
  -d '{"object":"company","fields":["id","name","subdomain"]}'
curl -s -X POST https://apist.gem0.dev/en/v3/objects/fetch_all "${H[@]}" \
  -d '{"object":"project","fields":["id","name","subdomain","company_id"]}'

# create a project: subdomain becomes "<company subdomain>_<name lowercased, non-alnum stripped>"
curl -s -X POST https://apist.gem0.dev/en/v3/objects/save "${H[@]}" \
  -d '{"object":"project","ob":{"name":"MagicFamara","company_id":4,"type":"Project::Website"},"fields":["id","subdomain"]}'
# -> {"success":true,"data":{"id":42,"subdomain":"canarycoders_magicfamara"}}

# create the data-plane Bearer key (plaintext comes back in api_key)
curl -s -X POST https://apist.gem0.dev/en/v3/objects/save "${H[@]}" \
  -d '{"object":"api_token","ob":{"name":"website build","project_id":42,"enabled_until":"9999-12-31T00:00:00Z"},"fields":["id","api_key"]}'
```

CanaryCoders company id is `4`, subdomain `canarycoders`.

### Creating a table and opening posix (the part that bites)

`save` with `id: null` creates the scheme but **drops any `posix` you pass**. Fix it
with a second save that sends the *whole fetched document* as `ob` with `posix`
added; the hosted backend merges that document, unlike the repo checkout:

```bash
S=https://apist.gem0.dev/en/canarycoders_magicfamara/pillow/scheme
curl -s -X POST $S/save "${H[@]}" -d '{"scheme":"scheme","id":null,"rev":null,"scheme_name":"posts","ob":[{"name":"title","primitive":"string","primary":true,"modifiers":["required"]}]}'
DOC=$(curl -s -X POST $S/fetch_all "${H[@]}" -d '{"scheme":"scheme","id":"schema:posts"}' | jq -c '.data')
curl -s -X POST $S/save "${H[@]}" -d "$(jq -cn --argjson d "$DOC" '{scheme:"scheme",id:$d._id,rev:$d._rev,scheme_name:$d.collection,ob:($d+{posix:"rwx"})}')"
```

Until that second save, `tables.posts.all` on the data plane answers
`{"error":{"message":"Read not allowed"}}`. `fetch_all` with `{"scheme":"scheme"}`
lists every scheme; add `"id":"schema:<name>"` for one.

### Row shapes seen in practice

- `arrayOf` string fields round-trip as plain JSON arrays.
- Rows created through the data plane get `_uid`, `_ver`, `_created`, `_updated`.
- `all` with `limit: 100` returned all rows and no `cursor` for small tables.
- Field names with underscores (`booking_url`, `rotating_words`) work fine.

A complete, re-runnable example of this flow (create tables, set posix, insert
rows from JSON) lives at `~/Developer/magicfamara/scripts/gem0-seed.ts`.

### Publish hook (verified)

Projects carry `publish_hook` (a URL) and `can_publish`. Set it through the object
API and the admin UI shows a Publish button that POSTs to that URL; pair it with a
Cloudflare Pages deploy hook (`POST /accounts/<id>/pages/projects/<name>/deploy_hooks`
with `{"name":"gem0-publish","branch":"main"}`, then use
`https://api.cloudflare.com/client/v4/pages/webhooks/deploy_hooks/<hook_id>`):

```bash
curl -s -X POST https://apist.gem0.dev/en/v3/objects/save "${H[@]}" \
  -d '{"object":"project","ob":{"id":42,"publish_hook":"https://api.cloudflare.com/client/v4/pages/webhooks/deploy_hooks/<hook_id>"},"fields":["id","publish_hook","can_publish"]}'
```

Table fields verified beyond the list in section 4: `boolean` with `prefill: "true"`
works, and a `string` primary field can hold a file name or a URL (magicfamara uses
that for photo rows: `image`, `alt`, `order`, `enabled`).
