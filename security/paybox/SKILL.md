---
name: paybox
description: MoonPay PayBox payment vault for AI agents — official MCP at https://api.paybox.sh/mcp, OAuth 2.1, scoped credentials, and Cheshire mcp-server proxy tools (get_paybox_*).
---

# PayBox

**Live catalog:** https://cheshireterminal.ai/skills/paybox  
**API:** https://cheshireterminal.ai/api/skills/paybox

[PayBox](https://paybox.sh/) is MoonPay's non-custodial **credential vault for agents**. Agents never receive raw card PANs, wallet private keys, or seed phrases — only scoped outputs (payment tokens, signatures, secrets under grant rules).

Official docs: https://docs.paybox.sh

## Official MCP connector (preferred)

```text
https://api.paybox.sh/mcp
```

Streamable HTTP MCP with **OAuth 2.1 + PKCE**. Add as a custom connector (Claude, Grok, Cursor, ChatGPT Developer mode), sign in, and approve a scoped grant.

### ChatGPT

1. Settings → Developer mode (web)
2. Plugins → New Plugin → Server URL
3. Paste `https://api.paybox.sh/mcp`
4. Authentication: **OAuth** (not No Auth)
5. Connect and complete sign-in

### Claude Code / Codex / Cursor

```bash
claude mcp add paybox --transport http https://api.paybox.sh/mcp
# or
codex mcp add paybox --url https://api.paybox.sh/mcp
```

### OAuth discovery (no auth)

```text
GET https://api.paybox.sh/.well-known/oauth-protected-resource
GET https://api.paybox.sh/.well-known/oauth-authorization-server
GET https://api.paybox.sh/health   → {"ok":true}
```

Scopes: `mcp`, optional `offline_access` (refresh token).

## Core official tools (after OAuth)

Discover at runtime via `tools/list`. Documented core surface includes:

- `list_credentials` — granted wallets / cards / secrets
- `request_payment` / `claim_payment_credentials` — one-time virtual cards
- `request_wallet_sign` / `request_swap` / `get_portfolio`
- `get_buy_link` — signed MoonPay fiat checkout into a wallet credential
- `discover_services` / `pay_x402` / `use_service` — x402 paid APIs
- `get_request` / `list_requests` — poll pending approvals
- `request_account_change` — ask user to widen grants
- Plugin tools (when enabled in the PayBox app)

Write tools return a status envelope (`success`, `pending_approval`, `pending_signature`, …). **Never re-call a write tool to finish it** — poll `get_request` with `request_id`.

## Cheshire mcp-server proxy

Monorepo package `mcp-server/` proxies PayBox without rehosting:

| Tool | Notes |
|------|--------|
| `get_paybox_connect` | Official URL, platforms, concepts |
| `set_paybox_session` | Store OAuth access token (masked in responses) |
| `clear_paybox_session` | Drop session token |
| `get_paybox_health` | Live API health (no auth) |
| `get_paybox_oauth_metadata` | Discovery docs |
| `list_paybox_mcp_tools` | Official `tools/list` |
| `call_paybox_mcp_tool` | Official `tools/call`; mutating tools need `confirm=true` |

Host env (optional single-tenant): `PAYBOX_ACCESS_TOKEN` or `PAYBOX_BEARER`.

**Do not** paste Cheshire `MCP_HTTP_AUTH_TOKEN` as a PayBox OAuth JWT.

## Security rules

- One agent client per agent; revoke from the PayBox dashboard / kill switch.
- Start with narrow grants (one wallet, low spend, always-approve).
- Secrets returned raw only when explicitly granted — prefer mediated tokens when available.
- PayBox does not custody spend rails: money moves wallet↔merchant; PayBox is the control plane.

## Related

- `moonpay` — pack entry + REST tools
- `moonpay-auth` / `moonpay-mcp` / `moonpay-x402` / `moonpay-buy-crypto`
- `moonpay-skills-index`
