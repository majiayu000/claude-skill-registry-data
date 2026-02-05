---
name: goth-providers
description: This skill should be used when the user asks to "add a provider", "configure google oauth", "set up microsoft login", "azure ad authentication", "oauth provider setup", "add social login", or needs help with specific OAuth provider configuration in Goth.
---

# Goth Providers

Expert guidance for configuring OAuth providers with github.com/markbates/goth. Focus on Google and Microsoft (Azure AD) with patterns applicable to all 70+ supported providers.

## Provider Registration Pattern

Register providers at application startup using `goth.UseProviders()`:

```go
import (
    "github.com/markbates/goth"
    "github.com/markbates/goth/providers/google"
    "github.com/markbates/goth/providers/azureadv2"
)

func init() {
    goth.UseProviders(
        google.New(
            os.Getenv("GOOGLE_CLIENT_ID"),
            os.Getenv("GOOGLE_CLIENT_SECRET"),
            "http://localhost:3000/auth/google/callback",
            "email", "profile",
        ),
        azureadv2.New(
            os.Getenv("AZURE_CLIENT_ID"),
            os.Getenv("AZURE_CLIENT_SECRET"),
            "http://localhost:3000/auth/microsoft/callback",
            azureadv2.ProviderOptions{
                Tenant: azureadv2.CommonTenant,
                Scopes: []string{"openid", "profile", "email"},
            },
        ),
    )
}
```

## Provider Constructor Pattern

All providers follow a similar constructor pattern:

```go
provider.New(
    clientID string,      // OAuth client/application ID
    clientSecret string,  // OAuth client secret
    callbackURL string,   // Your callback URL (must match provider config)
    scopes ...string,     // Permission scopes to request
)
```

## Callback URL Configuration

The callback URL must:
1. Match exactly what's registered in the provider's developer console
2. Be accessible from the user's browser
3. Handle the OAuth callback response

```go
// Development
callbackURL := "http://localhost:3000/auth/google/callback"

// Production
callbackURL := "https://yourdomain.com/auth/google/callback"

// Dynamic based on environment
func getCallbackURL(provider string) string {
    baseURL := os.Getenv("BASE_URL")
    if baseURL == "" {
        baseURL = "http://localhost:3000"
    }
    return fmt.Sprintf("%s/auth/%s/callback", baseURL, provider)
}
```

## Scopes Reference

### Common Scopes

| Scope | Purpose |
|-------|---------|
| `openid` | OpenID Connect authentication |
| `email` | Access user's email address |
| `profile` | Access basic profile info (name, picture) |

### Provider-Specific Scopes

Request only scopes needed for your application. More scopes = more user friction.

## Google OAuth Setup

### Console Configuration

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project or select existing
3. Enable "Google+ API" or "People API"
4. Configure OAuth consent screen
5. Create OAuth 2.0 credentials (Web application)
6. Add authorized redirect URIs

### Code Configuration

```go
import "github.com/markbates/goth/providers/google"

google.New(
    os.Getenv("GOOGLE_CLIENT_ID"),
    os.Getenv("GOOGLE_CLIENT_SECRET"),
    "http://localhost:3000/auth/google/callback",
    "email", "profile", // Common scopes
)
```

### Google-Specific Scopes

| Scope | Data Access |
|-------|-------------|
| `email` | Email address |
| `profile` | Name, picture, locale |
| `https://www.googleapis.com/auth/calendar.readonly` | Read calendars |
| `https://www.googleapis.com/auth/drive.readonly` | Read Drive files |

### Access User Data

```go
user, _ := gothic.CompleteUserAuth(w, r)
// user.Email - Google email
// user.Name - Display name
// user.AvatarURL - Profile picture
// user.AccessToken - For Google API calls
```

For detailed Google setup steps, see `references/google-oauth-setup.md`.

## Microsoft (Azure AD) Setup

### Azure Portal Configuration

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to Azure Active Directory → App registrations
3. Create new registration
4. Add redirect URI (Web platform)
5. Create client secret under Certificates & secrets
6. Configure API permissions

### Code Configuration

```go
import "github.com/markbates/goth/providers/azureadv2"

azureadv2.New(
    os.Getenv("AZURE_CLIENT_ID"),
    os.Getenv("AZURE_CLIENT_SECRET"),
    "http://localhost:3000/auth/microsoft/callback",
    azureadv2.ProviderOptions{
        Tenant: azureadv2.CommonTenant, // or specific tenant ID
        Scopes: []string{
            "openid",
            "profile",
            "email",
        },
    },
)
```

### Tenant Options

```go
// Any Microsoft account (personal + work/school)
Tenant: azureadv2.CommonTenant

// Only work/school accounts
Tenant: azureadv2.OrganizationsTenant

// Only personal Microsoft accounts
Tenant: azureadv2.ConsumersTenant

// Specific organization only
Tenant: "your-tenant-id"
```

### Microsoft-Specific Scopes

| Scope | Data Access |
|-------|-------------|
| `openid` | ID token |
| `profile` | Name, preferred_username |
| `email` | Email address |
| `User.Read` | Full profile via Graph API |
| `Calendars.Read` | Read calendar events |
| `Files.Read` | Read OneDrive files |

### Access User Data

```go
user, _ := gothic.CompleteUserAuth(w, r)
// user.Email - Microsoft email
// user.Name - Display name
// user.UserID - Azure AD object ID
// user.AccessToken - For Microsoft Graph API calls
// user.IDToken - JWT with claims
```

For detailed Microsoft setup steps, see `references/microsoft-oauth-setup.md`.

## Multiple Providers Pattern

Support multiple login options:

```go
func init() {
    goth.UseProviders(
        google.New(
            os.Getenv("GOOGLE_CLIENT_ID"),
            os.Getenv("GOOGLE_CLIENT_SECRET"),
            getCallbackURL("google"),
            "email", "profile",
        ),
        azureadv2.New(
            os.Getenv("AZURE_CLIENT_ID"),
            os.Getenv("AZURE_CLIENT_SECRET"),
            getCallbackURL("microsoft"),
            azureadv2.ProviderOptions{
                Tenant: azureadv2.CommonTenant,
                Scopes: []string{"openid", "profile", "email"},
            },
        ),
    )
}

// Login page template
const loginTemplate = `
<h1>Sign In</h1>
<a href="/auth/google">Sign in with Google</a>
<a href="/auth/microsoft">Sign in with Microsoft</a>
`
```

## Provider Selection at Runtime

Get available providers:

```go
// List all registered providers
providers := goth.GetProviders()
for name, provider := range providers {
    fmt.Printf("Provider: %s\n", name)
}

// Get specific provider
provider, err := goth.GetProvider("google")
if err != nil {
    // Provider not registered
}
```

## Custom Provider Name

Override the provider name if needed:

```go
// In your route handler
gothic.GetProviderName = func(req *http.Request) (string, error) {
    // Extract from URL path: /auth/{provider}
    parts := strings.Split(req.URL.Path, "/")
    if len(parts) >= 3 {
        return parts[2], nil
    }
    return "", errors.New("no provider specified")
}
```

## Environment Variables

Organize credentials by provider:

```bash
# Google OAuth
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxx

# Microsoft/Azure AD
AZURE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_CLIENT_SECRET=xxx~xxx
AZURE_TENANT_ID=common  # or specific tenant

# Application
BASE_URL=http://localhost:3000
SESSION_SECRET=your-32-byte-secret
```

## Common Issues

### "redirect_uri_mismatch" Error

The callback URL doesn't match provider configuration:
- Check exact URL including protocol (http vs https)
- Verify trailing slashes match
- Ensure port number is correct
- Check for localhost vs 127.0.0.1 differences

### "invalid_client" Error

Client ID or secret is wrong:
- Verify environment variables are loaded
- Check for extra whitespace in credentials
- Ensure correct project/app is selected in console

### "access_denied" Error

User denied permission or scopes are invalid:
- Review requested scopes
- Check consent screen configuration
- Verify app is published (if Google)

## Quick Reference

| Task | Code |
|------|------|
| Register provider | `goth.UseProviders(provider)` |
| Get provider | `goth.GetProvider("name")` |
| List providers | `goth.GetProviders()` |
| Dynamic callback | `fmt.Sprintf("%s/auth/%s/callback", baseURL, provider)` |

## Related Skills

- **goth-fundamentals** - Core Goth concepts and interfaces
- **goth-echo-security** - Framework integration and security

## Reference Documentation

- `references/google-oauth-setup.md` - Step-by-step Google configuration
- `references/microsoft-oauth-setup.md` - Step-by-step Microsoft/Azure AD configuration
