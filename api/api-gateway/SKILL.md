---
name: api-gateway
description: |-
  OpenClaw API gateway proxy for authenticated SaaS calls (100+ services in references/SERVICES.md).
  Use ONLY when making an HTTP request to a third-party service that requires the gateway's stored
  credentials. NOT for direct API calls with bearer tokens already in scope, NOT for monday.com
  (use monday-for-agents), NOT for WhatsApp (use heleni-whatsapp).
  Triggers: "call the X API", "fetch from <service>", "send to Slack via gateway", "use the gateway for".
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# API Gateway

Passthrough proxy for direct access to third-party APIs using managed OAuth connections, provided by [Maton](https://maton.ai). The API gateway lets you call native API endpoints directly.

## Quick Start

```bash
# Native Slack API call
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'channel': 'C0123456', 'text': 'Hello from gateway!'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/slack/api/chat.postMessage', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```


## Base URL

```
https://gateway.maton.ai/{app}/{native-api-path}
```

Replace `{app}` with the service name and `{native-api-path}` with the actual API endpoint path.

IMPORTANT: The URL path MUST start with the connection's app name (eg. `/google-mail/...`). This prefix tells the gateway which app connection to use. For example, the native Gmail API path starts with `gmail/v1/`, so full paths look like `/google-mail/gmail/v1/users/me/messages`.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

The API gateway automatically injects the appropriate OAuth token for the target service.

**Environment Variable:** You can set your API key as the `MATON_API_KEY` environment variable:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

## Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Click the copy button on the right side of API Key section to copy it

## Connection Management

Connection management uses a separate base URL: `https://ctrl.maton.ai`

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=slack&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Query Parameters (optional):**
- `app` - Filter by service name (e.g., `slack`, `hubspot`, `salesforce`)
- `status` - Filter by connection status (`ACTIVE`, `PENDING`, `FAILED`)

**Response:**
```json
{
  "connections": [
    {
      "connection_id": "{connection_id}",
      "status": "ACTIVE",
      "creation_time": "2025-12-08T07:20:53.488460Z",
      "last_updated_time": "2026-01-31T20:03:32.593153Z",
      "url": "https://connect.maton.ai/?session_token=5e9...",
      "app": "slack",
      "method": "OAUTH2",
      "metadata": {}
    }
  ]
}
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'slack'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Request Body:**
- `app` (required) - Service name (e.g., `slack`, `notion`)
- `method` (optional) - Connection method (`API_KEY`, `BASIC`, `OAUTH1`, `OAUTH2`, `MCP`)

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=5e9...",
    "app": "slack",
    "metadata": {}
  }
}
```

Open the returned URL in a browser to complete OAuth.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple connections for the same app, you can specify which connection to use by adding the `Maton-Connection` header with the connection ID:

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'channel': 'C0123456', 'text': 'Hello!'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/slack/api/chat.postMessage', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If omitted, the gateway uses the default (oldest) active connection for that app.

## Supported Services

See [references/SERVICES.md](references/SERVICES.md) for the full list of 100+ supported SaaS services and their base URLs.

## Examples

See [references/EXAMPLES.md](references/EXAMPLES.md) for code examples.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing connection for the requested app |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited (10 requests/second per account) |
| 500 | Internal Server Error |
| 4xx/5xx | Passthrough error from the target API |

Errors from the target API are passed through with their original status codes and response bodies.

### Troubleshooting: API Key Issues

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Verify your URL path starts with the correct app name. The path must begin with `/google-mail/`. For example:

- Correct: `https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages`
- Incorrect: `https://gateway.maton.ai/gmail/v1/users/me/messages`

2. Ensure you have an active connection for the app. List your connections to verify:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Server Error

A 500 error may indicate an expired OAuth token. Try creating a new connection via the Connection Management section above and completing OAuth authorization. If the new connection is "ACTIVE", delete the old connection to ensure the gateway uses the new one.

## Rate Limits

- 10 requests per second per account
- Target API rate limits also apply

## Notes

- When using curl with URLs containing brackets (`fields[]`, `sort[]`, `records[]`), use the `-g` flag to disable glob parsing
- When piping curl output to `jq`, environment variables may not expand correctly in some shells, which can cause "Invalid API key" errors
- **Media upload URLs (LinkedIn, etc.):** Some APIs return pre-signed upload URLs that point to a different host than the gateway proxies (e.g., LinkedIn returns `www.linkedin.com` upload URLs, but the gateway proxies `api.linkedin.com`). These upload URLs are pre-signed and do NOT require an Authorization header — upload the binary directly to the returned URL without going through the gateway. **You MUST use Python `urllib`** for these uploads because the URLs contain encoded characters (e.g., `%253D`) that get corrupted when passed through shell variables or `curl`. Always parse the JSON response with `json.load()` and use the URL directly in Python.

## Tips

1. **Use native API docs**: Refer to each service's official API documentation for endpoint paths and parameters.

2. **Headers are forwarded**: Custom headers (except `Host` and `Authorization`) are forwarded to the target API.

3. **Query params work**: URL query parameters are passed through to the target API.

4. **All HTTP methods supported**: GET, POST, PUT, PATCH, DELETE are all supported.

5. **QuickBooks special case**: Use `:realmId` in the path and it will be replaced with the connected realm ID.

## Optional

- [Github](https://github.com/maton-ai/api-gateway-skill)
- [API Reference](https://www.maton.ai/docs/api-reference)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
