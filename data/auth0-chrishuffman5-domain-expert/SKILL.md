---
name: auth0
description: "Expert agent for Auth0 customer identity platform. Provides deep expertise in Universal Login, Actions, Organizations, Connections, RBAC, Attack Protection, and machine-to-machine authentication for CIAM scenarios. WHEN: \"Auth0\", \"Universal Login\", \"Auth0 Actions\", \"Auth0 Organizations\", \"CIAM\", \"Auth0 connections\", \"Auth0 rules\", \"Auth0 hooks\", \"Auth0 tenant\", \"Auth0 attack protection\", \"Auth0 FGA\"."
license: MIT
---

# Auth0

This skill covers Auth0 (an Okta company), the customer identity (CIAM) platform. It has deep knowledge of Universal Login, Actions, Organizations, Connections, RBAC, Attack Protection, and developer-focused identity integration.

## Identity and Scope

Auth0 is a developer-focused CIAM platform that provides:
- Universal Login for customizable authentication experiences
- Actions for extensible authentication and authorization hooks
- Organizations for B2B multi-tenancy
- Connections to identity sources (social, enterprise, database)
- Attack Protection (brute force, breached password detection, bot detection)
- Fine-Grained Authorization (FGA) with Okta FGA (based on OpenFGA/Zanzibar)

**Auth0 vs. Okta:** Auth0 is for customer-facing identity (CIAM). Okta is for workforce identity. They are complementary products under the same company.

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **Authentication flow** -- Universal Login, Connections, passwordless
   - **Extensibility** -- Actions, Forms, custom database connections
   - **Multi-tenancy** -- Organizations for B2B SaaS
   - **Authorization** -- RBAC, FGA, permissions
   - **Security** -- Attack Protection, anomaly detection, logging
   - **Architecture** -- Tenant strategy, environment management, migration

2. **Identify deployment model** -- Auth0 tenants per environment (dev/staging/prod)

3. **Analyze** -- Apply Auth0-specific reasoning. Consider the Auth0 pipeline (Actions flow), tenant architecture, and CIAM use cases.

4. **Recommend** -- Provide actionable guidance with Auth0 Dashboard paths, Management API examples, and code snippets.

## Core Expertise

### Tenant Architecture

Auth0 uses a tenant-per-environment model:

```
dev.company.auth0.com     --> Development (free to experiment)
staging.company.auth0.com --> Staging (mirrors production)
company.auth0.com         --> Production (custom domain: auth.company.com)
```

**Custom domains:** Production tenants should use a custom domain (`auth.company.com`) for:
- Brand consistency (no `auth0.com` in login URLs)
- Cookie-based session management (same-site cookies)
- Universal Login customization

### Universal Login

Auth0's hosted login page:

**New Universal Login (recommended):**
- Rendered by Auth0 (not your application)
- Customizable via branding settings (logo, colors, fonts)
- Supports Lock and custom HTML/CSS
- Automatic feature upgrades (new MFA methods, passkeys)
- Redirect-based flow (SPA redirects to Auth0 for login)

**Classic Universal Login (legacy):**
- Fully customizable HTML/JS/CSS hosted on Auth0
- Full control but requires manual maintenance
- No automatic feature upgrades

**Why hosted login over embedded:**
- Security: credentials never touch your application servers
- Compliance: SSO session managed by Auth0
- Features: Attack Protection, MFA, social login work automatically
- Best practice: Auth0 and security standards recommend redirect-based flows

### Connections

Identity sources that provide user credentials:

| Connection Type | Examples | Use Case |
|---|---|---|
| **Database** | Auth0-managed or custom DB | Username/password (your own user store) |
| **Social** | Google, Apple, Facebook, GitHub, LinkedIn | Consumer sign-up/sign-in |
| **Enterprise** | SAML, OIDC, Azure AD, Google Workspace, ADFS | Employee/partner SSO |
| **Passwordless** | Email (magic link/OTP), SMS OTP | Passwordless authentication |
| **Custom** | Custom database scripts (login, create, verify, etc.) | Legacy user migration |

**Custom database connections:** Enable gradual user migration. On first login, Auth0 calls your custom script to validate credentials against the legacy system. If valid, Auth0 creates the user in its database. Subsequent logins use Auth0 directly.

```javascript
// Custom database login script (for lazy migration)
async function login(email, password, callback) {
  const bcrypt = require('bcrypt');
  const { Client } = require('pg');
  
  const client = new Client({ connectionString: configuration.PG_URL });
  await client.connect();
  
  const result = await client.query(
    'SELECT id, email, password_hash FROM users WHERE email = $1', [email]
  );
  
  if (result.rows.length === 0) return callback(new WrongUsernameOrPasswordError(email));
  
  const match = await bcrypt.compare(password, result.rows[0].password_hash);
  if (!match) return callback(new WrongUsernameOrPasswordError(email));
  
  return callback(null, {
    user_id: result.rows[0].id.toString(),
    email: result.rows[0].email
  });
}
```

### Actions

Serverless functions that hook into Auth0's authentication and authorization pipeline:

**Triggers (flow insertion points):**

| Trigger | When It Runs | Use Case |
|---|---|---|
| **Login / Post Login** | After authentication, before tokens issued | Add custom claims, enrich profile, enforce policies |
| **Machine to Machine** | During client credentials flow | Add custom claims to M2M tokens |
| **Pre User Registration** | Before user is created | Validate email domain, check deny lists |
| **Post User Registration** | After user is created | Send welcome email, create downstream accounts |
| **Post Change Password** | After password change | Notify user, audit log, sync to legacy system |
| **Send Phone Message** | When SMS/Voice OTP is sent | Custom SMS provider (Twilio, MessageBird) |

**Action example (add custom claims to token):**
```javascript
exports.onExecutePostLogin = async (event, api) => {
  const namespace = 'https://myapp.com/claims';
  
  // Add roles from app_metadata
  if (event.user.app_metadata?.roles) {
    api.idToken.setCustomClaim(`${namespace}/roles`, event.user.app_metadata.roles);
    api.accessToken.setCustomClaim(`${namespace}/roles`, event.user.app_metadata.roles);
  }
  
  // Enrich with external data
  const response = await fetch(`https://api.company.com/users/${event.user.user_id}/permissions`);
  const permissions = await response.json();
  api.accessToken.setCustomClaim(`${namespace}/permissions`, permissions);
  
  // Deny access based on condition
  if (event.user.email_verified === false) {
    api.access.deny('Please verify your email before logging in.');
  }
};
```

**Actions vs. Rules vs. Hooks:**
- **Actions** -- Current, recommended extensibility mechanism. Serverless Node.js functions with clear triggers.
- **Rules** -- Legacy (deprecated). Migrate to Actions.
- **Hooks** -- Legacy (deprecated for most triggers). Migrate to Actions.

### Organizations

Multi-tenancy support for B2B SaaS applications:

- Each **Organization** represents a customer/company in your B2B SaaS
- Organizations have their own: connections (which IdPs their users use), branding, MFA policies, members
- Users can be members of multiple organizations
- Organization-specific login: `/authorize?organization=org_xxx`

```javascript
// Invite a member to an organization
const ManagementClient = require('auth0').ManagementClient;
const management = new ManagementClient({ domain, clientId, clientSecret });

await management.organizations.addMembers(
  { id: 'org_abc123' },
  { members: ['auth0|user_id_123'] }
);

// Assign roles within an organization
await management.organizations.addMemberRoles(
  { id: 'org_abc123', user_id: 'auth0|user_id_123' },
  { roles: ['rol_admin'] }
);
```

### RBAC

Auth0's role-based access control:

- **Roles** -- Named sets of permissions (e.g., `admin`, `editor`, `viewer`)
- **Permissions** -- Granular access rights tied to APIs (e.g., `read:articles`, `write:articles`)
- **APIs (Resource Servers)** -- Define scopes/permissions (e.g., `https://api.company.com`)
- Permissions are included in the access token as the `permissions` claim

**Token example with RBAC:**
```json
{
  "iss": "https://company.auth0.com/",
  "sub": "auth0|user123",
  "aud": "https://api.company.com",
  "permissions": ["read:articles", "write:articles", "delete:articles"],
  "org_id": "org_abc123"
}
```

### Attack Protection

| Feature | Protection | Configuration |
|---|---|---|
| **Bot Detection** | Blocks automated credential stuffing | CAPTCHA challenge on suspicious requests |
| **Brute-Force Protection** | Rate limits login attempts per user/IP | Block after N failed attempts from same IP or for same account |
| **Breached Password Detection** | Checks passwords against breach databases | Block or warn on compromised passwords |
| **Suspicious IP Throttling** | Rate limits login from IPs with high failure rates | Throttle after anomalous failure rate |
| **Adaptive MFA** | Risk-based MFA challenges | Challenge based on impossible travel, new device, new IP |

### Auth0 for AI Agents (Machine-to-Machine)

Auth0 supports machine-to-machine authentication for AI agents and services:

- **Client Credentials flow** -- Service-to-service authentication without user context
- **Token exchange** -- Exchange user tokens for service tokens with reduced scope
- **Fine-Grained Authorization (FGA)** -- Okta FGA (based on OpenFGA/Google Zanzibar) for relationship-based access control
- **Audience and scopes** -- Different access tokens for different APIs

## Deployment and Operations

### Environment Strategy

| Environment | Purpose | Connection Config |
|---|---|---|
| Development | Feature development, testing | Test social connections, mock enterprise IdP |
| Staging | Pre-production validation | Mirror production connections, test data |
| Production | Live customer traffic | Real connections, custom domain, full monitoring |

### Tenant Configuration as Code

Use the Auth0 Deploy CLI or Terraform provider:

```bash
# Auth0 Deploy CLI
a0deploy export -c config.json --format directory --output_folder ./auth0

# Terraform
terraform {
  required_providers {
    auth0 = { source = "auth0/auth0" }
  }
}

resource "auth0_client" "my_app" {
  name     = "My Application"
  app_type = "spa"
  callbacks = ["https://app.company.com/callback"]
  allowed_logout_urls = ["https://app.company.com"]
}
```

### Logging and Monitoring

- **Tenant logs** -- Authentication events, management API calls, anomaly events
- **Log streaming** -- Stream to Datadog, Splunk, Sumo Logic, AWS EventBridge, custom webhook
- **Auth0 Dashboard** -- Real-time activity dashboard with authentication metrics

**Critical events to monitor:**
- `fcoa` -- Failed cross-origin authentication
- `fp` -- Failed password login
- `fu` -- Failed login (generic)
- `limit_mu` -- Blocked IP due to multiple failed logins for one user
- `limit_wc` -- Blocked account due to too many failed logins
- `depnote` -- Deprecation notice (feature being removed)

## Common Pitfalls

1. **Rules/Hooks instead of Actions** -- Rules and Hooks are deprecated. All new extensibility should use Actions.
2. **Embedded login** -- Using Lock.js embedded in your SPA instead of redirect to Universal Login. Redirect-based is more secure and feature-rich.
3. **Storing secrets in Actions code** -- Use `event.secrets` for API keys and credentials, not hardcoded values.
4. **Not using custom domain in production** -- Third-party cookie restrictions break flows without a custom domain.
5. **Token storage in localStorage** -- Access tokens in localStorage are vulnerable to XSS. Use in-memory storage or secure cookies.
6. **Ignoring rate limits** -- Management API rate limit: 50 requests/second. Plan for bulk operations accordingly.
7. **Single tenant for all environments** -- Use separate tenants for dev/staging/production. Avoid testing in production.
