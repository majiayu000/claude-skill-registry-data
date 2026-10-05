---
name: connection-profile
description: Connection profile schema design and implementation. Use when designing or implementing connectionProfile.yml or connectionState.yml files.
---

# Connection Profile & State Design Rules

**Rules for designing connectionProfile.yml and connectionState.yml schemas**

## 🚨 CRITICAL RULES

### Rule 1: Always Extend Core Profiles

**NEVER create custom profiles from scratch - ALWAYS extend core profiles**

```yaml
# ❌ WRONG - Custom profile
type: object
properties:
  apiKey:
    type: string

# ✅ CORRECT - Extend core profile
$ref: './node_modules/@zerobias-org/types-core/schema/tokenProfile.yml'
```

### Rule 2: connectionState MUST Extend baseConnectionState

**🚨 MANDATORY**: connectionState.yml MUST extend baseConnectionState.yml for expiresIn

```yaml
# ✅ CORRECT - Extends base with expiresIn
allOf:
  - $ref: './node_modules/@zerobias-org/types-core/schema/baseConnectionState.yml'
  - type: object
    properties:
      accessToken:
        type: string

# ❌ WRONG - Missing baseConnectionState
type: object
properties:
  accessToken:
    type: string
  # Missing expiresIn!
```

**WHY**: Server uses expiresIn to schedule automatic token refresh cronjobs

### Rule 3: expiresIn Must Be in Seconds

```yaml
# ✅ CORRECT
expiresIn:
  type: integer
  description: Token expiry time in SECONDS from now

# ❌ WRONG
expiresAt:
  type: string  # Don't use expiresAt, convert to expiresIn
```

**Calculation**: `expiresIn = Math.floor((expiresAt - now) / 1000)`

## Core Profile Selection

### Available Core Profiles

| Profile | When to Use | Contains |
|---------|-------------|----------|
| **tokenProfile.yml** | API Key, Bearer Token, PAT | token |
| **oauthClientProfile.yml** | OAuth2 Client Credentials | clientId, clientSecret |
| **oauthTokenProfile.yml** | OAuth2 with Refresh | clientId, clientSecret |
| **basicConnection.yml** | Username/Password, Email/Password | username, password |

**Path**: `./node_modules/@zerobias-org/types-core/schema/{profileName}.yml`

### Selection Decision Tree

```
@credential-manager provides authMethodType:

IF authMethodType == "bearer-token" OR "api-key"
  → EXTEND tokenProfile.yml

IF authMethodType == "oauth2-client-credentials"
  → EXTEND oauthClientProfile.yml

IF authMethodType == "oauth2-authorization-code"
  → EXTEND oauthTokenProfile.yml

IF authMethodType == "basic-auth"
  → EXTEND basicConnection.yml
```

## Available Core States

| State | When to Use | Contains |
|-------|-------------|----------|
| **tokenConnectionState.yml** | Simple token auth | accessToken + expiresIn |
| **oauthTokenState.yml** | OAuth with refresh | accessToken + refreshToken + expiresIn |

### State Selection

```
IF requiresRefresh == false
  → EXTEND tokenConnectionState.yml

IF requiresRefresh == true
  → EXTEND oauthTokenState.yml
```

## Common Patterns

### Pattern 1: Simple API Token

```yaml
# connectionProfile.yml
$ref: './node_modules/@zerobias-org/types-core/schema/tokenProfile.yml'

# connectionState.yml
$ref: './node_modules/@zerobias-org/types-core/schema/tokenConnectionState.yml'
```

### Pattern 2: OAuth Client Credentials

```yaml
# connectionProfile.yml
$ref: './node_modules/@zerobias-org/types-core/schema/oauthClientProfile.yml'

# connectionState.yml (no refresh)
$ref: './node_modules/@zerobias-org/types-core/schema/tokenConnectionState.yml'
```

### Pattern 3: OAuth with Refresh Token

```yaml
# connectionProfile.yml
$ref: './node_modules/@zerobias-org/types-core/schema/oauthTokenProfile.yml'

# connectionState.yml
$ref: './node_modules/@zerobias-org/types-core/schema/oauthTokenState.yml'
```

## 🚨 CRITICAL: OAuth Click-to-Connect — 3 layers (only 1 is insider)

**Choosing an OAuth `authorization_code` flow (the Hub "Connect" button) spans three layers, and
two of the three are contributor-self-serve content-as-code:**

1. **Module** — connectionProfile/state + `connect()/refresh()` (you author).
2. **Provider wiring** — the `oauth` artifact (`index.yml {id,url}`) + the `x-oauth-providers`
   link (you author + load as content — even to your own org first).
3. **External app + secret** — register the OAuth app and put client_id/secret in AWS Secrets
   Manager (**the only genuinely-insider step**; secrets can't be content).

If you ship layers 1–2 but no one does layer 3, the button stays dark — so **when OAuth
authorization-code is chosen, open a task for layer 3**.

### The module half — YOU author this (fully self-serve)

**Copy a real shipped OAuth module rather than authoring from scratch.** Verified
reference implementations in `@auditlogic/module-*` (all use `x-oauth-providers` + refresh). Note
the `$ref` scope: current modules use `@zerobias-org/types-core`; older ones (e.g. `slack`) use
`@auditmation/types-core` — same schemas, use `@zerobias-org/types-core` for new work:

| Module | Provider | Good example of |
|--------|----------|-----------------|
| `microsoft/azure/msgraph` | `microsoft.oauth` | **Entra/Azure AD** — reuse `microsoft.oauth` for any Entra-backed product; dual-mode (OAuth **or** manual clientId/secret/directoryId) |
| `atlassian/cloud/jira` | `atlassian.oauth` | explicit `connectionMode: [manual, oauth]` enum + oauth `basePath` rewrite |
| `slack/slack` | `slack.oauth` | minimal OAuth-only profile; `connect()` hard-requires `oauthConnectionDetails` |
| `github/github` | `github.oauth` | OAuth + PAT fallback |

**connectionProfile.yml** — extend BOTH `oauthTokenProfile` AND `oauthTokenState`, add the
provider hook, and use `x-ui-*` to control the connect form (this is what every real module does):

```yaml
# connectionProfile.yml — OAuth authorization-code (mirrors msgraph/jira/slack)
type: object
allOf:
  - $ref: './node_modules/@zerobias-org/types-core/schema/oauthTokenProfile.yml'
  - $ref: './node_modules/@zerobias-org/types-core/schema/oauthTokenState.yml'
  - type: object
    x-oauth-providers:
      - <vendor>.oauth          # e.g. microsoft.oauth for Entra/Azure AD-backed products
    x-ui-required:              # fields the connect form REQUIRES (manual-entry / OAuth-app creds)
      - clientId
      - clientSecret
    x-ui-hidden:               # HIDE the token-state fields the OAuth flow fills in for you
      - tokenType
      - accessToken
      - refreshToken
      - expiresIn
      - scope
      - url
    properties:
      clientId:
        type: string
      clientSecret:
        type: string
        format: password
```

> ⚠️ **`x-ui-*` = which fields the connect FORM shows.** Rule of thumb:
> - `x-ui-hidden`: the OAuth-flow fields the user should never type — always hide `tokenType`,
>   `refreshToken`, `expiresIn`, `scope`, `url`.
> - `x-ui-required`: the fields that ARE the manual connect method. This is a **real design choice**,
>   not fixed: `msgraph` requires the app creds (`clientId`/`clientSecret`/`directoryId`) and HIDES
>   `accessToken`; `slack` instead REQUIRES `accessToken` (it supports pasting a bot token) and hides
>   the rest. Pick per module: hide `accessToken` for pure click-to-connect; require it only if you
>   also support manual token paste. (The "Build-Time Resolution → The Pattern" example lower in
>   this file shows the require-`accessToken` variant — that's the slack-style choice, not a
>   contradiction.)

**connectionState.yml** — extend `oauthTokenState.yml` (accessToken + **refreshToken** +
`expiresIn` in SECONDS + scope). It MUST resolve to `baseConnectionState` (which `oauthTokenState`
already does) so the server schedules the refresh cronjob.

**`src/<Class>Impl.ts` — `connect()` / `refresh()`.** The OAuth app creds arrive at runtime as
a typed 2nd argument, `OauthConnectionDetails` (from `@zerobias-org/types-core-js`) — **never
hardcode or persist them**. Real signature (from msgraph/github):

```ts
import { OauthConnectionDetails } from '@zerobias-org/types-core-js';

async connect(
  connectionProfile: ConnectionProfile,
  oauthConnectionDetails?: OauthConnectionDetails,
): Promise<BaseConnectionState> { /* exchange code/refresh → accessToken */ }

async refresh(
  connectionProfile: ConnectionProfile,
  connectionState: BaseConnectionState,
  oauthConnectionDetails?: OauthConnectionDetails,
): Promise<BaseConnectionState> {
  // canonical: delegate to connect() with refresh=true
  return this.client.connect(connectionProfile, oauthConnectionDetails, true);
}
```

Gotchas the real modules encode:
- **Accept both casings.** The node→module boundary may deliver `clientId` OR `client_id`.
  msgraph reads `oauth?.clientId ?? oauth?.client_id` — a forced refresh silently lost creds
  until it handled both. Do the same for `clientSecret`/`client_secret`.
- **Dual-mode fallback.** OAuth is not strictly either/or with token auth. msgraph/jira accept
  the OAuth popup creds *or* fall back to `connectionProfile.clientId/clientSecret` for a manual
  client-credentials connection. Throw `InvalidCredentialsError` (or a specific message naming
  the missing field) only when neither path has what it needs.

#### 🚨 What the module does — and does NOT — do at runtime

The **platform's Global App** performs the authorization-code exchange (the popup, `code`,
`redirect_uri`) and hands your module an **already-minted `accessToken` + `refreshToken`** in the
connection state. So **do NOT implement a `code`→token exchange in the module** — that's a common
wasted effort. Your `connect()`/`refresh()` only:
- **`connect()` (normal OAuth):** just USE / validate the `accessToken` you were handed.
- **`refresh()`:** re-mint the token yourself — `POST` to the token endpoint with
  `grant_type: refresh_token`, `refresh_token` from the profile/state, and `client_id`/`client_secret`
  from `OauthConnectionDetails`. (Only the *manual* dual-mode fallback uses `grant_type: client_credentials`.)

#### 🚨 Where each URL / scope lives (non-obvious — get this right)

| Thing | Lives in | Example (msgraph) |
|-------|----------|-------------------|
| **Authorize** URL | the `oauth` provider `index.yml` (`url`) | `login.microsoftonline.com/…/oauth2/v2.0/authorize` |
| **Token** URL | **hardcoded constant in your client** — NOT the provider | `const BASE_TOKEN_URI + tenant + '/oauth2/v2.0/token'` |
| **Scopes** | **hardcoded constant in your client** (api.yml securityScheme only *documents* them) | `const MS_GRAPH_SCOPE` |
| `accessToken` / `refreshToken` | read them off **`connectionProfile`** at runtime (see note) | `this.connectionProfile.refreshToken` |

> **`connect()` has no `connectionState` argument — the tokens arrive on `connectionProfile`.**
> Because the profile `allOf`-includes `oauthTokenState`, `accessToken`/`refreshToken`/`expiresIn`
> are fields *on the profile object* the Hub hands you. Real modules read
> `this.connectionProfile.accessToken` / `.refreshToken` — do NOT look for a separate state param.
> (`refresh()` does receive a `connectionState` arg for metadata, but the refresh token still comes
> from the profile.)

The provider artifact carries **only** the authorize URL + a UUID. The **token endpoint and scopes
are yours to hardcode** in `connect()/refresh()` (they're universal per-provider constants — don't
put them in the profile or provider).

#### 🚨 Testing an OAuth module locally (there's no popup in a test run)

Every `connectionProfile` field is supplied as a **zbb secret whose name matches the field name**;
`describeModule<T>` injects them into the `ConnectionProfile` passed to `connect()` (non-secret test
params go via `zbb env set` → `test/e2e/constants.ts`). The catch: **there's no OAuth popup in
`testDirect`/`testDocker`**, so *something* has to supply a token. Two real paths:

- **Dual-mode / app-creds (easiest — what makes `msgraph` testable):** if the module also supports a
  manual `client_credentials` path, store `clientId`/`clientSecret`(+`directoryId`/tenant) as secrets;
  `connect()` mints its own `accessToken` — no popup, no pre-minted token needed.
  ```bash
  zbb secret create clientId     --module @zerobias-org/module-<v>-<p> --slot local
  zbb secret create clientSecret --module @zerobias-org/module-<v>-<p> --slot local
  ```
- **Pure click-to-connect only:** there's no way to mint a token locally — obtain a real
  `accessToken`/`refreshToken` **once, out-of-band** (Postman/curl against the provider) and store them
  as secrets so `connect()`/`refresh()` can run. Tests `this.skip()` gracefully when the values are
  absent, so CI stays green without them.

Reference e2e wiring: `msgraph`, `jira` (`test/e2e/` + `constants.ts`).

The `<vendor>.oauth` code refers to an **`OAuthProvider` resource** in the `zerobias-org/oauth`
repo. Reuse an existing provider when one fits (e.g. `microsoft` /
`login.microsoftonline.com/organizations/oauth2/v2.0/authorize` already exists — reuse it for
any Entra/Azure AD-backed product) rather than inventing a new one.

### The provider wiring — content-as-code YOU author + load (NOT insider)

`oauth` is a **loadable artifact type** (see `.claude/docs/dataloader-artifact-map.md`), just
like vendor/product/module. The provider lives in the **`zerobias-org/oauth`** repo as
`@zerobias-org/oauth-<vendor>` and its only manifest is `index.yml`:

```yaml
# zerobias-org/oauth · package/<vendor>/index.yml  (nest package/<vendor>/<suite>/ for a suite)
id: 9d975c18-45d4-4974-abcb-90aea1795c12          # stable UUID (repo-wide unique)
url: https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize   # public authorize URL
```

**No client_id, no secret — just the public authorize URL + a UUID.** The package's `package.json`
`zerobias` block deps on the vendor/suite/product package, which resolves the provider to a **VSP
by package-code convention**. The module references it via `x-oauth-providers: [<vendor>.oauth]`;
the two meet in `OAuthProvider` at dataload.

So the provider **and** the module→provider link are authored and loaded **exactly like any other
content** — you can even load them into your OWN org first (org-private) before PRing to the shared
catalog. **Reuse an existing provider when one fits** — already present:
`microsoft`, `github`, `atlassian`, `slack`, `zoho`, `google`. (e.g. reuse `oauth-microsoft` for
any Entra/Azure AD product; only add a new `oauth-<vendor>` package if none matches.)

#### 🚨 ALWAYS detect first — is the provider already in the repo?

**Whenever a module needs an authorization-code provider, check the `oauth` repo live — do NOT
trust the static list above (it drifts as providers are added).** Match your
vendor (and suite/product, if the provider is scoped):

```bash
gh api repos/zerobias-org/oauth/contents/package --jq '.[].name'          # top-level vendors
gh api repos/zerobias-org/oauth/git/trees/main:package?recursive=1 \
  --jq '.tree[] | select(.path|endswith("index.yml")) | .path'            # every provider (incl. nested suite/product)
```

Decision:
- **Provider exists** → reference it via `x-oauth-providers: [<code>]` and STOP. Nothing touches the oauth repo.
- **Provider MISSING** → you must **add it** — author the package with the recipe below and open a
  **separate content PR to `zerobias-org/oauth`** (contributor content, NOT the insider task).
  Flag this as an extra deliverable so it isn't forgotten; the module can't advertise OAuth until
  the provider is loaded.

#### Recipe: add a missing provider (a `zerobias-org/oauth` content PR)

> **Prerequisite:** the `dependencies` below reference `@zerobias-org/vendor-<vendor>` (or the
> suite/product package). That **catalog content must already exist** — if the vendor/product isn't
> in the catalog yet, create it FIRST via `/create-product`, then add the oauth provider. A provider
> whose vendor dep doesn't resolve won't load.

No scaffold script and **no gradle gate** — it's a 2-file Lerna package. Copy an existing
`package/<vendor>/` and change 4 things (generate the UUID with `uuidgen`):

```yaml
# package/<vendor>/index.yml
id: <fresh v4 UUID>                       # `uuidgen` — repo-wide unique, IMMUTABLE once published
url: https://<provider>/oauth2/authorize  # the AUTHORIZE endpoint (not the token endpoint)
```
```jsonc
// package/<vendor>/package.json  (only the load-bearing keys shown)
{
  "name": "@zerobias-org/oauth-<vendor>",
  "files": ["index.yml"],
  "scripts": { "nx:publish": "../../scripts/publish.sh" },
  "zerobias": {
    "package": "<vendor>.oauth",       // ← the code x-oauth-providers resolves against
    "import-artifact": "oauth",        // ← tells the dataloader the artifact type
    "dataloader-version": "<current>"  // copy from a sibling package's package.json
  },
  "dependencies": { "@zerobias-org/vendor-<vendor>": "latest" }  // ← binds to the VSP (must exist)
}
```
- **VSP scope** = whatever package you depend on: vendor-level → `@zerobias-org/vendor-<vendor>` +
  code `<vendor>.oauth`; suite/product-scoped → depend on that package + code
  `<vendor>.<suite>.<product>.oauth`, nested at `package/<vendor>/<suite>/…`.
- Publishes via Lerna to GitHub npm, then loads via the dataloader (`import-artifact: oauth`).
- **PR base is `main`** — the `zerobias-org/oauth` repo has no `dev` branch.

### The genuinely-insider half — external app + secret (a contributor CANNOT self-serve)

Only **two** things are NOT content-as-code, because they involve an external OAuth app and a
secret. **When OAuth authorization-code is chosen, tell the user to open a task for JUST these:**

```
Title: Register <vendor> OAuth app + Secrets Manager entry for click-to-connect

The <module-package> connector is OAuth-capable and its oauth provider artifact + connectionProfile
link are authored/loaded as content. Two insider steps remain before the "Connect" button works:
  1. Register (or confirm) the <vendor> OAuth app with the provider → obtain client_id +
     client_secret; allow-list ZeroBias's shared Global App redirect URI; grant scopes/admin-consent.
     (For a reused provider like Microsoft, the shared app may already exist.)
  2. Store client_id/client_secret in AWS Secrets Manager (dev + prod), keyed to the
     <vendor>.oauth OAuthProvider. Secrets cannot live in loadable content — this is the hard step.

Outcome: OAuth-enabled <vendor> connections show the click-to-Connect button in Hub.
```

> If the provider package doesn't exist yet, authoring it (`@zerobias-org/oauth-<vendor>`,
> `index.yml {id,url}`) is **your** job, not the insider's — it's a normal content PR to
> `zerobias-org/oauth`. The insider task is only the external app + the secret.

> OAuth **client-credentials** (Pattern 2) is different: it needs no click-to-connect popup
> and no provider link — the user supplies clientId/clientSecret directly. No insider task,
> fully contributor-self-serve. Extend `oauthClientProfile` (not `oauthTokenProfile`), and do
> NOT add `x-oauth-providers`.
> **Example (M2M / service account):** many products expose a *service account* (a Client ID +
> Client Secret from their admin console) exchanged via `client_credentials` at the product's own
> token endpoint — often an Auth0/Cognito-backed URL distinct from the vendor's user-SSO IdP. Don't
> assume the token IdP from who owns the product; verify the actual token endpoint. Such a module is
> Pattern 2 end-to-end — no insider task. The registration task is only for the
> **authorization_code** ("Connect" button) flow.

### Pattern 4: Custom Fields (Extend Core)

```yaml
# connectionProfile.yml - Add organizationId
allOf:
  - $ref: './node_modules/@zerobias-org/types-core/schema/tokenProfile.yml'
  - type: object
    required: [organizationId]
    properties:
      organizationId:
        type: string
        description: Organization identifier for API access

# connectionState.yml - Add extra state
allOf:
  - $ref: './node_modules/@zerobias-org/types-core/schema/tokenConnectionState.yml'
  - type: object
    properties:
      organizationName:
        type: string
        description: Cached organization name
```

## Connection Profile Scope

### What Belongs in connectionProfile

**ONLY connection parameters - minimal set needed to CONNECT**

```yaml
# ✅ GOOD - Connection parameters
- token / apiKey / clientId / clientSecret
- baseUrl (if API has multiple environments)
- organizationId (if required to authenticate)

# ❌ BAD - Operation parameters
- limit (pagination parameter)
- projectId (operation scope, not connection scope)
- fields (query parameter)
```

**Rule**: If you can connect WITHOUT it, it's an operation parameter (not profile)

### Check for Additional Optional Parameters

**Always review API docs for environment-specific optional parameters:**

```yaml
# Example: Service has optional region parameter
allOf:
  - $ref: './node_modules/@zerobias-org/types-core/schema/tokenProfile.yml'
  - type: object
    properties:
      region:
        type: string
        description: Optional region for multi-region deployments
        enum: [us-east-1, eu-west-1, ap-southeast-1]
    # region is optional, but include it if API docs mention it
```

**Don't omit parameters that some environments might need!**

## 🚨 CRITICAL: Check Parent Schema First

**Before adding ANY property, check what the parent schema provides:**

```bash
# Check what tokenProfile.yml provides
cat node_modules/@zerobias-org/types-core/schema/tokenProfile.yml

# Check what basicConnection.yml provides
cat node_modules/@zerobias-org/types-core/schema/basicConnection.yml

# Check what baseConnectionState.yml provides
cat node_modules/@zerobias-org/types-core/schema/baseConnectionState.yml
```

### Avoid Semantic Duplication

```yaml
# ❌ WRONG - basicConnection already has uri
allOf:
  - $ref: './node_modules/@zerobias-org/types-core/schema/basicConnection.yml'
  - type: object
    properties:
      url:    # Duplicate! basicConnection has uri
        type: string

# ✅ CORRECT - Use parent's uri, or extend if truly different
allOf:
  - $ref: './node_modules/@zerobias-org/types-core/schema/basicConnection.yml'
  # uri is already provided by basicConnection
```

**Semantic duplicates to avoid:**
- url / uri / baseUrl
- token / accessToken
- username / user / userName
- password / pass / pwd

## 🚨 CRITICAL: ALWAYS Check Product Documentation

**Before finalizing connectionProfile, check product docs for ALL auth parameters:**

```yaml
# Example: Missing mfaCode from product docs
allOf:
  - $ref: './node_modules/@zerobias-org/types-core/schema/basicConnection.yml'
  - type: object
    properties:
      mfaCode:    # Found in product docs!
        type: string
        description: Multi-factor authentication code (optional)
```

**Don't assume - verify:**
1. Read product documentation authentication section
2. Look for optional parameters (region, environment, mfaCode, etc.)
3. Include ALL mentioned parameters (even if optional)
4. Don't omit parameters some environments might need

## 🚨 CRITICAL: Connection Scope MUST NOT Limit Operations

**NEVER add organization/project/workspace IDs to connection:**

```yaml
# ❌ WRONG - Limits connection to single organization
connectionState:
  allOf:
    - $ref: './node_modules/@zerobias-org/types-core/schema/baseConnectionState.yml'
    - type: object
      properties:
        accessToken:
          type: string
        organizationId:    # NO! Limits scope
          type: string

# ✅ CORRECT - Connection works across all organizations
connectionState:
  allOf:
    - $ref: './node_modules/@zerobias-org/types-core/schema/baseConnectionState.yml'
    - type: object
      properties:
        accessToken:
          type: string
  # organizationId is operation parameter, NOT connection parameter
```

**WHY**: Connection should be reusable across all scopes. Use operation parameters for scope.

**Scope identifiers belong in operation parameters, NOT connection:**
- ❌ organizationId in connection
- ❌ workspaceId in connection
- ❌ projectId in connection
- ❌ teamId in connection
- ✅ These are operation parameters (use in API paths)

## 🚨 CRITICAL: Only Add Used Fields (for connectionState)

**For connectionState - don't add fields "just in case" - only add what's actually USED:**

```yaml
# ❌ WRONG - identityId not used anywhere
connectionState:
  properties:
    accessToken: string
    identityId: string    # Where is this used? Nowhere!

# ✅ CORRECT - Only fields that are actually used
connectionState:
  properties:
    accessToken: string
  # If connect() doesn't return identityId, don't add it
```

**Ask:**
1. Does connect() method return this field?
2. Do operations use this field?
3. Is it needed for refresh/reconnect?
If NO to all → don't add it

**For connectionProfile - include environment-optional fields:**

```yaml
# ✅ CORRECT - Include optional fields that some environments need
allOf:
  - $ref: './node_modules/@zerobias-org/types-core/schema/tokenProfile.yml'
  - type: object
    properties:
      region:
        type: string
        description: Optional region (needed in some deployments)
      mfaCode:
        type: string
        description: Multi-factor authentication code (optional)
    # These aren't required, but include them if product docs mention them
```

**connectionProfile vs connectionState:**
- **connectionProfile**: Include optional fields that might be needed in some environments (region, mfaCode, etc.)
- **connectionState**: Only fields actually used by connect() or operations

## Validation Checklist

Before finalizing connection schemas:

- [ ] **Checked parent schema** - no semantic duplicates (url/uri, token/accessToken)
- [ ] **Checked product docs thoroughly** - all auth parameters included (mfaCode, region, etc.)
- [ ] connectionProfile extends a core profile (NOT custom)
- [ ] connectionState extends baseConnectionState (includes expiresIn)
- [ ] expiresIn is in seconds (integer), not expiresAt timestamp
- [ ] If refresh capability: state extends oauthTokenState
- [ ] If simple token: state extends tokenConnectionState
- [ ] Custom fields use allOf to extend core
- [ ] All required fields marked as required
- [ ] Checked API docs for optional connection parameters (region, environment, etc.)
- [ ] Profile contains ONLY connection parameters (not operation parameters)
- [ ] **NO scope limitation** - no organizationId/projectId/workspaceId in connection
- [ ] **Only used fields** - every state field is actually used by connect() or operations
- [ ] Minimal set needed to connect (don't add operation scope parameters)

## 🚨 CRITICAL: Build-Time Schema Resolution

**ALWAYS use $ref in committed files - resolve at build time**

### Why Build-Time Resolution?

- **Clean source files**: `connectionProfile.yml` and `connectionState.yml` stay as `$refs` (single source of truth)
- **No duplicate maintenance**: Changes to core schemas automatically propagate
- **CI-friendly**: Resolution happens automatically during gradle's `:generate` task.

### The Pattern

**Committed files (source of truth):**
```yaml
# connectionProfile.yml - KEEP AS $REF
type: object
allOf:
  - $ref: './node_modules/@zerobias-org/types-core/schema/oauthTokenProfile.yml'
  - $ref: './node_modules/@zerobias-org/types-core/schema/oauthTokenState.yml'
  - type: object
    x-ui-required:
      - accessToken
    x-ui-hidden:
      - tokenType
      - refreshToken
    x-oauth-providers:
      - vendor.oauth

# connectionState.yml - KEEP AS $REF
$ref: './node_modules/@zerobias-org/types-core/schema/oauthTokenState.yml'
```

**Build-time resolution:**

Run `zbb generate` — it chains `syncMeta → assembleSpec → bundleSpec → generate*` automatically. `bundleSpec` natively inlines every `$ref` in `api.yml` + `connectionProfile.yml` (+ optional `connectionState.yml`); no manual `$ref` resolution step is needed.

```bash
zbb generate
```

### ❌ DON'T: Commit Resolved Files

```yaml
# ❌ WRONG - Committed resolved/flattened file
type: object
properties:
  tokenType:
    type: string
  accessToken:
    type: string
  # ... all properties inlined
```

**Problems:**
- Duplicate maintenance when core schemas change
- Merge conflicts
- Harder to see what's custom vs inherited

### ✅ DO: Commit $ref Files, Resolve at Build

```yaml
# ✅ CORRECT - Committed as $ref
$ref: './node_modules/@zerobias-org/types-core/schema/oauthTokenState.yml'
```

**Benefits:**
- Single source of truth
- Auto-inherits core schema updates
- Clear distinction between core and custom

## Common Mistakes

### ❌ Creating Custom Profile
```yaml
# DON'T DO THIS
type: object
properties:
  apiKey: string
  baseUrl: string
```
**Fix**: Extend tokenProfile.yml

### ❌ Missing baseConnectionState
```yaml
# DON'T DO THIS
type: object
properties:
  accessToken: string
```
**Fix**: Extend baseConnectionState or tokenConnectionState

### ❌ Using expiresAt Instead of expiresIn
```yaml
# DON'T DO THIS
expiresAt:
  type: string
  format: date-time
```
**Fix**: Convert to expiresIn (seconds) in connect() method

### ❌ No expiresIn for Refresh Tokens
```yaml
# DON'T DO THIS
properties:
  accessToken: string
  refreshToken: string
  # Missing expiresIn!
```
**Fix**: MUST extend baseConnectionState for expiresIn

## Remember

1. **Always extend core profiles** - Never create custom from scratch
2. **Always extend baseConnectionState** - Server needs expiresIn for cronjobs
3. **expiresIn in seconds** - Not timestamps, not milliseconds
4. **Use allOf for extensions** - Add custom fields via composition
5. **Receive data from @credential-manager** - Don't guess auth method

---

**Connection schemas are YAML schemas - design them like api.yml schemas!**
