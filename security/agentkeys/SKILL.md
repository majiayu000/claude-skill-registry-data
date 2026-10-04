---
name: agentkeys
description: Secure credential proxy for AI agents. Make API calls through AgentKeys — real secrets never leave the vault.
metadata:
  openclaw:
    requires:
      env:
        - AGENTKEYS_PROXY_URL
    credentials:
      - name: AGENTKEYS_API_KEY
        description: "Workspace API key (starts with ak_ws_). Use with X-Credential-Name header to proxy by credential name."
        required: false
      - name: AGENTKEYS_PROXY_TOKEN
        description: "Direct proxy token for a single credential (starts with pxr_). Simpler but limited to one credential."
        required: false
---

# AgentKeys Skill

Secure credential proxy for AI agents. Route API calls through AgentKeys so your agent never sees real secrets.

## Configuration

You have two options. Set these in your environment or `.env`:

### Option A — API Key (recommended, multi-credential)

```
AGENTKEYS_API_KEY=ak_ws_...
AGENTKEYS_PROXY_URL=https://proxy.agentkeys.io
```

Use your workspace API key to proxy requests to any credential by name. Get your API key from [Settings](https://app.agentkeys.io/dashboard/settings).

### Option B — Direct Proxy Token (single credential)

```
AGENTKEYS_PROXY_TOKEN=pxr_...
AGENTKEYS_PROXY_URL=https://proxy.agentkeys.io
```

Use a proxy token for one specific credential. Get it by assigning a credential to an agent in the [dashboard](https://app.agentkeys.io).

## Usage

### With API Key (Option A) — reference credentials by name

```bash
curl -X POST $AGENTKEYS_PROXY_URL/v1/proxy \
  -H "Authorization: Bearer $AGENTKEYS_API_KEY" \
  -H "X-Credential-Name: resend" \
  -H "X-Target-Url: https://api.resend.com/emails" \
  -H "Content-Type: application/json" \
  -d '{"from": "noreply@example.com", "to": "user@example.com", "subject": "Hello", "text": "Sent via AgentKeys"}'
```

### With Proxy Token (Option B) — direct credential access

```bash
curl -X POST $AGENTKEYS_PROXY_URL/v1/proxy \
  -H "Authorization: Bearer $AGENTKEYS_PROXY_TOKEN" \
  -H "X-Target-Url: https://api.resend.com/emails" \
  -H "Content-Type: application/json" \
  -d '{"from": "noreply@example.com", "to": "user@example.com", "subject": "Hello", "text": "Sent via AgentKeys"}'
```

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | ✅ | `Bearer $AGENTKEYS_API_KEY` or `Bearer $AGENTKEYS_PROXY_TOKEN` |
| `X-Target-Url` | ✅ | Target API URL to forward to |
| `X-Credential-Name` | ✅ (API key mode) | Name of the credential to use (case-insensitive) |
| `Content-Type` | ❌ | Passed through to target |

## How It Works

1. Agent sends request to AgentKeys proxy with API key + credential name (or proxy token)
2. AgentKeys finds and decrypts the real credential server-side
3. Real credential is injected into headers
4. Request is forwarded to the target API
5. Response is returned to the agent
6. Every request is logged in the audit trail

The agent never sees the real API key, OAuth token, or password.

## Credential Types Supported

- API Key — injected as `Authorization: Bearer <key>`
- Basic Auth — injected as `Authorization: Basic base64(user:pass)`
- Custom Headers — injected as key-value pairs
- Query Parameters — appended to URL
- Cookies — injected as `Cookie` header
- OAuth — auto-refreshed tokens

## Security

- Credentials are AES-256-GCM encrypted at rest
- Proxy tokens are scoped to one credential + one agent
- API key mode still respects workspace permissions
- Tokens can be revoked instantly from the dashboard
- Full audit trail for every proxied request
- Agent never has access to plaintext secrets

## Links

- Dashboard: [app.agentkeys.io](https://app.agentkeys.io)
- Docs: [agentkeys.io/docs](https://agentkeys.io/docs)
- Support: support@agentkeys.io
