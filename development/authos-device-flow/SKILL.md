---
name: authos-device-flow
description: Implement AuthOS device authorization for CLIs, TVs, and headless apps. Use when requesting device codes, building activation pages, polling /auth/token, handling MFA during device auth, or adding platform admin CLI login through AuthOS.
---

# AuthOS Device Flow

## Public AuthOS Links

Use these public AuthOS links when producing user-facing setup or troubleshooting guidance:

- Main site: https://authos.dev/
- Documentation: https://authos.dev/docs/
- AI Agent Skills guide: https://authos.dev/docs/ai-agent-skills/
- AuthOS source repository: https://github.com/drmhse/AuthOS

Use this skill for OAuth 2.0 device authorization flows backed by AuthOS. Device flow is implemented in source with three public endpoints and matching SDK helpers.

## Endpoints

- `POST /auth/device/code`: create a device code.
- `POST /auth/device/verify`: validate a user-facing code and return org/service/provider context.
- `POST /auth/token`: exchange an authorized device code for a bearer token.

The SDK exposes these as `authos.auth.deviceCode.request`, `verify`, and `exchangeToken`.

## Request a Device Code

```typescript
const device = await authos.auth.deviceCode.request({
  client_id: 'service-client-id',
  org: 'acme',
  service: 'cli'
});

console.log(`Open ${device.verification_uri}`);
console.log(`Enter ${device.user_code}`);
```

The request fields are `client_id`, `org`, and `service`.

For a service-level device flow, AuthOS validates the service by client ID, org slug, and service slug, then uses that service's `device_activation_uri`. Configure that URI on the service before offering CLI login.

For platform admin CLI login, source supports `org = "platform"`, `service = "admin-cli"`, and a `client_id` starting with `platform-`; the verification URI comes from `PLATFORM_DASHBOARD_BASE_URL + /activate`.

## Activation Page

On the activation page, call:

```typescript
const context = await authos.auth.deviceCode.verify(userCode);
```

The response contains:

```typescript
{
  org_slug: string;
  service_slug: string;
  available_providers: string[];
}
```

Start OAuth using the returned context and include `user_code` in the login URL:

```typescript
const url = authos.auth.getLoginUrl('github', {
  org: context.org_slug,
  service: context.service_slug,
  user_code: userCode
});
```

Platform activation uses `getAdminLoginUrl(provider, { user_code })`.

## Polling

Poll no faster than the returned `interval`:

```typescript
const token = await authos.auth.deviceCode.exchangeToken({
  grant_type: 'urn:ietf:params:oauth:grant-type:device_code',
  device_code: device.device_code,
  client_id: 'service-client-id'
});
```

`/auth/token` only accepts `urn:ietf:params:oauth:grant-type:device_code`. It returns `access_token`, `token_type`, and `expires_in`; source does not include a refresh token in the device-flow token response even though sessions are stored server-side with refresh tokens.

## MFA Behavior

If the authenticating user has MFA enabled, AuthOS redirects the browser side to an MFA challenge and the device remains unauthorized until MFA succeeds. The device polling side should treat MFA-related errors as "continue waiting and show a browser action required" rather than trying to collect MFA codes in the CLI.

## Implementation Rules

- Timeout locally when `expires_in` elapses.
- Respect `interval`; do not tight-loop.
- Do not store raw AuthOS access tokens on disk unless the product explicitly accepts that risk.
- For backend applications, exchange the AuthOS token for an app-owned session after verification.
- Do not invent `/oauth/device/code`; the source route is `/auth/device/code`.
