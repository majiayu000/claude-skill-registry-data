---
name: credentials
description: n8n credential types, REST API credential management, HTTP Request node authentication, predefinedCredentialType vs genericCredentialType, httpCustomAuth JSON format, credential creation via API, credential testing, credential type discovery, OAuth flows, and service-specific credential schemas. Auto-triggers on n8n credential, httpCustomAuth, predefinedCredentialType, genericCredentialType, credential API, credential test, OAuth, and HTTP Request auth tasks.
disable-model-invocation: false
user-invokable: true
argument-hint: "credential task"
---

# n8n Credentials

Credential types, REST API management, testing, type discovery, OAuth flows, and HTTP Request node authentication.

**Source: n8n-io/n8n GitHub repo, master branch. Verified 2026-03-30.**

---

## 1. Discovering Credential Types

### List all available types (internal API, session cookie)

```
GET /types/credentials.json
```

Returns every `ICredentialType` loaded from node packages: name, displayName, properties, test definition, extends (parent types).

Source: `credential-types.ts` — `recognizes(type)`, `getByName(type)`, `getSupportedNodes(type)`, `getParentTypes(type)`.

### Get JSON Schema for a specific type (public API, API key)

```
GET /api/v1/credentials/schema/:credentialTypeName
```

Returns JSON Schema with required fields. Hidden fields filtered out.

```bash
curl -H "X-N8N-API-KEY: $KEY" "$N8N_URL/api/v1/credentials/schema/freshdeskApi"
```
```json
{
  "additionalProperties": false,
  "type": "object",
  "properties": {
    "apiKey": { "type": "string" },
    "domain": { "type": "string" }
  },
  "required": ["apiKey", "domain"]
}
```

Source: `credentials.handler.ts` — calls `CredentialsHelper.getCredentialsProperties()`, filters hidden, converts via `toJsonSchema()`.

---

## 2. HTTP Request Node — Two Auth Modes

### Mode A: `genericCredentialType` (Generic Auth)

| `genericAuthType` value | Credential type | Fields | How it authenticates |
|---|---|---|---|
| `httpBasicAuth` | Basic Auth | `user`, `password` | `Authorization: Basic base64(user:pass)` |
| `httpBearerAuth` | Bearer Auth | `token` | `Authorization: Bearer {token}` |
| `httpHeaderAuth` | Header Auth | `name`, `value` | `{name}: {value}` header |
| `httpQueryAuth` | Query Auth | `name`, `value` | `?{name}={value}` query param |
| `httpDigestAuth` | Digest Auth | `user`, `password` | HTTP Digest challenge-response |
| `httpCustomAuth` | Custom Auth | `json` (freeform) | Headers + body + query from JSON |

```json
{ "authentication": "genericCredentialType", "genericAuthType": "httpHeaderAuth" }
```

### Mode B: `predefinedCredentialType` (Service Credential)

```json
{
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "supabaseApi"
}
```

```json
{
  "credentials": {
    "supabaseApi": { "id": "YOUR_CREDENTIAL_ID", "name": "Supabase account" }
  }
}
```

### When to Use Which

| Scenario | Use |
|---|---|
| Service has a built-in n8n credential type | `predefinedCredentialType` |
| Custom API with API key in header | `genericCredentialType` + `httpHeaderAuth` |
| Custom API with bearer token | `genericCredentialType` + `httpBearerAuth` |
| Login with email/password in body | `genericCredentialType` + `httpCustomAuth` |
| Multiple headers or mixed auth | `genericCredentialType` + `httpCustomAuth` |

---

## 3. httpCustomAuth — JSON Format

One field: `json` (a JSON string, not an object).

```json
{
  "headers": { "Header-Name": "value" },
  "body": { "field": "value" },
  "qs": { "param": "value" }
}
```

All three keys optional.

### Create via REST API

```bash
curl -X POST "$N8N_URL/api/v1/credentials" \
  -H "X-N8N-API-KEY: $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Custom Auth",
    "type": "httpCustomAuth",
    "data": {
      "json": "{\"headers\":{\"X-Api-Key\":\"secret123\"}}"
    }
  }'
```

**Critical:** `json` field is a **JSON string inside JSON** — double-encode it.

---

## 4. REST API — Credential CRUD

**Auth:** `X-N8N-API-KEY` header (public API) or session cookie (internal API).

| Method | Path | API | What |
|---|---|---|---|
| `POST` | `/api/v1/credentials` | Both | Create. Body: `{ name, type, data }`. Public API validates data against type's JSON Schema. |
| `GET` | `/api/v1/credentials` | Both | List (metadata, no secrets) |
| `GET` | `/api/v1/credentials/:id` | Internal | Get one. Optional `includeData=true` (returns redacted values) |
| `GET` | `/api/v1/credentials/schema/:type` | Public | JSON Schema for a credential type |
| `PATCH` | `/api/v1/credentials/:id` | Both | Update |
| `DELETE` | `/api/v1/credentials/:id` | Both | Delete |
| `PUT` | `/api/v1/credentials/:id/transfer` | Both | Transfer to another project |
| `PUT` | `/api/v1/credentials/:id/share` | Internal | Share with projects (licensed) |
| `GET` | `/api/v1/credentials/for-workflow?workflowId=X` | Internal | Credentials available for a workflow |
| `GET` | `/api/v1/credentials/new?name=X` | Internal | Generate unique credential name |

### Partial Update

**Key flag — `isPartialData`** (source: `credentials.handler.ts`):
- `false` (default): replaces the entire `data` object
- `true`: merges with existing decrypted data, then unredacts blanked values

```bash
curl -X PATCH "$N8N_URL/api/v1/credentials/:id" \
  -H "X-N8N-API-KEY: $KEY" \
  -H "Content-Type: application/json" \
  -d '{ "data": { "apiKey": "new-key" }, "isPartialData": true }'
```

---

## 5. Testing Credentials

**Endpoint:** `POST /api/v1/credentials/test`
**API:** Internal only (session cookie). NOT on public API.

```bash
curl -X POST "$N8N_URL/api/v1/credentials/test" \
  -H "Cookie: $SESSION_COOKIE" \
  -H "Content-Type: application/json" \
  -d '{ "credentials": { "id": "CRED_ID", "name": "My Cred", "type": "githubApi" } }'
```

**Response:** `{ "status": "OK", "message": "Connection successful!" }` or `{ "status": "Error", "message": "..." }`

### Three test strategies (source: `credentials-tester.service.ts`)

1. **Credential-defined test:** `ICredentialType.test` property contains a request definition — used directly
2. **Node-defined `testedBy`:** Iterates nodes supporting this credential type. If `testedBy` is a string, calls `nodeType.methods.credentialTest[name]`. If object, treats as request definition.
3. **OAuth2 token check:** For types extending `oAuth2Api`, checks `oauthTokenData.access_token` exists

If no test exists: `{ "status": "Error", "message": "No testing function found for this credential." }`

### Internal process (source: `credentials.controller.ts`)

1. Looks up stored credential by `id`, verifies `credential:read` scope
2. Decrypts stored data
3. Merges submitted data with stored data
4. `unredact()` replaces blanked values with originals
5. Delegates to CredentialsTester

---

## 6. OAuth Flows

### OAuth2 (source: `oauth2-credential.controller.ts`)

**Step 1 — Get authorization URL:**
```
GET /api/v1/oauth2-credential/auth?id=CREDENTIAL_ID
```
Returns authorization URL string. Generates CSRF state token. Supports PKCE (`grantType: 'pkce'`) and body auth (`authentication: 'body'`).

**Step 2 — Callback:**
```
GET /api/v1/oauth2-credential/callback?code=X&state=Y
```
Exchanges code for tokens. Stores `oauthTokenData` encrypted in credential.

### OAuth1 (source: `oauth1-credential.controller.ts`)

**Step 1:** `GET /api/v1/oauth1-credential/auth?id=CREDENTIAL_ID`
**Step 2:** `GET /api/v1/oauth1-credential/callback?oauth_verifier=X&oauth_token=Y&state=Z`

**Note:** `oauthTokenData` is stripped from PATCH body — tokens are only set via the callback flow.

---

## 7. Gotchas

1. **httpCustomAuth `json` is a string, not object** — `"json": "{...}"` not `"json": {...}`
2. **Values blanked on read** — API returns `__n8n_blank_value_...`. Use `isPartialData: true` on PATCH to avoid re-sending all fields.
3. **`$env` in sub-workflows** — may be restricted by `N8N_RESTRICT_ENVIRONMENT_VARIABLES_ACCESS`. Use credentials instead.
4. **`predefinedCredentialType` must match node's list** — type needs `genericAuth = true` or be in supported types
5. **Credentials shared by reference** — update affects ALL workflows using it
6. **IDs are instance-specific** — relink after importing to new instance
7. **Managed credentials** — cannot be updated (returns 400)
8. **OAuth tokens** — only set via callback flow, stripped from PATCH body

---

## 8. Links

- [HTTP Request credentials docs](https://docs.n8n.io/integrations/builtin/credentials/httprequest/)
- [Credentials library](https://docs.n8n.io/credentials/)
- [Credential source files](https://github.com/n8n-io/n8n/tree/master/packages/nodes-base/credentials)
