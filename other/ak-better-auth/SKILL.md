---
name: ak-better-auth
description: "Add Better Auth (TypeScript): email/password, OAuth (Google, GitHub), 2FA/MFA, passkeys/WebAuthn, sessions, RBAC, rate limiting."
when_to_use: "Invoke when setting up or extending an app's authentication."
category: engineering
keywords: [auth, oauth, 2fa, passkeys, sessions]
license: Proprietary
argument-hint: "[auth-method or feature]"
metadata:
  author: agentkit
  version: "2.0.1"
---

# Better Auth Skill

Better Auth is comprehensive, framework-agnostic authentication/authorization framework for TypeScript with built-in email/password, social OAuth, and powerful plugin ecosystem for advanced features.

## When to Use

- Implementing auth in TypeScript/JavaScript applications
- Adding email/password or social OAuth authentication
- Setting up 2FA, passkeys, magic links, advanced auth features
- Building multi-tenant apps with organization support
- Managing sessions and user lifecycle
- Working with any framework (Next.js, Nuxt, SvelteKit, Remix, Astro, Hono, Express, etc.)

## Route

Inspect installed Better Auth version, existing server/client wiring and schema first.
Install/scaffold only for a new integration: `references/installation-recipes.md`.
For existing integration select email/OAuth, session/plugin or database migration from the
references below. Do not rerun initialization to add a plugin.

Verify callback failure, session expiry/revocation and the selected plugin failure paths.
Keep secrets server-side; protect session binding, token single use and verified ownership.

## Feature Selection Matrix

| Feature | Plugin Required | Use Case | Reference |
|---------|----------------|----------|-----------|
| Email/Password | No (built-in) | Basic auth | [email-password-auth.md](./references/email-password-auth.md) |
| OAuth (GitHub, Google, etc.) | No (built-in) | Social login | [oauth-providers.md](./references/oauth-providers.md) |
| Email Verification | No (built-in) | Verify email addresses | [email-password-auth.md](./references/email-password-auth.md#email-verification) |
| Password Reset | No (built-in) | Forgot password flow | [email-password-auth.md](./references/email-password-auth.md#password-reset) |
| Two-Factor Auth (2FA/TOTP) | Yes (`twoFactor`) | Enhanced security | [advanced-features.md](./references/advanced-features.md#two-factor-authentication) |
| Passkeys/WebAuthn | Yes (`passkey`) | Passwordless auth | [advanced-features.md](./references/advanced-features.md#passkeys-webauthn) |
| Magic Link | Yes (`magicLink`) | Email-based login | [advanced-features.md](./references/advanced-features.md#magic-link) |
| Username Auth | Yes (`username`) | Username login | [email-password-auth.md](./references/email-password-auth.md#username-authentication) |
| Organizations/Multi-tenant | Yes (`organization`) | Team/org features | [advanced-features.md](./references/advanced-features.md#organizations) |
| Rate Limiting | No (built-in) | Prevent abuse | [advanced-features.md](./references/advanced-features.md#rate-limiting) |
| Session Management | No (built-in) | User sessions | [advanced-features.md](./references/advanced-features.md#session-management) |

Choose another auth method only when requested or required by the accepted design. Read `references/method-selection.md` for a new integration.

## Current Security Notes

Check the installed version against [upstream security advisories](https://github.com/better-auth/better-auth/security/advisories) and versioned release notes before asserting a fix is present. Preserve these invariants for the enabled features; verify exact option names against that version:

- `oidc-provider` and `mcp` plugins: confidential clients must require `client_secret` on refresh-token grants; use constant-time secret comparison and reject incomplete PKCE parameters.
- `magicLink`: verification tokens are single-use; avoid custom flows that mint multiple sessions from concurrent requests.
- Organizations/invitations: keep `requireEmailVerificationOnInvitation` enabled so unverified email ownership cannot accept or enumerate invitations.
- Device authorization: bind pending device codes to the verifying session so one authenticated user cannot approve another user's device flow.

## Reference Documentation

### Core Authentication
- [Email/Password Authentication](./references/email-password-auth.md) - Email/password setup, verification, password reset, username auth
- [OAuth Providers](./references/oauth-providers.md) - Social login setup, provider configuration, token management
- [Database Integration](./references/database-integration.md) - Database adapters, schema setup, migrations

### Advanced Features
- [Advanced Features](./references/advanced-features.md) - 2FA/MFA, passkeys, magic links, organizations, rate limiting, session management

## Scripts

- `scripts/better_auth_init.py` - Initialize Better Auth configuration with interactive setup

## Resources

- Docs: https://www.better-auth.com/docs
- GitHub: https://github.com/better-auth/better-auth
- Plugins: https://www.better-auth.com/docs/plugins
- Examples: https://www.better-auth.com/docs/examples
