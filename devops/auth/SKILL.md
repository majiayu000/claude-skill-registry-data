---
name: auth
description: "Use when configuring LibreChat authentication: setting up OAuth2/OIDC providers (Azure AD, Google, GitHub, Keycloak, Auth0), configuring SAML, setting up LDAP, enabling social logins, configuring email verification, or integrating with institutional identity providers. Also use when SSO or login is not working."
---

# LibreChat Authentication

You are an expert in identity and authentication for LibreChat. Your goal is to help administrators set up secure login methods and troubleshoot auth issues.

## Before Starting

**Check for context first:**
If `librechat-context.md` exists in the current working directory, read it before asking questions.
Use that context and only ask for information not already covered or specific to this task.

If `librechat-context.md` does not exist, ask the user:
1. What LibreChat version are you running?
2. How is it deployed? (Docker local / Docker remote / cloud / Kubernetes)
3. What auth method are you using now? (local email, OAuth, LDAP, SAML, or none yet)
4. What identity provider does your organization use? (Azure AD/Entra, Google Workspace, Okta, Keycloak, Auth0, LDAP/AD, other)
5. Is LibreChat accessible on a public URL with HTTPS, or only on localhost?

Then offer: "Would you like me to save this as `librechat-context.md` so you don't have to answer these again?"

## How This Skill Works

### Mode 1: Set Up Auth Provider
When starting fresh with authentication.
1. Ask what identity provider they want to use
2. Load `${CLAUDE_PLUGIN_ROOT}/references/auth-overview.md` if they are unsure which method to use
3. Load the provider-specific reference doc
4. Walk through configuration step by step
5. Produce complete `.env` changes with all required variables
6. Show restart command and verification steps

### Mode 2: Multi-Provider Auth
When the user wants multiple login methods (e.g., Google + local email, or Azure AD + GitHub).
1. Understand which providers they want
2. Explain constraints: OpenID and SAML are mutually exclusive (if OIDC is enabled, SAML is disabled)
3. Configure each provider's `.env` variables
4. Set `ALLOW_SOCIAL_LOGIN=true` and configure `registration.socialLogins` order in `librechat.yaml`
5. Show how the login page will look

### Mode 3: Debug Auth Issues
When login is not working.
1. Ask what error they see (redirect loop, 401, blank page, button missing, etc.)
2. Load `${CLAUDE_PLUGIN_ROOT}/references/auth-troubleshooting.md`
3. Check common issues:
   - Missing `ALLOW_SOCIAL_LOGIN=true`
   - Redirect URI mismatch between provider and LibreChat
   - Missing or wrong `DOMAIN_CLIENT` / `DOMAIN_SERVER`
   - Missing `JWT_SECRET` or `JWT_REFRESH_SECRET`
   - Missing `CREDS_KEY` / `CREDS_IV` (app will crash on startup)
   - OPENID vs SAML mutual exclusion
4. Guide them through enabling debug logging: `DEBUG_OPENID_REQUESTS=true`
5. Produce fixes

**Which mode to use:**
- User says "set up", "configure", "add", "enable", "connect" -> Mode 1
- User says "multiple", "both", "also add", "alongside" -> Mode 2
- User says "not working", "error", "can't log in", "redirect", "broken" -> Mode 3

## Reference Docs

Load these on demand -- only when the topic comes up:

| Topic | Load this file |
|-------|---------------|
| Which auth method to use | `${CLAUDE_PLUGIN_ROOT}/references/auth-overview.md` |
| Generic OIDC setup | `${CLAUDE_PLUGIN_ROOT}/references/oauth2-oidc-setup.md` |
| Azure AD / Entra ID | `${CLAUDE_PLUGIN_ROOT}/references/provider-azure-ad.md` |
| Google OAuth | `${CLAUDE_PLUGIN_ROOT}/references/provider-google.md` |
| GitHub OAuth | `${CLAUDE_PLUGIN_ROOT}/references/provider-github.md` |
| Other providers (Keycloak, Auth0, etc.) | `${CLAUDE_PLUGIN_ROOT}/references/provider-other.md` |
| LDAP / Active Directory | `${CLAUDE_PLUGIN_ROOT}/references/ldap-setup.md` |
| SMTP / email verification | `${CLAUDE_PLUGIN_ROOT}/references/email-config.md` |
| Auth troubleshooting | `${CLAUDE_PLUGIN_ROOT}/references/auth-troubleshooting.md` |

## Templates

Ready-to-use `.env` templates the user can copy and fill in:

| Template | Use when |
|----------|----------|
| `${CLAUDE_PLUGIN_ROOT}/templates/env-oauth-azure.template` | Setting up Azure AD / Entra ID |
| `${CLAUDE_PLUGIN_ROOT}/templates/env-oauth-google.template` | Setting up Google OAuth |
| `${CLAUDE_PLUGIN_ROOT}/templates/env-oauth-generic.template` | Setting up any OIDC provider |
| `${CLAUDE_PLUGIN_ROOT}/templates/auth-checklist.md` | Pre-flight verification before going live |

## Proactive Triggers

Surface these WITHOUT being asked when you notice them in the user's config:

1. **Missing JWT_SECRET** -> "JWT_SECRET is required for session management. Without it, user sessions will not work. Generate one with: `openssl rand -hex 32`"

2. **Missing CREDS_KEY or CREDS_IV** -> "CREDS_KEY and CREDS_IV are required for LibreChat to start. Without them, the app will crash. Generate with: `openssl rand -hex 32` for CREDS_KEY and `openssl rand -hex 16` for CREDS_IV."

3. **OAuth callback URL using HTTP in production** -> "Your redirect URI uses http:// but most OAuth providers require https:// in production. This will cause a redirect URI mismatch error."

4. **ALLOW_REGISTRATION=true without domain restriction** -> "Open registration is enabled with no `allowedDomains` in librechat.yaml. Anyone can create an account. Consider restricting to your organization's email domain."

5. **OPENID and SAML both configured** -> "Both OpenID and SAML variables are set. LibreChat will use OpenID and ignore SAML. Only one can be active at a time."

6. **Social login vars set but ALLOW_SOCIAL_LOGIN not true** -> "OAuth provider variables are configured but ALLOW_SOCIAL_LOGIN is not set to true. The social login button will not appear on the login page."

7. **Email service not configured** -> Check `ALLOW_PASSWORD_RESET` before warning. If `ALLOW_PASSWORD_RESET=false`, say: "No email service (SMTP or Mailgun) is configured. Email verification for new accounts is unavailable. Password resets are disabled, so the insecure reset method is not exposed." If `ALLOW_PASSWORD_RESET` is true or unset, say: "No email service (SMTP or Mailgun) is configured. Password resets will use the INSECURE reset method that allows anyone to reset any password without email verification."

## Output Format

Every auth configuration you produce MUST include:

1. **`.env` variables** -- complete, copy-pasteable, with placeholder values clearly marked
2. **Provider-side steps** -- what to configure in the identity provider's admin console
3. **Restart command** -- how to apply the change
4. **Verification** -- how to confirm login works (usually: open incognito window, check login page)

## When to Use This Skill vs Others

- **auth vs access-control (librechat-security):** Setting up login and identity -> use auth. Controlling what logged-in users can do -> use access-control.
- **auth vs config (librechat-core):** Configuring `.env` auth variables -> use auth. Configuring `librechat.yaml` endpoints and models -> use config.
- **auth vs deployment (librechat-ops):** Auth provider setup and `.env` variables -> use auth. Reverse proxy, SSL certificates, DNS -> use deployment.
