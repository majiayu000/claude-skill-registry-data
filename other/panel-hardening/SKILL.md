---
name: panel-hardening
description: Audit and harden a 3x-ui panel — scoped API tokens instead of admin passwords, credential rotation, fail2ban and per-client IP limits, certificate pinning, update channel, backups. Use when asked to secure or audit a panel, rotate credentials, review who can reach the API, or set up backups before a risky change.
---

# Hardening a 3x-ui panel

Read the current state first, change one thing at a time, and know which steps cut
your own connection to the panel. Several of these need panel **v3.5.0+** (tokens,
certificate helpers) or **v3.7.0+** (token scopes, `get_factory_defaults`).

## 1. Audit what exists

```
get_settings
list_api_tokens
get_fail2ban_status
get_panel_update_info
```

`get_settings` shows the listening port, base path, TLS certificate paths and the
subscription settings. A panel on the default port with an empty base path is
found by internet-wide scanners within hours; both are worth changing, and both
are set in the panel UI rather than through the API.

If you change the base path, this MCP server's `XUI_BASE_PATH` must change with it
or every subsequent call 404s.

## 2. Move this server off the admin password

A username and password grant everything and cannot be revoked without changing
the admin's own credentials. A scoped token can be disabled in one call.

```
create_api_token name="mcp-server" scope="admin" expires_at=0
```

The plaintext appears in that response **and nowhere else** — the panel stores a
SHA-256 hash. Capture it, put it in `XUI_API_TOKEN`, drop `XUI_USERNAME` and
`XUI_PASSWORD`, restart the server.

Scope `admin` is what this server needs: `monitor` reaches only status and metrics
routes (of the tools here, just `server_status` and `get_xray_versions`), and
`node-sync` is a fixed panel-to-node allowlist. Set `expires_at` (Unix ms) when the
token is for a contractor or a one-off task; leave 0 for the server's own token,
since an expiry it cannot renew is an outage waiting to happen.

Note for the CLI: `x-ui setting -getApiToken` now *rotates* a single shared
`cli-fallback` token rather than minting a new one, so running it again silently
invalidates a token someone is already using. Mint tokens through the API instead.

## 3. Prune the tokens that exist

`list_api_tokens` gives id, scope, expiry and enabled state — never values. For
anything unrecognised, disable before deleting; disabling is reversible and tells
you immediately what breaks:

```
set_api_token_enabled id=<id> enabled=false scope="<its stored scope>"
delete_api_token id=<id> scope="<its stored scope>"
```

Both require the token's stored `scope` and the panel fails closed on a mismatch,
so read it from `list_api_tokens` rather than guessing.

## 4. Rotate the admin credentials

```
update_admin_credentials old_username=… old_password=… new_username=… new_password=…
```

This invalidates the credentials this MCP server is authenticating with. Either
switch to a token first (step 2) and be unaffected, or update `XUI_USERNAME` /
`XUI_PASSWORD` and restart the server immediately afterwards. Rotating credentials
without doing one of the two leaves you locked out of your own automation.

## 5. Per-client limits and fail2ban

`get_fail2ban_status` reports whether the host can actually enforce bans, and this
is not a formality: without fail2ban installed the panel **records** IP usage but
enforces nothing. The job says so once per run and nowhere the user will look —
*"[LimitIP] Fail2Ban is not installed, Please install Fail2Ban from the x-ui bash
menu."* So a panel full of carefully set `limitIp` values can be enforcing none of
them, and it looks identical to one that is working.

With fail2ban present, `limitIp` becomes a real control: exceeding it bans the
source address rather than merely refusing the connection.

`get_client_ips_table` is the aggregated view behind those limits — the fastest way
to spot one credential in use from a dozen addresses. `clear_client_ips` resets a
single client's record after a legitimate change of network.

## 6. Certificates

```
get_web_cert_files
get_cert_hash cert_file="/path/from/get_web_cert_files"
```

The hash is what clients and nodes pin against, so record it before any renewal
and re-read it after. `get_remote_cert_hash server="host:443"` does the same for a
server you are about to pin from the outside — that is also how you verify a node's
identity before trusting it (see the `multi-node` skill).

## 7. Updates

```
get_panel_update_info
get_panel_update_status
set_update_channel dev=false
update_panel
```

Keep the stable channel unless you are deliberately testing. `update_panel`
restarts the panel: the call may not return cleanly, and this server's session
drops with it. Back up first (step 8), and re-check with `get_panel_update_status`
once it is back rather than assuming the update failed because the call errored.

`update_geofile` refreshes GeoIP/GeoSite data. Stale geo files quietly break
routing rules long before anyone connects the two.

## 8. Backups

```
test_telegram_bot
backup_to_telegram
```

Test the bot first — `backup_to_telegram` reports success on a bot that is
configured but cannot reach the chat. Take a backup before updates, before
template rewrites, and before any bulk client operation.

`export_clients` is the other half: it round-trips through `import_clients`, but it
carries every UUID and password, so keep it behind the resource link (the default)
rather than pasting it into a chat, and treat the export as a credential file.

## 9. Client hygiene

`delete_depleted_clients` and `delete_orphan_clients` are both **destructive and
panel-wide**. Enumerate first — `list_clients_paged` with a filter for what you are
about to remove — show the list, then delete. There is no undo and no confirmation
step inside the panel.
