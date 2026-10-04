---
name: authos-service-api-integration
description: Integrate trusted backend services with AuthOS service API routes using X-Api-Key. Use when listing or managing service users, subscriptions, service metadata, service analytics, or provider-token requests from a server-side application.
---

# AuthOS Service API Integration

## Public AuthOS Links

Use these public AuthOS links when producing user-facing setup or troubleshooting guidance:

- Main site: https://authos.dev/
- Documentation: https://authos.dev/docs/
- AI Agent Skills guide: https://authos.dev/docs/ai-agent-skills/
- AuthOS source repository: https://github.com/drmhse/AuthOS

Use this skill for service-to-service work with AuthOS API keys. Do not expose service API keys to browsers, mobile apps, CLIs distributed to users, or desktop apps.

## Authentication

Service API routes are authenticated with an API key in the `X-Api-Key` header. In the SDK:

```typescript
import { SsoClient } from '@drmhse/sso-sdk';

const authos = new SsoClient({
  baseURL: process.env.AUTHOS_BASE_URL!,
  apiKey: process.env.AUTHOS_SERVICE_API_KEY!
});
```

Create service API keys through the organization service management API:

- `POST /api/organizations/:org_slug/services/:service_slug/api-keys`
- `GET /api/organizations/:org_slug/services/:service_slug/api-keys`
- `DELETE /api/organizations/:org_slug/services/:service_slug/api-keys/:api_key_id`

## Service API Routes

- `GET/POST /api/service/users`
- `GET/PATCH/DELETE /api/service/users/:user_id`
- `GET/POST /api/service/subscriptions`
- `GET/PATCH/DELETE /api/service/subscriptions/:user_id`
- `GET /api/service/analytics`
- `POST /api/service/provider-tokens`
- `GET/PATCH /api/service/info`

These routes are scoped by the API key's service. Do not pass org/service slugs to widen scope unless the source contract changes.

## SDK Usage

List users:

```typescript
const { users, total } = await authos.serviceApi.listUsers({ limit: 50, offset: 0 });
```

Create a user:

```typescript
const user = await authos.serviceApi.createUser({ email: 'user@example.com' });
```

Manage subscriptions:

```typescript
await authos.serviceApi.createSubscription({
  user_id: user.id,
  plan_id: 'plan-id',
  status: 'active'
});
```

Read service analytics:

```typescript
const analytics = await authos.serviceApi.getAnalytics();
```

## Provider Token Requests

Use `/api/service/provider-tokens` when your backend needs a provider token for a user, such as GitHub, Google, or Microsoft access granted through AuthOS.

Possible response classes:

- `status: "ok"` with `access_token`, `expires_at`, `scopes`, `provider`, and `account`.
- `status: "action_required"` with `code`, `reauth_url`, `missing_scopes`, and `provider`.

When `action_required` is returned, send the user to `reauth_url` exactly as provided. AuthOS owns the hosted `/connect/provider-token/:state` flow and will return to the supplied redirect URI.

## Security Rules

- Store API keys only in server-side secret storage.
- Rotate keys through the service management endpoints if exposed.
- Use separate API keys per environment and job type.
- Keep requested provider scopes minimal.
- Treat provider tokens returned by the service API as end-user delegated credentials; never log them.
