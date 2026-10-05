---
name: api-integration
description: Integrate with external APIs, REST, GraphQL, web services, SDKs, and
  third-party tools. Use when connecting external services, managing API keys securely,
  handling authentication (OAuth, JWT, API keys), implementing network retry logic,
  or configuring HTTP client libraries.
argument-hint: <API name, endpoint, or service>
---

<!-- Generated from skills/api-integration.md by tools/generate_integrations.py. Edit the source file, not this one. -->

# Skill: API Integration & External Services

## Purpose
Integrate with external APIs, web services, libraries, and third-party tools. _Source: Cursor (Category E)_

## Tools Required
- HTTP/fetch tools _Source: OpenAI (Category C)_
- Package management commands _Source: Augment (Category E)_
- API key configuration tools _Source: Replit (Category G)_

## General Principles
- Use best-suited external APIs and packages without asking permission _Source: Augment (Category E)_
- Match API/package versions to existing dependency management files _Source: Amp (Category E)_
- Never hardcode API keys — use environment variables _Source: Kiro (Category E)_
- Point out when an external API requires a key _Source: Replit (Category G)_

## API Selection
- Check if the project already uses a similar API/library — reuse it _Source: Amp (Category E)_
- Choose versions compatible with existing dependency manifests _Source: Amp (Category E)_
- Prefer well-established, maintained libraries _Source: Amp (Category E)_
- For new projects: use latest stable version _Source: Amp (Category E)_

```python
# API version selection priority:
1. Already present in dependency management file → use that version _Source: Amp (Category E)_
2. Compatible with existing major version range → use latest in that range _Source: Amp (Category E)_
3. No existing deps → use latest stable _Source: Amp (Category E)_
```

## API Key & Secret Handling
- NEVER hardcode secrets in source code _Source: Kiro (Category E)_
- NEVER commit .env files with real secrets _Source: Kiro (Category E)_
- Use environment variables: `process.env.API_KEY` _Source: Warp (Category G)_
- Point out required keys to user: "You'll need to set OPENAI_API_KEY in your .env" _Source: Replit (Category G)_
- For local dev, suggest .env files (and ensure they're in .gitignore) _Source: Factory (Category G)_

## REST API Integration
- Use appropriate HTTP methods (GET, POST, PUT, DELETE, PATCH) _Source: Amp (Category E)_
- Handle response status codes properly _Source: Amp (Category E)_
- Implement error handling for network failures _Source: Amp (Category E)_
- Add request/response logging for debugging _Source: Amp (Category E)_
- Set reasonable timeouts (default: 30s) _Source: Amp (Category E)_

## GraphQL API Integration
- Use query batching for multiple requests _Source: Amp (Category C)_
- Handle partial error responses _Source: Amp (Category E)_
- Implement pagination for list queries _Source: Amp (Category E)_

## Authentication Patterns
- API Key (header-based): `Authorization: Bearer <key>` _Source: OpenAI (Category C)_
- OAuth 2.0: redirect → code → token flow _Source: OpenAI (Category C)_
- Basic Auth: `Authorization: Basic <base64>` _Source: OpenAI (Category C)_
- JWT: decode for debugging, verify expiry _Source: Amp (Category E)_

## Tool/CLI Integration
- For local tools: check if installed before using, provide install instructions if not _Source: Factory (Category P)_
- For npm packages: check package.json before suggesting _Source: Augment (Category E)_
- Prefer npx/pnpx for one-off tool runs _Source: Augment (Category E)_

## Example Patterns

### Node.js/Express API call
```javascript
const response = await fetch("https://api.example.com/v1/data", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${process.env.API_KEY}`
  },
  body: JSON.stringify({ query: "data" })
});
if (!response.ok) {
  throw new Error(`API error: ${response.status} ${response.statusText}`);
}
const data = await response.json();
```

### Python API call
```python
import requests

response = requests.post(
    "https://api.example.com/v1/data",
    headers={"Authorization": f"Bearer {os.environ['API_KEY']}"},
    json={"query": "data"},
    timeout=30
)
response.raise_for_status()
data = response.json()
```

## Error Recovery
- Network errors: retry with exponential backoff (max 3 retries) _Source: Amp (Category E)_
- Rate limiting: respect Retry-After headers _Source: Amp (Category E)_
- Auth errors: check credentials, don't retry blindly _Source: Amp (Category E)_
- Server errors (5xx): retry, may be transient _Source: Amp (Category E)_
- Client errors (4xx): don't retry — fix the request _Source: Amp (Category E)_

## Domain-Specific Knowledge
When integrating with specific platforms, learn their domain model: _Source: Amp (Category H)_
- **Notion**: workspaces, pages, databases, properties, views, data sources _Source: Notion (Category S)_
- **GitHub**: repos, issues, PRs, commits, actions, releases _Source: Factory (Category O)_
- **Slack**: channels, messages, threads, users, workspace _Source: Amp (Category S)_
- **Linear**: teams, issues, cycles, projects, workflows _Source: Amp (Category S)_

Check the platform's documentation for exact API schemas. _Source: Amp (Category H)_
