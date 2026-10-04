---
name: mint-and-revoke-tokens
description: Mint, list, or revoke bearer tokens (owner or friend access tokens) for the API, MCP, app, and CI with just mint-token / list-tokens / revoke-token.
---
# Mint and revoke tokens

Wandering OS has no login provider: access is a self-minted bearer-token scheme.
A token is 32 random bytes (base64url); the server stores only its SHA-256 hash
in a JSON array in the SSM parameter `/wos/tokens`. Owner tokens are the only
write credential; friend tokens are the trusted read tier.

## Read first
- docs/SECURITY_IAM.md — §2 "The bearer-token system, end to end" (mint/verify/revoke, roles, where tokens are typed in).
- tools/README.md — "mint-token, list-tokens, revoke-token" section for flag semantics.

## Commands
Needs AWS credentials for account 458443189947 (profile `wandering_os`).
```bash
just mint-token --role owner|friend --label <name> [--ttl 30d | --expires <iso>] [--dry-run]
just list-tokens [--json]
just revoke-token --label <name>        # exact label
just revoke-token --hash <prefix>       # hash prefix, e.g. 9f86d081
```
After minting the CI owner token: `gh secret set WOS_OWNER_TOKEN` (paste the raw token).

## Gotchas
- The raw token prints exactly once and is never stored — save it immediately; if lost, mint a new one.
- Revocation lags up to 5 minutes: every reader caches the allowlist per container.
- `revoke-token` refuses to remove the last remaining owner entry (would lock out phone, browser, CI, and bot at once) unless you pass `--force`.
- `--ttl` and `--expires` are mutually exclusive; expiry fails closed (a malformed `expiresAt` counts as expired).
- The bot's own owner token is not minted this way — use `just bootstrap-responder-token`, which pipes it straight into Secrets Manager and redeploys WosBotStack.
