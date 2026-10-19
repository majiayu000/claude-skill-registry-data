---
name: ovstorage-user-authenticate-to-backend
description: Use when configuring credentials or driving interactive authentication for a direct ovstorage backend connection.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, authentication, credentials]
tools: [Read]
compatibility: Requires ovstorage MCP tools or equivalent library calls. Backend credentials, browser/device auth, network access, and service URLs are user-supplied when needed.
---

# Authenticate to a Backend

## Goal

Create or refresh credentials for a backend connection without leaking secrets
into logs, route metadata, or tool output.

## When to use this

Use this when adding a new direct-mode connection (`file`, `http`,
`omniverse-storage-service`, `s3`, `gcs`, `azure`, `huggingface`,
`opendal`, or any
other backend kind), or when an existing connection reports
`AuthRequired`, `CredentialExpired`, or an inactive `auth_state_kind`
in `ovstorage_doctor`.

## Recipe

1. Inspect the configured backend layers and connections with
   [`ovstorage-user-getting-started`](../ovstorage-user-getting-started/SKILL.md).
2. Read the backend descriptor and credential schema before prompting for
   anything secret. Stack callers get this from the root Layer's
   `list_kinds`; CLI users can use the `connect` wizard.
3. For `file`, no external credential is normally required. Register the root
   path and keep credentials empty.
4. For `http`, prefer public URLs where they exist. If an HTTP route needs
   credentials, pass them through the connection credential schema —
   `bearer_token`, `username` + `password`, `signed_query`, or
   `secret_headers` — never through the address string; a query in `root_url`
   or `prefix` is rejected as `InvalidArgument` at `instantiate`.
5. If `authenticate_connection` returns an auth event stream, surface
   `OpenBrowser`, `DeviceCode`, `Progress`, `Succeeded`, `Failed`, and
   `Cancelled` events to the user exactly as events, then stop on a terminal
   event.
6. If it returns `Unsupported`, no flow ran and the connection's state is
   unchanged, so keep the registration and report the state rather than
   treating it as a failure. Backends that always answer this way: `s3`,
   `gcs`, `azure`, `huggingface`, `opendal`; broker connections on a direct endpoint (any
   address that is not `http(s)://`); and `file` and `http`, which have no
   connection-auth driver at all. `Unsupported` can also come from a layer
   that does not implement the call — a credentialless visibility-override row,
   or a remote service that has not implemented the RPC — so read it as "no flow
   was offered here", not as a statement about the backend kind. Where a
   credential is what is missing, supply one the origin accepts; re-running
   the flow is not the fix.

## Backend-specific auth

### `omniverse-storage-service`

The `omniverse-storage-service` backend authenticates over OIDC when its
`address` names a discovery root. The plugin reads `/api/v1/auth-config`
from that root to learn the OIDC issuer and client; the standard OIDC discovery doc supplies the
auth / token / device endpoints.

Two interactive flows:

- **Browser** (`InteractiveAuthCapability::Browser`): PKCE with a
  loopback redirect. The plugin opens the user's browser to the
  authorization endpoint, captures the code at a transient localhost
  callback, and exchanges it for the token bundle.
- **Headless** (`InteractiveAuthCapability::Headless`): RFC 8628
  device flow. The plugin requests a device code, surfaces a
  user-code + verification URL via `AuthEvent`, and polls the token
  endpoint until the user completes the flow on a separate device.

In both cases the resulting `OAuthToken` lands as the connection's
`oauth` credential bundle. The plugin proactively refreshes the access
token in a background task at ~90% of the token's TTL using the
refresh-token grant (or the client-credentials grant if that's the
configured method). No intervention required for long-running processes.

To pre-seed credentials (e.g. for CI), populate `oauth` with a long-lived
refresh token; the plugin will exchange it for an access token on first
use.

When `address` names a `grpc://` or `grpcs://` endpoint instead, there is
no discovery root and therefore no OIDC configuration: no sign-in flow,
no client-credentials grant, and no background refresh. Such a connection
takes an access token the host already holds — put it in the `oauth`
field with no refresh token — and the host rotates it by calling
`update_connection_credentials` again with a fresh one. An empty bundle
removes it.

### `s3`

The descriptor exposes three credential methods:

- `static_key` — long-lived IAM user key. Populate
  `aws_access_key_id` + `aws_secret_access_key`.
- `session` — short-lived STS / SSO credentials. Populate
  `aws_access_key_id` + `aws_secret_access_key` +
  `aws_session_token`.
- `aws_credentials_file` — read from an INI section. Populate
  `file_path` (defaults to `~/.aws/credentials`) and `profile`
  (defaults to `default`); the per-connection `profile` config key
  picks the section.

Each credential field's descriptor default is the matching `${AWS_*}`
env-var placeholder (e.g. `${AWS_ACCESS_KEY_ID}`); the host's
bundle-resolution layer expands these before the bundle reaches the
plugin. From the plugin's point of view the resolution chain is
bundle fields → env vars (via placeholder expansion) → shared
credentials file. IMDS, AWS SSO, web-identity tokens, and STS role
assumption are not implemented in-process; operators that need them
run their session helper (`aws sso login`, etc.) to materialise a
static-key profile.

### `gcs`

The descriptor exposes two credential methods:

- `service_account_key` — paste an ADC JSON blob into the
  `service_account_key` field. The plugin auto-detects the JSON
  `type`: `service_account` triggers JWT-bearer exchange (and is
  the only path that can mint V4-signed read URLs);
  `authorized_user` triggers an OAuth2 refresh-token exchange;
  `external_account` runs the workload-identity STS exchange (the
  subject token is re-fetched from its `file` or `url` source on
  every exchange, with an optional impersonation hop; token and
  impersonation endpoints must be https `*.googleapis.com` or
  loopback, the subject-token url https or loopback, and
  workforce-pool configs are rejected);
  `impersonated_service_account` mints its source credential's
  bearer and spends it on `generateAccessToken`. Every type except
  `service_account` reads through the plugin (`alt=media`) because
  only an RSA private key can V4-sign.
- `gcloud_adc_file` — populate `file_path` with the path to an
  ADC JSON file of any of those four types — e.g. written by
  `gcloud auth application-default login` (optionally with
  `--impersonate-service-account`) or by
  `gcloud iam workload-identity-pools create-cred-config`
  (defaults to `~/.config/gcloud/application_default_credentials.json`,
  with `~` expanded against `HOME` / `USERPROFILE` + `HOMEDRIVE`).

The plugin does **not** consult `GOOGLE_APPLICATION_CREDENTIALS` or
any other env var; if you need env-var expansion, do it in the host's
bundle-resolution layer before handing the bundle to the plugin.
GCE/GKE metadata-server identity and the AWS / `executable`
`external_account` source flavors are not implemented in-process.

### `http`

The descriptor exposes four credential methods. Distinct channels combine —
for example, a connection may hold a signed query and secret headers at once —
and a connection with none of them is anonymous:

- `bearer` — opaque token sent as `Authorization: Bearer <token>`
  on every request. Populate `bearer_token`.
- `basic` — HTTP Basic authentication. Populate both `username` and
  `password`; either value may be empty, but not both.
- `signed_query` — pre-issued query string appended verbatim to every
  request URL (leading `?` optional). Populate `signed_query`, and set
  the `signed_query_scope` **config** key to declare the token's scope
  family.
- `secret_headers` — credential-bearing headers in wire form, one
  `Name: Value` per line, sent with every request. Populate
  `secret_headers`. The separator is a line break, not a comma, so a
  value may contain commas. This is the secret-bearing counterpart to
  the `default_headers` config key, which rejects `Authorization`,
  `Cookie`, and `Proxy-Authorization`; those names are accepted here,
  while `Host`, `Range`, `If-Match`, and the framing and hop-by-hop
  headers are refused.

A signature is a credential with a declared scope, not part of the
address. Writing a query into `root_url` or `prefix` returns
`InvalidArgument` at `instantiate`: the object key is appended after the
route prefix, and a signature buried in config can be neither scoped nor
rotated. `signed_query_scope` accepts `prefix` (the token authorizes
everything under `root_url` — an Azure account, container, or directory
SAS, a CloudFront signed URL with a custom policy) or `object` (a
per-object presign, which a connection cannot hold and which returns
`Unsupported`; dispatch such a URL as a per-request address). The plugin
also refuses a token whose parameters name a per-object signature —
`X-Amz-Signature`, `sr=b`, a CloudFront canned policy — while
`signed_query_scope` says `prefix`. Supplying `signed_query` with no
scope, or a scope with no `signed_query`, is `InvalidArgument`; so is
setting Basic or Bearer credentials together with a `secret_headers` entry
named `Authorization`. Userinfo in `root_url` is the legacy Basic channel and
likewise conflicts with another `Authorization` writer, while it may coexist
with a signed query or non-Authorization secret header.

All channels are hot-swappable through
`update_connection_credentials` while the connection is live, but the
rotation may not change the connection's exact shape: the Authorization
method, presence of a signed query, and secret-header names and multiplicity
must remain fixed. Remove and re-add the connection to change that shape.
`signed_query_scope` is configuration rather than a credential, so rotating
into a signed query without that key (or supplying the key with no token) is
`InvalidArgument`. A replacement is probed before the atomic swap; reads keep
using the old snapshot while the probe runs. Credentials over a plaintext
`http://` route are refused except on loopback, and any secret-bearing
connection refuses an `https://` to `http://` redirect downgrade.

### `azure`

The descriptor exposes four distinct credential methods. The plugin
resolves them in this order:

- `account_key` — Shared Key signing. Populate `account_key`.
- `sas_token` — pre-issued shared-access signature appended verbatim
  to request URLs. Populate `sas_token`.
- `workload_identity` — Entra OAuth2 federated workload identity.
  Populate `federated_token_file` + `client_id` + `tenant_id`.
- `service_principal` — Entra OAuth2 client-credentials. Populate
  `client_id` + `client_secret` + `tenant_id`.

Each credential field's descriptor default is the matching
`${AZURE_*}` env-var placeholder
(`${AZURE_STORAGE_ACCOUNT_KEY}`, `${AZURE_STORAGE_SAS_TOKEN}`,
`${AZURE_TENANT_ID}`, `${AZURE_CLIENT_ID}`, `${AZURE_CLIENT_SECRET}`,
`${AZURE_FEDERATED_TOKEN_FILE}`); the host's bundle-resolution layer
expands these before the bundle reaches the plugin. The plugin
itself never reads `AZURE_*` env vars at runtime. Managed Identity
(IMDS), `az login`, VS Code, and PowerShell credential sources from
`DefaultAzureCredential` are not implemented in-process.

### `huggingface`

A single static access token in the `token` field (`hf_…`; a
read-scoped token is sufficient). The descriptor default is
`${HF_TOKEN}`, resolved by the host at TOML load — the plugin never
reads the environment itself. An empty bundle connects anonymously,
which serves public repositories; private and gated repositories
answer 404/403 without a token. The token is verified once at add
time with a lenient `whoami` check (only a definitive 401 parks the
connection); rotation goes through `update_connection_credentials`,
and `reauth` answers `Unsupported` because no interactive flow
exists.

### `opendal`

Auth depends on the chosen `service` (one of `fs`, `s3`, `webdav` —
the only services compiled in). `fs` requires no credentials.
The OpenDAL `s3` driver wants `access_key_id` + `secret_access_key`
(**bare names**, not `aws_*`-prefixed — these are NOT
interchangeable with the first-party `s3` plugin's credential
shape). `webdav` uses HTTP Basic credentials (`password`, plus
`username` passed through `config_json`). The adapter accepts only
`SecretValue::Bytes`, `SecretValue::OAuthToken`, and
`SecretValue::File` for these fields; `SecretValue::SystemIdentity`
and `SecretValue::MtlsCertPair` are rejected as `Unsupported`.
Ambient-identity flows (Kerberos ticket cache, etc.) are not
threaded through. See
[`plugin-opendal.md`](../../docs/public/plugin-storage/plugin-opendal.md)
for per-driver detail.

### `nucleus`

Omniverse Nucleus's auth shape predates the unified OAuth pattern
used by the Omniverse Storage Service and the cloud backends.
The descriptor exposes three user-selectable credential methods:

- **`sso`** — single sign-on (browser). Recommended. Binds no
  credential fields. The plugin (`establish_interactive_auth`)
  calls `Tokens::subscribe` to register a one-shot login intent,
  receives a server-generated `nonce`, and surfaces
  `AuthEvent::OpenBrowser` with the Nucleus login URL annotated
  with `?nonce=<nonce>`. The host UI opens the URL; once the user
  completes the form, the second response on the same subscription
  carries the authentication result. The plugin never touches raw
  passwords or 2FA challenges on this path.
- **`userpass`** — username and password. Binds `username` and
  `password`; drives Nucleus's `Credentials::auth` flow. For
  service accounts and headless deployments.
- **`api_token`** — API token. Binds a single `api_token`
  credential. Drives `Tokens::auth_with_api_token`; takes
  precedence over `username` / `password`. The `Auth` envelope's
  `username` is recorded as the authenticated principal. The
  recommended automation path.

Successful authentication via `sso` produces a refresh token that
the plugin persists in the OS keyring keyed by the *server
hostname* (not the host-minted, unstable `ConnectionId`). On
subsequent connects, warm-continuation reads `refresh_token` from
the keyring, rediscovers `tokens_url`, and exchanges the refresh
token without re-prompting; on a service-call `Expired` /
`InvalidToken`, the plugin invokes `Tokens::refresh` once per
token-generation epoch (concurrent callers share a single refresh
under a per-shared mutex). `AuthRequired` / `AuthExpired` /
`PermissionDenied` clear the keyring entry; `Transient` preserves
it for retry. SSO (`SSO::*`) and DeviceFlow (`DeviceFlow::*`) are
declared as target / deferred flows; they are not wired today.

### `broker`

The `broker` plugin authenticates to an upstream `ovstorage-broker`
daemon; the broker itself holds the long-lived cloud credentials and
runs its own authn substrate against whatever listener-authn mode
operators configured. From the calling host's perspective the
client-side credential surface is intentionally minimal:

- **`client_credentials`** — OIDC client credentials grant. Binds
  `client_id` + `client_secret`. Only valid when the configured
  `address` is a discovery URL (not a direct gRPC endpoint): the
  plugin fetches `/api/v1/auth-config`, follows the published
  `openid_configuration` URL to the IdP's standard OIDC discovery
  doc, and drives a non-interactive client-credentials grant. Suited
  for service accounts and headless deployments.

Interactive flows (PKCE loopback for `Browser`, RFC 8628 device flow
for `Headless`) are driven by `Factory::authenticate` against the
same broker-published `auth-config`. The host signals which mode is
available through the gRPC `x-ov-iauth: browser|headless|none`
metadata header attached by the broker-client SDK on every RPC; the
broker reads this on its streaming `Auth` RPC, threads the parsed
`InteractiveAuthCapability` into the upstream-OAuth flow, and emits
`AuthEvent::OpenBrowser` / `DeviceCode` / `Progress` / `Succeeded`
back to the host. `None` mode causes the broker to emit a terminal
`Failed { AuthRequired }` envelope without opening a browser tab or
device prompt — the fail-fast shape render workers and CI hosts
need.

**Three-tier OAuth, broker-held.** Successful interactive auth lands
a refresh token *on the broker* via the unary `RegisterCredential`
round-trip; the broker persists it through its `OAuthCredentialProvider`
+ `secret_tokens` row + `SecretStore` (per-`(BackendId, PrincipalView)`
slot). The host process holds only the short-lived broker bearer —
never the upstream cloud credentials. Workers and a coordinator that
share a `PrincipalView` at the broker hit the same cache slot, which
covers the multi-tenant SaaS and render-worker shapes without any
host-side coordination.

The broker daemon's listener authn mode (`jwt_verify`,
`trusted_unsigned_jwt`, `trusted_forwarded_headers`, `peer_cred`, or
the reserved `mtls`) decides how the host's bearer is validated —
that's operator-owned config and is not part of the
`broker-client`-side credential schema. See
[`docs/public/broker-operator/README.md`](../../docs/public/broker-operator/README.md)
for the daemon side.

## References

- [`docs/public/library-rust/README.md`](../../docs/public/library-rust/README.md) for
  `add_connection`, credential persistence, and `authenticate_connection`.
- [`plugin-file`](../../docs/public/plugin-storage/plugin-file.md)
  for local filesystem configuration.
- [`plugin-http`](../../docs/public/plugin-storage/plugin-http.md)
  for HTTP route behavior.
- [`plugin-services-client`](../../docs/public/plugin-storage/plugin-services-client.md)
  for the `omniverse-storage-service` OIDC flow.
- [`plugin-nucleus`](../../docs/public/plugin-storage/plugin-nucleus.md)
  for the Omniverse Nucleus auth flows.
- [`plugin-broker`](../../docs/public/plugin-storage/plugin-broker.md)
  for the broker-client Layer surface, discovery URL normalization,
  and the broker-held three-tier OAuth model.
- [`docs/public/broker-operator/README.md`](../../docs/public/broker-operator/README.md)
  for the daemon-side listener authn modes a broker operator
  configures.
- [`ovstorage-user-handle-errors`](../ovstorage-user-handle-errors/SKILL.md) for interpreting
  auth and permission failures.
