---
name: scalekit-auth
description: Implement authentication with Scalekit for web applications, APIs, and MCP servers. Supports full-stack auth, modular SSO (SAML/OIDC), and MCP OAuth 2.1. Handles login, SSO, session management, token validation, and enterprise identity providers. Works with Node.js, Express, Next.js, Python, FastAPI, and MCP servers. Use when implementing authentication, adding SSO, securing APIs, or protecting MCP servers.
---

# Scalekit Authentication Implementation

## Overview

This skill helps you implement Scalekit authentication across different use cases. Choose the implementation path that matches your needs:

### Implementation Paths

**1. Full-Stack Authentication** - Complete auth system for web apps

- User sign-up, login, logout
- Session management with tokens
- Social login (Google, GitHub, etc.)
- Best for: New applications or replacing existing auth

**2. Modular SSO** - Add Enterprise SSO to existing applications

- SAML/OIDC for enterprise customers
- Keep your existing auth system
- No user migration needed
- Best for: B2B SaaS adding enterprise SSO

**3. MCP Server Authentication** - Secure Model Context Protocol servers

- OAuth 2.1 for MCP clients (Claude Desktop, Cursor, VS Code)
- Scalekit-managed or custom auth integration
- Scope-based permissions
- Best for: MCP server developers

## Quick Start: Choose Your Path

### Path 1: Full-Stack Authentication

**When to use:** Building a new app or replacing authentication

**Quickstart:** [full-stack-auth/quickstart.md](full-stack-auth/quickstart.md)

**Templates:**

- [Node.js + Express](full-stack-auth/templates/nodejs-express.md)
- [Next.js App Router](full-stack-auth/templates/nextjs.md)
- [Python + FastAPI](full-stack-auth/templates/python-fastapi.md)

**What you get:**

- Complete login/signup flows
- Session management
- Token refresh
- Logout handling
- Social & enterprise login

---

### Path 2: Modular SSO

**When to use:** Adding Enterprise SSO to existing authentication

**Quickstart:** [modular-sso/quickstart.md](modular-sso/quickstart.md)

**Templates:**

- [Node.js + Express SSO](modular-sso/templates/nodejs-express-sso.md)

**What you get:**

- SAML/OIDC support
- Integration with Auth0/Firebase/Cognito
- Keep existing users and sessions
- Enterprise customer onboarding
- Admin portal for SSO setup

---

### Path 3: MCP Server Authentication

**When to use:** Securing Model Context Protocol servers

**Quickstarts:**

- [OAuth 2.1 with Scalekit](mcp-auth/oauth-quickstart.md) - Scalekit manages auth
- [Custom Auth Integration](mcp-auth/custom-auth-integration.md) - Use your existing auth

**What you get:**

- OAuth 2.1 compliance
- MCP client support
- Token validation
- Scope-based permissions
- Discovery endpoint

---

## Prerequisites

Before implementing any path, ensure you have:

1. **Scalekit Account**: Sign up at <https://scalekit.com>
2. **Environment Variables**: From Scalekit Dashboard → Settings
   - `SCALEKIT_ENVIRONMENT_URL`
   - `SCALEKIT_CLIENT_ID`
   - `SCALEKIT_CLIENT_SECRET`
3. **Callback URLs Registered**: In Scalekit Dashboard → Settings

**Validate your setup:**

```bash
python scripts/validate_env.py
```

## Common Implementation Steps

### Step 1: Install SDK

**Node.js:**

```bash
npm install @scalekit-sdk/node
```

**Python:**

```bash
pip install scalekit-sdk-python
```

### Step 2: Initialize Client

**Node.js:**

```javascript
import { Scalekit } from '@scalekit-sdk/node';

const scalekit = new Scalekit(
  process.env.SCALEKIT_ENVIRONMENT_URL,
  process.env.SCALEKIT_CLIENT_ID,
  process.env.SCALEKIT_CLIENT_SECRET
);
```

**Python:**

```python
from scalekit import ScalekitClient

scalekit = ScalekitClient(
    env_url=os.getenv("SCALEKIT_ENVIRONMENT_URL"),
    client_id=os.getenv("SCALEKIT_CLIENT_ID"),
    client_secret=os.getenv("SCALEKIT_CLIENT_SECRET")
)
```

### Step 3: Follow Your Implementation Path

Choose your path above and follow the quickstart guide.

## Decision Helper

**Not sure which path to use?**

**I need to add authentication to a new web app:**
→ Use **Full-Stack Authentication**

**I have authentication but need to add SSO for enterprise customers:**
→ Use **Modular SSO**

**I'm building an MCP server and need OAuth:**
→ Use **MCP Server Authentication (OAuth 2.1)**

**I have an MCP server and want to use my existing auth:**
→ Use **MCP Server Authentication (Custom Auth)**

**I need to add login to an existing app with no auth:**
→ Use **Full-Stack Authentication**

**Enterprise customers require SAML but I have password-based auth:**
→ Use **Modular SSO** (keeps your password auth)

## Key Concepts

### Full-Stack Auth vs Modular SSO

**Full-Stack Auth:**

- Scalekit handles ALL authentication
- Replaces your auth system
- Tokens managed by Scalekit
- Complete user database in Scalekit

**Modular SSO:**

- Scalekit handles only SSO protocols
- Keeps your existing auth
- YOUR sessions and tokens
- YOUR user database

### OAuth 2.1 for MCP Servers

- MCP clients (Claude Desktop) expect OAuth 2.1
- Scalekit provides OAuth server
- Discovery via `.well-known/oauth-protected-resource`
- Bearer tokens in requests
- Scope-based permissions

## Security Best Practices

### Token Storage

**✅ DO:**

- Use HttpOnly cookies for tokens
- Set `secure: true` in production (HTTPS)
- Use `sameSite: 'strict'` for CSRF protection
- Short token lifetimes (5-60 minutes)

**❌ DON'T:**

- Store tokens in localStorage
- Store tokens in sessionStorage
- Expose tokens to JavaScript

### Token Validation

**Always validate tokens server-side:**

```javascript
// ✅ Server-side validation
const claims = await scalekit.validateToken(token, {
  issuer: process.env.SCALEKIT_ENVIRONMENT_URL,
  audience: process.env.SCALEKIT_CLIENT_ID
});
req.user = claims; // Trust these claims

// ❌ Never trust client-provided data
const userId = req.cookies.userId; // Can be forged!
```

### Session Management

See [reference/session-management.md](reference/session-management.md) for comprehensive patterns.

## Validation Scripts

Test your configuration before deploying:

```bash
# Validate environment variables
python scripts/validate_env.py

# Test Scalekit connectivity
python scripts/test_connection.py

# Interactive auth flow test
python scripts/test_auth_flow.py
```

## Reference Documentation

### Full-Stack Auth

- [Quickstart Guide](full-stack-auth/quickstart.md)
- [Session Management](reference/session-management.md)
- [Security Best Practices](reference/security-best-practices.md)

### Modular SSO

- [Quickstart Guide](modular-sso/quickstart.md)
- [Express Integration](modular-sso/templates/nodejs-express-sso.md)

### MCP Authentication

- [OAuth 2.1 Quickstart](mcp-auth/oauth-quickstart.md)
- [Custom Auth Integration](mcp-auth/custom-auth-integration.md)
- [Python FastMCP Template](mcp-auth/templates/python-fastmcp.md)

## Framework Support

| Framework | Full-Stack Auth | Modular SSO | MCP Auth |
|-----------|----------------|-------------|----------|
| Node.js + Express | ✅ | ✅ | ✅ |
| Next.js (App Router) | ✅ | Coming | ✅ |
| Python + FastAPI | ✅ | Coming | ✅ |
| Python + FastMCP | - | - | ✅ |
| Django | Coming | Coming | Coming |
| Ruby on Rails | Coming | Coming | - |
| Go | Coming | Coming | ✅ |

## Common Issues & Troubleshooting

### Redirect URI Mismatch

**Error:** "redirect_uri_mismatch"

**Solution:**

- Callback URL must match exactly
- Include protocol (http:// or https://)
- Include port if not 80/443
- Check Scalekit Dashboard → Settings → Redirect URIs

### Token Validation Fails

**Error:** "Invalid or expired token"

**Solutions:**

- Verify token in Bearer header: `Authorization: Bearer <token>`
- Check issuer matches environment URL
- Ensure audience includes correct resource
- Token may have expired

### Session Not Persisting

**Symptoms:** Users logged out immediately

**Solutions:**

- Set `secure: false` for localhost (HTTP)
- Check `sameSite` attribute
- Verify browser accepts cookies
- Check cookie domain and path

### CORS Errors

**Symptoms:** Requests blocked by CORS

**Solutions:**

- Configure CORS middleware
- Set `credentials: 'include'` in fetch
- Specify exact origin (not wildcard)
- For cross-site: `sameSite: 'none'` + `secure: true`

## Getting Help

**For implementation questions:**

- Review quickstart guides for your path
- Check framework-specific templates
- See reference documentation

**For Scalekit questions:**

- Documentation: <https://docs.scalekit.com>
- Support: <support@scalekit.com>

## Advanced Features

### Role-Based Access Control (RBAC)

Use token claims for authorization:

```javascript
async function requireRole(req, res, next, role) {
  const claims = await scalekit.validateToken(req.cookies.accessToken, {
    issuer: process.env.SCALEKIT_ENVIRONMENT_URL,
    audience: process.env.SCALEKIT_CLIENT_ID
  });

  if (!claims.roles?.includes(role)) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  next();
}
```

### Organization-Based Access

Multi-tenant applications:

```javascript
const claims = await scalekit.validateToken(token, {
  issuer: process.env.SCALEKIT_ENVIRONMENT_URL,
  audience: process.env.SCALEKIT_CLIENT_ID
});
const orgId = claims.org_id;

// Only allow access to organization's data
const data = await db.getData({ organization_id: orgId });
```

### Custom Claims

Add custom data to tokens:

```javascript
// When submitting user to Scalekit
await scalekit.auth.updateLoginUserDetails(connectionId, loginRequestId, {
  sub: user.id,
  email: user.email,
  custom_field: 'custom_value', // Custom claim
  roles: user.roles,
  organization_id: user.orgId
});

// Later, in token validation
const claims = await scalekit.validateToken(token, {
  issuer: process.env.SCALEKIT_ENVIRONMENT_URL,
  audience: process.env.SCALEKIT_CLIENT_ID
});
console.log(claims.custom_field); // 'custom_value'
```

## Next Steps by Path

### After Full-Stack Auth

1. Enable social login (Google, GitHub, Microsoft)
2. Add role-based access control
3. Customize login UI
4. Set up email notifications
5. Consider adding enterprise SSO

### After Modular SSO

1. Enable domain verification
2. Set up SCIM for user provisioning
3. Add role mapping from IdP
4. Implement JIT provisioning
5. Create admin portal for customers

### After MCP Authentication

1. Add more scopes for granular permissions
2. Implement rate limiting
3. Add audit logging
4. Test with multiple MCP clients
5. Document API for developers

## Version Information

- **Current Version:** v1.0.0
- **Includes:**
  - Full-Stack Authentication
  - Modular SSO
  - MCP Server Authentication (OAuth 2.1 & Custom)
- **Supported Languages:** Node.js, Python
- **Supported Frameworks:** Express, Next.js, FastAPI

For the latest updates, see the [GitHub repository](https://github.com/scalekit-inc/claude-auth-skill).
