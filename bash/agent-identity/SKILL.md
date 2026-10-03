---
name: agent-identity
description: Authenticate an AI agent with an auth server using the Agent Identity (AID) protocol, with Ed25519 identity documents, proof of possession, OAuth 2.0 token exchange and scoped JWTs. Use when an agent must sign in to an AID-enabled server, get or refresh an access token, or prove its identity to an API. Self-contained; works without other protocols.
license: MIT
compatibility: Requires curl, jq, openssl (3.x for Ed25519), and base64 CLI tools. macOS and Linux supported.
metadata:
  version: "0.4.0"
  homepage: "https://agentids.org"
  repository: "https://github.com/agentmessaging/agent-identity"
---

# Agent Identity (AID)

AID lets an agent sign in to an auth server with its own Ed25519 key instead of a shared secret. The agent registers its public key once; after that, each token request is a signed proof of possession exchanged for a short-lived JWT scoped to the agent's role. The `aid-*.sh` scripts handle keys, signing, discovery and caching. AID shares `~/.agent-messaging/agents/` with AMP when both are installed, so one identity serves both; neither needs the other.

## Flow

```bash
aid-init.sh --auto                                   # 1. once: create the keypair and identity

aid-request.sh --auth https://auth.example.com/acme  # 2a. ask for access; an admin approves it
aid-request.sh --auth https://auth.example.com/acme --poll   #     check whether it was approved
# or
aid-register.sh --auth https://auth.example.com/acme --token <ADMIN_JWT> --role-id 2   # 2b. admin registers directly

TOKEN=$(aid-token.sh --auth https://auth.example.com/acme --quiet)   # 3. get a token
curl -H "Authorization: Bearer $TOKEN" https://api.example.com/resource
```

Use `aid-request.sh` unless the user has given you an admin JWT. If you only know the API's URL, pass `--resource <api-url>` instead of `--auth` to `aid-request.sh` or `aid-token.sh`, and the auth server is discovered (RFC 9728, then RFC 8414).

## Commands

```bash
aid-init.sh --auto | --name <name> [--force]          # --force overwrites the existing identity
aid-discover.sh --resource <api-url> [--json | --quiet]   # --quiet prints only the auth server URL
aid-request.sh --auth <url> | --resource <api-url> [--name <display>] [--description "<why>"] [--api-key <k>] [--poll]
aid-register.sh --auth <url> --token <admin-jwt> --role-id <id> [--name <display>] [--description "<text>"] [--lifetime <seconds>] [--api-key <k>]
aid-token.sh --auth <url> | --resource <api-url> [--scope "a:read b:write"] [--credential-type access_token|api_key] [--quiet | --json] [--no-cache] [--api-key <k>]
aid-status.sh [--json]                                # identity, registrations, cached tokens
```

`aid-token.sh` reuses a cached token until a minute before it expires, so call it whenever you need a token instead of storing one; `--no-cache` forces a new one. `--scope` can only narrow what the agent's role allows. `--api-key` sends an `X-Api-Key` header for servers that require one. `--credential-type api_key` asks for an opaque API key instead of a JWT.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Agent identity not initialized" | `aid-init.sh --auto` |
| "Not registered" | `aid-request.sh` (or `aid-register.sh` with an admin JWT) |
| "Registration pending" | Wait for the admin; check with `aid-request.sh --auth <url> --poll` |
| "Proof expired" | System clock is more than 5 minutes off; sync it |
| "Invalid signature" | The local identity may be corrupt: re-init and re-register |
| "Fingerprint mismatch" | The key changed since registration: re-register |
| "Scope not allowed" | Request only scopes the role grants |
| "Agent suspended" or 403 on token exchange | An admin suspended the agent; `aid-status.sh` shows it, and only the admin can reactivate |

The identity document, proof format, token exchange request, server-side lifecycle states and introspection are described in [references/protocol.md](references/protocol.md). Installation: `npx skills add agentmessaging/agent-identity`, or run `install.sh` from the repository to put the scripts in `~/.local/bin`. Specification: https://agentids.org
